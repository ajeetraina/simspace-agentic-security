#!/usr/bin/env python3
"""'What could go wrong' hook slide, adapted from the DevOps Show "02:47 AM" slide
into the workshop deck style. A commit lands in prod, authored by an agent, with no
human review - setting up "who approved that build?" before the concrete example."""
import subprocess, os

OUT = os.path.dirname(os.path.abspath(__file__))

# (label, value, mono, red)
ROWS = [
    ("Author", "svc-build-agent", True, False),
    ("Change", "Bumped a base image, regenerated the Dockerfile", False, False),
    ("Reviewer", "Approved by CI - all checks green", False, False),
    ("Deployed", "Production, 03:12 AM", False, False),
    ("Reviewed by a human", "No", False, True),
]

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")

def svg():
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" font-family="Helvetica, Arial, sans-serif">']
    p.append('<rect width="1600" height="900" fill="#FFFFFF"/>')
    p.append('<text x="70" y="96" font-size="44" font-weight="800" fill="#0B1533">02:47 AM. A commit lands.</text>')
    tx, ty, tw, rh = 70, 178, 1460, 84
    lw = 320  # label column width
    n = len(ROWS)
    # white table background
    p.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{rh*n}" rx="14" fill="#FFFFFF"/>')
    for i, (label, value, mono, red) in enumerate(ROWS):
        rtop = ty + i * rh
        # shaded label cell
        p.append(f'<rect x="{tx}" y="{rtop}" width="{lw}" height="{rh}" fill="#F3F5FA"/>')
        if i > 0:
            p.append(f'<line x1="{tx}" y1="{rtop}" x2="{tx+tw}" y2="{rtop}" stroke="#E2E8F8" stroke-width="1.5"/>')
        by = rtop + rh / 2 + 7
        p.append(f'<text x="{tx+28}" y="{by}" font-size="20" font-weight="700" fill="#0B1533">{esc(label)}</text>')
        vfont = ' font-family="Courier New, monospace"' if mono else ''
        vcol = "#E5484D" if red else "#334155"
        vweight = ' font-weight="800"' if red else ''
        p.append(f'<text x="{tx+lw+28}" y="{by}" font-size="20"{vfont}{vweight} fill="{vcol}">{esc(value)}</text>')
    # table border on top for crisp rounded edge
    p.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{rh*n}" rx="14" fill="none" stroke="#E2E8F8" stroke-width="1.5"/>')
    p.append(f'<line x1="{tx+lw}" y1="{ty}" x2="{tx+lw}" y2="{ty+rh*n}" stroke="#E2E8F8" stroke-width="1.5"/>')
    # payoff question, bottom-right
    p.append('<text x="1530" y="770" text-anchor="end" font-size="46" font-weight="800" fill="#2563EB">Who approved that build?</text>')
    p.append('</svg>')
    return "\n".join(p)

with open(f"{OUT}/incident.svg", "w") as f:
    f.write(svg())
subprocess.run(["rsvg-convert", "-w", "1600", "-h", "900",
                f"{OUT}/incident.svg", "-o", f"{OUT}/incident.png"], check=True)
subprocess.run(["cwebp", "-q", "90", f"{OUT}/incident.png",
                "-o", f"{OUT}/slide-incident.webp"], check=True)
print("rendered slide-incident.webp")
