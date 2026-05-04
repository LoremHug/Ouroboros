"""Add or update a node: persist to additions.yaml AND apply to local Kuzu DB.

Usage:
    python -m scripts.add_node N_NewName \\
        --layer observers --status STRONG --anchors 3 \\
        --title "Some Forced Identification" \\
        --summary "One-line claim" \\
        --why-status "Why DEMONSTRATED/STRONG/CONDITIONAL applies" \\
        --not-misinterpretations "Common misreadings" \\
        --content "Full structural argument..."
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from schema import Status, Layer, layer_of  # noqa: E402
from scripts.db import connect  # noqa: E402
from scripts import additions as additions_io  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("id")
    p.add_argument("--title")
    p.add_argument("--layer", choices=[l.value for l in Layer])
    p.add_argument("--status", choices=[s.value for s in Status])
    p.add_argument("--anchors", type=int)
    p.add_argument("--a-infinity", action="store_true", default=None)
    p.add_argument("--summary")
    p.add_argument("--why-status")
    p.add_argument("--not-misinterpretations")
    p.add_argument("--content")
    p.add_argument("--z-struct", type=float)
    p.add_argument("--z-therm", type=float)
    p.add_argument("--z-hidden", type=float)
    p.add_argument("--level", type=int)
    p.add_argument("--placeholder", action="store_true", default=None,
                   help="mark as is_placeholder")
    args = p.parse_args()

    field_map = {
        "title": args.title, "layer": args.layer, "status": args.status,
        "anchors": args.anchors, "a_infinity": args.a_infinity,
        "summary": args.summary, "why_status": args.why_status,
        "not_misinterpretations": args.not_misinterpretations,
        "content": args.content,
        "z_struct": args.z_struct, "z_therm": args.z_therm,
        "z_hidden": args.z_hidden, "level": args.level,
        "is_placeholder": args.placeholder,
    }
    spec = {"id": args.id}
    spec.update({k: v for k, v in field_map.items() if v is not None})
    if "layer" not in spec:
        spec["layer"] = layer_of(args.id).value

    additions_io.upsert_node(spec)

    db, conn = connect()
    res = conn.execute("MATCH (n:Node {id: $id}) RETURN count(n)", {"id": args.id})
    exists = res.get_next()[0] > 0

    if exists:
        sets = []
        params = {"id": args.id}
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
            print(f"updated in DB and additions.yaml: {args.id}")
        else:
            print(f"no-op: {args.id} (no fields)")
    else:
        defaults = {
            "title": "", "layer": layer_of(args.id).value, "status": Status.STUB.value,
            "anchors": 0, "a_infinity": False, "summary": "", "why_status": "",
            "not_misinterpretations": "", "content": "",
            "z_struct": 0.0, "z_therm": 0.0, "z_hidden": 0.0, "level": -1,
            "is_placeholder": False,
        }
        defaults.update({k: v for k, v in field_map.items() if v is not None})
        defaults["id"] = args.id
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
        print(f"created in DB and additions.yaml: {args.id}")
    print("→ remember to commit additions.yaml")


if __name__ == "__main__":
    main()
