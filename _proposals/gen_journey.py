#!/usr/bin/env python3
"""Generate the dev->prod road at each checkpoint of the journey.
Same layout as overall-flow.svg; stages light green as labs complete."""
import subprocess, os

OUT = os.path.dirname(os.path.abspath(__file__))

# stage geometry: id -> (x, y, w, h, KICKER, line1, line2, line3, accent)
STAGES = {
    "DEVELOP": (90, 285, 172, 150, "DEVELOP", "Agent in sandbox", "queries DHI MCP", "before FROM", "#7da2ff"),
    "BASE":    (292, 285, 172, 150, "BASE", "Hardened image", "DHI · 0 CVEs", "SLSA L3", "#7da2ff"),
    "BUILD":   (494, 285, 172, 150, "BUILD", "Buildx", "SBOM + provenance", "attached at build", "#7da2ff"),
    "SIGN":    (696, 285, 172, 150, "SIGN", "Keyless / Sigstore", "bound to digest", "verifiable", "#7da2ff"),
    "DEPLOY":  (1204, 285, 150, 150, "DEPLOY", "Signed image", "verified · pinned", "by digest", "#6ee7a8"),
    "INVOKE":  (1370, 285, 150, 150, "INVOKE", "Agent / MCP", "client", "signed, read-only", "#6ee7a8"),
}
GATE = (955, 250, 150, 205)

# lab -> stages it completes
LAB_STAGES = {
    1: ["BUILD"],
    2: ["BASE"],
    3: ["SIGN", "GATE", "DEPLOY"],
    4: ["DEVELOP", "INVOKE"],
}

CHECKPOINTS = [
    (0, "Start line — everything still to prove", "0 / 4"),
    (1, "Lab 1 done — you can see what's in it", "1 / 4"),
    (2, "Lab 2 done — hardened base, the CVEs collapse", "2 / 4"),
    (3, "Lab 3 done — signed, gated, promoted to production", "3 / 4"),
    (4, "Lab 4 done — the agent starts right; both ends boxed", "4 / 4"),
]

def done_stages(after_lab):
    d = set()
    for l in range(1, after_lab + 1):
        d.update(LAB_STAGES[l])
    return d

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")

def card(sid, done):
    x, y, w, h, kicker, l1, l2, l3, accent = STAGES[sid]
    is_done = sid in done
    fill = "#0b1533" if is_done else "#20293f"
    stroke = ' stroke="#1a7f37" stroke-width="3"' if is_done else ' stroke="#3a4considerable" '
    stroke = ' stroke="#1a7f37" stroke-width="3"' if is_done else ""
    op = "" if is_done else ' opacity="0.55"'
    kcol = accent if is_done else "#5b6b8c"
    tcol = "#ffffff" if is_done else "#8a97b4"
    scol = "#9aa6c2" if is_done else "#6b789a"
    s = f'<g{op}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}"{stroke}/>'
    s += f'<text x="{x+16}" y="{y+33}" font-size="15" font-weight="800" fill="{kcol}" letter-spacing="1">{esc(kicker)}</text>'
    s += f'<text x="{x+16}" y="{y+63}" font-size="17" font-weight="700" fill="{tcol}">{esc(l1)}</text>'
    s += f'<text x="{x+16}" y="{y+89}" font-size="13.5" fill="{scol}">{esc(l2)}</text>'
    s += f'<text x="{x+16}" y="{y+108}" font-size="13.5" fill="{scol}">{esc(l3)}</text>'
    if is_done:
        cx, cy = x + w - 24, y + 24
        s += f'<circle cx="{cx}" cy="{cy}" r="15" fill="#1a7f37"/>'
        s += f'<path d="M{cx-7},{cy} l5,6 l9,-11" stroke="#ffffff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    s += "</g>"
    return s

