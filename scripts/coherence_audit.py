#!/usr/bin/env python3
"""Coherence audit v2 — BFS in Python instead of unbounded Cypher path."""
import sys; sys.path.insert(0,'/home/user/Ouroboros')
from scripts.db import connect
from collections import Counter, defaultdict, deque

db, conn = connect()

def q(cypher, params=None):
    res = conn.execute(cypher, params or {})
    rows = []
    while res.has_next(): rows.append(res.get_next())
    return rows

def hdr(s): print(f"\n{'═'*70}\n  {s}\n{'═'*70}")

# Build adjacency once
print("Loading graph...")
adj = defaultdict(set)
edge_labels = []
for a, b, lbl in q("MATCH (a:Node)-[e:Edge]->(b:Node) RETURN a.id, b.id, e.label"):
    if a != b: adj[a].add(b); adj[b].add(a)
    edge_labels.append(lbl or '')
all_nodes = [r[0] for r in q("MATCH (n:Node) RETURN n.id")]
node_attrs = {r[0]: r for r in q("MATCH (n:Node) RETURN n.id, n.layer, n.status, n.title")}

# 1
hdr("1. BASIC COUNTS")
print(f"  Nodes: {len(all_nodes)}")
print(f"  Edges (directed records): {len(edge_labels)}")
u_edges = sum(len(s) for s in adj.values()) // 2
print(f"  Edges (undirected unique): {u_edges}")
print("\n  Status:")
for k,v in Counter(node_attrs[n][2] for n in all_nodes).most_common():
    print(f"    {k or 'null':<15} {v}")
print("\n  Layer:")
for k,v in Counter(node_attrs[n][1] for n in all_nodes).most_common():
    print(f"    {k or 'null':<15} {v}")

# 2 — connectivity via BFS from DEF
hdr("2. CONNECTIVITY")
orphans = [n for n in all_nodes if not adj[n]]
print(f"  Orphans (no edges): {len(orphans)}")
for n in orphans[:10]: print(f"    {n}")

# BFS from DEF
visited = set(); q_def = deque(['DEF']); visited.add('DEF')
while q_def:
    x = q_def.popleft()
    for y in adj[x]:
        if y not in visited:
            visited.add(y); q_def.append(y)
unreached = [n for n in all_nodes if n not in visited]
print(f"  Reachable from DEF: {len(visited)}/{len(all_nodes)}")
print(f"  Unreachable: {len(unreached)}")
for n in unreached[:10]: print(f"    {n} [{node_attrs[n][1]}]")

# Components
comps = []
seen = set()
for start in all_nodes:
    if start in seen or not adj[start]: continue
    comp = set(); qq = deque([start]); comp.add(start); seen.add(start)
    while qq:
        x = qq.popleft()
        for y in adj[x]:
            if y not in comp: comp.add(y); seen.add(y); qq.append(y)
    comps.append(comp)
print(f"  Connected components: {len(comps)}")
for i,c in enumerate(sorted(comps, key=len, reverse=True)[:5]):
    print(f"    #{i+1}: size={len(c)}{(' (sample: '+', '.join(list(c)[:3])+')') if len(c)<10 else ''}")

# 3
hdr("3. DEGREE DISTRIBUTION")
degs = {n: len(adj[n]) for n in all_nodes if adj[n]}
top = sorted(degs.items(), key=lambda x:-x[1])[:20]
print("  Top 20 hubs:")
for n,d in top: print(f"    {d:>3}  {n}")
print("\n  Distribution:")
dist = Counter(degs.values())
for d in sorted(dist.keys(), reverse=True):
    bar = '█' * min(40, dist[d])
    print(f"    deg={d:3}: {dist[d]:3} {bar}")

