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
<title>Diamond lattice - invariant skeleton</title>
<style>
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; background: #030508; color: #c8d0e0;
               font-family: -apple-system, 'Segoe UI', Roboto, Georgia, serif;
               overflow: hidden; }
  canvas { display: block; }

  /* Vignette overlay — softens edges, focuses center */
  #vignette { position: fixed; inset: 0; pointer-events: none;
              background: radial-gradient(ellipse at center,
                          transparent 30%, rgba(0,0,0,0.6) 100%);
              z-index: 2; }

  /* Info panel — fades in/out gracefully */
  #info { position: fixed; top: 24px; left: 24px; font-size: 12px;
          max-width: 380px; line-height: 1.6; z-index: 10;
          color: rgba(232, 236, 245, 0.78);
          transition: opacity 1.5s ease-out;
          pointer-events: none; user-select: none; }
  #info.faded { opacity: 0.25; }
  #info h1 { margin: 0 0 8px; font-size: 14px; font-weight: 500;
             color: rgba(255,255,255,0.92); letter-spacing: 0.5px; }
  #info .sub { font-size: 11px; opacity: 0.7; margin-top: 4px;
               font-family: 'SF Mono', Menlo, monospace; }

  /* Stats — minimal bottom-left */
  #stats { position: fixed; bottom: 20px; left: 24px; font-size: 10px;
           opacity: 0.35; font-family: 'SF Mono', Menlo, monospace;
           letter-spacing: 0.5px; z-index: 10;
           transition: opacity 0.5s; pointer-events: none; }
  #stats:hover { opacity: 0.7; }

  /* Controls — subtle bottom-right icons */
  #controls { position: fixed; bottom: 20px; right: 24px; z-index: 10;
              display: flex; gap: 12px; }
  .ctrl-btn { width: 32px; height: 32px; border: 1px solid rgba(255,255,255,0.15);
              background: rgba(0,0,0,0.3); border-radius: 50%;
              color: rgba(255,255,255,0.5); cursor: pointer;
              display: flex; align-items: center; justify-content: center;
              transition: all 0.2s; font-size: 13px;
              backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); }
  .ctrl-btn:hover { color: rgba(255,255,255,0.9);
                    border-color: rgba(255,255,255,0.4);
                    background: rgba(255,255,255,0.08); }
  .ctrl-btn:active { transform: scale(0.93); }

  /* Loading state */
  #loading { position: fixed; inset: 0; background: #030508;
             display: flex; align-items: center; justify-content: center;
             z-index: 100; transition: opacity 1s; }
  #loading.gone { opacity: 0; pointer-events: none; }
  #loading-dot { width: 6px; height: 6px; border-radius: 50%;
                 background: #88aaff; opacity: 0.6;
                 animation: pulse 1.4s ease-in-out infinite; }
  @keyframes pulse {
    0%, 100% { opacity: 0.2; transform: scale(0.8); }
    50% { opacity: 0.9; transform: scale(1.4); }
  }
</style>
</head>
<body>

<div id="loading"><div id="loading-dot"></div></div>

<div id="info">
  <h1>Diamond lattice</h1>
  Vertex-transitive sp³ tetrahedral coordination.<br>
  Invariant skeleton — substrate-cousin of A₀-locked structural form.
  <div class="sub">Fd-3m · space group 227</div>
</div>

<div id="stats">
  __N_ATOMS__ atoms · __N_BONDS__ bonds · __N_CELLS__³ unit cells
</div>

<div id="controls">
  <button class="ctrl-btn" id="btn-pause" title="Pause / resume rotation">⏸</button>
  <button class="ctrl-btn" id="btn-reset" title="Reset view">⟲</button>
  <button class="ctrl-btn" id="btn-fullscreen" title="Fullscreen">⛶</button>
</div>

<div id="vignette"></div>

<script type="importmap">
{
  "imports": {
    "three": "./lib/three.module.js",
    "three/addons/": "./lib/"
  }
}
</script>

<script type="module">
import * as THREE from 'three';
import { OrbitControls } from './lib/OrbitControls.js';
import { EffectComposer } from './lib/postprocessing/EffectComposer.js';
import { RenderPass } from './lib/postprocessing/RenderPass.js';
import { UnrealBloomPass } from './lib/postprocessing/UnrealBloomPass.js';
import { OutputPass } from './lib/postprocessing/OutputPass.js';

const DATA = __DATA_JSON__;

// ── Scene ──────────────────────────────────────────────────────────────
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x030508, 0.055);

const camera = new THREE.PerspectiveCamera(
  48, window.innerWidth / window.innerHeight, 0.1, 200
);

// Initial framing — angled view that shows tetrahedral structure
const baseDist = DATA.sphere_radius * 2.4;
const finalCameraPos = new THREE.Vector3(
  baseDist * 0.72, baseDist * 0.52, baseDist * 0.72
);
const entranceStartPos = finalCameraPos.clone().multiplyScalar(3.5);

