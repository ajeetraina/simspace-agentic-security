#!/usr/bin/env python3
"""Replace the 5-node inline progress spine in lab sections 02-07 with a slim
road-checkpoint spine (DEV zone / GATE / PROD zone), states: done / current / todo.
Kept in sync with the deck journey slides."""
import re, os

LAB = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "lab", "securing-the-agentic-stack")

DEV_PILLS = [("DEVELOP", 8), ("BASE", 134), ("BUILD", 260), ("SIGN", 386)]
PROD_PILLS = [("DEPLOY", 628), ("INVOKE", 766)]
PW, PH, PY = 118, 44, 40
PPW = 126  # prod pill width

def pill(label, x, w, done, current, show_here=False):
    if done:
        fill, tcol, stroke = "#0b1533", "#ffffff", ' stroke="#1a7f37" stroke-width="2.5"'
    elif current:
        fill, tcol, stroke = "#0b1533", "#ffffff", ' stroke="#2563eb" stroke-width="3"'
    else:
        fill, tcol, stroke = "#e2e7f5", "#7a86a8", ""
    s = f'<rect x="{x}" y="{PY}" width="{w}" height="{PH}" rx="9" fill="{fill}"{stroke}/>'
    s += f'<text x="{x+w/2}" y="{PY+27}" text-anchor="middle" font-size="13" font-weight="700" fill="{tcol}">{label}</text>'
    if done:
        cx, cy = x + w - 13, PY + 12
        s += f'<circle cx="{cx}" cy="{cy}" r="9" fill="#1a7f37"/>'
        s += f'<path d="M{cx-4},{cy} l3,3.5 l5.5,-6.5" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    if current and show_here:
        s += f'<text x="{x+w/2}" y="{PY-6}" text-anchor="middle" font-size="10" font-weight="800" fill="#2563eb">▶ you are here</text>'
    return s

def gate(done, current, show_here=False):
    x, w = 536, 70
    if done:
        fill, stroke = "#fff3e0", ' stroke="#1a7f37" stroke-width="2.5"'
    elif current:
        fill, stroke = "#fff3e0", ' stroke="#2563eb" stroke-width="3"'
    else:
        fill, stroke = "#efe4d2", ' stroke="#d9a066" stroke-width="1.5"'
    tcol = "#9a3412" if (done or current) else "#b79878"
    s = f'<rect x="{x}" y="32" width="{w}" height="60" rx="10" fill="{fill}"{stroke}/>'
    s += f'<text x="{x+w/2}" y="58" text-anchor="middle" font-size="12" font-weight="800" fill="{tcol}">GATE</text>'
    s += f'<text x="{x+w/2}" y="76" text-anchor="middle" font-size="8.5" fill="{tcol}">fail closed</text>'
    if done:
        cx, cy = x + w - 12, 44
        s += f'<circle cx="{cx}" cy="{cy}" r="9" fill="#1a7f37"/>'
        s += f'<path d="M{cx-4},{cy} l3,3.5 l5.5,-6.5" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    if current and show_here:
        s += f'<text x="{x+w/2}" y="26" text-anchor="middle" font-size="10" font-weight="800" fill="#2563eb">▶ here</text>'
    return s

def spine(done, current, baseline=False):
    aria = ("Progress spine: the development-to-production road. Stages "
            "DEVELOP, BASE, BUILD, SIGN sit in the development zone (an sbx sandbox); "
            "a CI GATE is the boundary; DEPLOY and INVOKE sit in the production zone "
            "(a read-only runtime box). Done stages are checked green, the current stage is marked.")
    p = [f'<svg viewBox="0 0 900 104" width="100%" role="img" aria-label="{aria}">']
    p.append('<g font-family="ui-sans-serif, system-ui, sans-serif">')
    # zones
    p.append('<rect x="2" y="14" width="516" height="82" rx="10" fill="#dce4ff" stroke="#2563eb" stroke-width="1.3" stroke-dasharray="6 4"/>')
    p.append('<text x="10" y="28" font-size="10.5" font-weight="800" fill="#1e3a8a">DEVELOPMENT</text>')
    p.append('<text x="120" y="28" font-size="9" fill="#3730a3">sbx microVM · host read-only</text>')
    p.append('<rect x="618" y="14" width="280" height="82" rx="10" fill="#e6f4ea" stroke="#1a7f37" stroke-width="1.3" stroke-dasharray="6 4"/>')
    p.append('<text x="626" y="28" font-size="10.5" font-weight="800" fill="#14532d">PRODUCTION</text>')
    p.append('<text x="720" y="28" font-size="9" fill="#14532d">read_only · cap_drop ALL</text>')
    # only the leftmost current stage gets the "you are here" marker
    order = ["DEVELOP", "BASE", "BUILD", "SIGN", "GATE", "DEPLOY", "INVOKE"]
    here = next((s for s in order if s in current), None)
    # dev pills
    for label, x in DEV_PILLS:
        p.append(pill(label, x, PW, label in done, label in current, show_here=(label == here)))
    p.append(gate("GATE" in done, "GATE" in current, show_here=(here == "GATE")))
    for label, x in PROD_PILLS:
        p.append(pill(label, x, PPW, label in done, label in current, show_here=(label == here)))
    # connector arrows
    p.append('<g stroke="#9aa6c2" stroke-width="1.6" fill="#9aa6c2">')
    for x0 in [126, 252, 378]:
        p.append(f'<line x1="{x0}" y1="62" x2="{x0+8}" y2="62"/><polygon points="{x0+8},59 {x0+13},62 {x0+8},65"/>')
    p.append('<line x1="504" y1="62" x2="536" y2="62"/><polygon points="536,59 541,62 536,65"/>')
    p.append('<line x1="606" y1="62" x2="628" y2="62"/><polygon points="628,59 633,62 628,65"/>')
    p.append('</g>')
    # baseline tag on the start-line spine
    if baseline:
        p.append('<text x="10" y="90" font-size="9" font-weight="700" fill="#b91c1c">baseline: node:20 · 431 pkgs · no SBOM · root — nothing to prove</text>')
    p.append('</g></svg>')
    return "\n".join(p)

ALL = {"DEVELOP", "BASE", "BUILD", "SIGN", "GATE", "DEPLOY", "INVOKE"}
STATES = {
    "02-agent-builds-it.md":  (set(), set(), True),
    "03-sbom-vex-slsa.md":    (set(), {"BUILD"}, False),
    "04-dhi-migration.md":    ({"BUILD"}, {"BASE"}, False),
    "05-ci-policy.md":        ({"BUILD", "BASE"}, {"SIGN", "GATE", "DEPLOY"}, False),
    "06-agent-sandbox.md":    ({"BUILD", "BASE", "SIGN", "GATE", "DEPLOY"}, {"DEVELOP", "INVOKE"}, False),
    "07-conclusion.md":       (ALL, set(), False),
}

pat = re.compile(r'<svg viewBox="0 0 900 (?:52|104)".*?</svg>', re.S)
for fname, (done, current, baseline) in STATES.items():
    path = os.path.join(LAB, fname)
    text = open(path).read()
    new = spine(done, current, baseline)
    out, n = pat.subn(new, text, count=1)
    assert n == 1, f"{fname}: expected 1 spine, found {n}"
    open(path, "w").write(out)
    print(f"replaced spine in {fname}  done={sorted(done)} current={sorted(current)}")
print("DONE")
