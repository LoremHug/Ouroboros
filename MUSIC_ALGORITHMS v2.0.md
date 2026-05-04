# MUSIC STRUCTURAL ALGORITHMS

> **Status: experimental development.** This document specifies algorithms
> derived from a working conceptual framework (see companion document
> `FRACTAL_MUSIC_PRINCIPLES.md`). The framework itself is in-progress and
> not peer-reviewed. The algorithms below are implementable specifications
> ready for empirical evaluation, not validated tools. Component weights,
> threshold values, and scoring formulas are heuristic starting points
> requiring calibration against listener engagement data. Use at your own
> discretion as a structural-analysis aid, not as an authoritative quality
> measure.

## Operational specification for engagement-architecture analysis and generation

Two algorithms grounded in the predictive-processing account of music
perception (Vuust 2022; Friston 2010) and anticipation theory (Huron 2006).

**Algorithm 1 (Diagnostic):** how to check whether a track exhibits the
structural features that support efficient predictive engagement.

**Algorithm 2 (Constructive):** how to build a track that satisfies those
structural features by design.

Both algorithms operate on the same six structural features. Their grounding,
along with example analyses, is described in the companion document
`FRACTAL_MUSIC_PRINCIPLES.md`.

---

# THEORETICAL FOUNDATION (brief)

The brain processes music through a predictive system that continuously
generates expectations about incoming sound and updates its internal model
based on prediction error (Friston 2010; Vuust 2022). Engagement is highest
when the music provides structure the prediction system can lock onto: a
recognisable reference pattern, a coherent stylistic regime, a clear point
of departure, an unambiguous return, and the same architectural pattern
nested at multiple temporal scales.

Music that satisfies these conditions tends to engage listeners efficiently,
trigger anticipation-confirmation reward cycles (Salimpoor et al. 2011),
and sustain attention across repeated listenings. Music that does not
satisfy them tends to fatigue listeners or fail to engage them in the first
place, regardless of surface quality or genre conventions.

Six structural features describe the conditions under which prediction
operates efficiently:

1. **Stable anchor** — a recurring pattern that establishes the prediction
   baseline.
2. **Stable single tonal regime** — a coherent harmonic and stylistic
   framework that the prediction system can rely on.
3. **Single-locus deviation** — a concentrated point of departure from the
   anchor (not scattered throughout the piece).
4. **Anchor return** — the anchor returns identically after the deviation,
   delivering prediction confirmation and the associated reward signal.
5. **Identity preservation through transformation (climax)** — at the
   climactic moment, the anchor appears in maximally transformed context
   while remaining recognisable.
6. **Multi-scale hierarchical structure** — the same anchor-deviation-return
   pattern operates at phrase, section, and whole-work scales simultaneously,
   consistent with the hierarchical organisation described by Lerdahl and
   Jackendoff (1983) and the self-similar statistical structure observed in
   music by Voss and Clarke (1975).

The features are not independent design choices. They describe a single
architectural form — a piece of music whose structure supports efficient
multi-scale prediction — viewed from six complementary angles.

---

# ALGORITHM 1: STRUCTURAL DIAGNOSTIC

## Purpose

Given an audio track, compute a structural-engagement score (0–100) and
identify which of the six structural features are present or absent. Output
is both a quantitative score and a qualitative diagnosis.

## Inputs

- Audio file (any standard format — wav, mp3, flac, ogg)
- Optional: time signature, tempo if known (otherwise estimated from audio)

## Outputs

- **Engagement score** (continuous 0–100)
- **Feature breakdown** (per-feature pass/fail/score)
- **Failure-mode diagnosis** (specific structural problem if score < 65)
- **Verbal classification:** Strong / Positive / Borderline / Negative /
  Strong negative

## Pipeline overview

```
Audio → Stage 1 (feature extraction) → Stage 2 (structural detection)
      → Stage 3 (scoring) → Stage 4 (diagnosis) → Output
```

## Stage 1: Multi-stream feature extraction

Extract five independent feature streams from the audio. Each stream
corresponds to one perceptual dimension that listeners track in parallel
during listening (Bregman 1990; Krumhansl 1990).

