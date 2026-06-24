"""Run Cypher queries against the Kuzu DB.

Usage:
    python -m scripts.query 'MATCH (n:Node) WHERE n.layer = "core" RETURN n.id'
    python -m scripts.query --neighbors N_BPIEngagement
    python -m scripts.query --class-a N_TraceDeepensBasin  # undirected, structurally
    python -m scripts.query --status CONDITIONAL
    python -m scripts.query --orphans

Class A queries enforce undirected traversal at tool level — Class A
(true identity, sibling, or directional grounding) is structurally
discoverable from either side; storage direction is rhetorical, not
structural. Per audit findings, see CLAUDE.md "Compact mathematical
articulation" and N_TraceDeepensBasin commentary.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.db import connect  # noqa: E402


def run(cypher: str) -> None:
    db, conn = connect()
    res = conn.execute(cypher)
    cols = res.get_column_names()
    print("  ".join(c.ljust(20) for c in cols))
    print("─" * (22 * len(cols)))
    while res.has_next():
        row = res.get_next()
        print("  ".join(str(v)[:60].ljust(20) for v in row))


def neighbors(node_id: str, depth: int = 1) -> None:
    db, conn = connect()
    cy = f"""
        MATCH (a:Node {{id: $nid}})-[e:Edge*1..{depth}]-(b:Node)
        RETURN DISTINCT b.id, b.layer, b.status, b.title
    """
    res = conn.execute(cy, {"nid": node_id})
    print(f"Neighbors of {node_id} (depth ≤ {depth}):")
    while res.has_next():
        row = res.get_next()
        print(f"  {row[0]:<30} [{row[1]:<10}] {row[2]:<14} {row[3][:60]}")


def by_status(status: str) -> None:
    db, conn = connect()
    res = conn.execute("""
        MATCH (n:Node) WHERE n.status = $st
        RETURN n.id, n.layer, n.title
    """, {"st": status})
    while res.has_next():
        row = res.get_next()
        print(f"  {row[0]:<30} [{row[1]:<10}] {row[2][:80]}")


def orphans() -> None:
    """Nodes with no path to DEF (in either direction)."""
    db, conn = connect()
    # Nodes that aren't connected to DEF at all
    res = conn.execute("""
        MATCH (n:Node)
        WHERE n.id <> 'DEF'
          AND NOT EXISTS { MATCH (n)-[:Edge*]-(:Node {id: 'DEF'}) }
        RETURN n.id, n.layer, n.status
    """)
    print("Nodes with no path to DEF:")
    found = False
    while res.has_next():
        row = res.get_next()
        print(f"  {row[0]:<30} [{row[1]}] {row[2]}")
        found = True
    if not found:
        print("  (none — all nodes connect to DEF)")


# Label patterns identifying structurally-symmetric relations (Class A
# proper, sibling, paired-readings, substrate-cousin). These should be
# discoverable from either endpoint regardless of edge storage direction.
CLASS_A_LABEL_PATTERNS = (
    "class_a", "iff", "same_", "is_compound", "is_substrate_cousin",
    "instance_of_compound", "sibling_", "paired_", "two_sides_of",
    "two_coordinates", "two_face", "three_readings", "anchor",
    "primitive", "_grounds_", "two_metric_readings",
)


def class_a_neighbors(node_id: str, depth: int = 2) -> None:
    """Find all structurally-related neighbors via undirected traversal,
    filtered to Class-A-like labels.

    Enforces undirected (-[:Edge]-) traversal at tool level: structural
    symmetry of Class A means visibility from either endpoint is required,
    independent of which side the edge was authored from. Storage stays
    minimal (one edge per pair, option A from audit); query enforces
    symmetry of reading.

    Filter is conservative — includes true Class A, sibling relations,
    and grounding/derivation pairs that share substrate-cousin character.
    For pure topology neighbors (no label filter), use --neighbors.
    """
    db, conn = connect()
    cy = f"""
        MATCH (a:Node {{id: $nid}})-[e:Edge*1..{depth}]-(b:Node)
        WHERE b.id <> $nid
        RETURN DISTINCT b.id, b.layer, b.status, b.title
    """
    res = conn.execute(cy, {"nid": node_id})
    rows = []
    while res.has_next():
        rows.append(res.get_next())

    # Filter to those reachable via at least one Class-A-like edge
    # (verify by checking direct neighbors' edge labels)
    direct = conn.execute("""
        MATCH (a:Node {id: $nid})-[e:Edge]-(b:Node)
        RETURN DISTINCT b.id, e.label
    """, {"nid": node_id})

    direct_class_a = set()
    while direct.has_next():
        bid, lbl = direct.get_next()
        if lbl and any(p in lbl.lower() for p in CLASS_A_LABEL_PATTERNS):
            direct_class_a.add(bid)

    print(f"Class A neighbors of {node_id} (depth ≤ {depth}, undirected):")
    if not direct_class_a:
        print(f"  (no Class-A-like direct edges; check --neighbors for any)")
        return

    # For depth-1, show only Class A direct; for deeper, show all reachable
    if depth == 1:
        for nid, layer, status, title in rows:
            if nid in direct_class_a:
                print(f"  {nid:<30} [{layer or '?':<10}] [{status or '?':<14}] {(title or '')[:55]}")
    else:
        print(f"  Direct Class A: {len(direct_class_a)} nodes")
        print(f"  Total reachable in {depth} hops: {len(rows)} nodes")
        for nid, layer, status, title in rows:
            marker = "★" if nid in direct_class_a else " "
            print(f"  {marker} {nid:<30} [{layer or '?':<10}] [{status or '?':<14}] {(title or '')[:50]}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("cypher", nargs="?", help="raw Cypher query")
    g.add_argument("--neighbors", metavar="ID", help="show neighbors of node (all edges)")
    g.add_argument("--class-a", metavar="ID", dest="class_a",
                   help="show Class-A-like neighbors (undirected, structural symmetry enforced)")
    g.add_argument("--status", metavar="STATUS", help="list nodes by status")
    g.add_argument("--orphans", action="store_true", help="find nodes not reaching DEF")
    p.add_argument("--depth", type=int, default=1,
                   help="depth for --neighbors / --class-a (default 1)")
    args = p.parse_args()

    if args.neighbors:
        neighbors(args.neighbors, args.depth)
    elif args.class_a:
        class_a_neighbors(args.class_a, args.depth)
    elif args.status:
        by_status(args.status)
    elif args.orphans:
        orphans()
    elif args.cypher:
        run(args.cypher)


if __name__ == "__main__":
    main()
