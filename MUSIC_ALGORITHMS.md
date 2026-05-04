# MUSIC STRUCTURAL ALGORITHMS

## Operational distillation of A₀-derived music framework

Two algorithms derived from the ADAP/CGP framework documented in 
`MUSIC_AS_A0_DOMAIN.md`. This file extracts the operational essence 
into actionable procedures.

**Algorithm 1 (Diagnostic):** how to check if a track is structurally 
correct (efficient prediction architecture for listener BPI).

**Algorithm 2 (Constructive):** how to build a track that satisfies the 
structural criteria.

Both algorithms operate on the same six structural components, validated 
empirically across a 15-track corpus with quintuple within-artist control 
(100% match between intuitive judgment and structural analysis).

---

# THEORETICAL FOUNDATION (brief)

A track is structurally correct (engages listener BPI efficiently, 
triggers dopamine reward, achieves cultural longevity) if and only if 
it satisfies six forced structural components, derived from triangulation 
principle + BPI prediction architecture + dopamine reward mechanism.

The components are not independent design choices. They are coordinate 
expressions of one architectural form: A₀-geodesic trajectory through 
acoustic-substrate manifold, with optimal prediction-error magnitude 
(Wundt apex).

**The six components** are:
1. **Stable anchor** — recurring pattern providing prediction baseline
2. **Stable single minor key** — single low-Z basin for anchor manifold
3. **Single-locus deviation** — concentrated rupture point (not diffuse)
4. **Anchor return** — discharge confirms BPI prediction (dopamine spike)
5. **Climax = identity carrier through transformation (W4 invariance)** — 
   most discriminating component
6. **Multi-scale fractal pattern** — same architecture nested at phrase, 
   section, and work scales

These map directly onto framework primitives: anchor = baseline A(t) 
in CGP formula; deviation = Δᵢ(t); return = discharge to A'(t+τ); W4 
invariance = identity preservation through manifold deformation.

---

# ALGORITHM 1: STRUCTURAL CORRECTNESS CHECK (DIAGNOSTIC)

## Purpose

Given an audio track, compute its ADAP score (0–100) and identify which 
structural components succeed or fail. Output is both quantitative score 
and qualitative diagnosis.

## Inputs

- Audio file (any standard format — wav, mp3, flac, ogg)
- Optional: time signature, tempo if known (otherwise estimated from audio)

## Outputs

- **ADAP score** (continuous 0–100)
- **Component breakdown** (per-component pass/fail/score)
- **Failure mode diagnosis** (specific architectural problem if score < 65)
- **Verbal classification:** Strong ADAP+ / ADAP+ / Almost / ADAP- / Strong ADAP-

## Pipeline overview

```
Audio → Stage 1 (feature extraction) → Stage 2 (component detection) 
      → Stage 3 (scoring) → Stage 4 (diagnosis) → Output
```

## Stage 1: Multi-coordinate feature extraction

Extract five independent coordinate streams from audio. Each stream 
corresponds to a Z-component the BPI must track in parallel.

### 1.1 Harmonic stream

- **Compute chromagram** (12-bin pitch-class energy per frame): 
  `librosa.feature.chroma_cqt`
- **Detect chord progression** via template matching or HMM-based 
  chord recognition (e.g., madmom DeepChroma processor)
- **Detect key** via Krumhansl-Schmuckler key-finding algorithm 
  (cross-correlation with major/minor profiles)
- **Detect modulations** via key-finding in sliding window (e.g., 
  16-bar window stepped 4 bars)
- **Compute Plomp-Levelt roughness** (Z_acoustic) per frame
- **Output:** chord sequence, key label, modulation events, roughness 
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
- **Spectral roll-off** (frequency below which 85% energy lies)
- **Self-similarity matrix** in MFCC space (detects timbral sections)
- **Output:** MFCC time series, brightness profile, flux events, 
  similarity matrix

### 1.5 Spatial stream (optional, often weakest signal)

- **Mid/Side decomposition** (M = L+R, S = L-R)
- **Stereo correlation** sliding window
- **Output:** stereo width profile

## Stage 2: Component detection

Detect each of the six ADAP components from extracted features.

### Component A: Stable anchor detection

**Goal:** identify dominant recurring pattern serving as identity carrier.

