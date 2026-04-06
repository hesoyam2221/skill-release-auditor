# Launch Checklist

## P0
- Installer references missing file: Installer references `skill_helper.py` but it is not present in the package.
- README claims missing file or directory: README mentions `server/` but it was not found in the package.
- README describes HTTP/server architecture not found in code: README appears to describe a local HTTP bridge, but no matching HTTP implementation was detected in code.
- Potentially broad file/path access without containment checks: Code appears to read local file paths with no visible resolve/containment boundary.

## P1
- Release tree contains non-release artifacts: Found: `.git`
- No visible tests or smoke harness: No tests/ directory or obvious test files were found.

## P2
- None