# 4 — β₁/V
hdr("4. CYCLE-RICHNESS β₁/V")
V = len([n for n in all_nodes if adj[n]])  # nodes with edges
E = u_edges
beta1 = E - V + len(comps)
print(f"  V (with edges) = {V}")
print(f"  E (undirected) = {E}")
print(f"  components = {len(comps)}")
print(f"  β₁ = E - V + comps = {beta1}")
print(f"  β₁/V = {beta1/V:.3f}  (cycle-rich threshold: ≥ 2)")

# 5 — Tarjan articulation points (iterative)
hdr("5. ARTICULATION POINTS")
def tarjan_ap(graph):
    visited = {}; low = {}; parent = {}; aps = set(); timer = [0]
    for root in graph:
        if root in visited: continue
        # iterative DFS
        stack = [(root, iter(graph[root]))]
        visited[root] = timer[0]; low[root] = timer[0]; timer[0] += 1
        parent[root] = None
        root_children = 0
        while stack:
            u, it = stack[-1]
            try:
                v = next(it)
                if v not in visited:
                    parent[v] = u
                    visited[v] = timer[0]; low[v] = timer[0]; timer[0] += 1
                    if u == root: root_children += 1
                    stack.append((v, iter(graph[v])))
                elif v != parent[u]:
                    low[u] = min(low[u], visited[v])
            except StopIteration:
                stack.pop()
                if stack:
                    p = stack[-1][0]
                    low[p] = min(low[p], low[u])
                    if parent[p] is not None and low[u] >= visited[p]:
                        aps.add(p)
        if root_children > 1: aps.add(root)
    return aps

aps = tarjan_ap(adj)
print(f"  Articulation points: {len(aps)}")
# For each AP, list isolated component sizes
for ap in sorted(aps):
    if len(adj[ap]) < 2: continue
    comps_split = []; seen_ap = {ap}
    for nb in adj[ap]:
        if nb in seen_ap: continue
        comp = set(); qq = deque([nb]); comp.add(nb); seen_ap.add(nb)
        while qq:
            x = qq.popleft()
            for y in adj[x]:
                if y not in seen_ap: seen_ap.add(y); comp.add(y); qq.append(y)
        comps_split.append(comp)
    if len(comps_split) >= 2:
        sizes = sorted([len(c) for c in comps_split], reverse=True)
        # identify smallest isolated parts
        smallest = min(comps_split, key=len)
        sample = ', '.join(sorted(smallest)[:3]) + ('…' if len(smallest)>3 else '')
        print(f"    {ap:<35} → isolates {sizes[1:]} ({sample})")

# 6 — triangles
hdr("6. M1 (Z-TRIANGLE) DENSITY")
triangles = 0
sorted_nodes = sorted(all_nodes)
for i, a in enumerate(sorted_nodes):
    nbs_a = [n for n in adj[a] if n > a]
    for j, b in enumerate(nbs_a):
        for c in nbs_a[j+1:]:
            if c in adj[b]:
                triangles += 1
print(f"  Distinct undirected triangles: {triangles}")
print(f"  Triangle density (per node): {triangles*3/V:.2f}")

# 7 — layer matrix
hdr("7. CROSS-LAYER CONNECTIVITY")
mat = defaultdict(int)
for a in all_nodes:
    la = node_attrs[a][1] or '?'
    for b in adj[a]:
        if a < b:
            lb = node_attrs[b][1] or '?'
            key = tuple(sorted([la, lb]))
            mat[key] += 1
print(f"  {'layer-pair':<40} edges")
for (la,lb),c in sorted(mat.items(), key=lambda x:-x[1]):
    print(f"    {la:<15} ↔ {lb:<20} {c}")

# 8 — twins (Jaccard=1 cliques)
hdr("8. JACCARD=1 GROUPS (cousin-families)")
groups = defaultdict(list)
for n in all_nodes:
    if not adj[n]: continue
    fp = frozenset(adj[n])
    groups[fp].append(n)
print("  Identical-neighbor-set groups (≥3 members = cousin clique):")
for fp, members in sorted(groups.items(), key=lambda x:-len(x[1])):
    if len(members) >= 3:
        print(f"    {len(members)} members: {sorted(members)[:6]}{'…' if len(members)>6 else ''}")

