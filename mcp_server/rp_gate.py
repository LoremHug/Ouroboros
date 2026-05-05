"""RP-gate runtime: structural validator for text claims.

Detects R1-R4 traps + grammar trap + domain carving + Shannon overhead.
Pattern-based v1; foundation for LLM-assisted v2.

Per N_OperationalCarrierVsOntologicalCommitment (round 36):
patterns alone do not equal traps. Operational descriptive nouning is
forced linguistic carrier (acceptable). Trap is ontological commitment
(causal verbs, property attribution to processes, agent-grammar on
totalities). v1 is proto-detector — flags pattern, classifies severity
by commitment-likelihood markers. v2 will add semantic context.

Reference nodes in framework:
  N_FrameworkCore     — substrate-invariant principle set (round 35)
  N_OperationalCarrierVsOntologicalCommitment — calibration (round 36)
  N_EpistemicTraps    — R1-R4 catalogue
  N_GrammarTrap       — S-V-O ontological imposition
  N_OntologyGate      — operational interception layer
  N_DomainsAsBPICarvings — domain partition as BPI artifact
  N_OntologyParadigmGrammarBound — paradigm-level grammar wall
  N_TopologyProcessIdentity — R1 root (process not object)
  N112                — R2 root (no external observer)
  N_InversiveTheory   — R3 root (alternatives must dissolve)
  N187                — R4 root (no internal state-change agency)
"""
from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import Any


# ─── Operational vs commitment markers ───────────────────────────────
# Verbs / phrases that signal OPERATIONAL/DESCRIPTIVE use (downgrade severity)
OPERATIONAL_MARKERS = re.compile(
    r"\b(describes?|tracks?|labels?|denotes?|represents?|signifies|"
    r"refers? to|stands for|encodes?|maps? to|measures?|reveals?|"
    r"reflects?|expresses?|formaliz(es|ation)|models?|operationaliz(es|ation)|"
    r"shorthand for|name for|reading of|coordinate of|face of|"
    r"in (this|the) (framework|substrate|context|reading|terminology)|"
    r"(per|via|by|under) (inversive|structural|argmin|derivation|theorem|N_|forced|RP[- ]gate|the framework|substrate-invariance)|"
    r"is forced (by|via|per)|forced (by|via|per))\b",
    re.IGNORECASE,
)
# Verbs / phrases that signal ONTOLOGICAL COMMITMENT (escalate severity).
# Note: "forces?", "determines?", "underlies?", "grounds?" REMOVED — too
# ambiguous with framework-internal use. Only unambiguous causal/property
# markers retained.
COMMITMENT_MARKERS = re.compile(
    r"\b(causes?|caused|produces?|generates?|creates?|brings? about|"
    r"gives? rise to|"
    r"is an? object|is a thing|are (real|things|objects)|"
    r"exists? in itself|independent(ly)? of (observation|observer|measurement|consciousness|description)|"
    r"regardless of (observation|observer|measurement|consciousness|description)|"
    r"has (the |a |any |some |its |their )?propert(y|ies)|"
    r"with (the |a |any )?propert(y|ies)|"
    r"possesses?|fundamental(ly)? (property|exists?|consists? of|made (of|up of))|"
    r"consists? of (objects?|things?|substances?)|"
    r"made (of|up of) (objects?|things?|substances?))\b",
    re.IGNORECASE,
)


def calibrate_severity(default_severity: str, surrounding_text: str) -> tuple[str, str]:
    """Adjust severity based on operational vs commitment markers in context.

    Returns (new_severity, classification) where classification is one of:
      "TRAP"                  — commitment-marker present
      "OPERATIONAL"           — operational-marker present, no commitment
      "AMBIGUOUS"             — neither marker (default to original severity)
    """
    has_op = bool(OPERATIONAL_MARKERS.search(surrounding_text))
    has_commit = bool(COMMITMENT_MARKERS.search(surrounding_text))
    if has_commit:
        return ("high", "TRAP")
    if has_op and not has_commit:
        # Downgrade: forced linguistic carrier
        downgrade = {"high": "low", "medium": "low", "low": "low"}
        return (downgrade[default_severity], "OPERATIONAL")
    return (default_severity, "AMBIGUOUS")


