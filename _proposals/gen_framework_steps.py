#!/usr/bin/env python3
"""Rebuild "Your security framework - try these steps" natively so each row's
description (SBOM + VEX, SLSA provenance, ...) sits in an aligned right-hand
column instead of crowding the bold label. Overwrites assets/slide-54.webp."""
import subprocess, os

OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(OUT)

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")

ROWS = [
    ("1", "Know what is in your images", "SBOM + VEX"),
    ("2", "Verify where they came from", "SLSA provenance + image signing"),
    ("3", "Start from a trusted base", "Docker Hardened Images"),
    ("4", "Enforce at the pipeline", "Docker Scout build policies"),
    ("5", "Isolate your agents", "MCP servers in hardened containers"),
]

def svg():
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" font-family="Helvetica, Arial, sans-serif">']
    p.append('<rect width="1600" height="900" fill="#0B1533"/>')
    p.append('<text x="95" y="128" font-size="46" font-weight="800" fill="#FFFFFF">Your security framework - try these steps</text>')
    x0, w = 95, 1410
    desc_x = 780           # aligned description column
    y = 214
    h, gap = 92, 18
    for num, label, desc in ROWS:
        cy = y + h / 2 + 8
        p.append(f'<rect x="{x0}" y="{y}" width="{w}" height="{h}" rx="12" fill="#17213E"/>')
        p.append(f'<rect x="{x0}" y="{y}" width="6" height="{h}" rx="3" fill="#4F7CFF"/>')
        p.append(f'<text x="{x0+45}" y="{cy}" font-size="30" font-weight="800" fill="#4F7CFF">{num}</text>')
        p.append(f'<text x="{x0+110}" y="{cy}" font-size="23" font-weight="700" fill="#FFFFFF">{esc(label)}</text>')
        p.append(f'<text x="{desc_x}" y="{cy}" font-size="21" fill="#A6B6D9">{esc(desc)}</text>')
        y += h + gap
    p.append('</svg>')
    return "\n".join(p)

with open(f"{OUT}/framework-steps.svg", "w") as f:
    f.write(svg())
subprocess.run(["rsvg-convert", "-w", "1600", "-h", "900", f"{OUT}/framework-steps.svg", "-o", f"{OUT}/framework-steps.png"], check=True)
subprocess.run(["cwebp", "-q", "90", f"{OUT}/framework-steps.png", "-o", f"{OUT}/slide-54.webp"], check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["cp", f"{OUT}/slide-54.webp", f"{ROOT}/lab/securing-the-agentic-stack-slides/assets/slide-54.webp"], check=True)
print("rebuilt slide-54.webp")