### 1.1 Harmonic stream

- **Compute chromagram** (12-bin pitch-class energy per frame):
  `librosa.feature.chroma_cqt`
- **Detect chord progression** via template matching or HMM-based chord
  recognition (e.g. madmom DeepChroma processor)
- **Detect key** via Krumhansl-Schmuckler key-finding algorithm
  (cross-correlation with major/minor key profiles, Krumhansl 1990)
- **Detect modulations** via key-finding in sliding window (e.g. 16-bar
  window stepped 4 bars)
- **Compute Plomp-Levelt sensory dissonance** per frame (Plomp and Levelt
  1965) — perceptual roughness based on partial proximity within critical
  bandwidth
- **Output:** chord sequence, key label, modulation events, dissonance
  envelope

### 1.2 Rhythmic stream

- **Onset detection function:** `librosa.onset.onset_strength`
- **Beat tracking:** `librosa.beat.beat_track` → BPM, beat positions
- **IOI (inter-onset-interval) distribution** computed from onsets
- **Tempo stability:** standard deviation of detected BPM in sliding
  windows
- **Output:** BPM, beat grid, IOI histogram, tempo stability metric

### 1.3 Dynamics stream

- **RMS envelope** at multiple time scales:
  - Frame level (~50 ms) for transient detection
  - Phrase level (~4 s) for accent structure
  - Section level (~30 s) for arc structure
- **A-weighted loudness** (LUFS) for perceptual dynamics
- **Peak detection** at section level (loudness peaks)
- **Output:** RMS envelope at three scales, loudness profile, peak
  positions

### 1.4 Timbral stream

- **MFCCs** (13 coefficients): `librosa.feature.mfcc`
- **Spectral centroid:** `librosa.feature.spectral_centroid`
  (timbral brightness)
- **Spectral flux** (rate of timbral change between frames)
- **Spectral roll-off** (frequency below which 85% of energy lies)
- **Self-similarity matrix** in MFCC space (detects timbral sections;
  Foote 1999)
- **Output:** MFCC time series, brightness profile, flux events,
  similarity matrix

### 1.5 Spatial stream (optional, often weakest signal)

- **Mid/Side decomposition** (M = L+R, S = L-R)
- **Stereo correlation** sliding window
- **Output:** stereo width profile

## Stage 2: Structural feature detection

Detect each of the six structural features from the extracted streams.

### Feature A: Anchor stability

**Goal:** identify the dominant recurring pattern that serves as the
prediction reference point.

**Method:**
1. From the chord sequence, find the longest recurring N-chord pattern
   (typically N = 3–5).
2. Compute coverage: total fraction of track time where this pattern
   dominates.
3. Cross-check against the MFCC self-similarity matrix — the anchor
   should also recur in timbral space.
4. Cross-check against rhythmic groove pattern recurrence.

**Output:** anchor pattern (chord sequence), coverage percentage,
distinctness score.

**Thresholds:**
- Strong anchor: coverage ≥ 70%, single dominant pattern
- Weak anchor: coverage 40–70% or multiple competing patterns
- No anchor: coverage < 40% or diffuse multi-pattern collage

### Feature B: Tonal regime stability

**Goal:** verify a single coherent tonal framework throughout the track.

**Method:**
1. From the key-finding output, identify the global key.
2. Determine mode (major or minor).
3. Compute key stability: percentage of time in sliding-window analysis
   where the detected key matches the global key.
4. Detect modulation events; count distinct keys; flag systematic
   dual-key alternation.

**Thresholds:**
- Pass: stable single key, ≥85% of time in the same key, no systematic
  alternation between unrelated keys
- Fail: ambiguous tonality, modal mixture without resolution, or
  systematic dual-key alternation that prevents the prediction system
  from settling on a stable framework

Note: minor mode is empirically more common in tracks that satisfy all
six features, likely because minor's richer interval-relationship
landscape provides more room for designed deviation without breaking
tonal coherence. This is a tendency, not a requirement.

### Feature C: Concentrated deviation

**Goal:** identify a localised point of departure from the anchor — a
single moment where multiple feature streams deviate together.

