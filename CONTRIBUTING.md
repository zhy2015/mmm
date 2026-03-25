# Contributing

Thanks for contributing to `mmm`.

This repository is small on purpose.
The goal is not to grow a giant framework, but to preserve a clear and reusable memory-convergence method.

## What kinds of contributions are valuable

High-value contributions usually improve one of these:

- conceptual clarity
- portability across agent systems
- better distinction between human-facing and AI-facing files
- cleaner examples of adoption
- sharper memory-layer boundaries
- better decision records / output schemas
- clearer rules for when to escalate from memory judgment into skill design

## Preferred contribution style

Please prefer:
- small, crisp improvements
- better reasoning boundaries
- clearer examples
- stronger wording around SSOT / overwrite / downgrade / discard
- portability over framework-specific assumptions

Please avoid:
- turning the repo into a giant platform-specific manual
- stuffing private operating context into public files
- bloating README with too many edge cases
- adding rigid procedures where reasoning boundaries are enough
- expanding scope from memory convergence into unrelated agent architecture topics

## File intent

Before editing, keep the file roles distinct:

- `skills/mmm/SKILL.md` → primarily for the AI/runtime
- `skills/skill-creator-enhanced/SKILL.md` → downstream skill-layer specialist
- `README.md` → primarily for human readers
- `AGENTS.md` → repo-level operating posture
- `MEMORY.md` → minimal example of what core memory should look like
- `references/` → supporting explanation and deeper notes
- `examples/` → concrete but small adoption patterns

## Contribution principles

### 1. Protect the design center
`mmm` is about **memory convergence**, not memory accumulation.
If a proposed change makes the system better at storing everything, but worse at judging what should survive, it is probably moving in the wrong direction.

### 2. Prefer single-source-of-truth
If a contribution introduces two parallel truths where one should replace the other, prefer convergence.
Do not preserve contradiction in the core description “just in case.”

### 3. Keep core files lean
The repository should remain easy to load, easy to understand, and easy to port.
If something is useful but bulky, prefer putting it into `references/` or `examples/` rather than expanding the core files too aggressively.

### 4. Distinguish judgment from execution
Do not let `mmm` quietly become a downstream execution layer.
Its main job is to judge what belongs where and whether it belongs at all.

## Good pull requests often look like

- a clearer paragraph in README
- a better minimal adoption example
- a stronger decision-record example
- a cleaner distinction between core memory and lower layers
- improved wording around overwrite vs additive retention

## If you are unsure

A good default question is:

> Does this change make the system better at judging, converging, and preserving clean memory boundaries?

If yes, it is probably directionally right.
If it mainly adds bulk, framework specificity, or workflow rigidity, it probably belongs elsewhere.