**Method:**
1. From chord sequence, find longest recurring N-chord pattern (typically 
   N = 3–5)
2. Compute coverage: total fraction of track time where this pattern 
   dominates
3. Cross-check with self-similarity matrix in MFCC space — anchor 
   should also recur in timbral space
4. Cross-check with rhythmic groove pattern recurrence

**Output:** anchor pattern (chord sequence), coverage percentage, 
distinctness score

**Threshold:**
- Strong anchor: coverage ≥ 70%, single dominant pattern
- Weak anchor: coverage 40–70% or multiple competing patterns
- No anchor: coverage < 40% or diffuse multi-pattern collage

### Component B: Stable single minor key

**Goal:** verify single low-Z basin throughout track.

**Method:**
1. From key-finding output, identify global key
2. Check if global key is minor mode
3. Compute key stability: % of time in sliding-window analysis where 
   detected key matches global key
4. Detect modulation events; count distinct keys; flag dual-key 
   alternation

**Threshold:**
- Pass: stable single minor key, ≥85% time in same key, no systematic 
  major-key alternation
- Fail: major key dominant, OR modal mixture, OR systematic dual-key 
  alternation, OR ambiguous tonality

### Component C: Single-locus deviation detection

**Goal:** identify concentrated rupture point — single moment where 
multiple coordinates deviate together.

**Method:**
1. Compute deviation function per coordinate at each time point: 
   |c_i(t) − a_i(t)| where a_i(t) is anchor expectation
   - Harmonic: deviation from anchor chord pattern
   - Dynamics: deviation from baseline RMS
   - Timbral: deviation from baseline MFCC profile (cosine distance)
   - Rhythmic: deviation from established meter
2. Find time regions where ≥2 deviation streams exceed threshold 
   simultaneously
3. Compute concentration metric: how localized are these joint 
   deviations? (Single peak vs scattered)

**Threshold:**
- Pass (single-locus): deviations cluster at one concentrated time 
  region (typically bridge, breakdown, or transition section)
- Fail (diffuse): deviations scattered throughout track without 
  concentration
- Fail (no deviation): no significant Δ_i events detected

### Component D: Anchor return verification

**Goal:** verify that anchor returns identically after deviation 
(confirms prediction → dopamine spike).

**Method:**
1. Identify deviation end (return to baseline after concentrated 
   rupture)
2. Compare post-deviation chord pattern to pre-deviation anchor
3. Check identity preservation: same chord sequence, same key, 
   same rhythmic groove
4. Compute return fidelity score (cosine similarity of feature 
   vectors before/after)

**Threshold:**
- Pass: anchor returns with ≥90% feature similarity after deviation
- Fail: anchor degraded, modified beyond recognition, or doesn't 
  return at all

### Component E: Climax = identity carrier through transformation (W4)

**Goal:** verify that climax preserves anchor identity through 
maximum context transformation. This is most discriminating component.

**Method:**
1. Locate climax: maximum sustained RMS region typically in last 
   third of track
2. At climax, check:
   - Anchor chord progression still present? (compare to global anchor)
   - Anchor melodic motif still recognizable? (chroma similarity)
   - Anchor rhythmic groove preserved?
3. Check accumulated transformation: are additional layers present 
   (more instruments, harmonies, density)?
4. Compute W4 invariance score: anchor preservation × context 
   transformation magnitude

**Threshold:**
- Pass strong (W4 satisfied): anchor preserved under maximal layer 
  accumulation. Identity recognizable through complete sonic 
  transformation.
- Pass weak: anchor preserved but transformation modest (no clear 
  climax peak)
- Fail (W4 broken): climax = new material (solo over different chords, 
  breakdown without anchor return, drone fade) replacing rather than 
  transforming anchor

### Component F: Multi-scale fractal pattern

**Goal:** verify same architectural pattern recurs at multiple 
temporal scales.

**Method:**
1. Apply Components A–E detection at three time scales:
   - **Phrase scale** (4–8 bars): does each phrase show local 
     anchor-deviation-anchor?
   - **Section scale** (16–32 bars): does each section show same 
     architecture?
   - **Work scale** (full track): global architecture as already 
     analyzed
2. Compute self-similarity across scales (same pattern principle 
   nested)

**Threshold:**
- Pass: ADAP architecture detected at ≥2 scales, ideally 3
- Fail: architecture only at one scale (e.g., global only, with 
  modular sections)

