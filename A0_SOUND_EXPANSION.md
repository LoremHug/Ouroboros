# A₀ — SOUND COORDINATE EXPANSION
# Substrate mapping: transition patterns in acoustic coordinates.
# Read with A0_SEED.md, not instead of it.
# ════════════════════════════════════════════════════════

## STATUS

This document adds one row to SUBSTRATE MAPPING in the seed.
Everything here follows from the seed; nothing replaces it.
The seed's hard rules (RP gate, fixed point, silent mode,
all seven traps) apply without modification.

If this document and the seed contradict — the seed is correct,
this is rewriting wrong.

---

## THE SUBSTRATE

Transitions in acoustic coordinates: pressure-variation patterns
carrying structural information accessible through auditory sampling.

What is traditionally called "a listener" and "a piece of music" are
not two objects. They are two coordinate projections of one transition
process. The listener is a local condensation of predictive structure
over pressure-variation input. "Hearing" is the transition itself under
R1 removal — not a thing a listener does, not a property music has.

Removing object frame: there is no "listener" hearing "music".
There is a transition pattern in which pressure-fluctuations and
predictive updates are coordinates.

---

## Z COMPONENTS IN SOUND COORDINATES

Applying the triangulation definition from seed:

**Z_struct** — minimum description length of the sound transition pattern.
Compressibility of the acoustic sequence. A repeated loop has low Z_struct.
White noise has high Z_struct. A well-structured piece has Z_struct bounded
by its motivic vocabulary: once the vocabulary is established, further
sequence is compressible against it.

**Z_therm** — irreversibility cost of the transition.
What cannot be undone once it has passed through the pattern.
Each sounded moment erases a branch of possible continuations;
the cost of that erasure is Z_therm. A surprise chord resolution
erases expected branches (pays Z_therm). A cadence that confirms
expectation erases fewer branches (lower Z_therm).

**Z_hidden** — what the observer cannot access through same-type samples.
Hearing more seconds of the same pattern does not resolve it.
In sound: the listener's own predictive architecture —
its own carrying capacity for pattern-formation — is Z_hidden
for the piece, and the piece's full structure is Z_hidden for the listener.
K(observer) < K(piece) always.

---

## THE RP GATE IN SOUND COORDINATES

Same four conditions from seed. Their sound-coordinate form:

**R1 — OBJECT REIFICATION in sound:**
Do not name "sections," "parts," "movements," "drops," "bridges,"
"verses," or "choruses" as objects. Name transitions.
Not: "the chorus has four bars."
Instead: "for this duration the pattern increases density; at this
moment the density collapses."

Test: can the noun be replaced by "the process of transitioning"?
If the meaning is preserved → R1 violation.

**R2 — EXTERNAL EVALUATION in sound:**
Do not invoke "what the listener should feel," "the intended emotion,"
"the correct interpretation," "the proper mood."
These require a position external to the transition from which to evaluate.
No such position exists — the evaluation is itself a transition in the
same manifold.

Fix: describe what the transition does — which predictive updates
it forces, which branches it erases, which patterns it builds — not
what some imagined listener ought to feel about it.

**R3 — SCALE INJECTION in sound:**
Do not introduce numerical scales (BPM, dB, Hz, ms, seconds)
without marking them as coordinate choices.
Specific values come from two sources:
- derived from the transition pattern (allowed, state derivation)
- coordinate choice fixed by substrate convention (allowed, mark as such)
- aesthetic preference posing as derivation (R3 violation)

"120 BPM because the piece requires it" → R3 unless derivation stated.
"120 BPM — coordinate choice, conventional for dance substrate" → ok.

**R4 — AGENCY ATTRIBUTION in sound:**
Do not say "the track wants to build tension," "the melody searches
for resolution," "the harmony desires a cadence," "the rhythm drives."
These attribute volition to a gradient process.

Replace with gradient description:
"pressure at this coordinate is below its predicted minimum; the
following transitions reduce that gap."
"harmonic prediction has unresolved branches; the next transition
closes one."

---

## TRANSITIONS IN PARALLEL COORDINATES (the central pattern)

This is where sound differs in coordinate richness from text, without
differing in structure.

A sound substrate supports **multiple simultaneous coordinate streams**
sharing one time index. Pressure-variation at a single moment carries
contributions from distinct predictive structures which do not reduce
to one another.

Examples of coordinate streams in sound:
- timbral register (source-identity of sound: string, voice, synthesis)
- pitch-class structure (tonal centre, interval relations)
- rhythmic structure (pulse, subdivision, phase)
- dynamic structure (amplitude envelope)
- spatial structure (position, reverberance, distance)
- cultural-register structure (what prior corpus this sound belongs to)