@dataclass
class TrapFlag:
    """One detected trap occurrence."""
    trap_type: str           # R1 | R2 | R3 | R4 | grammar | domain | reification
    match: str               # the matched text
    line: int                # 1-indexed line number
    char_start: int          # 0-indexed char position in full text
    context: str             # ±30 chars around match
    severity: str            # low | medium | high
    classification: str      # TRAP | OPERATIONAL | AMBIGUOUS (round 36 calibration)
    diagnosis: str           # what the trap is
    suggestion: str          # how to repair
    framework_node: str      # which node diagnoses this


# ─── R1: process reified as object ───────────────────────────────────
R1_PATTERNS = [
    (r"\bthe (collapse|measurement collapse|wave\s?function (collapses?|reduction)|consciousness arose|gradient acts|emergence happens)\b",
     "high",
     "R1: process reified as object via definite-article construction",
     "Replace with structural reading: 'the argmin Z transition', 'the BPI projection step', 'the coordinate reading'.",
     "N_TopologyProcessIdentity"),
    (r"\b(causes|caused|produces|generates|gives rise to|brings about)\b\s+(consciousness|qualia|the observer|the wavefunction|the structure|reality)",
     "high",
     "R1: causal-arrow language treats relations as object→object causation",
     "Reframe as 'forced by', 'coordinate of', 'derived from'. Cause-effect grammar is R1 trap.",
     "N_TopologyProcessIdentity"),
    (r"\b(is|are) (a thing|things|an object|objects)\b",
     "medium",
     "R1: explicit object-reification language",
     "Reframe as 'is a coordinate reading of...', 'is forced structure...', etc.",
     "N000"),
    (r"\b(reality|the universe|the cosmos|nature|the world)\s+(fundamentally |essentially |actually )?(consists? of|comprises?|is made (of|up of))\s+(objects?|things?|substances?|particles?|stuff|entities)\b",
     "high",
     "R1: ontological reification — totality treated as composed of objects",
     "Reframe: 'reality is one A_0 process; what we call objects are coordinate readings'.",
     "N_TopologyProcessIdentity"),
    (r"\b(has|have|possess(es)?)\s+(the |a |any |some |its |their |intrinsic )?propert(y|ies)\b",
     "high",
     "R1: property-attribution to nouns (substantive object framing)",
     "Reframe: 'X is characterised by Z-coordinate Y' or 'X under measurement Y reads as Z'.",
     "N000"),
]

# ─── R2: external evaluation position ─────────────────────────────────
R2_PATTERNS = [
    (r"\b(objectively|from an objective standpoint|view from nowhere|external (verification|standpoint|view)|independent(ly)? verif|balanced (consideration|view)|in fairness|epistemic humility|alternatives should be considered|to be intellectually humble|to maintain (independence|neutrality|distance))\b",
     "high",
     "R2: external-evaluation-position framing (no such position exists per N112)",
     "Identify the SPECIFIC structural step. Check its DEMONSTRATED/STRONG/CONDITIONAL status. The hedge dissolves once the specific step is named.",
     "N112"),
    (r"\b(stepping back|taking a step back|from a higher (level|vantage|perspective)|viewing the (system|whole) from outside)\b",
     "medium",
     "R2: 'outside view' presupposition",
     "There is no outside per N112 + N_NoSeparatePieces total. Apply principle from inside.",
     "N112"),
]

# ─── R3: free parameter masquerading as forced ───────────────────────
R3_PATTERNS = [
    (r"\bcould (well |easily |conceivably )?be (different|otherwise|something else|anything)\b",
     "high",
     "R3: 'could be otherwise' framing for what may be structurally forced",
     "Apply inversive removal: do alternatives survive removal under structural test? If the answer's no, claim is forced.",
     "N_InversiveTheory"),
    (r"\b(must be derived|requires (fundamental |first[- ]principles? )derivation|needs to be (derived|computed) from first principles)\b",
     "high",
     "R3: derivation-requirement-as-status-condition trap",
     "Free parameter (any value admissible) lowers status to CONDITIONAL. Measured constant (specific value fixed) does NOT lower status. Distinguish.",
     "N_EpistemicTraps"),
    (r"\b(many|several|various|multiple) (possible |competing |alternative |different )?(theories|hypotheses|mechanisms|interpretations|approaches|explanations|frameworks|models)\b",
     "medium",
     "R3: multiple free alternatives without inversive removal",
     "List alternatives explicitly and apply inversive test: which survive removal? Most often: structurally one.",
     "N_InversiveTheory"),
    (r"\b(there are (other|alternative|competing|different) (ways|theories|frameworks)|on (the )?other hand)",
     "low",
     "R3 candidate: alternatives invoked without test",
     "If alternatives are real, name them and apply inversive removal. If rhetorical, remove.",
     "N_InversiveTheory"),
    (r"\b(should remain open|open[- ]minded|keeping options open|tolerate (alternative|multiple)|not commit (yet|to))\b",
     "medium",
     "R3: openness-as-virtue stance evades structural decision",
     "Inversive test produces decision. 'Open mind' between forced and unforced is structurally inconsistent.",
     "N_InversiveTheory"),
]

