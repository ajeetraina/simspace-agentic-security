#!/usr/bin/env python3
"""Redesigned '02:47 AM' cold-open, dark terminal style (replaces the light
growing-table slide-incident-1..5 + recap). Two beats:
  slide-incident-commit  - a commit landed, author is an agent, 812 lines changed
  slide-incident-review  - who reviewed it? CI said yes; the reviewers array is empty
Palette matches the deck's dark slides (gen_framework_steps): #0B1533 bg, #17213E
cards, #4F7CFF accent. Rendered SVG -> png -> webp via rsvg-convert + cwebp."""
import subprocess, os

OUT = os.path.dirname(os.path.abspath(__file__))

BG      = "#0B1533"
SWOOSH  = "#111E42"
CARD    = "#0E1A3A"   # terminal body
BAR     = "#1A2547"   # terminal title bar
BORDER  = "#243157"
MUTE    = "#8698BE"   # prompt / dim output
TXT     = "#C7D2E8"   # default mono text
DIM     = "#9AAAC9"   # git metadata lines
WHITE   = "#FFFFFF"
ORANGE  = "#E0A15C"   # command keywords (git / pr)
BLUE    = "#6EA8FE"   # numbers
PURPLE  = "#B98BE0"   # flags
GREEN   = "#57C08A"   # strings / check / +++
PINK    = "#E5548A"   # svc-build-agent
CAP     = "#AEB9D6"   # caption base

CARDX, CARDW = 64, 1472
MONO = "Menlo, 'DejaVu Sans Mono', 'Courier New', monospace"

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def bg():
    return (f'<rect width="1600" height="900" fill="{BG}"/>'
            # soft whale-swoosh watermarks
            f'<path d="M1080,-80 C1280,120 1170,400 1440,500 S1660,780 1600,1000 '
            f'L1760,1000 L1760,-120 Z" fill="{SWOOSH}" opacity="0.55"/>'
            f'<path d="M-120,560 C160,470 300,690 560,600 S900,540 1040,760 '
            f'L1040,1000 L-160,1000 Z" fill="{SWOOSH}" opacity="0.40"/>')

def titlebar(y):
    """terminal title bar: 'bash' label + copy glyph, top corners rounded."""
    h = 44
    s  = f'<rect x="{CARDX}" y="{y}" width="{CARDW}" height="{h}" rx="12" fill="{BAR}"/>'
    s += f'<rect x="{CARDX}" y="{y+h-14}" width="{CARDW}" height="14" fill="{BAR}"/>'  # square bottom
    # small prompt glyph
    s += f'<rect x="{CARDX+22}" y="{y+15}" width="15" height="13" rx="2.5" fill="none" stroke="{MUTE}" stroke-width="1.6"/>'
    s += f'<path d="M{CARDX+25} {y+19} l3 2.5 -3 2.5" fill="none" stroke="{MUTE}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
    s += f'<text x="{CARDX+48}" y="{y+29}" font-family="{MONO}" font-size="17" font-weight="700" fill="{MUTE}">bash</text>'
    # copy icon (two offset rounded rects), top-right
    cx = CARDX + CARDW - 42
    s += f'<rect x="{cx+6}" y="{y+13}" width="15" height="17" rx="3" fill="none" stroke="{MUTE}" stroke-width="1.6"/>'
    s += f'<rect x="{cx}" y="{y+18}" width="15" height="17" rx="3" fill="{BAR}" stroke="{MUTE}" stroke-width="1.6"/>'
    return s

def card_frame(y, h):
    return (f'<rect x="{CARDX}" y="{y}" width="{CARDW}" height="{h}" rx="12" fill="{CARD}" '
            f'stroke="{BORDER}" stroke-width="1.5"/>')

def line(x, y, parts, size=22):
    """parts: list of (text, color, weight700?). monospace, so cols align by spaces."""
    spans = []
    first = True
    for text, col, *rest in parts:
        bold = rest[0] if rest else False
        w = ' font-weight="700"' if bold else ''
        pos = f' x="{x}"' if first else ''
        spans.append(f'<tspan{pos} fill="{col}"{w}>{esc(text)}</tspan>')
        first = False
    return f'<text y="{y}" font-family="{MONO}" font-size="{size}" xml:space="preserve">{"".join(spans)}</text>'