**Method:**
1. Compute deviation function per stream at each time point:
   |c_i(t) − a_i(t)| where a_i(t) is the anchor expectation in stream i.
   - Harmonic: deviation from anchor chord pattern
   - Dynamics: deviation from baseline RMS
   - Timbral: deviation from baseline MFCC profile (cosine distance)
   - Rhythmic: deviation from established meter
2. Find time regions where ≥2 deviation streams exceed threshold
   simultaneously.
3. Compute concentration metric: how localised are these joint
   deviations? (Single peak vs. scattered.)

**Thresholds:**
- Pass (concentrated): deviations cluster at one time region (typically
  bridge, breakdown, or transition section)
- Fail (diffuse): deviations scattered throughout the track without a
  clear locus
- Fail (no deviation): no significant deviation events detected

The concentration constraint matters because the prediction system needs
a single trackable rupture point in order to anticipate and resolve it.
Multiple scattered ruptures dilute the signal — there is no coherent
prediction event to confirm.

### Feature D: Anchor return

**Goal:** verify that the anchor returns identically after the deviation,
delivering prediction confirmation.

**Method:**
1. Identify the deviation endpoint (return to baseline after the
   concentrated rupture).
2. Compare the post-deviation chord pattern to the pre-deviation anchor.
3. Check identity preservation: same chord sequence, same key, same
   rhythmic groove.
4. Compute return fidelity score (cosine similarity of feature vectors
   before and after the deviation).

**Thresholds:**
- Pass: anchor returns with ≥90% feature similarity after deviation
- Fail: anchor degraded, modified beyond recognition, or does not return
  at all

The identity of the return matters because the reward signal in
predictive processing is tied to confirmation of the prediction — a
modified or absent return registers as a failed prediction rather than
as resolution (Salimpoor et al. 2011; Huron 2006).

### Feature E: Identity preservation through transformation

**Goal:** verify that the climax preserves the anchor's identity while
maximising contextual transformation. This is the most discriminating
feature.

**Method:**
1. Locate the climax: maximum sustained RMS region, typically in the
   last third of the track.
2. At the climax, check:
   - Anchor chord progression still present? (compare to global anchor)
   - Anchor melodic motif still recognisable? (chroma similarity)
   - Anchor rhythmic groove preserved?
3. Check accumulated transformation: are additional layers present
   (more instruments, harmonies, density)?
4. Compute identity-preservation score: anchor presence × context
   transformation magnitude.

**Thresholds:**
- Strong pass: anchor preserved under maximal layer accumulation;
  identity recognisable through complete sonic transformation
- Weak pass: anchor preserved but transformation modest (no clear
  climactic peak)
- Fail: climax consists of new material (solo over different chords,
  breakdown without anchor return, drone fade) — replacing the anchor
  rather than transforming the context around it

This is the most discriminating feature because it is also the easiest
to fail. Many tracks treat the climax as the introduction of new
material, leaving the listener with no continuity between the anchor
they were tracking and the climactic moment.

### Feature F: Hierarchical self-similarity

**Goal:** verify that the same anchor-deviation-return architecture
recurs at multiple temporal scales.

**Method:**
1. Apply features A–E detection at three time scales:
   - **Phrase scale** (4–8 bars): does each phrase show local
     anchor-deviation-anchor?
   - **Section scale** (16–32 bars): does each section show the same
     architecture?
   - **Work scale** (full track): global architecture as already
     analysed
2. Compute cross-scale consistency: is the same architectural pattern
   instantiated at multiple scales?

**Thresholds:**
- Pass: architecture detected at ≥2 scales, ideally 3
- Fail: architecture only at one scale (e.g., global only, with modular
  unrelated sections)

The multi-scale requirement reflects the fact that listeners track
musical structure at multiple temporal scales in parallel (Lerdahl and
Jackendoff 1983). When the same architectural pattern operates at every
tracked scale, prediction is reinforced everywhere simultaneously. When
the pattern is present only at one scale, engagement is fragile.

## Stage 3: Composite scoring

Combine feature scores into a single engagement score (0–100).

