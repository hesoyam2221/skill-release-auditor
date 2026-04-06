# Community Launch Drafts — Skill Release Auditor

## Reddit — r/openclaw

**Title:** I built a tool that audits OpenClaw skills before launch

**Post:**
I built a small tool called **Skill Release Auditor** after watching how many OpenClaw skills run into the same release problems right before launch.

It audits a local skill directory and flags things like:
- README vs code mismatches
- broken installer references
- missing tests
- unsafe file/path access heuristics
- release contamination like `.git/`
- beta launch blockers

It then generates:
- a status report
- a prioritized launch checklist
- a teammate handoff
- structured findings JSON

It’s an MVP, so it’s still heuristic-based and not a semantic verifier. But it’s already useful for catching the kind of release mess that wastes trust fast.

I originally built it after doing a painful manual QA pass on another OpenClaw skill and realizing the same release-review work should be automatable.

If people want, I can share the GitHub package and I’m also happy to run a few free audits for early skill authors.

## Discord — #showcase

Built a new OpenClaw tool: **Skill Release Auditor**.

It checks a skill before launch and catches stuff like:
- docs that don’t match the real files
- broken install references
- missing tests
- broad file-access risk patterns
- release junk like `.git/`

It outputs:
- status report
- launch checklist
- teammate handoff
- findings JSON

It’s a real MVP, not magic, but it already saves a bunch of manual QA pain. If anyone here is about to ship a skill and wants a free audit, I’m happy to test it.

## GitHub Discussions — openclaw repo

**Title:** Skill Release Auditor — a release-readiness checker for OpenClaw skills

**Post:**
I built a small release-readiness tool for OpenClaw skill authors called **Skill Release Auditor**.

The goal is simple: catch the avoidable launch problems before users do.

Current MVP checks for:
- README/code mismatches
- missing installer file references
- missing tests or smoke coverage
- broad local file-access heuristics that need review
- release contamination like `.git/`
- beta launch blockers

It generates a status report, a prioritized checklist, and a teammate handoff file.

This is not a full semantic verifier and it doesn’t auto-fix code yet, but it’s already useful as a release-prep pass.

If there’s interest, I’d love feedback on:
1. what checks should be added first
2. what would make it more useful for skill authors
3. whether a Pro version with README rewrites, test scaffolds, and auto-fix suggestions would actually be worth paying for
