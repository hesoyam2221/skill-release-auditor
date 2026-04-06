# Skill Release Auditor

Audit an OpenClaw skill before launch.

Skill Release Auditor is a local MVP tool that checks a skill directory for:
- README vs code mismatches
- broken installer references
- unsafe file/path access heuristics
- missing tests or smoke coverage
- release contamination like `.git/`
- beta launch blockers

It then generates:
- `findings.json`
- `status.md`
- `launch-checklist.md`
- `handoff.md`

## Why this exists
OpenClaw skills are getting more ambitious, but a lot of them still ship with the same avoidable launch problems: docs that describe a different system than the code, installers that reference missing files, no smoke tests, and weak beta safety boundaries.

This tool exists to catch that before release.

## MVP status
This is the free MVP version.

It is useful today, but it is still heuristic-based:
- it does not fully understand code semantics
- it does not auto-fix upstream code
- it does not replace human QA judgment

## Install from GitHub

### Option 1 — clone the repo/package
```bash
git clone <YOUR-GITHUB-REPO-URL>
cd skill-release-auditor
```

### Option 2 — copy into OpenClaw skills manually
If you want it inside your OpenClaw skills directory:
```bash
cp -r skill-release-auditor ~/.openclaw/skills/
```

## Manual usage
Run the auditor directly:

```bash
python3 scripts/audit_skill.py /path/to/skill --output-dir /path/to/output --collaborator Demo
```

Example:
```bash
python3 scripts/audit_skill.py ~/.openclaw/skills/my-skill --output-dir ~/skill-audit-output --collaborator Teammate
```

## Output files
The audit writes:
- `findings.json`
- `status.md`
- `launch-checklist.md`
- `handoff.md`

## Good fit
- skill authors preparing a beta release
- collaborators doing QA for another builder
- OpenClaw users preparing a GitHub or ClawHub release

## Current limitations
- local directory audit only
- deterministic checks + heuristics only
- no automatic patching yet
- no generated README rewrites yet
- no generated test scaffold yet

## Roadmap
### Free
- stronger finding rules
- better report quality
- more packaging checks

### Pro
- auto-fix suggestions
- README rewrite drafts
- test scaffold generation
- team handoff packs
- release scorecards

## License
Choose a license before public push. MIT is the simplest default if you want maximum adoption.
