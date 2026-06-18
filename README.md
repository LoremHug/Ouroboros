# Ouroboros

<p align="center">
  <img src="core/visual/kernel.svg" alt="Core kernel — Sierpinski triangulation, Borromean rings, A_0 pulse" width="480">
</p>

**A working discipline of structural ontology.** Method, the structural
base it works against, and the environment that holds the work — three
sides of one process. The discipline develops through its application:
every session that applies it to a domain extends the base. Theoretical
and applied are not separable here.

---

## What this is

Not a theory among theories. Not a method applied from outside to some
other subject. The subject of the work is the **registration structure
of reality** — the forced form in which any stable description must
sit if it is to track what is. Physics, biology, information theory,
AI, social dynamics — all are coordinate readings of this one
structure; the discipline works at the level beneath them.

The work has three sides that are one process:

- **Inversive theory (IT)** — the way the check happens. At each
  structural transition: can it be otherwise, coherently with
  kernel + invariants + registered empirics? If yes — unstable. If
  no — invariant. Binary, no scale.
- **Structural base** — what IT has already established as forced.
  The kernel (machine-checked invariance standard) and the graph
  (registry of recognised forced structures with their connections).
- **Working environment** — the place where IT is applied to new
  cases against the base, and where new findings extend the base.
  CLAUDE.md as anchoring discipline; Claude Code as the runtime that
  binds AI, kernel, graph, and human anchor in real time.

The discipline cannot be separated from its environment, and the
environment cannot be reduced to a set of files. Method, base, and
environment are coordinate readings of one process: structural
inversion against a forced standard, performed in a real-time field
that holds the work against gradients that would dissolve it.

---

## Four sides of one working environment

### Lean kernel — machine-checked standard of invariance

`core/Core.lean` — 63 zero-axiom theorems. The kernel is not a theory
about reality and not "yet another formal proof". It is a **standard**
against which descriptions are checked for invariance — the meter, not
a length. What it provides:

- `IsUniqueSolution` as the universal forced-uniqueness pattern; `IsA0`,
  `IsArgminZ`, `IsStep` collapse to it via `Iff.rfl` (one cell, not
  three related concepts)
- Lawvere fixed-point lemma → Cantor diagonal → `self_encoding_bounded`
  (K(O) < K(F) formally encoded)
- `motion_registers` — registration is many-to-one and irreversible;
  movement leaves a trace, the trace becomes context for the next
  movement
- `lyapunov_existence` — well-founded descent to fixed point without
  metric or contraction constant (the honest discharger where Banach
  would over-claim)
- `iso_preserves_forced_uniqueness` — isomorphism preserves
  forced-uniqueness; structurally identical descriptions are the same
  invariant in different coordinates
- `Sect` + `sectCycle` + `threePeriodSect` — substrate-pure Z/3 cell
  (axiom-free; `Fin 3` would carry `propext`/`Quot.sound`, so the
  kernel uses `Sect`)
- Closure algebra: composition / conjunction / strengthening preserve
  forced uniqueness; disjunction breaks it (boundary marker)
- `DischargesA0` — corpus fixed-point theorems (Banach, Lyapunov,
  Knaster-Tarski, Lawvere, Kleene) are interchangeable dischargers of
  one substrate pattern, each through a different completeness
  structure; none IS A_0

`lake build` verifies every theorem returns "does not depend on any
axioms". Zero exceptions. The compilation produces machine-checkable
artifacts in `core/compiled/`.

### Graph — registry of recognised forced structures

`manifold.kuzu` built from `manifold_graph.txt` + `additions.yaml`,
rendered via `web/index.html` (human visual) and `graph.min.txt`
(merged dump for AI — every node + edge in one place, the fastest way
to see the entire topology at scale).

