#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

DOC_FILES = ["README.md", "SKILL.md"]
INSTALLER_NAMES = ["install.sh", "install.py", "setup.sh"]
CODE_EXTS = {".py", ".sh", ".js", ".ts", ".mjs", ".cjs"}
JUNK_DIRS = {".git", ".pytest_cache", "__pycache__", ".mypy_cache", ".ruff_cache", ".DS_Store"}
HTTP_HINTS = ["http.server", "aiohttp", "fastapi", "flask", "localhost:7700", "/v1/chat", "bridge listening on http"]
PLAYWRIGHT_HINTS = ["playwright", "cdp", "chromium"]
APPLE_ONLY_HINTS = ["osascript", "Google Chrome", "pbcopy", "System Events"]
FILE_RISK_HINTS = ["file:", "expanduser()", "read_text(", "open("]
CONTAINMENT_HINTS = ["resolve(", "relative_to(", "is_relative_to("]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def list_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for p in root.rglob("*"):
        files.append(p)
    return files


def find_main_code_files(root: Path) -> list[Path]:
    out = []
    for p in root.rglob("*"):
        if p.is_file() and p.suffix in CODE_EXTS and ".git" not in p.parts:
            out.append(p)
    return sorted(out)


def detect_installer_refs(installer_text: str) -> list[str]:
    refs = set()
    for raw_line in installer_text.splitlines():
        line = raw_line.strip()
        if not line.startswith("cp "):
            continue

        for match in re.finditer(r'\$\(dirname "\$0"\)/([^"\s]+)', line):
            refs.add(match.group(1))
        for match in re.finditer(r'\$\(dirname \"\$0\"\)/([^"\s]+)', line):
            refs.add(match.group(1))

        quoted = re.findall(r'"([^"]+)"', line)
        for q in quoted:
            if q.startswith("$(dirname"):
                continue
            if q.startswith("~/") or q.startswith("/"):
                continue
            if "/" not in q or q.startswith("."):
                refs.add(q)

    return sorted(x for x in refs if x and x not in {"$(dirname", "$0"})


def severity_from_tag(tag: str) -> str:
    if tag in {"readme_mismatch", "installer_missing_file", "unsafe_file_access"}:
        return "P0"
    if tag in {"no_tests", "release_contamination", "skill_readme_inconsistency"}:
        return "P1"
    return "P2"


def add_finding(findings: list[dict[str, Any]], tag: str, title: str, detail: str, source: str) -> None:
    findings.append({
        "tag": tag,
        "severity": severity_from_tag(tag),
        "title": title,
        "detail": detail,
        "source": source,
    })


def audit(root: Path) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    all_paths = list_files(root)
    files = [p for p in all_paths if p.is_file()]
    dirs = [p for p in all_paths if p.is_dir()]

    rel_files = [str(p.relative_to(root)) for p in files]
    rel_dirs = [str(p.relative_to(root)) for p in dirs]

    readme = root / "README.md"
    skill = root / "SKILL.md"
    installer = next((root / name for name in INSTALLER_NAMES if (root / name).exists()), None)
    code_files = find_main_code_files(root)
    code_text = "\n\n".join(read_text(p) for p in code_files[:20])
    readme_text = read_text(readme)
    skill_text = read_text(skill)
    installer_text = read_text(installer) if installer else ""

    if any((root / junk).exists() for junk in JUNK_DIRS):
        junk_found = [junk for junk in JUNK_DIRS if (root / junk).exists()]
        add_finding(findings, "release_contamination", "Release tree contains non-release artifacts", f"Found: {', '.join(junk_found)}", str(root))

    tests_present = (root / "tests").exists() or any("test" in p.name.lower() for p in files)
    if not tests_present:
        add_finding(findings, "no_tests", "No visible tests or smoke harness", "No tests/ directory or obvious test files were found.", str(root))

    if installer:
        refs = detect_installer_refs(installer_text)
        missing = [ref for ref in refs if not (root / ref).exists()]
        for ref in missing:
            add_finding(findings, "installer_missing_file", "Installer references missing file", f"Installer references `{ref}` but it is not present in the package.", str(installer))

    if readme_text:
        for claimed in ["bridge.py", "config.yaml", "requirements.txt", "skill.yaml", "core/", "server/", "tests/"]:
            if claimed in readme_text and not (root / claimed.rstrip('/')).exists():
                add_finding(findings, "readme_mismatch", "README claims missing file or directory", f"README mentions `{claimed}` but it was not found in the package.", str(readme))

        readme_claims_http = any(hint in readme_text.lower() for hint in [h.lower() for h in HTTP_HINTS])
        code_has_http = any(hint in code_text.lower() for hint in [h.lower() for h in HTTP_HINTS])
        readme_claims_playwright = any(hint in readme_text.lower() for hint in [h.lower() for h in PLAYWRIGHT_HINTS])
        code_has_playwright = any(hint in code_text.lower() for hint in [h.lower() for h in PLAYWRIGHT_HINTS])
        code_is_apple = any(hint.lower() in code_text.lower() for hint in APPLE_ONLY_HINTS)

        if readme_claims_http and not code_has_http:
            add_finding(findings, "readme_mismatch", "README describes HTTP/server architecture not found in code", "README appears to describe a local HTTP bridge, but no matching HTTP implementation was detected in code.", str(readme))
        if readme_claims_playwright and not code_has_playwright:
            add_finding(findings, "readme_mismatch", "README describes Playwright/CDP behavior not found in code", "README mentions Playwright/CDP-style automation, but matching implementation was not detected.", str(readme))
        if code_is_apple and ("linux" in readme_text.lower() or "windows" in readme_text.lower()):
            pass

    if skill_text and readme_text:
        if ("macos" in skill_text.lower()) != ("macos" in readme_text.lower()):
            add_finding(findings, "skill_readme_inconsistency", "SKILL.md and README differ on platform expectations", "Platform constraints appear inconsistently documented between SKILL.md and README.", str(skill))

    file_risk = any(h in code_text for h in FILE_RISK_HINTS)
    containment = any(h in code_text for h in CONTAINMENT_HINTS)
    if file_risk and not containment:
        add_finding(findings, "unsafe_file_access", "Potentially broad file/path access without containment checks", "Code appears to read local file paths with no visible resolve/containment boundary.", str(root))

    what_works = []
    if code_files:
        what_works.append("Package contains implementation code files")
    if installer:
        what_works.append("Package contains an installer script")
    if readme.exists():
        what_works.append("Package contains README.md")
    if skill.exists():
        what_works.append("Package contains SKILL.md")

    status_pct = 85
    if any(f["severity"] == "P0" for f in findings):
        status_pct = 55
    elif any(f["severity"] == "P1" for f in findings):
        status_pct = 70

    verdict = "marketplace ready"
    if any(f["severity"] == "P0" for f in findings):
        verdict = "not ready"
    elif any(f["severity"] == "P1" for f in findings):
        verdict = "beta possible with blockers"

    return {
        "target": str(root),
        "status_pct": status_pct,
        "verdict": verdict,
        "inventory": {
            "files": rel_files,
            "dirs": rel_dirs,
            "readme": readme.exists(),
            "skill": skill.exists(),
            "installer": str(installer.relative_to(root)) if installer else None,
            "tests_present": tests_present,
        },
        "what_works": what_works,
        "findings": findings,
    }


