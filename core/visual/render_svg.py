"""
Render core kernel visual surface as animated SVG.

Composition (matches core/visual/kernel.html):
- Sierpinski triangulation background (self-similarity)
- Borromean rings at center (3-slot mutual constraint)
- Z/3 marker orbits (ThreePeriod canonical action)
- A_0 halo pulse at center (forced unique stable point)

SVG with SMIL animations:
- Vector quality — crisp at any zoom
- True alpha — no palette banding
- Small file — typical <50 KB
- Loops cleanly: rotations complete 120° per cycle, indistinguishable
  from full cycle due to triangle's Z/3 symmetry.

GitHub renders SVG via `![](file.svg)` markdown syntax.
"""

import math

# ── Canvas ──────────────────────────────────────────────────────────────────
W = H = 600
cx = cy = W / 2

LOOP_SEC = 12.0                   # slow meditative pace
PULSE_SEC = 4.0                   # 3 pulses per main loop

# ── Palette (works on both light and dark GitHub backgrounds) ──────────────
# No background rectangle: SVG is transparent, blends with parent.
SIERPINSKI = '#5a6482'            # dusty slate-blue
Z3_DOT = '#464b5f'                # dark slate
A0_AMBER = '#b48232'              # warm amber
LABEL_COLOR = '#3c3c46'

RINGS = [
    ('B', '#be4b41'),             # terracotta
    ('P', '#3c8c5f'),             # sage
    ('I', '#3c64a5'),             # slate blue
]

