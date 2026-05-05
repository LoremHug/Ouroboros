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
) -> dict[str, Any]:
    """Run M1, M2/M5, M3, M4 detectors and return aggregated report."""
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