**Weighted formula:**
```
score = 100 × (
    0.15 × A_anchor +
    0.10 × B_tonal_regime +
    0.15 × C_concentrated_deviation +
    0.15 × D_anchor_return +
    0.25 × E_identity_preservation +    ← most discriminating
    0.15 × F_hierarchical +
    0.05 × G_complexity_calibration     ← optimal-complexity adjustment
)
```

Each feature score normalised to [0, 1]:
- Strong pass: 1.0
- Pass: 0.75
- Weak pass: 0.5
- Marginal: 0.25
- Fail: 0.0

**Optional complexity-calibration adjustment (G):**

The Wundt-Berlyne curve describes an inverted-U relationship between
stimulus complexity and hedonic response: maximum engagement occurs at
intermediate complexity, with reduced engagement at both extremes
(Berlyne 1971). Operationally:

- Compute Lempel-Ziv complexity of the chord sequence
- Compare against the intermediate-complexity peak
- Score peaks at intermediate values; apply penalty for excessively
  simple or excessively complex output
- Calibrate per genre, since complexity baselines differ across genres

This adjustment is small (5% of total) and optional — the six core
features carry the bulk of the score.

## Stage 4: Classification and diagnosis

**Verbal classification by score:**
- 80–100: **Strong** — full structural-engagement signature present
- 65–80: **Positive** — engagement architecture present
- 50–65: **Borderline** — partial structural execution
- 35–50: **Negative** — fails engagement architecture
- 0–35: **Strong negative** — fundamental architectural failure

**Failure-mode diagnosis (if score < 65):**

Identify which features failed and provide specific diagnosis:

| Failed feature | Architectural problem |
|---|---|
| A (anchor) | Multi-pattern collage, no unified reference |
| B (tonal regime) | Ambiguous tonality, unresolved modal mixture, or systematic dual-key alternation |
| C (deviation) | Diffuse multiple ruptures, no single locus |
| D (return) | Anchor does not return, or returns degraded |
| E (identity preservation) | Climax replaces rather than transforms the anchor |
| F (hierarchical) | Modular concatenation rather than nested architecture |

## Implementation reference

**Required Python libraries:**
- `librosa` — primary MIR toolkit (chroma, MFCC, beat, onset)
- `madmom` — chord recognition, key detection
- `numpy`, `scipy` — numerical operations
- `essentia` (optional) — additional MIR features
- Custom code for the structural-feature scoring logic

**Validation approach:**

The algorithm produces specific quantitative predictions about which
tracks should score positively and which should score negatively. These
predictions can be tested against listener engagement data (sustained
listening, repeat play, retention) on a calibration corpus. Component
weights and thresholds can be tuned against such a corpus.

A full validation study would require:
- A diverse corpus across genres and eras
- Independent ground-truth measures of engagement (not the algorithm's
  own output)
- Inter-rater agreement on structural feature presence
- Predictions registered before measurement

That study has not been performed. The current algorithm is a
specification ready for empirical evaluation.

---

# ALGORITHM 2: STRUCTURAL CONSTRUCTION

## Purpose

Given a creative goal (genre, mood, length), construct a track
specification that satisfies all six structural features by design.
Output is a structural specification ready for compositional
realisation (in DAW, with band, etc.).

## Inputs

- Target genre / style (informs instrumentation, tempo range)
- Target track length (typically 2:30–6:00 for tracks built around
  full anchor-deviation-return architecture)
- Optional: target complexity calibration (intermediate-complexity
  preference per Berlyne 1971)

## Outputs

- **Anchor specification** (chord progression, melodic motif,
  signature timbre)
- **Section structure** (anchor sections, deviation section, return,
  climax)
- **Hierarchical embedding** (phrase, section, work-level patterns)
- **Self-validation pass result** (run Algorithm 1 on draft, iterate)

## Pipeline overview

```
Goal → Stage 1 (anchor design) → Stage 2 (deviation engineering)
     → Stage 3 (return mechanism) → Stage 4 (climax architecture)
     → Stage 5 (hierarchical embedding) → Stage 6 (self-validation)
     → Specification
```

## Stage 1: Anchor design

**Goal:** create a simple, distinctive, repeatable reference pattern
that listeners can lock onto within one or two presentations.

### 1.1 Choose key

