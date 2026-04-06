---
name: skill-release-auditor
description: Audit an OpenClaw skill or local skill-like project for release readiness, packaging integrity, README-vs-code mismatches, broken installer references, unsafe file/path handling, missing tests, release contamination, and ClawHub beta launch blockers. Use when reviewing a skill before shipping, creating a launch checklist, generating a teammate handoff, or turning a manual QA/release review into a repeatable audit.
---

# Skill Release Auditor

Use this skill when a local skill directory needs a release-readiness audit.

## Workflow

1. Resolve the target directory.
2. Run `scripts/audit_skill.py` against it.
3. Review the generated findings.
4. If the user wants artifact files, render:
   - status report
   - launch checklist
   - teammate handoff
5. Keep the audit read-only by default.

## Scripts

- `scripts/audit_skill.py` — deterministic scanner and report writer

## Expected outputs

The script can generate:
- `status.md`
- `launch-checklist.md`
- `handoff.md`
- `findings.json`

## References

- Read `references/checklists.md` for severity rules and beta launch criteria.
- Read `references/finding-patterns.md` for how specific findings should be interpreted.
