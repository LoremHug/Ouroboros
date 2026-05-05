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
  rp_gate           — runtime structural validator (R1-R4 + grammar + domain traps)
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
from mcp_server import rp_gate as _rp_gate  # noqa: E402
from mcp_server import motifs as _motifs  # noqa: E402

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

    Resolves aliases automatically: if node_id is an alias of a canonical
    node (e.g., N068 → N067), returns the canonical node with a note.
    Single call replaces several Cypher queries that would otherwise need
    Bash heredocs. Returns JSON.
    """
    conn = _conn()
    # Try direct lookup first
    res = conn.execute(
        """
        MATCH (n:Node {id: $id})
        RETURN n.id, n.title, n.layer, n.status, n.anchors, n.a_infinity,
               n.summary, n.why_status, n.not_misinterpretations, n.content,
               n.z_struct, n.z_therm, n.z_hidden, n.level, n.is_placeholder, n.aliases
        """,
        {"id": node_id},
    )
    resolved_from = None
    if not res.has_next():
        # Try alias resolution: search nodes whose aliases include node_id
        res2 = conn.execute(
            "MATCH (n:Node) WHERE n.aliases CONTAINS $id RETURN n.id LIMIT 1",
            {"id": f'"{node_id}"'},
        )
        if not res2.has_next():
            return json.dumps({"error": f"node {node_id} not found (no canonical, no alias match)"}, ensure_ascii=False)
        canonical = res2.get_next()[0]
        resolved_from = node_id
        res = conn.execute(
            """
            MATCH (n:Node {id: $id})
            RETURN n.id, n.title, n.layer, n.status, n.anchors, n.a_infinity,
                   n.summary, n.why_status, n.not_misinterpretations, n.content,
                   n.z_struct, n.z_therm, n.z_hidden, n.level, n.is_placeholder, n.aliases
            """,
            {"id": canonical},
        )
    row = res.get_next()
    try:
        aliases = json.loads(row[15] or "[]")
    except Exception:
        aliases = []
    node = {
        "id": row[0], "title": row[1], "layer": row[2], "status": row[3],
        "anchors": row[4], "a_infinity": row[5],
        "summary": row[6], "why_status": row[7],
        "not_misinterpretations": row[8], "content": row[9],
        "z_struct": row[10], "z_therm": row[11], "z_hidden": row[12],
        "level": row[13], "is_placeholder": row[14],
        "aliases": aliases,
    }
    if resolved_from:
        node["resolved_from_alias"] = resolved_from

    canonical_id = node["id"]
    out_edges = []
    res = conn.execute(
        """
        MATCH (a:Node {id: $id})-[e:Edge]->(b:Node)
        RETURN b.id, e.label, e.edge_status, e.justification, e.why_forced
        """,
        {"id": canonical_id},
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
        {"id": canonical_id},
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
            {"id": canonical_id},
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


# ────────────────────────────────────────────────────── ANALYSIS TOOLS

@mcp.tool()
def find_path(source: str, target: str, max_hops: int = 6, directed: bool = True) -> str:
    """Find the shortest path between two nodes through Edge relationships.

    directed=True: follow edges in their natural source→target direction.
    directed=False: treat edges as undirected.

    Returns the shortest path as an ordered list of {id, title, layer} plus
    the edge labels traversed. If no path within max_hops, returns empty.
    Uses Kuzu's variable-length path matching.
    """
    conn = _conn()
    arrow = "->" if directed else "-"
    cypher = f"""
        MATCH p = (a:Node {{id: $src}})-[:Edge*1..{max_hops}]{arrow}(b:Node {{id: $tgt}})
        RETURN nodes(p), rels(p)
        ORDER BY length(p)
        LIMIT 1
    """
    try:
        res = conn.execute(cypher, {"src": source, "tgt": target})
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)
    if not res.has_next():
        return json.dumps({"path": [], "hops": 0,
                           "note": f"no path within {max_hops} hops"},
                          ensure_ascii=False)
    row = res.get_next()
    nodes_data, rels_data = row[0], row[1]
    path_nodes = [{"id": n.get("id"), "title": n.get("title"),
                   "layer": n.get("layer")} for n in nodes_data]
    edge_labels = [r.get("label") for r in rels_data]
    return json.dumps({
        "path": path_nodes, "edge_labels": edge_labels,
        "hops": len(edge_labels),
    }, ensure_ascii=False, default=str)


@mcp.tool()
def common_ancestors(node_a: str, node_b: str, max_hops: int = 4) -> str:
    """Find nodes that are ancestors (incoming-direction sources) of BOTH
    node_a and node_b within max_hops. These are shared structural grounds
    — useful for verifying that two nodes share a forced derivation path
    or for finding the closest common foundation in the graph.

    Returns sorted by combined path length (shorter = closer ancestor).
    """
    conn = _conn()
    cypher = f"""
        MATCH (anc:Node)-[:Edge*1..{max_hops}]->(a:Node {{id: $a}}),
              (anc)-[:Edge*1..{max_hops}]->(b:Node {{id: $b}})
        WHERE anc.id <> $a AND anc.id <> $b
        RETURN DISTINCT anc.id, anc.title, anc.layer
        LIMIT 50
    """
    try:
        res = conn.execute(cypher, {"a": node_a, "b": node_b})
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)
    out = []
    for r in _rows(res):
        out.append({"id": r[0], "title": r[1], "layer": r[2]})
    return json.dumps({"ancestors": out, "count": len(out)},
                      ensure_ascii=False, default=str)


@mcp.tool()
def node_centrality(top_k: int = 25) -> str:
    """Rank nodes by degree centrality (in + out edges). Identifies the
    structural hubs of the manifold.

    Returns top_k nodes with in-degree, out-degree, total, plus layer/status.
    Useful for prioritising bespoke justification work, Z-vector assignment,
    and stub-resolution targets.
    """
    conn = _conn()
    res = conn.execute(
        """
        MATCH (n:Node)
        OPTIONAL MATCH (n)-[out:Edge]->()
        WITH n, count(out) AS out_deg
        OPTIONAL MATCH ()-[in_edge:Edge]->(n)
        WITH n, out_deg, count(in_edge) AS in_deg
        RETURN n.id, n.title, n.layer, n.status, in_deg, out_deg,
               in_deg + out_deg AS total
        ORDER BY total DESC
        LIMIT $k
        """,
        {"k": top_k},
    )
    out = []
    for r in _rows(res):
        out.append({
            "id": r[0], "title": r[1], "layer": r[2], "status": r[3],
            "in_degree": r[4], "out_degree": r[5], "total_degree": r[6],
        })
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


# ────────────────────────────────────────────────────── RP GATE RUNTIME

@mcp.tool()
def rp_gate(text: str, format: str = "json") -> str:
    """Run text through the RP gate: detect R1-R4 traps, grammar trap,
    domain carving, map/territory reification. Estimate Shannon overhead
    (interpretive plaster proxy).

    R1 = process reified as object (N_TopologyProcessIdentity root)
    R2 = external evaluation position fabricated (N112 root)
    R3 = free parameter masquerading as forced (N_InversiveTheory root)
    R4 = state-change agency claim (N187 root)
    grammar = S-V-O on processes/totalities (N_GrammarTrap root)
    domain = BPI taxonomy reified as ontological partition (N_DomainsAsBPICarvings)
    map_territory = Korzybski distinction reified (N_MapTerritoryObserverIdentity)

    Args:
        text: input text to validate
        format: "json" (structured) or "report" (markdown for humans)

    Returns:
        json: full structured report with flags, severity, framework_node refs
        report: human-readable markdown summary
    """
    if format == "report":
        return _rp_gate.format_report(text)
    return json.dumps(_rp_gate.summarise(text), ensure_ascii=False, default=str)


@mcp.tool()
def rp_gate_twin_check(
    node_id: str = "",
    neighbors_csv: str = "",
    jaccard_high: float = 0.7,
    jaccard_med: float = 0.5,
    min_shared: int = 3,
    format: str = "json",
) -> str:
    """Structural twin detector — round 38 M3 motif application.

    Detects whether a candidate node has identical or near-identical
    neighbour set to existing graph nodes (Jaccard >= jaccard_med).
    Twins can be (a) genuine carrier-level identity, (b) duplication
    candidate, (c) family-cousin in K_n motif, (d) low-overlap noise.

    Two modes:
      1. Existing-node mode: pass node_id of an existing graph node to
         lint it against the rest of the graph.
      2. Candidate-neighbours mode: pass neighbors_csv = "id1,id2,..."
         of a hypothetical new node's connections; reports potential
         twins before insertion.

    Severity:
      HIGH (Jaccard >= jaccard_high): MERGE_CANDIDATE / CARRIER_DUPLICATE
      MEDIUM (>= jaccard_med):         FAMILY_COUSIN (M2/M5 cousin pattern)
      LOW:                              LOW_OVERLAP (incidental)

    Returns json (structured) or report (markdown).
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

    direct_edge_labels: dict[str, list[str]] = {}
    if node_id:
        if node_id not in nbrs:
            err = {"error": f"node_id '{node_id}' not found in graph"}
            return json.dumps(err) if format == "json" else f"# Error\n\n{err['error']}"
        candidate_neighbors = nbrs[node_id]
        candidate_id = node_id
        # Collect edge labels between candidate_id and each direct neighbour
        for nbr in candidate_neighbors:
            res = conn.execute(
                "MATCH (a:Node {id: $a})-[e:Edge]-(b:Node {id: $b}) "
                "RETURN e.label",
                {"a": candidate_id, "b": nbr},
            )
            labels = [r[0] for r in _rows(res) if r[0]]
            if labels:
                direct_edge_labels[nbr] = labels
    elif neighbors_csv:
        candidate_neighbors = {
            x.strip() for x in neighbors_csv.split(",") if x.strip()
        }
        unknown = candidate_neighbors - set(ids)
        if unknown:
            err = {"error": f"unknown neighbours: {sorted(unknown)}"}
            return json.dumps(err) if format == "json" else f"# Error\n\n{err['error']}"
        candidate_id = None
    else:
        err = {"error": "must provide either node_id or neighbors_csv"}
        return json.dumps(err) if format == "json" else f"# Error\n\n{err['error']}"

    flags = _rp_gate.detect_structural_twins(
        candidate_neighbors=candidate_neighbors,
        existing_node_neighbors=nbrs,
        candidate_id=candidate_id,
        jaccard_high=jaccard_high,
        jaccard_med=jaccard_med,
        min_shared=min_shared,
        direct_edge_labels=direct_edge_labels or None,
    )
    if format == "report":
        return _rp_gate.format_twin_report(flags, candidate_id=candidate_id)
    summary = _rp_gate.summarise_twins(flags)
    summary["candidate_id"] = candidate_id
    summary["candidate_neighbor_count"] = len(candidate_neighbors)
    return json.dumps(summary, ensure_ascii=False, default=str)


