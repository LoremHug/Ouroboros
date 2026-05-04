"""Migrate manifold_graph.txt → Kuzu DB.

Idempotent: drops and recreates DB on each run.
Parses node blocks ([N_xxx] ... fields ... edges).
Extracts: CLAIM, WHY DEMONSTRATED/STRONG/CONDITIONAL/OPERATIONAL, NOT, edges.
Filters spurious section markers (META, CONCL, NORM_SILENCE).
Marks "Stub — Referenced in Edge Lists" entries as is_placeholder.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from schema import Node, Edge, Status, EdgeStatus, Layer, layer_of  # noqa: E402
from scripts.db import connect, reset, DB_PATH  # noqa: E402
from scripts import additions as additions_io  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
GRAPH_FILE = ROOT / "manifold_graph.txt"

# Allowlist for valid node IDs: DEF, Nxxx (numeric), N_Xxx (named).
# Spurious markers like META/CONCL/NORM_SILENCE are filtered out.
VALID_ID_RE = re.compile(r"^(DEF|N\d+[a-z]?|N_[A-Za-z]\w*)$")

NODE_HEADER_RE = re.compile(r"^\[([A-Za-z0-9_]+)\](?:\s*\((.*?)\))?\s*$")
STATUS_RE = re.compile(r"^Status:\s*(.+?)(?:\s*\|\s*A\s*=\s*(\S+))?\s*$")

# Field markers that begin multi-line node-level field bodies.
# Each runs until the next marker, edge line, node header, or comment.
FIELD_MARKERS = {
    "CLAIM": "summary",
    "WHY DEMONSTRATED": "why_status",
    "WHY STRONG": "why_status",
    "WHY CONDITIONAL": "why_status",
    "WHY OPERATIONAL": "why_status",
    "WHY NOT DEMONSTRATED": "why_status",
    "WHY NOT PURE DEMONSTRATED": "why_status",
    "NOT": "not_misinterpretations",
}
FIELD_RE = re.compile(
    r"^(" + "|".join(re.escape(k) for k in FIELD_MARKERS) + r"):\s*(.*)$"
)

EDGE_RE = re.compile(
    r"^([A-Za-z0-9_]+)\s*-->\s*([A-Za-z0-9_]+)\s*"
    r"(?::\s*([^\[\n]+?))?\s*"
    r"(?:\[([A-Z])\])?\s*$"
)


def parse_status(s: str) -> Status:
    """First token of multi-status (e.g. 'DEMONSTRATED / STRONG' → DEMONSTRATED)."""
    primary = s.strip().split("/")[0].strip().split("(")[0].strip()
    try:
        return Status(primary)
    except ValueError:
        return Status.STUB


def parse_anchors(a: str | None) -> tuple[int, bool]:
    if not a:
        return 0, False
    a = a.strip()
    if a in ("∞", r"\infty", "infinity", "inf"):
        return 0, True
    nums = re.findall(r"\d+", a)
    if not nums:
        return 0, False
    return max(int(n) for n in nums), False


def parse_graph(text: str) -> tuple[dict[str, Node], list[Edge]]:
    nodes: dict[str, Node] = {}
    edges: list[Edge] = []
    skipped_markers: list[str] = []

    lines = text.splitlines()
    n = len(lines)

    # Walking state for current node
    cur: dict | None = None  # active node accumulator
    cur_field: str | None = None  # field currently being accumulated
    cur_field_lines: list[str] = []

    def commit_field():
        """Save current field body into current node."""
        nonlocal cur_field, cur_field_lines
        if cur is None or cur_field is None:
            cur_field = None
            cur_field_lines = []
            return
        body = "\n".join(cur_field_lines).strip()
        # Append to existing (multiple WHY blocks merge)
        prev = cur.get(cur_field, "")
        cur[cur_field] = (prev + "\n\n" + body).strip() if prev else body
        cur_field = None
        cur_field_lines = []

    def commit_node():
        nonlocal cur
        if cur is None:
            return
        commit_field()
        title = cur.get("title", "")
        is_placeholder = "Stub — Referenced" in title or "stub" in title.lower()
        nodes[cur["id"]] = Node(
            id=cur["id"],
            title=title,
            layer=layer_of(cur["id"]),
            status=cur.get("status", Status.STUB),
            anchors=cur.get("anchors", 0),
            a_infinity=cur.get("a_infinity", False),
            summary=cur.get("summary", "")[:1000],
            why_status=cur.get("why_status", ""),
            not_misinterpretations=cur.get("not_misinterpretations", ""),
            content="\n".join(cur.get("content_lines", [])).strip(),
            is_placeholder=is_placeholder,
        )
        cur = None

    i = 0
    while i < n:
        line = lines[i]
        stripped = line.rstrip()

        # Skip section comments
        if stripped.startswith("%"):
            commit_field()
            i += 1
            continue

        # Node header
        m = NODE_HEADER_RE.match(stripped)
        if m:
            commit_node()
            nid = m.group(1)
            if not VALID_ID_RE.match(nid):
                skipped_markers.append(nid)
                cur = None
                i += 1
                continue
            cur = {
                "id": nid,
                "title": (m.group(2) or "").strip(),
                "content_lines": [],
            }
            i += 1
            continue

        # Status (only valid in active node)
        if cur is not None:
            sm = STATUS_RE.match(stripped)
            if sm:
                commit_field()
                cur["status"] = parse_status(sm.group(1))
                anchors, a_inf = parse_anchors(sm.group(2))
                cur["anchors"] = anchors
                cur["a_infinity"] = a_inf
                i += 1
                continue

            # New field marker (CLAIM:, WHY *:, NOT:)
            fm = FIELD_RE.match(stripped)
            if fm:
                commit_field()
                cur_field = FIELD_MARKERS[fm.group(1)]
                first_value = fm.group(2).strip()
                if first_value:
                    cur_field_lines = [first_value]
                else:
                    cur_field_lines = []
                i += 1
                continue

        # Edge line
        em = EDGE_RE.match(stripped)
        if em and "-->" in stripped:
            commit_field()
            src, tgt, label, est = em.groups()
            try:
                edge_status = EdgeStatus(est) if est else EdgeStatus.D
            except ValueError:
                edge_status = EdgeStatus.D
            edges.append(Edge(
                source=src,
                target=tgt,
                label=(label or "").strip(),
                edge_status=edge_status,
            ))
            i += 1
            continue

        # Continuation: append to current field if active, else to free content
        if cur is not None:
            if cur_field is not None:
                if line.strip():
                    cur_field_lines.append(line.rstrip())
                elif cur_field_lines:
                    # Blank line ends the field body
                    commit_field()
            else:
                cur["content_lines"].append(line)

        i += 1

    commit_node()

    if skipped_markers:
        print(f"skipped {len(skipped_markers)} non-node markers: {', '.join(skipped_markers)}")

    # Synthesize stubs for edge endpoints not seen in any block.
    # Filter edges referencing skipped markers.
    valid_edges = []
    for e in edges:
        if not VALID_ID_RE.match(e.source) or not VALID_ID_RE.match(e.target):
            continue
        valid_edges.append(e)
    edges = valid_edges

    for e in edges:
        for nid in (e.source, e.target):
            if nid not in nodes:
                nodes[nid] = Node(
                    id=nid,
                    layer=layer_of(nid),
                    status=Status.STUB,
                    summary="(referenced in edges, no block content)",
                    is_placeholder=True,
                )
    return nodes, edges


def write_to_kuzu(nodes: dict[str, Node], edges: list[Edge]) -> None:
    reset()
    db, conn = connect()

    for n in nodes.values():
        conn.execute(
            """
            CREATE (n:Node {
                id: $id, title: $title, layer: $layer, status: $status,
                anchors: $anchors, a_infinity: $a_inf,
                summary: $summary, why_status: $why,
                not_misinterpretations: $not_m,
                content: $content,
                z_struct: $zs, z_therm: $zt, z_hidden: $zh, level: $lvl,
                is_placeholder: $ph
            })
            """,
            {
                "id": n.id, "title": n.title, "layer": n.layer.value,
                "status": n.status.value, "anchors": n.anchors,
                "a_inf": n.a_infinity,
                "summary": n.summary,
                "why": n.why_status,
                "not_m": n.not_misinterpretations,
                "content": n.content,
                "zs": n.z_struct, "zt": n.z_therm, "zh": n.z_hidden,
                "lvl": n.level, "ph": n.is_placeholder,
            },
        )

    seen: set[tuple[str, str, str]] = set()
    for e in edges:
        key = (e.source, e.target, e.label)
        if key in seen:
            continue
        seen.add(key)
        conn.execute(
            """
            MATCH (a:Node {id: $src}), (b:Node {id: $tgt})
            CREATE (a)-[:Edge {
                label: $label, edge_status: $st,
                justification: $j, why_forced: $w
            }]->(b)
            """,
            {
                "src": e.source, "tgt": e.target, "label": e.label,
                "st": e.edge_status.value,
                "j": e.justification, "w": e.why_forced,
            },
        )


def apply_additions(conn) -> tuple[int, int]:
    """Apply nodes and edges from additions.yaml on top of the migrated DB."""
    data = additions_io.load()
    n_added = 0
    e_added = 0

    for nspec in data.get("nodes") or []:
        nid = nspec["id"]
        # Upsert: delete if exists, then create.
        conn.execute("MATCH (n:Node {id: $id}) DETACH DELETE n", {"id": nid})
        layer_value = nspec.get("layer") or layer_of(nid).value
        params = {
            "id": nid,
            "title": nspec.get("title", ""),
            "layer": layer_value,
            "status": nspec.get("status", "STUB"),
            "anchors": int(nspec.get("anchors", 0)),
            "a_inf": bool(nspec.get("a_infinity", False)),
            "summary": nspec.get("summary", ""),
            "why": nspec.get("why_status", ""),
            "not_m": nspec.get("not_misinterpretations", ""),
            "content": nspec.get("content", ""),
            "zs": float(nspec.get("z_struct", 0.0)),
            "zt": float(nspec.get("z_therm", 0.0)),
            "zh": float(nspec.get("z_hidden", 0.0)),
            "lvl": int(nspec.get("level", -1)),
            "ph": bool(nspec.get("is_placeholder", False)),
        }
        conn.execute(
            """
            CREATE (n:Node {
                id: $id, title: $title, layer: $layer, status: $status,
                anchors: $anchors, a_infinity: $a_inf,
                summary: $summary, why_status: $why,
                not_misinterpretations: $not_m, content: $content,
                z_struct: $zs, z_therm: $zt, z_hidden: $zh, level: $lvl,
                is_placeholder: $ph
            })
            """,
            params,
        )
        n_added += 1

    for espec in data.get("edges") or []:
        # Verify endpoints exist
        for endpoint_id in (espec["source"], espec["target"]):
            r = conn.execute("MATCH (n:Node {id: $id}) RETURN count(n)", {"id": endpoint_id})
            if r.get_next()[0] == 0:
                raise RuntimeError(
                    f"additions.yaml references missing node {endpoint_id} "
                    f"in edge {espec['source']} → {espec['target']} : {espec.get('label','')}"
                )
        # Skip if exact (source, target, label) already present
        r = conn.execute(
            """
            MATCH (a:Node {id: $src})-[e:Edge]->(b:Node {id: $tgt})
            WHERE e.label = $lbl
            RETURN count(e)
            """,
            {"src": espec["source"], "tgt": espec["target"], "lbl": espec.get("label", "")},
        )
        if r.get_next()[0] > 0:
            continue
        conn.execute(
            """
            MATCH (a:Node {id: $src}), (b:Node {id: $tgt})
            CREATE (a)-[:Edge {
                label: $lbl, edge_status: $st,
                justification: $j, why_forced: $w
            }]->(b)
            """,
            {
                "src": espec["source"], "tgt": espec["target"],
                "lbl": espec.get("label", ""),
                "st": espec.get("edge_status", "D"),
                "j": espec.get("justification", "") or "",
                "w": espec.get("why_forced", "") or "",
            },
        )
        e_added += 1

    return n_added, e_added


def main() -> None:
    text = GRAPH_FILE.read_text(encoding="utf-8")
    nodes, edges = parse_graph(text)
    print(f"parsed: {len(nodes)} nodes, {len(edges)} edges")

    by_status: dict[str, int] = {}
    by_layer: dict[str, int] = {}
    placeholders = 0
    has_why = 0
    has_not = 0
    for n in nodes.values():
        by_status[n.status.value] = by_status.get(n.status.value, 0) + 1
        by_layer[n.layer.value] = by_layer.get(n.layer.value, 0) + 1
        if n.is_placeholder:
            placeholders += 1
        if n.why_status:
            has_why += 1
        if n.not_misinterpretations:
            has_not += 1
    print("status     :", by_status)
    print("layer      :", by_layer)
    print(f"placeholders: {placeholders}")
    print(f"with why_status: {has_why}")
    print(f"with NOT field : {has_not}")

    write_to_kuzu(nodes, edges)
    print(f"wrote → {DB_PATH}")

    # Apply additions.yaml on top
    db, conn = connect()
    n_added, e_added = apply_additions(conn)
    if n_added or e_added:
        print(f"applied additions.yaml: +{n_added} nodes, +{e_added} edges")


if __name__ == "__main__":
    main()
