<div align="center">

# Skill Release Auditor

**Catch security issues in OpenClaw skills before they ship.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0--beta-blue.svg)]()
[![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.4+-red.svg)]()

</div>

## Why?

- **341** malicious skills found on ClawHub (ClawHavoc, 2026)
- **47%** of all skills have at least one security issue (Snyk)
- **21,000+** OpenClaw instances exposed online (Censys)
- **CVE-2026-25253** — Remote code execution via Gateway

## What It Checks

| Check | Severity | Description |
|-------|----------|-------------|
| README/code mismatch | P0 | README describes different functionality than code |
| Broken installer refs | P0 | install.sh references missing files |
| Unsafe file access | P0 | file: paths without containment |
| Missing tests | P1 | No unit or smoke tests |
| Release contamination | P1 | .git/, .env, __pycache__ in release |

## Quick Start
```bash
git clone https://github.com/hesoyam2221/skill-release-auditor.git
cd skill-release-auditor
python3 scripts/audit_skill.py /path/to/your/skill
```

## Professional Audits

| Package | Price | Includes |
|---------|-------|----------|
| Basic | $50 | Core audit + report |
| Standard | $100 | Full hardening + 3 skill checks |
| Premium | $150 | Deep audit + priority support |

**Platform:** https://dos-kde-jun-beyond.trycloudflare.com
**Fiverr:** https://www.fiverr.com/hesoyam2221

## Links

- [Auth Recovery Assistant](https://github.com/hesoyam2221/auth-recovery-assistant)
- [YouTube — ClawSafe](https://youtube.com/@ClawSafe)
- [Twitter](https://x.com/MaximusDev1094)

*Built by ClawSafe — Security + Audit for OpenClaw AI Agents*
