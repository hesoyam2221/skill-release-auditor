# Skill Release Auditor — Build Spec

## Purpose

Skill Release Auditor is an OpenClaw skill that audits another skill directory for launch readiness.

Its job is to catch exactly the class of failures found in a real release QA audit, including:
- README does not match the real implementation
- installer references missing files
- unsafe file/path behavior
- missing tests or smoke validation
- release contamination (`.git/`, temp files, secrets, junk)
- weak ClawHub listing readiness
- packaging inconsistency between SKILL.md, installer, code, and shipped files

This skill is designed to produce a clear, actionable release report and a prioritized fix list without modifying the audited project by default.

---

## What the skill does

### Core features

#### 1. Skill directory inventory
- scans the target skill directory
- lists key files present and missing
- identifies scripts, references, assets, tests, installer files, and metadata files
- detects release contamination such as `.git/`, temporary files, caches, or stray local artifacts

#### 2. Documentation vs implementation audit
- reads `README.md`, `SKILL.md`, installer files, and core code files
- compares documented architecture and usage claims against the actual file tree and code behavior
- flags mismatches such as:
  - README mentions files that do not exist
  - README claims HTTP server but code only implements file bridge
  - docs claim cross-platform support but code is platform-specific

#### 3. Installer audit
- inspects install scripts (`install.sh`, similar scripts)
- checks whether referenced files actually exist
- checks whether installation steps match the actual package structure
- reports broken copy commands, stale references, and misleading setup instructions

#### 4. Safety and risk audit
- searches for patterns such as:
  - broad file reads (`expanduser`, unrestricted `Path(...)`, `open(...)`, `read_text(...)`)
  - missing containment checks (`resolve`, `relative_to`, `is_relative_to`)
  - shell execution / subprocess usage
  - browser/UI automation fragility indicators
  - dangerous defaults not clearly documented
- produces a beta safety verdict, not just raw pattern matches

#### 5. Test readiness audit
- detects presence or absence of:
  - `tests/`
  - smoke-test scripts
  - example files usable for validation
  - install verification steps in docs
- reports whether the package has enough validation for an honest beta

#### 6. ClawHub launch readiness audit
- checks for listing-ready components:
  - README
  - SKILL.md
  - screenshots/assets folder or documented screenshot plan
  - release package cleanliness
  - honest positioning and constraints
- reports whether the package is launch-ready, beta-only, or blocked

#### 7. Prioritized release checklist generation
- produces a sorted list of blockers by launch impact
- labels tasks by severity:
  - P0 hard blocker
  - P1 serious issue
  - P2 polish / confidence issue
- optionally separates:
  - tasks the current operator can do autonomously
  - tasks that require the upstream/canonical owner

#### 8. Handoff generation
- generates a collaborator handoff similar to the `heso-handoff.md` pattern
- per task includes:
  - what
  - why
  - how
  - priority

---

## Input

The user provides one or more of the following:

### Required input
- path to the skill directory to audit

Example:
- `Audit ~/projects/my-skill for release readiness`
- `Review ~/.openclaw/skills/my-skill and prepare a launch checklist`

### Optional inputs
- target release stage:
  - local draft
  - beta
  - audited beta
  - marketplace / ClawHub release
- output directory for reports
- collaborator name for handoff generation
- whether the audit should be read-only or may propose patches only in a separate workspace
- whether to generate follow-up artifacts:
  - release checklist
  - handoff file
  - README rewrite draft
  - installer-fix notes
  - test draft
  - listing prep

### Example request
"Audit `~/projects/skill-x` for ClawHub beta readiness. Output a status report, prioritized checklist, installer-fix notes, and a teammate handoff into `~/audit-output/`. Read-only only."

---

## Output

The skill returns a structured audit plus optional artifact files.

### Primary output
A status report with sections like:
- Project status (% complete, release stage estimate)
- What works
- What is missing
- QA findings
- Bugs / risks
- Launch blockers
- Recommendation and realistic launch timeline

### Optional generated artifacts
- `status.md`
- `launch-checklist.md`
- `handoff.md`
- `README-beta-draft.md`
- `installer-fix-notes.md`
- `tests-draft.md`
- `listing-prep.md`

### Verdict labels
- `not ready`
- `beta possible with blockers`
- `audited beta ready`
- `marketplace ready`

---

## Technical architecture

## High-level flow

1. Resolve the target skill path
2. Inventory the directory tree
3. Read high-signal files:
   - `SKILL.md`
   - `README.md`
   - installer script(s)
   - main implementation files
   - tests if present
4. Run heuristic checks:
   - missing-file references
   - doc/code mismatches
   - unsafe path handling
   - subprocess/browser fragility indicators
   - missing tests
   - release contamination
5. Score findings by severity
6. Generate human-readable reports and optional structured JSON
7. Optionally generate derived launch artifacts

## Detection model

The auditor should combine:
- deterministic file existence checks
- simple static code heuristics
- rule-based documentation consistency checks
- packaging/release hygiene checks

It should not pretend to fully understand semantics when it only has heuristics. It should label findings as:
- confirmed
- likely
- needs human verification

