# Smoke Test

## Goal
Verify that the MVP can audit a local skill and write output files.

## Command
```bash
python3 scripts/audit_skill.py /path/to/skill --output-dir /tmp/skill-audit-output --collaborator Demo
```

## Expected
- JSON summary printed to stdout
- output directory created
- files written:
  - `findings.json`
  - `status.md`
  - `launch-checklist.md`
  - `handoff.md`

## Verified local example
Test target used during development:
- `/path/to/example-skill`

Expected high-signal findings on that target:
- README mismatch
- broken installer reference
- missing tests
- release contamination
- unsafe file access heuristics