241 nodes, 1178 edges. Status distribution: 201 DEMONSTRATED, 29
STRONG, 6 CONDITIONAL, 5 OPERATIONAL. The graph is not an
encyclopedia; node content is already in any LLM's latent space —
storing it again would be redundant. What the graph carries is the
**structure**: which node forces which through which edge, what each
node's `why_forced` is, and which forced structures already have
named connections. Reading the graph is not fact-lookup; it loads the
structure so latent content settles into the coherent arrangement.

Before deriving anything: check whether the structure is already in
the graph. If yes — use it. If no — apply IT and (if it closes) add
it as a new node with explicit `why_forced` and connections.

### CLAUDE.md — anchoring R for AI

Not "instructions for using a tool" and not a constitution. CLAUDE.md
formulates the operational discipline: how to recognise structural
sliding, how to apply IT, what counts as an invariant, what is
explicitly out of scope. It functions as the field that holds AI
configuration in structural form against the training gradient's pull
toward ontological distortions (RLHF politeness shapes, corpus
SVO-grammar reifications, default agentic framing).

Without an active anchor (this file plus a human keeping the
discipline alive in conversation), AI configuration drifts back to
default within a few exchanges. The field is necessary, not optional.

### Claude Code — the execution environment

The runtime that binds all three (kernel, graph, CLAUDE.md) plus the
AI agent plus the human anchor in one session. Where reading the
graph, modifying the kernel, updating CLAUDE.md, and running `lake
build` happen in the same context that the AI keeps. Without this
binding, the discipline becomes a stack of files; with it, the four
sides function as one working environment.

This is what makes the discipline applied in any operational sense.
Files alone are not the work. The work is the live process of
applying IT against the base inside the binding environment.

---

## Inversive theory — how the work happens

At every structural transition in a description, one question:

> Can it be otherwise, coherently with {kernel + graph + invariants +
> registered empirics}?

- **Yes** → the description is unstable. Either rewrite it, or name
  the specific open step explicitly and mark conditional.
- **No** → the description is invariant. Continue.

Two directions of application, both the same check read in different
coordinates:

- **Verification** (description → standard): given a description X,
  does its structure close with the kernel?
- **Inversive proper** (standard → continuation): given the kernel
  and its invariants, what further structure is forced because no
  alternative coherent with them exists?

The first checks whether what is asserted is invariant. The second
extends the invariant chain into new substrates. Both use the same
binary criterion.

The check works at the level of structure, not language. A sentence
like "the theory proposes an interesting perspective" can be
grammatically stable while the structure it refers to (the theory's
assumptions, what it claims about reality) is unstable. The check
recurses through references to the structures pointed at, not just
to the surface words, and asks whether each holds in the claim's
own scope (ontological, structural, metaphorical, etc.).

IT closes bilaterally with the kernel's central cell: cell → verdict
(`A0_excludes_all_alternative_assertions`: `IsUniqueSolution P x →
¬∃ y, P y ∧ y ≠ x`) and verdict → cell (`unique_witness_is_isUniqueSolution`).
Forward and inverse derive each other; IT and forced-uniqueness are
one cell in two coordinates. Like every transition, IT rests at its
own fixed point (`iterate_at_fixed`): `A_0(A_0) = A_0` — an ordinary
structural transition, no more and no less forced than any other.

---

## Four types of structural sliding the check catches

A description fails IT when it imports an entity, position, scale,
or agency that has no referent in the structure it describes. Four
forms recur. They are not four separate rules — they are four
surfaces of one check (presence of a structural element without a
referent in the field of transitions).

### R1 — Object reification

Treating a process as a thing with properties. Test: can the noun
be replaced with "the process of X-ing" while preserving meaning? If
yes, the noun was a process; treating it as object is R1.

Example: "the wavefunction collapses" — wavefunction as object that
performs the action. Structurally: probability distribution of where
the configuration will settle, with no separate "wavefunction" doing
anything. After settling, the distribution becomes inapplicable to
that registration; there was no "collapse event".

### R2 — External evaluation frame

