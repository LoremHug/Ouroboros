"""Read/write additions.yaml — post-migration source of truth for new edges/nodes.

Format (also documented at top of additions.yaml itself):
    edges: [{source, target, label, edge_status, justification, why_forced}]
    nodes: [{id, title, layer, status, anchors, a_infinity, summary,
             why_status, is_placeholder, content}]
"""
from __future__ import annotations
from pathlib import Path
from typing import Any
import yaml

ROOT = Path(__file__).resolve().parent.parent
ADDITIONS_FILE = ROOT / "additions.yaml"


def _split_docstring(text: str) -> tuple[str, str]:
    """Strip the leading triple-quoted docstring (if any) so YAML loads cleanly."""
    s = text.lstrip()
    if not s.startswith('"""'):
        return "", text
    end = s.find('"""', 3)
    if end == -1:
        return "", text
    docstring = s[3:end]
    rest = s[end + 3:]
    return docstring, rest


def load() -> dict[str, list[dict[str, Any]]]:
    if not ADDITIONS_FILE.exists():
        return {"edges": [], "nodes": []}
    raw = ADDITIONS_FILE.read_text(encoding="utf-8")
    _, body = _split_docstring(raw)
    data = yaml.safe_load(body) or {}
    return {
        "edges": data.get("edges") or [],
        "nodes": data.get("nodes") or [],
    }


def save(data: dict[str, list[dict[str, Any]]]) -> None:
    """Preserve the leading docstring; rewrite YAML body."""
    raw = ADDITIONS_FILE.read_text(encoding="utf-8") if ADDITIONS_FILE.exists() else ""
    docstring, _ = _split_docstring(raw)
    body = yaml.safe_dump(
        {"edges": data.get("edges") or [], "nodes": data.get("nodes") or []},
        sort_keys=False, allow_unicode=True, width=88, default_flow_style=False,
    )
    if docstring:
        out = f'"""{docstring}"""\n\n{body}'
    else:
        out = body
    ADDITIONS_FILE.write_text(out, encoding="utf-8")


def append_edge(edge: dict[str, Any]) -> bool:
    """Append edge if (source, target, label) is new. Returns True if appended."""
    data = load()
    key = (edge["source"], edge["target"], edge.get("label", ""))
    for e in data["edges"]:
        if (e["source"], e["target"], e.get("label", "")) == key:
            return False
    data["edges"].append(edge)
    save(data)
    return True


def update_edge(edge: dict[str, Any]) -> None:
    """Insert or overwrite by (source, target, label)."""
    data = load()
    key = (edge["source"], edge["target"], edge.get("label", ""))
    for i, e in enumerate(data["edges"]):
        if (e["source"], e["target"], e.get("label", "")) == key:
            data["edges"][i] = edge
            save(data)
            return
    data["edges"].append(edge)
    save(data)


def upsert_node(node: dict[str, Any]) -> None:
    data = load()
    for i, n in enumerate(data["nodes"]):
        if n["id"] == node["id"]:
            merged = {**n, **node}
            data["nodes"][i] = merged
            save(data)
            return
    data["nodes"].append(node)
    save(data)
