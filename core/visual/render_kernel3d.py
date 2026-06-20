"""
Render core kernel as 3D fractal: Sierpinski-in-plane x 3_1 screw axis
= L(3,1) deck transformation manifest in 3D visual substrate.

Structural decisions (inherited from 2D render_svg.py + 3D lift):
- 3-fold subdivision (Z/3 forced, not S_4 of standard Sierpinski tet)
- 3_1 screw axis (rotation + translation, no fixed points = free Z/3 action
  = L(3,1) deck transformation form, not just rotation around fixed axis)
- A_0 central axis with pulse at origin
- No structure outside closure
- Transparent background, blends with parent

Same structure as 2D kernel.svg, lifted into 3D substrate coordinate.

Output: kernel3d.html (self-contained, Three.js via CDN, WebGL render).
"""

import math
import json
import os

# Fractal parameters
SIERPINSKI_DEPTH = 5           # 3^5 = 243 leaf triangles per layer
N_LAYERS = 9                   # 3 full Z/3 deck cycles visible
LAYER_HEIGHT = 0.35            # vertical spacing per layer
TRIANGLE_SIZE = 2.2            # outer triangle radius

# Colors (carry over palette from 2D kernel.svg)
SIERPINSKI_HEX = '#5a6482'     # dusty slate-blue (in-plane subdivision)
A0_HEX = '#b48232'             # warm amber (A_0 + helical screw edges)
HELIX_HEX = '#a8703a'          # slightly darker amber for helical edges
                               # (visually marks 3_1 screw axis as triple
                               # helix linking corresponding corners
                               # across Z/3 deck transformation layers)


def hex_to_rgb(h):
    h = h.lstrip('#')
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255)


def gen_sierpinski(p1, p2, p3, depth, max_depth):
    """Recursive 3-fold subdivision (same logic as render_svg.py)."""
    out = [(max_depth - depth, p1, p2, p3)]
    if depth == 0:
        return out
    m12 = ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)
    m23 = ((p2[0]+p3[0])/2, (p2[1]+p3[1])/2)
    m31 = ((p3[0]+p1[0])/2, (p3[1]+p1[1])/2)
    out += gen_sierpinski(p1, m12, m31, depth-1, max_depth)
    out += gen_sierpinski(m12, p2, m23, depth-1, max_depth)
    out += gen_sierpinski(m31, m23, p3, depth-1, max_depth)
    return out


def build_fractal_edges():
    """Build 3D edge list: Sierpinski subdivision lifted with 3_1 screw axis.

    Each z-layer is a Sierpinski fractal, rotated by 120 degrees per layer
    (Z/3 screw). After 3 layers, structure returns to same orientation
    (Z/3 deck transformation cycle). N_LAYERS = 9 shows 3 full cycles.

    Returns two edge lists:
    - sierpinski edges: in-plane Sierpinski subdivision per layer
    - helical edges: triple helix connecting outer corners across layers,
      visually manifesting the 3_1 screw axis (rotation + translation).
      Triple helix is THE classic L(3,1) deck transformation form;
      without it, the screw structure would be invisible because
      Sierpinski triangle is itself Z/3 fixed under rotation.
    """
    R = TRIANGLE_SIZE
    initial = []
    for k in range(3):
        a = math.pi / 2 + k * 2 * math.pi / 3
        initial.append((R * math.cos(a), R * math.sin(a)))

    base_triangles = gen_sierpinski(initial[0], initial[1], initial[2],
                                     SIERPINSKI_DEPTH, SIERPINSKI_DEPTH)

    sierpinski_edges = []
    layer_corners = []  # store per-layer absolute corner positions
    for layer in range(N_LAYERS):
        z = (layer - (N_LAYERS - 1) / 2) * LAYER_HEIGHT
        rot = layer * 2 * math.pi / 3  # 3_1 screw: 120 deg per layer
        cr, sr = math.cos(rot), math.sin(rot)

        def transform(p):
            x, y = p
            return (cr * x - sr * y, sr * x + cr * y, z)

        # Sierpinski subdivision in this layer
        for (level, p1, p2, p3) in base_triangles:
            r1, r2, r3 = transform(p1), transform(p2), transform(p3)
            sierpinski_edges.append((r1, r2, level))
            sierpinski_edges.append((r2, r3, level))
            sierpinski_edges.append((r3, r1, level))

        # Store outer corners (initial[0], initial[1], initial[2]) at
        # this layer for helical-edge generation
        layer_corners.append([transform(v) for v in initial])

    # Helical edges: connect corner k of layer N to corner k of layer N+1.
    # Each layer's corner k is rotated 120 deg from previous layer's
    # corner k (because layer rotation is 120 deg per step), so connection
    # forms helix ascending around central axis. Three helices total
    # (k = 0, 1, 2) make the triple helix.
    helical_edges = []
    for layer in range(N_LAYERS - 1):
        for k in range(3):
            p_curr = layer_corners[layer][k]
            p_next = layer_corners[layer + 1][k]
            helical_edges.append((p_curr, p_next, -1))  # -1 = helix marker

    return sierpinski_edges, helical_edges


