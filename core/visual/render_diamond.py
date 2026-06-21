"""
Render diamond cubic lattice as invariant skeleton manifestation in 3D substrate.

Mathematically: diamond cubic crystal structure (Fd-3m, space group 227).
The substrate-cousin in carbon-physical substrate of the invariant skeleton
that is being visualized:

- Vertex-transitive: every atom in identical local environment
- sp3 tetrahedral coordination: 4 bonds per atom at 109.47 deg
- Z/3 local rotation symmetry around each [111] body diagonal
- 6-membered rings as smallest closed loops
- Two interpenetrating FCC sublattices offset by (1/4, 1/4, 1/4)
- 8 atoms per conventional unit cell

What is shown: invariant load-bearing skeleton only — atom positions and
bonds. No events, no dynamics overlay, no A_0 markers, no axis lines, no
helical decorations. Visual aesthetic: glowing nodes + light-beam bonds
(AA-VFX style), making the skeleton visible as gestalt while remaining
mathematically exact.

Output: diamond_lattice.html — self-contained, local Three.js, WebGL render.
"""

import math
import json
import os

# ── Lattice parameters ───────────────────────────────────────────────
N_CELLS = 8                    # NxNxN unit cells (8^3 = 512 cells)
LATTICE_CONST = 1.0            # normalized lattice constant a
SPHERICAL_TRUNCATE = True      # only include atoms within sphere radius R
SPHERE_RADIUS = N_CELLS * 0.5  # truncation radius in lattice units

# Bond detection tolerance
BOND_TOLERANCE = 0.02          # ±2% of nearest-neighbor distance

# ── Diamond cubic basis (fractional coords of conventional unit cell) ─
DIAMOND_BASIS = [
    # FCC sublattice 1 (origin)
    (0.00, 0.00, 0.00),
    (0.50, 0.50, 0.00),
    (0.50, 0.00, 0.50),
    (0.00, 0.50, 0.50),
    # FCC sublattice 2 (offset by (1/4, 1/4, 1/4) along body diagonal)
    (0.25, 0.25, 0.25),
    (0.75, 0.75, 0.25),
    (0.75, 0.25, 0.75),
    (0.25, 0.75, 0.75),
]

# Nearest-neighbor distance: a · sqrt(3) / 4
NN_DIST = LATTICE_CONST * math.sqrt(3) / 4
NN_DIST_MIN = NN_DIST * (1 - BOND_TOLERANCE)
NN_DIST_MAX = NN_DIST * (1 + BOND_TOLERANCE)


def generate_atoms():
    """Generate atom positions for NxNxN unit cells, centered at origin.

    If SPHERICAL_TRUNCATE is on, atoms beyond SPHERE_RADIUS are excluded
    (gives natural rounded extent rather than cubical box edges).
    """
    atoms = []
    offset = -N_CELLS * LATTICE_CONST / 2
    for ix in range(N_CELLS):
        for iy in range(N_CELLS):
            for iz in range(N_CELLS):
                cx = ix * LATTICE_CONST + offset
                cy = iy * LATTICE_CONST + offset
                cz = iz * LATTICE_CONST + offset
                for bx, by, bz in DIAMOND_BASIS:
                    px = cx + bx * LATTICE_CONST
                    py = cy + by * LATTICE_CONST
                    pz = cz + bz * LATTICE_CONST
                    if SPHERICAL_TRUNCATE:
                        r = math.sqrt(px*px + py*py + pz*pz)
                        if r > SPHERE_RADIUS:
                            continue
                    atoms.append((px, py, pz))
    return atoms