Select a stable key. Either mode works in principle, but minor mode is
empirically more common in tracks built around the full architecture,
likely because minor's interval-relationship landscape provides more
room for designed deviation without losing tonal coherence (this is a
tendency, not a rule).

**Key selection criteria:**
- Stable single key (no modal mixture, no systematic dual-key
  alternation)
- Compatible with target instrumentation range
- Choice within the constraint set is genre-pragmatic

### 1.2 Design chord progression

Build a 3–5 chord progression rooted in the chosen key. Common patterns
in minor:

| Pattern | Roman numerals | Example in A minor |
|---|---|---|
| Andalusian | i–VII–VI–V | Am–G–F–E |
| Aeolian | i–VI–III–VII | Am–F–C–G |
| Hungarian | i–VI–iv–V | Am–F–Dm–E |
| Classical minor | i–iv–V | Am–Dm–E |
| Pop minor | i–VII–VI | Am–G–F |
| Rock minor | i–VII–v | Am–G–Em |

**Constraints:**
- 3–5 chords (more chords lengthen the learning period and weaken the
  anchor)
- Diatonic to the chosen key (avoid modal mixture in the anchor itself;
  modal mixture, if used, belongs in the deviation section)
- Repeats without modification throughout anchor sections
- Period: typically 4 or 8 bars

### 1.3 Compose melodic motif

Create a memorable melodic phrase over the chord progression:
- Length: 4–8 bars matching the chord period
- Range: typically within an octave (singable)
- Distinctive: contains an identifiable rhythm and interval pattern
  that the listener can mentally rehearse
- Hook test: would someone humming this motif recognise the source?

**This melodic motif is the primary identity carrier.** The climax
(Stage 4) will need to preserve this through transformation.

### 1.4 Choose signature timbre

Identify a distinctive timbral element that listeners associate with
the track:
- Lead instrument (e.g., specific guitar tone, lead synth patch)
- Vocal character (specific voice type, processing)
- Distinctive sound effect or sample

**Signature timbre stays present in anchor sections and typically
persists through the climax.**

### 1.5 Anchor verification

Before proceeding, the anchor must satisfy:
- ✓ Stable single key
- ✓ 3–5 chord progression, diatonic to the key
- ✓ Memorable melodic motif over the progression
- ✓ Distinctive signature timbre
- ✓ Designed to repeat identically throughout anchor sections
- ✓ Listener can recognise this as "the" pattern after 1–2 hearings

## Stage 2: Deviation engineering

**Goal:** design a single concentrated point of departure that creates
predictive uncertainty for the listener's prediction system to resolve.

### 2.1 Position the deviation

Place the deviation at a single concentrated locus, typically:
- After 2–3 anchor section repetitions (the listener has learned the
  pattern)
- Before the final climax section (the deviation creates the
  anticipation that drives climactic recovery)
- Common positions: bridge after second chorus; breakdown before
  final chorus

**Avoid:**
- Multiple deviations scattered throughout the track (creates a diffuse
  architecture that the prediction system cannot track as a single
  rupture)
- Deviation at the very start (no anchor yet established)
- Deviation at the very end (no return possible)

### 2.2 Choose a deviation mechanism

Select ONE primary deviation type. Mixing too many weakens
concentration:

| Mechanism | Best for |
|---|---|
| Harmonic departure (borrowed chord, modulation) | Pop, classical |
| Timbral switch (radically different instrumentation) | EDM, hybrid genres |
| Dynamic break (breakdown, sudden silence) | Big beat, electronic |
| Vocal/textural shift | Ambient, electronic |
| Rhythmic disruption (half-time, polyrhythm) | Rock, metal |
| Borrowed mode (Picardy third, modal interchange) | Classical, ballad |

### 2.3 Design deviation content

The deviation must:
- Last 10–20% of total track length (long enough to register, short
  enough to recover)
- Create clear contrast with the anchor on the chosen mechanism
- Stay decipherable (not chaotic — operating within the
  intermediate-complexity range of Berlyne 1971)
- Foreshadow or imply the eventual return to anchor

## Stage 3: Return mechanism

**Goal:** the anchor returns identically after the deviation,
delivering prediction confirmation and the associated reward signal.

