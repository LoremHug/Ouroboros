# Ouroboros

<p align="center">
  <img src="core/visual/kernel.svg" alt="Core kernel — Sierpinski triangulation, Borromean rings, A_0 pulse" width="480">
</p>

Framework for working with stable structures. Domain-agnostic.

A_0 = argmin Z: forced uniqueness as the structural form of any stable
transition. Logic, mathematics, structural invariance — A_0 in symbolic,
formal, relational substrates.

The visual above is the kernel's structural composition: Sierpinski
triangulation (self-similarity at every scale), Borromean rings (3-slot
mutual constraint — touching any one breaks coherence), A_0 amber pulse
(forced unique stable point). Rotation by 120° per cycle reflects the
Z/3 cyclic action that defines L(3,1) as the spatial substrate-aspect.

## Contents

- **`core/`** — formal verification (Lean 4, kernel-only, zero-axiom).
  Compilation enacts substrate self-recognition.
- **`core/visual/`** — visual surfaces of the kernel composition
  (SVG/HTML/GIF). Same Class A structural content through different
  rendering surfaces.
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