def edges_to_buffers(sierpinski_edges, helical_edges):
    """Flatten edges into position + color arrays for Three.js BufferGeometry.

    Rounds floats to 3 decimals (sufficient for visual precision at all
    practical zoom levels) to reduce file size.

    Sierpinski edges colored slate-blue with opacity fading by subdivision
    level (outer strong, inner fades). Helical edges colored amber to
    visually mark them as part of A_0/screw-axis structure, full opacity
    since there are only 3*(N-1) of them — visual emphasis warranted.
    """
    positions = []
    colors = []
    sierp_rgb = hex_to_rgb(SIERPINSKI_HEX)
    helix_rgb = hex_to_rgb(HELIX_HEX)

    def r(v):
        return round(v, 3)

    # Sierpinski edges first
    for (p1, p2, level) in sierpinski_edges:
        positions.extend([r(p1[0]), r(p1[1]), r(p1[2])])
        positions.extend([r(p2[0]), r(p2[1]), r(p2[2])])
        op = max(0.05, 0.7 * (0.78 ** level))
        col = [r(sierp_rgb[0] * op), r(sierp_rgb[1] * op), r(sierp_rgb[2] * op)]
        colors.extend(col)
        colors.extend(col)

    # Helical edges (full opacity, amber for screw axis visual emphasis)
    for (p1, p2, _) in helical_edges:
        positions.extend([r(p1[0]), r(p1[1]), r(p1[2])])
        positions.extend([r(p2[0]), r(p2[1]), r(p2[2])])
        col = [r(helix_rgb[0] * 0.92), r(helix_rgb[1] * 0.92),
               r(helix_rgb[2] * 0.92)]
        colors.extend(col)
        colors.extend(col)

    return {'positions': positions, 'colors': colors}


HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Core kernel - 3D manifestation</title>
<style>
  html, body { margin: 0; padding: 0; background: #0a0a0a; color: #d0d0d0;
               font-family: Georgia, 'Times New Roman', serif;
               overflow: hidden; }
  canvas { display: block; }
  #info { position: fixed; top: 16px; left: 16px; font-size: 13px;
          opacity: 0.78; max-width: 420px; line-height: 1.55;
          pointer-events: none; }
  #info b { color: #f0f0f0; }
  #legend { position: fixed; bottom: 16px; left: 16px; font-size: 11px;
            opacity: 0.55; line-height: 1.45; pointer-events: none; }
  #formula { position: fixed; top: 16px; right: 16px; font-size: 13px;
             font-family: 'Courier New', monospace; opacity: 0.6;
             text-align: right; line-height: 1.6; pointer-events: none; }
</style>
</head>
<body>
<div id="info">
  <b>Core kernel - 3D manifestation</b><br>
  Sierpinski subdivision (in-plane) x 3_1 screw axis (vertical)<br>
  = L(3,1) deck transformation in visual substrate.<br>
  Z/3 forced via screw axis: rotation + translation, no fixed points
  (free action). Self-similar at all scales.
</div>
<div id="formula">
  A_0 = argmin Z(x)<br>
  &nbsp;&nbsp;x in C(A_0)<br>
  A_0 = F(A_0)<br>
  K(O) &lt; K(F)
