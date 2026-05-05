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


# ─── M7: induced-cycle topology (graph-level property) ──────────────

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
