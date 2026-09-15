#!/usr/bin/env python3
"""'Docker Hardened Images' feature slide - inserted after slide-32 (the DHI
scout-compare numbers). Light layout: DHI logo + three feature bullets + the
catalog URL on the left, a Docker Hub hardened-images catalog panel mock on the
right. SVG -> png -> webp via rsvg + cwebp."""
import subprocess, os

OUT = os.path.dirname(os.path.abspath(__file__))
BLUE = "#1D63ED"
INK = "#17191E"
GRAY = "#5B6B84"
PURPLE = "#7C5CFC"
CARDBORDER = "#E4E8EF"
ICONBG = "#1B2530"
LABELP = "#8250DF"
PANEL = "#FFFFFF"
SHADOW = "#C9D2E0"

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def whale(ox, oy):
    """Simplified Docker container-stack + whale glyph, ~150px wide."""
    p = []
    u, g = 22, 4
    # container stack: bottom row 4, middle row 2, top 1
    def box(cx, cy):
        p.append(f'<rect x="{cx}" y="{cy}" width="{u}" height="{u}" rx="3" fill="{BLUE}"/>')
    bx, by = ox + 26, oy + 30
    for i in range(4):
        box(bx + i * (u + g), by)                    # bottom row
    for i in range(2):
        box(bx + (i + 1) * (u + g), by - (u + g))    # middle row
    box(bx + 1 * (u + g), by - 2 * (u + g))          # top box
    # whale body
    p.append(f'<rect x="{ox+8}" y="{by+u+6}" width="{u*4+g*3+40}" height="26" rx="13" fill="{BLUE}"/>')
    # tail
    p.append(f'<path d="M{ox+8},{by+u+8} q-16,-4 -22,-18 q14,2 22,12 Z" fill="{BLUE}"/>')
    # spout
    p.append(f'<circle cx="{ox+22}" cy="{by+u+19}" r="4" fill="#FFFFFF"/>')
    return "".join(p)

def icon_shield_plus(cx, cy):
    return (f'<path d="M{cx},{cy-30} l26,10 v20 c0,20 -12,30 -26,38 c-14,-8 -26,-18 -26,-38 v-20 Z" '
            f'fill="none" stroke="{PURPLE}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M{cx},{cy-6} v22 M{cx-11},{cy+5} h22" stroke="{PURPLE}" stroke-width="4" stroke-linecap="round"/>')

def icon_box_check(cx, cy):
    return (f'<path d="M{cx},{cy-30} l26,15 v30 l-26,15 l-26,-15 v-30 Z" fill="none" '
            f'stroke="{PURPLE}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M{cx-26},{cy-15} l26,15 l26,-15 M{cx},{cy} v30" stroke="{PURPLE}" '
            f'stroke-width="3" fill="none" opacity="0.55"/>'
            f'<path d="M{cx-11},{cy+4} l7,8 l14,-16" stroke="{PURPLE}" stroke-width="4" '
            f'fill="none" stroke-linecap="round" stroke-linejoin="round"/>')

def icon_shield_check(cx, cy):
    return (f'<path d="M{cx},{cy-30} l26,10 v20 c0,20 -12,30 -26,38 c-14,-8 -26,-18 -26,-38 v-20 Z" '
            f'fill="none" stroke="{PURPLE}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M{cx-13},{cy+4} l9,10 l17,-20" stroke="{PURPLE}" stroke-width="4" '
            f'fill="none" stroke-linecap="round" stroke-linejoin="round"/>')

# right-panel catalog cards: (name, sub, desc1, desc2)
CARDS = [
    ("arangodb", "arangodb", "Multi-model NoSQL database optimized for", "flexibility and performance."),
    ("redis", "redis", "In-memory key-value store ideal for caching and", "real-time data."),
    ("tomcat", "apache", "Java servlet container for running web", "applications."),
    ("grafana", "grafana", "Analytics dashboard platform for visualizing", "time-series data."),
    ("golang", "go", "Lightweight compiler and toolchain for", "building Go applications."),
    ("node.js", "node.js", "JavaScript runtime built on Chrome's V8", "engine for scalable apps."),
    ("azul", "azul", "", ""),
    ("maven", "maven", "", ""),
    ("kubectl", "kubernetes", "", ""),
]

def card(x, y, w, h, name, sub, d1, d2):
    p = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#FFFFFF" '
         f'stroke="{CARDBORDER}" stroke-width="1.5"/>']
    p.append(f'<text x="{x+16}" y="{y+22}" font-size="9.5" font-weight="700" '
             f'fill="{LABELP}" letter-spacing="0.8">HARDENED IMAGE</text>')
    p.append(f'<rect x="{x+16}" y="{y+34}" width="34" height="34" rx="7" fill="{ICONBG}"/>')
    p.append(f'<text x="{x+33}" y="{y+57}" font-size="16" font-weight="800" fill="#FFFFFF" '
             f'text-anchor="middle">{esc(name[0].upper())}</text>')
    p.append(f'<text x="{x+58}" y="{y+50}" font-size="15" font-weight="800" fill="{INK}">{esc(name)}</text>')
    p.append(f'<text x="{x+58}" y="{y+66}" font-size="11" fill="{BLUE}">{esc(sub)}</text>')
    if d1:
        p.append(f'<text x="{x+16}" y="{y+96}" font-size="10.5" fill="{GRAY}">{esc(d1)}</text>')
    if d2:
        p.append(f'<text x="{x+16}" y="{y+112}" font-size="10.5" fill="{GRAY}">{esc(d2)}</text>')
    rows = [("OS", "Alpine, Debian"), ("Architecture", "amd64, arm64"), ("Compliance", "FIPS")]
    ry = y + 140
    for lbl, val in rows:
        p.append(f'<text x="{x+16}" y="{ry}" font-size="10.5" fill="{GRAY}">{lbl}</text>')
        p.append(f'<text x="{x+w-16}" y="{ry}" font-size="10.5" font-weight="600" fill="{INK}" '
                 f'text-anchor="end">{val}</text>')
        ry += 22
    return "".join(p)