</div>
<div id="legend">
  Drag = rotate &middot; scroll = zoom &middot; idle = auto-rotate<br>
  Central pulse = A_0 (forced unique stable point)<br>
  Vertical axis = 3_1 screw axis of L(3,1) deck transformation
</div>

<script type="importmap">
{
  "imports": {
    "three": "./lib/three.module.js"
  }
}
</script>

<script type="module">
import * as THREE from 'three';
import { OrbitControls } from './lib/OrbitControls.js';

const FRACTAL = __FRACTAL_JSON__;

// Scene
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  55, window.innerWidth / window.innerHeight, 0.01, 1000
);
camera.position.set(4.5, 3.2, 5.5);
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setClearColor(0x0a0a0a, 1);
document.body.appendChild(renderer.domElement);

// Fractal mesh
const geom = new THREE.BufferGeometry();
geom.setAttribute('position',
  new THREE.Float32BufferAttribute(FRACTAL.positions, 3));
geom.setAttribute('color',
  new THREE.Float32BufferAttribute(FRACTAL.colors, 3));
const mat = new THREE.LineBasicMaterial({
  vertexColors: true, transparent: true, opacity: 0.95
});
const fractal = new THREE.LineSegments(geom, mat);
scene.add(fractal);

// A_0 vertical axis (the 3_1 screw axis)
const axisGeo = new THREE.BufferGeometry();
axisGeo.setAttribute('position', new THREE.Float32BufferAttribute([
  0, 0, -2.5, 0, 0, 2.5
], 3));
const axisMat = new THREE.LineBasicMaterial({
  color: 0xb48232, transparent: true, opacity: 0.25
});
scene.add(new THREE.Line(axisGeo, axisMat));

// A_0 pulse at origin
const pulseGeo = new THREE.SphereGeometry(0.08, 24, 24);
const pulseMat = new THREE.MeshBasicMaterial({
  color: 0xb48232, transparent: true, opacity: 0.9
});
const pulse = new THREE.Mesh(pulseGeo, pulseMat);
scene.add(pulse);

// Halo
const haloGeo = new THREE.SphereGeometry(0.22, 24, 24);
const haloMat = new THREE.MeshBasicMaterial({
  color: 0xb48232, transparent: true, opacity: 0.35
});
const halo = new THREE.Mesh(haloGeo, haloMat);
scene.add(halo);

// Controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.06;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.45;
controls.minDistance = 1.0;
controls.maxDistance = 18;
controls.target.set(0, 0, 0);

let lastInteract = 0;
controls.addEventListener('start', () => { lastInteract = Date.now(); });

// Animation
let t = 0;
function animate() {
  requestAnimationFrame(animate);
  t += 0.016;

  // Auto-rotate resumes after 3s idle
  controls.autoRotate = (Date.now() - lastInteract > 3000);

  // A_0 pulse: amplitude + halo opacity inverse
  const pf = 1 + 0.5 * Math.sin(t * 1.4);
  pulse.scale.setScalar(pf);
  halo.scale.setScalar(pf * 1.4);
  halo.material.opacity = 0.35 * (2 - pf) / 1.5;

  controls.update();
  renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// Expose for debugging / external camera control
window.scene = scene;
window.camera = camera;
window.controls = controls;
</script>
</body>
</html>
'''


def main():
    sierp_edges, helix_edges = build_fractal_edges()
    fractal = edges_to_buffers(sierp_edges, helix_edges)
    fractal_json = json.dumps(fractal, separators=(',', ':'))

    html = HTML_TEMPLATE.replace('__FRACTAL_JSON__', fractal_json)

    out_path = '/home/user/Ouroboros/core/visual/kernel3d.html'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)

    size_kb = os.path.getsize(out_path) / 1024
    print(f'Wrote {out_path}')
    print(f'  size: {size_kb:.1f} KB')
    print(f'  sierpinski edges: {len(sierp_edges)}')
    print(f'  helical edges: {len(helix_edges)} '
          f'(3 helices x {N_LAYERS - 1} segments = triple helix manifest)')
    print(f'  total edges: {len(sierp_edges) + len(helix_edges)}')
    print(f'  layers: {N_LAYERS} (3 full Z/3 cycles)')
    print(f'  Sierpinski depth: {SIERPINSKI_DEPTH}')


if __name__ == '__main__':
    main()