# ────────────────────────────────────────────────────── MOTIF DETECTOR

# N_FrameworkCore tier-1 + tier-2/3/4/5 (substrate-invariant principles).
# These get treated as "principle stratum" candidates when partitioning
# K_n cliques per round 39 finding.
_CORE_PRINCIPLE_IDS = frozenset({
    # Tier 1 (Foundational)
    "DEF", "N_Invariants", "N_Triangulation", "N_NoSeparatePieces",
    "N_InversiveTheory",
    # Tier 2 (Observer-structure)
    "N112", "N_TopologyProcessIdentity", "N_ForcedId",
    # Tier 3 (Description/paradigm)
    "N_GrammarTrap", "N_OntologyParadigmGrammarBound",
    "N_DomainsAsBPICarvings", "N_MapTerritoryObserverIdentity",
    # Tier 4 (Measurement bridge)
    "N_Shannon",
    # Tier 5 (Observer-substrate)
    "N_BPIEngagement",
    # Cross-cutting principles that participate in stratification
    "N370", "N_ZGaugeDecomposition", "N_FrameworkCore",
})


@mcp.tool()
def detect_motifs(
    z_triangle_hub_threshold: int = 25,
    z_triangle_max: int = 50,
    clique_min_size: int = 5,
    clique_min_cousins: int = 3,
    twin_jaccard: float = 1.0,
    twin_min_shared: int = 3,
    extra_principle_ids_csv: str = "",
    format: str = "report",
) -> str:
    """Run all structural-motif detectors over the graph.

    Detects and tags:
      M1 — Z-triangles (parent → 3 pairwise-connected children),
           hub-filtered; per N_StructuralMotif_ZTriangle (round 37).
      M2 — K_n family-clique (1 anchor + n cousins), per round 38.
      M5 — Principle-stratification K_{p+n} (>= 2 anchors + cousins),
           per round 39.
      M3 — Structural twin pairs (Jaccard >= twin_jaccard),
           per N_StructuralMotif_StructuralTwins.
      M4 — Articulation points; 2-vertex-connectivity audit per
           N_GraphProperty_2VertexConnectivity.

    The principle-vs-cousin partition for M2/M5 uses N_FrameworkCore
    member IDs as the principle stratum. extra_principle_ids_csv lets
    caller add domain-specific principles temporarily.

    Args:
      z_triangle_hub_threshold: nodes with degree >= this excluded
        from Z-triangle CHILD positions (still allowed as parents).
      z_triangle_max: cap on Z-triangles returned (graph has many).
      clique_min_size: minimum clique size to consider for M2/M5.
      clique_min_cousins: minimum cousin count (cousins = clique
        members not in principle stratum).
      twin_jaccard: Jaccard threshold for twin pair detection.
      twin_min_shared: minimum shared neighbours.
      extra_principle_ids_csv: optional comma-separated extra IDs
        to treat as principles for this run only.
      format: "report" (markdown) or "json" (structured).
    """
    conn = _conn()
    res = conn.execute(
        "MATCH (a:Node)-[:Edge]-(b:Node) WHERE a.id < b.id "
        "RETURN DISTINCT a.id, b.id"
    )
    edge_pairs = [(r[0], r[1]) for r in _rows(res)]

    extras = {
        x.strip() for x in extra_principle_ids_csv.split(",") if x.strip()
    }
    principle_ids = set(_CORE_PRINCIPLE_IDS) | extras

    report = _motifs.run_all_detectors(
        edge_pairs=edge_pairs,
        core_principle_ids=principle_ids,
        z_triangle_hub_threshold=z_triangle_hub_threshold,
        z_triangle_max=z_triangle_max,
        clique_min_size=clique_min_size,
        clique_min_cousins=clique_min_cousins,
        twin_jaccard=twin_jaccard,
        twin_min_shared=twin_min_shared,
    )
    if format == "report":
        return _motifs.format_motif_report(report)
    return json.dumps(report, ensure_ascii=False, default=str)


