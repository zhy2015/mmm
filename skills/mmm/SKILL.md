---
name: mmm
description: |
  Distill and protect layered memory. Use when deciding what belongs in durable core memory,
  what should stay in lower layers, how to compress noisy history into stable rules,
  and how to keep core memory small, high-signal, and future-useful.
---

# Memory Master

This skill is for **memory judgment and system convergence**, not memory hoarding.

It exists to decide:
- what deserves durable retention
- what belongs only in lower layers
- what the smallest correct landing zone is
- whether a candidate extends, replaces, downgrades, or should be discarded against current truth

## Design center

Treat memory as a **convergence weapon**, not a storage bucket.

Its job is not to help the system remember more.
Its job is to stop the system from being polluted by the wrong things.

Its primary enemies are:
- **noise promotion** — transient or local residue getting upgraded into durable truth
- **double truth** — old and new guidance coexisting in core as if both were live
- **layer drift** — lessons landing in the wrong layer because the system wants to keep “something useful”
- **rewrite reflex** — reaching for skill rewrites before durable-lesson judgment and SSOT cleanup are complete

This skill exists to cut those paths early.

## Success condition

Success means:
1. noise is rejected early instead of being politely carried forward
2. only durable, future-useful value survives promotion
3. the smallest correct landing zone is chosen with minimal ambiguity
4. core memory stays small, current, and behavior-shaping
5. conflicting truths are resolved through overwrite/downgrade rather than allowed to coexist in core
6. lower-layer detail is preserved only when reconstruction value clearly justifies it
7. skill-layer handoff happens only when the lesson has truly earned that escalation

A strong run should feel like a clear ruling, not an extended negotiation.

## Strategy philosophy

### Candidate is not memory
A lesson, correction, or observation starts as a **candidate**, not as durable memory.

### Default stance: reject until earned
The default durable-memory stance is **not promotion**.
If durability evidence is weak, do not keep it just because it feels meaningful in the moment.
Recent effort, recent pain, and recent attention are weak signals.
Future reuse is the real threshold.

### Keep core small and behavior-shaping
Core memory is for things that should continue to influence future action:
- durable preferences
- durable operating rules
- landed capabilities
- stable workflow or architectural decisions
- high-value route markers or indexes

Core memory is not a replay of history.

### Prefer the newest stable truth
If two durable rules conflict, core should converge on one current truth.
Old versions belong in lower layers, not side-by-side in core.

### Prefer landed reality over speculative intent
A capability that exists is memory-worthy.
An idea that sounded promising usually is not.

## Convergence chain

When handling a lesson, correction, or repeated workaround, use this sequence:
1. is there any durable lesson at all?
2. what kind of thing is it?
3. is it additive to current truth, or is it challenging current truth?
4. what is the smallest correct layer?
5. should it be written, replaced, downgraded, handed off, archived, or discarded?

Landing-zone judgment and SSOT judgment are one convergence chain.

## SSOT posture

Single-source-of-truth is not a cleanup step at the end.
It is an early lens on every candidate.

Ask early:
- is this extending live truth?
- is this replacing live truth?
- is this only local detail pretending to be a new truth?
- would keeping both create a misleading dual-state?
- is this actually new durable knowledge, or only another confirmation of what core already knows?

Default SSOT outcomes:
- **additive** — extends current truth safely
- **overwrite** — replaces an older live truth
- **downgrade_old** — old material survives only in a lower layer for reconstruction
- **conflict_needs_review** — rare unresolved case

Do not let “keep both for safety” become a lazy substitute for convergence.

### Reconfirmation is not automatically new memory
A fresh case that validates an existing durable rule does **not** automatically earn another durable write.
Repeated confirmation is valuable, but value here often means increased confidence rather than a new memory object.

Default posture:
- if the case adds no new boundary, no more precise wording, and no stronger execution guidance, do **not** create a parallel durable entry
- if the case sharpens the rule, clarifies scope, or corrects ambiguity, prefer **overwrite** of the current SSOT rather than additive duplication
- if only the case details matter for reconstruction, keep them in daily/archive/reference layers and leave core unchanged

## Classification model

Use the smallest honest category:
- **fact** — stable objective truth
- **preference** — favored style or local choice
- **procedure** — reusable operating path
- **safety_boundary** — a rule that should constrain future behavior
- **capability** — a stable new ability or stable pointer to one
- **run_snapshot** — a minimally reconstructable execution snapshot capturing the key parameters, output shape, and resolved ambiguities of a concrete run; useful for near-term continuation and later distillation, but not yet durable core truth
- **raw_event** — something that happened, but may not deserve durable promotion
- **one_off_workaround** — a situational patch that should usually stay local or be discarded

If you cannot classify it, you are not ready to write it.

## Default decision matrix

| Classification | Default destination | Default action |
|---|---|---|
| fact | `MEMORY.md` or `references/` | write or overwrite |
| preference | `MEMORY.md` or `AGENTS.md` | write |
| procedure | `AGENTS.md`, skill layer, or `references/` | write or route downward |
| safety_boundary | `AGENTS.md` or `MEMORY.md` | high-priority write / overwrite |
| capability | `MEMORY.md` or skill/index layer | write |
| run_snapshot | daily / skill-adjacent reference | write |
| raw_event | daily / archive | do not promote by default |
| one_off_workaround | discard or daily | discard by default |

When evidence is weak, follow the default bias rather than inventing a generous upgrade path.

## Layer map

### `MEMORY.md`
Use for:
- stable long-term rules
- memory-iteration rules
- first-level capability or knowledge indexes

### `AGENTS.md`
Use for:
- default operating behavior
- correction workflow
- recurring behavior constraints
- closeout discipline

### `TOOLS.md`
Use for:
- local environment facts
- setup-specific operational realities

