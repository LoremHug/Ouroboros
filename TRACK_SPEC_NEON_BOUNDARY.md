# TRACK SPECIFICATION: "Neon Boundary"

## Complete instrumental composition satisfying the engagement architecture specification

This document specifies a complete instrumental track that satisfies all
six structural features defined in `FRACTAL_MUSIC_PRINCIPLES.md`. The
specification is detailed enough to be translated by AI music generation
systems (Suno, Udio, MusicGen, MusicLM, Riffusion, Magenta-compatible
systems) into produced audio.

---

# SECTION 1: METADATA

| Parameter | Value |
|---|---|
| Working title | Neon Boundary |
| Key | A minor (natural minor with raised 7th in V chord) |
| Tempo | 100 BPM |
| Time signature | 4/4 |
| Total length | 3:12 (80 bars) |
| Genre | Synthwave instrumental (cinematic electronic) |
| Lyrics | None (purely instrumental) |
| Mood progression | Atmospheric → driving → tense → triumphant → fade |

---

# SECTION 2: HIGH-LEVEL NATURAL LANGUAGE PROMPT

For AI systems that accept text prompts (Suno, Udio, MusicGen, etc.),
use this complete prompt:

```
A 3 minute 12 second synthwave instrumental track in A minor at 100 BPM,
4/4 time. 80s-influenced electronic instrumentation: SuperSaw lead synth
carrying main melody, warm analog-style pad chords, synth bass (Moog-
style), 80s electronic drum kit (gated reverb snare, electronic kick,
hi-hat), brass synth for counter-melody, atmospheric pads with
shimmer reverb.

Structure (precise timing):

[0:00-0:19] Intro: solo lead synth plays main 4-bar melodic motif
twice with reverb. Soft pad underneath. Sub-bass on chord roots.
Minimal drums (only kick on 1 of each bar). Establishes the chord
progression Am - F - G - E repeated twice.

[0:19-0:57] Section A1 — main theme: Lead synth continues main motif.
Synth bass enters with arpeggiated pattern. Drums establish full
groove: gated snare on 2 and 4, kick on 1 and 3, hi-hat eighth notes.
Pad sustained underneath. Same Am-F-G-E progression continues for
16 bars (4 iterations).

[0:57-1:35] Section A2 — theme with counter-melody: Lead continues
main motif. Brass synth enters with sustained counter-melody. Drums
fuller with cymbals and clap accents. Bass becomes more active with
octave jumps. Same chord progression for 16 more bars.

[1:35-1:54] Bridge build: Anchor continues but with rising intensity.
Filter sweep up on lead synth. Drum fills build. Last bar: dramatic
pause, brief silence on beat 4.

[1:54-2:13] DEVIATION SECTION (single-locus rupture): TIMBRAL AND
TEXTURAL SWITCH while maintaining A minor key. Main lead synth drops
out. New aggressive arpeggiated synth takes over. Rhythmic feel
switches to half-time. Drums become heavier with electronic kick
and distorted snare. Sub-bass becomes prominent and distorted. Chord
progression simplifies to Am vamp with E chord interjections (Am-Am-
Am-E pattern over 8 bars). Pad drops out. Brass drops out. Atmosphere
darker, tense.

[2:13-2:24] Return transition: Drum fill builds dramatically. Filter
sweep down. Pad and brass return progressively. Pickup chord (E major)
leads into climax with anticipation.

[2:24-2:53] Section A3 — CLIMAX with identity preservation: ORIGINAL
ANCHOR RETURNS IDENTICALLY. Same Am-F-G-E progression. Same main motif
on lead synth. BUT now with maximum layer accumulation: counter-
melody continues from before, additional harmonies (third and fifth
above main motif), full pad sweeping, brass synth playing chord
stabs on each downbeat, full electronic drum kit with crashes on
chord changes, sub-bass added, atmospheric pads sustained underneath,
reverb tails creating wash. The melody you've heard before is preserved
but now sits in maximally rich orchestration.

[2:53-3:02] Section A4 — sustained climax with melodic variations:
Counter-melody takes the lead briefly, then main motif returns.
Maximum density continues. Optional: orchestral hits or stop-time
accents on downbeats of last 2 bars.

[3:02-3:12] Outro: Layers strip away progressively. Bar by bar:
drums fade, brass drops, counter-melody drops, pad fades, leaving
just lead synth and bass. Final 2 bars: lead plays motif simply over
sustained Am chord. Final note: A4 sustained with reverb fade.

Multi-scale structure: the same anchor-deviation-return architecture
appears at micro-level (within each 4-bar phrase), section-level
(within each 16-bar section), and work-level (intro-build-deviation-
climax-outro).

Mood arc: atmospheric opening → driving build → temporary
tension/struggle in deviation section → triumphant return → satisfied
resolution.
```

