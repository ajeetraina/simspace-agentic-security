#!/usr/bin/env python3
"""'Horror stories' beat - inserted after the 02:47 AM cold-open (slide-incident-approve).
A dark divider in the incident palette, then two real documented AI-agent incidents
(Docker blog comics) normalised onto clean 1600x900 canvases.
  slide-horror         - dark divider
  slide-horror-1       - 'rm -rf *' with root: .ssh / .aws / prod (security-risks blog)
  slide-horror-2       - 'clean up my desktop' -> rm -rf family_photos/ (rm-rf-incident blog)
SVG -> png -> webp via rsvg-convert + cwebp; comics fit-contained via Pillow."""
import subprocess, os
from PIL import Image, ImageFilter

OUT = os.path.dirname(os.path.abspath(__file__))
CACHE = "/Users/ajeetraina/.claude/image-cache/3ddb7cbc-2fb2-4adc-b397-b8c57f9dddab"

BG, SWOOSH, WHITE = "#0B1533", "#111E42", "#FFFFFF"
CAP, ACCENT, PINK = "#AEB9D6", "#4F7CFF", "#E5548A"
MONO = "Menlo, 'DejaVu Sans Mono', 'Courier New', monospace"

def bg():
    return (f'<rect width="1600" height="900" fill="{BG}"/>'
            f'<path d="M1080,-80 C1280,120 1170,400 1440,500 S1660,780 1600,1000 '
            f'L1760,1000 L1760,-120 Z" fill="{SWOOSH}" opacity="0.55"/>'
            f'<path d="M-120,560 C160,470 300,690 560,600 S900,540 1040,760 '
            f'L1040,1000 L-160,1000 Z" fill="{SWOOSH}" opacity="0.40"/>')

def divider():
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" font-family="Helvetica, Arial, sans-serif">']
    p.append(bg())
    p.append(f'<text x="72" y="240" font-size="34" font-weight="800" fill="{PINK}" letter-spacing="2">FROM THE WILD</text>')
    p.append(f'<text x="70" y="350" font-size="104" font-weight="800" fill="{WHITE}">Horror stories</text>')
    p.append(f'<text x="72" y="410" font-size="34" fill="{CAP}">These aren&#39;t hypothetical - they shipped, and someone paid for them.</text>')
    # two teaser rows - single clean line each
    rows = [
        ("1", "“Clean up my project folder”", " → agent had root, ran ", "rm -rf *", " — .ssh · .aws · prod.db gone"),
        ("2", "“Organize my wife’s desktop”", " → ", "rm -rf family_photos/", " — Trash bypassed, 15 yrs of photos gone"),
    ]
    y = 500
    for num, quote, pre, cmd, post in rows:
        p.append(f'<rect x="72" y="{y}" width="1456" height="96" rx="12" fill="#17213E"/>')
        p.append(f'<rect x="72" y="{y}" width="6" height="96" rx="3" fill="{ACCENT}"/>')
        p.append(f'<text x="116" y="{y+60}" font-size="30" font-weight="800" fill="{ACCENT}">{num}</text>')
        p.append(f'<text x="164" y="{y+58}" font-size="23" xml:space="preserve">'
                 f'<tspan font-weight="700" fill="{WHITE}">{quote}</tspan>'
                 f'<tspan fill="{CAP}">{pre}</tspan>'
                 f'<tspan font-family="{MONO}" font-weight="700" fill="{PINK}">{cmd}</tspan>'
                 f'<tspan fill="{CAP}">{post}</tspan></text>')
        y += 112
    p.append('</svg>')
    return "\n".join(p)

# --- divider ---
with open(f"{OUT}/slide-horror.svg", "w") as f:
    f.write(divider())
subprocess.run(["rsvg-convert", "-w", "1600", "-h", "900",
                f"{OUT}/slide-horror.svg", "-o", f"{OUT}/slide-horror.png"], check=True)
subprocess.run(["cwebp", "-q", "90", f"{OUT}/slide-horror.png", "-o", f"{OUT}/slide-horror.webp"],
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("rendered slide-horror")

# --- comics: fit-contain onto 1600x900 white canvas (no stretch) ---
def contain(src, dst):
    # Render at 2x (3200x1800) so the webp carries extra pixels for the projector,
    # LANCZOS resample, then an unsharp pass to keep comic text crisp (not blurred).
    S = 2
    im = Image.open(src).convert("RGB")
    canvas = Image.new("RGB", (1600 * S, 900 * S), "#FFFFFF")
    scale = min(1600 * S / im.width, 900 * S / im.height)
    w, h = round(im.width * scale), round(im.height * scale)
    im = im.resize((w, h), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=120, threshold=2))
    canvas.paste(im, ((1600 * S - w) // 2, (900 * S - h) // 2))
    canvas.save(dst, "WEBP", quality=95, method=6)
    print("rendered", os.path.basename(dst), canvas.size)

contain(f"{CACHE}/2.jpeg", f"{OUT}/slide-horror-1.webp")
contain(f"{CACHE}/3.jpeg", f"{OUT}/slide-horror-2.webp")
print("DONE")