# 9 — Class-A neighbor sets (Jaccard via symmetric difference, excluding each other)
print("\n  High-Jaccard outside families (potential overlooked duplicates):")
big_fams = {m for fp,mem in groups.items() if len(mem)>=3 for m in mem}
seen_pairs=set()
hits=[]
nodelist = [n for n in all_nodes if adj[n] and n not in big_fams]
for i in range(len(nodelist)):
    for j in range(i+1, len(nodelist)):
        a, b = nodelist[i], nodelist[j]
        A = adj[a] - {b}; B = adj[b] - {a}
        if len(A) < 4 or len(B) < 4: continue
        inter = len(A & B); union = len(A | B)
        jac = inter/union if union else 0
        if jac >= 0.7:
            hits.append((jac, a, b, inter, len(A), len(B)))
for jac,a,b,inter,da,db in sorted(hits, key=lambda x:-x[0])[:10]:
    print(f"    J={jac:.2f}  {a:<35} {b:<35} shared={inter} deg=({da},{db})")
if not hits: print("    (none — graph clean of structural duplicates)")

# 10 — edge label patterns
hdr("9. EDGE-LABEL DISCIPLINE")
patterns = Counter()
for lbl in edge_labels:
    if not lbl: patterns['(empty)'] += 1; continue
    l = lbl.lower()
    if 'sibling' in l: patterns['sibling_*'] += 1
    elif 'class_a' in l or 'classa' in l: patterns['class_a_*'] += 1
    elif 'iff' in l or l.startswith('same_'): patterns['same_/iff_*'] += 1
    elif 'paired' in l: patterns['paired_*'] += 1
    elif 'instance' in l: patterns['instance_of_*'] += 1
    elif 'ground' in l: patterns['grounds_*'] += 1
    elif 'force' in l: patterns['forces_*'] += 1
    elif 'argmin' in l: patterns['argmin_*'] += 1
    elif 'cousin' in l: patterns['cousin_*'] += 1
    elif 'realis' in l or 'realiz' in l: patterns['realises_*'] += 1
    elif 'chain' in l: patterns['chain_*'] += 1
    else: patterns['other'] += 1
print("  Edge-label categories (1175 directed records):")
for k,v in patterns.most_common():
    pct = 100*v/len(edge_labels)
    print(f"    {k:<22} {v:>4} ({pct:5.1f}%)")

# 11 — data integrity
hdr("10. DATA INTEGRITY")
nostat = [n for n in all_nodes if not node_attrs[n][2]]
notitle = [n for n in all_nodes if not node_attrs[n][3]]
nolbl = sum(1 for l in edge_labels if not l)
print(f"  Nodes with no status: {len(nostat)}")
for n in nostat[:5]: print(f"    {n}")
print(f"  Nodes with no title: {len(notitle)}")
for n in notitle[:5]: print(f"    {n}")
print(f"  Edges with no label: {nolbl}")

# 12 — bidirectional check
hdr("11. EDGE DIRECTIONALITY (Class A symmetry check)")
directed = defaultdict(set)
for a, b, lbl in q("MATCH (a:Node)-[e:Edge]->(b:Node) RETURN a.id, b.id, e.label"):
    directed[(a,b)].add(lbl or '')
bidir = sum(1 for (a,b) in directed if (b,a) in directed and a<b)
asymm_pairs = [(a,b) for (a,b) in directed if (b,a) not in directed]
print(f"  Distinct (a→b) source records: {len(directed)}")
print(f"  Bidirectional pairs (a↔b both): {bidir}")
print(f"  Asymmetric (a→b only): {len(asymm_pairs)}")
print("  (Note: undirected discovery enforced at query-tool level per audit; asymmetry is rhetorical, not structural)")

print("\n" + "═"*70)
print("  COHERENCE AUDIT COMPLETE")
print("═"*70)
