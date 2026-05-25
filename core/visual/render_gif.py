"""
Render core kernel visual surface as animated GIF.

Composition (matches core/visual/kernel.html):
- Sierpinski triangulation background (self-similarity)
- Borromean rings at center (3-slot mutual constraint)
- Z/3 marker orbits (ThreePeriod canonical action)
- A_0 halo pulse at center (forced unique stable point)

Designed for white README background. Anti-aliased via 2x supersampling.
Loops cleanly: all rotations complete 120° per loop, indistinguishable
from full cycle due to 3-fold rotational symmetry of triangle.
"""

from PIL import Image, ImageDraw, ImageFont
import math

# ── Output parameters ───────────────────────────────────────────────────────
OUT_W = OUT_H = 400              # final GIF resolution
SS = 2                            # supersampling factor (render at SS×, downscale)
W = OUT_W * SS
H = OUT_H * SS
cx, cy = W / 2, H / 2

LOOP_SEC = 6.0                    # one full visual cycle (meditative pace)
FPS = 10                          # 60 frames total
N_FRAMES = int(LOOP_SEC * FPS)
FRAME_MS = int(1000 / FPS)

# ── Palette for white/paper background ──────────────────────────────────────
BG = (252, 251, 247)              # warm paper white
SIERPINSKI = (90, 100, 130)       # dusty slate-blue
Z3_DOT = (70, 75, 95)             # dark slate
A0_AMBER = (180, 130, 50)         # warm amber for A_0 pulse
A0_LABEL = (90, 90, 100)
LABEL_COLOR = (60, 60, 70)

# Borromean rings — muted, paper-friendly
RING_COLORS = [
    (190, 75, 65),    # B — terracotta
    (60, 140, 95),    # P — sage
    (60, 100, 165),   # I — slate blue
]
RING_LABELS = ['B', 'P', 'I']

# ── Sierpinski (self-similar fractal background) ────────────────────────────
def sierpinski(draw, p1, p2, p3, depth, alpha, line_w):
    """Recursive triangulation outline — fading at deeper levels."""
    if depth == 0 or alpha < 0.015:
        return
    rgba = SIERPINSKI + (int(255 * alpha),)
    draw.line([p1, p2, p3, p1], fill=rgba, width=line_w)
    m12 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    m23 = ((p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2)
    m31 = ((p3[0] + p1[0]) / 2, (p3[1] + p1[1]) / 2)
    next_w = max(1, line_w - 1) if depth < 5 else line_w
    sierpinski(draw, p1, m12, m31, depth - 1, alpha * 0.78, next_w)
    sierpinski(draw, m12, p2, m23, depth - 1, alpha * 0.78, next_w)
    sierpinski(draw, m31, m23, p3, depth - 1, alpha * 0.78, next_w)


def z3_orbit(draw, angle, scale, alpha):
    """Three small markers at 120° around center, orbiting."""
    r = 245 * SS * scale
    for k in range(3):
        a = angle + k * (2 * math.pi / 3)
        x = cx + r * math.cos(a)
        y = cy + r * math.sin(a)
        rgba = Z3_DOT + (int(255 * alpha),)
        rad = 4 * SS
        draw.ellipse([x - rad, y - rad, x + rad, y + rad], fill=rgba)


def draw_borromean(draw, font_label):
    """Three rings at 120° around center, woven via arc-overlay illusion."""
    ring_r = min(W, H) * 0.125
    offset = ring_r * 0.55
    centers = []
    for k in range(3):
        a = -math.pi / 2 + k * (2 * math.pi / 3)
        rx = cx + offset * math.cos(a)
        ry = cy + offset * math.sin(a)
        centers.append((rx, ry, a))

    base_w = 3 * SS

    # Pass 1: each full ring at low alpha — the "under" layer
    for k, (rx, ry, _) in enumerate(centers):
        rgba = RING_COLORS[k] + (110,)
        for w in range(base_w):
            r = ring_r - base_w / 2 + w
            draw.ellipse(
                [rx - r, ry - r, rx + r, ry + r],
                outline=rgba, width=1
            )

    # Pass 2: top-arc at higher alpha to fake the weave
    for k, (rx, ry, label_a) in enumerate(centers):
        rgba = RING_COLORS[k] + (230,)
        start_a = math.degrees(label_a - math.pi / 3)
        end_a = math.degrees(label_a + math.pi / 3)
        for w in range(base_w + 1):
            r_off = w - base_w / 2
            bbox = [
                rx - ring_r - r_off, ry - ring_r - r_off,
                rx + ring_r + r_off, ry + ring_r + r_off
            ]
            draw.arc(bbox, start=start_a, end=end_a, fill=rgba, width=1)

    # Labels at the outer edge of each ring
    for k, (rx, ry, label_a) in enumerate(centers):
        label_x = rx + ring_r * 1.42 * math.cos(label_a)
        label_y = ry + ring_r * 1.42 * math.sin(label_a)
        text = RING_LABELS[k]
        bbox = font_label.getbbox(text)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(
            (label_x - tw / 2, label_y - th / 2),
            text, fill=LABEL_COLOR + (240,), font=font_label
        )


def draw_a0_center(draw, font, pulse):
    """A_0 marker at center with pulsing halo."""
    # Outer halo: radius modulated by pulse
    halo_r = (4 + 6 * pulse) * SS
    halo_alpha = int(60 * (1.0 - pulse * 0.5))
    halo_rgba = A0_AMBER + (halo_alpha,)
    draw.ellipse(
        [cx - halo_r, cy - halo_r, cx + halo_r, cy + halo_r],
        fill=halo_rgba
    )

    # Inner dot: stable brightness
    inner_r = 3.5 * SS
    draw.ellipse(
        [cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r],
        fill=A0_AMBER + (230,)
    )

    # Label below
    text = 'A₀'
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    draw.text(
        (cx - tw / 2, cy + 14 * SS),
        text, fill=A0_LABEL + (200,), font=font
    )


def _load_fonts():
    """Try system fonts; fall back to default."""
    paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
        '/usr/share/fonts/TTF/DejaVuSans.ttf',
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, 14 * SS), ImageFont.truetype(p, 11 * SS)
        except (OSError, IOError):
            continue
    return ImageFont.load_default(), ImageFont.load_default()