---

# SECTION 3: ANCHOR — CORE STRUCTURAL ELEMENTS

## 3.1 Chord progression (Anchor)

**Pattern:** Am – F – G – E
**Roman numerals (A minor):** i – VI – VII – V
**Pattern name:** Aeolian-derived progression with raised 7th
**Duration:** 4 bars (1 chord per bar in 4/4 time)
**Loop:** repeats throughout anchor sections (intro, A1, A2, A3, A4, outro)

Detailed chord voicings (root position, but voice as appropriate to
instrument):

| Bar | Chord | Notes (root position) | Notes (close voicing for synth/piano) |
|---|---|---|---|
| 1 | Am | A – C – E | A4 – C5 – E5 |
| 2 | F  | F – A – C | F4 – A4 – C5 |
| 3 | G  | G – B – D | G4 – B4 – D5 |
| 4 | E  | E – G# – B | E4 – G#4 – B4 |

**Critical constraint:** progression must NEVER change in anchor
sections. Same exact chords throughout intro, A1, A2, climax (A3, A4),
and outro. This is the identity carrier — the anchor.

## 3.2 Main melodic motif (Identity carrier)

**4-bar phrase** that plays over the chord progression. This is the
melody listeners will remember — it must return identically through the
climax (identity preservation through transformation).

Notation: `<note><octave> <duration>` where q=quarter, h=half, e=eighth,
r=rest

```
Bar 1 (over Am):    A5 q  | C6 q  | E6 q  | C6 q
Bar 2 (over F):     F5 q  | A5 q  | F5 q  | C5 q
Bar 3 (over G):     G5 q  | B5 q  | G5 q  | D5 q
Bar 4 (over E):     G#5 q | B5 q  | E5 q  | (rest q)
```

**Melodic shape:** ascending arpeggios in bars 1-2, descending pattern
in bar 3, cadential gesture in bar 4 with final breath (rest) before
phrase repeats.

**Critical constraint:** this exact motif must appear in:
- Intro (played on lead synth with reverb)
- A1 (played on lead synth, full groove)
- A2 (played on lead synth, with counter-melody added)
- A3 (climax — preserved with full orchestration over it)
- A4 (climax continued — possibly variations but main motif must return)
- Outro (played simply on lead, fading)

If main motif doesn't appear identifiably in climax, **identity
preservation through transformation fails and track no longer satisfies
the specification.**

## 3.3 Counter-melody (introduced in Section A2)

**4-bar phrase** played simultaneously with main motif. Sustained whole
notes giving harmonic depth.

```
Bar 1 (over Am):    E5 (whole note)
Bar 2 (over F):     C5 (whole note)
Bar 3 (over G):     D5 (whole note)
Bar 4 (over E):     B4 (whole note)
```

Counter-melody outlines 5th of each chord (E-C-D-B). Provides upper
harmony to each chord root. Adds without competing with main motif.

**Optional richer counter-melody** (alternative for variety in A4):

```
Bar 1 (over Am):    E5 h | A5 h
Bar 2 (over F):     C5 h | F5 h
Bar 3 (over G):     D5 h | G5 h
Bar 4 (over E):     B4 h | E5 h
```

## 3.4 Bass line

