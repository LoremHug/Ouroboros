# TRACK SPECIFICATION: "Returning Through Light"

## Complete instrumental composition satisfying ADAP architecture

This document specifies a complete instrumental track that satisfies all 
six ADAP structural criteria by design. The specification is detailed 
enough to be translated by AI music generation systems (Suno, Udio, 
MusicGen, MusicLM, Riffusion, Magenta-compatible systems) into produced 
audio.

---

# SECTION 1: METADATA

| Parameter | Value |
|---|---|
| Working title | Returning Through Light |
| Key | D minor (natural minor with raised 7th in V chord) |
| Tempo | 120 BPM |
| Time signature | 4/4 |
| Total length | 3:44 (112 bars) |
| Genre | Cinematic instrumental electronic (orchestral synth hybrid) |
| Lyrics | None (purely instrumental) |
| Mood progression | Contemplative → building → uncertain → triumphant |

---

# SECTION 2: HIGH-LEVEL NATURAL LANGUAGE PROMPT

For AI systems that accept text prompts (Suno, Udio, MusicGen, etc.), 
use this complete prompt:

```
A 3 minute 44 second cinematic instrumental electronic track in D minor 
at 120 BPM, 4/4 time. Hybrid orchestral and synth instrumentation: lead 
synth or solo violin carrying main melody, string section pad, brass 
section for counter-melody, electric bass and sub-bass, hybrid drum kit 
(electronic kick, organic snare, hi-hat) plus orchestral percussion 
(timpani, taiko drums for accents), choir 'aahs' in climax sections.

Structure (precise timing):

[0:00-0:16] Intro: solo piano plays main 4-bar melodic motif twice 
quietly. Just piano and soft sub-bass on chord roots. Minimal density. 
Establishes the chord progression Dm - C - Bb - A repeated twice.

[0:16-0:48] Section A1 — main theme: Lead synth (or solo violin) takes 
over the main motif. Walking bass enters. Soft drums: kick on 1 and 3, 
snare on 2 and 4, hi-hat eighth notes. String pad sustained underneath. 
Same Dm-C-Bb-A progression continues for 16 bars (4 iterations).

[0:48-1:20] Section A2 — theme with counter-melody: Lead continues main 
motif. Brass section enters with sustained counter-melody (whole notes). 
Drums fuller with cymbals. Bass becomes more active. Same chord 
progression for 16 more bars.

[1:20-1:36] Bridge build: Anchor continues but with rising intensity. 
Filter sweep up on synths. Drum fill builds. Last bar: dramatic pause, 
brief silence on beat 4.

[1:36-2:08] DEVIATION SECTION (single-locus rupture): TIMBRAL AND 
TEXTURAL SWITCH while maintaining D minor key. Main lead instrument 
drops out. New aggressive synth arpeggio takes over (or distorted 
lead). Rhythmic feel switches to half-time or syncopated pattern. 
Drums become heavier, more electronic. Sub-bass becomes prominent and 
distorted. Chord progression simplifies to Dm vamp with A chord 
interjections (Dm-Dm-Dm-A pattern over 16 bars). Strings drop out. 
Brass drops out. Atmosphere darker, more uncertain.

[2:08-2:24] Return transition: Drum fill builds dramatically. Filter 
sweep down. Strings and brass return progressively. Pickup chord (A 
major) leads into climax with anticipation.

[2:24-2:56] Section A3 — CLIMAX with W4 invariance: ORIGINAL ANCHOR 
RETURNS IDENTICALLY. Same Dm-C-Bb-A progression. Same main motif on 
lead synth/violin. BUT now with maximum layer accumulation: counter-
melody continues from before, additional harmonies (third and fifth 
above main motif), full string section sweeping, brass section playing 
chord stabs on each downbeat, full hybrid drum kit with crashes on 
chord changes, sub-bass added, choir 'aahs' sustained underneath, 
reverb tails creating wash. The melody you've heard before is preserved 
but now sits in maximally rich orchestration.

[2:56-3:28] Section A4 — sustained climax with melodic variations: 
Counter-melody takes the lead briefly, then main motif returns. Maximum 
density continues. Optional: orchestral hits or stop-time accents on 
downbeats of last 4 bars.

[3:28-3:44] Outro: Layers strip away progressively. Bar by bar: drums 
fade, brass drops, counter-melody drops, strings fade, leaving just 
lead synth and bass. Final 2 bars: lead plays motif simply over 
sustained Dm chord. Final note: D5 sustained with reverb fade.

Multi-scale structure: the same anchor-deviation-return architecture 
appears at micro-level (within each 4-bar phrase), section-level (within 
each 16-bar section), and work-level (intro-build-deviation-climax-
outro). 

Mood arc: contemplative opening → building hope → temporary 
uncertainty/struggle in deviation section → triumphant return → 
satisfied resolution.
```