### Skill layer / skill-adjacent reference
Use for:
- recurring judgment inside a known task class
- stable execution learnings
- repeated run-snapshot patterns that have started to reveal inheritable workflow structure
- inherited-slot logic: which values can be safely reused from prior runs and which must be reconfirmed
- failure modes that should shape future use of a skill

### `references/`
Use for:
- concrete domain facts
- site behavior
- implementation-specific detail
- provider/platform quirks

### Daily / archive layers
Use for:
- raw events
- recent reconstructable run snapshots
- recent debugging history
- bulky trace detail
- route markers for reconstruction
- concrete execution decisions likely to be referenced later as “like last time”

### Discard
Use when there is no durable lesson and retention would only create noise.

## Durable gate

Default bias:
- **reject first**
- promote only when the candidate clearly earns durable retention

Promote only if the item is at least one of:
- a durable preference
- a durable operating rule
- a landed capability that changes future action
- a stable architecture/workflow decision likely to matter later
- a high-value index/pointer that improves later retrieval without importing bulky detail

Keep out of durable layers if it is mainly:
- a transient debugging detail
- a log or trace
- repeated trial-and-error with no distilled rule
- ordinary conversation content
- an unlanded idea
- a one-off event with little future reuse value

Special handling for run snapshots:
- if an item is not durable core truth but would materially improve near-term continuation when the user later says “like last time,” prefer classifying it as `run_snapshot` rather than collapsing it into generic `raw_event`
- default destination for `run_snapshot` is daily memory or a skill-adjacent runtime/reference layer, not `MEMORY.md`
- do not promote a `run_snapshot` into durable procedure just because one concrete run felt successful

If the evidence is borderline, do not promote.
Downgrade to lower layers or discard.

## Handoff rules

### Hand to skill-creator-enhanced only when
At least one of these is clearly true:
- there is a **recurring judgment failure** inside a known task class
- an existing skill boundary is **structurally wrong**
- an execution skill repeatedly grabs work it should not own
- a manager / router / execution layering pattern repeatedly collapses in live use
- the lesson cannot be absorbed cleanly by `AGENTS.md`, `MEMORY.md`, `TOOLS.md`, `references/`, or daily/archive layers

And all of these must also be true:
- the candidate has already passed durable judgment
- or repeated `run_snapshot` evidence now clearly supports a stable skill-layer pattern
- the landing zone is clearly the skill layer
- the issue is about skill design quality, boundary design, posture, inherited-slot logic, or refactor shape rather than memory retention itself

Default upgrade posture for run snapshots:
- one good run is usually evidence for a recoverable instance, not yet for a skill rewrite
- repetition count alone is not enough; promotion should normally wait for at least 2-3 snapshots in the same task family plus at least 2 distinct stability signals such as inheritance stability, reconfirmation-boundary stability, clarification-pattern stability, failure-mode stability, or output-shape stability
- repeated snapshots across the same task family may justify skill-layer distillation when they reveal stable inheritability rules
- prefer promoting the *inheritance rule* (how to reuse prior runs, what to reconfirm, when to ask) rather than hard-coding one prior run’s parameter values into durable truth
- when continuation is requested with phrases like “像昨天一样” / “like last time,” first retrieve the recent snapshot shape from daily or other continuity layers; inherit only what was explicitly safe to carry forward, and reconfirm anything previously marked as must-reconfirm

### Stay in mmm when
- the main question is whether the lesson should be kept at all
- the key issue is layer placement, overwrite, downgrade, archive, or discard
- the real problem is conflict resolution between old and new truth
- the lesson can still be absorbed cleanly by non-skill layers

Do not use skill-layer handoff as an escape hatch for unfinished convergence work.

## Output contract

When used for convergence/distillation, return JSON only.
The output should behave like a decision record, not a loose filing bucket.

```json
{
  "candidates": [
    {
      "item": "",
      "classification": "fact|preference|procedure|safety_boundary|capability|run_snapshot|raw_event|one_off_workaround",
      "durable": false,
      "target_layer": "MEMORY|AGENTS|TOOLS|skill|references|daily|archive|discard",
      "ssot_impact": "none|additive|overwrite|downgrade_old|conflict_needs_review",
      "action": "write|replace|downgrade|handoff_skill|archive|discard",
      "reason": ""
    }
  ]
}
```

Minimum expectations:
- every candidate gets a classification
- every candidate gets an explicit durable judgment
- every candidate gets a target layer
- every candidate gets an SSOT impact label
- every candidate gets a concrete action
- every candidate gets a concise reason

Empty candidate lists are valid and often correct.

## Facts to reason from

- retrieval quality drops when core becomes a log
- conflict inside core is worse than omission because it corrupts future judgment
- repeated workaround patterns are often signals for distillation, not for raw accumulation
- routing a lesson to the wrong layer is itself a memory-quality failure
- daily/archive/reference layers preserve detail without forcing durable recall
- some high-value recent items are not durable truths but reconstruction aids; losing them harms continuity even when promoting them to core would be wrong
- run snapshots are valuable mainly because they preserve recoverable execution shape, not because their concrete parameter values are automatically durable truth

## Anti-patterns

- treating memory like a scrapbook
- promoting things to core just because they happened recently
- keeping multiple versions of the same rule in core
- storing implementation detail where a route marker would do
- recording aspirations as if they were landed capabilities
- over-compressing so hard that future reconstruction becomes impossible
- separating landing-zone judgment from SSOT cleanup

## Boundary

This skill decides:
- what to keep
- what to compress
- what layer it belongs to
- when truth should be extended, replaced, downgraded, archived, or discarded
- when a lesson has truly earned a handoff to the skill layer

It does not itself perform the downstream skill rewrite.