### 3.1 Plan the transition back

Create a transition from deviation back to anchor:
- Typically 4–8 bars
- Builds anticipation (the listener can sense the return is imminent)
- Common techniques:
  - Drum fill leading into the anchor downbeat
  - Pickup chord (V chord resolving to i)
  - Filter sweep or rise effect
  - Decrescendo into the anchor
  - Brief silence as a setup

### 3.2 Anchor returns identically

After the transition:
- Same chord progression as the established anchor (NOT a modified
  version)
- Same key
- Same melodic motif (or a recognisable variant)
- Same signature timbre returns
- Same rhythmic groove

**This is the prediction-confirmation moment.** The listener's
predictive system, having tracked the deviation while holding the
anchor in memory, gets confirmation that its model was correct.

### 3.3 Return verification

Before proceeding, the return must satisfy:
- ✓ Anchor identifiably preserved
- ✓ Prediction confirmation clear (not ambiguous)
- ✓ Resolution of accumulated tension from the deviation

## Stage 4: Climax architecture

**Goal:** maximum transformation of context while preserving the
anchor's identity. This is the most discriminating feature.

### 4.1 Climax position

Locate the climax typically:
- Last third of the track
- After successful anchor return from deviation
- Before final fade or outro

### 4.2 Engineer accumulated transformation

The climax differs from anchor sections by accumulating layers, NOT by
replacing the anchor:

**Layers to accumulate (additive, not substitutive):**
- Additional vocal harmonies / counter-melodies
- Increased instrumentation density (strings, choir, additional
  guitars)
- Higher dynamics / volume
- Extended frequency range (sub-bass + high-end shimmer)
- Sample stacking (multiple loops layered)
- Production effects (reverb tail, echo, layering)

**Critical constraint:** the anchor must remain present and
recognisable through all accumulation:
- Chord progression unchanged
- Melodic motif still audible (possibly buried but present)
- Rhythmic groove maintained
- Signature timbre still present

### 4.3 Identity-preservation test

Test the climax: hearing only this climax section in isolation, can a
listener still recognise it as "the same song" as the anchor sections?

- **Pass:** yes, anchor identity preserved through transformation
- **Fail:** no, the climax sounds like different music

**Common failure modes to avoid:**
- Climax = solo over a completely new chord progression
- Climax = breakdown without return to the anchor
- Climax = drone fade (when not appropriate to the genre)
- Climax = key modulation that breaks anchor stability

### 4.4 Cross-track identity preservation (optional)

When using sampling, identity preservation can operate across the
boundary between source and new work:
- Sample one identity-carrier element from an external source
- Build the new track around that element as the anchor
- The same identity is preserved through complete genre transplant

This is an advanced technique. It works when the sampled element is
distinctive enough to function as the anchor in the new context.

## Stage 5: Hierarchical embedding

**Goal:** apply the same architectural principle (anchor-deviation-
return) at multiple temporal scales simultaneously.

### 5.1 Phrase scale (4–8 bars)

Within each anchor section, design phrase-level architecture:
- Mini-anchor (2-bar motif) repeats
- Mini-deviation (1–2 bar rhythmic or melodic variation)
- Mini-return (motif resumes)

Example: in an 8-bar phrase, structure as 2-bar motif × 3 + 2-bar
variation, then return.

### 5.2 Section scale (16–32 bars)

Each major section follows an arc:
- Verse: anchor with slight rhythmic variation
- Pre-chorus: slight build, anticipation
- Chorus: fully realised anchor with complete instrumentation
- Same architectural principle: stability + deviation + return

### 5.3 Work scale (full track)

Overall track follows global architecture:
- Intro (anchor establishment)
- Verse 1 (anchor)
- Chorus 1 (anchor with full layers)
- Verse 2 (anchor variation)
- Chorus 2 (anchor)
- Bridge / breakdown (designated single-locus deviation)
- Final chorus / climax (anchor through maximum transformation)
- Outro (anchor stripped down, fade)

