# Quickstart

This file is for people who want to **adopt `mmm` quickly** without reading the whole repository first.

## Goal

Use `mmm` as an upstream convergence judge for:
- durable lesson judgment
- memory landing-zone choice
- overwrite / downgrade / archive / discard decisions
- deciding whether something really belongs in the skill layer

## Minimal adoption path

If you only have 3 minutes, read in this order:

1. `README.md`  
   Understand what `mmm` is and what problem it solves.
2. `skills/mmm/SKILL.md`  
   This is the actual upstream judge your system should route to first.
3. `AGENTS.md`  
   Copy/adapt the routing posture into your own runtime rules.
4. `MEMORY.md`  
   Use as a shape reference for what core memory should stay like.

## Smallest working integration

You only need four things:

### 1. Add the `mmm` skill
Put `skills/mmm/SKILL.md` into your skill system.

### 2. Add a routing rule
When the system sees any of the following, route to `mmm` first:
- lesson
- correction
- repeated workaround
- memory placement uncertainty
- overwrite / downgrade / archive / discard question
- uncertainty about whether something belongs in a skill

### 3. Keep `mmm` as judge, not executor-of-everything
`mmm` should decide:
- keep or reject
- class
- landing zone
- SSOT impact
- write / overwrite / downgrade / archive / discard / handoff

It should **not** automatically rewrite the whole system every time.

### 4. Add a downstream specialist only if needed
Only after the result clearly lands in the skill layer should you hand off to:
- `skills/skill-creator-enhanced/SKILL.md`

## First deployment checklist

- [ ] The system can route memory-governance questions to `mmm`
- [ ] Core memory is no longer used as a transcript/log bucket
- [ ] The system prefers overwrite over parallel conflicting truths
- [ ] Run snapshots stay in lower layers unless clearly promoted
- [ ] Skill rewrites no longer happen before landing-zone judgment

## Common mistake

The most common mistake is to read `mmm` as a memory storage system.

It is not.

It is a **convergence judge**.

## One-line summary

> Put `mmm` in front of memory writes and skill-boundary decisions, not behind them.