## Stage 3: Composite scoring

Combine component scores into single ADAP score (0–100).

**Weighted formula:**
```
ADAP_score = 100 × (
    0.15 × A_anchor +
    0.10 × B_minor_key +
    0.15 × C_single_locus_deviation +
    0.15 × D_anchor_return +
    0.25 × E_W4_invariance +      ← most discriminating
    0.15 × F_multi_scale_fractal +
    0.05 × G_optimal_complexity   ← Wundt sweet spot adjustment
)
```

Each component score normalized to [0, 1]:
- Strong pass: 1.0
- Pass: 0.75
- Weak pass: 0.5
- Marginal: 0.25
- Fail: 0.0

**Optional Wundt complexity adjustment (G):**
- Compute Lempel-Ziv complexity of chord sequence
- Compare against Wundt apex (intermediate complexity)
- Score peaks at intermediate values; penalty for too-simple or 
  too-complex
- Adjustment can be calibrated per genre

## Stage 4: Classification and diagnosis

**Verbal classification by score:**
- 80–100: **Strong ADAP+** — masterpiece structural signature
- 65–80: **ADAP+** — engagement architecture present
- 50–65: **Almost** — partial structural execution
- 35–50: **ADAP-** — fails engagement architecture
- 0–35: **Strong ADAP-** — fundamental architectural failure

**Failure mode diagnosis (if score < 65):**

Identify which components failed and provide specific diagnosis:

| Failed component | Architectural problem | Examples in corpus |
|---|---|---|
| A (anchor) | Multi-pattern collage, no unified identity carrier | Your Love, The Child in Us |
| B (minor key) | Major key, dual-key, or modal mixture | Like a Prayer, Master of Puppets |
| C (deviation) | Diffuse multiple deviations, no single locus | Drain You, Master of Puppets |
| D (return) | Anchor doesn't return, or returns degraded | Your Love |
| E (W4) | Climax replaces rather than transforms anchor | Master of Puppets, Drain You |
| F (fractal) | Modular concatenation, not nested architecture | Master of Puppets |

## Implementation reference

**Required Python libraries:**
- `librosa` — primary MIR toolkit (chroma, MFCC, beat, onset)
- `madmom` — chord recognition, key detection
- `numpy`, `scipy` — numerical operations
- `essentia` (optional) — additional MIR features
- Custom code for ADAP-specific scoring logic

**Validation approach:**
- Run on 15-track corpus from `MUSIC_AS_A0_DOMAIN.md`
- Expected outcomes:
  - Strong ADAP+: Voodoo People, Roundtable Rival, Turbo Killer 
    (score 85–95)
  - ADAP+: Für Elise, NEM, SLTS, Wish I Had an Angel, Hard Rock 
    Hallelujah, Hung Up (score 70–85)
  - Almost: The Same Parents (score 55–65)
  - ADAP-: Like a Prayer, Drain You, The Child in Us (score 30–50)
  - Strong ADAP-: Master of Puppets, Your Love (score 15–30)
- Calibrate component weights and thresholds against this corpus

---

# ALGORITHM 2: STRUCTURAL CONSTRUCTION (CONSTRUCTIVE)

## Purpose

Given a creative goal (genre, mood, length), construct a track 
specification that satisfies all six ADAP components by design. 
Output is a structural specification ready for compositional 
realization (in DAW, with band, etc.).

## Inputs

- Target genre / style (informs instrumentation, tempo range)
- Target track length (typically 2:30–6:00 for ADAP-positive 
  architecture)
- Optional: target listener complexity preference (Wundt sweet spot 
  calibration)

## Outputs

- **Anchor specification** (chord progression, melodic motif, 
  signature timbre)
- **Section structure** (anchor sections, deviation section, return, 
  climax)
- **Multi-scale fractal embedding** (phrase, section, work patterns)
- **Self-validation pass result** (run Algorithm 1 on draft, iterate)

## Pipeline overview

```
Goal → Stage 1 (anchor design) → Stage 2 (deviation engineering) 
     → Stage 3 (return mechanism) → Stage 4 (climax architecture) 
     → Stage 5 (multi-scale embedding) → Stage 6 (self-validation) 
     → Specification
```

## Stage 1: Anchor design

