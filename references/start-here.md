# Start Here

If this is your **first time opening the `mmm` repo**, use this page as the shortest navigation path.

## What `mmm` is

`mmm` is a memory-convergence method for AI agents.
It is designed to answer:
- what deserves durable retention
- what should stay in lower layers
- when new truth should overwrite old truth
- when something should be discarded instead of saved
- when an issue should escalate into the skill layer

## Best first-reading order

### If you are a human evaluating the repo
1. `README.md`
2. `references/quickstart.md`
3. `references/adoption-map.md`
4. `references/adoption-pitfalls.md`

### If you are wiring it into an agent/runtime
1. `skills/mmm/SKILL.md`
2. `AGENTS.md`
3. `MEMORY.md`
4. `examples/minimal-adoption.md`

## Fast file map

- `README.md` → what the project is
- `skills/mmm/SKILL.md` → the actual convergence judge
- `AGENTS.md` → repo/runtime posture
- `MEMORY.md` → shape of core memory
- `references/quickstart.md` → shortest adoption path
- `references/adoption-map.md` → where `mmm` sits in the system
- `references/adoption-pitfalls.md` → common installation mistakes
- `references/decision-record-example.md` → what good output looks like
- `examples/minimal-adoption.md` → small integration example

## One-line install rule

> Put `mmm` before durable writes and before skill-boundary escalation.

## One-line anti-pattern

> If your system writes first and asks questions later, `mmm` is not really installed.