def gate(done):
    x, y, w, h = GATE
    is_done = "GATE" in done
    fill = "#fff3e0" if is_done else "#efe4d2"
    op = "" if is_done else ' opacity="0.55"'
    s = f'<g{op}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="#d97706" stroke-width="3"/>'
    s += f'<text x="{x+w/2}" y="{y+42}" text-anchor="middle" font-size="18" font-weight="800" fill="#9a3412">CI GATE</text>'
    s += f'<text x="{x+w/2}" y="{y+72}" text-anchor="middle" font-size="12.5" fill="#9a3412">no critical CVEs</text>'
    s += f'<text x="{x+w/2}" y="{y+93}" text-anchor="middle" font-size="12.5" fill="#9a3412">SBOM present</text>'
    s += f'<text x="{x+w/2}" y="{y+114}" text-anchor="middle" font-size="12.5" fill="#9a3412">provenance verified</text>'
    s += f'<line x1="{x+30}" y1="{y+130}" x2="{x+w-30}" y2="{y+130}" stroke="#e6b98a" stroke-width="1.5"/>'
    s += f'<text x="{x+w/2}" y="{y+156}" text-anchor="middle" font-size="15" font-weight="800" fill="#b91c1c">FAIL CLOSED</text>'
    s += f'<text x="{x+w/2}" y="{y+180}" text-anchor="middle" font-size="11.5" fill="#9a3412">dev → prod boundary</text>'
    if is_done:
        cx, cy = x + w - 22, y + 22
        s += f'<circle cx="{cx}" cy="{cy}" r="14" fill="#1a7f37"/>'
        s += f'<path d="M{cx-6},{cy} l4,5 l8,-10" stroke="#ffffff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    s += "</g>"
    return s

