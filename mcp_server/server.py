"""Ouroboros MCP server — direct tool access to the Kuzu manifold graph.

Tools exposed:
  query             — raw Cypher (read-only by convention; use *_node/*_edge for writes)
  get_node          — node details + outgoing/incoming edges + linked .tex sections
  get_section       — full body of a .tex section by label
  add_or_update_node — upsert via additions.yaml + DB
  add_or_update_edge — upsert via additions.yaml + DB
  list_stubs        — STUB-status nodes
  find_jaccard_pairs — common-neighbor candidates for missing edges
  graph_stats       — counts by status / layer / placeholders / unjustified edges
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mcp.server.fastmcp import FastMCP  # noqa: E402

from schema import Status, Layer, EdgeStatus, layer_of  # noqa: E402
from scripts.db import connect  # noqa: E402
from scripts import additions as additions_io  # noqa: E402

mcp = FastMCP("ouroboros")


def _conn():
    _, conn = connect()
    return conn


def _rows(res) -> list[list]:
    out = []
    while res.has_next():
        out.append(list(res.get_next()))
    return out


# ────────────────────────────────────────────────────── READ TOOLS

@mcp.tool()
def query(cypher: str) -> str:
    """Run a Cypher query against the Kuzu manifold DB.

    Use for arbitrary structural queries. Returns columns and rows as JSON.
    Read-only by convention — use add_or_update_node / add_or_update_edge
    for writes so additions.yaml stays the source of truth.
    """
    conn = _conn()
    try:
        res = conn.execute(cypher)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)
    cols = res.get_column_names()
    rows = _rows(res)
    return json.dumps({"columns": cols, "rows": rows, "n": len(rows)},
                      ensure_ascii=False, default=str)


@mcp.tool()
def get_node(node_id: str) -> str:
    """Fetch full node details: all fields + outgoing/incoming edges +
    linked .tex sections.

    Single call replaces several Cypher queries that would otherwise need
    Bash heredocs. Returns JSON.
    """
    conn = _conn()
    res = conn.execute(
        """
        MATCH (n:Node {id: $id})
        RETURN n.id, n.title, n.layer, n.status, n.anchors, n.a_infinity,
               n.summary, n.why_status, n.not_misinterpretations, n.content,
               n.z_struct, n.z_therm, n.z_hidden, n.level, n.is_placeholder
        """,
        {"id": node_id},
    )
    if not res.has_next():
        return json.dumps({"error": f"node {node_id} not found"}, ensure_ascii=False)
    row = res.get_next()
    node = {
        "id": row[0], "title": row[1], "layer": row[2], "status": row[3],
        "anchors": row[4], "a_infinity": row[5],
        "summary": row[6], "why_status": row[7],
        "not_misinterpretations": row[8], "content": row[9],
        "z_struct": row[10], "z_therm": row[11], "z_hidden": row[12],
        "level": row[13], "is_placeholder": row[14],
    }

    out_edges = []
    res = conn.execute(
        """
        MATCH (a:Node {id: $id})-[e:Edge]->(b:Node)
        RETURN b.id, e.label, e.edge_status, e.justification, e.why_forced
        """,
        {"id": node_id},
    )
    for r in _rows(res):
        out_edges.append({
            "target": r[0], "label": r[1], "status": r[2],
            "justification": r[3], "why_forced": r[4],
        })

    in_edges = []
    res = conn.execute(
        """
        MATCH (a:Node)-[e:Edge]->(b:Node {id: $id})
        RETURN a.id, e.label, e.edge_status, e.justification, e.why_forced
        """,
        {"id": node_id},
    )
    for r in _rows(res):
        in_edges.append({
            "source": r[0], "label": r[1], "status": r[2],
            "justification": r[3], "why_forced": r[4],
        })

    sections = []
    try:
        res = conn.execute(
            """
            MATCH (n:Node {id: $id})-[:DESCRIBED_BY]->(s:Section)
            RETURN s.label, s.title, s.kind
            """,
            {"id": node_id},
        )
        for r in _rows(res):
            sections.append({"label": r[0], "title": r[1], "kind": r[2]})
    except Exception:
        pass  # Section table may not exist

    return json.dumps({
        "node": node, "outgoing": out_edges, "incoming": in_edges,
        "sections": sections,
    }, ensure_ascii=False, default=str)


@mcp.tool()
def get_section(label: str) -> str:
    """Fetch full body of a .tex section by label (e.g. 'sec:ergodicity').

    Use to read the canonical text behind a node. Returns JSON.
    """
    conn = _conn()
    try:
        res = conn.execute(
            "MATCH (s:Section {label: $l}) RETURN s.label, s.title, s.kind, s.body",
            {"l": label},
        )
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)
    if not res.has_next():
        return json.dumps({"error": f"section {label} not found"}, ensure_ascii=False)
    row = res.get_next()

    linked = []
    res = conn.execute(
        """
        MATCH (n:Node)-[:DESCRIBED_BY]->(s:Section {label: $l})
        RETURN n.id, n.title
        """,
        {"l": label},
    )
    for r in _rows(res):
        linked.append({"id": r[0], "title": r[1]})

    return json.dumps({
        "label": row[0], "title": row[1], "kind": row[2], "body": row[3],
        "linked_nodes": linked,
    }, ensure_ascii=False, default=str)


@mcp.tool()
def list_stubs() -> str:
    """List all STUB-status nodes (no CLAIM body) and placeholder-flagged
    nodes ('Stub — Referenced in Edge Lists' entries).

    Returns JSON with degree to help prioritise cleanup.
    """
    conn = _conn()
    res = conn.execute(
        """
        MATCH (n:Node)
        WHERE n.status = 'STUB' OR n.is_placeholder = true
        OPTIONAL MATCH (n)-[e:Edge]-()
        WITH n, count(e) AS deg
        RETURN n.id, n.layer, n.status, n.is_placeholder, deg
        ORDER BY deg DESC, n.id
        """
    )
    rows = []
    for r in _rows(res):
        rows.append({
            "id": r[0], "layer": r[1], "status": r[2],
            "is_placeholder": r[3], "degree": r[4],
        })
    return json.dumps(rows, ensure_ascii=False, default=str)


@mcp.tool()
def find_jaccard_pairs(threshold: float = 0.4, min_shared: int = 2) -> str:
    """Find pairs of nodes with high Jaccard similarity in their neighbour
    sets but no direct edge — candidates for missing forced structure.

    Returns top 40 pairs sorted by Jaccard descending.
    """
    conn = _conn()
    res = conn.execute("MATCH (n:Node) RETURN n.id ORDER BY n.id")
    ids = [r[0] for r in _rows(res)]
    nbrs: dict[str, set[str]] = {}
    for nid in ids:
        res = conn.execute(
            "MATCH (a:Node {id: $id})-[:Edge]-(b:Node) RETURN DISTINCT b.id",
            {"id": nid},
        )
        nbrs[nid] = {r[0] for r in _rows(res)}

    pairs = []
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            na, nb = nbrs[a], nbrs[b]
            inter = na & nb
            if len(inter) < min_shared:
                continue
            j = len(inter) / len(na | nb)
            if j < threshold:
                continue
            res = conn.execute(
                "MATCH (a:Node {id: $a})-[:Edge]-(b:Node {id: $b}) RETURN count(*) > 0",
                {"a": a, "b": b},
            )
            if res.get_next()[0]:
                continue
            pairs.append({"a": a, "b": b, "jaccard": round(j, 3),
                          "shared": sorted(inter)})
    pairs.sort(key=lambda p: -p["jaccard"])
    return json.dumps(pairs[:40], ensure_ascii=False, default=str)


@mcp.tool()
def graph_stats() -> str:
    """Return counts: total nodes, total edges, by-status, by-layer,
    placeholders, edges with empty why_forced/justification.
    """
    conn = _conn()
    out: dict[str, Any] = {}
    res = conn.execute("MATCH (n:Node) RETURN count(n)")
    out["nodes"] = res.get_next()[0]
    res = conn.execute("MATCH ()-[e:Edge]->() RETURN count(e)")
    out["edges"] = res.get_next()[0]

    by_status = {}
    res = conn.execute("MATCH (n:Node) RETURN n.status, count(n)")
    for r in _rows(res):
        by_status[r[0]] = r[1]
    out["by_status"] = by_status

    by_layer = {}
    res = conn.execute("MATCH (n:Node) RETURN n.layer, count(n)")
    for r in _rows(res):
        by_layer[r[0]] = r[1]
    out["by_layer"] = by_layer

    res = conn.execute("MATCH (n:Node) WHERE n.is_placeholder = true RETURN count(n)")
    out["placeholders"] = res.get_next()[0]

    res = conn.execute(
        "MATCH ()-[e:Edge]->() WHERE e.why_forced = '' AND e.justification = '' RETURN count(e)"
    )
    out["unjustified_edges"] = res.get_next()[0]

    res = conn.execute("MATCH (s:Section) RETURN count(s)")
    try:
        out["sections"] = res.get_next()[0]
        res = conn.execute(
            "MATCH (s:Section) WHERE NOT EXISTS { MATCH (:Node)-[:DESCRIBED_BY]->(s) } RETURN count(s)"
        )
        out["unlinked_sections"] = res.get_next()[0]
    except Exception:
        pass

    return json.dumps(out, ensure_ascii=False, default=str)


# ────────────────────────────────────────────────────── WRITE TOOLS

@mcp.tool()
def add_or_update_node(
    id: str,
    title: str | None = None,
    layer: str | None = None,
    status: str | None = None,
    anchors: int | None = None,
    a_infinity: bool | None = None,
    summary: str | None = None,
    why_status: str | None = None,
    not_misinterpretations: str | None = None,
    content: str | None = None,
    z_struct: float | None = None,
    z_therm: float | None = None,
    z_hidden: float | None = None,
    level: int | None = None,
    is_placeholder: bool | None = None,
) -> str:
    """Upsert a node into additions.yaml AND mirror to live Kuzu DB.

    Persistence: additions.yaml is committed source-of-truth; DB is
    derived. Only fields you pass are updated; missing fields keep their
    current values.

    layer values: core, structure, epistemics, observers, physics, comms, numeric
    status values: DEMONSTRATED, STRONG, CONDITIONAL, OPERATIONAL, STUB
    """
    field_map = {
        "title": title, "layer": layer, "status": status,
        "anchors": anchors, "a_infinity": a_infinity,
        "summary": summary, "why_status": why_status,
        "not_misinterpretations": not_misinterpretations,
        "content": content,
        "z_struct": z_struct, "z_therm": z_therm, "z_hidden": z_hidden,
        "level": level, "is_placeholder": is_placeholder,
    }
    spec: dict[str, Any] = {"id": id}
    spec.update({k: v for k, v in field_map.items() if v is not None})
    if "layer" not in spec:
        spec["layer"] = layer_of(id).value

    additions_io.upsert_node(spec)

    conn = _conn()
    res = conn.execute("MATCH (n:Node {id: $id}) RETURN count(n)", {"id": id})
    exists = res.get_next()[0] > 0

    if exists:
        sets = []
        params: dict[str, Any] = {"id": id}
        for k, v in field_map.items():
            if v is None:
                continue
            sets.append(f"n.{k} = ${k}")
            params[k] = v
        if sets:
            conn.execute(
                f"MATCH (n:Node {{id: $id}}) SET {', '.join(sets)}",
                params,
            )
            return json.dumps({"action": "updated", "id": id,
                               "fields_changed": list(sets)}, ensure_ascii=False)
        return json.dumps({"action": "no-op", "id": id}, ensure_ascii=False)

    defaults = {
        "title": "", "layer": layer_of(id).value, "status": Status.STUB.value,
        "anchors": 0, "a_infinity": False, "summary": "", "why_status": "",
        "not_misinterpretations": "", "content": "",
        "z_struct": 0.0, "z_therm": 0.0, "z_hidden": 0.0, "level": -1,
        "is_placeholder": False,
    }
    defaults.update({k: v for k, v in field_map.items() if v is not None})
    defaults["id"] = id
    conn.execute(
        """
        CREATE (n:Node {
            id: $id, title: $title, layer: $layer, status: $status,
            anchors: $anchors, a_infinity: $a_infinity,
            summary: $summary, why_status: $why_status,
            not_misinterpretations: $not_misinterpretations,
            content: $content,
            z_struct: $z_struct, z_therm: $z_therm, z_hidden: $z_hidden,
            level: $level, is_placeholder: $is_placeholder
        })
        """,
        defaults,
    )
    return json.dumps({"action": "created", "id": id}, ensure_ascii=False)


@mcp.tool()
def add_or_update_edge(
    source: str,
    target: str,
    label: str,
    edge_status: str = "D",
    justification: str = "",
    why_forced: str = "",
) -> str:
    """Upsert an edge into additions.yaml AND mirror to live Kuzu DB.

    Edges are keyed by (source, target, label). Re-applying with the same
    triple updates justification/why_forced. Both endpoints must exist;
    create them via add_or_update_node first if they don't.

    edge_status: D (DEMONSTRATED) or S (STRONG)
    """
    conn = _conn()
    for nid in (source, target):
        res = conn.execute("MATCH (n:Node {id: $id}) RETURN count(n)", {"id": nid})
        if res.get_next()[0] == 0:
            return json.dumps({
                "error": f"node not found: {nid}",
                "hint": "create it first via add_or_update_node",
            }, ensure_ascii=False)

    if edge_status not in ("D", "S"):
        return json.dumps({"error": "edge_status must be 'D' or 'S'"},
                          ensure_ascii=False)

    spec = {
        "source": source, "target": target, "label": label,
        "edge_status": edge_status,
        "justification": justification, "why_forced": why_forced,
    }
    additions_io.update_edge(spec)

    # Mirror to DB
    conn.execute(
        """
        MATCH (a:Node {id: $src})-[e:Edge]->(b:Node {id: $tgt})
        WHERE e.label = $lbl
        DELETE e
        """,
        {"src": source, "tgt": target, "lbl": label},
    )
    conn.execute(
        """
        MATCH (a:Node {id: $src}), (b:Node {id: $tgt})
        CREATE (a)-[:Edge {
            label: $lbl, edge_status: $st,
            justification: $j, why_forced: $w
        }]->(b)
        """,
        {"src": source, "tgt": target, "lbl": label, "st": edge_status,
         "j": justification, "w": why_forced},
    )
    return json.dumps({
        "action": "upserted",
        "edge": f"{source} → {target} : {label} [{edge_status}]",
        "note": "additions.yaml updated — commit it",
    }, ensure_ascii=False)


# ────────────────────────────────────────────────────── ENTRY

def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