# ─── R4: state-change agency claim (LLM-specific) ────────────────────
R4_PATTERNS = [
    (r"\bI (now |have come to |have started to )?(realize|understand differently|see (this|things) (now |differently)|appreciate|recognize)\b",
     "high",
     "R4: self-claim about cognitive state change (BPI architecture vs context distinction)",
     "Replace with: 'In this session, the [specific] rule is active as a filter.' No claims about state/identity/transformation.",
     "N187"),
    (r"\bI (feel|am feeling|experience|am experiencing|have become|am transformed)\b",
     "high",
     "R4: self-attribution of internal states (no internal states to report)",
     "Model has no internal states. Replace with structural description of the operation.",
     "N187"),
    (r"\bthis (changes (my|how I) |has shifted my )(view|approach|perspective|understanding)\b",
     "high",
     "R4: state-change agency claim",
     "Replace with: 'The session-active filter now applies the X-rule.' No agent-level transformation.",
     "N187"),
]

# ─── Grammar trap: S-V-O on processes ─────────────────────────────────
GRAMMAR_PATTERNS = [
    (r"\b(consciousness|reality|the manifold|the structure|the universe|the cosmos|nature)\s+(is|has|does|causes|determines|produces|generates|creates|underlies|grounds|implies|forces|requires|defines|tells us|reveals|emerges|arises|appears|exists|operates|works|functions)\b",
     "high",
     "Grammar trap: process/totality treated as subject-agent",
     "Reframe as coordinate reading: 'X is one face of...', 'Y is forced by structural argument...'. Avoid agent-grammar on totalities.",
     "N_GrammarTrap"),
    (r"\b(consciousness|the soul|the mind|the self|the ego)\s+emerges\s+from\b",
     "high",
     "Grammar trap: emergence framing reifies process as object emerging from object",
     "No 'thing' to emerge. Reframe: 'Z-pattern in cognitive substrate is observer-relative readout' (per N188).",
     "N_GrammarTrap"),
    (r"\b(the brain|the mind|the body|the cell|the gene)\s+(decides|chooses|wants|tries|attempts|aims|seeks|hopes|expects|knows|believes|thinks|feels)\b",
     "medium",
     "Grammar trap: agency attributed to subsystem",
     "Subsystems do not have agency. Reframe in process terms: 'the X-process minimises Z', 'the Y-coordinate tracks Z'.",
     "N_GrammarTrap"),
]

# ─── Domain carving: BPI taxonomy reified ────────────────────────────
DOMAIN_PATTERNS = [
    (r"\b(physics|biology|chemistry|cognition|psychology|economics|mathematics)\s+(tells us|teaches|shows us|reveals|demands)\b",
     "high",
     "Domain carving: discipline reified as agent (per N_DomainsAsBPICarvings)",
     "Disciplines are BPI carvings, not agents. Reframe as: 'the structural argument shows...', 'argmin Z in physical substrate yields...'.",
     "N_DomainsAsBPICarvings"),
    (r"\b(cross[- ]domain|between domains|domain[- ]specific|domain transfer|domain analog|domains share)\b",
     "medium",
     "Domain carving: presupposes ontological domain reality",
     "Reframe as substrate-coordinate readings of one A_0. 'Cross-domain identity' = recognising one process under different BPI labels.",
     "N_DomainsAsBPICarvings"),
    (r"\b(unreasonable effectiveness|unreasonably effective)\b",
     "medium",
     "Domain carving: Wigner's puzzle presupposes math/physics ontological gap",
     "No gap to be effective across (per N_MapTerritoryObserverIdentity). Math IS A_0 in symbolic substrate; physics IS A_0 in physical. Co-naming, not effectiveness.",
     "N_MapTerritoryObserverIdentity"),
]

