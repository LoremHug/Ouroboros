#!/usr/bin/env python3
"""Generate graph.min.txt — minified whole-graph dump for AI consumption.

Not a human visual (that is web/index.html). This is the bare merged
structure (manifold_graph.txt ⊕ additions.yaml, resolved through the DB):
every node with status + one-line claim, every edge as adjacency, grouped
by layer. One read = the whole graph at scale.

Build artifact, regenerated from manifold.kuzu. Run after migrate.py.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scripts.db import connect  # noqa: E402

OUT = ROOT / "graph.min.txt"
ST = {"DEMONSTRATED": "D", "STRONG": "S", "CONDITIONAL": "C",
      "OPERATIONAL": "O", "STUB": "·"}
ES = {"D": "D", "S": "S"}
SUMMARY_MAX = 78

_REPL = {
    r"\\to\b": "->", r"\\rightarrow\b": "->", r"\\Rightarrow\b": "=>",
    r"\\geq\b": ">=", r"\\leq\b": "<=", r"\\neq\b": "!=", r"\\approx\b": "~",
    r"\\times\b": "x", r"\\cdot\b": ".", r"\\pm\b": "+/-", r"\\equiv\b": "==",
    r"\\alpha\b": "alpha", r"\\beta\b": "beta", r"\\eta\b": "eta",
    r"\\delta\b": "delta", r"\\Delta\b": "Delta", r"\\pi\b": "pi",
    r"\\sqrt\b": "sqrt", r"\\infty\b": "inf", r"\\sum\b": "sum",
    r"\\partial\b": "d", r"\\nabla\b": "grad",
    r"\\langle\b": "<", r"\\rangle\b": ">", r"\\,": " ", r"\\;": " ",
    r"\\Omega\b": "Omega", r"\\omega\b": "omega", r"\\Gamma\b": "Gamma",
    r"\\gamma\b": "gamma", r"\\lambda\b": "lambda", r"\\mu\b": "mu",
    r"\\nu\b": "nu", r"\\rho\b": "rho", r"\\sigma\b": "sigma",
    r"\\Sigma\b": "Sigma", r"\\phi\b": "phi", r"\\Phi\b": "Phi",
    r"\\psi\b": "psi", r"\\Psi\b": "Psi", r"\\theta\b": "theta",
    r"\\Theta\b": "Theta", r"\\tau\b": "tau", r"\\kappa\b": "kappa",
    r"\\xi\b": "xi", r"\\zeta\b": "zeta", r"\\chi\b": "chi", r"\\ell\b": "l",
}


def delatex(s: str) -> str:
    """Strip LaTeX noise, keep readable plain text."""
    s = s or ""
    s = re.sub(r"\\(label|ref|eqref|cite|footnote)\{[^}]*\}", "", s)
    s = re.sub(
        r"\\(emph|textbf|textit|text|mathbb|mathrm|mathcal|mathsf|mathit|"
        r"operatorname|boldsymbol|mathfrak)\s*\{([^{}]*)\}",
        r"\2", s,
    )
    for k, v in _REPL.items():
        s = re.sub(k, v, s)
    s = s.replace("_{", "_").replace("^{", "^")
    s = re.sub(r"\\[A-Za-z]+", "", s)        # leftover no-arg commands
    s = s.replace("$", "").replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", s).strip()


def squash(s: str, n: int = SUMMARY_MAX) -> str:
    """De-LaTeX + collapse + truncate at a word boundary."""
    s = delatex(s)
    if len(s) <= n:
        return s
    return s[:n].rsplit(" ", 1)[0] + "…"


def main() -> None:
    _db, conn = connect()

    nodes: dict[str, dict] = {}
    r = conn.execute(
        "MATCH (n:Node) RETURN n.id, n.layer, n.status, n.summary, "
        "n.anchors, n.is_placeholder ORDER BY n.id"
    )
    while r.has_next():
        nid, layer, status, summary, anchors, ph = r.get_next()
        nodes[nid] = {
            "layer": layer or "?", "status": status or "STUB",
            "summary": squash(summary), "anchors": anchors or 0,
            "ph": bool(ph), "out": [],
        }

    n_edges = 0
    r = conn.execute(
        "MATCH (a:Node)-[e:Edge]->(b:Node) "
        "RETURN a.id, b.id, e.label, e.edge_status ORDER BY a.id, b.id, e.label"
    )
    while r.has_next():
        src, tgt, label, est = r.get_next()
        if src in nodes:
            nodes[src]["out"].append((tgt, label or "", ES.get(est, est or "D")))
            n_edges += 1

    # status / layer tallies
    from collections import Counter
    sc, lc = Counter(), Counter()
    for d in nodes.values():
        sc[d["status"]] += 1
        lc[d["layer"]] += 1

    lines: list[str] = []
    A = lines.append
    A("# OUROBOROS — minified graph (AI dump; bare merged structure, not a visual).")
    A(f"# nodes={len(nodes)} edges={n_edges}")
    A("# status: D=DEMONSTRATED S=STRONG C=CONDITIONAL O=OPERATIONAL ·=STUB")
    A("# counts: " + " ".join(f"{ST.get(k,k)}={v}" for k, v in sc.most_common()))
    A("# layers: " + " ".join(f"{k}={v}" for k, v in lc.most_common()))
    A("# line:  ID[status] (A=anchors) summary  >>  tgt:label[edge_status] | ...")
    A("#")

    # group by layer (stable order), nodes by id within
    layer_order = [k for k, _ in lc.most_common()]
    for layer in layer_order:
        A(f"## {layer}")
        for nid in sorted(k for k, d in nodes.items() if d["layer"] == layer):
            d = nodes[nid]
            st = ST.get(d["status"], "?")
            tag = f"{nid}[{st}]"
            if d["anchors"]:
                tag += f"(A{d['anchors']})"
            if d["ph"]:
                tag += "(stub)"
            head = f"{tag} {d['summary']}".rstrip()
            if d["out"]:
                edges = " | ".join(f"{t}:{lbl}[{es}]" for t, lbl, es in d["out"])
                A(f"{head}  >>  {edges}")
            else:
                A(head)
        A("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote → {OUT}")
    print(f"  {len(nodes)} nodes, {n_edges} edges, {len(lines)} lines, "
          f"{OUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
