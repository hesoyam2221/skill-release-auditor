# Finding Patterns

## Documentation mismatch
Examples:
- README claims files that are absent
- README claims HTTP server but no HTTP implementation exists
- README claims cross-platform support but code is clearly platform-specific

## Installer breakage
Examples:
- `cp` source file missing
- installer writes files never mentioned in docs
- installer requires files outside release artifact

## Safety / risk
Examples:
- `file:` pattern with `expanduser()` and no containment checks
- subprocess-heavy automation with weak documentation of limits
- browser automation with no stated fragility note

## Test readiness
Examples:
- no `tests/` directory
- no smoke steps in README
- no sample prompt or usage validation flow

## Release hygiene
Examples:
- `.git/` present
- caches, temp files, secrets, logs shipped in release tree