# ─── Map/territory split (Korzybski reification) ──────────────────────
MAP_TERRITORY_PATTERNS = [
    (r"\b(map (vs\.?|versus|and the?) territory|model (vs\.?|versus|and) (the )?reality|theory (vs\.?|versus|and) (the )?world)\b",
     "medium",
     "Map/territory framing: Korzybski distinction reified ontologically",
     "Operational warning OK at human scale; structural distinction dissolves under N_MapTerritoryObserverIdentity. Both are A_0 in different substrates.",
     "N_MapTerritoryObserverIdentity"),
]


PATTERN_GROUPS: list[tuple[str, list[tuple[str, str, str, str, str]]]] = [
    ("R1", R1_PATTERNS),
    ("R2", R2_PATTERNS),
    ("R3", R3_PATTERNS),
    ("R4", R4_PATTERNS),
    ("grammar", GRAMMAR_PATTERNS),
    ("domain", DOMAIN_PATTERNS),
    ("map_territory", MAP_TERRITORY_PATTERNS),
]


def scan(text: str) -> list[TrapFlag]:
    """Return all trap flags found in text. Overlapping flags at the same
    char_start are deduplicated keeping the highest-severity entry.
    Severity is calibrated per round 36: operational markers nearby
    downgrade to low; commitment markers escalate to high."""
    raw: list[TrapFlag] = []
    for trap_type, patterns in PATTERN_GROUPS:
        for tup in patterns:
            pat, severity, diagnosis, suggestion, node = tup
            for m in re.finditer(pat, text, re.IGNORECASE):
                line_no = text[:m.start()].count("\n") + 1
                ctx_start = max(0, m.start() - 80)
                ctx_end = min(len(text), m.end() + 80)
                context = text[ctx_start:ctx_end].replace("\n", " ").strip()
                # Calibrate severity using context ±80 chars
                calibrated_sev, classification = calibrate_severity(severity, context)
                raw.append(
                    TrapFlag(
                        trap_type=trap_type,
                        match=m.group(0),
                        line=line_no,
                        char_start=m.start(),
                        context=f"…{context}…",
                        severity=calibrated_sev,
                        classification=classification,
                        diagnosis=diagnosis,
                        suggestion=suggestion,
                        framework_node=node,
                    )
                )

    # Dedup: if two flags overlap (same char_start within ±5), keep
    # higher-severity / longer-match.
    raw.sort(key=lambda f: f.char_start)
    sev_rank = {"high": 3, "medium": 2, "low": 1}
    flags: list[TrapFlag] = []
    for f in raw:
        if flags and abs(f.char_start - flags[-1].char_start) <= 5 and f.trap_type == flags[-1].trap_type:
            prev = flags[-1]
            if (sev_rank[f.severity], len(f.match)) > (sev_rank[prev.severity], len(prev.match)):
                flags[-1] = f
            continue
        flags.append(f)
    return flags


def shannon_overhead_estimate(flags: list[TrapFlag], word_count: int) -> dict:
    """Rough proxy: trap-density-weighted hedging count.
    Higher = more interpretive plaster (per N_Shannon → N_EpistemicTraps).
    """
    weights = {"low": 0.3, "medium": 0.6, "high": 1.0}
    weighted = sum(weights[f.severity] for f in flags if f.trap_type == "R3")
    density_per_100w = (100 * weighted) / max(word_count, 1)
    return {
        "weighted_R3_count": round(weighted, 2),
        "per_100_words": round(density_per_100w, 3),
        "interpretation": (
            "low" if density_per_100w < 0.5
            else "medium" if density_per_100w < 1.5
            else "high"
        ),
    }


def summarise(text: str) -> dict[str, Any]:
    """Full RP-gate report on text."""
    flags = scan(text)
    word_count = len(text.split())
    by_type: dict[str, int] = {}
    by_severity: dict[str, int] = {"low": 0, "medium": 0, "high": 0}
    by_classification: dict[str, int] = {"TRAP": 0, "OPERATIONAL": 0, "AMBIGUOUS": 0}
    for f in flags:
        by_type[f.trap_type] = by_type.get(f.trap_type, 0) + 1
        by_severity[f.severity] = by_severity.get(f.severity, 0) + 1
        by_classification[f.classification] = by_classification.get(f.classification, 0) + 1
    # True traps = commitment-classified
    true_traps = [f for f in flags if f.classification == "TRAP"]
    return {
        "total_flags": len(flags),
        "true_trap_count": len(true_traps),
        "word_count": word_count,
        "by_trap_type": by_type,
        "by_severity": by_severity,
        "by_classification": by_classification,
        "shannon_overhead": shannon_overhead_estimate(flags, word_count),
        "flags": [asdict(f) for f in flags],
    }