# ── Sierpinski generation ───────────────────────────────────────────────────
def gen_triangles(p1, p2, p3, depth, max_depth, out):
    """Recursively generate (level, triangle_points)."""
    out.append((max_depth - depth, (p1, p2, p3)))
    if depth == 0:
        return
    m12 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    m23 = ((p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2)
    m31 = ((p3[0] + p1[0]) / 2, (p3[1] + p1[1]) / 2)
    gen_triangles(p1, m12, m31, depth - 1, max_depth, out)
    gen_triangles(m12, p2, m23, depth - 1, max_depth, out)
    gen_triangles(m31, m23, p3, depth - 1, max_depth, out)


def sierpinski_svg(depth=6):
    """Outer triangle + recursive subdivision, grouped by level for opacity."""
    R = min(W, H) * 0.43
    verts = []
    for k in range(3):
        a = -math.pi / 2 + k * (2 * math.pi / 3)
        verts.append((cx + R * math.cos(a), cy + R * math.sin(a)))

    triangles = []
    gen_triangles(verts[0], verts[1], verts[2], depth, depth, triangles)

    # Group by level for separate opacity / stroke-width
    by_level = {}
    for lvl, tri in triangles:
        by_level.setdefault(lvl, []).append(tri)

    parts = ['  <!-- Sierpinski triangulation: self-similarity surface -->']
    parts.append(f'  <g id="sierpinski" stroke="{SIERPINSKI}" fill="none">')
    # Outer level (0) is the strongest, deeper levels fade
    for lvl in sorted(by_level.keys()):
        opacity = round(0.55 * (0.78 ** lvl), 3)
        if opacity < 0.025:
            continue
        stroke_w = max(0.4, 1.3 - 0.15 * lvl)
        parts.append(
            f'    <g stroke-opacity="{opacity}" '
            f'stroke-width="{stroke_w}">'
        )
        for (p1, p2, p3) in by_level[lvl]:
            pts = f'{p1[0]:.2f},{p1[1]:.2f} {p2[0]:.2f},{p2[1]:.2f} ' \
                  f'{p3[0]:.2f},{p3[1]:.2f}'
            parts.append(f'      <polygon points="{pts}" />')
        parts.append('    </g>')

    # Rotation animation: 120° per loop (Z/3 → visually full cycle)
    parts.append(
        f'    <animateTransform attributeName="transform" type="rotate" '
        f'from="0 {cx} {cy}" to="120 {cx} {cy}" '
        f'dur="{LOOP_SEC}s" repeatCount="indefinite" />'
    )
    parts.append('  </g>')
    return '\n'.join(parts)


def z3_orbit_svg(radius_factor, rotate_forward, duration_offset_ratio):
    """Three small markers at 120° around center, orbiting."""
    r_orbit = min(W, H) * radius_factor
    direction = "" if rotate_forward else "-"
    parts = [
        f'  <!-- Z/3 orbit (radius {radius_factor}, '
        f'{"forward" if rotate_forward else "reverse"}) -->',
        f'  <g fill="{Z3_DOT}" fill-opacity="0.45">'
    ]
    for k in range(3):
        a = -math.pi / 2 + k * (2 * math.pi / 3)
        x = cx + r_orbit * math.cos(a)
        y = cy + r_orbit * math.sin(a)
        parts.append(f'    <circle cx="{x:.2f}" cy="{y:.2f}" r="3.5" />')
    parts.append(
        f'    <animateTransform attributeName="transform" type="rotate" '
        f'from="0 {cx} {cy}" to="{direction}120 {cx} {cy}" '
        f'dur="{LOOP_SEC}s" repeatCount="indefinite" />'
    )
    parts.append('  </g>')
    return '\n'.join(parts)


def borromean_svg():
    """Three interlocking rings with weave illusion."""
    ring_r = min(W, H) * 0.125
    offset = ring_r * 0.55
    parts = [
        '  <!-- Borromean rings: 3-slot mutual constraint -->'
    ]

    # Compute ring centers
    centers = []
    for k in range(3):
        a = -math.pi / 2 + k * (2 * math.pi / 3)
        rx = cx + offset * math.cos(a)
        ry = cy + offset * math.sin(a)
        centers.append((rx, ry, a))

    # Pass 1: full rings at low alpha (the "under" layer)
    parts.append('  <g id="borromean-under" fill="none" stroke-width="3">')
    for k, (rx, ry, _) in enumerate(centers):
        _, color = RINGS[k]
        parts.append(
            f'    <circle cx="{rx:.2f}" cy="{ry:.2f}" r="{ring_r:.2f}" '
            f'stroke="{color}" stroke-opacity="0.40" />'
        )
    parts.append('  </g>')

    # Pass 2: top-arcs at high alpha (the "over" layer at label sectors)
    parts.append('  <g id="borromean-over" fill="none" stroke-width="3.2" '
                 'stroke-linecap="round">')
    for k, (rx, ry, label_a) in enumerate(centers):
        _, color = RINGS[k]
        # Arc spans ±60° around the label angle
        start_ang = label_a - math.pi / 3
        end_ang = label_a + math.pi / 3
        x1 = rx + ring_r * math.cos(start_ang)
        y1 = ry + ring_r * math.sin(start_ang)
        x2 = rx + ring_r * math.cos(end_ang)
        y2 = ry + ring_r * math.sin(end_ang)
        # SVG arc: M start A rx ry x-axis-rotation large-arc-flag sweep-flag x y
        parts.append(
            f'    <path d="M {x1:.2f} {y1:.2f} '
            f'A {ring_r:.2f} {ring_r:.2f} 0 0 1 {x2:.2f} {y2:.2f}" '
            f'stroke="{color}" stroke-opacity="0.92" />'
        )
    parts.append('  </g>')

    # Labels at outer edges
    parts.append('  <g id="borromean-labels" fill="' + LABEL_COLOR + '" '
                 'font-family="Georgia, serif" font-size="18" '
                 'text-anchor="middle" dominant-baseline="central">')
    for k, (rx, ry, label_a) in enumerate(centers):
        label, _ = RINGS[k]
        lx = rx + ring_r * 1.42 * math.cos(label_a)
        ly = ry + ring_r * 1.42 * math.sin(label_a)
        parts.append(f'    <text x="{lx:.2f}" y="{ly:.2f}">{label}</text>')
    parts.append('  </g>')

    return '\n'.join(parts)


def a0_center_svg():
    """A_0 with pulsing halo."""
    parts = [
        '  <!-- A_0 forced unique stable point -->',
        f'  <g id="a0-center">',
        # Pulsing halo
        f'    <circle cx="{cx}" cy="{cy}" r="4" fill="{A0_AMBER}">',
        f'      <animate attributeName="r" values="4;14;4" '
        f'dur="{PULSE_SEC}s" repeatCount="indefinite" />',
        f'      <animate attributeName="fill-opacity" '
        f'values="0.55;0.08;0.55" dur="{PULSE_SEC}s" '
        f'repeatCount="indefinite" />',
        f'    </circle>',
        # Inner stable dot
        f'    <circle cx="{cx}" cy="{cy}" r="3.2" '
        f'fill="{A0_AMBER}" fill-opacity="0.95" />',
        # Label below
        f'    <text x="{cx}" y="{cy + 24}" fill="{A0_AMBER}" '
        f'fill-opacity="0.8" font-family="Georgia, serif" '
        f'font-style="italic" font-size="14" text-anchor="middle">A₀</text>',
        '  </g>'
    ]
    return '\n'.join(parts)


def main():
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"
     width="{W}" height="{H}" preserveAspectRatio="xMidYMid meet">
  <!-- Core kernel visual surface — auto-generated by render_svg.py
       Composition: Sierpinski + Borromean rings + Z/3 orbits + A_0 pulse
       All rotations complete 120° per loop (Z/3 symmetry → visually full).
       Transparent background: blends with light or dark parent.
  -->

{sierpinski_svg(depth=6)}

{z3_orbit_svg(radius_factor=0.40, rotate_forward=True,
              duration_offset_ratio=0)}

{z3_orbit_svg(radius_factor=0.22, rotate_forward=False,
              duration_offset_ratio=0.5)}

{borromean_svg()}

{a0_center_svg()}
</svg>
'''
    out_path = '/home/user/Ouroboros/core/visual/kernel.svg'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(svg)
    import os
    size_kb = os.path.getsize(out_path) / 1024
    print(f'Wrote {out_path}')
    print(f'  size: {size_kb:.1f} KB')
    print(f'  resolution: vector (rendered at any zoom)')
    print(f'  loop: {LOOP_SEC}s rotation, {PULSE_SEC}s A_0 pulse')


if __name__ == '__main__':
    main()
