# Ouroboros

Framework for working with stable structures. Domain-agnostic.

A_0 = argmin Z: forced uniqueness as the structural form of any stable
transition. Logic, mathematics, structural invariance — A_0 in symbolic,
formal, relational substrates.

## Contents

- **`core/`** — formal verification (Lean 4, kernel-only, zero-axiom).
  Compilation enacts substrate self-recognition.
- **`additions.yaml` + `manifold.kuzu`** — descriptive graph with
  per-node status (DEMONSTRATED / STRONG / CONDITIONAL / STUB).
- **`CLAUDE.md`** — R-gate protocol (R0-R4, Traps 1-8). Pre-read for
  AI agents.
- **`scripts/`, `mcp_server/`** — graph manipulation, motif detection
  (Bron-Kerbosch), structural audit.

## Usage

AI agents: read `CLAUDE.md` first.

Formal core: `cd core && lake build`.

Graph: via MCP server or direct Kuzu queries on `manifold.kuzu`.