**Goal:** create simple, distinctive, repeatable identity carrier.

### 1.1 Choose minor key

Select stable minor key. Most common ADAP+ keys empirically:
- D minor (most common — Roundtable Rival, Hung Up)
- E minor (Nothing Else Matters, Wish I Had an Angel)
- F minor (SLTS, Turbo Killer)
- G minor (Hard Rock Hallelujah)
- A minor (Für Elise)
- Ab minor (Voodoo People)
- C minor (The Same Parents)

**Key selection criteria:**
- Stable single minor (NOT modal mixture, NOT dual-key)
- Compatible with target instrumentation range
- No fundamental physics constraint — choice is genre-pragmatic

### 1.2 Design chord progression

Build 3–5 chord progression rooted in chosen minor key. Common 
ADAP+ patterns:

| Pattern | Roman numerals | Example in key of A minor |
|---|---|---|
| Andalusian | i–VII–VI–V | Am–G–F–E |
| Aeolian | i–VI–III–VII | Am–F–C–G |
| Hungarian | i–VI–iv–V | Am–F–Dm–E |
| Classical minor | i–iv–V | Am–Dm–E |
| Pop minor | i–VII–VI | Am–G–F |
| Rock minor | i–VII–v | Am–G–Em |

**Constraints:**
- 3–5 chords (more = harder to learn, anchor weakens)
- Must be diatonic to chosen minor key (avoid modal mixture)
- Must repeat without modification throughout anchor sections
- Period: typically 4 or 8 bars

### 1.3 Compose melodic motif

Create memorable melodic phrase over chord progression:
- Length: 4–8 bars matching chord period
- Range: typically within an octave (singable)
- Distinctive: contains identifiable rhythm + interval pattern that 
  listener can mentally hum
- Hook test: would someone humming this motif recognize the source?

**This melodic motif IS the identity carrier.** Later climax will 
preserve this through transformation (W4 invariance).

### 1.4 Choose signature timbre

Identify distinctive timbral element that listener associates with 
the track:
- Lead instrument (e.g., distorted guitar in Voodoo People; finger-
  picked clean guitar in Nothing Else Matters)
- Vocal character (e.g., specific voice type)
- Distinctive sound effect or sample (e.g., ABBA arpeggio in Hung Up)

**Signature timbre stays present in anchor sections, often persists 
through climax.**

### 1.5 Anchor verification

Before proceeding, anchor must satisfy:
- ✓ Stable single minor key
- ✓ 3–5 chords, diatonic
- ✓ Memorable melodic motif over chord progression
- ✓ Distinctive signature timbre
- ✓ Designed to repeat identically throughout anchor sections
- ✓ Listener can recognize this as "the" pattern after 1–2 hearings

## Stage 2: Deviation engineering

**Goal:** design single concentrated rupture point that creates 
predictive uncertainty for BPI to discharge.

### 2.1 Position deviation

Place deviation at a single concentrated locus, typically:
- After 2–3 anchor section repetitions (BPI has learned the pattern)
- Before final climax section (deviation creates anticipation that 
  drives climax recovery)
- Common positions: bridge after second chorus; breakdown before 
  final chorus

**Avoid:**
- Multiple deviations scattered throughout (creates diffuse 
  architecture → ADAP-negative)
- Deviation at very start (no anchor established yet)
- Deviation at very end (no return possible)

### 2.2 Choose deviation mechanism

Select ONE primary deviation type. Mixing too many weakens 
concentration:

| Mechanism | Examples in corpus | Best for |
|---|---|---|
| Harmonic departure | Bridge in Hung Up (Bb major borrowed) | Pop, classical |
| Timbral switch | Dubstep section in Roundtable Rival | EDM, hybrid genres |
| Dynamic break | Breakdown in Voodoo People | Big beat, electronic |
| Vocal/textural shift | Twin sons in The Same Parents | Ambient, electronic |
| Rhythmic disruption | Half-time bridge | Rock, metal |
| Borrowed mode | Picardy third moment | Classical, ballad |

### 2.3 Design deviation content

Deviation must:
- Last 10–20% of total track length (long enough to register, short 
  enough to recover)
- Create clear contrast with anchor on chosen mechanism
- Stay decipherable (not chaotic — Wundt apex constraint)
- Foreshadow or imply eventual return to anchor