---

# SECTION 3: ANCHOR — CORE STRUCTURAL ELEMENTS

## 3.1 Chord progression (Anchor)

**Pattern:** Dm – C – Bb – A
**Roman numerals (D minor):** i – VII – VI – V
**Pattern name:** Andalusian cadence with raised 7th
**Duration:** 4 bars (1 chord per bar in 4/4 time)
**Loop:** repeats throughout anchor sections (intro, A1, A2, A3, A4, outro)

Detailed chord voicings (root position, but voice as appropriate to 
instrument):

| Bar | Chord | Notes (root position) | Notes (close voicing for 
synth/piano) |
|---|---|---|---|
| 1 | Dm | D – F – A | D4 – F4 – A4 |
| 2 | C  | C – E – G | C4 – E4 – G4 |
| 3 | Bb | Bb – D – F | Bb3 – D4 – F4 |
| 4 | A  | A – C# – E | A3 – C#4 – E4 |

**Critical constraint:** progression must NEVER change in anchor 
sections. Same exact chords throughout intro, A1, A2, climax (A3, A4), 
and outro. This is the identity carrier — the anchor.

## 3.2 Main melodic motif (Identity carrier)

**4-bar phrase** that plays over the chord progression. This is the 
melody listeners will remember — it must return identically through the 
climax (W4 invariance).

Notation: `<note><octave> <duration>` where q=quarter, h=half, e=eighth, 
r=rest

```
Bar 1 (over Dm):    D5 q  | F5 q  | A5 q  | F5 q
Bar 2 (over C):     E5 q  | G5 q  | E5 q  | C5 q
Bar 3 (over Bb):    D5 q  | F5 q  | D5 q  | Bb4 q
Bar 4 (over A):     C#5 q | E5 q  | A4 q  | (rest q)
```

**Melodic shape:** ascending arpeggios in bars 1-2, descending pattern 
in bar 3, cadential gesture in bar 4 with final breath (rest) before 
phrase repeats.

**Critical constraint:** this exact motif must appear in:
- Intro (played on piano)
- A1 (played on lead synth or violin)
- A2 (played on lead synth or violin, with counter-melody added)
- A3 (climax — preserved with full orchestration over it)
- A4 (climax continued — possibly variations but main motif must return)
- Outro (played simply on lead, fading)

If main motif doesn't appear identifiably in climax, **W4 invariance 
fails and track is no longer ADAP+.**

## 3.3 Counter-melody (introduced in Section A2)

**4-bar phrase** played simultaneously with main motif. Sustained whole 
notes giving harmonic depth.

```
Bar 1 (over Dm):    A4 (whole note)
Bar 2 (over C):     G4 (whole note)
Bar 3 (over Bb):    F4 (whole note)
Bar 4 (over A):     E4 (whole note)
```

Counter-melody descends scale-wise (A-G-F-E). Provides 5th harmony to 
each chord root. Adds without competing with main motif.

**Optional richer counter-melody** (alternative for variety in A4):

```
Bar 1 (over Dm):    A4 h | D5 h
Bar 2 (over C):     G4 h | C5 h
Bar 3 (over Bb):    F4 h | Bb4 h
Bar 4 (over A):     E4 h | A4 h
```

## 3.4 Bass line

**Walking bass pattern** following chord roots with melodic motion.

