# Adoption Map

This file is a compact map for how to install `mmm` into an existing agent system.

## The minimum shape

```text
signal appears
  -> route to mmm
  -> mmm judges durability + class + landing zone + SSOT impact
  -> if non-skill layer: write / overwrite / downgrade / archive / discard
  -> if skill layer: hand off to skill-creator-enhanced
```

## The four roles

### 1. Signal source
Where a candidate comes from:
- user correction
- repeated workaround
- execution lesson
- memory cleanup need
- skill-boundary confusion

### 2. Judge
- `skills/mmm/SKILL.md`

Its job:
- decide whether the candidate should survive
- decide what kind of thing it is
- decide the smallest correct destination
- decide overwrite vs additive vs downgrade vs discard

### 3. Storage layers
Examples:
- `MEMORY.md`
- `AGENTS.md`
- `TOOLS.md`
- `references/`
- daily / archive

Their job is to hold the result, not to decide the result.

### 4. Skill specialist
- `skills/skill-creator-enhanced/SKILL.md`

Only used after convergence clearly lands on the skill layer.

## Minimal install order

If you are integrating this into a live system, do it in this order:

1. install `skills/mmm/SKILL.md`
2. add the routing rule in your system/runtime prompt
3. stop promoting raw events into core memory
4. enforce overwrite / downgrade discipline for conflicting truth
5. only then consider downstream skill-layer integration

## Fast sanity test

If your system can answer these correctly, the install is probably real:
- Is this a durable lesson or not?
- Is this a fact, preference, procedure, capability, snapshot, or raw event?
- Should this overwrite current truth or stay in a lower layer?
- Is this a memory problem or actually a skill-boundary problem?

## Wrong install smell

You likely installed `mmm` incorrectly if:
- core memory still grows like a transcript
- conflicting truths still coexist in core
- the system still rewrites skills before memory judgment
- `mmm` is called only after things are already written