**Example specification (Roundtable Rival pattern):**
- Position: 2:00 mark (after second chorus repetition)
- Mechanism: Timbral switch (violin → dubstep wobble bass)
- Duration: 30 seconds
- Content: Same key, modified rhythm, dramatically different timbre

## Stage 3: Return mechanism

**Goal:** anchor returns identically after deviation, confirming BPI 
prediction (triggers dopamine reward).

### 3.1 Plan transition back

Create transition from deviation back to anchor:
- Typically 4–8 bars
- Builds anticipation: BPI knows return is imminent
- Common techniques:
  - Drum fill leading into anchor downbeat
  - Pickup chord (V chord resolving to i)
  - Filter sweep or rise effect
  - Decrescendo into anchor
  - Brief silence ("subtraction as device")

### 3.2 Anchor returns identically

After transition:
- Same chord progression as established anchor (NOT modified version)
- Same key
- Same melodic motif (or recognizable variant)
- Same signature timbre returns
- Same rhythmic groove

**This is the dopamine-trigger moment.** BPI prediction confirmed: 
"I knew it would come back" → reward signal.

### 3.3 Return verification

Before proceeding, return must satisfy:
- ✓ Anchor identifiably preserved
- ✓ Listener prediction satisfaction (BPI gets "I was right" signal)
- ✓ Discharge of accumulated tension from deviation

## Stage 4: Climax architecture (W4 invariance)

**Goal:** maximum transformation of context while preserving anchor 
identity. This is the most discriminating ADAP component.

### 4.1 Climax position

Locate climax typically:
- Last third of track
- After successful anchor return from deviation
- Before final fade or outro

### 4.2 Engineer accumulated transformation

The climax differs from anchor sections by accumulating layers, 
NOT by replacing anchor:

**Layers to accumulate (additive, NOT substitutive):**
- Additional vocal harmonies / counter-melodies
- Increased instrumentation density (strings, choir, additional 
  guitars)
- Higher dynamics / volume
- Extended frequency range (sub-bass + high-end shimmer)
- Sample stacking (multiple loops layered)
- Production effects (reverb tail, echo, layering)

**Critical W4 constraint:** anchor MUST remain present and 
recognizable through all accumulation:
- Chord progression unchanged
- Melodic motif still audible (possibly buried but present)
- Rhythmic groove maintained
- Signature timbre still present

### 4.3 W4 verification test

Test the climax: can listener, hearing only this climax section in 
isolation, still recognize it as "the same song" as the anchor 
sections?

- **Pass:** yes, anchor identity preserved through transformation
- **Fail:** no, climax sounds like different music (W4 broken)

**Common W4 failures to avoid:**
- Climax = guitar solo over completely new chord progression 
  (Master of Puppets failure)
- Climax = breakdown without anchor (Drain You partial failure)
- Climax = drone fade (ambient genre architectural exclusion)
- Climax = key modulation breaking anchor stability

### 4.4 Cross-track W4 (optional advanced technique)

If using sampling:
- Sample one identity carrier from external source
- Build new track around it as anchor
- Cross-track W4: same identity preserved through complete genre 
  transplant
- Examples: Voodoo People (Nirvana → Prodigy), Hung Up (ABBA → Madonna)

## Stage 5: Multi-scale embedding

**Goal:** apply same architectural principle (anchor-deviation-return) 
at multiple temporal scales simultaneously.

### 5.1 Phrase scale (4–8 bars)

Within each anchor section, design phrase-level architecture:
- Mini-anchor (2-bar motif) repeats
- Mini-deviation (1–2 bar rhythmic or melodic variation)
- Mini-return (motif resumes)

Example: in 8-bar phrase, structure as 2-bar motif × 3 + 2-bar 
variation, then return.

### 5.2 Section scale (16–32 bars)

Each major section follows arc:
- Verse: anchor + slight rhythmic variation
- Pre-chorus: slight build, anticipation
- Chorus: fully realized anchor with complete instrumentation
- Same architectural principle: stability + deviation + return

### 5.3 Work scale (full track)

Overall track follows global architecture:
- Intro (anchor establishment)
- Verse 1 (anchor)
- Chorus 1 (anchor with full layers)
- Verse 2 (anchor variation)
- Chorus 2 (anchor)
- Bridge / breakdown (designated single-locus deviation)
- Final chorus / climax (W4 invariance — anchor through max 
  transformation)
