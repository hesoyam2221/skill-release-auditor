# Skill Release Auditor

A local OpenClaw skill that audits another skill directory for release readiness.

## What it can do in this MVP
- audit a local skill or skill-like project directory
- detect README vs file-tree mismatches
- detect broken installer file references
- flag broad file/path access heuristics that need human review
- flag missing tests
- flag release contamination like `.git/`
- generate:
  - `findings.json`
  - `status.md`
  - `launch-checklist.md`
  - `handoff.md`

## What it cannot do yet
- fully understand code semantics
- automatically fix upstream source code
- generate perfect documentation rewrites from code
- publish to ClawHub directly
- replace real human QA judgment

## MVP status
This is an honest MVP. It is useful now for local release audits, but it still relies on heuristics and is best used as a release reviewer assistant, not as a final authority.

## Example usage
```bash
python3 scripts/audit_skill.py /path/to/skill --output-dir /path/to/output --collaborator Heso
```

## Example output
The audit writes:
- `findings.json`
- `status.md`
- `launch-checklist.md`
- `handoff.md`

## Best fit
- skill authors preparing a beta release
- collaborators doing QA/release work
- ClawHub launch prep

## Current limitations
- local directory only
- no package/build-system integration yet
- static heuristics only
- smoke-test expectations still need human confirmation

## Release stance
Ship as beta.
Do not market as a complete semantic verifier.
Market it as a practical release-audit assistant for OpenClaw skills.