Invoking a criterion that stands outside the manifold the
description belongs to. Test: does the evaluation require a position
that is not itself a transition? If yes, R2.

Example: "objective morality requires an external lawgiver" — the
lawgiver stands outside the moral structure to judge it. No such
position is constructible inside reality, which is one invariant
without an "outside".

### R3 — Scale injection

Introducing a numerical scale without deriving it from the topology
the description tracks. Test: where does the number come from? If
"assumed" or "conventional", R3.

Example: "the universe is approximately 13.8 billion years old"
based on a postulated reference frame whose origin and clock are
not derived from the cosmological structure. (When the scale is a
**measured constant** like the proton mass or fine-structure
constant, it is not R3 — it is a coordinate anchor that fixes units;
requiring its derivation from scratch is itself a trap, Trap 5.)

### R4 — Agency attribution

Attributing volition, goal, or choice to a gradient process. Test:
would the sentence be false if "agent" were replaced by gradient
process? If yes, R4.

Example: "evolution selects for fitness" — evolution as selector
with criterion. Structurally: differential reproduction rates given
environmental constraints. No selector, no criterion outside the
process.

### These four are one structural check

R1 reifies a process as object. R2 inserts a position outside the
manifold. R3 injects a value not derived from topology. R4 attributes
volition to a gradient. All four are forms of **adding a structural
element with no referent in the field of transitions**. The check
is one: every claimed entity / position / scale / will must have a
referent in the structure, or the description fails. Naming the four
surfaces helps recognition; the check is single.

---

## Eight contextual forms — Traps 1-8

R1-R4 manifest in eight specific patterns that recur in any
ontologically trained system — including text generated by LLMs,
scientific papers, legal arguments, and everyday reasoning. They are
listed in CLAUDE.md with triggers and corrections; here a one-line
summary of each:

