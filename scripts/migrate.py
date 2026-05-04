"""Migrate manifold_graph.txt → Kuzu DB.

Idempotent: drops and recreates DB on each run.
Parses node blocks ([N_xxx] ... edges) and adjacency lines (A --> B : label [D]).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

# Make package imports work when run as script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from schema import Node, Edge, Status, EdgeStatus, layer_of  # noqa: E402
from scripts.db import connect, reset, DB_PATH  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
GRAPH_FILE = ROOT / "manifold_graph.txt"

NODE_HEADER_RE = re.compile(r"^\[([A-Za-z0-9_]+)\](?:\s*\((.*?)\))?\s*$")
STATUS_RE = re.compile(r"^Status:\s*(.+?)(?:\s*\|\s*A\s*=\s*(\S+))?\s*$")
CLAIM_RE = re.compile(r"^CLAIM:\s*(.+)$", re.IGNORECASE)
EDGE_RE = re.compile(
    r"^([A-Za-z0-9_]+)\s*-->\s*([A-Za-z0-9_]+)\s*"
    r"(?::\s*([^\[\n]+?))?\s*"
    r"(?:\[([A-Z])\])?\s*$"
)


def parse_status(s: str) -> tuple[Status, int, bool]:
    """Extract primary status, anchor count, and a_infinity flag."""
    s_part = s.strip()
    # Multi-status lines like "DEMONSTRATED / STRONG" → take first
    primary = s_part.split("/")[0].strip().split("(")[0].strip()
    try:
        status = Status(primary)
    except ValueError:
        status = Status.STUB
    return status


def parse_anchors(a: str | None) -> tuple[int, bool]:
    """Parse 'A=N' or 'A=∞'. Returns (anchors, a_infinity)."""
    if not a:
        return 0, False
    a = a.strip()
    if a in ("∞", r"\infty", "infinity", "inf"):
        return 0, True
    # Multi-value like "4,5" — take max
    nums = re.findall(r"\d+", a)
    if not nums:
        return 0, False
    return max(int(n) for n in nums), False


def parse_graph(text: str) -> tuple[dict[str, Node], list[Edge]]:
    nodes: dict[str, Node] = {}
    edges: list[Edge] = []

    lines = text.splitlines()
    i = 0
    current_id: str | None = None
    current_title: str = ""
    current_status: Status = Status.STUB
    current_anchors: int = 0
    current_a_inf: bool = False
    current_claim: str = ""
    current_content: list[str] = []

    def flush():
        nonlocal current_id, current_title, current_status
        nonlocal current_anchors, current_a_inf, current_claim, current_content
        if current_id is None:
            return
        nodes[current_id] = Node(
            id=current_id,
            title=current_title,
            layer=layer_of(current_id),
            status=current_status,
            anchors=current_anchors,
            a_infinity=current_a_inf,
            summary=current_claim[:280],
            content="\n".join(current_content).strip(),
        )
        current_id = None
        current_title = ""
        current_status = Status.STUB
        current_anchors = 0
        current_a_inf = False
        current_claim = ""
        current_content = []

    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()

        # Skip section comments
        if stripped.startswith("%"):
            i += 1
            continue

        m = NODE_HEADER_RE.match(stripped)
        if m:
            flush()
            current_id = m.group(1)
            current_title = (m.group(2) or "").strip()
            i += 1
            continue

        if current_id is not None:
            sm = STATUS_RE.match(stripped)
            if sm:
                current_status = parse_status(sm.group(1))
                current_anchors, current_a_inf = parse_anchors(sm.group(2))
                i += 1
                continue
            cm = CLAIM_RE.match(stripped)
            if cm:
                current_claim = cm.group(1).strip()

        # Edge line works regardless of node context (block-level edges live
        # both inside node bodies and between blocks)
        em = EDGE_RE.match(stripped)
        if em and "-->" in stripped:
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
            if current_id is not None:
                current_content.append(stripped)
            i += 1
            continue

        if current_id is not None:
            current_content.append(line)

        i += 1

    flush()

    # Synthesize Node entries for any edge endpoints missing from blocks
    for e in edges:
        for nid in (e.source, e.target):
            if nid not in nodes:
                nodes[nid] = Node(
                    id=nid,
                    layer=layer_of(nid),
                    status=Status.STUB,
                    summary="(referenced in edges, no block content)",
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
                summary: $summary, content: $content,
                z_struct: $zs, z_therm: $zt, z_hidden: $zh, level: $lvl
            })
            """,
            {
                "id": n.id, "title": n.title, "layer": n.layer.value,
                "status": n.status.value, "anchors": n.anchors,
                "a_inf": n.a_infinity, "summary": n.summary,
                "content": n.content, "zs": n.z_struct, "zt": n.z_therm,
                "zh": n.z_hidden, "lvl": n.level,
            },
        )

    # Dedup edges (same source/target/label can appear repeatedly in source file)
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


def main() -> None:
    text = GRAPH_FILE.read_text(encoding="utf-8")
    nodes, edges = parse_graph(text)
    print(f"parsed: {len(nodes)} nodes, {len(edges)} edges")

    by_status: dict[str, int] = {}
    by_layer: dict[str, int] = {}
    for n in nodes.values():
        by_status[n.status.value] = by_status.get(n.status.value, 0) + 1
        by_layer[n.layer.value] = by_layer.get(n.layer.value, 0) + 1
    print("status:", by_status)
    print("layer :", by_layer)

    write_to_kuzu(nodes, edges)
    print(f"wrote → {DB_PATH}")


if __name__ == "__main__":
    main()