# ---------------------------------------------------------------- slide 1
def slide_commit():
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" font-family="Helvetica, Arial, sans-serif">']
    p.append(bg())
    p.append(f'<text x="64" y="118" font-size="86" font-weight="800" fill="{WHITE}">02:47 AM</text>')
    p.append(f'<text x="66" y="198" font-size="46" font-weight="800" fill="{WHITE}">A commit landed.</text>')
    ty = 236
    p.append(titlebar(ty))
    bodytop, h = ty + 44, 300
    p.append(card_frame(bodytop, h))
    tx = CARDX + 34
    ly = bodytop + 40
    step = 27
    rows = [
        [("$ ", MUTE), ("git", ORANGE), (" log ", TXT), ("-1", ORANGE), (" --stat", TXT)],
        [("commit a9d0e42 ", DIM), ("(HEAD -> main, origin/main)", DIM)],
        [("Author: ", DIM), ("svc-build-agent", TXT), (" <ci@dockerlabs.xyz>", DIM)],
        [("Date:   Tue 02:47:11", DIM)],
        [(" ", DIM)],
        [("    chore: bump base image, regenerate Dockerfile", TXT)],
        [(" ", DIM)],
        [(" Dockerfile        | ", TXT), (" 34", BLUE), (" +++++++", GREEN), ("------", MUTE)],
        [(" package-lock.json | ", TXT), ("812", BLUE), (" ++++++++++++++++++++++++++++++++", GREEN)],
    ]
    for r in rows:
        p.append(line(tx, ly, r))
        ly += step
    # caption
    cap = ('<text x="64" y="646" font-size="30" fill="%s">'
           'The author isn&#39;t a person. '
           '<tspan font-family="%s" fill="%s" font-weight="700">svc-build-agent</tspan>'
           '. It changed <tspan font-style="italic">how the app is built</tspan> '
           '- and <tspan fill="%s" font-weight="700">812 lines</tspan> of dependencies.'
           '</text>') % (CAP, MONO, PINK, WHITE)
    p.append(cap)
    p.append('</svg>')
    return "\n".join(p)

# ---------------------------------------------------------------- slide 2
def slide_review():
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" font-family="Helvetica, Arial, sans-serif">']
    p.append(bg())
    p.append(f'<text x="64" y="130" font-size="86" font-weight="800" fill="{WHITE}">Who reviewed it?</text>')
    ty = 210
    p.append(titlebar(ty))
    bodytop, h = ty + 44, 300
    p.append(card_frame(bodytop, h))
    tx = CARDX + 34
    ly = bodytop + 42
    step = 29
    rows = [
        [("$ ", MUTE), ("gh", TXT), (" pr", ORANGE), (" checks ", TXT), ("4127", BLUE)],
        [("build     pass   2m14s", TXT)],
        [("scan      pass   0m48s", TXT)],
        [("publish   pass   1m03s", TXT)],
        [("✓ ", GREEN), ("all checks passed → merged to main", TXT)],
        [(" ", TXT)],
        [("$ ", MUTE), ("gh", TXT), (" pr", ORANGE), (" view ", TXT), ("4127", BLUE),
         (" --json", PURPLE), (" reviews ", TXT), ("-q", PURPLE), (" '.reviews'", GREEN)],
    ]
    for r in rows:
        p.append(line(tx, ly, r, size=23))
        ly += step
    # blinking-cursor block on the next line
    p.append(f'<rect x="{tx}" y="{ly-19}" width="15" height="22" fill="none" stroke="{TXT}" stroke-width="2"/>')
    # caption
    cap = ('<text x="64" y="612" font-size="30" fill="%s">CI said yes. '
           '<tspan fill="%s" font-weight="700">The reviewers array is empty.</tspan></text>') % (CAP, WHITE)
    p.append(cap)
    p.append('</svg>')
    return "\n".join(p)

# ---------------------------------------------------------------- slide 3 (punchline / recap)
def slide_approve():
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" font-family="Helvetica, Arial, sans-serif">']
    p.append(bg())
    p.append(f'<text x="64" y="128" font-size="78" font-weight="800" fill="{WHITE}">Who approved that build?</text>')
    ty = 214
    p.append(titlebar(ty))
    bodytop, h = ty + 44, 272
    p.append(card_frame(bodytop, h))
    tx = CARDX + 34
    ly = bodytop + 42
    step = 29
    rows = [
        [("$ ", MUTE), ("git", ORANGE), (" log ", TXT), ("-1", ORANGE), (" --format=", TXT), ("'%an'", GREEN)],
        [("svc-build-agent", TXT), ("   # an agent, not a person", MUTE)],
        [(" ", TXT)],
        [("$ ", MUTE), ("gh", TXT), (" pr", ORANGE), (" view ", TXT), ("4127", BLUE),
         (" --json", PURPLE), (" reviews ", TXT), ("-q", PURPLE), (" '.reviews | length'", GREEN)],
        [("0", PINK, True), ("   # human reviewers", MUTE)],
    ]
    for r in rows:
        p.append(line(tx, ly, r, size=23))
        ly += step
    cap = ('<text x="64" y="600" font-size="30" fill="%s">An agent wrote it. CI approved it. '
           '<tspan fill="%s" font-weight="700">No human ever did.</tspan></text>') % (CAP, WHITE)
    p.append(cap)
    p.append('</svg>')
    return "\n".join(p)

FRAMES = [("slide-incident-commit", slide_commit()),
          ("slide-incident-review", slide_review()),
          ("slide-incident-approve", slide_approve())]

for name, doc in FRAMES:
    with open(f"{OUT}/{name}.svg", "w") as f:
        f.write(doc)
    subprocess.run(["rsvg-convert", "-w", "1600", "-h", "900",
                    f"{OUT}/{name}.svg", "-o", f"{OUT}/{name}.png"], check=True)
    subprocess.run(["cwebp", "-q", "90", f"{OUT}/{name}.png", "-o", f"{OUT}/{name}.webp"],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("rendered", name)
print("DONE", len(FRAMES), "frames")
