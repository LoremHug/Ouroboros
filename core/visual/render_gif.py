"""
Render core kernel visual surface as animated GIF.

Same composition as core/visual/kernel.html (without interactivity):
- Sierpinski triangulation background (self-similarity)
- Borromean rings at center (3-slot mutual constraint)
- Z/3 marker orbits (ThreePeriod canonical action)
- A_0 pulse at center (forced unique stable point)

Loops cleanly via 3-fold rotational symmetry: all rotations complete
exactly 1/3 cycle per loop, indistinguishable from full cycle due to
triangle's Z/3 symmetry.
"""

from PIL import Image, ImageDraw, ImageFont
import math

# ── Parameters ──────────────────────────────────────────────────────────────
W = H = 720
cx, cy = W / 2, H / 2
N_FRAMES = 60
FRAME_MS = 50  # 3 s loop

BG = (10, 10, 10)
SIERPINSKI_COLOR = (80, 100, 140)   # bluish grey
Z3_COLOR = (180, 200, 240)          # pale blue-violet
A0_COLOR_BRIGHT = (255, 240, 200)   # warm cream
A0_LABEL_COLOR = (180, 180, 180)

# Ring colors B, P, I — distinguishable hues
RING_COLORS = [
    (255, 120, 110),   # B — red
    (120, 200, 140),   # P — green
    (120, 160, 255),   # I — blue
]
RING_LABELS = ['B', 'P', 'I']


def sierpinski(draw, ax, ay, bx, by, cx_, cy_, depth, alpha):
    """Recursive Sierpinski triangle outline."""
    if depth == 0 or alpha < 0.02:
        return
    rgba = SIERPINSKI_COLOR + (int(255 * alpha),)
    draw.line([(ax, ay), (bx, by), (cx_, cy_), (ax, ay)],
              fill=rgba, width=1)
    mAB = ((ax + bx) / 2, (ay + by) / 2)
    mBC = ((bx + cx_) / 2, (by + cy_) / 2)
    mCA = ((cx_ + ax) / 2, (cy_ + ay) / 2)
    sierpinski(draw, ax, ay, mAB[0], mAB[1], mCA[0], mCA[1],
               depth - 1, alpha * 0.85)
    sierpinski(draw, mAB[0], mAB[1], bx, by, mBC[0], mBC[1],
               depth - 1, alpha * 0.85)
    sierpinski(draw, mCA[0], mCA[1], mBC[0], mBC[1], cx_, cy_,
               depth - 1, alpha * 0.85)


def z3_orbit(draw, angle, scale):
    """Three small markers at 120° around center, orbiting."""
    r = 280 * scale
    for k in range(3):
        a = angle + k * (2 * math.pi / 3)
        x = cx + r * math.cos(a)
        y = cy + r * math.sin(a)
        rgba = Z3_COLOR + (90,)
        draw.ellipse([x - 3.5, y - 3.5, x + 3.5, y + 3.5], fill=rgba)


