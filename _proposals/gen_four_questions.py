#!/usr/bin/env python3
"""Bridge slide between the agentic workflow (slide-07) and the journey road.
Adapts the DevOps Show "four questions" framework into the workshop deck style:
Evidence / Baseline / Gate / Boundary - the four layers the road then draws.
Same palette + fonts as gen_journey.py so it sits native next to slide-07/journey-0."""
import subprocess, os

OUT = os.path.dirname(os.path.abspath(__file__))

# id -> (num, KICKER, q_line1, q_line2, foot1, foot2)
CARDS = [
    ("1", "EVIDENCE", "What is in this, and", "where did it come from?",
     "SBOM · VEX · SLSA", "provenance"),
    ("2", "BASELINE", "Did it start from", "something trustworthy?",
     "Docker Hardened", "Images"),
    ("3", "GATE", "Is it allowed", "to pass?",
     "Build policies · signing", "· admission"),
    ("4", "BOUNDARY", "What could it reach", "while it worked?",
     "Sandbox runtime · network,", "filesystem, credentials"),
]

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")

def card(i, c):
    num, kicker, q1, q2, f1, f2 = c
    x = 70 + i * 372          # 344 wide + 28 gap
    y, w, h = 210, 344, 470
    s = f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#F7F9FF" stroke="#E2E8F8" stroke-width="1.5"/>'
    s += f'<text x="{x+26}" y="{y+66}" font-size="52" font-weight="800" fill="#C7D0EA">{num}</text>'
    s += f'<text x="{x+26}" y="{y+110}" font-size="15" font-weight="800" fill="#2563EB" letter-spacing="1">{esc(kicker)}</text>'
    s += f'<text x="{x+26}" y="{y+150}" font-size="21" font-weight="700" fill="#0B1533">{esc(q1)}</text>'
    s += f'<text x="{x+26}" y="{y+178}" font-size="21" font-weight="700" fill="#0B1533">{esc(q2)}</text>'
    s += f'<text x="{x+26}" y="{y+h-42}" font-size="13.5" fill="#5B6B8C">{esc(f1)}</text>'
    s += f'<text x="{x+26}" y="{y+h-22}" font-size="13.5" fill="#5B6B8C">{esc(f2)}</text>'
    s += "</g>"
    return s

def svg():
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" font-family="Helvetica, Arial, sans-serif">']
    p.append('<rect width="1600" height="900" fill="#FFFFFF"/>')
    p.append('<text x="70" y="92" font-size="42" font-weight="800" fill="#0B1533">Every agent-driven change answers four questions</text>')
    p.append('<text x="70" y="134" font-size="22" fill="#64748B">Four layers that make agent-driven change governable - before we walk the road.</text>')
    for i, c in enumerate(CARDS):
        p.append(card(i, c))
    # bottom takeaway, two-tone
    p.append('<text x="70" y="748" font-size="22" font-weight="800" fill="#0B1533">Evidence and baseline make governance possible. '
             '<tspan fill="#2563EB">Gate and boundary make it real.</tspan></text>')
    p.append('</svg>')
    return "\n".join(p)

with open(f"{OUT}/four-questions.svg", "w") as f:
    f.write(svg())
subprocess.run(["rsvg-convert", "-w", "1600", "-h", "900",
                f"{OUT}/four-questions.svg", "-o", f"{OUT}/four-questions.png"], check=True)
subprocess.run(["cwebp", "-q", "90", f"{OUT}/four-questions.png",
                "-o", f"{OUT}/slide-framework.webp"], check=True)
print("rendered slide-framework.webp")