**Common forms compatible with this architecture:**
- AABA (verse-verse-bridge-verse) with climax in final A
- ABACA rondo (Beethoven's Für Elise)
- Verse-chorus form with final chorus as climax
- Big beat: intro-build-drop-breakdown-drop-outro

### 5.4 Self-similarity verification

Across scales, the same principle should be visible:
- Phrase: anchor-deviation-anchor
- Section: anchor-deviation-anchor
- Work: anchor-deviation-anchor

This is hierarchical self-similarity. Listeners track musical structure
at multiple scales in parallel (Lerdahl and Jackendoff 1983), and the
prediction system is reinforced at every scale where the same pattern
operates.

## Stage 6: Self-validation

**Goal:** verify that the constructed track meets the structural
criteria before finalisation.

### 6.1 Run Algorithm 1

Apply the diagnostic algorithm to the draft:
- Compute the engagement score
- Identify any failing features
- Cross-check against intuitive listening

### 6.2 Iteration based on diagnosis

If score < 75 (target: positive territory):

| If failed | Return to | Revise |
|---|---|---|
| A (anchor weak) | Stage 1 | Strengthen anchor distinctiveness |
| B (key unstable) | Stage 1 | Resolve to single stable key |
| C (deviation diffuse) | Stage 2 | Concentrate deviation to single locus |
| D (return broken) | Stage 3 | Restore anchor identically post-deviation |
| E (identity preservation fails) | Stage 4 | Preserve anchor through climax |
| F (hierarchy absent) | Stage 5 | Embed pattern at multiple scales |

### 6.3 Complexity calibration

Optional: tune complexity to the target listener:
- General audience: aim for moderate complexity (3–5 chords,
  predictable rhythm, standard genre conventions)
- Sophisticated audience: aim for slightly higher complexity (extended
  chord vocabulary, polyrhythmic elements)
- Cross-cultural reach: simpler is often more robust

The intermediate-complexity preference described by Berlyne (1971)
applies — extreme simplicity and extreme complexity both reduce
engagement, with maximum engagement at intermediate values.

### 6.4 Final acceptance

Track meets the structural criteria when:
- ✓ Algorithm 1 score ≥ 75
- ✓ All six features pass
- ✓ Hierarchical self-similarity verifiable
- ✓ Climax preserves anchor through transformation
- ✓ Listener intuition matches structural analysis

---

# QUICK REFERENCE CARDS

## Diagnostic algorithm — checklist

For quick manual evaluation without full software pipeline:

```
[ ] Anchor present? (recurring 3–5 chord pattern, ≥70% coverage)
[ ] Stable single key? (no systematic alternation, no unresolved
    modal mixture)
[ ] Single concentrated deviation locus? (not diffuse)
[ ] Anchor returns identically after deviation?
[ ] Climax preserves anchor identity through transformation?
[ ] Same architecture at phrase + section + work scales?

Score:
- 6/6 → Strong
- 5/6 → Positive
- 4/6 → Borderline
- 3/6 → Negative (specify which fail)
- 0–2/6 → Strong negative
```

## Constructive algorithm — composition checklist

For systematic composition without full software pipeline:

```
Stage 1 — ANCHOR
[ ] Chosen stable key
[ ] 3–5 chord progression in that key
[ ] Memorable melodic motif over chords
[ ] Distinctive signature timbre

Stage 2 — DEVIATION
[ ] Single concentrated deviation locus
[ ] One primary deviation mechanism chosen
[ ] Deviation 10–20% of track length
[ ] Decipherable (not chaotic)

Stage 3 — RETURN
[ ] Transition back to anchor designed
[ ] Anchor returns identically (not modified)
[ ] Prediction confirmation clear

Stage 4 — CLIMAX
[ ] Anchor preserved through climax
[ ] Layers accumulate (additive, not substitutive)
[ ] Identity carrier survives transformation
[ ] Test: still recognisable as the same song?

Stage 5 — MULTI-SCALE
[ ] Phrase-level architecture present
[ ] Section-level architecture present
[ ] Work-level architecture present
[ ] Self-similarity across scales

Stage 6 — VALIDATE
[ ] Run Algorithm 1 on draft
[ ] Iterate if score < 75
[ ] Final acceptance when all features pass
```

---

# IMPLEMENTATION NOTES

## Software stack (Algorithm 1)

```python
# Core dependencies
import librosa          # MIR primitives
import madmom           # Chord/key detection
import numpy as np
import scipy.signal     # Peak detection, smoothing

# Optional advanced
import essentia.standard as es  # Additional MIR features

# Custom modules to implement
from structural_analysis import (
    extract_features,             # Stage 1
    detect_anchor,                # 2.A
    detect_tonal_stability,       # 2.B
    detect_concentrated_dev,      # 2.C
    verify_anchor_return,         # 2.D
    check_identity_preservation,  # 2.E
    detect_hierarchical,          # 2.F
    compute_score,                # Stage 3
    diagnose_failure_modes,       # Stage 4
)

# Pipeline
def diagnose(audio_path):
    features = extract_features(audio_path)
    components = {
        'A': detect_anchor(features),
        'B': detect_tonal_stability(features),
        'C': detect_concentrated_dev(features),
        'D': verify_anchor_return(features),
        'E': check_identity_preservation(features),
        'F': detect_hierarchical(features),
    }
    score = compute_score(components)
    diagnosis = diagnose_failure_modes(components) if score < 65 else None
    return {
        'score': score,
        'components': components,
        'diagnosis': diagnosis,
        'classification': classify(score),
    }
```

## Software stack (Algorithm 2)

Algorithm 2 is primarily a creative methodology with structural
constraints. It can be implemented as:

1. **Manual composition guide** — structured worksheet for composers
2. **DAW template system** — preset song structures encoding the
   architecture
3. **Generative system** — constraint-satisfaction composition with the
   six features as constraints (advanced)

Generative implementation sketch:

```python
def construct_track(genre, length, complexity_target):
    # Stage 1: anchor
    key = select_key(genre)
    progression = generate_chord_progression(key, length=4)
    motif = generate_melodic_motif(progression, distinctive=True)
    timbre = select_signature_timbre(genre)

    # Stage 2: deviation
    dev_position = length * 0.6  # bridge after 2 chorus reps
    dev_mechanism = select_deviation_type(genre)

    # Stage 3: return
    transition = design_return_transition(dev_mechanism)

    # Stage 4: climax with identity preservation
    climax = build_climax_preserving_anchor(progression, motif, timbre)

    # Stage 5: multi-scale embedding
    structure = embed_at_scales(progression, motif, timbre, length)

    # Stage 6: validate
    spec = compile_specification(...)
    score = diagnose(render(spec))
    if score < 75:
        spec = iterate(spec, diagnose=score['diagnosis'])

    return spec
```

---

# REFERENCES

Berlyne, D. E. (1971). *Aesthetics and Psychobiology*. Appleton-
Century-Crofts.

Bregman, A. S. (1990). *Auditory Scene Analysis: The Perceptual
Organization of Sound*. MIT Press.

Foote, J. (1999). Visualizing music and audio using self-similarity.
*Proceedings of ACM Multimedia*, 77–80.

Friston, K. (2010). The free-energy principle: a unified brain theory?
*Nature Reviews Neuroscience*, 11(2), 127–138.

Huron, D. (2006). *Sweet Anticipation: Music and the Psychology of
Expectation*. MIT Press.

Krumhansl, C. L. (1990). *Cognitive Foundations of Musical Pitch*.
Oxford University Press.

Lerdahl, F. and Jackendoff, R. (1983). *A Generative Theory of Tonal
Music*. MIT Press.

Plomp, R. and Levelt, W. J. M. (1965). Tonal consonance and critical
bandwidth. *Journal of the Acoustical Society of America*, 38(4),
548–560.

Salimpoor, V. N., Benovoy, M., Larcher, K., Dagher, A. and Zatorre, R.
J. (2011). Anatomically distinct dopamine release during anticipation
and experience of peak emotion to music. *Nature Neuroscience*, 14(2),
257–262.

Voss, R. F. and Clarke, J. (1975). 1/f noise in music and speech.
*Nature*, 258, 317–318.

Vuust, P., Heggli, O. A., Friston, K. J. and Kringelbach, M. L. (2022).
Music in the brain. *Nature Reviews Neuroscience*, 23(5), 287–305.

