#!/usr/bin/env python3
"""'A layered approach to AI governance' overview - inserted before the Sandboxing
run (after slide-43 / Part 4 intro). Dark deck palette (#0B1533 bg, #16223F rows,
blue accent), a dashed 'Docker Business + AI Governance Policies' container with six
layers; the DHI foundation row is highlighted. SVG -> png -> webp via rsvg + cwebp."""
import subprocess, os

OUT = os.path.dirname(os.path.abspath(__file__))
BG, SWOOSH, WHITE = "#0B1533", "#111E42", "#FFFFFF"
CAP, DESC = "#AEB9D6", "#A6B6D9"
ROW, ROWBORDER = "#16223F", "#28375E"
HI, HIBORDER, HIDESC = "#1B4BA6", "#5B8DEF", "#D5E1F7"
LABEL, DASH = "#58A6FF", "#3B6FE0"

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# (name, description, highlight)
ROWS = [
    ("Gordon", "In-product governance guidance, inside Docker Desktop", False),
    ("Agentic Compose & Docker Agent", "Declarative multi-agent orchestration - secure golden templates", False),
    ("Docker Model Runner", "Local, air-gapped LLM execution for your workloads", False),
    ("MCP Toolkit & Gateway", "Access only to MCP servers the organization authorizes", False),
    ("Docker Sandboxes", "Isolated, portable runtime - policies travel with the sandbox", False),
    ("Docker Hardened Images (DHI)", "The trusted foundation: scanned, verified, authorized", True),
]

def bg():
    return (f'<rect width="1600" height="900" fill="{BG}"/>'
            f'<path d="M1080,-80 C1280,120 1170,400 1440,500 S1660,780 1600,1000 '
            f'L1760,1000 L1760,-120 Z" fill="{SWOOSH}" opacity="0.55"/>'
            f'<path d="M-120,560 C160,470 300,690 560,600 S900,540 1040,760 '
            f'L1040,1000 L-160,1000 Z" fill="{SWOOSH}" opacity="0.40"/>')

def svg():
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" font-family="Helvetica, Arial, sans-serif">']
    p.append(bg())
    p.append(f'<text x="80" y="96" font-size="48" font-weight="800" fill="{WHITE}">A layered approach to AI governance</text>')
    p.append(f'<text x="80" y="146" font-size="24" fill="{CAP}">Every layer adds an enforceable control and the policies travel with the workload, whether it</text>')
    p.append(f'<text x="80" y="178" font-size="24" fill="{CAP}">runs on a laptop or in the cloud.</text>')
    # container
    cx, cy, cw, ch = 90, 222, 1420, 650
    p.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="16" fill="#0E1A38" '
             f'stroke="{DASH}" stroke-width="2" stroke-dasharray="9 7"/>')
    p.append(f'<text x="132" y="272" font-size="20" font-weight="800" fill="{LABEL}" '
             f'letter-spacing="1.5">DOCKER BUSINESS  +  AI GOVERNANCE POLICIES</text>')
    rx, rw, rh, step, y0 = 132, 1336, 80, 92, 298
    for i, (name, desc, hi) in enumerate(ROWS):
        ry = y0 + i * step
        fill = HI if hi else ROW
        border = HIBORDER if hi else ROWBORDER
        dcol = HIDESC if hi else DESC
        p.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="10" fill="{fill}" '
                 f'stroke="{border}" stroke-width="{2 if hi else 1.5}"/>')
        p.append(f'<text x="{rx+36}" y="{ry+49}" font-size="25" font-weight="800" fill="{WHITE}">{esc(name)}</text>')
        p.append(f'<text x="{rx+520}" y="{ry+49}" font-size="22" fill="{dcol}">{esc(desc)}</text>')
    p.append('</svg>')
    return "\n".join(p)

with open(f"{OUT}/slide-governance.svg", "w") as f:
    f.write(svg())
subprocess.run(["rsvg-convert", "-w", "1600", "-h", "900",
                f"{OUT}/slide-governance.svg", "-o", f"{OUT}/slide-governance.png"], check=True)
subprocess.run(["cwebp", "-q", "92", f"{OUT}/slide-governance.png", "-o", f"{OUT}/slide-governance.webp"],
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("rendered slide-governance")