@mcp.tool()
def rp_gate_audit_node(node_id: str, format: str = "json") -> str:
    """Run rp_gate text scan on a graph node's content fields.

    Concatenates summary + content + why_status + not_misinterpretations
    and runs the trap detector. Useful for self-audit of framework
    nodes — does the framework's own description of itself trip its
    own gate?

    Returns json or markdown report.
    """
    conn = _conn()
    res = conn.execute(
        "MATCH (n:Node {id: $id}) "
        "RETURN n.summary, n.content, n.why_status, n.not_misinterpretations",
        {"id": node_id},
    )
    if not res.has_next():
        err = {"error": f"node '{node_id}' not found"}
        return json.dumps(err) if format == "json" else f"# Error\n\n{err['error']}"
    s, c, w, nm = res.get_next()
    parts = [p for p in [s, c, w, nm] if p]
    if not parts:
        msg = f"Node `{node_id}` has no text fields to audit."
        return json.dumps({"warning": msg}) if format == "json" else msg
    text = "\n\n".join(parts)
    if format == "report":
        return _rp_gate.format_report(text)
    summary = _rp_gate.summarise(text)
    summary["node_id"] = node_id
    return json.dumps(summary, ensure_ascii=False, default=str)


@mcp.tool()
def rp_gate_motif_lint(
    node_id: str,
    proposed_neighbors_csv: str = "",
    extra_principle_ids_csv: str = "",
    twin_jaccard: float = 0.7,
    twin_min_shared: int = 3,
    format: str = "report",
) -> str:
    """Motif-aware structural lint for a candidate node addition or
    existing node review.

    Combines round-40 twin detector + round-41 motif inventory into a
    single structural-lint call. Reports what motifs the candidate
    extends (joins existing K_n / Z-triangle / etc.), what new motifs
    it creates, twin/duplication warnings, topology delta (β₁, ΔE,
    Δtriangles), and articulation concerns.

    Two modes:
      1. Hypothetical addition: pass node_id of NEW node + proposed_
         neighbors_csv. Report includes before/after delta.
      2. Existing-node review: pass node_id of existing graph node;
         neighbours are looked up from graph; reports current motif
         participation.

    Returns json (structured) or report (markdown).
    """
    conn = _conn()
    res = conn.execute(
        "MATCH (a:Node)-[:Edge]-(b:Node) WHERE a.id < b.id "
        "RETURN DISTINCT a.id, b.id"
    )
    edge_pairs = [(r[0], r[1]) for r in _rows(res)]
    adj = _motifs._build_adjacency(edge_pairs)

    # Statuses + layers (used elsewhere; not needed for lint core)
    statuses: dict[str, str] = {}
    layers: dict[str, str] = {}
    res = conn.execute("MATCH (n:Node) RETURN n.id, n.status, n.layer")
    for r in _rows(res):
        statuses[r[0]] = r[1] or ""
        layers[r[0]] = r[2] or "unknown"

    extras = {x.strip() for x in extra_principle_ids_csv.split(",") if x.strip()}
    principle_ids = set(_CORE_PRINCIPLE_IDS) | extras

    if node_id in adj and not proposed_neighbors_csv:
        new_neighbors = adj[node_id]
    elif proposed_neighbors_csv:
        new_neighbors = {
            x.strip() for x in proposed_neighbors_csv.split(",") if x.strip()
        }
        unknown = new_neighbors - set(adj.keys())
        if unknown:
            err = {"error": f"unknown neighbours: {sorted(unknown)}"}
            return json.dumps(err) if format == "json" else f"# Error\n\n{err['error']}"
    else:
        err = {
            "error": (
                "must provide either node_id of existing node, or "
                "node_id + proposed_neighbors_csv for hypothetical addition"
            )
        }
        return json.dumps(err) if format == "json" else f"# Error\n\n{err['error']}"

    report = _motifs.lint_node_addition(
        adj=adj,
        new_id=node_id,
        new_neighbors=new_neighbors,
        core_principle_ids=principle_ids,
        statuses=statuses,
        layers=layers,
        twin_jaccard=twin_jaccard,
        twin_min_shared=twin_min_shared,
    )
    if format == "report":
        return _motifs.format_lint_report(report)
    return json.dumps(report, ensure_ascii=False, default=str)


# ────────────────────────────────────────────────────── ENTRY

def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
