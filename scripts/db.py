"""Kuzu DB connection and schema bootstrap."""
from __future__ import annotations
import kuzu
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "manifold.kuzu"


def connect(create_if_missing: bool = True) -> tuple[kuzu.Database, kuzu.Connection]:
    db = kuzu.Database(str(DB_PATH))
    conn = kuzu.Connection(db)
    if create_if_missing:
        bootstrap_schema(conn)
    return db, conn


def bootstrap_schema(conn: kuzu.Connection) -> None:
    """Create node/edge tables if missing. Idempotent."""
    conn.execute("""
        CREATE NODE TABLE IF NOT EXISTS Node(
            id STRING PRIMARY KEY,
            title STRING,
            layer STRING,
            status STRING,
            anchors INT64,
            a_infinity BOOLEAN,
            summary STRING,
            why_status STRING,
            not_misinterpretations STRING,
            content STRING,
            z_struct DOUBLE,
            z_therm DOUBLE,
            z_hidden DOUBLE,
            level INT64,
            is_placeholder BOOLEAN,
            aliases STRING
        )
    """)
    conn.execute("""
        CREATE REL TABLE IF NOT EXISTS Edge(
            FROM Node TO Node,
            label STRING,
            edge_status STRING,
            justification STRING,
            why_forced STRING
        )
    """)


def reset() -> None:
    """Delete the entire DB. Use only for clean re-migration."""
    import shutil
    if DB_PATH.exists():
        if DB_PATH.is_dir():
            shutil.rmtree(DB_PATH)
        else:
            DB_PATH.unlink()
    # Kuzu may also leave WAL/SHM sidecar files
    for suffix in (".wal", ".shm", ".tmp"):
        side = DB_PATH.with_suffix(DB_PATH.suffix + suffix)
        if side.exists():
            side.unlink()


if __name__ == "__main__":
    db, conn = connect()
    res = conn.execute("MATCH (n:Node) RETURN count(n)")
    print("nodes:", res.get_next()[0])
    res = conn.execute("MATCH ()-[e:Edge]->() RETURN count(e)")
    print("edges:", res.get_next()[0])