camera.position.copy(entranceStartPos);
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({
  antialias: true,
  powerPreference: 'high-performance'
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setClearColor(0x030508, 1);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 0.85;
document.body.appendChild(renderer.domElement);

// ── Post-processing: UnrealBloomPass for AA-VFX-style glow ──────────────
const composer = new EffectComposer(renderer);
composer.setSize(window.innerWidth, window.innerHeight);
composer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

const renderPass = new RenderPass(scene, camera);
composer.addPass(renderPass);

const bloomPass = new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  1.4,    // strength
  0.65,   // radius
  0.0     // threshold (everything blooms)
);
composer.addPass(bloomPass);

const outputPass = new OutputPass();
composer.addPass(outputPass);

// ── Procedural gaussian point sprite ────────────────────────────────────
function makeGaussianSprite(size = 128) {
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = size;
  const ctx = canvas.getContext('2d');
  const g = ctx.createRadialGradient(
    size/2, size/2, 0, size/2, size/2, size/2
  );
  g.addColorStop(0.00, 'rgba(255,255,255,1.0)');
  g.addColorStop(0.12, 'rgba(255,255,255,0.95)');
  g.addColorStop(0.30, 'rgba(220,235,255,0.5)');
  g.addColorStop(0.55, 'rgba(150,180,255,0.15)');
  g.addColorStop(1.00, 'rgba(80,120,255,0.0)');
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, size, size);
  const tex = new THREE.CanvasTexture(canvas);
  tex.needsUpdate = true;
  return tex;
}

const spriteTex = makeGaussianSprite();

// ── Atoms: glowing point sprites ───────────────────────────────────────
const atomsGeo = new THREE.BufferGeometry();
atomsGeo.setAttribute('position',
  new THREE.Float32BufferAttribute(DATA.atoms_positions, 3));
atomsGeo.setAttribute('color',
  new THREE.Float32BufferAttribute(DATA.atoms_colors, 3));

const atomsMat = new THREE.PointsMaterial({
  size: 0.28,
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
controls.dampingFactor = 0.05;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.35;
controls.minDistance = 0.5;
controls.maxDistance = DATA.sphere_radius * 5;
controls.target.set(0, 0, 0);
controls.enabled = false;  // disable during entrance

let lastInteract = 0;
let autoRotatePaused = false;
controls.addEventListener('start', () => { lastInteract = Date.now(); });

// ── Entrance animation ─────────────────────────────────────────────────
let entranceT = 0;
const ENTRANCE_DURATION = 2.8;  // seconds

function easeOutQuint(t) {
  return 1 - Math.pow(1 - t, 5);
}

// ── UI controls ────────────────────────────────────────────────────────
const btnPause = document.getElementById('btn-pause');
const btnReset = document.getElementById('btn-reset');
const btnFullscreen = document.getElementById('btn-fullscreen');
const infoPanel = document.getElementById('info');

btnPause.addEventListener('click', () => {
  autoRotatePaused = !autoRotatePaused;
  btnPause.textContent = autoRotatePaused ? '▶' : '⏸';
  btnPause.title = autoRotatePaused ? 'Resume rotation' : 'Pause rotation';
});

btnReset.addEventListener('click', () => {
  // Smooth interpolate camera back to initial position
  resetT = 0;
  resetStartPos = camera.position.clone();
  resetting = true;
  lastInteract = Date.now();
});

btnFullscreen.addEventListener('click', () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen();
  } else {
    document.exitFullscreen();
  }
});

let resetting = false;
let resetT = 0;
let resetStartPos = new THREE.Vector3();
const RESET_DURATION = 1.2;

// Fade info panel after delay
setTimeout(() => infoPanel.classList.add('faded'), 5500);

// Show info on mouse near top-left
document.addEventListener('mousemove', (e) => {
  if (e.clientX < 420 && e.clientY < 220) {
    infoPanel.classList.remove('faded');
  } else {
    if (Date.now() - lastInteract > 1000) {
      infoPanel.classList.add('faded');
    }
  }
});

// ── Hide loading screen after first frame ──────────────────────────────
let firstFrameRendered = false;

// ── Render loop ────────────────────────────────────────────────────────
const clock = new THREE.Clock();

function animate() {
  requestAnimationFrame(animate);
  const dt = clock.getDelta();

  // Entrance animation
  if (entranceT < 1) {
    entranceT += dt / ENTRANCE_DURATION;
    if (entranceT >= 1) {
      entranceT = 1;
      controls.enabled = true;
    }
    const e = easeOutQuint(Math.min(entranceT, 1));
    camera.position.lerpVectors(entranceStartPos, finalCameraPos, e);
    camera.lookAt(0, 0, 0);
  }

  // Reset animation
  if (resetting) {
    resetT += dt / RESET_DURATION;
    if (resetT >= 1) {
      resetT = 1;
      resetting = false;
    }
    const e = easeOutQuint(Math.min(resetT, 1));
    camera.position.lerpVectors(resetStartPos, finalCameraPos, e);
    camera.lookAt(0, 0, 0);
  }

  // Auto-rotate logic
  const shouldAutoRotate = !autoRotatePaused
    && !resetting
    && entranceT >= 1
    && (Date.now() - lastInteract > 3000);
  controls.autoRotate = shouldAutoRotate;

  controls.update();
  composer.render();

  // Hide loading after first frame
  if (!firstFrameRendered) {
    firstFrameRendered = true;
    setTimeout(() => {
      document.getElementById('loading').classList.add('gone');
    }, 200);
  }
}
animate();

// ── Resize ─────────────────────────────────────────────────────────────
window.addEventListener('resize', () => {
  const w = window.innerWidth, h = window.innerHeight;
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h);
  composer.setSize(w, h);
});

// ── Expose for debugging ───────────────────────────────────────────────
window.scene = scene;
window.camera = camera;
window.controls = controls;
window.composer = composer;
window.bloomPass = bloomPass;
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