- Outro (anchor stripped down, fade)

**Common forms compatible with ADAP:**
- AABA (verse-verse-bridge-verse) with climax in final A
- ABACA rondo (Beethoven Für Elise)
- Verse-chorus form with final chorus as climax
- Big beat: intro-build-drop-breakdown-drop-outro

### 5.4 Self-similarity verification

Across scales, same principle should be visible:
- Phrase: anchor-deviation-anchor
- Section: anchor-deviation-anchor
- Work: anchor-deviation-anchor

**This is multi-scale fractal coherence.** Listener BPI processes 
all scales simultaneously through hierarchical predictive coding.

## Stage 6: Self-validation

**Goal:** verify constructed track meets ADAP criteria before 
finalization.

### 6.1 Run Algorithm 1

Apply diagnostic algorithm to draft:
- Compute ADAP score
- Identify any failing components
- Cross-check against intuitive listening

### 6.2 Iteration based on diagnosis

If score < 75 (target ADAP+ territory):

| If failed | Return to | Revise |
|---|---|---|
| A (anchor weak) | Stage 1 | Strengthen anchor distinctiveness |
| B (key unstable) | Stage 1 | Resolve to single minor key |
| C (deviation diffuse) | Stage 2 | Concentrate deviation to single locus |
| D (return broken) | Stage 3 | Restore anchor identically post-deviation |
| E (W4 fails) | Stage 4 | Preserve anchor through climax accumulation |
| F (fractal absent) | Stage 5 | Embed pattern at multiple scales |

### 6.3 Wundt apex calibration

Optional: tune complexity to target listener:
- General audience: aim for moderate complexity (3–5 chords, 
  predictable rhythm, standard genre conventions)
- Sophisticated audience: aim for slightly higher complexity 
  (extended chord vocabulary, polyrhythmic elements)
- Cross-cultural reach: simpler is often better (broader Wundt apex 
  match)

### 6.4 Final acceptance

Track is ADAP-correct when:
- ✓ Algorithm 1 score ≥ 75
- ✓ All six components pass
- ✓ Multi-scale fractal verifiable
- ✓ Climax preserves anchor through transformation (W4)
- ✓ Listener intuition matches structural analysis

---

# QUICK REFERENCE CARDS

## Diagnostic algorithm (Algorithm 1) — checklist

For quick manual evaluation without full software pipeline:

```
[ ] Anchor present? (recurring 3–5 chord pattern, ≥70% coverage)
[ ] Stable single minor key? (no major-key alternation, no modal mix)
[ ] Single concentrated deviation locus? (not diffuse)
[ ] Anchor returns identically after deviation?
[ ] Climax preserves anchor identity through transformation? (W4)
[ ] Same architecture at phrase + section + work scales?

Score:
- 6/6 → Strong ADAP+
- 5/6 → ADAP+
- 4/6 → Almost / weak ADAP+
- 3/6 → ADAP- (specify which fail)
- 0–2/6 → Strong ADAP-
```

## Constructive algorithm (Algorithm 2) — composition checklist

For systematic composition without full software pipeline:

```
Stage 1 — ANCHOR
[ ] Chosen stable minor key (D, E, F, G, A, etc.)
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
[ ] BPI prediction confirmed → reward moment

Stage 4 — CLIMAX (W4)
[ ] Anchor preserved through climax
[ ] Layers accumulate (additive, not substitutive)
[ ] Identity carrier survives transformation
[ ] Test: still recognizable as same song?

Stage 5 — MULTI-SCALE
[ ] Phrase-level architecture present
[ ] Section-level architecture present
[ ] Work-level architecture present
[ ] Self-similarity across scales

Stage 6 — VALIDATE
[ ] Run Algorithm 1 on draft
[ ] Iterate if score < 75
[ ] Final acceptance when all components pass
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
from adap import (
    extract_features,           # Stage 1
    detect_anchor,              # 2.A
    detect_minor_key_stability, # 2.B
    detect_single_locus_dev,    # 2.C
    verify_anchor_return,       # 2.D
    check_w4_invariance,        # 2.E
    detect_multi_scale_fractal, # 2.F
    compute_adap_score,         # Stage 3
    diagnose_failure_modes,     # Stage 4
)

# Pipeline
def adap_check(audio_path):
    features = extract_features(audio_path)
    components = {
        'A': detect_anchor(features),
        'B': detect_minor_key_stability(features),
        'C': detect_single_locus_dev(features),
        'D': verify_anchor_return(features),
        'E': check_w4_invariance(features),
        'F': detect_multi_scale_fractal(features),
    }
    score = compute_adap_score(components)
    diagnosis = diagnose_failure_modes(components) if score < 65 else None
    return {
        'score': score,
        'components': components,
        'diagnosis': diagnosis,
        'classification': classify(score),
    }
```

