"""Add or update a node in the Kuzu DB.

Usage:
    python -m scripts.add_node N_NewName \\
        --layer observers --status STRONG --anchors 3 \\
        --title "Some Forced Identification" \\
        --summary "One-line claim" \\
        --content "Full structural argument..."
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from schema import Status, Layer, layer_of  # noqa: E402
from scripts.db import connect  # noqa: E402


def upsert(node_id: str, **kwargs) -> None:
    db, conn = connect()
    res = conn.execute("MATCH (n:Node {id: $id}) RETURN count(n)", {"id": node_id})
    exists = res.get_next()[0] > 0

    if exists:
        sets = []
        params = {"id": node_id}
        for k, v in kwargs.items():
            if v is None:
                continue
            sets.append(f"n.{k} = ${k}")
            params[k] = v
        if sets:
            conn.execute(
                f"MATCH (n:Node {{id: $id}}) SET {', '.join(sets)}",
                params,
            )
            print(f"updated: {node_id}")
        else:
            print(f"no-op: {node_id} (no fields)")
    else:
        defaults = {
            "title": "", "layer": layer_of(node_id).value, "status": Status.STUB.value,
            "anchors": 0, "a_infinity": False, "summary": "", "content": "",
            "z_struct": 0.0, "z_therm": 0.0, "z_hidden": 0.0, "level": -1,
        }
        defaults.update({k: v for k, v in kwargs.items() if v is not None})
        defaults["id"] = node_id
        conn.execute(
            """
            CREATE (n:Node {
                id: $id, title: $title, layer: $layer, status: $status,
                anchors: $anchors, a_infinity: $a_infinity,
                summary: $summary, content: $content,
                z_struct: $z_struct, z_therm: $z_therm, z_hidden: $z_hidden,
                level: $level
            })
            """,
            defaults,
        )
        print(f"created: {node_id}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("id", help="node id (e.g. N_NewThing)")
    p.add_argument("--title")
    p.add_argument("--layer", choices=[l.value for l in Layer])
    p.add_argument("--status", choices=[s.value for s in Status])
    p.add_argument("--anchors", type=int)
    p.add_argument("--a-infinity", action="store_true", default=None)
    p.add_argument("--summary")
    p.add_argument("--content")
    p.add_argument("--z-struct", type=float)
    p.add_argument("--z-therm", type=float)
    p.add_argument("--z-hidden", type=float)
    p.add_argument("--level", type=int)
    args = p.parse_args()

    fields = {k: v for k, v in vars(args).items() if k != "id" and v is not None}
    upsert(args.id, **{k.replace("-", "_"): v for k, v in fields.items()})


if __name__ == "__main__":
    main()