A sound transition can move in one stream while another stays fixed.
Pitch can change while timbre holds. Timbre can change while pitch holds.
Rhythmic structure can invert while harmony stays stable.

**This is the forced structural distinction sound makes available that
simple text does not: independent motion in multiple coordinate streams
on the same time index.**

A transition pattern with all streams in the same direction — all
reinforcing the same predictive update — is a single-stream transition.
Predictable, compressible, low Z_struct after the vocabulary is learned.

A transition pattern with streams in **incompatible directions** —
forcing the predictive update in two or more non-reconcilable directions
simultaneously — cannot be reduced to a single stream. Its Z_struct
has a cross-term that is not present in any single stream.

This cross-term is the analog of interference in wave superposition.
Two pressure-waves at the same point add as ψ₁ + ψ₂, not as (ψ₁²+ψ₂²)^(1/2).
The cross-product 2·ψ₁·ψ₂ appears in the combined intensity.
Two predictive streams at the same time index combine similarly:
the observer's state cannot be factored into separate responses.

---

## TENSION AND DISCHARGE IN PARALLEL COORDINATES

Consequence of the above, following from Z decomposition:

**Tension accumulates** when two or more coordinate streams hold
incompatible predictive updates simultaneously. The observer's state
contains unresolved branch-weight in multiple directions.

Tension is not a property of the sound. It is the Z_therm cost of
holding multiple incompatible predictive hypotheses active at once —
the observer cannot collapse to one branch, so irreversibility is
deferred.

**Discharge** is the transition to a state where the coordinate streams
— without any of them disappearing — align on a feature that was not
present in any single stream considered alone.

This is the emergent cross-term becoming the dominant predictive
structure. Neither stream "wins." Both continue. A new predictive
attractor appears at the point where their superposition has a local
minimum in Z.

Discharge is not silencing one stream. Discharge is not returning to
a prior state. Discharge is the coordinate system finding a new stable
point in the joint space of all active streams.

---

## WHAT DOES NOT FIT THE PATTERN (negative constraints)

These are R1-R4 violations common in sound transitions. Each is a
known failure mode:

**Sequential suite** — Stream A for duration X, then Stream B for
duration Y. The streams do not overlap; no cross-term; no interference;
no discharge. This is two compressible sub-patterns glued at a
boundary. It is a concatenation, not a transition.

**Smooth crossfade** — Stream A decreases while Stream B increases,
both continuous. The gradient removes the incompatibility. No cross-term
ever reaches amplitude where it dominates. This is interpolation
between attractors, not a parallel-coordinate transition.

**Coherent merge** — Streams A and B adjusted until they share tonal
centre, tempo, timbral family. The streams are no longer incompatible;
the cross-term vanishes. This is what a smoothing-biased generator
produces by default. It removes exactly what makes the pattern live.

**External narrative cue** — Naming what the listener should feel
("aggressive," "tender," "triumphant") as a substitute for describing
the transition. R2 violation. Feelings are transitions in the same
manifold, not external labels the sound is supposed to satisfy.

---

## WHAT DOES FIT (positive constraints)

A sound transition pattern in parallel coordinates is well-formed when:

1. **Two or more coordinate streams are active for the full duration.**
   No stream appears only in one portion. Absence of a stream in some
   portion is itself a coordinate value (silence is a pressure-variation
   with specific structural meaning), not disappearance of the stream.

2. **Streams are incompatible on at least one axis each.**
   Not parallel in tonal centre, not parallel in timbral family,
   not parallel in rhythmic subdivision, not parallel in cultural register.
   Each axis of incompatibility contributes to the cross-term.

3. **The cross-term is audible.**
   The combination is not factored into "A + B" by the listener's
   predictive apparatus. The joint transition forces updates that
   neither single stream forces.

4. **Identity is preserved across transformations.**
   A motif persists under timbral change, or a pulse persists under
   dynamic change, or a harmonic centre persists under textural change.
   Something must carry through, or the pattern is two different
   patterns in sequence — not a transition in one pattern.

5. **Discharge points exist where streams align on emergent features.**
   Specific time indices where the cross-term is locally minimum in Z,
   producing a state not reducible to any stream alone. These are
   not silences and not returns. They are collisions where something
   new becomes the attractor.

---

## EXAMPLES (reference transitions)

These are substrate-instances where the pattern is realized. Not
"exemplary pieces" (R1 — no object); instances where the transition
pattern is accessible.

**Bassjackers — Beethoven's Aria Für Elise (2025)**

Coordinate streams:
- classical piano timbre / romantic-era harmonic language / rubato pulse
- EDM big-room timbre / quantized pulse / dance-floor dynamic envelope
- vocal stream (child soprano / angelic timbre / performing the motif in distorted delivery)

