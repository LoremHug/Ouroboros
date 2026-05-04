"""Parse THE_IMPEDANCE_MANIFOLD_v3_6.tex into sections, store as Section nodes,
link to Node entries via DESCRIBED_BY.

Run after migrate.py. Idempotent: drops Section/DESCRIBED_BY before refilling.
Heuristic-matches sections to Nodes by name, prints unmatched for review.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.db import connect  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TEX = ROOT / "THE_IMPEDANCE_MANIFOLD_v3_6.tex"

SECTION_RE = re.compile(r"\\(chapter|section|subsection)\*?(?:\[[^\]]*\])?\{([^}]*)\}")
LABEL_RE = re.compile(r"\\label\{(sec:[^}]+|chap:[^}]+|part:[^}]+)\}")

# Manual overrides — node_id → list of sec labels.
# Anything not listed falls back to heuristic (substring match).
MANUAL_MAP: dict[str, list[str]] = {
    "DEF": ["sec:a0-method", "sec:epistemic-manifold"],
    "N_Triangulation": ["sec:triangulation"],
    "N_BPIEngagement": ["sec:bpi-engagement"],
    "N_DopaminePredictionError": ["sec:dopamine-prediction-error"],
    "N_FEP": ["sec:hom-fep"],
    "N_Logic": ["sec:logic-a0"],
    "N_TopologyProcessIdentity": ["sec:topology-process-identity"],
    "N_LeptonMassScale": ["sec:lepton-mass-scale"],
    "N_AestheticEngagement": ["sec:aesthetic-engagement", "sec:aesthetic-measure"],
    "N_EpistemicTraps": ["sec:traps56"],
    "N_WylerStepG": ["sec:alpha-fixedpoint"],
    "N_Bar": ["sec:koide", "sec:koide-45deg"],
    "N304": ["sec:n304-llm-fractal"],
    "N310": ["sec:iso-kolmogorov"],
    "N371": ["sec:bpi-origin"],
    "N370": ["sec:l31-minimality", "sec:z3-minimality"],
    "N372": ["sec:sr2ruo4"],
    "N373": ["sec:ute2"],
    "N374": ["sec:upt3"],
    "N375": ["sec:cuprates"],
    "N376": ["sec:iron-sc"],
    "N377": ["sec:sae-absorption"],
    "N365": ["sec:taylor-relaxation"],
    "N366": ["sec:fusion-z"],
    "N367": ["sec:rotodiffusion"],
    "N363": ["sec:zipf"],
    "N330": ["sec:hom-social"],
    "N332": ["sec:hom-social"],
    "N_PhiAttractor": ["sec:fibonacci"],
    "N_EngagementArchitecture": [
        "sec:adap-statement", "sec:adap-cross-substrate",
        "sec:adap-primitives", "sec:adap-status",
        "sec:adap-corpus", "sec:adap-algo1", "sec:adap-algo2",
        "sec:adap-ai-validation", "sec:ai-adap-failures",
        "sec:music-stability", "sec:music-production",
        "sec:music-harmony", "sec:hom-music",
    ],
    "N327": ["sec:weber-fechner", "sec:weber-snr"],
    "N_Math": ["sec:n301-math-language"],
    "N_NoSeparatePieces": ["sec:reduction1", "sec:reduction2", "sec:reduction3", "sec:reduction4"],
    "N_CommThm": ["sec:opt-comm"],
}


def parse_tex_sections(tex: str) -> list[dict]:
    """Walk text, emit sections {label, title, kind, body}."""
    lines = tex.splitlines()
    n = len(lines)
    sections: list[dict] = []

    # Find all (line_no, kind, title, label?) tuples
    markers = []
    for i, line in enumerate(lines):
        for m in SECTION_RE.finditer(line):
            kind, title = m.group(1), m.group(2).strip()
            # Look for label on same or next non-empty line
            label = None
            lm = LABEL_RE.search(line)
            if lm:
                label = lm.group(1)
            else:
                # Check next 3 lines for label
                for j in range(i + 1, min(i + 4, n)):
                    nlm = LABEL_RE.search(lines[j])
                    if nlm:
                        label = nlm.group(1)
                        break
            markers.append((i, kind, title, label))

    # Slice text between consecutive markers (regardless of kind)
    for idx, (start, kind, title, label) in enumerate(markers):
        end = markers[idx + 1][0] if idx + 1 < len(markers) else n
        body_lines = lines[start + 1:end]
        body = "\n".join(body_lines).strip()
        # Strip excess LaTeX commands from body for readability
        body = clean_latex(body)
        sections.append({
            "label": label,
            "title": clean_latex_inline(title),
            "kind": kind,
            "body": body[:8000],  # cap to keep DB writes reasonable
        })
    return [s for s in sections if s["label"]]  # only labeled


_RE_LABEL = re.compile(r"\\label\{[^}]+\}")
_RE_TEXTBF = re.compile(r"\\textbf\{([^}]*)\}")
_RE_TEXTIT = re.compile(r"\\textit\{([^}]*)\}")
_RE_EMPH = re.compile(r"\\emph\{([^}]*)\}")
_RE_TEXORPDFSTRING = re.compile(r"\\texorpdfstring\{([^}]*)\}\{[^}]*\}")
_RE_BOX_BEGIN = re.compile(r"\\begin\{[a-zA-Z]+\}(\[[^\]]*\])?")
_RE_BOX_END = re.compile(r"\\end\{[a-zA-Z]+\}")
_RE_TILDE = re.compile(r"~")
_RE_DASH = re.compile(r"---")
_RE_DOUBLE_QUOTE = re.compile(r"``|''")


def clean_latex_inline(s: str) -> str:
    s = _RE_TEXORPDFSTRING.sub(r"\1", s)
    s = _RE_TEXTBF.sub(r"\1", s)
    s = _RE_TEXTIT.sub(r"\1", s)
    s = _RE_EMPH.sub(r"\1", s)
    s = _RE_LABEL.sub("", s)
    s = _RE_TILDE.sub(" ", s)
    s = _RE_DASH.sub("—", s)
    s = _RE_DOUBLE_QUOTE.sub('"', s)
    return s.strip()


def clean_latex(s: str) -> str:
    s = clean_latex_inline(s)
    s = _RE_BOX_BEGIN.sub("", s)
    s = _RE_BOX_END.sub("", s)
    # Collapse runs of blank lines
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def heuristic_match(node_id: str, sections: list[dict]) -> list[str]:
    """Fallback: substring match between node id and section label/title."""
    name = node_id.replace("N_", "").lower()
    if not name or name in {"def"}:
        return []
    matches: list[str] = []
    # Strip common short suffixes that confuse matches
    candidates = {name, name.replace("engagement", ""), name.replace("predictionerror", "")}
    for sec in sections:
        if not sec["label"]:
            continue
        label_clean = sec["label"].replace("sec:", "").replace("-", "").lower()
        title_clean = sec["title"].lower().replace(" ", "").replace("-", "")
        for cand in candidates:
            if len(cand) >= 4 and (cand in label_clean or cand in title_clean):
                matches.append(sec["label"])
                break
    return matches


def bootstrap_section_schema(conn) -> None:
    """Idempotent: drop Section table + DESCRIBED_BY rel and recreate."""
    # Kuzu syntax: drop with cascade, but simpler — try to drop, ignore if missing
    for stmt in [
        "DROP TABLE DESCRIBED_BY",
        "DROP TABLE Section",
    ]:
        try:
            conn.execute(stmt)
        except Exception:
            pass
    conn.execute("""
        CREATE NODE TABLE Section(
            label STRING PRIMARY KEY,
            title STRING,
            kind STRING,
            body STRING
        )
    """)
    conn.execute("""
        CREATE REL TABLE DESCRIBED_BY(
            FROM Node TO Section
        )
    """)


def main() -> None:
    if not TEX.exists():
        print(f"error: {TEX} not found")
        sys.exit(1)

    text = TEX.read_text(encoding="utf-8", errors="replace")
    sections = parse_tex_sections(text)
    print(f"parsed {len(sections)} labeled sections from .tex")

    # Dedup by label: keep the longest body
    by_label: dict[str, dict] = {}
    for s in sections:
        prev = by_label.get(s["label"])
        if prev is None or len(s["body"]) > len(prev["body"]):
            by_label[s["label"]] = s
    sections = list(by_label.values())
    print(f"unique by label: {len(sections)}")

    db, conn = connect()
    bootstrap_section_schema(conn)

    # Insert all sections
    for s in sections:
        conn.execute(
            """
            CREATE (s:Section {
                label: $lbl, title: $ttl, kind: $k, body: $body
            })
            """,
            {"lbl": s["label"], "ttl": s["title"], "k": s["kind"], "body": s["body"]},
        )
    print(f"inserted {len(sections)} Section rows")

    # Build mapping
    sec_labels = {s["label"] for s in sections}
    res = conn.execute("MATCH (n:Node) RETURN n.id")
    node_ids: list[str] = []
    while res.has_next():
        node_ids.append(res.get_next()[0])

    linked = 0
    unmatched: list[str] = []
    for nid in node_ids:
        labels = MANUAL_MAP.get(nid, [])
        if not labels:
            labels = heuristic_match(nid, sections)
        # Filter to existing labels
        labels = [l for l in labels if l in sec_labels]
        if not labels:
            unmatched.append(nid)
            continue
        for lbl in labels:
            conn.execute(
                """
                MATCH (n:Node {id: $nid}), (s:Section {label: $lbl})
                CREATE (n)-[:DESCRIBED_BY]->(s)
                """,
                {"nid": nid, "lbl": lbl},
            )
            linked += 1

    print(f"linked {linked} Node→Section relationships")
    print(f"unmatched nodes ({len(unmatched)}): {', '.join(unmatched[:30])}{'…' if len(unmatched) > 30 else ''}")


if __name__ == "__main__":
    main()
