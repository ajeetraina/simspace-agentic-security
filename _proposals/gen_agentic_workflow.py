#!/usr/bin/env python3
"""Regenerate slide-07.webp ('The Agentic Workflow') as the twin of the new
Traditional Workflow slide: same Inner/Outer loops, but an AI agent sits at
every stage. Trimmed subtitle. Renders SVG -> PNG (rsvg-convert) -> webp."""
import math, subprocess, os

W, H = 2000, 1125
BLUE = "#24467f"
INK = "#111827"
SUB = "#334155"
LABEL = "#4b5563"
LOOP_TXT = "#1f2937"
BOT = "#1f3a63"        # robot body navy
SCREEN = "#16a34a"     # green "AI" screen (echoes original)

def arc_point(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)

def loop(cx, cy, r, sw):
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

def robot(cx, cy, s=1.0):
    """Simple AI-agent glyph: antenna + head with green screen + ears + base."""
    hw, hh = 30 * s, 26 * s
    p = []
    p.append(f'<line x1="{cx:.1f}" y1="{cy-hh-14*s:.1f}" x2="{cx:.1f}" y2="{cy-hh:.1f}" '
             f'stroke="{BOT}" stroke-width="{3*s:.1f}"/>')
    p.append(f'<circle cx="{cx:.1f}" cy="{cy-hh-16*s:.1f}" r="{4.5*s:.1f}" fill="{BOT}"/>')
    p.append(f'<rect x="{cx-hw-8*s:.1f}" y="{cy-6*s:.1f}" width="{8*s:.1f}" height="{18*s:.1f}" rx="{3*s:.1f}" fill="{BOT}"/>')
    p.append(f'<rect x="{cx+hw:.1f}" y="{cy-6*s:.1f}" width="{8*s:.1f}" height="{18*s:.1f}" rx="{3*s:.1f}" fill="{BOT}"/>')
    p.append(f'<rect x="{cx-hw:.1f}" y="{cy-hh:.1f}" width="{2*hw:.1f}" height="{2*hh:.1f}" rx="{8*s:.1f}" fill="{BOT}"/>')
    sw_, sh_ = 34 * s, 22 * s
    p.append(f'<rect x="{cx-sw_/2:.1f}" y="{cy-sh_/2:.1f}" width="{sw_:.1f}" height="{sh_:.1f}" rx="{4*s:.1f}" fill="{SCREEN}"/>')
    p.append(f'<text x="{cx:.1f}" y="{cy+6*s:.1f}" text-anchor="middle" font-size="{15*s:.1f}" '
             f'font-weight="800" fill="#052e16">AI</text>')
    return f'<g>{"".join(p)}</g>'

def label(cx, cy, text, size=34):
    return (f'<text x="{cx:.0f}" y="{cy:.0f}" text-anchor="middle" '
            f'font-size="{size}" font-weight="600" fill="{LABEL}">{text}</text>')

def stage(cx, cy, r, deg, name, scale, loff):
    px, py = arc_point(cx, cy, r + 88, deg)
    lx, ly = arc_point(cx, cy, r + 88 + loff, deg)
    return robot(px, py, scale) + "\n" + label(lx, ly + 10, name)

s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
     f'font-family="Helvetica, Arial, sans-serif">',
     f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
     f'<text x="110" y="130" font-size="78" font-weight="800" fill="{INK}">The Agentic Workflow</text>',
     f'<text x="112" y="205" font-size="40" fill="{SUB}">Now an agent sits at <tspan font-weight="700">every</tspan> stage - the attack surface is no</text>',
     f'<text x="112" y="255" font-size="40" fill="{SUB}">longer just what you pull.</text>']

# Inner loop -- Code / Build / Test / Open Source (east open for Push)
icx, icy, ir = 700, 665, 155
s.append(loop(icx, icy, ir, 26))
s.append(f'<text x="{icx}" y="{icy-6}" text-anchor="middle" font-size="46" fill="{LOOP_TXT}">Inner</text>')
s.append(f'<text x="{icx}" y="{icy+44}" text-anchor="middle" font-size="46" fill="{LOOP_TXT}">Loop</text>')
for deg, name in [(-90, "Build"), (45, "Test"), (135, "Open Source"), (180, "Code")]:
    s.append(stage(icx, icy, ir, deg, name, 0.92, 92))

# Outer loop -- Integrate / Test / Deploy (west open where Push enters)
ocx, ocy, orad = 1360, 665, 210
s.append(loop(ocx, ocy, orad, 30))
s.append(f'<text x="{ocx}" y="{ocy-6}" text-anchor="middle" font-size="52" fill="{LOOP_TXT}">Outer</text>')
s.append(f'<text x="{ocx}" y="{ocy+50}" text-anchor="middle" font-size="52" fill="{LOOP_TXT}">Loop</text>')
for deg, name in [(-90, "Integrate"), (0, "Test"), (90, "Deploy")]:
    s.append(stage(ocx, ocy, orad, deg, name, 1.0, 96))

# Push connector between the loops
mx = (icx + ir + ocx - orad) / 2
s.append(f'<g stroke="{BLUE}" stroke-width="16" stroke-linecap="round" fill="{BLUE}">'
         f'<line x1="{icx+ir+34}" y1="{icy}" x2="{ocx-orad-46}" y2="{ocy}"/>'
         f'<polygon points="{ocx-orad-46},{ocy-18} {ocx-orad-16},{ocy} {ocx-orad-46},{ocy+18}"/></g>')
s.append(label(mx, icy - 34, "Push"))

s.append('</svg>')

out_dir = os.path.dirname(os.path.abspath(__file__))
svg_path = os.path.join(out_dir, "agentic-workflow.svg")
png_path = os.path.join(out_dir, "agentic-workflow.png")
webp_path = os.path.join(out_dir, "slide-07b.webp")
with open(svg_path, "w") as f:
    f.write("\n".join(s))
subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), svg_path, "-o", png_path], check=True)
from PIL import Image
Image.open(png_path).convert("RGB").save(webp_path, "WEBP", quality=92, method=6)
print("wrote", webp_path)
