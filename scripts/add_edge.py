"""Add an edge: persist to additions.yaml AND apply to local Kuzu DB.

Usage:
    python -m scripts.add_edge N_BPIEngagement N_Shannon \\
        --label shannon_capacity_is_BPI_constraint \\
        --status D \\
        --justification "K(O)<K(F) and Shannon capacity are one structure" \\
        --why-forced "Alternative requires two independent info-limit mechanisms"
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from schema import EdgeStatus  # noqa: E402
from scripts.db import connect  # noqa: E402
from scripts import additions as additions_io  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("source")
    p.add_argument("target")
    p.add_argument("--label", required=True)
    p.add_argument("--status", choices=[e.value for e in EdgeStatus], default="D")
    p.add_argument("--justification", default="")
    p.add_argument("--why-forced", default="")
    p.add_argument("--update", action="store_true", help="overwrite if (src,tgt,label) exists")
    args = p.parse_args()

    db, conn = connect()
    # Verify endpoints
    for nid in (args.source, args.target):
        r = conn.execute("MATCH (n:Node {id: $id}) RETURN count(n)", {"id": nid})
        if r.get_next()[0] == 0:
            print(f"error: node not found: {nid}")
            print("create it first with: python -m scripts.add_node " + nid)
            sys.exit(1)

    # Persist to additions.yaml first (source of truth)
    edge_spec = {
        "source": args.source,
        "target": args.target,
        "label": args.label,
        "edge_status": args.status,
        "justification": args.justification,
        "why_forced": args.why_forced,
    }
    if args.update:
        additions_io.update_edge(edge_spec)
        action = "updated in additions.yaml"
    else:
        appended = additions_io.append_edge(edge_spec)
        if not appended:
            print(f"edge already in additions.yaml: {args.source} → {args.target} : {args.label}")
            print("use --update to overwrite")
            return
        action = "appended to additions.yaml"

    # Apply to live DB (idempotent: delete-by-key + create)
    conn.execute(
        """
        MATCH (a:Node {id: $src})-[e:Edge]->(b:Node {id: $tgt})
        WHERE e.label = $lbl
        DELETE e
        """,
        {"src": args.source, "tgt": args.target, "lbl": args.label},
    )
    conn.execute(
        """
        MATCH (a:Node {id: $src}), (b:Node {id: $tgt})
        CREATE (a)-[:Edge {
            label: $lbl, edge_status: $st,
            justification: $j, why_forced: $w
        }]->(b)
        """,
        {
            "src": args.source, "tgt": args.target, "lbl": args.label,
            "st": args.status, "j": args.justification, "w": args.why_forced,
        },
    )
    print(f"edge {action} and applied to DB:")
    print(f"  {args.source} → {args.target}  :  {args.label}  [{args.status}]")
    print("→ remember to commit additions.yaml")


if __name__ == "__main__":
    main()
