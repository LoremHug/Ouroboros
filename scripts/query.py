"""Run Cypher queries against the Kuzu DB.

Usage:
    python -m scripts.query 'MATCH (n:Node) WHERE n.layer = "core" RETURN n.id'
    python -m scripts.query --neighbors N_BPIEngagement
    python -m scripts.query --status CONDITIONAL
    python -m scripts.query --orphans
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


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("cypher", nargs="?", help="raw Cypher query")
    g.add_argument("--neighbors", metavar="ID", help="show neighbors of node")
    g.add_argument("--status", metavar="STATUS", help="list nodes by status")
    g.add_argument("--orphans", action="store_true", help="find nodes not reaching DEF")
    p.add_argument("--depth", type=int, default=1, help="depth for --neighbors (default 1)")
    args = p.parse_args()

    if args.neighbors:
        neighbors(args.neighbors, args.depth)
    elif args.status:
        by_status(args.status)
    elif args.orphans:
        orphans()
    elif args.cypher:
        run(args.cypher)


if __name__ == "__main__":
    main()