def generate_bonds(atoms):
    """Find all bonds via spatial-grid neighbor search (O(N))."""
    bonds = []
    grid_size = NN_DIST_MAX
    grid = {}
    for i, (x, y, z) in enumerate(atoms):
        gx, gy, gz = (int(math.floor(x / grid_size)),
                      int(math.floor(y / grid_size)),
                      int(math.floor(z / grid_size)))
        grid.setdefault((gx, gy, gz), []).append(i)

    for i, (x1, y1, z1) in enumerate(atoms):
        gx = int(math.floor(x1 / grid_size))
        gy = int(math.floor(y1 / grid_size))
        gz = int(math.floor(z1 / grid_size))
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    cell = (gx + dx, gy + dy, gz + dz)
                    if cell not in grid:
                        continue
                    for j in grid[cell]:
                        if j <= i:
                            continue
                        x2, y2, z2 = atoms[j]
                        d2 = ((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
                        if (NN_DIST_MIN**2) < d2 < (NN_DIST_MAX**2):
                            bonds.append((i, j))
    return bonds


def atom_color(pos):
    """Cool palette: bright cyan-white center, fading to deeper blue at edges.

    Matches AA-VFX aesthetic while encoding radial depth visually.
    """
    x, y, z = pos
    r = math.sqrt(x*x + y*y + z*z)
    d = r / SPHERE_RADIUS  # 0 = center, 1 = edge

    # Brightness fades with radius (center brightest, edge dimmer)
    brightness = max(0.25, 1.0 - d * 0.55)

    # Center: bright cyan-white. Edge: deeper blue-violet.
    rc = 0.50 + 0.35 * d
    gc = 0.85 - 0.25 * d
    bc = 1.00

    return (round(rc * brightness, 3),
            round(gc * brightness, 3),
            round(bc * brightness, 3))


def build_buffers():
    """Build position and color buffers for atoms (Points) and bonds (Lines)."""
    atoms = generate_atoms()
    bonds = generate_bonds(atoms)

    atom_positions = []
    atom_colors_arr = []
    for pos in atoms:
        atom_positions.extend([round(pos[0], 3), round(pos[1], 3),
                                round(pos[2], 3)])
        c = atom_color(pos)
        atom_colors_arr.extend(c)

    bond_positions = []
    bond_colors_arr = []
    for (i, j) in bonds:
        p1, p2 = atoms[i], atoms[j]
        c1, c2 = atom_color(p1), atom_color(p2)
        # Bonds slightly dimmer than atoms for visual layering
        bond_positions.extend([round(p1[0], 3), round(p1[1], 3),
                                round(p1[2], 3)])
        bond_positions.extend([round(p2[0], 3), round(p2[1], 3),
                                round(p2[2], 3)])
        bond_colors_arr.extend([round(c1[0]*0.5, 3), round(c1[1]*0.5, 3),
                                 round(c1[2]*0.5, 3)])
        bond_colors_arr.extend([round(c2[0]*0.5, 3), round(c2[1]*0.5, 3),
                                 round(c2[2]*0.5, 3)])

    return {
        'atoms_positions': atom_positions,
        'atoms_colors': atom_colors_arr,
        'bonds_positions': bond_positions,
        'bonds_colors': bond_colors_arr,
        'n_atoms': len(atoms),
        'n_bonds': len(bonds),
        'sphere_radius': SPHERE_RADIUS,
    }


HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Diamond lattice - invariant skeleton manifestation</title>
<style>
  html, body { margin: 0; padding: 0; background: #050810; color: #c8d0e0;
               font-family: Georgia, 'Times New Roman', serif;
               overflow: hidden; }
  canvas { display: block; }
  #info { position: fixed; top: 16px; left: 16px; font-size: 12px;
          opacity: 0.65; max-width: 380px; line-height: 1.55;
          pointer-events: none; }
  #info b { color: #e8ecf5; font-size: 13px; }
  #stats { position: fixed; bottom: 16px; left: 16px; font-size: 10px;
           opacity: 0.4; line-height: 1.4; pointer-events: none;
           font-family: 'Courier New', monospace; }
  #legend { position: fixed; bottom: 16px; right: 16px; font-size: 10px;
            opacity: 0.4; line-height: 1.4; text-align: right;
            pointer-events: none; }
</style>
</head>
<body>
<div id="info">
  <b>Diamond cubic lattice</b><br>
  Space group Fd-3m. Vertex-transitive sp3 tetrahedral coordination.<br>
  Z/3 rotation symmetry along each [111] body diagonal axis.<br>
  Invariant skeleton manifestation — substrate-cousin in carbon-physical
  substrate of the load-bearing structural form.
</div>
<div id="stats">
  atoms: __N_ATOMS__   bonds: __N_BONDS__   cells: __N_CELLS__^3
</div>
<div id="legend">
  drag: rotate &middot; scroll: zoom &middot; idle: auto-rotate
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

const DATA = __DATA_JSON__;

// ── Scene setup ────────────────────────────────────────────────────────
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x050810, 0.045);