def render_frame(t, font_label, font_small):
    """Render one frame at normalised time t ∈ [0, 1)."""
    # Render at SS× resolution, then downscale with LANCZOS for AA
    img = Image.new('RGBA', (W, H), color=BG + (255,))
    draw = ImageDraw.Draw(img)

    # Sierpinski: 120° rotation per loop (Z/3 → looks like full cycle)
    rot = t * (2 * math.pi / 3) - math.pi / 2
    R = min(W, H) * 0.43
    verts = [
        (cx + R * math.cos(rot + k * 2 * math.pi / 3),
         cy + R * math.sin(rot + k * 2 * math.pi / 3))
        for k in range(3)
    ]
    sierpinski(draw, verts[0], verts[1], verts[2],
               depth=7, alpha=0.45, line_w=1 * SS)

    # Z/3 markers: two orbits, opposite direction, different scale
    z3_orbit(draw, t * (2 * math.pi / 3) - math.pi / 2,
             scale=1.0, alpha=0.45)
    z3_orbit(draw, -t * (2 * math.pi / 3) + 0.3,
             scale=0.55, alpha=0.30)

    # Borromean rings + labels (static topology, time-independent)
    draw_borromean(draw, font_label)

    # A_0 pulse: 3 pulses per loop for 3-fold rhythm
    pulse_raw = math.sin(t * 2 * math.pi * 3)
    pulse = 0.5 + 0.5 * pulse_raw
    draw_a0_center(draw, font_small, pulse)

    # Downscale to output resolution with anti-aliasing
    out = img.resize((OUT_W, OUT_H), Image.LANCZOS)
    return out.convert('RGB')


def main():
    font_label, font_small = _load_fonts()
    print(f'Rendering {N_FRAMES} frames at {OUT_W}×{OUT_H} '
          f'({LOOP_SEC}s loop @ {FPS} fps, {SS}× supersample)...')
    frames = []
    for i in range(N_FRAMES):
        t = i / N_FRAMES
        frame = render_frame(t, font_label, font_small)
        # No dithering: dither-noise kills inter-frame compression
        frame_p = frame.quantize(
            colors=48,
            method=Image.Quantize.MEDIANCUT,
            dither=Image.Dither.NONE,
        )
        frames.append(frame_p)
        if i % 20 == 0:
            print(f'  frame {i}/{N_FRAMES}')

    out_path = '/home/user/Ouroboros/core/visual/kernel.gif'
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_MS,
        loop=0,
        optimize=True,
        disposal=2,
    )
    import os
    size_kb = os.path.getsize(out_path) / 1024
    print(f'Wrote {out_path}')
    print(f'  size: {size_kb:.1f} KB')
    print(f'  frames: {N_FRAMES} @ {FRAME_MS}ms = {LOOP_SEC}s loop')


if __name__ == '__main__':
    main()
