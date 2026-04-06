# Release Audit Checklists

## P0 hard blockers
- README materially misrepresents the implementation
- installer references files that do not exist
- unsafe file access behavior for a beta skill with no clear boundary
- no realistic install/smoke validation path for release artifact

## P1 serious issues
- no tests or smoke coverage
- release tree contains `.git/` or obvious junk
- SKILL.md and README are inconsistent
- platform constraints not documented honestly

## P2 polish issues
- missing screenshots plan
- weak listing metadata
- unclear roadmap / support boundaries

## Beta minimum
- honest README
- coherent installer
- bounded or documented risk areas
- at least one smoke-test path
- clean release tree