const camera = new THREE.PerspectiveCamera(
  50, window.innerWidth / window.innerHeight, 0.1, 200
);
const initDist = DATA.sphere_radius * 2.2;
camera.position.set(initDist * 0.7, initDist * 0.55, initDist * 0.7);
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setClearColor(0x050810, 1);
document.body.appendChild(renderer.domElement);

// ── Gaussian point sprite texture (procedural) ─────────────────────────
function makeGaussianSprite(size = 128) {
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = size;
  const ctx = canvas.getContext('2d');
  const gradient = ctx.createRadialGradient(
    size/2, size/2, 0, size/2, size/2, size/2
  );
  gradient.addColorStop(0.0,  'rgba(255,255,255,1.0)');
  gradient.addColorStop(0.15, 'rgba(255,255,255,0.9)');
  gradient.addColorStop(0.35, 'rgba(200,220,255,0.4)');
  gradient.addColorStop(0.7,  'rgba(120,160,255,0.08)');
  gradient.addColorStop(1.0,  'rgba(80,120,255,0.0)');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, size, size);
  const texture = new THREE.CanvasTexture(canvas);
  texture.needsUpdate = true;
  return texture;
}

const spriteTex = makeGaussianSprite();

// ── Atoms: glowing point sprites ───────────────────────────────────────
const atomsGeo = new THREE.BufferGeometry();
atomsGeo.setAttribute('position',
  new THREE.Float32BufferAttribute(DATA.atoms_positions, 3));
atomsGeo.setAttribute('color',
  new THREE.Float32BufferAttribute(DATA.atoms_colors, 3));

const atomsMat = new THREE.PointsMaterial({
  size: 0.32,
  map: spriteTex,
  vertexColors: true,
  transparent: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  sizeAttenuation: true
});

const atomsPoints = new THREE.Points(atomsGeo, atomsMat);
scene.add(atomsPoints);

// ── Bonds: emissive light beams ────────────────────────────────────────
const bondsGeo = new THREE.BufferGeometry();
bondsGeo.setAttribute('position',
  new THREE.Float32BufferAttribute(DATA.bonds_positions, 3));
bondsGeo.setAttribute('color',
  new THREE.Float32BufferAttribute(DATA.bonds_colors, 3));

const bondsMat = new THREE.LineBasicMaterial({
  vertexColors: true,
  transparent: true,
  opacity: 0.55,
  blending: THREE.AdditiveBlending,
  depthWrite: false
});

const bondsLines = new THREE.LineSegments(bondsGeo, bondsMat);
scene.add(bondsLines);

// ── Controls ───────────────────────────────────────────────────────────
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.06;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.35;
controls.minDistance = 0.5;
controls.maxDistance = DATA.sphere_radius * 4;
controls.target.set(0, 0, 0);

let lastInteract = 0;
controls.addEventListener('start', () => { lastInteract = Date.now(); });

// ── Render loop ────────────────────────────────────────────────────────
function animate() {
  requestAnimationFrame(animate);
  controls.autoRotate = (Date.now() - lastInteract > 3000);
  controls.update();
  renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// Expose for debugging
window.scene = scene;
window.camera = camera;
window.controls = controls;
</script>
</body>
</html>
'''


def main():
    buffers = build_buffers()
    n_atoms = buffers.pop('n_atoms')
    n_bonds = buffers.pop('n_bonds')

    data_json = json.dumps(buffers, separators=(',', ':'))

    html = (HTML_TEMPLATE
            .replace('__DATA_JSON__', data_json)
            .replace('__N_ATOMS__', str(n_atoms))
            .replace('__N_BONDS__', str(n_bonds))
            .replace('__N_CELLS__', str(N_CELLS)))

    out_path = '/home/user/Ouroboros/core/visual/diamond_lattice.html'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)

    size_kb = os.path.getsize(out_path) / 1024
    print(f'Wrote {out_path}')
    print(f'  size: {size_kb:.1f} KB')
    print(f'  atoms: {n_atoms}')
    print(f'  bonds: {n_bonds}')
    print(f'  unit cells: {N_CELLS}^3 = {N_CELLS**3}')
    print(f'  bond length: {NN_DIST:.4f} (a*sqrt(3)/4)')
    print(f'  sphere radius: {SPHERE_RADIUS}')


if __name__ == '__main__':
    main()
