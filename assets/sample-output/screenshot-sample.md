# Release Audit — demo-skill

- **Project status:** 68%
- **Verdict:** beta possible with blockers

## What works
- Package contains implementation code files
- Package contains README.md
- Package contains SKILL.md
- Package contains an installer script

## Findings
- **P0 — Installer references missing file**
  - Installer references `skill_helper.py` but it is not present in the package.
  - Source: `install.sh`

- **P0 — README claims missing file or directory**
  - README mentions `server/` but it was not found in the package.
  - Source: `README.md`

- **P1 — No visible tests or smoke harness**
  - No tests/ directory or obvious test files were found.
  - Source: `demo-skill/`

- **P1 — Release tree contains non-release artifacts**
  - Found: `.git`
  - Source: `demo-skill/`