def render_status(audit_data: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Release Audit — {Path(audit_data['target']).name}")
    lines.append("")
    lines.append(f"- **Project status:** {audit_data['status_pct']}%")
    lines.append(f"- **Verdict:** {audit_data['verdict']}")
    lines.append("")
    lines.append("## What works")
    for item in audit_data["what_works"] or ["No positive signals detected."]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Findings")
    if not audit_data["findings"]:
        lines.append("- No major findings.")
    else:
        for f in audit_data["findings"]:
            lines.append(f"- **{f['severity']} — {f['title']}**")
            lines.append(f"  - {f['detail']}")
            lines.append(f"  - Source: `{f['source']}`")
    return "\n".join(lines) + "\n"


def render_checklist(audit_data: dict[str, Any]) -> str:
    lines = ["# Launch Checklist", ""]
    grouped = {"P0": [], "P1": [], "P2": []}
    for f in audit_data["findings"]:
        grouped[f["severity"]].append(f)
    for sev in ["P0", "P1", "P2"]:
        lines.append(f"## {sev}")
        if not grouped[sev]:
            lines.append("- None")
        else:
            for f in grouped[sev]:
                lines.append(f"- {f['title']}: {f['detail']}")
        lines.append("")
    return "\n".join(lines)


def render_handoff(audit_data: dict[str, Any], collaborator: str | None) -> str:
    name = collaborator or "Collaborator"
    lines = [f"# {name} handoff", "", "Based on a read-only release audit.", ""]
    for f in sorted(audit_data["findings"], key=lambda x: x["severity"]):
        lines.append(f"## {f['severity']} — {f['title']}")
        lines.append("### What")
        lines.append(f["title"])
        lines.append("")
        lines.append("### Why")
        lines.append(f["detail"])
        lines.append("")
        lines.append("### Source")
        lines.append(f"`{f['source']}`")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="Audit a skill directory for release readiness")
    ap.add_argument("target", help="Path to skill/project directory")
    ap.add_argument("--output-dir", help="Directory to write reports into")
    ap.add_argument("--collaborator", help="Name for handoff generation")
    args = ap.parse_args()

    root = Path(args.target).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Target directory does not exist: {root}")

    data = audit(root)
    out_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else None

    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "findings.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
        (out_dir / "status.md").write_text(render_status(data), encoding="utf-8")
        (out_dir / "launch-checklist.md").write_text(render_checklist(data), encoding="utf-8")
        (out_dir / "handoff.md").write_text(render_handoff(data, args.collaborator), encoding="utf-8")

    print(json.dumps({
        "target": data["target"],
        "status_pct": data["status_pct"],
        "verdict": data["verdict"],
        "findings_count": len(data["findings"]),
        "p0": sum(1 for f in data["findings"] if f["severity"] == "P0"),
        "p1": sum(1 for f in data["findings"] if f["severity"] == "P1"),
        "p2": sum(1 for f in data["findings"] if f["severity"] == "P2"),
        "output_dir": str(out_dir) if out_dir else None,
    }, indent=2))


if __name__ == "__main__":
    main()
