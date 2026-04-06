# ClawHub Listing Draft — Skill Release Auditor

## Title
Skill Release Auditor

## Short description
Audit an OpenClaw skill for launch blockers, README/code mismatches, broken installer references, unsafe file-access patterns, missing tests, and ClawHub beta readiness.

## Category
Developer Tools / QA / Release Engineering

## Tags
- openclaw
- skill-audit
- qa
- release
- clawhub
- packaging
- docs
- installer
- beta-launch

## Long description
Skill Release Auditor is a local OpenClaw skill for authors who want a fast, honest release-readiness review before shipping a skill.

Point it at a skill directory and it will inspect the package for common launch failures such as README claims that do not match the real files, installer references to missing files, unsafe local file-access patterns, missing tests, and release contamination like `.git/` directories.

This is not a semantic verifier and it does not auto-fix the audited project. It is an MVP release-audit assistant that turns manual QA instincts into a repeatable report with a status summary, launch checklist, teammate handoff, and structured findings JSON.

Best for:
- skill authors preparing a beta release
- collaborators doing QA for another builder
- ClawHub listing preparation
- fast packaging sanity checks before publishing

## Honest beta note
This is an MVP. It uses deterministic checks plus heuristics. It should guide release work, not replace human judgment.

## Suggested screenshots
1. terminal run of `audit_skill.py`
2. generated `status.md`
3. generated `launch-checklist.md`
4. generated `handoff.md`
