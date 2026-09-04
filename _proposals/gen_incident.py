#!/usr/bin/env python3
"""'What could go wrong' cold-open, adapted from the DevOps Show "02:47 AM" slide.
The deck is a pure image-per-slide viewer (no reveal fragments), so the animation
is a SEQUENCE OF BUILD FRAMES: the story grows one row at a time, newest row
spotlighted, ending on "who approved that build?". The presenter arrows through
slide-incident-1..5 then slide-incident (full) - it reads as the story unfolding.
slide-incident.webp (full) is also reused later as the callback recap."""
import subprocess, os

OUT = os.path.dirname(os.path.abspath(__file__))

# (label, value, mono, danger)
ROWS = [
    ("Author", "svc-build-agent", True, False),
    ("Change", "Bumped a base image, regenerated the Dockerfile", False, False),
    ("Reviewer", "Approved by CI - all checks green", False, False),
    ("Deployed", "Production, 03:12 AM", False, False),
    ("Reviewed by a human", "No", False, True),
]

TX, TY, TW, RH, LW = 70, 178, 1460, 84, 320

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")

def row_svg(i, state):
    label, value, mono, danger = ROWS[i]
    rtop = TY + i * RH
    out = []
    if state == "spot":
        acc = "#E5484D" if danger else "#2563EB"
        accbg = "#FDECEE" if danger else "#EAF1FE"
        out.append(f'<rect x="{TX}" y="{rtop}" width="{TW}" height="{RH}" fill="{accbg}"/>')
        out.append(f'<rect x="{TX}" y="{rtop}" width="6" height="{RH}" fill="{acc}"/>')
        lcol = acc
    else:
        out.append(f'<rect x="{TX}" y="{rtop}" width="{LW}" height="{RH}" fill="#F3F5FA"/>')
        lcol = "#0B1533"
    if i > 0:
        out.append(f'<line x1="{TX}" y1="{rtop}" x2="{TX+TW}" y2="{rtop}" stroke="#E2E8F8" stroke-width="1.5"/>')
    by = rtop + RH / 2 + 7
    out.append(f'<text x="{TX+28}" y="{by}" font-size="20" font-weight="700" fill="{lcol}">{esc(label)}</text>')
    vfont = ' font-family="Courier New, monospace"' if mono else ''
    vcol = "#E5484D" if danger else "#334155"
    vweight = ' font-weight="800"' if danger else ''
    out.append(f'<text x="{TX+LW+28}" y="{by}" font-size="20"{vfont}{vweight} fill="{vcol}">{esc(value)}</text>')
    return "".join(out)

def render(k, question, spotlight_last):
    """k rows shown (0..k). newest spotlighted if spotlight_last. question at bottom."""
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" font-family="Helvetica, Arial, sans-serif">']
    p.append('<rect width="1600" height="900" fill="#FFFFFF"/>')
    p.append('<text x="70" y="96" font-size="44" font-weight="800" fill="#0B1533">02:47 AM. A commit lands.</text>')
    h = RH * k
    p.append(f'<rect x="{TX}" y="{TY}" width="{TW}" height="{h}" rx="14" fill="#FFFFFF"/>')
    for i in range(k):
        state = "spot" if (spotlight_last and i == k - 1) else "normal"
        p.append(row_svg(i, state))
    p.append(f'<rect x="{TX}" y="{TY}" width="{TW}" height="{h}" rx="14" fill="none" stroke="#E2E8F8" stroke-width="1.5"/>')
    p.append(f'<line x1="{TX+LW}" y1="{TY}" x2="{TX+LW}" y2="{TY+h}" stroke="#E2E8F8" stroke-width="1.5"/>')
    if question:
        p.append('<text x="1530" y="770" text-anchor="end" font-size="46" font-weight="800" fill="#2563EB">Who approved that build?</text>')
    p.append('</svg>')
    return "\n".join(p)

# build frames 1..5 (growing, newest spotlighted, no question yet)
FRAMES = [(f"slide-incident-{k}", render(k, False, True)) for k in range(1, 6)]
# final / callback recap: all rows calm + the question
FRAMES.append(("slide-incident", render(5, True, False)))

for name, doc in FRAMES:
    with open(f"{OUT}/{name}.svg", "w") as f:
        f.write(doc)
    subprocess.run(["rsvg-convert", "-w", "1600", "-h", "900",
                    f"{OUT}/{name}.svg", "-o", f"{OUT}/{name}.png"], check=True)
    subprocess.run(["cwebp", "-q", "90", f"{OUT}/{name}.png", "-o", f"{OUT}/{name}.webp"],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("rendered", name)
print("DONE", len(FRAMES), "frames")
