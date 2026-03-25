# Decision record example

This file shows the kind of output shape that fits the `mmm` design.

The point is not the exact schema forever.
The point is that `mmm` should return a **decision record**, not a vague filing bucket.

## Why this matters

A weak memory system says:
- “I saved it.”
- “This seems useful.”
- “I’ll remember this for later.”

A stronger convergence system says:
- what the item is
- what class it belongs to
- whether it is durable
- where it should land
- how it affects current truth
- what concrete action should happen next

## Example JSON

```json
{
  "candidates": [
    {
      "item": "The system should route durable-lesson placement questions through mmm first.",
      "classification": "procedure",
      "durable": true,
      "target_layer": "AGENTS",
      "ssot_impact": "additive",
      "action": "write",
      "reason": "This is a reusable operating rule that shapes future behavior."
    },
    {
      "item": "A one-off debugging workaround for a broken local script.",
      "classification": "one_off_workaround",
      "durable": false,
      "target_layer": "discard",
      "ssot_impact": "none",
      "action": "discard",
      "reason": "The workaround is local, temporary, and not a stable rule."
    },
    {
      "item": "A successful recent run with reusable near-term continuation value but unclear long-term durability.",
      "classification": "run_snapshot",
      "durable": false,
      "target_layer": "daily",
      "ssot_impact": "none",
      "action": "write",
      "reason": "This should be preserved as a reconstructable snapshot, not promoted into core memory yet."
    }
  ]
}
```

## Field intent

- `item` → the candidate lesson or memory object
- `classification` → what kind of thing it is
- `durable` → whether it deserves durable retention
- `target_layer` → the smallest correct landing zone
- `ssot_impact` → how it affects current truth
- `action` → the next concrete step
- `reason` → concise justification

## Design note

A good decision record creates auditability.
Someone reading it later should be able to answer:
- why this was kept or rejected
- why it landed in this layer
- whether it extended or replaced prior truth
- whether the system acted consistently with its own philosophy

## Not a rigid forever-schema

This example is intentionally lightweight.
Different runtimes may add fields, rename fields, or use a different envelope.
What matters is preserving the decision structure:

- classification
- durability judgment
- landing-zone judgment
- SSOT effect
- explicit action
- reason