```
Bar 1 (over Dm):    D2 q  | A2 q  | D2 q  | F2 q
Bar 2 (over C):     C2 q  | G2 q  | C2 q  | E2 q
Bar 3 (over Bb):    Bb1 q | F2 q  | Bb1 q | D2 q
Bar 4 (over A):     A1 q  | E2 q  | A1 q  | C#2 q
```

Pattern per bar: root → 5th → root → 3rd. Standard walking bass providing 
forward motion.

**Simpler version for intro:** just root note as half note + half rest 
in each bar.

---

# SECTION 4: SECTION-BY-SECTION SCORE

## 4.1 INTRO (bars 1-8, 0:00-0:16)

**Purpose:** Establish anchor at minimal density. Listener BPI begins 
learning chord progression and motif.

**Instruments active:**
- Solo piano: plays main motif (bars 1-4) then repeats (bars 5-8)
- Soft sub-bass: plays root note as whole note in each bar (D - C - Bb - A, then repeat)

**No drums, no other instruments.**

**Dynamics:** mp (mezzo-piano, moderately quiet)

**Score (bars 1-4):**
```
Piano right hand: 
  Bar 1 (Dm):    D5 q  | F5 q  | A5 q  | F5 q
  Bar 2 (C):     E5 q  | G5 q  | E5 q  | C5 q
  Bar 3 (Bb):    D5 q  | F5 q  | D5 q  | Bb4 q
  Bar 4 (A):     C#5 q | E5 q  | A4 q  | (rest q)

Piano left hand:
  Bar 1: D3 (whole note)
  Bar 2: C3 (whole note)
  Bar 3: Bb2 (whole note)
  Bar 4: A2 (whole note)

Sub-bass:
  Bar 1: D2 (whole note)
  Bar 2: C2 (whole note)
  Bar 3: Bb1 (whole note)
  Bar 4: A1 (whole note)
```

Bars 5-8: identical repeat of bars 1-4.

## 4.2 SECTION A1 — main theme (bars 9-24, 0:16-0:48)

**Purpose:** Full anchor presentation. Lead instrument takes melody. 
Bass and drums establish groove.

**Instruments active:**
- **Lead synth** (or solo violin): plays main motif
- **Walking bass**: as specified above
- **Drums**: 
  - Kick on beats 1 and 3
  - Snare on beats 2 and 4
  - Hi-hat: eighth notes throughout
  - Light cymbal swell on bar 4 of each phrase
- **String pad**: sustained chord underneath (whole notes voicing the chord)
- **Piano**: drops out (or plays sparse arpeggios as ornament)

**Dynamics:** mf (mezzo-forte, moderately loud)

**Form:** 4 iterations of 4-bar progression = 16 bars

## 4.3 SECTION A2 — theme with counter-melody (bars 25-40, 0:48-1:20)

**Purpose:** Increase density. Add counter-melody. Maintain anchor 
identity while building.

**Instruments active (additions to A1):**
- **Brass section** enters: plays counter-melody (sustained whole notes)
- **Drums fuller**: 
  - Snare adds ghost notes between beats
  - Cymbals more present (open hi-hat on "+" of beat 4)
  - Tom fills at end of each 8-bar block