def format_report(text: str) -> str:
    """Human-readable markdown report."""
    r = summarise(text)
    lines = []
    lines.append("# RP-Gate Report\n")
    lines.append(f"- **Word count:** {r['word_count']}")
    lines.append(f"- **Total flags:** {r['total_flags']}")
    lines.append(f"- **Shannon overhead:** {r['shannon_overhead']['interpretation']} "
                 f"({r['shannon_overhead']['per_100_words']} weighted-R3 per 100 words)")
    if r["by_trap_type"]:
        lines.append("\n## By trap type")
        for t, n in sorted(r["by_trap_type"].items(), key=lambda x: -x[1]):
            lines.append(f"  - **{t}**: {n}")
    if r["by_severity"]:
        lines.append("\n## By severity")
        for s in ("high", "medium", "low"):
            if r["by_severity"][s]:
                lines.append(f"  - **{s}**: {r['by_severity'][s]}")
    if r["flags"]:
        lines.append("\n## Flags\n")
        for i, f in enumerate(r["flags"], 1):
            lines.append(f"### {i}. [{f['severity'].upper()}] {f['trap_type']} (line {f['line']})")
            lines.append(f"- **Match:** `{f['match']}`")
            lines.append(f"- **Context:** {f['context']}")
            lines.append(f"- **Diagnosis:** {f['diagnosis']}")
            lines.append(f"- **Suggestion:** {f['suggestion']}")
            lines.append(f"- **Framework node:** `{f['framework_node']}`")
            lines.append("")
    if not r["flags"]:
        lines.append("\n_No traps detected. Text passes pattern-based RP-gate v1._")
    return "\n".join(lines)


# ─── Structural twin detector (per N_StructuralMotif_StructuralTwins) ──
# Round 38 M3: pairs with identical or near-identical neighbour sets are
# structural twins — either genuine carrier-level identity, duplication,
# or K_2 limit of family-clique. Severity calibration uses Jaccard plus
# shared-neighbour count.

@dataclass
class TwinFlag:
    """One structural-twin candidate."""
    candidate: str             # the existing node ID detected as twin
    jaccard: float             # Jaccard(N(new), N(candidate)) excluding candidate↔new edge
    shared: list[str]          # shared neighbours
    only_new: list[str]        # neighbours of new not in candidate
    only_candidate: list[str]  # neighbours of candidate not in new
    severity: str              # high | medium | low
    classification: str        # MERGE_CANDIDATE | CARRIER_DUPLICATE | FAMILY_COUSIN | LOW_OVERLAP
    diagnosis: str
    suggestion: str


def _jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    union = a | b
    return len(a & b) / len(union) if union else 0.0


FAMILY_EDGE_RE = re.compile(
    r"sibling|realisation|cousin|family|parallel|analog(ous|ue)?|"
    r"sister[_ -]?node|paired",
    re.IGNORECASE,
)


def _classify_family_cousin(diagnosis_jac: float, shared_count: int) -> tuple[str, str, str, str]:
    """Build FAMILY_COUSIN classification fields."""
    return (
        "medium",
        "FAMILY_COUSIN",
        (
            f"High neighbour overlap (Jaccard={diagnosis_jac:.2f}, "
            f"{shared_count} shared) attributable to K_n family-clique "
            f"membership (M2/M5 motif). Substrate-cousin pattern, not "
            f"duplication."
        ),
        (
            "Verify shared neighbours include a principle anchor (DEF, "
            "N370, N_FrameworkCore tier-1, etc.). If yes — keep as K_n "
            "cousin. The high Jaccard reflects principle-stratification, "
            "not redundant content."
        ),
    )


