"""Read Kuzu DB → generate self-contained map.html with embedded data.

Click on node/edge opens a side panel with full content from DB.
Style adapted from user's D3 reference (JetBrains Mono + Syne, dark theme,
layered colors, glow on core nodes).
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.db import connect  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "web" / "map.html"


def fetch_data() -> dict:
    db, conn = connect()
    nodes = []
    res = conn.execute("""
        MATCH (n:Node)
        RETURN n.id, n.title, n.layer, n.status, n.anchors, n.a_infinity,
               n.summary, n.why_status, n.not_misinterpretations,
               n.content, n.z_struct, n.z_therm, n.z_hidden, n.level,
               n.is_placeholder
    """)
    while res.has_next():
        row = res.get_next()
        nodes.append({
            "id": row[0], "title": row[1], "layer": row[2],
            "status": row[3], "anchors": row[4], "a_infinity": row[5],
            "summary": row[6],
            "why_status": row[7],
            "not_misinterpretations": row[8],
            "content": row[9],
            "z_struct": row[10], "z_therm": row[11], "z_hidden": row[12],
            "level": row[13], "is_placeholder": row[14],
        })

    edges = []
    res = conn.execute("""
        MATCH (a:Node)-[e:Edge]->(b:Node)
        RETURN a.id, b.id, e.label, e.edge_status, e.justification, e.why_forced
    """)
    while res.has_next():
        row = res.get_next()
        edges.append({
            "source": row[0], "target": row[1], "label": row[2],
            "edge_status": row[3], "justification": row[4],
            "why_forced": row[5],
        })

    # Compute degree
    deg: dict[str, int] = {}
    for e in edges:
        deg[e["source"]] = deg.get(e["source"], 0) + 1
        deg[e["target"]] = deg.get(e["target"], 0) + 1
    for n in nodes:
        n["degree"] = deg.get(n["id"], 0)

    # DESCRIBED_BY: node → list of section labels
    # Section table may not exist yet (if enrich_from_tex hasn't run)
    sections_by_node: dict[str, list[dict]] = {n["id"]: [] for n in nodes}
    sections: dict[str, dict] = {}
    try:
        res = conn.execute("""
            MATCH (n:Node)-[:DESCRIBED_BY]->(s:Section)
            RETURN n.id, s.label, s.title, s.kind
        """)
        while res.has_next():
            row = res.get_next()
            nid, lbl, title, kind = row
            sections_by_node.setdefault(nid, []).append({
                "label": lbl, "title": title, "kind": kind,
            })
        # Section bodies in separate map (for embedded lookup by label)
        res = conn.execute("MATCH (s:Section) RETURN s.label, s.title, s.kind, s.body")
        while res.has_next():
            row = res.get_next()
            sections[row[0]] = {
                "label": row[0], "title": row[1], "kind": row[2], "body": row[3],
            }
    except Exception:
        pass  # Section table not yet created

    for n in nodes:
        n["sections"] = sections_by_node.get(n["id"], [])

    return {"nodes": nodes, "edges": edges, "sections": sections}


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ouroboros — Manifold Graph</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600&family=Syne:wght@400;700;800&display=swap');

:root {
  --bg: #080b0f; --surface: #0d1117;
  --core: #e8c547; --structure: #4fa3e0; --epistemics: #e05c4f;
  --observers: #6bcf8f; --physics: #a78bfa; --comms: #f59e42; --numeric: #64748b;
  --text: #e2e8f0; --muted: #64748b;
  --status-DEMONSTRATED: #1B7F3A; --status-STRONG: #1A5E9E;
  --status-CONDITIONAL: #B25A00; --status-OPERATIONAL: #5B4A9E;
  --status-STUB: #4a4a4a;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: var(--bg); color: var(--text);
  font-family: 'JetBrains Mono', monospace; overflow: hidden;
  width: 100vw; height: 100vh;
}
#canvas { width: 100%; height: 100%; }

#title {
  position: fixed; top: 24px; right: 24px; text-align: right; z-index: 10;
}
#title h1 {
  font-family: 'Syne', sans-serif; font-size: 18px; font-weight: 800;
  letter-spacing: 0.05em;
}
#title p {
  font-size: 10px; letter-spacing: 0.15em; color: var(--muted);
  text-transform: uppercase; margin-top: 4px;
}

#legend {
  position: fixed; top: 24px; left: 24px; background: rgba(13,17,23,0.92);
  border: 1px solid rgba(255,255,255,0.08); padding: 16px 20px;
  backdrop-filter: blur(12px); z-index: 10; min-width: 220px;
}
#legend h3 {
  font-family: 'Syne', sans-serif; font-size: 10px; font-weight: 700;
  letter-spacing: 0.2em; text-transform: uppercase; color: var(--muted);
  margin-bottom: 12px;
}
.legend-item {
  display: flex; align-items: center; justify-content: space-between;
  gap: 10px; margin-bottom: 7px; font-size: 11px; color: var(--muted);
  cursor: pointer; transition: color 0.2s;
}
.legend-item:hover { color: var(--text); }
.legend-item.active { color: var(--text); }
.legend-left { display: flex; align-items: center; gap: 10px; }
.legend-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.legend-count { color: var(--muted); font-size: 10px; }

#search {
  position: fixed; top: 24px; left: 50%; transform: translateX(-50%);
  background: rgba(13,17,23,0.92); border: 1px solid rgba(255,255,255,0.08);
  padding: 10px 16px; backdrop-filter: blur(12px); z-index: 10;
}
#search input {
  background: transparent; border: none; outline: none; color: var(--text);
  font-family: 'JetBrains Mono', monospace; font-size: 12px; width: 280px;
}
#search input::placeholder { color: var(--muted); }

#info {
  position: fixed; bottom: 24px; left: 24px;
  font-size: 10px; color: var(--muted); letter-spacing: 0.08em;
}

#stats {
  position: fixed; bottom: 24px; right: 24px;
  font-size: 10px; color: var(--muted); letter-spacing: 0.08em; text-align: right;
}

#tooltip {
  position: fixed; background: rgba(13,17,23,0.97);
  border: 1px solid rgba(255,255,255,0.12); padding: 10px 14px;
  font-size: 11px; pointer-events: none; opacity: 0;
  transition: opacity 0.15s; max-width: 240px; line-height: 1.5; z-index: 100;
}
#tooltip .t-name { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 13px; margin-bottom: 4px; }
#tooltip .t-meta { font-size: 9px; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); }

#panel {
  position: fixed; top: 0; right: 0; width: 480px; height: 100vh;
  background: rgba(13,17,23,0.97); border-left: 1px solid rgba(255,255,255,0.08);
  backdrop-filter: blur(20px); padding: 32px; overflow-y: auto;
  transform: translateX(520px); transition: transform 0.25s ease-out; z-index: 50;
}
#panel.open { transform: translateX(0); }
#panel .close {
  position: absolute; top: 16px; right: 16px; cursor: pointer;
  width: 28px; height: 28px; display: flex; align-items: center;
  justify-content: center; color: var(--muted); font-size: 18px;
  border: 1px solid rgba(255,255,255,0.08);
}
#panel .close:hover { color: var(--text); }
#panel .p-id {
  font-family: 'Syne', sans-serif; font-size: 22px; font-weight: 800;
  letter-spacing: 0.02em; margin-bottom: 4px; word-break: break-all;
}
#panel .p-title { font-size: 12px; color: var(--muted); margin-bottom: 16px; line-height: 1.5; }
#panel .badges { display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
.badge {
  font-size: 9px; letter-spacing: 0.15em; padding: 4px 10px;
  text-transform: uppercase; border: 1px solid currentColor;
}
#panel .section { margin-top: 24px; }
#panel .section-title {
  font-family: 'Syne', sans-serif; font-size: 9px; font-weight: 700;
  letter-spacing: 0.25em; text-transform: uppercase; color: var(--muted);
  margin-bottom: 8px;
}
#panel .content {
  font-size: 11px; line-height: 1.7; white-space: pre-wrap;
  word-break: break-word; color: var(--text); opacity: 0.85;
  font-family: 'JetBrains Mono', monospace;
}
#panel .edge-list { display: flex; flex-direction: column; gap: 6px; }
#panel .edge-item {
  display: flex; align-items: center; gap: 8px; font-size: 11px;
  padding: 6px 8px; border: 1px solid rgba(255,255,255,0.05); cursor: pointer;
}
#panel .edge-item:hover { background: rgba(255,255,255,0.03); }
#panel .edge-arrow { color: var(--muted); font-size: 10px; }
#panel .edge-label { color: var(--muted); font-size: 10px; margin-left: auto; }

.node circle { cursor: pointer; transition: r 0.2s, opacity 0.2s; }
.node text { pointer-events: none; font-family: 'JetBrains Mono', monospace; }
line.link { cursor: pointer; }
line.link:hover { stroke-opacity: 1 !important; }

.dimmed { opacity: 0.1 !important; }
</style>
</head>
<body>

<div id="title">
  <h1>Ouroboros</h1>
  <p>Manifold Graph · live</p>
</div>

<div id="search">
  <input type="text" placeholder="search node id or title…" id="search-input">
</div>

<div id="legend"><h3>Layers</h3><div id="legend-items"></div></div>

<div id="tooltip">
  <div class="t-name" id="t-name"></div>
  <div class="t-meta" id="t-meta"></div>
</div>

<div id="panel">
  <div class="close" onclick="closePanel()">×</div>
  <div id="panel-content"></div>
</div>

<div id="info">scroll → zoom · drag → pan · click node/edge → details · click legend → filter · esc → close</div>
<div id="stats" id="stats-text"></div>

<svg id="canvas"></svg>

<script>
// ─────────────────────────────────────────── DATA (embedded by generator)
const DATA = __DATA__;

const LAYER_COLORS = {
  core: '#e8c547', structure: '#4fa3e0', epistemics: '#e05c4f',
  observers: '#6bcf8f', physics: '#a78bfa', comms: '#f59e42', numeric: '#64748b',
};
const LAYER_ORDER = ['core', 'structure', 'epistemics', 'observers', 'physics', 'comms', 'numeric'];

// Index lookups
const nodeById = new Map(DATA.nodes.map(n => [n.id, n]));
const edgesByNode = new Map();
DATA.nodes.forEach(n => edgesByNode.set(n.id, []));
DATA.edges.forEach(e => {
  edgesByNode.get(e.source)?.push(e);
  edgesByNode.get(e.target)?.push(e);
});

// ─────────────────────────────────────────── LAYOUT
const W = window.innerWidth, H = window.innerHeight;
const svg = d3.select('#canvas').attr('width', W).attr('height', H);
const zoomG = svg.append('g');
svg.call(d3.zoom().scaleExtent([0.15, 6]).on('zoom', e => zoomG.attr('transform', e.transform)));

const defs = svg.append('defs');
const glow = defs.append('filter').attr('id', 'glow');
glow.append('feGaussianBlur').attr('stdDeviation', '3').attr('result', 'blur');
const fm = glow.append('feMerge');
fm.append('feMergeNode').attr('in', 'blur');
fm.append('feMergeNode').attr('in', 'SourceGraphic');

function nodeRadius(n) {
  if (n.layer === 'core') return 14 + Math.min(n.degree, 12);
  if (n.layer === 'numeric') return 5;
  return 8 + Math.min(n.degree * 0.6, 8);
}

const sim = d3.forceSimulation(DATA.nodes)
  .force('link', d3.forceLink(DATA.edges).id(d => d.id).distance(d => {
    const sl = (typeof d.source === 'object' ? d.source.layer : nodeById.get(d.source).layer);
    const tl = (typeof d.target === 'object' ? d.target.layer : nodeById.get(d.target).layer);
    if (sl === 'core' && tl === 'core') return 60;
    if (sl === 'core' || tl === 'core') return 100;
    if (sl === 'numeric' || tl === 'numeric') return 70;
    return 130;
  }).strength(0.4))
  .force('charge', d3.forceManyBody().strength(d =>
    d.layer === 'core' ? -900 : d.layer === 'numeric' ? -90 : -350))
  .force('center', d3.forceCenter(W / 2, H / 2))
  .force('collision', d3.forceCollide().radius(d => nodeRadius(d) + 6));

const link = zoomG.append('g').selectAll('line')
  .data(DATA.edges).join('line')
  .attr('class', 'link')
  .attr('stroke', d => {
    const sl = nodeById.get(d.source.id || d.source).layer;
    const tl = nodeById.get(d.target.id || d.target).layer;
    return (sl === 'core' || tl === 'core') ? 'rgba(255,255,255,0.18)' : 'rgba(255,255,255,0.06)';
  })
  .attr('stroke-width', d => {
    const sl = nodeById.get(d.source.id || d.source).layer;
    const tl = nodeById.get(d.target.id || d.target).layer;
    return (sl === 'core' && tl === 'core') ? 1.5 : 0.8;
  })
  .on('click', (e, d) => { e.stopPropagation(); openEdgePanel(d); });

const node = zoomG.append('g').selectAll('g')
  .data(DATA.nodes).join('g')
  .attr('class', 'node')
  .call(d3.drag()
    .on('start', (e, d) => { if (!e.active) sim.alphaTarget(0.2).restart(); d.fx = d.x; d.fy = d.y; })
    .on('drag', (e, d) => { d.fx = e.x; d.fy = e.y; })
    .on('end', (e, d) => { if (!e.active) sim.alphaTarget(0); }));

node.append('circle')
  .attr('r', nodeRadius)
  .attr('fill', d => d.is_placeholder ? 'transparent' : LAYER_COLORS[d.layer] + (d.layer === 'numeric' ? '55' : 'cc'))
  .attr('stroke', d => LAYER_COLORS[d.layer])
  .attr('stroke-width', d => d.layer === 'core' ? 2 : 1)
  .attr('stroke-dasharray', d => d.is_placeholder ? '3,3' : null)
  .attr('filter', d => d.layer === 'core' ? 'url(#glow)' : null);

node.filter(d => d.layer !== 'numeric' || d.id === 'DEF')
  .append('text')
  .text(d => d.id.replace('N_', ''))
  .attr('dy', d => -nodeRadius(d) - 4)
  .attr('text-anchor', 'middle')
  .attr('font-size', d => d.layer === 'core' ? 11 : 9)
  .attr('font-weight', d => d.layer === 'core' ? 600 : 300)
  .attr('fill', d => d.layer === 'core' ? LAYER_COLORS[d.layer] : LAYER_COLORS[d.layer] + 'cc')
  .attr('letter-spacing', '0.04em');

node.on('click', (e, d) => { e.stopPropagation(); openNodePanel(d); });

// Tooltip
const tooltip = document.getElementById('tooltip');
const tName = document.getElementById('t-name');
const tMeta = document.getElementById('t-meta');
node.on('mouseover', (e, d) => {
  tooltip.style.opacity = '1';
  tName.textContent = d.id;
  tName.style.color = LAYER_COLORS[d.layer];
  const adj = edgesByNode.get(d.id)?.length || 0;
  tMeta.textContent = `${d.layer.toUpperCase()} · ${d.status} · A=${d.a_infinity ? '∞' : d.anchors} · deg ${adj}`;
  tooltip.style.left = (e.clientX + 14) + 'px';
  tooltip.style.top = (e.clientY - 10) + 'px';
  highlightConnected(d);
}).on('mousemove', e => {
  tooltip.style.left = (e.clientX + 14) + 'px';
  tooltip.style.top = (e.clientY - 10) + 'px';
}).on('mouseout', () => {
  tooltip.style.opacity = '0';
  resetHighlight();
});

function highlightConnected(d) {
  link.classed('dimmed', l => !(l.source === d || l.target === d || l.source.id === d.id || l.target.id === d.id));
  node.classed('dimmed', n => {
    if (n === d) return false;
    return !DATA.edges.some(l =>
      ((l.source.id || l.source) === d.id && (l.target.id || l.target) === n.id) ||
      ((l.target.id || l.target) === d.id && (l.source.id || l.source) === n.id));
  });
}
function resetHighlight() {
  link.classed('dimmed', false);
  node.classed('dimmed', false);
}

// ─────────────────────────────────────────── PANEL
const panel = document.getElementById('panel');
const panelContent = document.getElementById('panel-content');

function statusColor(s) {
  return ({ DEMONSTRATED: '#1B7F3A', STRONG: '#1A5E9E', CONDITIONAL: '#B25A00',
            OPERATIONAL: '#5B4A9E', STUB: '#4a4a4a' })[s] || '#4a4a4a';
}

function escapeHtml(s) {
  if (!s) return '';
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function openNodePanel(d) {
  const adj = edgesByNode.get(d.id) || [];
  const out = adj.filter(e => (e.source.id || e.source) === d.id);
  const inE = adj.filter(e => (e.target.id || e.target) === d.id);
  const sc = statusColor(d.status);
  const layerColor = LAYER_COLORS[d.layer];

  panelContent.innerHTML = `
    <div class="p-id" style="color:${layerColor}">${escapeHtml(d.id)}</div>
    <div class="p-title">${escapeHtml(d.title || '—')}</div>
    <div class="badges">
      <span class="badge" style="color:${layerColor}">${d.layer}</span>
      <span class="badge" style="color:${sc}">${d.status}</span>
      <span class="badge" style="color:#64748b">A = ${d.a_infinity ? '∞' : d.anchors}</span>
      <span class="badge" style="color:#64748b">deg ${adj.length}</span>
      ${d.is_placeholder ? '<span class="badge" style="color:#B25A00">PLACEHOLDER</span>' : ''}
    </div>
    ${d.summary ? `<div class="section"><div class="section-title">Claim</div><div class="content">${escapeHtml(d.summary)}</div></div>` : ''}
    ${d.why_status ? `<div class="section"><div class="section-title">Why ${escapeHtml(d.status)}</div><div class="content">${escapeHtml(d.why_status)}</div></div>` : ''}
    ${d.not_misinterpretations ? `<div class="section"><div class="section-title">NOT (common misinterpretations)</div><div class="content">${escapeHtml(d.not_misinterpretations)}</div></div>` : ''}
    ${out.length ? `<div class="section"><div class="section-title">Outgoing → (${out.length})</div><div class="edge-list">${out.map(e => renderEdgeItem(e, 'out')).join('')}</div></div>` : ''}
    ${inE.length ? `<div class="section"><div class="section-title">← Incoming (${inE.length})</div><div class="edge-list">${inE.map(e => renderEdgeItem(e, 'in')).join('')}</div></div>` : ''}
    ${d.sections && d.sections.length ? `<div class="section"><div class="section-title">.tex sections (${d.sections.length})</div><div class="edge-list">${d.sections.map(s => `<div class="edge-item" onclick='openSectionPanel(${JSON.stringify(s.label)})'><span class="edge-arrow">§</span><span>${escapeHtml(s.title)}</span><span class="edge-label">${escapeHtml(s.label)}</span></div>`).join('')}</div></div>` : ''}
    ${d.content ? `<div class="section"><div class="section-title">Free body</div><div class="content">${escapeHtml(d.content)}</div></div>` : ''}
  `;
  panel.classList.add('open');
}

function renderEdgeItem(e, dir) {
  const otherId = dir === 'out' ? (e.target.id || e.target) : (e.source.id || e.source);
  const other = nodeById.get(otherId);
  const arrow = dir === 'out' ? '→' : '←';
  const color = other ? LAYER_COLORS[other.layer] : '#64748b';
  return `<div class="edge-item" onclick='focusNode(${JSON.stringify(otherId)})'>
    <span class="edge-arrow">${arrow}</span>
    <span style="color:${color}">${escapeHtml(otherId)}</span>
    <span class="edge-label">${escapeHtml(e.label || '—')}</span>
  </div>`;
}

function openEdgePanel(e) {
  const src = nodeById.get(e.source.id || e.source);
  const tgt = nodeById.get(e.target.id || e.target);
  panelContent.innerHTML = `
    <div class="p-id">edge</div>
    <div class="p-title">${escapeHtml(e.label || '—')}</div>
    <div class="badges">
      <span class="badge" style="color:#64748b">[${e.edge_status}]</span>
    </div>
    <div class="section">
      <div class="section-title">Source</div>
      <div class="edge-item" onclick='focusNode(${JSON.stringify(src.id)})'>
        <span style="color:${LAYER_COLORS[src.layer]}">${escapeHtml(src.id)}</span>
        <span class="edge-label">${escapeHtml(src.title)}</span>
      </div>
    </div>
    <div class="section">
      <div class="section-title">Target</div>
      <div class="edge-item" onclick='focusNode(${JSON.stringify(tgt.id)})'>
        <span style="color:${LAYER_COLORS[tgt.layer]}">${escapeHtml(tgt.id)}</span>
        <span class="edge-label">${escapeHtml(tgt.title)}</span>
      </div>
    </div>
    ${e.justification ? `<div class="section"><div class="section-title">Justification</div><div class="content">${escapeHtml(e.justification)}</div></div>` : ''}
    ${e.why_forced ? `<div class="section"><div class="section-title">Why forced</div><div class="content">${escapeHtml(e.why_forced)}</div></div>` : ''}
    ${(!e.justification && !e.why_forced) ? '<div class="section"><div class="content" style="color:#64748b">No justification recorded yet. This edge needs a why_forced argument.</div></div>' : ''}
  `;
  panel.classList.add('open');
}

function closePanel() { panel.classList.remove('open'); }
function focusNode(id) {
  const n = nodeById.get(id);
  if (n) openNodePanel(n);
}
function openSectionPanel(label) {
  const s = DATA.sections[label];
  if (!s) return;
  // Find linked nodes
  const linked = DATA.nodes.filter(n => (n.sections || []).some(x => x.label === label));
  panelContent.innerHTML = `
    <div class="p-id" style="color:#a78bfa">§ ${escapeHtml(s.label)}</div>
    <div class="p-title">${escapeHtml(s.title)}</div>
    <div class="badges">
      <span class="badge" style="color:#a78bfa">${s.kind}</span>
    </div>
    ${linked.length ? `<div class="section"><div class="section-title">Linked nodes (${linked.length})</div><div class="edge-list">${linked.map(n => `<div class="edge-item" onclick='focusNode(${JSON.stringify(n.id)})'><span style="color:${LAYER_COLORS[n.layer]}">${escapeHtml(n.id)}</span><span class="edge-label">${escapeHtml(n.title || '')}</span></div>`).join('')}</div></div>` : ''}
    ${s.body ? `<div class="section"><div class="section-title">Section text</div><div class="content">${escapeHtml(s.body)}</div></div>` : ''}
  `;
  panel.classList.add('open');
}
window.focusNode = focusNode;
window.closePanel = closePanel;
window.openSectionPanel = openSectionPanel;

document.addEventListener('keydown', e => { if (e.key === 'Escape') closePanel(); });
svg.on('click', () => closePanel());

// ─────────────────────────────────────────── LEGEND
const legendItems = document.getElementById('legend-items');
const layerCounts = {};
DATA.nodes.forEach(n => layerCounts[n.layer] = (layerCounts[n.layer] || 0) + 1);
const activeFilters = new Set();
LAYER_ORDER.forEach(layer => {
  const item = document.createElement('div');
  item.className = 'legend-item';
  item.dataset.layer = layer;
  item.innerHTML = `<div class="legend-left"><div class="legend-dot" style="background:${LAYER_COLORS[layer]}"></div>${layer}</div><span class="legend-count">${layerCounts[layer] || 0}</span>`;
  item.onclick = () => toggleLayer(layer, item);
  legendItems.appendChild(item);
});

function toggleLayer(layer, el) {
  if (activeFilters.has(layer)) {
    activeFilters.delete(layer);
    el.classList.remove('active');
  } else {
    activeFilters.add(layer);
    el.classList.add('active');
  }
  applyFilter();
}
function applyFilter() {
  if (activeFilters.size === 0) {
    node.style('display', null);
    link.style('display', null);
    return;
  }
  node.style('display', d => activeFilters.has(d.layer) ? null : 'none');
  link.style('display', d => {
    const sl = (d.source.layer || nodeById.get(d.source).layer);
    const tl = (d.target.layer || nodeById.get(d.target).layer);
    return (activeFilters.has(sl) && activeFilters.has(tl)) ? null : 'none';
  });
}

// ─────────────────────────────────────────── SEARCH
const searchInput = document.getElementById('search-input');
searchInput.addEventListener('input', e => {
  const q = e.target.value.trim().toLowerCase();
  if (!q) { resetHighlight(); return; }
  const matches = DATA.nodes.filter(n =>
    n.id.toLowerCase().includes(q) || (n.title || '').toLowerCase().includes(q));
  const matchSet = new Set(matches.map(n => n.id));
  node.classed('dimmed', n => !matchSet.has(n.id));
  link.classed('dimmed', l =>
    !(matchSet.has(l.source.id || l.source) && matchSet.has(l.target.id || l.target)));
});
searchInput.addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    const q = searchInput.value.trim().toLowerCase();
    const m = DATA.nodes.find(n =>
      n.id.toLowerCase() === q || n.id.toLowerCase().includes(q));
    if (m) openNodePanel(m);
  }
});

// ─────────────────────────────────────────── TICK
sim.on('tick', () => {
  link.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
  node.attr('transform', d => `translate(${d.x},${d.y})`);
});

// Stats
document.getElementById('stats').textContent =
  `${DATA.nodes.length} nodes · ${DATA.edges.length} edges`;
</script>
</body>
</html>
"""


def main() -> None:
    data = fetch_data()
    html = HTML_TEMPLATE.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote → {OUT}")
    print(f"  {len(data['nodes'])} nodes, {len(data['edges'])} edges")
    print(f"  open with: file://{OUT}")


if __name__ == "__main__":
    main()
