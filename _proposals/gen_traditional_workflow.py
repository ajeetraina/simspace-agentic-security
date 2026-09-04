#!/usr/bin/env python3
"""Generate the 'Traditional Workflow' loop slide that precedes slide-07.webp
('The Agentic Workflow'). Same Inner/Outer loops, but a developer (human) sits
at every stage instead of an agent. Renders SVG -> PNG (rsvg-convert) -> webp."""
import math, subprocess, os

W, H = 2000, 1125
BLUE = "#24467f"       # loop arrow navy (approx match to slide-07)
INK = "#111827"        # title black
SUB = "#334155"        # subtitle grey
LABEL = "#4b5563"      # stage label grey
LOOP_TXT = "#1f2937"   # "Inner/Outer Loop" text
SKIN = "#1f3a63"       # person icon fill

def arc_point(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)

def loop(cx, cy, r, sw):
    """4 chunky clockwise arc segments with arrowheads -> a rotating loop."""
    out = []
    seg, gap = 90, 16
    for k in range(4):
        start = k * seg - 90 + 4
        end = start + seg - gap
        x0, y0 = arc_point(cx, cy, r, start)
        x1, y1 = arc_point(cx, cy, r, end)
        out.append(
            f'<path d="M {x0:.1f} {y0:.1f} A {r} {r} 0 0 1 {x1:.1f} {y1:.1f}" '
            f'fill="none" stroke="{BLUE}" stroke-width="{sw}" stroke-linecap="round"/>')
        tang = end + 90
        ah = sw * 1.7
        t = math.radians(tang)
        tipx, tipy = x1 + ah * math.cos(t), y1 + ah * math.sin(t)
        p = math.radians(tang + 90)
        b1x, b1y = x1 + ah * 0.7 * math.cos(p), y1 + ah * 0.7 * math.sin(p)
        b2x, b2y = x1 - ah * 0.7 * math.cos(p), y1 - ah * 0.7 * math.sin(p)
        out.append(f'<polygon points="{tipx:.1f},{tipy:.1f} {b1x:.1f},{b1y:.1f} '
                   f'{b2x:.1f},{b2y:.1f}" fill="{BLUE}"/>')
    return "\n".join(out)

def person(cx, cy, s=1.0):
    head_r = 15 * s
    hy = cy - 20 * s
    body = (f'<path d="M {cx-26*s:.1f} {cy+28*s:.1f} '
            f'C {cx-26*s:.1f} {cy-2*s:.1f} {cx-14*s:.1f} {cy+2*s:.1f} {cx:.1f} {cy+2*s:.1f} '
            f'C {cx+14*s:.1f} {cy+2*s:.1f} {cx+26*s:.1f} {cy-2*s:.1f} {cx+26*s:.1f} {cy+28*s:.1f} Z" '
            f'fill="{SKIN}"/>')
    head = f'<circle cx="{cx:.1f}" cy="{hy:.1f}" r="{head_r:.1f}" fill="{SKIN}"/>'
    return f'<g>{head}{body}</g>'

def label(cx, cy, text, size=34):
    return (f'<text x="{cx:.0f}" y="{cy:.0f}" text-anchor="middle" '
            f'font-size="{size}" font-weight="600" fill="{LABEL}">{text}</text>')

s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
     f'font-family="Helvetica, Arial, sans-serif">',
     f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
     f'<text x="110" y="130" font-size="78" font-weight="800" fill="{INK}">The Traditional Workflow</text>',
     f'<text x="112" y="205" font-size="40" fill="{SUB}">A human writes, reviews, and ships at every stage. The attack surface is</text>',
     f'<text x="112" y="255" font-size="40" fill="{SUB}">only what <tspan font-weight="700">you</tspan> choose to pull.</text>']

def stage(cx, cy, r, deg, name, scale, loff):
    """Person on the ring at `deg`, with its label further out along the same angle."""
    px, py = arc_point(cx, cy, r + 82, deg)
    lx, ly = arc_point(cx, cy, r + 82 + loff, deg)
    return person(px, py, scale) + "\n" + label(lx, ly + 10, name)

# Inner loop -- Code / Build / Test / Open Source (east left open for Push)
icx, icy, ir = 700, 665, 155
s.append(loop(icx, icy, ir, 26))
s.append(f'<text x="{icx}" y="{icy-6}" text-anchor="middle" font-size="46" fill="{LOOP_TXT}">Inner</text>')
s.append(f'<text x="{icx}" y="{icy+44}" text-anchor="middle" font-size="46" fill="{LOOP_TXT}">Loop</text>')
for deg, name in [(-90, "Build"), (45, "Test"), (135, "Open Source"), (180, "Code")]:
    s.append(stage(icx, icy, ir, deg, name, 1.05, 95))

# Outer loop -- Integrate / Test / Deploy (west left open where Push enters)
ocx, ocy, orad = 1360, 665, 210
s.append(loop(ocx, ocy, orad, 30))
s.append(f'<text x="{ocx}" y="{ocy-6}" text-anchor="middle" font-size="52" fill="{LOOP_TXT}">Outer</text>')
s.append(f'<text x="{ocx}" y="{ocy+50}" text-anchor="middle" font-size="52" fill="{LOOP_TXT}">Loop</text>')
for deg, name in [(-90, "Integrate"), (0, "Test"), (90, "Deploy")]:
    s.append(stage(ocx, ocy, orad, deg, name, 1.12, 100))

# Push connector between the loops
mx = (icx + ir + ocx - orad) / 2
s.append(f'<g stroke="{BLUE}" stroke-width="16" stroke-linecap="round" fill="{BLUE}">'
         f'<line x1="{icx+ir+34}" y1="{icy}" x2="{ocx-orad-46}" y2="{ocy}"/>'
         f'<polygon points="{ocx-orad-46},{ocy-18} {ocx-orad-16},{ocy} {ocx-orad-46},{ocy+18}"/></g>')
s.append(label(mx, icy - 34, "Push"))

s.append('</svg>')

out_dir = os.path.dirname(os.path.abspath(__file__))
svg_path = os.path.join(out_dir, "traditional-workflow.svg")
png_path = os.path.join(out_dir, "traditional-workflow.png")
webp_path = os.path.join(out_dir, "slide-06b.webp")
with open(svg_path, "w") as f:
    f.write("\n".join(s))
subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), svg_path, "-o", png_path], check=True)
from PIL import Image
Image.open(png_path).convert("RGB").save(webp_path, "WEBP", quality=92, method=6)
print("wrote", webp_path)