def draw_borromean(draw, font, font_label):
    """Three rings at 120° around center, with weave illusion."""
    ring_r = min(W, H) * 0.13
    offset = ring_r * 0.55
    centers = []
    for k in range(3):
        a = -math.pi / 2 + k * (2 * math.pi / 3)
        rx = cx + offset * math.cos(a)
        ry = cy + offset * math.sin(a)
        centers.append((rx, ry, a))

    # Pass 1: each full ring at lower alpha
    for k, (rx, ry, _) in enumerate(centers):
        rgba = RING_COLORS[k] + (90,)
        # Draw ring as annulus by stroking
        for w in range(6):
            r = ring_r - 3 + w
            draw.ellipse([rx - r, ry - r, rx + r, ry + r],
                         outline=rgba, width=1)

    # Pass 2: top-arcs at full opacity to fake the weave
    for k, (rx, ry, label_a) in enumerate(centers):
        rgba = RING_COLORS[k] + (240,)
        start_a = math.degrees(label_a - math.pi / 3)
        end_a = math.degrees(label_a + math.pi / 3)
        # PIL arc draws clockwise from positive-x axis at degree 0
        bbox = [rx - ring_r - 3, ry - ring_r - 3,
                rx + ring_r + 3, ry + ring_r + 3]
        # Draw a thick arc by overlaying several arc strokes
        for w in range(7):
            r_off = w - 3
            bbox_w = [rx - ring_r - r_off, ry - ring_r - r_off,
                      rx + ring_r + r_off, ry + ring_r + r_off]
            draw.arc(bbox_w, start=start_a, end=end_a,
                     fill=rgba, width=1)

    # Labels for each ring
    for k, (rx, ry, label_a) in enumerate(centers):
        label_x = rx + ring_r * 1.45 * math.cos(label_a)
        label_y = ry + ring_r * 1.45 * math.sin(label_a)
        text = RING_LABELS[k]
        bbox = font_label.getbbox(text)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((label_x - tw / 2, label_y - th / 2),
                  text, fill=(220, 220, 220, 230), font=font_label)


def draw_a0_center(draw, font, pulse):
    """A_0 marker at center with pulsing brightness."""
    intensity = int(255 * pulse)
    r, g, b = A0_COLOR_BRIGHT
    color = (r, g, b, intensity)
    radius = 5
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                 fill=color)
    # Label below
    text = 'A_0'
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw / 2, cy + 14), text,
              fill=A0_LABEL_COLOR + (200,), font=font)


def _load_font():
    """Try a few system font paths; fall back to default."""
    candidates = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/TTF/DejaVuSansMono.ttf',
    ]
    for path in candidates:
        try:
            font_label = ImageFont.truetype(path, 16)
            font_small = ImageFont.truetype(path, 11)
            return font_label, font_small
        except (OSError, IOError):
            continue
    # Fallback
    return ImageFont.load_default(), ImageFont.load_default()


def render_frame(t, font_label, font_small):
    """Render one frame at normalised time t ∈ [0, 1)."""
    img = Image.new('RGBA', (W, H), color=BG + (255,))
    draw = ImageDraw.Draw(img)

    # Sierpinski rotation: 1/3 cycle per loop (Z/3 symmetry → looks full)
    rot = t * (2 * math.pi / 3) - math.pi / 2
    R = min(W, H) * 0.44
    verts = []
    for k in range(3):
        a = rot + k * (2 * math.pi / 3)
        verts.append((cx + R * math.cos(a), cy + R * math.sin(a)))
    sierpinski(draw, verts[0][0], verts[0][1],
               verts[1][0], verts[1][1],
               verts[2][0], verts[2][1],
               depth=7, alpha=0.55)

    # Z/3 markers: two orbits, opposite rotations
    z3_orbit(draw, t * (2 * math.pi / 3) - math.pi / 2, scale=1.0)
    z3_orbit(draw, -t * (2 * math.pi / 3) - math.pi / 2 + 0.4, scale=0.55)

    # Borromean rings + labels
    draw_borromean(draw, font_small, font_label)

    # A_0 pulse: 3 pulses per loop (3-fold)
    pulse = 0.55 + 0.45 * math.sin(t * 2 * math.pi * 3)
    draw_a0_center(draw, font_small, pulse)

    return img.convert('RGB')


def main():
    font_label, font_small = _load_font()
    frames = []
    for i in range(N_FRAMES):
        t = i / N_FRAMES
        frame = render_frame(t, font_label, font_small)
        # Convert to palette mode for smaller GIF
        frame_p = frame.convert('P', palette=Image.Palette.ADAPTIVE,
                                colors=128)
        frames.append(frame_p)
        if i % 10 == 0:
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
    print(f'Wrote {out_path} ({size_kb:.1f} KB, {N_FRAMES} frames @ {FRAME_MS}ms)')


if __name__ == '__main__':
    main()