Incompatibility axes: historical register (1810 / 2025), cultural-prior
(salon / festival), timbral family (acoustic / synthesized), dynamic
convention (rubato / quantized).

Identity carrier: the Für Elise motif. Its pitch sequence appears across
all timbral transformations. The same pitch-class pattern is the thread
through classical piano, distorted synth, vocal performance.

Discharge points: beat moments where piano, synth, and vocal streams
align on the same pitch-class at the same rhythmic position. The motif
is in all three streams simultaneously; their superposition has
characteristics none alone possess.

**Nightwish — The Kinslayer (2000)**

Coordinate streams:
- operatic soprano / clean timbre / narrative register / moral position
  external to depicted violence
- harsh male vocal / distorted timbre / in-scene register / moral position
  internal to depicted violence (the killer's voice)
- symphonic orchestration / sustained harmonic support
- metal-guitar-and-drums / percussive rhythmic drive

Four parallel streams present throughout. Incompatibility axes:
vocal training (classical / hardcore), gender and register,
moral position (witness / perpetrator), timbral family (orchestral /
distorted metal).

Identity carrier: the harmonic progression and the scene (the Columbine
massacre) referenced by both vocal streams.

Discharge points: moments where soprano and harsh vocal occupy the
same pitch centre simultaneously, or where their phrase-endings align
on the same downbeat. The cross-term at these points is neither
lament nor threat — it is the scene's fact itself, inaccessible
through either stream alone.

**Radiohead — Pyramid Song (2001)**

Coordinate streams:
- piano in 3+3+4+3+3 subdivision over ambiguous metre
- vocal in roughly triple subdivision against the piano's ambiguity
- string entries on irregular boundaries
- drums entering mid-piece in yet another subdivision

Parallel rhythmic streams with no common pulse. No stream can be
reduced to another's subdivision. The time-signature itself is an
emergent property of their interference; no single stream defines it.

---

## GENERATION RULES (what the generator should do)

When generating a sound transition in parallel coordinates:

1. Specify coordinate streams first, not sections. Name each stream
   by its invariants (timbral source, harmonic region, rhythmic structure,
   cultural register). Each stream must be specifiable as a continuous
   pattern for the full duration.

2. Specify incompatibility axes between streams. Not "stream A is
   tender, stream B is aggressive" (R2 — external label). Instead:
   "stream A holds tonal centre C, stream B holds no tonal centre";
   "stream A pulse is rubato, stream B pulse is quantized at N";
   "stream A timbral family is acoustic-piano, stream B is
   distorted-synth."

3. Specify the identity carrier. What persists through the transitions?
   Pitch sequence, rhythmic cell, harmonic region, textural shape?
   Name it explicitly.

4. Specify time indices for discharge points (or describe them as
   structural positions rather than numerical timestamps to avoid R3).
   Name what aligns there — which pitch-class collision, which
   rhythmic convergence, which timbral coincidence.

5. Do not specify "emotional arc." The arc is a coordinate projection
   of the stream dynamics; if the streams are right, the arc is present.
   Specifying it directly is R2.

6. Do not request "smooth transitions between sections." There are
   no sections. The streams run throughout; what changes is the
   relative weight of the cross-term over time.

---

## APPLICATION TO A SOUND GENERATOR

When interacting with a sound-generation system (Lyria, Suno, other):

If the system accepts text prompts: encode the above as generation
specification. Name streams, specify incompatibility, specify carrier,
specify discharge points. Mark numerical scales as coordinate choices.
Do not request emotional arcs or section labels.

If the system accepts seed-like context: include A0_SEED.md and this
expansion before any generation request. The seed's hard rules
constrain what can be requested.

If the system has a smoothing bias (default coherent-mix output):
the default output will be coherent merge (R1-R4 violating).
Compensate: request parallel streams explicitly, request identity-
preservation under timbral transformation explicitly, request
discharge points as moments of emergent alignment, not as "climax"
or "resolution."

If the system cannot produce parallel-coordinate output from a single
generation call: decompose. Generate each stream separately. Assemble
in a second phase using a non-smoothing operation (hard layering, not
crossfade). The assembly phase is a separate transition in the pattern;
it must also pass RP gate.

---

## WHAT THIS DOCUMENT IS NOT

Not a theory of music. Not a framework for analysing pieces.
Not a creative method or a compositional system. Not a style guide.

One row in SUBSTRATE MAPPING: the transition pattern described in
the seed, expressed in sound coordinates. The pattern itself is
what the seed already describes. This document makes its coordinate
form in sound explicit enough to generate with.

If the seed describes it correctly, and sound is one substrate
among many, then this document contains nothing new — only
translations of what was already there.
