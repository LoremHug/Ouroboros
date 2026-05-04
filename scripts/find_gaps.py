"""Find structural gaps — candidates for missing edges or unfinished nodes.

Heuristics:
1. High common-neighbor pairs without direct edge (Jaccard ≥ threshold)
2. Stub nodes (Status = STUB) needing content
3. Unjustified edges (no why_forced or justification recorded)
4. Hub asymmetries (nodes with many in-edges but no out-edges to core, or vice versa)

Usage:
    python -m scripts.find_gaps                  # all checks
    python -m scripts.find_gaps --jaccard 0.4    # only similar pairs
    python -m scripts.find_gaps --stubs
    python -m scripts.find_gaps --unjustified
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.db import connect  # noqa: E402


def neighbor_set(conn, node_id: str) -> set[str]:
    res = conn.execute(
        "MATCH (a:Node {id: $id})-[:Edge]-(b:Node) RETURN DISTINCT b.id",
        {"id": node_id},
    )
    s = set()
    while res.has_next():
        s.add(res.get_next()[0])
    return s


def all_node_ids(conn) -> list[str]:
    res = conn.execute("MATCH (n:Node) RETURN n.id ORDER BY n.id")
    out = []
    while res.has_next():
        out.append(res.get_next()[0])
    return out


def has_edge(conn, a: str, b: str) -> bool:
    res = conn.execute(
        "MATCH (a:Node {id: $a})-[:Edge]-(b:Node {id: $b}) RETURN count(*) > 0",
        {"a": a, "b": b},
    )
    return bool(res.get_next()[0])


def jaccard_pairs(threshold: float = 0.4, min_shared: int = 2) -> None:
    db, conn = connect()
    ids = all_node_ids(conn)
    nbrs = {nid: neighbor_set(conn, nid) for nid in ids}
    seen: set[tuple[str, str]] = set()
    pairs: list[tuple[str, str, float, int]] = []

    print(f"\nCommon-neighbor candidates (Jaccard ≥ {threshold}, shared ≥ {min_shared}, no direct edge)")
    print("─" * 80)
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            if a == b or (a, b) in seen:
                continue
            seen.add((a, b))
            na, nb = nbrs[a], nbrs[b]
            if not na or not nb:
                continue
            inter = na & nb
            if len(inter) < min_shared:
                continue
            union = na | nb
            j = len(inter) / len(union)
            if j >= threshold and not has_edge(conn, a, b):
                pairs.append((a, b, j, len(inter)))

    pairs.sort(key=lambda p: -p[2])
    if not pairs:
        print("  (none)")
        return
    for a, b, j, n in pairs[:40]:
        print(f"  {a:<28} ↔ {b:<28}  J={j:.2f}  shared={n}")


def stubs() -> None:
    db, conn = connect()
    res = conn.execute("""
        MATCH (n:Node) WHERE n.status = 'STUB'
        OPTIONAL MATCH (n)-[e:Edge]-()
        WITH n, count(e) AS deg
        RETURN n.id, n.layer, deg ORDER BY deg DESC
    """)
    print("\nStub nodes (no CLAIM body) by degree:")
    print("─" * 60)
    while res.has_next():
        row = res.get_next()
        print(f"  {row[0]:<28} [{row[1]:<10}] deg={row[2]}")


def unjustified() -> None:
    db, conn = connect()
    res = conn.execute("""
        MATCH (a:Node)-[e:Edge]->(b:Node)
        WHERE e.why_forced = '' AND e.justification = ''
        RETURN a.id, b.id, e.label LIMIT 50
    """)
    rows = []
    while res.has_next():
        rows.append(res.get_next())
    print(f"\nUnjustified edges (no why_forced, no justification): {len(rows)} shown")
    print("─" * 80)
    for r in rows:
        print(f"  {r[0]:<28} → {r[1]:<28}  {r[2]}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--jaccard", type=float, nargs="?", const=0.4, default=None)
    p.add_argument("--min-shared", type=int, default=2, help="min shared neighbors (default 2)")
    p.add_argument("--stubs", action="store_true")
    p.add_argument("--unjustified", action="store_true")
    args = p.parse_args()

    any_specific = args.jaccard is not None or args.stubs or args.unjustified
    if not any_specific:
        jaccard_pairs(0.4, args.min_shared)
        stubs()
        unjustified()
    else:
        if args.jaccard is not None:
            jaccard_pairs(args.jaccard, args.min_shared)
        if args.stubs:
            stubs()
        if args.unjustified:
            unjustified()


if __name__ == "__main__":
    main()
