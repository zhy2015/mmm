# Adoption Pitfalls

This note records the most common mistakes when people adopt `mmm` into an existing agent system.

## 1. Treating `mmm` as a storage manager

Wrong mental model:
- `mmm` exists to save more memory

Correct mental model:
- `mmm` exists to reject noise, choose landing zones, and preserve SSOT

## 2. Routing to `mmm` too late

Common failure:
- the system writes first
- then asks `mmm` whether the write made sense

Correct posture:
- route to `mmm` **before** durable writes and before skill-boundary escalation

## 3. Using `mmm` as a generic rewriting engine

`mmm` should not become the thing that rewrites every layer itself.
Its job is to produce a convergence judgment:
- keep / reject
- class
- destination
- SSOT impact
- action

Execution can still happen elsewhere.

## 4. Promoting run snapshots too aggressively

A successful run is not automatically a durable procedure.

Default:
- keep concrete runs in daily / lower layers
- only promote when stable reuse structure clearly appears

## 5. Keeping conflicting truths “for safety”

This is one of the most damaging habits.

If two durable rules conflict, convergence should usually prefer:
- overwrite
- downgrade old truth to lower layers

not parallel live truth in core.

## 6. Jumping to skill rewrite before landing-zone judgment

Many teams rewrite skills when the real issue is still:
- wrong memory layer
- duplicate truth
- noisy core memory
- lack of overwrite discipline

Fix the convergence problem first.

## 7. Copying the repo literally instead of adapting it

This repository is a portable example.
Do not assume every file name and every layer name must be copied exactly.
Preserve the logic, adapt the wording and file map to your runtime.

## One-line check

If your system still tends to:
- write first
- keep both versions
- promote one-off runs
- rewrite skills too early

then `mmm` has not really been installed yet.