def svg():
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" '
         'font-family="Helvetica, Arial, sans-serif">']
    p.append('<rect width="1600" height="900" fill="#FFFFFF"/>')

    # ---- left column ----
    p.append(whale(70, 150))
    p.append(f'<text x="230" y="222" font-size="46" font-weight="800" fill="{INK}">docker</text>')
    p.append(f'<text x="230" y="272" font-size="46" font-weight="800" fill="{BLUE}">hardened images</text>')

    bullets = [
        (icon_shield_plus, "Ultra-Minimal Footprint with", "Near-Zero CVEs"),
        (icon_box_check, "7-Day Remediation for Critical &", "High CVEs, SLA-Guaranteed"),
        (icon_shield_check, "Built in provenance, SLSA", "compliance, SBOMs"),
    ]
    ys = [400, 560, 720]
    for (icon, l1, l2), y in zip(bullets, ys):
        p.append(icon(110, y))
        p.append(f'<text x="185" y="{y-6}" font-size="33" font-weight="700" fill="{INK}">{esc(l1)}</text>')
        p.append(f'<text x="185" y="{y+34}" font-size="33" font-weight="700" fill="{INK}">{esc(l2)}</text>')

    url = "https://hub.docker.com/hardened-images/catalog"
    p.append(f'<text x="70" y="852" font-size="27" fill="{BLUE}" '
             f'text-decoration="underline">{esc(url)}</text>')

    # ---- right panel: Docker Hub catalog ----
    px, py, pw, ph = 838, 66, 712, 800
    p.append(f'<rect x="{px+6}" y="{py+8}" width="{pw}" height="{ph}" rx="16" fill="{SHADOW}" opacity="0.5"/>')
    p.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="16" fill="{PANEL}" '
             f'stroke="{CARDBORDER}" stroke-width="1.5"/>')
    # blue header
    p.append(f'<path d="M{px},{py+16} a16,16 0 0 1 16,-16 h{pw-32} a16,16 0 0 1 16,16 v48 h{-pw} Z" fill="{BLUE}"/>')
    p.append(f'<text x="{px+30}" y="{py+42}" font-size="19" font-weight="800" fill="#FFFFFF">docker hub</text>')
    p.append(f'<rect x="{px+pw-230}" y="{py+16}" width="210" height="30" rx="15" fill="#FFFFFF" opacity="0.22"/>')
    p.append(f'<text x="{px+pw-195}" y="{py+36}" font-size="13" fill="#EAF0FF">Search</text>')

    inx = px + 28
    inw = pw - 56
    p.append(f'<text x="{inx}" y="{py+112}" font-size="25" font-weight="800" fill="{INK}">Docker hardened images</text>')
    p.append(f'<text x="{inx}" y="{py+140}" font-size="13" fill="{GRAY}">'
             f'Enterprise-ready, secure container images with built-in compliance and minimal vulnerabilities.</text>')
    # search box
    sby = py + 158
    p.append(f'<rect x="{inx}" y="{sby}" width="{inw-150}" height="42" rx="8" fill="#FFFFFF" '
             f'stroke="{CARDBORDER}" stroke-width="1.5"/>')
    p.append(f'<circle cx="{inx+22}" cy="{sby+21}" r="7" fill="none" stroke="{GRAY}" stroke-width="2"/>')
    p.append(f'<text x="{inx+42}" y="{sby+27}" font-size="14" fill="{GRAY}">Search</text>')
    p.append(f'<rect x="{inx+inw-138}" y="{sby}" width="138" height="42" rx="8" fill="#FFFFFF" '
             f'stroke="{CARDBORDER}" stroke-width="1.5"/>')
    p.append(f'<text x="{inx+inw-69}" y="{sby+27}" font-size="13" fill="{GRAY}" text-anchor="middle">Filter by...</text>')

    # cards grid, 3 columns
    gx0 = inx
    gap = 16
    cw = (inw - 2 * gap) / 3
    ch = 224
    gy0 = py + 224
    ystep = ch + 18
    # clip so the bottom row is cut off inside the panel like the screenshot
    p.append(f'<clipPath id="pnl"><rect x="{px}" y="{py+72}" width="{pw}" height="{ph-72}" rx="16"/></clipPath>')
    p.append(f'<g clip-path="url(#pnl)">')
    for i, (name, sub, d1, d2) in enumerate(CARDS):
        r, c = divmod(i, 3)
        cx = gx0 + c * (cw + gap)
        cy = gy0 + r * ystep
        p.append(card(cx, cy, cw, ch, name, sub, d1, d2))
    p.append('</g>')

    p.append('</svg>')
    return "\n".join(p)

with open(f"{OUT}/slide-hardened-images.svg", "w") as f:
    f.write(svg())
subprocess.run(["rsvg-convert", "-w", "1600", "-h", "900",
                f"{OUT}/slide-hardened-images.svg", "-o", f"{OUT}/slide-hardened-images.png"], check=True)
subprocess.run(["cwebp", "-q", "92", f"{OUT}/slide-hardened-images.png", "-o", f"{OUT}/slide-hardened-images.webp"],
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("rendered slide-hardened-images")