**Arpeggiated synth bass pattern** following chord roots with melodic
motion in the synthwave style.

```
Bar 1 (over Am):    A2 q  | E3 q  | A2 q  | C3 q
Bar 2 (over F):     F2 q  | C3 q  | F2 q  | A2 q
Bar 3 (over G):     G2 q  | D3 q  | G2 q  | B2 q
Bar 4 (over E):     E2 q  | B2 q  | E2 q  | G#2 q
```

Pattern per bar: root → 5th → root → 3rd. Standard synthwave bass
pattern providing forward motion.

**Simpler version for intro:** just root note as half note + half rest
in each bar.

---

# SECTION 4: SECTION-BY-SECTION SCORE

## 4.1 INTRO (bars 1-8, 0:00-0:19)

**Purpose:** Establish anchor at minimal density. Listener's predictive
system begins learning chord progression and motif.

**Instruments active:**
- **Lead synth** (SuperSaw with long reverb): plays main motif (bars
  1-4) then repeats (bars 5-8)
- **Soft pad**: sustained whole note matching chord underneath
- **Sub-bass**: plays root note as whole note in each bar
- **Kick drum**: kick only on beat 1 of each bar (minimal pulse)

**No snare, no hi-hat, no other instruments.**

**Dynamics:** mp (mezzo-piano, moderately quiet)

**Score (bars 1-4):**
```
Lead synth:
  Bar 1 (Am):    A5 q  | C6 q  | E6 q  | C6 q
  Bar 2 (F):     F5 q  | A5 q  | F5 q  | C5 q
  Bar 3 (G):     G5 q  | B5 q  | G5 q  | D5 q
  Bar 4 (E):     G#5 q | B5 q  | E5 q  | (rest q)

Pad:
  Bar 1: Am chord (A4-C5-E5) sustained whole note
  Bar 2: F chord (F4-A4-C5) sustained whole note
  Bar 3: G chord (G4-B4-D5) sustained whole note
  Bar 4: E chord (E4-G#4-B4) sustained whole note

Sub-bass:
  Bar 1: A1 (whole note)
  Bar 2: F1 (whole note)
  Bar 3: G1 (whole note)
  Bar 4: E1 (whole note)

Kick: beat 1 of each bar only
```

Bars 5-8: identical repeat of bars 1-4.

## 4.2 SECTION A1 — main theme (bars 9-24, 0:19-0:57)

**Purpose:** Full anchor presentation. Lead instrument continues melody.
Bass and drums establish groove.

**Instruments active:**
- **Lead synth**: plays main motif
- **Synth bass**: arpeggiated pattern as specified above
- **Drums**:
  - Kick on beats 1 and 3
  - Gated reverb snare on beats 2 and 4
  - Hi-hat: closed eighth notes throughout
  - Open hi-hat on the "+" of beat 4 of each phrase
- **Pad**: sustained chord underneath (whole notes voicing the chord)
- **Reverb on lead synth**: present but less prominent than intro

**Dynamics:** mf (mezzo-forte, moderately loud)

**Form:** 4 iterations of 4-bar progression = 16 bars

## 4.3 SECTION A2 — theme with counter-melody (bars 25-40, 0:57-1:35)

**Purpose:** Increase density. Add counter-melody. Maintain anchor
identity while building.

**Instruments active (additions to A1):**
- **Brass synth** enters: plays counter-melody (sustained whole notes)
- **Drums fuller**:
  - Snare adds clap layer on 2 and 4
  - Cymbals more present (open hi-hat throughout)
  - Tom fills at end of each 8-bar block