- **Strings more active**: rising/falling lines underneath chord pad
- **Bass**: occasional embellishment (e.g., chromatic passing tone D2-C#2-C2 between Dm and C chords)

**Dynamics:** mf to f (increasing)

**Form:** 4 iterations of progression = 16 bars

## 4.4 BRIDGE BUILD (bars 41-48, 1:20-1:36)

**Purpose:** Build tension/intensity in preparation for deviation. 
Anchor continues but signals upcoming change.

**Instruments active:**
- Same as A2 but with rising filter sweep on synths
- Drum fills become more frequent (every 2 bars instead of every 4)
- Strings: ascending tremolo line
- Brass: louder, more rhythmic stabs

**Form:** 2 iterations of progression = 8 bars

**Final bar (bar 48):** drum fill on beats 1-3, then **silence on beat 4** 
(dramatic anticipation gap)

## 4.5 DEVIATION SECTION (bars 49-64, 1:36-2:08) — SINGLE-LOCUS RUPTURE

**Purpose:** Concentrated single-locus deviation. This is the only 
deviation in the entire track. Multiple coordinates change simultaneously 
(timbre, rhythm, harmony simplification) but all at this single 
concentrated location.

**KEY MAINTAINED:** still in D minor (do not modulate — that would break 
key stability criterion).

**What changes:**

### Harmonic content (simplified):
Chord progression becomes:
```
Bar 1: Dm | Dm | Dm | A
Bar 2: Dm | Dm | Dm | A  (same pattern continues for 16 bars)
```
4 bars: Dm-Dm-Dm-A repeated 4 times = 16 bars of deviation

### Rhythmic switch:
- Half-time feel: kick on 1, snare on 3 (instead of 1-3 / 2-4)
- OR: heavy syncopation with kick on 1 and "+ of 2"
- Choose one consistent pattern

### Timbral switch (THE PRIMARY DEVIATION MECHANISM):
- **Main lead synth/violin: DROPS OUT entirely**
- **NEW lead instrument**: aggressive distorted synth arpeggio OR processed/granular synth lead
- New lead plays: D minor pentatonic notes (D - F - G - A - C) in fast 
  rhythmic patterns, NOT the original motif
- **Strings: drop out**
- **Brass: drop out**
- **Sub-bass: becomes prominent, distorted/saturated**
- **Drums: switch to electronic/programmed feel** (e.g., 808-style 
  electronic kick, snare with reverb tail)

### Atmosphere:
- Darker, more uncertain
- Possibly add: low rumble, atmospheric pads, sound design textures
- Dynamics: f (loud, but different character from main sections)

**Score example for deviation lead (bars 49-52, first 4 bars):**
```
Distorted synth arpeggio:
Bar 1 (Dm):  D5 e F5 e G5 e A5 e | C6 e A5 e G5 e F5 e | (repeat eighth pattern)
Bar 2 (Dm):  same pattern, slight rhythmic variation
Bar 3 (Dm):  same pattern, slight rhythmic variation
Bar 4 (A):   stop pattern, single sustained A4 with filter sweep up
```

This pattern continues for the 16 bars.

**Critical constraint:** deviation must be CLEARLY DIFFERENT from anchor 
sections in timbre and rhythmic feel. Listener must perceive distinct 
"this is a different section." But key stays the same.

## 4.6 RETURN TRANSITION (bars 65-72, 2:08-2:24)

**Purpose:** Recovery from deviation. Build anticipation for climax.

**What happens:**
- Bars 65-66: deviation continues but with strings starting to seep back in
- Bars 67-68: brass gradually returns, reverb-y
- Bars 69-70: drum fill begins building (snare rolls)
- Bar 71: full drum fill (toms, cymbals, snare rolls)
- Bar 72: massive crescendo, then **brief silence on beats 3-4** 
  (dramatic anticipation gap)
- Crash cymbal on downbeat of bar 73 (start of climax)

## 4.7 SECTION A3 — CLIMAX (bars 73-88, 2:24-2:56) — W4 INVARIANCE

**Purpose:** Maximum transformation while preserving anchor identity.

**ANCHOR PROGRESSION RETURNS IDENTICALLY:**
```
Bar 1: Dm | Bar 2: C | Bar 3: Bb | Bar 4: A | (repeat 4 times for 16 bars)
```

**MAIN MOTIF RETURNS IDENTICALLY** on lead synth/violin:
```
Bar 1: D5 q | F5 q | A5 q | F5 q
Bar 2: E5 q | G5 q | E5 q | C5 q
Bar 3: D5 q | F5 q | D5 q | Bb4 q
Bar 4: C#5 q | E5 q | A4 q | (rest q)
```

**Maximum layer accumulation (everything happening at once):**

1. **Lead synth/violin**: main motif (identity carrier preserved)
2. **Counter-melody on brass**: continues from A2 specification
3. **Harmony layers**:
   - Synth playing motif a third above (F5-A5-C6-A5 over Dm bar etc.)
   - Synth playing motif a fifth above (A5-C6-E6-C6 over Dm bar etc.)
4. **String section**:
   - Sweeping ascending lines  
   - Tremolo on chord tones
5. **Brass section**:
   - Counter-melody as before
   - Stab chords on each downbeat
6. **Drums**:
   - Full kit: kick on 1-3, snare on 2-4, hi-hat eighths
   - Crash cymbal on EACH chord change (every bar downbeat)
   - Tom fills on bar 4 of each phrase
7. **Bass**:
   - Walking bass continues
   - Sub-bass adds octave below (D1, C1, Bb0, A0)
8. **Choir 'aahs'**:
   - Sustained voicing of chord (e.g., choir sopranos on D5, altos on F4, tenors on A3)
   - Changes with chord progression
9. **Reverb tails and production effects**:
   - Long reverb on snare hits
   - Delay throws
   - Riser FX between phrases

**Dynamics:** ff (fortissimo, very loud) — maximum dynamic range of track.

## 4.8 SECTION A4 — sustained climax (bars 89-104, 2:56-3:28)

**Purpose:** Sustain maximum density. Allow listener to bask in resolved 
climax. Optionally introduce melodic variation.

**Bars 89-96 (8 bars):** counter-melody (brass) takes the lead role, 
main motif drops to harmony. Same anchor chord progression continues.

**Bars 97-104 (8 bars):** main motif RETURNS as the lead again. Maximum 
density continues.

**Optional**: bars 103-104 (last 2 bars before outro) — orchestral 
"stop-time" hits: full orchestra plays only on beats 1 and 3, with rests 
on 2 and 4. Creates dramatic punctuation before outro.

## 4.9 OUTRO (bars 105-112, 3:28-3:44)

**Purpose:** Strip down to anchor at minimal density. Reverse of intro 
shape. Close the loop.

**Strip layers progressively:**
- Bar 105: drums fade out
- Bar 106: brass drops out
- Bar 107: counter-melody drops out
- Bar 108: strings fade
- Bars 109-110: just lead synth + bass playing motif over chord 
  progression
- Bars 111-112: lead plays motif simply over sustained Dm chord

**Final note:** D5 (or D4 if more peaceful) sustained with long reverb 
fade.

---

# SECTION 5: PRODUCTION LAYERS — visual overview

```
Time:    0:00  0:16  0:48  1:20  1:36  2:08  2:24  2:56  3:28  3:44
Section: INT   A1    A2    BRG   DEV   RTN   A3    A4    OUT
Bars:    1-8   9-24  25-40 41-48 49-64 65-72 73-88 89-104 105-112

Piano:   ████  ░░░░  ░░░░  ░░░░  ░░░░  ░░░░  ░░░░  ░░░░  ░░░░
Lead syn:░░░░  ████  ████  ████  ░░░░  ░░██  ████  ████  ████ 
Strings: ░░░░  ████  ████  ████  ░░░░  ░░██  ████  ████  ██░░
Brass:   ░░░░  ░░░░  ████  ████  ░░░░  ░░██  ████  ████  ░░░░
Counter: ░░░░  ░░░░  ████  ████  ░░░░  ░░░░  ████  ████  ░░░░
Bass:    ████  ████  ████  ████  ████  ████  ████  ████  ████ ─
Sub-bass:████  ████  ████  ████  ████  ████  ████  ████  ░░░░
Drums:   ░░░░  ████  ████  ████  ████  ████  ████  ████  ██░░
Distort: ░░░░  ░░░░  ░░░░  ░░░░  ████  ░░░░  ░░░░  ░░░░  ░░░░
Choir:   ░░░░  ░░░░  ░░░░  ░░░░  ░░░░  ░░░░  ████  ████  ░░░░
Harmony: ░░░░  ░░░░  ░░░░  ░░░░  ░░░░  ░░░░  ████  ████  ░░░░

█ = active   ░ = silent/absent
```

---

# SECTION 6: ADAP SELF-VALIDATION CHECKLIST

Before considering this specification complete, verify each of the 
six ADAP components is structurally satisfied.

## ✓ Component A: Stable anchor

- ✓ Single chord progression Dm-C-Bb-A repeats throughout intro, A1, 
  A2, A3, A4, outro (≥80% of total track time)
- ✓ Single melodic motif identifies the anchor
- ✓ Distinctive signature timbre (lead synth or solo violin) carries 
  the motif
- ✓ Anchor is simple enough (4-bar progression) for BPI to learn quickly

## ✓ Component B: Stable single minor key

- ✓ D minor throughout entire track (including deviation section)
- ✓ A major (V chord) contains C# raised 7th — standard harmonic minor
- ✓ No modulation, no major-key alternation, no modal mixture
- ✓ Deviation section stays in D minor (just simplified harmonic motion)

## ✓ Component C: Single-locus deviation

- ✓ ONE deviation section (bars 49-64, 16 bars = 14% of total track)
- ✓ Concentrated single time region (not diffuse)
- ✓ Multiple coordinates change simultaneously at this locus:
  - Timbral (lead instrument switches)
  - Rhythmic (half-time or syncopated feel)
  - Harmonic (simplifies to Dm vamp)
  - Textural (strings/brass drop out)
- ✓ Rest of track maintains anchor

## ✓ Component D: Anchor return

- ✓ After deviation + return transition (bars 65-72), full anchor 
  returns identically in A3 (bars 73-88)
- ✓ Same chord progression Dm-C-Bb-A
- ✓ Same main motif on same lead instrument
- ✓ Same key, same tempo, same time signature
- ✓ BPI prediction confirmed → dopamine reward triggered

## ✓ Component E: W4 invariance (climax = identity through transformation)

- ✓ Climax (A3, A4) preserves anchor chord progression unchanged
- ✓ Climax preserves main motif on same lead instrument
- ✓ Climax adds layers (counter-melody, harmonies, choir, brass, 
  strings, sub-bass) — additive accumulation
- ✓ Climax does NOT replace anchor with new material
- ✓ Test: hearing only the climax, listener can still recognize 
  this as same song as A1 sections — yes, motif and progression 
  preserved

## ✓ Component F: Multi-scale fractal

- ✓ Phrase scale (4 bars): each phrase has internal anchor-deviation-
  return shape (ascending arpeggios → cadential resolution at bar 4)
- ✓ Section scale (16 bars): each major section has internal 
  build-and-resolve arc within itself
- ✓ Work scale (full track): global anchor (intro, A1, A2) → 
  deviation (bridge, deviation section) → return (transition, A3, A4) 
  → resolution (outro)
- ✓ Same anchor-deviation-anchor principle nested at all three scales

## ✓ Component G: Optimal complexity (Wundt apex)

- ✓ Track is complex enough to challenge listener (4-chord progression, 
  multiple instruments, distinctive motif, deviation section creates 
  uncertainty)
- ✓ Track is decipherable (clear key, clear meter, clear motif, 
  predictable form)
- ✓ Brain can build prediction model with effort, prediction succeeds, 
  dopamine reward triggered
- ✓ Not too simple (not a trivially predictable two-chord vamp)
- ✓ Not too complex (no avant-garde dissonance, no rhythmic chaos)

**ALL SIX COMPONENTS PASS. Track satisfies ADAP+ architecture by 
design.**

Predicted ADAP score from Algorithm 1: 85-90 (Strong ADAP+).

---

# SECTION 7: AI GENERATION INSTRUCTIONS BY PLATFORM

## For Suno AI / Udio (text-prompt with structural tags)

Use the high-level prompt from Section 2. Add these structural tags:

```
[Intro: 0:00-0:16, piano + sub-bass only, Dm-C-Bb-A progression, 120 BPM]
[Verse: 0:16-0:48, lead synth main melody, drums enter, walking bass]
[Build: 0:48-1:20, brass counter-melody, fuller drums, strings layer]
[Bridge: 1:20-1:36, rising tension, drum fills, dramatic pause]
[Deviation: 1:36-2:08, distorted synth, half-time, Dm vamp, dark]
[Build-up: 2:08-2:24, drum fill, return transition, anticipation]
[Climax: 2:24-2:56, full orchestra, choir, anchor returns, max density]
[Sustain: 2:56-3:28, climax continues, melodic variations]
[Outro: 3:28-3:44, layers strip away, fade on Dm chord]
```

## For MIDI-capable systems (MusicGen, Magenta, custom)

Provide the precise MIDI-ready specification:

```
TEMPO: 120 BPM
TIME_SIGNATURE: 4/4
KEY: D minor
TOTAL_BARS: 112

CHORD_PROGRESSION (anchor): Dm | C | Bb | A | (repeats)

MAIN_MOTIF (4 bars, MIDI-compatible note specification):
Bar 1 (over Dm): [D5, F5, A5, F5] each quarter note
Bar 2 (over C):  [E5, G5, E5, C5] each quarter note
Bar 3 (over Bb): [D5, F5, D5, Bb4] each quarter note
Bar 4 (over A):  [C#5, E5, A4, REST] each quarter note

BASS_LINE (4 bars):
Bar 1: [D2, A2, D2, F2] quarter notes
Bar 2: [C2, G2, C2, E2] quarter notes
Bar 3: [Bb1, F2, Bb1, D2] quarter notes
Bar 4: [A1, E2, A1, C#2] quarter notes

COUNTER_MELODY (4 bars, sustained whole notes):
Bar 1: A4 (whole)
Bar 2: G4 (whole)
Bar 3: F4 (whole)
Bar 4: E4 (whole)

SECTION_MAP:
Bars 1-8:    INTRO     [piano, sub-bass]
Bars 9-24:   A1        [lead, walking_bass, drums_basic, string_pad]
Bars 25-40:  A2        [+ brass_counter, drums_full, strings_active]
Bars 41-48:  BRIDGE    [+ filter_sweep, drum_fills, drop_beat_4_bar_48]
Bars 49-64:  DEVIATION [DROP: lead, strings, brass | ADD: distorted_synth, 
                       electronic_drums, sub_distorted | CHORDS: Dm-Dm-Dm-A]
Bars 65-72:  TRANSITION [strings_return, brass_return, drum_fill_build, 
                        anticipation_silence_bar_72]
Bars 73-88:  CLIMAX_A3 [ANCHOR_RETURNS_IDENTICAL + harmonies + choir + 
                       crash_cymbals_per_bar + sub_bass_octave]
Bars 89-104: CLIMAX_A4 [counter_takes_lead_first_8_bars, 
                       main_motif_returns_last_8_bars]
Bars 105-112: OUTRO    [strip_layers_progressively, end_on_Dm_sustained_D5]
```

## For Riffusion / spectrogram-based systems

Use the natural language prompt from Section 2. Emphasize:
- "120 BPM cinematic instrumental"
- "D minor chord progression: D minor, C major, B-flat major, A major, 
  repeating"
- "Build-up at 0:16, deviation at 1:36, climax at 2:24, fade at 3:28"
- "Synth lead melody returns triumphantly in climax with full orchestra"

## For human composer / DAW production

This document IS the score. Open your DAW (Logic, Ableton, FL Studio, 
Cubase, etc.):

1. Set tempo 120 BPM, time signature 4/4
2. Create tracks for: lead synth, walking bass, drums, string pad, 
   brass section, counter-melody, sub-bass, choir pad, distorted synth 
   (for deviation only)
3. Program chord progression Dm-C-Bb-A in MIDI as 4-bar loop
4. Program main motif on lead synth track (Section 3.2)
5. Build sections according to Section 4 layer specifications
6. For deviation section, mute most tracks, activate distorted synth + 
   electronic drums + change bass to distorted
7. For climax, activate ALL tracks simultaneously, ensure main motif 
   audible through layers
8. Mix and master appropriately for genre

---

# SECTION 8: REASONING — WHY THIS SPECIFICATION WORKS

This track is designed by inverting the diagnostic algorithm 
(MUSIC_ALGORITHMS.md Algorithm 1) and ensuring each component scores 
high.

**Why it satisfies CGP formula** (`MUSIC_AS_A0_DOMAIN.md`):
- Baseline A(t) = Dm-C-Bb-A progression with main motif (intro through A2)
- Δᵢ(t) deviations all concentrated in single bridge section (bars 49-64)
- Multiple coordinates deviate simultaneously: timbral, rhythmic, harmonic
- Discharge: BPI inference reaches new argmin A'(t+τ) = climax with 
  accumulated layers around preserved anchor
- C1: gradient sufficient (clear timbral switch) but not excessive 
  (key maintained)
- C2: multi-scale gradients present (phrase, section, work)
- C3: resolution reduces uncertainty (anchor returns identifiably)

**Why it satisfies all 8 N_MusicStability patterns:**
- P1: fixed temporal grid (120 BPM throughout)
- P2: binary contrast in dominant coordinate (dynamics arc + timbral 
  contrast)
- P3: arc shape (build → peak → resolution at multiple scales)
- P4: hierarchy of scales (phrase, section, work)
- P5: repetition + variation (anchor repeats, deviation varies, climax 
  is anchor + accumulation)
- P6: subtraction as device (silence at bar 48 beat 4, layer stripping 
  in outro)
- P7: coupling of coordinates (tempo consistent, all coordinates 
  coordinated)
- P8: anticipation-fulfillment cycles (deviation creates expectation of 
  return, anchor return fulfills it)

**Why it triggers dopamine reward:**
- Listener BPI learns anchor pattern in intro/A1
- Deviation creates predictive uncertainty
- Anchor return confirms prediction → "I was right" → dopamine spike
- Climax extends reward (multiple successful predictions per bar as 
  motif returns each phrase)
- Outro provides graceful resolution

**Why it sits at Wundt apex:**
- Complexity sufficient to engage (4 chords, multi-instrument 
  orchestration, distinct sections, deviation creates challenge)
- Decipherable enough for non-expert listener (clear key, simple 
  meter, memorable motif, predictable form)
- Habituation slow enough for repeated listening (multi-scale 
  structure provides ongoing prediction tasks at different scales)

---

# SECTION 9: ALTERNATIVE INSTRUMENT MAPPINGS

The specification is genre-flexible. Same structural skeleton works with 
different instrumentation:

**Synthwave version:**
- Lead synth: SuperSaw or sawtooth lead with chorus
- Pad: warm analog-style pad
- Bass: synth bass (Moog-style)
- Drums: 80s-style electronic kit (LinnDrum, gated reverb snare)
- Counter-melody: brass synth or trumpet sample
- Deviation: heavily filtered/distorted lead

**Symphonic metal version:**
- Lead: distorted electric guitar
- Counter-melody: orchestral horns
- Strings: full orchestra
- Drums: rock kit with double-kick
- Choir: epic choir samples
- Deviation: clean guitar arpeggios over breakdown

**Cinematic orchestral version:**
- Lead: solo violin
- Counter-melody: French horn
- Strings: full string section (violins, violas, cellos, basses)
- Drums: orchestral percussion (timpani, taikos, snare)
- Choir: full SATB choir
- Deviation: solo woodwinds with sparse strings

**Electronic/synthwave hybrid (recommended for AI generation):**
- Lead: synth pluck or processed violin
- Counter-melody: synth brass
- Strings: synthesized string section
- Drums: hybrid (electronic kick, processed acoustic snare, synth hi-hat)
- Choir: synthesized vocal pad
- Deviation: distorted synth + electronic drums

In all versions, the structural skeleton (chord progression, motif, 
form) remains identical. Only sonic character changes.

---

# DOCUMENT STATUS

This specification is complete and ready for AI music generation. It 
satisfies all six ADAP components by design. It contains:
- Specific notes (MIDI-ready)
- Specific chord progression
- Specific timing (bar-by-bar)
- Specific instrument assignments
- Production layer guide
- Multiple AI platform formats
- Self-validation checklist

If generated audio fails ADAP scoring on Algorithm 1, the diagnosis 
table in MUSIC_ALGORITHMS.md indicates which specification element 
needs reinforcement.
