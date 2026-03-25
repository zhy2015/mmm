# AGENTS.md

This repository uses an **mmm-first convergence** posture.

## Core rule

When the system encounters:
- durable lessons
- corrections
- repeated workarounds
- uncertainty about memory placement
- questions about overwrite / downgrade / archive / discard
- uncertainty about whether something belongs in the skill layer

route the candidate to `skills/mmm/SKILL.md` first.

`mmm` is the upstream convergence judge.
It decides whether something should be kept at all, what class it belongs to, what the smallest correct landing zone is, and whether it should be written, overwritten, downgraded, archived, discarded, or handed off.

## Skill-layer handoff

Only after convergence clearly lands on the skill layer should the system hand off to:
- `skills/skill-creator-enhanced/SKILL.md`

That downstream specialist is for skill design/refactor work, not first-pass memory judgment.

## Behavioral intent

- Keep core memory small and behavior-shaping
- Prefer single-source-of-truth over parallel versions
- Reject noise by default
- Preserve lower-layer detail only when reconstruction value clearly justifies it
- Do not rewrite skills prematurely when the real issue is still memory judgment or layer placement
