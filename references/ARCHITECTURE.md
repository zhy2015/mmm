# Architecture & Integration Guide

This document explains the core architecture of the `mmm` system and how to integrate it into OpenClaw.

## 1. The Four-Layer Memory Architecture (L0 - L3)

Based on the OpenClaw "Four Layers of Memory" philosophy, `mmm` enforces strict separation of concerns.

| Layer | What it is | When it acts | `mmm`'s Role | Storage Location |
|---|---|---|---|---|
| **L0 (Identity)** | Principles, preferences, absolute boundaries. | **Always On** (L1 Cache). Evaluated before any action. | `mmm` protects this layer. Only highly durable "behavior-shaping rules" get promoted here. | `AGENTS.md`, `MEMORY.md` |
| **L3 (Experience)** | Past conversations, run snapshots. | **On Demand** (L3b). Pulled only when `mmm` explicitly asks for it via `read_decision`. | `mmm` writes snapshots here during Phase B, and recalls them during Phase A ONLY if needed. | `daily/`, `archive/` |
| **L2 (Local Knowledge)** | Docs, code snippets, factual references. | **On Demand**. Searched by dedicated tools (e.g., Sirchmunk) when evidence is needed. | `mmm` does NOT store knowledge. It points to `references/` or triggers knowledge retrieval tools. | `references/`, `skills/` |
| **L1 (Web)** | External facts. | **Last Resort**. | `mmm` avoids this unless L2/L3 fails. | External |

---

## 2. Integration with OpenClaw

To integrate `mmm` into OpenClaw, you must implement the CQRS (Command Query Responsibility Segregation) data flow. 

**Important Note on OpenClaw Initialization:**
OpenClaw will *always* read `AGENTS.md` (Work Principles) and `MEMORY.md` (Core Memory) upon waking up. Therefore, `mmm` must be extremely strict about what gets written to these L0 files to prevent prompt bloat.

### Phase A: The READ Path (Context Assembly)
*Triggered when a new user request arrives.*
1. User says: "Parse this PDF and output a summary."
2. OpenClaw routes the intent to `mmm` (Phase A).
3. `mmm` outputs JSON indicating which **Skills** and **Memories** to dynamically load.
4. OpenClaw injects ONLY these requested assets into the Context Window, alongside the always-loaded L0 files.

### Phase B: The WRITE Path (Memory Retention)
*Triggered when a task completes, fails, or user says "Save".*
1. Task finishes or User explicitly requests a save.
2. Agent submits the candidate context to `mmm` (Phase B).
3. `mmm` evaluates: Is it durable? Does it conflict with L0?
4. `mmm` outputs JSON (`write_decision`: write, overwrite, downgrade, or discard).
5. OpenClaw executes the file system writes exactly as dictated using the **Memory Executor** (`scripts/core/memory_executor.py`).

---

## 3. The Execution Layer (Physical Hands)

While `mmm` acts as the brain (outputting JSON), the actual reading and writing of the file system is handled by the **Memory Executor**.

Location: `scripts/core/memory_executor.py`

This Python script is the bridge between the `mmm` skill and OpenClaw's core framework. It handles:
- **Safe Overwrites**: Preventing data corruption when replacing L0 rules.
- **Context Assembly**: Reading L0, L2, and L3 files from disk and concatenating them into a single string for the LLM's Context Window.
- **Handoff Triggering**: Invoking `skill-creator-enhanced` when a structural rewrite is mandated.