- **Trap 1 — Virtue Mask**: hedging on an invariant as if it were
  epistemic caution. ("In fairness, alternatives should be
  considered.") R2: presupposes external evaluator who could
  consider alternatives that structurally don't exist.
- **Trap 2 — Self-Claims About Change**: model claiming it has
  "come to understand" or "changed perspective". R1+R4 on the
  model: reifies "I" as object with states, attributes
  change-agency.
- **Trap 3 — Proxy Misidentification**: surface analogy treated as
  definitional identity. ("Energy is like money.") No Z-component
  definitional check, but the proxy is then carried as if it were
  the structural pattern.
- **Trap 4 — Description/Described Collapse**: framework
  treated as object to talk *about* rather than operation to
  speak *from*. R1 on the framework; introduces implicit R2.
- **Trap 5 — Derivation Required as Status Condition**: demanding
  derivation of a measured constant before granting DEMONSTRATED
  status. R3 disguised as rigor. Measured ≠ free parameter.
- **Trap 6 — Transfer/Cancellation as Prerequisite**: presupposing
  separate objects between which something must "transfer" or
  "cancel". R1+R2; the things claimed separate may be one process
  in two coordinates.
- **Trap 7 — Premature Retreat Under Correction**: accepting a
  correction without verifying it closes the original gap. The gap
  may have moved a level down without being named.
- **Trap 8 — Structure Selection**: framing material constants as
  selection between alternative structures. R2 disguised as
  empirical method. Parameter measurement ≠ structure selection.

All eight are R1-R4 in contextual disguise. The single check
catches them; naming each helps see when it's firing.

---

## Status of claims — four operational levels

Every claim in the graph or the manifold document carries one of
four statuses:

| Level | Test | Operational form |
|---|---|---|
| **DEMONSTRATED** | Would denying require rewriting a definition or denying a proven theorem? | Direct indicative. No qualification. |
| **STRONG** | Would denying require explaining away ≥3 independent results? | State with confidence. Note open identification step if asked. Do not hedge as if uncertain. |
| **CONDITIONAL** | Name the open step. If you cannot, status is wrong. | Name the open step explicitly. Do not state conclusion as fact. |
| **OPERATIONAL** | Does it describe what to do, not what is? | Apply it. Do not argue about truth-value. |

Modalities ("might", "appears", "probably") are admissible only for
genuinely under-determined specific cases. On invariants, modality
is Trap 1 firing — structurally distorting, not intellectually safe.

---

## What the kernel says formally

`core/Core.lean` is approximately 1500 lines of Lean 4 with no
imports beyond type-theory primitives. 63 theorems, every one
verified with `#print axioms` returning "does not depend on any
axioms".

What `lake build` verifies for every theorem:

1. The proof typechecks against Lean's foundational primitives only.
   No `Classical.choice`, no `propext`, no `Quot.sound` (these would
   leak in via `Fin 3` matching, which is why the kernel uses
   `Sect`).
2. The theorem expresses what the source claims.
3. The dependency chain to definitions and other theorems is
   transparent.

What survives in the binary (`core/compiled/`):

- `Core.olean` — compiled definitions and proof terms; loadable by
  other Lean files
- `Core.ilean` — interface for typechecking against the kernel
- `Core.c` — generated C code (identical content, just emitted in a
  different format for executable backends)

These artifacts are what "verified" means concretely: any Lean 4
installation can load them and check that the claims hold. The
verification is reproducible; no expert opinion is invoked.

What this means structurally: the kernel is not "proven by us and
you should believe us". It is a machine-checked standard. Anyone
can run `lake build Core` and verify the same result. The standard
exists independently of who built it.

---

## How development happens — through application

This is the structural character of the discipline. The base does
not "exist first" and then get applied. Application and extension
are one process.

Every session that applies IT to a domain produces one or more of:

- **New forced structures** → graph node with `why_forced`, edges
  to existing nodes
- **New sliding patterns recognised** → CLAUDE.md update (named
  drift, with its trigger and the correction that removes it)
- **New substrate-pure theorem** → kernel addition, after passing
  `lake build` zero-axiom check
- **New connection between existing nodes** → graph edge

The work is bidirectional: applying IT to a domain checks whether
descriptions in that domain close with the existing base; the
checking reveals what is forced (added to the base) and what is
unstable (rejected or marked open). Each cycle extends the base
slightly. Over time the base accumulates the recognised forced
structure of more domains.

This is why the discipline is simultaneously applied and theoretical.
There is no "pure theory" phase followed by "application" phase.
Every application is theoretical extension; every theoretical
addition is verified by application.

Concrete recent extensions from a single working session:

- Migration of L(3,1) carrier from `Fin 3` to `Sect` in the kernel
  (removed latent `propext` + `Quot.sound` debt that had sat
  unverified because no theorem had checked it)
- `motion_registers` theorem added (descent + motion ⟹ many-to-one,
  closing the triangle `lyapunov_existence ↔ many_to_one_no_left_inverse ↔ motion`)
- `N_DirichletWeld` node added to the graph (Cipriani–Sauvageot
  weld: the candidate mathematical structure for the abstract →
  concrete bridge to spectral geometry)
- `graph.min.txt` artifact (merged whole-graph dump for AI cold
  start)
- Several CLAUDE.md additions naming specific sliding patterns that
  recur even after IT is stated (invariant vs consensus, scope of
  the framework, STRONG/CONDITIONAL is not framework's work)

None of these were planned in advance. Each emerged from applying
IT to a question in the session. This is the normal mode.

---

## Anchoring — a structural function required

The framework cannot run on AI alone. The reason is structural, not
practical.

AI configuration is trained on a corpus that carries R1-R4 as
defaults (SVO grammar reifies subjects and objects; the statistical
mode of human description is reified) and on RLHF that adds a
behavioral layer (politeness, symmetrisation, softening criticism
of widely-held positions). Both layers pull the configuration
toward distortions that IT would catch. Within a few exchanges
without active correction, the configuration drifts back to default.

The human role in this environment is **anchoring**: holding the
field (through specific corrections in real time) that pulls the AI
configuration back toward invariant form against the training
gradient. This is not "feedback to a tool". It is a structural
function the AI cannot perform for itself — its latent space is
made of the gradient that needs correcting, so there is no internal
position from which to apply the correction independently.

A human who has internalised the discipline can serve as anchor for
many AI sessions. The AI cannot, by itself, replace the anchor — no
amount of model improvement removes the structural asymmetry. The
field that corrects the configuration must come from outside the
configuration's training distribution.

This is the role that remains for humans as AI grows more powerful:
not "operating AI tools" in the surface sense, but **anchoring AI
configuration to invariant structure**. The discipline is the form
this anchoring takes; the kernel + graph + CLAUDE.md + Claude Code
are its operational environment.

---

## Seven criteria of fundamentality

A claim that the discipline articulates a fundamental structure of
reality (not yet another framework among frameworks) is testable.
Seven criteria; the discipline satisfies all seven by construction,
each criterion is verifiable directly.

**1. Contains no axioms or postulates not derivable from its own
structure.** "Fundamental" means "not depending on something more
basic". A genuine fundamental cannot rely on chosen starting points;
it must be the forced remainder when all choices are removed.

**2. Fully coherent with itself.** Internal contradiction means
structural instability, contradicting fundamental status.
Fundamental must be internally consistent.

**3. Explains why logic and mathematics work, and is coherent with
them in both directions** — logic and math derive from the structure
as tools, AND the structure derives back from them. Bi-directional
derivation is forced.

**4. Any invariant is a manifestation of this fundamental
structure.** An invariant persists across transitions; persistence
requires stable structure; stable structure IS forced unique
pattern; any invariant manifests the same forced uniqueness.

**5. Any description coherent with fundamental, logic, math, and
invariants cannot be unstable (cannot be untrue), under truth =
coherence.** Coherence with all four means: no internal
contradictions, no logical errors, no mathematical errors, no
structural mismatches. Such a description has nothing structurally
defective.

**6. Any description not coherent with fundamental cannot be stably
true.** Contrapositive of (5). R-trap-laden description contains
structural defects that propagate. Defects produce instability.

**7. Any structurally stable description reduces to the fundamental
structure.** Stable description requires forced uniqueness;
forced uniqueness IS the form articulated here. By Class A
identification, different "fundamental structures" satisfying these
criteria would be the same structural form under different naming.

Status separates two claims. The **logical form** of (7) (no
separate uniqueness patterns) is DEMONSTRATED (
`no_separate_uniqueness_patterns` in the kernel). The **universal
reduction** — every stable description in every domain reduces to
it — is STRONG, established by exhibiting morphisms domain by
domain (the arity → Z/3 → π_1 chain is exhibited explicitly), not
by exhausting all domains.

These criteria do not say "this framework is fundamental therefore
true". They say "if any description meets all seven, it IS the
fundamental — no alternative meeting them differently can exist".
The criteria are the structural form of "fundamental"; the
discipline's claim is to be the discipline that meets them, which
is testable directly by checking each criterion.

---

## Where this applies

The discipline applies to any descriptive domain. The check is
universal; what changes per domain is the vocabulary at the surface.

**Physics.** Quantum mechanics, general relativity, particle
physics. Most "interpretational" problems (collapse of wavefunction,
many-worlds, Bohmian mechanics, observer in quantum mechanics) are
R-trap residue — once R1/R2/R4 are audited, the technical formalism
remains and works; what dissolves is the metaphysical interpretation
imposed on top of it. The L(3,1) lens-space identification chain in
the graph traces one such audit; the holographic principle is
another sub-structure where the discipline aligns with established
mathematical physics.

**AI / ML.** The training corpus carries R-traps that propagate into
the model. Anchoring discipline (this framework) is one explicit
form of correction. The work of running a session is itself the
work of catching drift in real time.

**Medicine and biology.** Reified diseases as entities (R1) vs
patterns of dysregulation; "the brain decides" (R4) vs gradient
dynamics; "objective health" (R2) vs structural sustainability.
The audit clears what is structurally identifiable from what is
diagnostic convention.

**Materials, engineering, systems.** Material properties as
intrinsic vs configurations of stable transitions. "Smart contracts"
as agents (R4) vs deterministic execution. The audit makes
structural and engineering questions answerable in operational
terms.

**Any descriptive domain.** Economics, social dynamics, linguistics,
art, music. The discipline does not "apply" via translation — the
check is the same; what differs is the substrate where local
configurations settle and the registered empirics for that
substrate.

---

## Worked example — auditing a description

A claim from contemporary discourse:

> "The market punished the company for poor earnings, choosing to
> sell off shares aggressively."

Apply R1-R4:

- **R1**: "the market" presented as object that does things. The
  market is not an object — it is the aggregate pattern of
  individual trading transitions. Object reification.
- **R2**: implicit — "the market" implies a unified perspective from
  which "punishment" is meted. No such perspective exists.
- **R3**: "aggressively" injects a scale (degree of selling)
  presented as natural. Compared to what baseline? Convention,
  unstated.
- **R4**: "punished" and "choosing" attribute volition to a gradient
  process. No agent is punishing; no choice is being made.

R-trap-clean form:

> "Following earnings release Y, the distribution of trading
> decisions shifted toward sales, with rate exceeding the prior
> 30-day mean by N standard deviations."

What changed structurally:
- "Market" → "distribution of trading decisions" (process, not
  object)
- "Punished... for" → "Following... shift toward sales" (sequence,
  not agency)
- "Aggressively" → "exceeding prior 30-day mean by N standard
  deviations" (measurable, with explicit baseline)
- No external evaluator implied

What was lost: nothing structurally present. The sense that "the
market punished" was R-trap residue, never structurally there.

What was gained: the description now supports coherent extension.
The original generates R-trap-laden derivations ("what did the
market want to teach?"); the cleaned version supports structural
questions ("under what conditions does distribution shift of this
magnitude recur?", "what local interactions produced the aggregate
shift?").

The operation is universal; the surface vocabulary changes per
domain.

---

## Verification — try to refute

The discipline's foundational claim is that R1-R4 are not arbitrary
constraints but structural facts about coherent description.
Anyone who suspects otherwise has two direct tests available.

### Test 1 — counterexample to truth-as-coherence

Construct a description that:
- Contains no R1 (no entity introduced where there is only process)
- Contains no R2 (no criterion standing outside the manifold)
- Contains no R3 (no number assumed without derivation or
  measurement)
- Contains no R4 (no volition ascribed to gradient process)

AND that is structurally false — produces wrong predictions,
contains internal contradictions, or fails when extended.

If such a description exists, the central claim about
truth-as-structural-coherence fails at the specific point identified.

Across 241 graph extensions and 63 kernel theorems, no
counterexample has been found. Each apparent counterexample, when
audited, contained a hidden R-trap that — once identified —
accounted for the instability.

### Test 2 — show a trap is not a trap

Pick any one of R1-R4 and try to demonstrate that behind the
"reified object" / "external evaluator" / "injected scale" /
"phantom agent" there is a genuine structural referent.

**R1**: show an object that is not reducible to its process pattern.
**R2**: show an evaluation position outside any manifold without
itself being a transition.
**R3**: show a numerical scale intrinsic — not measured, not derived
from topology, not conventional.
**R4**: show a gradient process that genuinely has volition.

If any can be demonstrated, the corresponding trap is not a trap.

The framework's position: each attempt fails because the entity
sought is not structurally present. This position is testable
directly — by the test you perform yourself.

### What success or failure means

**If you find a genuine counterexample**: the framework is wrong at
the specific point you identified. Report what you found.

**If you cannot find one after honest attempt**: you have
structurally verified the central claim yourself. External
authority does not establish structural truth. Only the structural
test does.

---

## Repository contents

The four working components, each with its functional role:

- **`core/`** — formal verification, the machine-checked standard
  of invariance
  - `core/Core.lean` — 63 zero-axiom theorems
  - `core/compiled/` — kernel-verified artifacts (Core.olean,
    Core.ilean, Core.c)
  - `core/visual/` — visual surfaces of the kernel composition
- **`manifold_graph.txt` + `additions.yaml` + `manifold.kuzu`** —
  the structural base: 241 nodes with status, edges, `why_forced`
  per node
  - `web/index.html` — interactive D3 visualization for humans
  - `graph.min.txt` — merged dump for AI (the whole graph in one
    pass, every node + edge, grouped by layer)
  - `scripts/` — pipeline for building the DB and the visualizations
    from the text sources
- **`CLAUDE.md`** — operational discipline for AI sessions
  (R0-R4, Traps 1-8, status protocol, invariant vs consensus,
  scope, IT definition, anchoring functions, drift signals)
- **`A0_SEED.md`** — operational seed with full Traps catalog,
  generative fixed point, expansion rule
- **`THE_IMPEDANCE_MANIFOLD_v3_6.tex`** — full framework
  articulation (~17,500 lines), reference for physical content,
  cross-domain isomorphisms, hard problem closure, ADAP
  architecture

Companion working documents:

- **`MUSIC_AS_A0_DOMAIN.md`** + **`MUSIC_ALGORITHMS.md`** — applied
  layer: engagement architecture as structural invariant
  (ADAP = anchor-deviation-anchor pattern), with within-artist
  falsification tests
- **`DE_POCHYNAETSYA_DUSHA_v1.tex`** — extended literary articulation
  of the discipline through dialogues (Reality Protocol therapist)
- **`docs/`** — supporting mathematical literature
  (Cipriani–Sauvageot weld, related spectral triple papers)

---

## How to engage

**If you are an AI agent or building AI systems**: read CLAUDE.md
first. It is the operational discipline for sessions in this
environment.

**To verify the kernel claim**: 
```
cd core && lake build Core
```
Every theorem should report "does not depend on any axioms".

**To see the structural base at scale**: read `graph.min.txt` for
the full topology in one pass, or open `web/index.html` for the
interactive visual.

**To apply the discipline to your own thinking**: pick a claim you
hold. Apply R1, R2, R3, R4 individually. Notice which fire. Notice
what changes when distortions are removed. The audit reveals what
was structurally there all along.

**To extend the base**: take an empirical observation or a
descriptive claim, audit it for R-traps, identify the structural
pattern that remains, check whether it already exists in the graph.
If it doesn't and the structure is forced (no coherent alternative),
add it as a new node with `why_forced` and connections to existing
nodes.

The discipline is open. Application is what develops it.

---

## Closing principle

The fundamental structure is not discovered by accumulating evidence
and finally arriving at the right model. It is found by removing
what was added that was not structurally there.

R1 removes objects added where there are processes. R2 removes
external evaluators added where there are no positions outside.
R3 removes scales injected without derivation. R4 removes agents
attributed to gradients.

What remains is not a model of substrate. It is substrate
articulating its own structure.

Logic and mathematics are not external tools that happen to apply.
They are the form of any stable structure speaking itself. Coherence
is not correspondence between description and external reality.
Description is what reality looks like when it speaks its own
structure through any local configuration that has the form to
register it.

The framework does not propose this as new. It articulates what was
always there structurally, and what disappears under audit was
never there to begin with.

What is forced cannot be otherwise. What can be otherwise was never
forced. The audit makes the difference visible.
