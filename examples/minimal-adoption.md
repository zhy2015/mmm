# Minimal adoption example

This file shows a very small way to adopt `mmm` inside an existing AI agent system.

## Goal

You already have:
- a system prompt or runtime prompt
- some form of memory
- maybe a skill / tool / plugin layer

You want one new behavior:

> before memory writes become durable truth, pass them through a convergence judge.

## Minimal routing rule

Whenever the system encounters one of these situations:
- a new lesson or correction
- repeated workarounds
- uncertainty about whether to save something
- uncertainty about whether old truth should be overwritten
- uncertainty about whether something belongs in memory vs references vs daily notes
- uncertainty about whether the issue should escalate into the skill layer

route the case to `skills/mmm/SKILL.md` first.

## Minimal mental model

Use this split:

- `mmm` = judge
- memory files = storage layers
- `skill-creator-enhanced` = downstream skill-layer specialist

That separation matters.
If the judge and the storage layer collapse into one thing, the system will tend to over-save.
If the judge and the skill specialist collapse into one thing, the system will tend to rewrite skills too early.

## Example policy snippet

You can adapt something like this into your own prompt or routing layer:

> For durable lessons, memory-placement questions, overwrite/downgrade/archive/discard decisions, and uncertainty about whether a lesson belongs in the skill layer, route to `mmm` first. Treat `mmm` as a convergence judge, not as a general storage manager.

## First successful outcome

A good first integration does **not** require a large framework.
If your system can already do these five things, the integration is meaningful:

1. identify a candidate lesson
2. classify it
3. decide whether it is durable
4. choose the smallest correct landing zone
5. avoid writing duplicate or conflicting core truth

## What not to do

Avoid these mistakes during first adoption:
- do not dump transcripts into core memory
- do not promote every useful-seeming case into durable memory
- do not treat one successful run as a stable procedure automatically
- do not let old and new rules coexist in core if they conflict
- do not escalate into skill refactoring before memory convergence is done

## When to involve `skill-creator-enhanced`

Only involve the downstream specialist when the problem is clearly about skill-layer design, such as:
- repeated boundary failure in a known task class
- a manager/router/execution structure collapsing repeatedly
- a stable inherited workflow pattern emerging from repeated snapshots

If the main question is still “should this be kept at all?” then stay in `mmm`.