- **Pad more active**: rising/falling lines underneath chord pad
- **Bass**: occasional embellishment (e.g., chromatic passing tone
  A2-G#2-G2 between Am and G chords)

**Dynamics:** mf to f (increasing)

**Form:** 4 iterations of progression = 16 bars

## 4.4 BRIDGE BUILD (bars 41-48, 1:35-1:54)

**Purpose:** Build tension/intensity in preparation for deviation.
Anchor continues but signals upcoming change.

**Instruments active:**
- Same as A2 but with rising filter sweep on lead synth
- Drum fills become more frequent (every 2 bars instead of every 4)
- Pad: ascending automation sweep
- Brass: louder, more rhythmic stabs
- White noise sweep building through final 2 bars

**Form:** 2 iterations of progression = 8 bars

**Final bar (bar 48):** drum fill on beats 1-3, then **silence on beat 4**
(dramatic anticipation gap)

## 4.5 DEVIATION SECTION (bars 49-56, 1:54-2:13) — SINGLE-LOCUS RUPTURE

**Purpose:** Concentrated single-locus deviation. This is the only
deviation in the entire track. Multiple feature streams change
simultaneously (timbre, rhythm, harmony simplification) but all at this
single concentrated location.

**KEY MAINTAINED:** still in A minor (do not modulate — that would
break the single tonal regime requirement).

**What changes:**

### Harmonic content (simplified):
Chord progression becomes:
```
Bar 1: Am | Am | Am | E
Bar 2: Am | Am | Am | E  (same pattern continues for 8 bars)
```
4 bars: Am-Am-Am-E repeated 2 times = 8 bars of deviation

### Rhythmic switch:
- Half-time feel: kick on 1, snare on 3 (instead of 1-3 / 2-4)
- Heavy emphasis on beat 1 with sub-bass hit
- Choose one consistent pattern

### Timbral switch (THE PRIMARY DEVIATION MECHANISM):
- **Main lead synth: DROPS OUT entirely**
- **NEW lead instrument**: aggressive arpeggiated synth (sawtooth with
  resonant filter) OR FM-synthesis bell-like lead
- New lead plays: A minor pentatonic notes (A - C - D - E - G) in fast
  rhythmic patterns, NOT the original motif
- **Pad: drops out**
- **Brass: drops out**
- **Sub-bass: becomes prominent, distorted/saturated**
- **Drums: switch to aggressive electronic feel** (heavy electronic
  kick, processed snare with longer reverb tail, syncopated hi-hat)

### Atmosphere:
- Darker, more uncertain
- Add: low rumble, atmospheric noise textures
- Dynamics: f (loud, but different character from main sections)

**Score example for deviation lead (bars 49-52, first 4 bars):**
```
Arpeggiated synth lead:
Bar 1 (Am):  A5 e C6 e D6 e E6 e | G6 e E6 e D6 e C6 e | (eighth pattern)
Bar 2 (Am):  same pattern, slight rhythmic variation
Bar 3 (Am):  same pattern, slight rhythmic variation
Bar 4 (E):   stop pattern, single sustained E5 with filter sweep up
```

This pattern continues for the 8 bars.

**Critical constraint:** deviation must be CLEARLY DIFFERENT from anchor
sections in timbre and rhythmic feel. Listener must perceive distinct
"this is a different section." But key stays the same.

## 4.6 RETURN TRANSITION (bars 57-60, 2:13-2:24)

**Purpose:** Recovery from deviation. Build anticipation for climax.

**What happens:**
- Bar 57: deviation continues but with pad starting to seep back in
- Bar 58: brass gradually returns, reverb-y stabs
- Bar 59: drum fill begins building (snare rolls)
- Bar 60: full drum fill (toms, cymbals, snare rolls), massive
  crescendo, then **brief silence on beats 3-4** (dramatic anticipation
  gap)
- Crash cymbal on downbeat of bar 61 (start of climax)

## 4.7 SECTION A3 — CLIMAX (bars 61-72, 2:24-2:53) — IDENTITY PRESERVATION

**Purpose:** Maximum transformation while preserving anchor identity.

**ANCHOR PROGRESSION RETURNS IDENTICALLY:**
```
Bar 1: Am | Bar 2: F | Bar 3: G | Bar 4: E | (repeat 3 times for 12 bars)
```

**MAIN MOTIF RETURNS IDENTICALLY** on lead synth:
```
Bar 1: A5 q | C6 q | E6 q | C6 q
Bar 2: F5 q | A5 q | F5 q | C5 q
Bar 3: G5 q | B5 q | G5 q | D5 q
Bar 4: G#5 q | B5 q | E5 q | (rest q)
```

**Maximum layer accumulation (everything happening at once):**

1. **Lead synth**: main motif (identity carrier preserved)
2. **Counter-melody on brass synth**: continues from A2 specification
3. **Harmony layers**:
   - Synth playing motif a third above (C6-E6-G6-E6 over Am bar etc.)
   - Synth playing motif a fifth above (E6-G6-B6-G6 over Am bar etc.)
4. **Pad section**:
   - Sweeping sustained chords with shimmer reverb
   - Stereo-widened layered pads
5. **Brass synth**:
   - Counter-melody as before
   - Stab chords on each downbeat
6. **Drums**:
   - Full kit: kick on 1-3, gated snare on 2-4, hi-hat eighths
   - Crash cymbal on EACH chord change (every bar downbeat)
   - Tom fills on bar 4 of each phrase
7. **Bass**:
   - Active arpeggiated pattern (octave jumps)
8. **Sub-bass**: doubled with bass an octave below

**Dynamics:** ff (fortissimo)

**Form:** 3 iterations of progression = 12 bars

## 4.8 SECTION A4 — sustained climax (bars 73-76, 2:53-3:02)

**Purpose:** Extend climactic state. Allow listener to fully experience
the anchor returning under maximum transformation.

**What happens:**
- Bars 73-74: counter-melody on brass takes lead briefly while main
  motif harmonizes underneath
- Bars 75-76: main motif returns on top, full layering continues

**Optional accent:** stop-time hits on downbeats of bar 76 (everything
silent except hits on beats 1, 2, 3, 4 with crash cymbal each).

**Form:** 1 iteration of progression = 4 bars

## 4.9 OUTRO (bars 77-80, 3:02-3:12)

**Purpose:** Graceful resolution. Strip layers progressively.

**What happens:**
- Bar 77: drums fade out, brass drops, counter-melody continues
- Bar 78: counter-melody drops, pad fades, only lead and bass remain
- Bar 79: lead plays motif simply over sustained Am chord
- Bar 80: final note A4 sustained with long reverb tail, fade to silence

**Final dynamic:** decrescendo to pp (pianissimo) and beyond.

---

# SECTION 5: PRODUCTION LAYER GUIDE

## 5.1 Mix balance per section

| Section | Lead | Bass | Drums | Pad | Brass | Effects |
|---|---|---|---|---|---|---|
| Intro | Prominent | Quiet | Minimal | Soft | Off | Long reverb on lead |
| A1 | Prominent | Medium | Medium | Medium | Off | Standard reverb |
| A2 | Prominent | Medium | Strong | Medium | Medium | Standard reverb |
| Bridge | Prominent | Strong | Strong | Strong | Strong | Filter sweep |
| Deviation | OFF (replaced) | DISTORTED | HEAVY | OFF | OFF | Saturation |
| Transition | Building | Strong | Building | Returning | Returning | Sweep down |
| Climax | MAXIMUM | MAXIMUM | MAXIMUM | MAXIMUM | MAXIMUM | Wash |
| Outro | Fading | Fading | Off | Fading | Off | Long reverb |

## 5.2 Frequency space

- **Sub-bass (20-60 Hz):** sub-bass synth, kick drum fundamental
- **Bass (60-250 Hz):** synth bass, kick drum body
- **Low-mids (250-500 Hz):** pad chords, bass harmonics
- **Mids (500-2000 Hz):** lead synth body, vocals (none here), brass
- **High-mids (2000-5000 Hz):** lead synth presence, snare crack
- **Highs (5000+ Hz):** hi-hat, cymbals, lead synth air, reverb tails

## 5.3 Stereo image

- **Center:** kick, sub-bass, snare, lead synth main, vocals (none)
- **Slight left/right:** pad layers, hi-hat, brass
- **Wide stereo:** atmospheric pads, reverb returns, climax washes

---

# SECTION 6: SELF-VALIDATION CHECKLIST

Before finalizing, verify each structural feature passes:

**Feature A: Stable anchor**
- ✓ Recurring 4-chord pattern (Am-F-G-E)
- ✓ Coverage ≥70% of track time (intro + A1 + A2 + A3 + A4 + outro =
  64 of 80 bars = 80%)
- ✓ Same chord progression returns identically

**Feature B: Stable single tonal regime**
- ✓ A minor throughout
- ✓ No modulations
- ✓ No systematic dual-key alternation
- ✓ Coherent timbral palette throughout (synthwave electronic)

**Feature C: Concentrated deviation**
- ✓ Single deviation locus (bars 49-56, ~10% of track)
- ✓ Multiple feature streams deviate together (timbre + rhythm +
  harmony simplification)
- ✓ Not scattered — one clear rupture point

**Feature D: Anchor return**
- ✓ Original chord progression returns identically after deviation
- ✓ Original main motif returns identically after deviation
- ✓ Return is recognizable as same pattern (not modified version)

**Feature E: Identity preservation through transformation**
- ✓ Climax (A3-A4) preserves anchor chord progression
- ✓ Climax preserves main motif on lead synth
- ✓ Climax adds layers (harmonies, pad sweeps, brass, drums) WITHOUT
  replacing anchor
- ✓ Identity carrier (motif) survives maximum context transformation

**Feature F: Multi-scale hierarchical structure**
- ✓ Phrase scale: each 4-bar phrase = mini anchor-deviation-return
  (motif establishes, varies in bar 3-4, resolves)
- ✓ Section scale: each 16-bar section = anchor pattern with internal
  build
- ✓ Work scale: full track = intro-A1-A2-bridge-deviation-climax-outro

**Engineered tension cycle:**
- ✓ Anchor establishes prediction baseline
- ✓ Deviation introduces controlled break
- ✓ Anchor return delivers prediction confirmation
- ✓ Climax demonstrates anchor's robustness through transformation

**Optimal complexity range (Wundt-Berlyne curve):**
- ✓ Not too simple (not a trivially predictable two-chord vamp)
- ✓ Not too complex (no avant-garde dissonance, no rhythmic chaos)
- ✓ Sufficient elements for predictive engagement
- ✓ Decipherable for non-expert listener

**ALL SIX FEATURES SATISFIED. Track meets the engagement architecture
specification.**

Predicted engagement score from Algorithm 1: 80-90 (Strong).

---

# SECTION 7: AI GENERATION INSTRUCTIONS BY PLATFORM

## For Suno AI / Udio (text-prompt with structural tags)

Use the high-level prompt from Section 2. Add these structural tags:

```
[Intro: 0:00-0:19, lead synth + pad + sub-bass, Am-F-G-E progression, 100 BPM]
[Verse: 0:19-0:57, lead synth main melody, drums enter, synth bass]
[Build: 0:57-1:35, brass counter-melody, fuller drums, pad layer]
[Bridge: 1:35-1:54, rising tension, drum fills, dramatic pause]
[Deviation: 1:54-2:13, distorted arpeggio synth, half-time, Am vamp, dark]
[Build-up: 2:13-2:24, drum fill, return transition, anticipation]
[Climax: 2:24-2:53, full layers, anchor returns, max density]
[Sustain: 2:53-3:02, climax continues, melodic variations]
[Outro: 3:02-3:12, layers strip away, fade on Am chord]
```

## For MIDI-capable systems (MusicGen, Magenta, custom)

Provide the precise MIDI-ready specification:

```
TEMPO: 100 BPM
TIME_SIGNATURE: 4/4
KEY: A minor
TOTAL_BARS: 80

CHORD_PROGRESSION (anchor): Am | F | G | E | (repeats)

MAIN_MOTIF (4 bars, MIDI-compatible note specification):
Bar 1 (over Am): [A5, C6, E6, C6] each quarter note
Bar 2 (over F):  [F5, A5, F5, C5] each quarter note
Bar 3 (over G):  [G5, B5, G5, D5] each quarter note
Bar 4 (over E):  [G#5, B5, E5, REST] each quarter note

BASS_LINE (4 bars):
Bar 1: [A2, E3, A2, C3] quarter notes
Bar 2: [F2, C3, F2, A2] quarter notes
Bar 3: [G2, D3, G2, B2] quarter notes
Bar 4: [E2, B2, E2, G#2] quarter notes

COUNTER_MELODY (4 bars, sustained whole notes):
Bar 1: E5 (whole)
Bar 2: C5 (whole)
Bar 3: D5 (whole)
Bar 4: B4 (whole)

SECTION_MAP:
Bars 1-8:    INTRO     [lead, pad, sub-bass, kick_only]
Bars 9-24:   A1        [lead, synth_bass, drums_basic, pad]
Bars 25-40:  A2        [+ brass_counter, drums_full, pad_active]
Bars 41-48:  BRIDGE    [+ filter_sweep, drum_fills, drop_beat_4_bar_48]
Bars 49-56:  DEVIATION [DROP: lead, pad, brass | ADD: arp_synth,
                       electronic_drums, sub_distorted | CHORDS: Am-Am-Am-E]
Bars 57-60:  TRANSITION [pad_return, brass_return, drum_fill_build,
                        anticipation_silence_bar_60]
Bars 61-72:  CLIMAX_A3 [ANCHOR_RETURNS_IDENTICAL + harmonies + brass +
                       crash_cymbals_per_bar + sub_bass_octave]
Bars 73-76:  CLIMAX_A4 [counter_takes_lead_first_2_bars,
                       main_motif_returns_last_2_bars]
Bars 77-80:  OUTRO     [strip_layers_progressively, end_on_Am_sustained_A4]
```

## For Riffusion / spectrogram-based systems

Use the natural language prompt from Section 2. Emphasize:
- "100 BPM synthwave instrumental"
- "A minor chord progression: A minor, F major, G major, E major,
  repeating"
- "Build-up at 0:19, deviation at 1:54, climax at 2:24, fade at 3:02"
- "Synth lead melody returns triumphantly in climax with full layering"

## For human composer / DAW production

This document IS the score. Open your DAW (Logic, Ableton, FL Studio,
Cubase, etc.):

1. Set tempo 100 BPM, time signature 4/4
2. Create tracks for: lead synth (SuperSaw), synth bass (Moog-style),
   electronic drums, pad, brass synth, counter-melody synth, sub-bass,
   atmospheric pad, arpeggiated synth (for deviation only)
3. Program chord progression Am-F-G-E in MIDI as 4-bar loop
4. Program main motif on lead synth track (Section 3.2)
5. Build sections according to Section 4 layer specifications
6. For deviation section, mute most tracks, activate arpeggiated synth +
   electronic drums + change bass to distorted
7. For climax, activate ALL tracks simultaneously, ensure main motif
   audible through layers
8. Mix and master appropriately for synthwave genre conventions

---

# SECTION 8: REASONING — WHY THIS SPECIFICATION WORKS

This track is designed by inverting the diagnostic algorithm
(`MUSIC_ALGORITHMS.md` Algorithm 1) and ensuring each feature satisfies
its structural condition.

**Why anchor stability holds:**
Recurring 4-chord pattern (Am-F-G-E) covers 80% of track time. Same
chord progression returns identically across all anchor sections.
Listener's predictive system locks onto this pattern within first 1-2
hearings of the intro.

**Why tonal regime stability holds:**
Single key (A minor) throughout. No modulations. Coherent timbral
palette (synthwave electronic). Prediction system relies on consistent
rules and they remain consistent.

**Why concentrated deviation works:**
Single deviation locus at bars 49-56 (10% of track length). Multiple
feature streams deviate together: timbre (lead synth replaced by
arpeggio synth, pad and brass drop out, drums become electronic),
rhythm (half-time feel), harmony (simplified to Am vamp). Concentration
creates a single trackable rupture point that the predictive system
can anticipate and resolve.

**Why anchor return delivers prediction confirmation:**
Original chord progression and main motif return identically after the
deviation. Return is recognizable as the same pattern, not a modified
version. This delivers the prediction-confirmation signal that
correlates with dopamine release in the nucleus accumbens (Salimpoor
et al. 2011).

**Why identity preservation through transformation works:**
Climax (sections A3-A4) preserves anchor chord progression and main
motif on lead synth. Layers accumulate around the anchor (harmonies,
pad sweeps, brass stabs, full drums, sub-bass doubling) without
replacing the anchor itself. Identity carrier (the motif) survives
maximum context transformation. Listener experiences this as anchor's
robustness demonstrated under perturbation.

**Why multi-scale hierarchical structure works:**
The same anchor-deviation-return pattern operates at three scales:
- Phrase scale (4 bars): motif establishes, varies in bars 3-4,
  resolves at end of bar 4
- Section scale (16 bars): anchor pattern with internal build
- Work scale (full track): intro-build-deviation-climax-outro

When the same pattern operates at every scale the brain processes in
parallel, prediction is reinforced everywhere simultaneously.

**Why the engineered tension cycle dissolves into satisfaction:**
The deviation is designed to introduce controlled predictive tension.
The listener's prediction system, having locked onto the anchor,
registers the disruption and tracks it as an event requiring
resolution. The anchor return then delivers prediction confirmation,
producing the engagement-and-release experience listeners feel as
satisfaction. The climax extends this experience by demonstrating that
the anchor survives even under maximum context transformation —
producing what listeners experience as triumph.

**Why complexity sits in the optimal range:**
- Sufficient complexity to engage (4 chords, multi-layer
  orchestration, distinct sections, deviation creates challenge)
- Decipherable for non-expert listener (clear key, simple meter,
  memorable motif, predictable form)
- Habituation slow enough for repeated listening (multi-scale
  structure provides ongoing prediction tasks at different scales)

This places the track within the intermediate-complexity range
described by Berlyne (1971), where engagement is highest.

---

# SECTION 9: ALTERNATIVE INSTRUMENT MAPPINGS

The specification is genre-flexible. Same structural skeleton works with
different instrumentation:

**Synthwave version (specified above):**
- Lead synth: SuperSaw or sawtooth lead with chorus
- Pad: warm analog-style pad
- Bass: synth bass (Moog-style)
- Drums: 80s-style electronic kit (gated reverb snare)
- Counter-melody: brass synth
- Deviation: aggressive arpeggiated synth

**Cinematic orchestral version:**
- Lead: solo violin or oboe
- Counter-melody: French horn
- Strings: full string section (violins, violas, cellos, basses)
- Drums: orchestral percussion (timpani, taikos, snare)
- Pad: synthesized vocal pad or string pad
- Deviation: solo woodwinds with sparse strings

**Symphonic metal version:**
- Lead: distorted electric guitar or violin
- Counter-melody: orchestral horns
- Strings: full orchestra
- Drums: rock kit with double-kick
- Pad: epic choir samples
- Deviation: clean guitar arpeggios over breakdown

**Hybrid electronic-orchestral version:**
- Lead: synth pluck or processed violin
- Counter-melody: synth brass
- Strings: synthesized string section
- Drums: hybrid (electronic kick, processed acoustic snare, synth
  hi-hat)
- Pad: synthesized vocal pad
- Deviation: distorted synth + electronic drums

In all versions, the structural skeleton (chord progression, motif,
form) remains identical. Only sonic character changes.

---

# DOCUMENT STATUS

This specification is complete and ready for AI music generation. It
satisfies all six structural features defined in
`FRACTAL_MUSIC_PRINCIPLES.md` by design. It contains:
- Specific notes (MIDI-ready)
- Specific chord progression
- Specific timing (bar-by-bar)
- Specific instrument assignments
- Production layer guide
- Multiple AI platform formats
- Self-validation checklist

If generated audio fails the diagnostic algorithm (Algorithm 1 in
`MUSIC_ALGORITHMS.md`), the diagnosis table indicates which
specification element needs reinforcement.