def svg(after_lab, headline, frac):
    done = done_stages(after_lab)
    n = after_lab
    dev_done = {"DEVELOP", "BASE", "BUILD", "SIGN"} <= done
    prod_done = {"DEPLOY", "INVOKE"} <= done
    parts = []
    parts.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" font-family="Helvetica, Arial, sans-serif">')
    parts.append('<rect width="1600" height="900" fill="#E7ECFF"/>')
    # title + dynamic headline
    parts.append('<text x="70" y="76" font-size="42" font-weight="800" fill="#0B1533">The journey: development → production</text>')
    parts.append(f'<text x="70" y="116" font-size="23" font-weight="700" fill="#B91C1C" >{esc(headline)}</text>' if after_lab==0 else f'<text x="70" y="116" font-size="23" font-weight="700" fill="#14532D">{esc(headline)}</text>')
    # DEV zone
    devstroke = "#1a7f37" if dev_done else "#2563eb"
    parts.append(f'<rect x="55" y="150" width="880" height="330" rx="18" fill="#DCE4FF" stroke="{devstroke}" stroke-width="2.5" stroke-dasharray="9 7"/>')
    parts.append('<text x="82" y="188" font-size="24" font-weight="800" fill="#1E3A8A">DEVELOPMENT</text>')
    # sbx bracket around DEVELOP
    sbxstroke = "#1a7f37" if "DEVELOP" in done else "#4f46e5"
    parts.append(f'<rect x="76" y="252" width="200" height="205" rx="12" fill="#EEF3FF" stroke="{sbxstroke}" stroke-width="2" stroke-dasharray="5 5"/>')
    parts.append('<text x="176" y="274" text-anchor="middle" font-size="12.5" font-weight="700" fill="#3730A3">sbx microVM · host read-only</text>')
    for sid in ["DEVELOP", "BASE", "BUILD", "SIGN"]:
        parts.append(card(sid, done))
    parts.append(gate(done))
    # PROD zone
    prodstroke = "#1a7f37"
    parts.append(f'<rect x="1170" y="150" width="380" height="330" rx="18" fill="#E6F4EA" stroke="{prodstroke}" stroke-width="2.5" stroke-dasharray="9 7"{"" if prod_done else " opacity=\"0.8\""}/>')
    parts.append('<text x="1196" y="188" font-size="24" font-weight="800" fill="#14532D">PRODUCTION</text>')
    rtstroke = "#1a7f37"
    parts.append(f'<rect x="1188" y="252" width="344" height="205" rx="12" fill="#F0FAF3" stroke="{rtstroke}" stroke-width="2" stroke-dasharray="5 5"/>')
    parts.append('<text x="1360" y="274" text-anchor="middle" font-size="12" font-weight="700" fill="#14532D">runtime box · read_only · cap_drop ALL · non-root</text>')
    for sid in ["DEPLOY", "INVOKE"]:
        parts.append(card(sid, done))
    # arrows
    parts.append('<g stroke="#64748B" stroke-width="2.5" fill="#64748B">')
    for x0 in [264, 466, 668]:
        parts.append(f'<line x1="{x0}" y1="360" x2="{x0+22}" y2="360"/><polygon points="{x0+22},354 {x0+34},360 {x0+22},366"/>')
    parts.append('<line x1="870" y1="360" x2="951" y2="360"/><polygon points="951,354 963,360 951,366"/>')
    parts.append('</g>')
    gcol = "#1a7f37"
    parts.append(f'<g stroke="{gcol}" stroke-width="3" fill="{gcol}"><line x1="1105" y1="360" x2="1152" y2="360"/><polygon points="1152,353 1166,360 1152,367"/></g>')
    parts.append('<text x="1135" y="345" text-anchor="middle" font-size="12" font-weight="800" fill="#1a7f37">pass</text>')
    # baseline strip (red early, green at finish)
    if after_lab < 4:
        opacity = "1" if after_lab == 0 else "0.4"
        parts.append(f'<g opacity="{opacity}"><rect x="55" y="500" width="1050" height="66" rx="12" fill="#FDECEA" stroke="#F0B4AE" stroke-width="1.5"/>')
        parts.append('<text x="80" y="528" font-size="15" font-weight="800" fill="#B91C1C">UNGOVERNED BASELINE — what the agent shipped on your host</text>')
        parts.append('<text x="80" y="552" font-size="14" fill="#8A1C13">FROM node:20 · 431 pkgs · no SBOM · root · nothing you can prove</text></g>')
    else:
        parts.append('<rect x="55" y="500" width="1050" height="66" rx="12" fill="#E6F4EA" stroke="#1a7f37" stroke-width="1.5"/>')
        parts.append('<text x="80" y="528" font-size="15" font-weight="800" fill="#14532D">PROVABLE END TO END — same source, same agent, first-try green</text>')
        parts.append('<text x="80" y="552" font-size="14" fill="#1a7f37">0C · 0H · 1M · 4L · 78 pkgs · SBOM · signed · non-root</text>')
    # progress bar (4 lab segments)
    parts.append('<text x="1130" y="524" font-size="15" font-weight="800" fill="#0B1533">'+esc(frac)+' stages provable</text>')
    bx, bw, gap = 1130, 96, 12
    for i in range(4):
        seg_done = (i + 1) <= after_lab
        col = "#1a7f37" if seg_done else "#c3cbe4"
        parts.append(f'<rect x="{bx + i*(bw+gap)}" y="540" width="{bw}" height="20" rx="10" fill="{col}"/>')
        parts.append(f'<text x="{bx + i*(bw+gap) + bw/2}" y="592" text-anchor="middle" font-size="13" font-weight="700" fill="{"#14532D" if seg_done else "#8a93b4"}">Lab {i+1}</text>')
    # sandbox both-ends caption
    parts.append('<rect x="55" y="640" width="1495" height="96" rx="16" fill="#0B1533"/>')
    parts.append('<text x="80" y="682" font-size="20" font-weight="800" fill="#FFFFFF">Same discipline at both ends — the agent that BUILDS runs in a box; the service it BECOMES runs in a box.</text>')
    parts.append('<text x="80" y="714" font-size="16" fill="#C7D2FE">sbx microVM at authoring time · read_only + cap_drop ALL at runtime. Least privilege on the left and the right of the road.</text>')
    parts.append('</svg>')
    return "\n".join(parts)

files = []
for after_lab, headline, frac in CHECKPOINTS:
    name = f"journey-{after_lab}"
    with open(f"{OUT}/{name}.svg", "w") as f:
        f.write(svg(after_lab, headline, frac))
    subprocess.run(["rsvg-convert", "-w", "1280", "-h", "720", f"{OUT}/{name}.svg", "-o", f"{OUT}/{name}.png"], check=True)
    files.append(f"{OUT}/{name}.png")
    print("rendered", name)
print("DONE", len(files))
