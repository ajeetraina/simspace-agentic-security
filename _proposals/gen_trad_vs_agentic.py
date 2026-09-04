#!/usr/bin/env python3
"""Regenerate slide-06.webp as a flat-style 'Traditional vs Agentic Developer
Workflow' comparison (two columns + blast-radius quote). SVG -> PNG -> webp."""
import subprocess, os

W, H = 2000, 1125
INK = "#111827"
NAVY = "#0d1b3e"       # dark card
LIGHT = "#eef2f7"      # light card
ORANGE = "#f59e0b"
GREY = "#475569"
LIGHTTXT = "#cbd5e1"
PERSON = "#1f3a63"

def person(cx, cy, s=1.0):
    hy = cy - 20 * s
    body = (f'<path d="M {cx-26*s:.1f} {cy+28*s:.1f} '
            f'C {cx-26*s:.1f} {cy-2*s:.1f} {cx-14*s:.1f} {cy+2*s:.1f} {cx:.1f} {cy+2*s:.1f} '
            f'C {cx+14*s:.1f} {cy+2*s:.1f} {cx+26*s:.1f} {cy-2*s:.1f} {cx+26*s:.1f} {cy+28*s:.1f} Z" '
            f'fill="{PERSON}"/>')
    return f'<g><circle cx="{cx:.1f}" cy="{hy:.1f}" r="{15*s:.1f}" fill="{PERSON}"/>{body}</g>'

def warn(cx, cy, s=1.0):
    p = f'{cx:.1f},{cy-13*s:.1f} {cx-13*s:.1f},{cy+9*s:.1f} {cx+13*s:.1f},{cy+9*s:.1f}'
    return (f'<g><polygon points="{p}" fill="none" stroke="{ORANGE}" stroke-width="{3*s:.1f}" '
            f'stroke-linejoin="round"/>'
            f'<line x1="{cx:.1f}" y1="{cy-4*s:.1f}" x2="{cx:.1f}" y2="{cy+2*s:.1f}" '
            f'stroke="{ORANGE}" stroke-width="{3*s:.1f}" stroke-linecap="round"/>'
            f'<circle cx="{cx:.1f}" cy="{cy+6*s:.1f}" r="{1.7*s:.1f}" fill="{ORANGE}"/></g>')

s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
     f'font-family="Helvetica, Arial, sans-serif">',
     f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
     f'<text x="110" y="128" font-size="70" font-weight="800" fill="{INK}">Traditional vs Agentic Developer Workflow</text>']

# Cards
s.append(f'<rect x="110" y="220" width="855" height="700" rx="28" fill="{LIGHT}"/>')
s.append(f'<rect x="1035" y="220" width="855" height="700" rx="28" fill="{NAVY}"/>')
s.append(f'<text x="162" y="312" font-size="34" font-weight="800" letter-spacing="1.5" fill="#0f172a">TRADITIONAL WORKFLOW</text>')
s.append(f'<text x="1087" y="312" font-size="34" font-weight="800" letter-spacing="1.5" fill="{ORANGE}">AGENTIC WORKFLOW</text>')

def bullet(icon_svg, tx, y, main, qual, main_fill, qual_fill, qual_italic, qual_bold):
    it = ' font-style="italic"' if qual_italic else ''
    fw = ' font-weight="700"' if qual_bold else ''
    return (icon_svg + f'<text x="{tx}" y="{y+9}" font-size="25" fill="{main_fill}" xml:space="preserve">'
            f'<tspan font-weight="700">{main}</tspan>'
            f'<tspan fill="{qual_fill}"> - </tspan>'
            f'<tspan fill="{qual_fill}"{it}{fw}>{qual}</tspan></text>')

# Left bullets (human)
left = [("Developer pulls base image", "manually, with intent"),
        ("Developer installs dependencies", "reviewed in a PR"),
        ("CI pipeline runs", "with human-authored config")]
y = 420
for main, qual in left:
    s.append(bullet(person(186, y, 0.6), 226, y, main, qual, "#1f2937", GREY, True, False))
    y += 92

# Right bullets (agent)
right = [("Agent pulls base image", "autonomously"),
         ("Agent installs packages", "no human review"),
         ("Agent invokes external tools", "with real credentials"),
         ("Agent modifies Dockerfile", "mid-pipeline")]
y = 420
for main, qual in right:
    s.append(bullet(warn(1112, y, 0.85), 1150, y, main, qual, LIGHTTXT, "#ffffff", False, True))
    y += 92

# Blast-radius quote
s.append(f'<rect x="110" y="968" width="6" height="46" rx="3" fill="#2563eb"/>')
s.append(f'<text x="138" y="1004" font-size="34" font-style="italic" fill="#334155">'
         f'"The better the agent, the bigger the blast radius."</text>')

s.append('</svg>')

out_dir = os.path.dirname(os.path.abspath(__file__))
svg_path = os.path.join(out_dir, "trad-vs-agentic.svg")
png_path = os.path.join(out_dir, "trad-vs-agentic.png")
webp_path = os.path.join(out_dir, "slide-06-new.webp")
with open(svg_path, "w") as f:
    f.write("\n".join(s))
subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), svg_path, "-o", png_path], check=True)
from PIL import Image
Image.open(png_path).convert("RGB").save(webp_path, "WEBP", quality=92, method=6)
print("wrote", webp_path)