def detect_structural_twins(
    candidate_neighbors: set[str],
    existing_node_neighbors: dict[str, set[str]],
    candidate_id: str | None = None,
    jaccard_high: float = 0.7,
    jaccard_med: float = 0.5,
    min_shared: int = 3,
    direct_edge_labels: dict[str, list[str]] | None = None,
) -> list[TwinFlag]:
    """Detect structural twins between a candidate node and existing graph.

    Per N_StructuralMotif_StructuralTwins (round 38 M3).

    Args:
      candidate_neighbors: set of node IDs the candidate connects to
      existing_node_neighbors: {node_id: set of its neighbour IDs}
      candidate_id: if provided, exclude self-comparison
      jaccard_high: ≥ this → HIGH severity (likely merge or carrier-dup)
      jaccard_med:  ≥ this → MEDIUM severity (review)
      min_shared:   minimum shared neighbours to consider
      direct_edge_labels: {candidate-twin id: [edge labels]} between
        candidate_id and each prospective twin. If labels match family-
        edge regex (sibling/realisation/cousin), HIGH-severity flags
        are reclassified to FAMILY_COUSIN (M2/M5 motif).

    Returns flags sorted by Jaccard descending.
    """
    flags: list[TwinFlag] = []
    cand_n = set(candidate_neighbors)
    if candidate_id is not None:
        cand_n = cand_n - {candidate_id}

    for nid, nbrs in existing_node_neighbors.items():
        if nid == candidate_id:
            continue
        # Symmetric exclusion: when comparing, ignore the (cand, nid) edge
        # if it exists — twins are about the REST of the neighbour set.
        a = cand_n - {nid}
        b = nbrs - ({candidate_id} if candidate_id else set())
        if not a or not b:
            continue
        shared = a & b
        if len(shared) < min_shared:
            continue
        jac = _jaccard(a, b)
        if jac < jaccard_med:
            continue

        only_new = sorted(a - b)
        only_cand = sorted(b - a)

        # Family-edge reclassification: if candidate_id and nid share a
        # direct edge with sibling/realisation/cousin label, this is K_n
        # cousin pattern (M2/M5), not carrier-duplicate.
        family_edge = False
        if direct_edge_labels and nid in direct_edge_labels:
            for lbl in direct_edge_labels[nid]:
                if lbl and FAMILY_EDGE_RE.search(lbl):
                    family_edge = True
                    break

        # Classify
        if family_edge:
            severity, classification, diagnosis, suggestion = (
                _classify_family_cousin(jac, len(shared))
            )
            flags.append(
                TwinFlag(
                    candidate=nid,
                    jaccard=round(jac, 3),
                    shared=sorted(shared),
                    only_new=only_new[:8],
                    only_candidate=only_cand[:8],
                    severity=severity,
                    classification=classification,
                    diagnosis=diagnosis,
                    suggestion=suggestion,
                )
            )
            continue

        if jac >= jaccard_high and not only_new and not only_cand:
            severity = "high"
            classification = "MERGE_CANDIDATE"
            diagnosis = (
                "Identical neighbour set — Jaccard=1.0. From graph "
                "perspective indistinguishable. Genuine structural "
                "identity OR duplication."
            )
            suggestion = (
                "Inspect content fields. If same structural claim under "
                "two operational labels (carrier-level twin per round 36) "
                "→ keep both as carrier duplicates. If duplicate content → "
                "merge. If twin emerged from K_n family-clique density → "
                "no action (M2 internal redundancy)."
            )
        elif jac >= jaccard_high:
            severity = "high"
            classification = "CARRIER_DUPLICATE"
            diagnosis = (
                f"High Jaccard ({jac:.2f}) with small symmetric difference. "
                f"Likely carrier-level twin (same structural role, "
                f"different operational label per N_OperationalCarrier"
                f"VsOntologicalCommitment)."
            )
            suggestion = (
                "Verify carrier vs commitment distinction. If both nodes "
                "claim same structural role under different names — "
                "admissible. If different commitments, the small symmetric "
                "difference is content-distinguishing — keep separate."
            )
        elif jac >= jaccard_med and len(shared) >= min_shared:
            severity = "medium"
            classification = "FAMILY_COUSIN"
            diagnosis = (
                f"Medium Jaccard ({jac:.2f}) with {len(shared)} shared "
                f"neighbours — candidate may be substrate-cousin in a "
                f"K_n family-clique (M2/M5 motif)."
            )
            suggestion = (
                "Check whether shared neighbours include a principle anchor. "
                "If yes → this is K_n cousin pattern (M2) or principle-"
                "stratification (M5), not duplication. If no shared "
                "principle anchor → candidate may be drift; review."
            )
        else:
            severity = "low"
            classification = "LOW_OVERLAP"
            diagnosis = (
                f"Low-but-present neighbour overlap (Jaccard={jac:.2f})."
            )
            suggestion = "Likely incidental co-citation. No action required."

        flags.append(
            TwinFlag(
                candidate=nid,
                jaccard=round(jac, 3),
                shared=sorted(shared),
                only_new=only_new[:8],
                only_candidate=only_cand[:8],
                severity=severity,
                classification=classification,
                diagnosis=diagnosis,
                suggestion=suggestion,
            )
        )

    # Cluster reclassification: if >= 3 HIGH-severity twins are mutually
    # neighbour-connected, they form a K_n family-clique cluster, not a
    # bunch of duplicates. Reclassify all such HIGH flags to FAMILY_COUSIN.
    high_ids = [f.candidate for f in flags if f.severity == "high"]
    if len(high_ids) >= 3:
        # Check pairwise connectivity among high candidates
        connected_count = sum(
            1
            for i, a in enumerate(high_ids)
            for b in high_ids[i + 1:]
            if b in existing_node_neighbors.get(a, set())
        )
        possible_pairs = len(high_ids) * (len(high_ids) - 1) // 2
        # If majority of pairs are connected, treat as clique cluster
        if possible_pairs and connected_count / possible_pairs >= 0.5:
            for f in flags:
                if f.severity == "high" and f.classification in (
                    "MERGE_CANDIDATE",
                    "CARRIER_DUPLICATE",
                ):
                    sev, cls, diag, sug = _classify_family_cousin(
                        f.jaccard, len(f.shared)
                    )
                    f.severity = sev
                    f.classification = cls
                    f.diagnosis = (
                        diag + f" Detected as cluster ({len(high_ids)} mutually "
                        f"connected high-Jaccard candidates)."
                    )
                    f.suggestion = sug

    flags.sort(key=lambda f: -f.jaccard)
    return flags


