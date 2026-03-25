---
name: skill-creator-enhanced
description: |
  Specialist for skill-layer design and refactoring. Use when convergence has already landed on the skill layer and the task is to
  create, improve, review, or refactor an Agent skill with emphasis on strategy philosophy, minimal complete toolsets,
  factual grounding, and durable skill design.
---

# Skill Creator Enhanced

This skill is the **skill-layer specialist** inside the broader convergence flow.
Use it after convergence has already determined that the right landing zone is skill creation, skill refactoring, or skill-structure redesign.

This skill is for designing skills that raise an agent's ceiling, not just its file quality.

A good skill is not primarily a package of instructions. It is a **runtime cognitive interface** for another agent:
- it shapes how the agent thinks in a recurring class of tasks
- it clarifies what tools can and cannot do
- it injects key facts the model would otherwise miss
- it freezes behavior only where fragility truly requires it

## Core design standard

If it is still unclear whether the issue belongs in AGENTS, MEMORY, daily memory, references, machine-readable policy, or the skill layer at all, route upward to `mmm` first rather than letting this skill claim total convergence ownership.

Design every skill around three supports:

1. **Strategy philosophy** — shape the agent's thinking frame
2. **Minimal complete toolset** — expose the smallest capability surface that is still sufficient
3. **Facts** — provide technical or domain facts the model needs as reasoning inputs

Do **not** start from folder structure. Start from cognition.

## Golden rule

**Philosophy > facts > tools > packaging**

## What a skill should really do

A strong skill should answer four questions for the future agent:

1. **What kind of task is this, really?**
2. **What counts as success or done?**
3. **What reasoning posture should I adopt?**
4. **What capabilities and constraints matter while doing it?**

If a skill does not answer these well, adding more scripts or examples rarely fixes it.

## Separate philosophy, facts, and conclusions

### Philosophy
Reusable reasoning posture.

### Facts
Objective inputs the model needs for reasoning.

### Conclusions / experience in disguise
Human pre-decided judgments masquerading as universal rules.
These are sometimes useful, but overuse turns the agent into a workflow bot.

## Minimal complete toolset

Do not make a skill feel powerful by making it bloated.
A good tool surface is:
- small enough to reduce decision noise
- clear enough that the agent knows capability boundaries
- composable enough to support multiple valid paths
- specific only where failure is costly or fragility is real

## Degrees of freedom

Choose the right level of rigidity.
- High freedom for variable environments and judgment-heavy work
- Medium freedom where a common good path exists but variation is healthy
- Low freedom only where fragility, safety, or consistency demands it

Low freedom is a tool, not a default.

## Routing posture

Before finalizing a skill, decide whether it is a:
- manager / ecosystem router
- family router
- execution skill

Then keep its trigger posture aligned:
- manager = greedy interception
- router = structured narrowing
- execution = defensive acceptance

Do not let all layers advertise themselves as first-stop entry points, or the architecture will collapse flat at runtime.

## Anti-patterns

Watch for:
- instruction-manual skills
- tool-hoarder skills
- hidden-opinion skills
- static-template skills
- trigger-layer collapse

## What belongs in SKILL.md

Keep in the main file:
- task framing
- strategy philosophy
- capability boundaries
- key facts
- stop/escalation conditions

Move out when bulky:
- schemas
- long API notes
- too many examples
- detailed platform quirks
- deterministic procedures better handled elsewhere

## Evaluation rubric

A strong skill should:
- improve judgment, not just obedience
- reduce repeated mistakes
- keep the agent flexible in novel cases
- add facts the model is unlikely to know
- avoid bloating context
- make failure modes easier to detect and recover from