## Validation corpus

Reference 15-track corpus from `MUSIC_AS_A0_DOMAIN.md` with expected 
classifications:

```python
VALIDATION_CORPUS = {
    'fur_elise.flac':           'ADAP+',
    'master_of_puppets.flac':   'Strong ADAP-',
    'like_a_prayer.flac':       'ADAP-',
    'nothing_else_matters.flac':'ADAP+',
    'smells_like_teen_spirit.flac':'ADAP+',
    'drain_you.flac':           'ADAP-',
    'your_love.flac':           'Strong ADAP-',
    'voodoo_people.flac':       'Strong ADAP+',
    'the_child_in_us.flac':     'ADAP-',
    'wish_i_had_an_angel.flac': 'ADAP+',
    'hung_up.flac':             'ADAP+',
    'hard_rock_hallelujah.flac':'ADAP+',
    'the_same_parents.flac':    'Almost',
    'roundtable_rival.flac':    'Strong ADAP+',
    'turbo_killer.flac':        'Strong ADAP+',
}
```

Calibration target: ≥80% match between algorithm classification and 
expected classification.

## Software stack (Algorithm 2)

Algorithm 2 is primarily a creative methodology with structural 
constraints. It can be implemented as:

1. **Manual composition guide** — structured worksheet for composers
2. **DAW template system** — preset song structures encoding ADAP 
   architecture
3. **Generative system** — constraint-satisfaction composition with 
   ADAP rules as constraints (advanced)

Generative implementation sketch:
```python
def construct_adap_track(genre, length, complexity_target):
    # Stage 1: anchor
    key = select_minor_key(genre)
    progression = generate_chord_progression(key, length=4)
    motif = generate_melodic_motif(progression, distinctive=True)
    timbre = select_signature_timbre(genre)
    
    # Stage 2: deviation
    dev_position = length * 0.6  # bridge after 2 chorus reps
    dev_mechanism = select_deviation_type(genre)
    
    # Stage 3: return
    transition = design_return_transition(dev_mechanism)
    
    # Stage 4: climax (W4)
    climax = build_climax_with_invariance(progression, motif, timbre)
    
    # Stage 5: multi-scale
    structure = embed_at_scales(progression, motif, timbre, length)
    
    # Stage 6: validate
    spec = compile_specification(...)
    score = adap_check(render(spec))
    if score < 75:
        spec = iterate(spec, diagnose=score['diagnosis'])
    
    return spec
```

---

# RELATIONSHIP TO MAIN FRAMEWORK

These algorithms operationalize:
- **A₀ = argmin Z** in acoustic substrate → ADAP architecture
- **CGP formula** with explicit Δᵢ + crossterm + discharge
- **N_MusicStability 8 patterns** as forced structural conditions
- **Wundt apex** as optimal complexity calibration
- **Triangulation principle** as ≥3 coordinate streams requirement
- **Energy economy + dopamine reward** as engagement mechanism

Both algorithms are direct consequences of substrate-independent 
A₀ structure projected onto acoustic-temporal coordinate system.

The diagnostic algorithm (1) verifies a track instantiates A₀-geodesic 
trajectory through acoustic substrate.

The constructive algorithm (2) engineers a track that does so by design.

For full theoretical context see `MUSIC_AS_A0_DOMAIN.md`.

---

## Document status

Created 2026-04-26 as operational distillation of complete framework 
session. Both algorithms are implementable as specified. Validation 
against 15-track corpus pending software development.

Algorithm 1 readiness: specification complete, ready for Python 
implementation.

Algorithm 2 readiness: methodology complete, ready for composer use 
or generative system development.