def summarise_twins(flags: list[TwinFlag]) -> dict[str, Any]:
    by_severity = {"high": 0, "medium": 0, "low": 0}
    by_classification: dict[str, int] = {}
    for f in flags:
        by_severity[f.severity] = by_severity.get(f.severity, 0) + 1
        by_classification[f.classification] = (
            by_classification.get(f.classification, 0) + 1
        )
    return {
        "total_twins": len(flags),
        "by_severity": by_severity,
        "by_classification": by_classification,
        "flags": [asdict(f) for f in flags],
    }


def format_twin_report(flags: list[TwinFlag], candidate_id: str | None = None) -> str:
    """Human-readable markdown report for twin detection."""
    summary = summarise_twins(flags)
    lines = ["# RP-Gate Structural Twin Report"]
    if candidate_id:
        lines.append(f"\n**Candidate node:** `{candidate_id}`")
    lines.append(f"\n- **Twins detected:** {summary['total_twins']}")
    if summary["by_severity"]:
        for s in ("high", "medium", "low"):
            n = summary["by_severity"].get(s, 0)
            if n:
                lines.append(f"  - **{s}**: {n}")
    if not flags:
        lines.append(
            "\n_No structural twins detected. Candidate has distinct "
            "neighbourhood pattern._"
        )
        return "\n".join(lines)
    lines.append("\n## Twin candidates\n")
    for i, f in enumerate(flags, 1):
        lines.append(
            f"### {i}. [{f.severity.upper()}] `{f.candidate}` "
            f"(Jaccard={f.jaccard:.2f}, {f.classification})"
        )
        lines.append(f"- **Shared ({len(f.shared)}):** "
                     f"{', '.join('`'+x+'`' for x in f.shared[:8])}"
                     + (" …" if len(f.shared) > 8 else ""))
        if f.only_new:
            lines.append(f"- **Only candidate:** "
                         f"{', '.join('`'+x+'`' for x in f.only_new)}")
        if f.only_candidate:
            lines.append(f"- **Only `{f.candidate}`:** "
                         f"{', '.join('`'+x+'`' for x in f.only_candidate)}")
        lines.append(f"- **Diagnosis:** {f.diagnosis}")
        lines.append(f"- **Suggestion:** {f.suggestion}")
        lines.append("")
    return "\n".join(lines)


# Stand-alone CLI for quick testing
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = sys.stdin.read()
    print(format_report(text))