## Suggested implementation pieces

### `scripts/audit_skill.py`
Main deterministic auditor.

Responsibilities:
- walk the skill directory
- detect core files
- inspect install scripts for referenced filenames
- inspect code for path and subprocess patterns
- emit JSON findings

### `references/checklists.md`
Audit rules and release criteria.

Examples:
- beta minimum requirements
- ClawHub launch criteria
- README honesty rules
- installer validity rules

### `references/finding-patterns.md`
Maps specific findings to severity and suggested remediation.

Examples:
- missing installer file reference -> P0
- `.git/` included in release tree -> P1
- no tests -> P1
- platform-specific code but vague docs -> P0/P1 depending on claims

### `scripts/render_report.py` or in-skill rendering logic
Converts findings JSON into:
- status report
- checklist
- handoff
- optional README/test/listing drafts

---

## Scope for v1 (MVP)

The MVP should deliver real value with a narrow, reliable core.

### v1 must do
- audit one local skill directory
- inventory files and detect missing expected files
- read `README.md`, `SKILL.md`, installer script(s), and main code files
- detect broken installer references
- detect obvious doc/code mismatches
- detect broad `file:` / path-read risk patterns
- detect missing tests
- detect release contamination (`.git/`)
- output:
  - status report
  - prioritized launch checklist
  - teammate handoff

### v1 should not try to do
- full semantic program verification
- auto-fix upstream source code
- package publishing
- screenshot generation
- runtime browser-driven validation of third-party UIs

### Why this MVP is enough
Because it already automates the most painful and repeated release-review work:
- is the package coherent?
- is the installer broken?
- are the docs lying?
- is it safe enough for beta?
- what must be fixed first?

That alone is highly valuable.

---

## v2 / Premium features

### 1. Auto-generated rewrite drafts
- README rewrite draft based on real code inventory
- corrected SKILL.md suggestions
- listing copy draft

### 2. Test scaffold generation
- generate pytest skeletons for parser/path/install checks
- generate smoke-test checklist or scripts

### 3. Structured scorecard
- launch score from 0 to 100
- sub-scores:
  - docs honesty
  - installer integrity
  - safety
  - test maturity
  - listing readiness

### 4. Multi-skill batch mode
- audit a folder of skills and rank them by readiness

### 5. Marketplace optimization mode
- suggest better title, tags, positioning, screenshot plan, pricing posture

### 6. Secret leakage scan
- look for likely tokens, credentials, and unsafe release artifacts

### 7. CI/export mode
- produce machine-readable JSON for GitHub Actions or other automation

---

## Estimated build effort

### MVP
- **2 to 4 days**

Breakdown:
- day 1: skill scaffolding, file inventory, core audit rules
- day 2: doc/code mismatch checks, installer checks, report rendering
- day 3: checklist + handoff generation, refine severity rules
- day 4: optional polish, test on 2 to 3 real skills

### v2 / premium layer
- **additional 3 to 7 days** depending on rewrite automation and scaffold generation depth

---

## File structure of the skill

```text
skill-release-auditor/
├── SKILL.md
├── scripts/
│   ├── audit_skill.py
│   ├── render_report.py
│   └── common.py
├── references/
│   ├── checklists.md
│   ├── finding-patterns.md
│   └── reporting-templates.md
└── assets/
    └── sample-output/
        ├── status.md
        ├── checklist.md
        └── handoff.md
```

### File responsibilities

#### `SKILL.md`
- trigger description
- workflow instructions
- when to read which references
- how to use scripts and outputs

#### `scripts/audit_skill.py`
- runs deterministic scans
- emits JSON-like findings model

#### `scripts/render_report.py`
- turns findings into markdown artifacts

#### `scripts/common.py`
- shared helpers for path scanning, text extraction, severity normalization

#### `references/checklists.md`
- official audit checklist and launch criteria by release stage

#### `references/finding-patterns.md`
- mapping from patterns to risks, severity, and remediation guidance

#### `references/reporting-templates.md`
- standard markdown report shapes

#### `assets/sample-output/`
- examples showing what good output looks like

---

## Audit logic derived from a real release-audit case

A real QA report should be treated as the reference example for the first version of this skill.

The auditor must be able to automatically detect patterns like:
- README claims files that do not exist
- installer references `openclaw_claude_skill.py` but file is missing
- code contains broad `file:` reads with `expanduser()` and no root containment
- package has no visible tests
- copied release tree contains `.git/`
- actual implementation is AppleScript file bridge while docs claim Playwright HTTP server

If the tool cannot prove a mismatch deterministically, it should still produce a human-review finding such as:
- "README claims HTTP server architecture, but no server module or HTTP library was found in the package"

This is important: the skill should think like a release auditor, not just a grep script.

---

## Definition of success

The spec is successful if, after implementation, the skill can be pointed at a skill folder and reliably produce:
- a useful launch-readiness verdict
- a prioritized blocker list
- a teammate handoff
- the exact kind of QA insight a human release reviewer would normally produce

In other words, the skill should convert an ad hoc QA/release review into a repeatable product.
