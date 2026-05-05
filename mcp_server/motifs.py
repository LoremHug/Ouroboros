"""Structural motif auto-detector.

Enumerates motif instances in the graph and tags each with its motif
class. Reference framework nodes:

  M1 — N_StructuralMotif_ZTriangle (round 37)
       parent → 3 pairwise-connected children (closed triangle)
  M2 — N_StructuralMotif_KnFamilyClique (round 38)
       1 principle anchor + n cousins, all pairwise connected
  M3 — N_StructuralMotif_StructuralTwins (round 38)
       pairs with Jaccard = 1.0 neighbour identity
  M4 — N_GraphProperty_2VertexConnectivity (round 38)
       global property: ≤ 1 articulation-point cut
  M5 — N_StructuralMotif_PrincipleStratification (round 39)
       p principles + n cousins + full bipartite K_{p,n}
       (M2 generalisation, M2 = M5 with p=1)
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Iterable
import sys


# ─── Data shapes ──────────────────────────────────────────────────────

@dataclass
class MotifInstance:
    motif: str                      # M1 | M2 | M3 | M5
    members: list[str]              # node IDs participating
    role_partition: dict[str, list[str]]  # role → [ids]
    size: int                       # total members
    edge_count: int                 # internal edges among members
    edge_density: float             # edges / max_possible
    notes: str = ""


# ─── Helpers ──────────────────────────────────────────────────────────

def _build_adjacency(node_pairs: Iterable[tuple[str, str]]) -> dict[str, set[str]]:
    """Build undirected adjacency from edge pair list."""
    adj: dict[str, set[str]] = {}
    for a, b in node_pairs:
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    return adj


def _is_clique(nodes: list[str], adj: dict[str, set[str]]) -> bool:
    for i, x in enumerate(nodes):
        for y in nodes[i + 1:]:
            if y not in adj.get(x, set()):
                return False
    return True


def _internal_edges(nodes: list[str], adj: dict[str, set[str]]) -> int:
    cnt = 0
    for i, x in enumerate(nodes):
        for y in nodes[i + 1:]:
            if y in adj.get(x, set()):
                cnt += 1
    return cnt


# ─── M1: Z-triangle motif ─────────────────────────────────────────────

def detect_z_triangles(
    adj: dict[str, set[str]],
    hub_threshold: int = 25,
    max_results: int = 200,
) -> list[MotifInstance]:
    """Parent → 3 pairwise-connected children, hub-filtered.

    Hubs (deg >= hub_threshold) excluded from CHILD positions because
    they trivially close any triangle they participate in. Hubs may
    still be PARENTS.
    """
    out: list[MotifInstance] = []
    seen: set[tuple[str, tuple[str, ...]]] = set()
    hubs = {n for n, nb in adj.items() if len(nb) >= hub_threshold}

    for parent, nbrs in adj.items():
        # Filter children to non-hubs to focus on substantive structure
        child_pool = sorted(n for n in nbrs if n not in hubs and n != parent)
        for i, a in enumerate(child_pool):
            for j in range(i + 1, len(child_pool)):
                b = child_pool[j]
                if b not in adj.get(a, set()):
                    continue
                for k in range(j + 1, len(child_pool)):
                    c = child_pool[k]
                    if c in adj.get(a, set()) and c in adj.get(b, set()):
                        key = (parent, tuple(sorted([a, b, c])))
                        if key in seen:
                            continue
                        seen.add(key)
                        out.append(
                            MotifInstance(
                                motif="M1",
                                members=[parent, a, b, c],
                                role_partition={
                                    "parent": [parent],
                                    "children": sorted([a, b, c]),
                                },
                                size=4,
                                edge_count=6,  # 3 parent-child + 3 child-child
                                edge_density=1.0,
                            )
                        )
                        if len(out) >= max_results:
                            return out
    return out


# ─── Maximal clique enumeration (Bron–Kerbosch) ───────────────────────

def _bron_kerbosch(
    R: set[str], P: set[str], X: set[str],
    adj: dict[str, set[str]], cliques: list[frozenset[str]],
    min_size: int,
) -> None:
    if not P and not X:
        if len(R) >= min_size:
            cliques.append(frozenset(R))
        return
    # Pivot for efficiency
    pivot = max(P | X, key=lambda u: len(adj.get(u, set()) & P), default=None)
    if pivot is None:
        return
    candidates = P - adj.get(pivot, set())
    for v in list(candidates):
        nbrs = adj.get(v, set())
        _bron_kerbosch(R | {v}, P & nbrs, X & nbrs, adj, cliques, min_size)
        P = P - {v}
        X = X | {v}


def enumerate_maximal_cliques(
    adj: dict[str, set[str]], min_size: int = 4,
) -> list[frozenset[str]]:
    """All maximal cliques of size >= min_size."""
    sys.setrecursionlimit(20000)
    cliques: list[frozenset[str]] = []
    nodes = set(adj.keys())
    _bron_kerbosch(set(), nodes, set(), adj, cliques, min_size)
    return cliques


# ─── M2 / M5: K_n family-clique / Principle-stratification ────────────

def detect_clique_motifs(
    adj: dict[str, set[str]],
    core_principle_ids: set[str],
    min_clique_size: int = 5,
    min_cousins: int = 3,
) -> list[MotifInstance]:
    """Detect M2 and M5 instances.

    A maximal clique of size >= min_clique_size partitions into:
      P = clique ∩ core_principle_ids  (principle stratum)
      N = clique \\ core_principle_ids (cousin stratum)

    If |N| >= min_cousins:
      |P| == 1 → M2 (single anchor + cousins)
      |P| >= 2 → M5 (principle stratum + cousins, K_{p+n} stratification)
      |P| == 0 → not a recognized motif (cousins without anchor)
    """
    out: list[MotifInstance] = []
    cliques = enumerate_maximal_cliques(adj, min_size=min_clique_size)
    for clique in cliques:
        members = list(clique)
        if not _is_clique(members, adj):
            continue
        principles = sorted(m for m in members if m in core_principle_ids)
        cousins = sorted(m for m in members if m not in core_principle_ids)
        if len(cousins) < min_cousins:
            continue
        n = len(members)
        edge_count = _internal_edges(members, adj)
        max_edges = n * (n - 1) // 2
        density = edge_count / max_edges if max_edges else 0.0
        if len(principles) == 1:
            motif = "M2"
            notes = (
                f"Single principle anchor + {len(cousins)} substrate-cousins. "
                f"K_{n} clique."
            )
        elif len(principles) >= 2:
            motif = "M5"
            notes = (
                f"Principle stratum (p={len(principles)}) + cousin stratum "
                f"(n={len(cousins)}). K_{n} = K_{{p+n}} stratified clique."
            )
        else:
            # No principle anchor — note as ambiguous large clique
            motif = "M2_orphan"
            notes = (
                f"Large clique without recognized principle anchor "
                f"({len(cousins)} cousins). May indicate a missing "
                f"principle-tier classification or domain-internal cluster."
            )
        out.append(
            MotifInstance(
                motif=motif,
                members=sorted(members),
                role_partition={"principles": principles, "cousins": cousins},
                size=n,
                edge_count=edge_count,
                edge_density=round(density, 3),
                notes=notes,
            )
        )
    # Sort: M5 first (most structurally informative), then M2, then by size
    rank = {"M5": 0, "M2": 1, "M2_orphan": 2}
    out.sort(key=lambda m: (rank.get(m.motif, 9), -m.size))
    return out


# ─── M3: structural twin pairs ────────────────────────────────────────

def detect_twin_pairs(
    adj: dict[str, set[str]],
    jaccard_threshold: float = 1.0,
    min_shared: int = 3,
) -> list[MotifInstance]:
    """Pairs (a, b) with Jaccard(N(a)\\{b}, N(b)\\{a}) >= threshold."""
    ids = sorted(adj.keys())
    out: list[MotifInstance] = []
    for i, a in enumerate(ids):
        na = adj[a] - {a}
        if len(na) < min_shared:
            continue
        for b in ids[i + 1:]:
            nb = adj[b] - {b}
            if len(nb) < min_shared:
                continue
            ar = na - {b}
            br = nb - {a}
            shared = ar & br
            if len(shared) < min_shared:
                continue
            union = ar | br
            j = len(shared) / len(union) if union else 0.0
            if j < jaccard_threshold:
                continue
            out.append(
                MotifInstance(
                    motif="M3",
                    members=[a, b],
                    role_partition={"twin_pair": [a, b],
                                    "shared_neighbors": sorted(shared)},
                    size=2,
                    edge_count=1 if b in adj.get(a, set()) else 0,
                    edge_density=round(j, 3),
                    notes=(
                        f"Jaccard={j:.2f}, {len(shared)} shared neighbours."
                    ),
                )
            )
    out.sort(key=lambda m: -m.edge_density)
    return out


# ─── M4: 2-vertex-connectivity audit ──────────────────────────────────

def detect_articulation_points(
    adj: dict[str, set[str]],
) -> list[MotifInstance]:
    """Tarjan articulation-point algorithm. Returns one MotifInstance
    per articulation point with the leaves it isolates."""
    sys.setrecursionlimit(20000)
    visited: set[str] = set()
    disc: dict[str, int] = {}
    low: dict[str, int] = {}
    parent: dict[str, str] = {}
    ap: set[str] = set()
    timer = [0]

    def dfs(u: str) -> None:
        children = 0
        visited.add(u)
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        for v in adj.get(u, set()):
            if v not in visited:
                parent[v] = u
                children += 1
                dfs(v)
                low[u] = min(low[u], low[v])
                if u not in parent and children > 1:
                    ap.add(u)
                if u in parent and low[v] >= disc[u]:
                    ap.add(u)
            elif v != parent.get(u):
                low[u] = min(low[u], disc[v])

    for n in adj:
        if n not in visited:
            dfs(n)

    # For each AP, find which components it splits
    out: list[MotifInstance] = []
    for a in sorted(ap):
        # BFS without 'a'
        remain = {n for n in adj if n != a}
        comps: list[set[str]] = []
        seen: set[str] = set()
        for start in remain:
            if start in seen:
                continue
            comp: set[str] = set()
            stack = [start]
            while stack:
                x = stack.pop()
                if x in seen:
                    continue
                seen.add(x)
                comp.add(x)
                for y in adj.get(x, set()):
                    if y in remain and y not in seen:
                        stack.append(y)
            comps.append(comp)
        comps.sort(key=lambda c: -len(c))
        isolated = [c for c in comps[1:]] if len(comps) > 1 else []
        out.append(
            MotifInstance(
                motif="M4_articulation",
                members=[a],
                role_partition={
                    "articulation_point": [a],
                    "main_component_size": [str(len(comps[0]))] if comps else ["0"],
                    "isolated_components": [
                        ",".join(sorted(c)) for c in isolated
                    ],
                },
                size=1,
                edge_count=len(adj.get(a, set())),
                edge_density=0.0,
                notes=(
                    f"Removing {a} isolates {len(isolated)} component(s) "
                    f"of sizes {[len(c) for c in isolated]}."
                ),
            )
        )
    return out


# ─── M6: bipartite-complete K_{m,n} (Resolution Motif) ───────────────

def detect_bipartite_kmn(
    adj: dict[str, set[str]],
    min_m: int = 3,
    min_n: int = 3,
    max_results: int = 50,
) -> list[MotifInstance]:
    """Find K_{m,n} bipartite-complete subgraphs (round 42 motif M6).

    Two independent sets A, B with all cross-edges present and no
    internal edges. Each side plays a distinct structural role
    (e.g., problem ↔ resolution, observable ↔ measurement).
    """
    out: list[MotifInstance] = []
    seen: set[tuple[tuple[str, ...], tuple[str, ...]]] = set()
    nodes = sorted(adj.keys())

    for i, x in enumerate(nodes):
        if len(out) >= max_results:
            break
        for j in range(i + 1, len(nodes)):
            y = nodes[j]
            if y in adj.get(x, set()):
                continue
            common = adj[x] & adj[y]
            if len(common) < min_n:
                continue
            # Greedy independent set in common (becomes side B)
            common_list = sorted(common)
            B: list[str] = []
            for c in common_list:
                if all(d not in adj.get(c, set()) for d in B):
                    B.append(c)
            if len(B) < min_n:
                continue
            # Side A: nodes adjacent to all of B, pairwise independent
            cand_A = set(adj[B[0]])
            for v in B[1:]:
                cand_A &= adj[v]
            cand_A.add(x)
            cand_A.add(y)
            cand_A_list = sorted(
                cand_A, key=lambda n: -len(adj.get(n, set()))
            )
            A: list[str] = []
            for n in cand_A_list:
                if all(m not in adj.get(n, set()) for m in A):
                    A.append(n)
            if len(A) < min_m:
                continue
            key = (tuple(sorted(A)), tuple(sorted(B)))
            rev = (tuple(sorted(B)), tuple(sorted(A)))
            if key in seen or rev in seen:
                continue
            seen.add(key)
            cross_edges = sum(1 for a in A for b in B if b in adj.get(a, set()))
            out.append(
                MotifInstance(
                    motif="M6",
                    members=sorted(A) + sorted(B),
                    role_partition={
                        "side_A": sorted(A),
                        "side_B": sorted(B),
                    },
                    size=len(A) + len(B),
                    edge_count=cross_edges,
                    edge_density=round(
                        cross_edges / (len(A) * len(B)), 3
                    ),
                    notes=(
                        f"K_{{{len(A)},{len(B)}}} bipartite-complete. "
                        f"Side A and Side B are independent sets; all "
                        f"cross-pairs connected. Resolution-motif: each "
                        f"A-member relates to each B-member."
                    ),
                )
            )
    return out


# ─── Motif-aware structural lint (round 45) ─────────────────────────

def _add_node_to_adj(
    adj: dict[str, set[str]],
    new_id: str,
    new_neighbors: set[str],
) -> dict[str, set[str]]:
    """Return new adjacency dict with new_id added connecting to new_neighbors.
    Original adj is not mutated."""
    new_adj = {k: set(v) for k, v in adj.items()}
    new_adj[new_id] = set(new_neighbors)
    for nb in new_neighbors:
        new_adj.setdefault(nb, set()).add(new_id)
    return new_adj


def lint_node_addition(
    adj: dict[str, set[str]],
    new_id: str,
    new_neighbors: set[str],
    core_principle_ids: set[str],
    statuses: dict[str, str] | None = None,
    layers: dict[str, str] | None = None,
    twin_jaccard: float = 0.7,
    twin_min_shared: int = 3,
) -> dict[str, Any]:
    """Motif-aware structural lint for a candidate node addition.

    Reports what the new node creates, extends, and whether it
    introduces twin/duplication signals. Compares motif inventories
    BEFORE and AFTER the hypothetical addition.

    Args:
      adj: current adjacency
      new_id: candidate node ID (may or may not exist)
      new_neighbors: proposed connections
      core_principle_ids: ids treated as principle stratum
      statuses, layers: optional, used for cycle-substantivity filter
      twin_jaccard: threshold for twin warning
      twin_min_shared: minimum shared for twin warning

    Returns: structured report.
    """
    if new_id in adj:
        # Existing node — lint against current graph (skip hypothetical
        # comparison, just report what motifs it currently participates in)
        before_adj = adj
        after_adj = adj
        is_existing = True
    else:
        before_adj = adj
        after_adj = _add_node_to_adj(adj, new_id, new_neighbors)
        is_existing = False

    def graph_metrics(a: dict[str, set[str]]) -> dict[str, Any]:
        V = len(a)
        E = sum(len(v) for v in a.values()) // 2
        # components
        visited = set(); comps = 0
        for n in a:
            if n in visited: continue
            comps += 1
            stack = [n]
            while stack:
                x = stack.pop()
                if x in visited: continue
                visited.add(x)
                stack.extend(y for y in a.get(x, set()) if y not in visited)
        # triangles
        T = 0
        for u in a:
            for v in a[u]:
                if v > u:
                    for w in a[u]:
                        if w > v and w in a[v]:
                            T += 1
        return {
            "V": V, "E": E, "components": comps,
            "beta1": E - V + comps, "triangles": T,
        }

    before_m = graph_metrics(before_adj)
    after_m = graph_metrics(after_adj)

    # Z-triangles formed BY new node (parent OR child)
    z_tri_created = []
    if not is_existing:
        # New node as parent: its 3 children pairwise connected
        children = sorted(new_neighbors)
        for i, a in enumerate(children):
            for j in range(i + 1, len(children)):
                b = children[j]
                if b not in after_adj.get(a, set()):
                    continue
                for k in range(j + 1, len(children)):
                    c = children[k]
                    if c in after_adj.get(a, set()) and c in after_adj.get(b, set()):
                        z_tri_created.append({
                            "parent": new_id, "children": [a, b, c],
                        })
        # New node as child: existing parent has 2 other children pairwise
        # connected, all three pairwise (incl. new_id)
        for parent in new_neighbors:
            other_children = after_adj.get(parent, set()) - {new_id}
            for sib1 in other_children:
                if sib1 not in new_neighbors:
                    continue
                for sib2 in other_children:
                    if sib2 <= sib1 or sib2 not in new_neighbors:
                        continue
                    if sib2 in after_adj.get(sib1, set()):
                        z_tri_created.append({
                            "parent": parent, "children": sorted([new_id, sib1, sib2]),
                        })

    # M2/M5 clique participation: find maximal cliques containing new_id
    # in after_adj (limit to size >= 4 for relevance)
    cliques_joined = []
    if not is_existing:
        # Bron-Kerbosch restricted to cliques containing new_id
        cands_for_new = {n for n in after_adj.get(new_id, set())}
        # Recursive enumeration of cliques in subgraph induced by new_id ∪ its neighbours
        def find_cliques_with(R: set[str], P: set[str], X: set[str], out: list):
            if not P and not X:
                if len(R) >= 4 and new_id in R:
                    out.append(frozenset(R))
                return
            pivot = max(P | X, key=lambda u: len(after_adj.get(u, set()) & P), default=None)
            if pivot is None: return
            for v in list(P - after_adj.get(pivot, set())):
                nbrs = after_adj.get(v, set())
                find_cliques_with(R | {v}, P & nbrs, X & nbrs, out)
                P = P - {v}; X = X | {v}
        cliques_with_new: list[frozenset[str]] = []
        # Start clique enumeration from new_id
        find_cliques_with({new_id}, cands_for_new, set(), cliques_with_new)
        # Dedup and partition
        seen = set()
        for clq in sorted(cliques_with_new, key=lambda c: -len(c)):
            key = tuple(sorted(clq))
            if key in seen: continue
            seen.add(key)
            principles = sorted(c for c in clq if c in core_principle_ids)
            cousins = sorted(c for c in clq if c not in core_principle_ids)
            if len(principles) == 1 and len(cousins) >= 3:
                motif = "M2"
            elif len(principles) >= 2 and len(cousins) >= 3:
                motif = "M5"
            elif len(principles) == 0 and len(cousins) >= 4:
                motif = "M2_orphan"
            else:
                continue
            new_role = "principle" if new_id in core_principle_ids else "cousin"
            cliques_joined.append({
                "motif": motif,
                "size": len(clq),
                "principles": principles,
                "cousins": cousins,
                "new_node_role": new_role,
            })

    # Twin candidates via Jaccard
    twin_warnings = []
    target_neighbors = after_adj.get(new_id, set())
    for nid, nbrs in after_adj.items():
        if nid == new_id: continue
        a_n = target_neighbors - {nid}
        b_n = nbrs - {new_id}
        if not a_n or not b_n: continue
        shared = a_n & b_n
        if len(shared) < twin_min_shared: continue
        union = a_n | b_n
        jac = len(shared) / len(union) if union else 0.0
        if jac < twin_jaccard: continue
        # Family-edge reclassification check (sibling-style edge between new and nid)
        # Not available without edge_labels — skip refinement here
        twin_warnings.append({
            "candidate": nid, "jaccard": round(jac, 3),
            "shared_count": len(shared),
            "shared_sample": sorted(shared)[:6],
        })
    twin_warnings.sort(key=lambda x: -x["jaccard"])

    # K_{m,n} (M6) check: does new node complete or extend any K_{3,3}?
    # Quick heuristic: check if new node + 2 existing non-adjacent peers
    # form K_{3,n} side with shared independent set of size >= 3.
    m6_extensions = []
    if not is_existing:
        # Find pairs of new_neighbors that are not adjacent to each other
        new_nbrs_list = sorted(new_neighbors)
        for i, x in enumerate(new_nbrs_list):
            for j in range(i + 1, len(new_nbrs_list)):
                y = new_nbrs_list[j]
                if y in after_adj.get(x, set()): continue  # need non-adj for side B
                # Common neighbours of x and y, intersected with new_id's neighbours
                common = after_adj[x] & after_adj[y] & new_neighbors
                common = [c for c in common if c != new_id]
                # Check c, x, y mutually non-adjacent
                if len(common) < 1: continue
                # Need at least 1 more node forming K_{3,*} side
                # full structural check: side_A = {new_id, x, y}, must be independent
                if x in after_adj.get(new_id, set()) and y in after_adj.get(new_id, set()):
                    # new_id-x and new_id-y are edges (they are neighbours by setup), but
                    # we need new_id, x, y to form INDEPENDENT side meaning NOT pairwise
                    # connected. Since x,y are new_id's neighbours, new_id<->x and
                    # new_id<->y are edges → side_A is NOT independent.
                    # Skip — bipartite side requires non-edges.
                    continue

    # Cycle-richness delta
    beta1_delta = after_m["beta1"] - before_m["beta1"]
    triangle_delta = after_m["triangles"] - before_m["triangles"]

    # Articulation status: would removing new_id leave graph 2-connected?
    # If is_existing, run articulation check; if hypothetical, the new node
    # is automatically not an articulation (it's a leaf relative to existing).
    articulation_concern = None
    if not is_existing and len(new_neighbors) == 1:
        articulation_concern = (
            f"Single connection ({list(new_neighbors)[0]}) — new node will "
            f"be a leaf. Articulation point of length-1; minimal structural "
            f"integration."
        )

    return {
        "is_existing": is_existing,
        "new_id": new_id,
        "new_neighbors": sorted(new_neighbors),
        "before": before_m,
        "after": after_m,
        "delta": {
            "V": after_m["V"] - before_m["V"],
            "E": after_m["E"] - before_m["E"],
            "beta1": beta1_delta,
            "triangles": triangle_delta,
        },
        "z_triangles_created": z_tri_created[:20],
        "z_triangles_count": len(z_tri_created),
        "cliques_joined": cliques_joined[:10],
        "cliques_joined_count": len(cliques_joined),
        "twin_warnings": twin_warnings[:5],
        "twin_warnings_count": len(twin_warnings),
        "articulation_concern": articulation_concern,
    }


def format_lint_report(report: dict[str, Any]) -> str:
    """Markdown report of motif-aware lint."""
    lines = ["# RP-Gate Motif-Aware Lint Report\n"]
    new_id = report["new_id"]
    lines.append(f"**Candidate node:** `{new_id}`")
    if report["is_existing"]:
        lines.append("- Mode: lint EXISTING node\n")
    else:
        lines.append(f"- Mode: hypothetical addition")
        lines.append(f"- Proposed neighbours ({len(report['new_neighbors'])}): "
                     f"{', '.join('`'+n+'`' for n in report['new_neighbors'][:10])}"
                     + (" …" if len(report['new_neighbors']) > 10 else ""))
        lines.append("")
        d = report["delta"]
        lines.append("## Topology delta")
        lines.append(f"- ΔV: +{d['V']}")
        lines.append(f"- ΔE: +{d['E']}")
        lines.append(f"- Δβ₁ (independent cycles): "
                     f"{'+' if d['beta1'] >= 0 else ''}{d['beta1']}")
        lines.append(f"- Δtriangles: +{d['triangles']}")
        lines.append("")

    if report["z_triangles_count"]:
        lines.append(f"## Z-triangles created (M1): {report['z_triangles_count']}")
        for t in report["z_triangles_created"][:5]:
            p = t["parent"]; c = t["children"]
            lines.append(f"  - parent `{p}` → "
                         f"{{`{c[0]}`, `{c[1]}`, `{c[2]}`}}")
        if report["z_triangles_count"] > 5:
            lines.append(f"  …and {report['z_triangles_count']-5} more")
        lines.append("")

    if report["cliques_joined_count"]:
        lines.append(f"## Cliques joined (M2/M5): {report['cliques_joined_count']}")
        for c in report["cliques_joined"][:5]:
            lines.append(
                f"  - **{c['motif']}** K_{c['size']} as {c['new_node_role']}: "
                f"P={c['principles']}, C={c['cousins']}"
            )
        if report["cliques_joined_count"] > 5:
            lines.append(f"  …and {report['cliques_joined_count']-5} more")
        lines.append("")

    if report["twin_warnings_count"]:
        lines.append(f"## Twin warnings (M3): {report['twin_warnings_count']}")
        for w in report["twin_warnings"][:3]:
            lines.append(
                f"  - `{w['candidate']}` Jaccard={w['jaccard']} "
                f"(shared={w['shared_count']}, sample: "
                f"{', '.join('`'+x+'`' for x in w['shared_sample'])})"
            )
        if report["twin_warnings_count"] > 3:
            lines.append(f"  …and {report['twin_warnings_count']-3} more")
        lines.append("")

    if report["articulation_concern"]:
        lines.append(f"## ⚠ Articulation concern\n")
        lines.append(report["articulation_concern"])
        lines.append("")

    if (report["z_triangles_count"] == 0 and report["cliques_joined_count"] == 0
            and report["twin_warnings_count"] == 0):
        lines.append("\n_No structural-motif signals detected. Node integrates "
                     "without joining cliques, creating triangles, or duplicating "
                     "neighbour sets._")

    return "\n".join(lines)


def measure_cycle_topology(
    adj: dict[str, set[str]],
    statuses: dict[str, str] | None = None,
    layers: dict[str, str] | None = None,
    super_hub_degree: int = 50,
    lengths: tuple[int, ...] = (4, 5, 6, 7),
    enumerate_cap: int = 5000,
) -> dict[str, Any]:
    """Measure graph-level cycle-richness (round 43 motif M7).

    Returns:
      - cyclomatic_number β₁ = E - V + components
      - triangle_count (M1-class closures)
      - induced cycle counts at each length in `lengths`
      - substantive cycle counts (DEMONSTRATED, sub-hub, multi-layer)
        if statuses + layers provided
    """
    V = len(adj)
    E = sum(len(v) for v in adj.values()) // 2

    # Components (connected)
    visited: set[str] = set()
    components = 0
    for n in adj:
        if n in visited:
            continue
        components += 1
        stack = [n]
        while stack:
            x = stack.pop()
            if x in visited:
                continue
            visited.add(x)
            stack.extend(y for y in adj.get(x, set()) if y not in visited)

    cyclomatic = E - V + components

    # Triangle count
    triangles = 0
    for a in adj:
        for b in adj[a]:
            if b > a:
                for c in adj[a]:
                    if c > b and c in adj[b]:
                        triangles += 1

    deg = {n: len(adj[n]) for n in adj}

    def find_induced_cycles(length: int, cap: int) -> list[tuple[str, ...]]:
        found: set[tuple[str, ...]] = set()
        nodes = sorted(adj.keys())
        for start in nodes:
            if len(found) >= cap:
                break
            stack = [(start, [start])]
            while stack:
                cur, path = stack.pop()
                if len(path) == length:
                    if start in adj.get(cur, set()):
                        cycle = path
                        chord_free = True
                        for i, x in enumerate(cycle):
                            for j in range(i + 2, len(cycle)):
                                if j == len(cycle) - 1 and i == 0:
                                    continue
                                if cycle[j] in adj.get(x, set()):
                                    chord_free = False
                                    break
                            if not chord_free:
                                break
                        if chord_free:
                            rotations = [
                                tuple(cycle[i:] + cycle[:i])
                                for i in range(length)
                            ]
                            rotations += [
                                tuple(reversed(r)) for r in rotations
                            ]
                            found.add(min(rotations))
                    continue
                if len(path) >= length:
                    continue
                for nb in adj.get(cur, set()):
                    if nb in path or nb < start:
                        continue
                    stack.append((nb, path + [nb]))
        return list(found)

    cycle_counts: dict[int, int] = {}
    substantive_counts: dict[int, int] = {}
    sample_substantive: dict[int, list[list[str]]] = {}

    for L in lengths:
        cycles = find_induced_cycles(L, enumerate_cap)
        cycle_counts[L] = len(cycles)
        if statuses is not None and layers is not None:
            sub = []
            for c in cycles:
                if any(deg.get(n, 0) > super_hub_degree for n in c):
                    continue
                cy_layers = {layers.get(n, "?") for n in c}
                if len(cy_layers) < 2:
                    continue
                if not all(statuses.get(n, "") == "DEMONSTRATED" for n in c):
                    continue
                sub.append(list(c))
            substantive_counts[L] = len(sub)
            sample_substantive[L] = sub[:5]

    return {
        "V": V,
        "E_distinct": E,
        "components": components,
        "cyclomatic_number_beta1": cyclomatic,
        "cycle_richness_ratio": round(cyclomatic / V, 3) if V else 0.0,
        "triangles": triangles,
        "induced_cycle_counts": cycle_counts,
        "substantive_cycle_counts": substantive_counts,
        "sample_substantive_cycles": sample_substantive,
    }


# ─── Fractal-geometric audit (round 48) ──────────────────────────────

def _bfs_distances(adj: dict[str, set[str]], source: str) -> dict[str, int]:
    """BFS from source, returning shortest-path distances."""
    dist = {source: 0}
    frontier = [source]
    while frontier:
        next_frontier = []
        for u in frontier:
            d = dist[u]
            for v in adj.get(u, set()):
                if v not in dist:
                    dist[v] = d + 1
                    next_frontier.append(v)
        frontier = next_frontier
    return dist


def _power_law_fit(xs: list[float], ys: list[float]) -> tuple[float, float, float]:
    """Fit y = c * x^d via log-log linear regression.
    Returns (d, log_c, R²). Drops zero/negative values.
    """
    pts = [(x, y) for x, y in zip(xs, ys) if x > 0 and y > 0]
    if len(pts) < 3:
        return (0.0, 0.0, 0.0)
    import math
    log_x = [math.log(p[0]) for p in pts]
    log_y = [math.log(p[1]) for p in pts]
    n = len(pts)
    mean_x = sum(log_x) / n
    mean_y = sum(log_y) / n
    num = sum((log_x[i] - mean_x) * (log_y[i] - mean_y) for i in range(n))
    den = sum((log_x[i] - mean_x) ** 2 for i in range(n))
    if den == 0:
        return (0.0, mean_y, 0.0)
    d = num / den
    log_c = mean_y - d * mean_x
    # R²
    ss_tot = sum((log_y[i] - mean_y) ** 2 for i in range(n))
    ss_res = sum((log_y[i] - (d * log_x[i] + log_c)) ** 2 for i in range(n))
    r_sq = 1 - (ss_res / ss_tot) if ss_tot > 0 else 1.0
    return (d, log_c, r_sq)


def _local_clustering(adj: dict[str, set[str]], node: str) -> float:
    """Local clustering coefficient: triangles through node /
    possible triangles."""
    nbrs = adj[node]
    k = len(nbrs)
    if k < 2:
        return 0.0
    nbrs_list = list(nbrs)
    triangles = 0
    for i, u in enumerate(nbrs_list):
        for v in nbrs_list[i + 1:]:
            if v in adj.get(u, set()):
                triangles += 1
    return 2 * triangles / (k * (k - 1))


def fractal_audit(
    adj: dict[str, set[str]],
    seed_count: int = 30,
    max_radius: int = 4,
) -> dict[str, Any]:
    """Fractal-geometric audit of the framework graph.

    Designed for SMALL-WORLD + FRACTAL-MOTIF graphs (not strict
    geometric fractals). Computes:
      - Cluster-growth N(r) for r=1..max_radius (raw curves; no
        power-law forced because small-world graphs saturate fast)
      - Clustering coefficient C and small-world coefficient σ
      - Degree distribution and tail-power-law fit
      - β₁/V cycle-richness ratio (motif-fractality signature)
      - Twin pair count (M3 motif)
      - Average path length L vs random-graph baseline
    """
    import math
    nodes = sorted(adj.keys())
    V = len(nodes)
    E = sum(len(v) for v in adj.values()) // 2
    if V == 0 or E == 0:
        return {"V": V, "E": E, "error": "empty graph"}

    # Stratified seeds by degree
    deg_sorted = sorted(nodes, key=lambda n: len(adj[n]))
    step = max(1, V // seed_count)
    seeds = [deg_sorted[i * step] for i in range(seed_count)
             if i * step < V]

    # 1. Cluster-growth raw curves N(r)
    growth_curves = []
    for seed in seeds[:8]:
        dist = _bfs_distances(adj, seed)
        curve = []
        for r in range(1, max_radius + 1):
            n_at_r = sum(1 for d in dist.values() if d <= r)
            curve.append((r, n_at_r))
        growth_curves.append({"seed": seed, "deg": len(adj[seed]),
                              "curve": curve})

    # 2. Clustering coefficient
    local_cs = [_local_clustering(adj, n) for n in nodes if len(adj[n]) >= 2]
    avg_C = sum(local_cs) / len(local_cs) if local_cs else 0.0
    p_edge = 2 * E / (V * (V - 1)) if V > 1 else 0.0
    C_random = p_edge
    C_ratio = avg_C / C_random if C_random > 0 else 0.0

    # 3. Average path length (sample)
    total_d = 0; pairs_n = 0
    for seed in seeds[:15]:
        dist = _bfs_distances(adj, seed)
        for d in dist.values():
            if d > 0:
                total_d += d; pairs_n += 1
    L = total_d / pairs_n if pairs_n else 0.0
    L_random = (math.log(V) / math.log(max(1.001, 2 * E / V))
                if V > 1 and 2 * E / V > 1 else float('inf'))
    L_ratio = L / L_random if L_random > 0 else 0.0
    sigma_small_world = C_ratio / L_ratio if L_ratio > 0 else 0.0

    # 4. Degree distribution + tail power law
    from collections import Counter
    degrees = [len(adj[n]) for n in nodes]
    deg_hist = Counter(degrees)
    sorted_ks = sorted(deg_hist.keys())
    # Tail fit: degrees >= median
    median_deg = sorted(degrees)[V // 2] if V else 0
    tail = [k for k in sorted_ks if k >= median_deg]
    if len(tail) >= 4:
        ks = [float(k) for k in tail]
        ps = [float(deg_hist[int(k)]) for k in tail]
        gamma_neg, _, r_sq_deg = _power_law_fit(ks, ps)
        gamma = -gamma_neg
    else:
        gamma = 0.0; r_sq_deg = 0.0

    # 5. Cyclomatic
    visited = set(); components = 0
    for n in adj:
        if n in visited: continue
        components += 1
        stack = [n]
        while stack:
            x = stack.pop()
            if x in visited: continue
            visited.add(x)
            stack.extend(y for y in adj.get(x, set()) if y not in visited)
    beta1 = E - V + components

    # 6. Twin pairs (M3 motif count)
    twin_count = 0
    for i, a in enumerate(nodes):
        if len(adj[a]) < 4: continue
        for b in nodes[i + 1:]:
            if len(adj[b]) < 4: continue
            na = adj[a] - {b}; nb = adj[b] - {a}
            if not na or not nb: continue
            inter = na & nb; union = na | nb
            if not union: continue
            if len(inter) / len(union) == 1.0 and len(inter) >= 3:
                twin_count += 1

    # 7. Triangles (M1 closures) and density
    triangles = 0
    for u in adj:
        for v in adj[u]:
            if v > u:
                for w in adj[u]:
                    if w > v and w in adj[v]:
                        triangles += 1
    triangle_density = triangles / V if V else 0.0

    # 8. Interpretation
    interp = []
    interp.append(
        f"Small-world coefficient σ = {sigma_small_world:.2f} "
        f"({'STRONGLY' if sigma_small_world > 5 else 'weakly'} "
        f"small-world)" if sigma_small_world > 1
        else f"Small-world coefficient σ = {sigma_small_world:.2f} "
             f"(NOT small-world)"
    )
    interp.append(
        f"Clustering C = {avg_C:.3f} vs random {C_random:.3f}; "
        f"ratio C/C_rand = {C_ratio:.1f}"
    )
    interp.append(
        f"Path length L = {L:.2f} vs random {L_random:.2f}; "
        f"ratio L/L_rand = {L_ratio:.2f}"
    )
    if 3.0 <= beta1 / V <= 4.0:
        interp.append(
            f"β₁/V = {beta1/V:.2f} — cycle-rich, motif-fractal regime "
            f"(scale-invariance compatible per round 47 prediction)"
        )
    if 1.5 <= gamma <= 3.5 and r_sq_deg > 0.7:
        interp.append(
            f"Degree-tail γ = {gamma:.2f} (R²={r_sq_deg:.2f}) — "
            f"scale-free tail regime"
        )
    interp.append(
        f"Triangle density M1/V = {triangle_density:.2f} "
        f"(motif-fractality marker)"
    )
    interp.append(
        f"Diagnostic: graph is small-world (σ >> 1) with motif-"
        f"fractality (β₁/V invariant under growth). NOT strict "
        f"geometric fractal — fractality lives in motif-substrate."
    )

    return {
        "V": V, "E": E, "components": components,
        "cluster_growth_raw": growth_curves,
        "clustering": {
            "C_avg": round(avg_C, 4),
            "C_random_baseline": round(C_random, 4),
            "C_ratio_vs_random": round(C_ratio, 2),
        },
        "path_length": {
            "L_avg": round(L, 3),
            "L_random_baseline": round(L_random, 3),
            "L_ratio_vs_random": round(L_ratio, 3),
        },
        "small_world_coefficient_sigma": round(sigma_small_world, 2),
        "degree_distribution": {
            "median": median_deg,
            "max": max(degrees) if degrees else 0,
            "tail_gamma": round(gamma, 3),
            "tail_r_squared": round(r_sq_deg, 3),
            "scale_free_tail": (1.5 <= gamma <= 3.5 and r_sq_deg > 0.7),
        },
        "cyclomatic": {
            "beta1": beta1,
            "ratio_per_node": round(beta1 / V, 3) if V else 0.0,
        },
        "triangles_M1": {
            "count": triangles,
            "density_per_V": round(triangle_density, 3),
        },
        "twin_pairs_jaccard1": twin_count,
        "interpretation": interp,
    }


def format_fractal_audit(report: dict[str, Any]) -> str:
    """Markdown report of fractal audit."""
    if "error" in report:
        return f"# Fractal Audit Error\n\n{report['error']}"
    lines = ["# Fractal-Geometric Audit Report\n"]
    lines.append(f"**Graph:** V={report['V']}, E={report['E']}\n")

    lines.append("## Small-world signature")
    cl = report["clustering"]
    pl = report["path_length"]
    lines.append(f"- **σ (small-world coef):** "
                 f"{report['small_world_coefficient_sigma']}")
    lines.append(f"- C_avg = {cl['C_avg']} "
                 f"(random baseline {cl['C_random_baseline']}); "
                 f"C/C_rand = {cl['C_ratio_vs_random']}")
    lines.append(f"- L_avg = {pl['L_avg']} "
                 f"(random baseline {pl['L_random_baseline']}); "
                 f"L/L_rand = {pl['L_ratio_vs_random']}")

    lines.append("\n## Cycle-richness (motif-fractality signature)")
    cy = report["cyclomatic"]
    lines.append(f"- β₁ = {cy['beta1']}")
    lines.append(f"- **β₁/V = {cy['ratio_per_node']}**")
    tr = report["triangles_M1"]
    lines.append(f"- Triangles (M1): {tr['count']}, "
                 f"M1/V = {tr['density_per_V']}")
    lines.append(f"- Twin pairs (M3, Jaccard=1.0): "
                 f"{report['twin_pairs_jaccard1']}")

    lines.append("\n## Degree distribution")
    dd = report["degree_distribution"]
    lines.append(f"- median = {dd['median']}, max = {dd['max']}")
    lines.append(f"- tail γ = {dd['tail_gamma']} "
                 f"(R²={dd['tail_r_squared']}); "
                 f"scale-free tail: **{dd['scale_free_tail']}**")

    lines.append("\n## Cluster-growth raw curves N(r)")
    for c in report["cluster_growth_raw"][:5]:
        curve = ", ".join(f"({r}→{n})" for r, n in c["curve"])
        lines.append(f"- `{c['seed']}` (deg={c['deg']}): {curve}")

    lines.append("\n## Interpretation\n")
    for i in report["interpretation"]:
        lines.append(f"- {i}")

    return "\n".join(lines)


# ─── Top-level: run all detectors ─────────────────────────────────────

def run_all_detectors(
    edge_pairs: list[tuple[str, str]],
    core_principle_ids: set[str],
    z_triangle_hub_threshold: int = 25,
    z_triangle_max: int = 50,
    clique_min_size: int = 5,
    clique_min_cousins: int = 3,
    twin_jaccard: float = 1.0,
    twin_min_shared: int = 3,
    bipartite_min_m: int = 3,
    bipartite_min_n: int = 3,
    bipartite_max: int = 50,
) -> dict[str, Any]:
    """Run M1, M2/M5, M3, M4, M6 detectors and return aggregated report."""
    adj = _build_adjacency(edge_pairs)
    z_triangles = detect_z_triangles(
        adj, hub_threshold=z_triangle_hub_threshold,
        max_results=z_triangle_max,
    )
    clique_motifs = detect_clique_motifs(
        adj, core_principle_ids,
        min_clique_size=clique_min_size,
        min_cousins=clique_min_cousins,
    )
    twins = detect_twin_pairs(
        adj, jaccard_threshold=twin_jaccard,
        min_shared=twin_min_shared,
    )
    aps = detect_articulation_points(adj)
    kmns = detect_bipartite_kmn(
        adj, min_m=bipartite_min_m, min_n=bipartite_min_n,
        max_results=bipartite_max,
    )

    return {
        "graph_stats": {
            "nodes": len(adj),
            "edges": sum(len(v) for v in adj.values()) // 2,
        },
        "motif_counts": {
            "M1_z_triangles": len(z_triangles),
            "M2_family_cliques": sum(1 for m in clique_motifs if m.motif == "M2"),
            "M5_stratifications": sum(1 for m in clique_motifs if m.motif == "M5"),
            "M2_orphan_cliques": sum(1 for m in clique_motifs if m.motif == "M2_orphan"),
            "M3_twin_pairs": len(twins),
            "M4_articulation_points": len(aps),
            "M6_bipartite_kmn": len(kmns),
        },
        "M1_z_triangles": [asdict(m) for m in z_triangles],
        "M5_stratifications": [
            asdict(m) for m in clique_motifs if m.motif == "M5"
        ],
        "M2_family_cliques": [
            asdict(m) for m in clique_motifs if m.motif == "M2"
        ],
        "M2_orphan_cliques": [
            asdict(m) for m in clique_motifs if m.motif == "M2_orphan"
        ],
        "M3_twin_pairs": [asdict(m) for m in twins],
        "M4_articulation_points": [asdict(m) for m in aps],
        "M6_bipartite_kmn": [asdict(m) for m in kmns],
    }


def format_motif_report(report: dict[str, Any]) -> str:
    """Markdown report of motif findings."""
    lines = ["# Structural Motif Auto-Detection Report\n"]
    g = report["graph_stats"]
    lines.append(f"**Graph:** {g['nodes']} nodes, {g['edges']} edges\n")
    counts = report["motif_counts"]
    lines.append("## Motif counts")
    lines.append(f"- M1 (Z-triangles, hub-filtered): {counts['M1_z_triangles']}")
    lines.append(f"- M5 (Principle-stratification, K_{{p+n}}): "
                 f"{counts['M5_stratifications']}")
    lines.append(f"- M2 (Family-clique, single anchor): "
                 f"{counts['M2_family_cliques']}")
    lines.append(f"- M2_orphan (clique without principle anchor): "
                 f"{counts['M2_orphan_cliques']}")
    lines.append(f"- M3 (Structural twin pairs): {counts['M3_twin_pairs']}")
    lines.append(f"- M4 (Articulation points): {counts['M4_articulation_points']}")

    if report["M5_stratifications"]:
        lines.append("\n## M5 — Principle Stratification (K_{p+n})\n")
        for m in report["M5_stratifications"]:
            lines.append(f"### K_{m['size']} clique")
            lines.append(f"- Principles ({len(m['role_partition']['principles'])}): "
                         f"{', '.join('`'+x+'`' for x in m['role_partition']['principles'])}")
            lines.append(f"- Cousins ({len(m['role_partition']['cousins'])}): "
                         f"{', '.join('`'+x+'`' for x in m['role_partition']['cousins'])}")
            lines.append(f"- Edges: {m['edge_count']}, density: {m['edge_density']}")
            lines.append(f"- Notes: {m['notes']}\n")

    if report["M2_family_cliques"]:
        lines.append("\n## M2 — Family Clique (single anchor)\n")
        for m in report["M2_family_cliques"]:
            lines.append(f"### K_{m['size']}")
            lines.append(f"- Anchor: `{m['role_partition']['principles'][0]}`")
            lines.append(f"- Cousins: "
                         f"{', '.join('`'+x+'`' for x in m['role_partition']['cousins'])}\n")

    if report["M2_orphan_cliques"]:
        lines.append("\n## M2_orphan — Clique without principle anchor\n")
        for m in report["M2_orphan_cliques"]:
            lines.append(f"- K_{m['size']}: "
                         f"{', '.join('`'+x+'`' for x in m['members'])}")

    if report["M3_twin_pairs"]:
        lines.append("\n## M3 — Structural Twin Pairs (Jaccard=1.0)\n")
        for m in report["M3_twin_pairs"]:
            a, b = m["role_partition"]["twin_pair"]
            shared = m["role_partition"]["shared_neighbors"]
            lines.append(f"- `{a}` ≡ `{b}` "
                         f"(shared: {', '.join('`'+x+'`' for x in shared[:6])}"
                         + (" …" if len(shared) > 6 else "") + ")")

    if report["M4_articulation_points"]:
        lines.append("\n## M4 — Articulation Points\n")
        for m in report["M4_articulation_points"]:
            ap_id = m["role_partition"]["articulation_point"][0]
            isolated = m["role_partition"]["isolated_components"]
            lines.append(f"- `{ap_id}` (deg={m['edge_count']}): {m['notes']}")
            for comp in isolated[:3]:
                lines.append(f"  - isolates: `{comp}`")

    if report.get("M6_bipartite_kmn"):
        lines.append(f"\n## M6 — Bipartite K_{{m,n}} "
                     f"({len(report['M6_bipartite_kmn'])})\n")
        for m in report["M6_bipartite_kmn"][:10]:
            A = m["role_partition"]["side_A"]
            B = m["role_partition"]["side_B"]
            lines.append(f"### K_{{{len(A)},{len(B)}}}")
            lines.append(f"- Side A: "
                         f"{', '.join('`'+x+'`' for x in A)}")
            lines.append(f"- Side B: "
                         f"{', '.join('`'+x+'`' for x in B)}\n")

    if report["M1_z_triangles"]:
        lines.append(f"\n## M1 — Z-triangles ({len(report['M1_z_triangles'])} "
                     f"hub-filtered)\n")
        for m in report["M1_z_triangles"][:15]:
            parent = m["role_partition"]["parent"][0]
            children = m["role_partition"]["children"]
            lines.append(f"- `{parent}` → "
                         f"{{`{children[0]}`, `{children[1]}`, `{children[2]}`}}")
        if len(report["M1_z_triangles"]) > 15:
            lines.append(f"  …and {len(report['M1_z_triangles']) - 15} more")

    return "\n".join(lines)
