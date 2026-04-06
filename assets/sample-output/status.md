# Release Audit — example-skill

- **Project status:** 55%
- **Verdict:** not ready

## What works
- Package contains implementation code files
- Package contains an installer script
- Package contains README.md
- Package contains SKILL.md

## Findings
- **P1 — Release tree contains non-release artifacts**
  - Found: `.git`
  - Source: `example-skill/`
- **P1 — No visible tests or smoke harness**
  - No tests/ directory or obvious test files were found.
  - Source: `example-skill/`
- **P0 — Installer references missing file**
  - Installer references `skill_helper.py` but it is not present in the package.
  - Source: `example-skill/install.sh`
- **P0 — README claims missing file or directory**
  - README mentions `server/` but it was not found in the package.
  - Source: `example-skill/README.md`
- **P0 — README describes HTTP/server architecture not found in code**
  - README appears to describe a local HTTP bridge, but no matching HTTP implementation was detected in code.
  - Source: `example-skill/README.md`
- **P0 — Potentially broad file/path access without containment checks**
  - Code appears to read local file paths with no visible resolve/containment boundary.
  - Source: `example-skill/`
