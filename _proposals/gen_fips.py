#!/usr/bin/env python3
"""Rebuild the FIPS 140 slide natively with clear vertical spacing between the
title, sub-heading, paragraph and bullets (they were crammed together).
Overwrites assets/slide-28.webp."""
import subprocess, os

OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(OUT)
MONO = 'font-family="Courier New, monospace"'

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")

PARA = [
    "FIPS 140 mandates that cryptographic modules meet NIST-validated",
    "standards. Required for US government contracts, healthcare",
    "(HIPAA), finance, and defense workloads.",
]

TERM = [
    ("# Pull the FIPS variant", "c"),
    ("FROM dhi.io/node:24-debian13-fips", ""),
    ("", ""),
    ("# Inspect the signed FIPS attestation", "c"),
    ("docker scout attest get \\", ""),
    ("  --predicate-type https://docker.com/dhi/fips/v0.1 \\", ""),
    ("  --verify \\", ""),
    ("  dhi.io/node:24-debian13-fips", ""),
    ("", ""),
    ("# Output shows certification details:", "c"),
    ('# "standard": "FIPS 140-3"', "c"),
    ('# "certification": "CMVP #4985"', "c"),
    ('# "status": "active"', "c"),
]

def check(x, y):
    return (f'<path d="M{x},{y} l6,7 l12,-15" stroke="#16A34A" stroke-width="3.5" '
            'fill="none" stroke-linecap="round" stroke-linejoin="round"/>')

def svg():
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" font-family="Helvetica, Arial, sans-serif">']
    p.append('<rect width="1600" height="900" fill="#FFFFFF"/>')
    # lock icon
    p.append('<rect x="95" y="92" width="48" height="48" rx="12" fill="#E7EFFE"/>')
    p.append('<rect x="110" y="116" width="18" height="14" rx="2.5" fill="#1E40AF"/>')
    p.append('<path d="M113,116 L113,111 A6,6 0 0 1 125,111 L125,116" stroke="#1E40AF" stroke-width="2.6" fill="none"/>')
    # title
    p.append('<text x="160" y="132" font-size="46" font-weight="800" fill="#0B1533">FIPS 140</text>')
    # sub-heading (clear gap below title)
    p.append('<text x="95" y="205" font-size="21" fill="#64748B">Federal Information Processing Standard - validated cryptography</text>')
    # paragraph (clear gap below sub-heading)
    py = 262
    for line in PARA:
        p.append(f'<text x="95" y="{py}" font-size="20" fill="#334155">{esc(line)}</text>')
        py += 31
    # bullets (clear gap below paragraph)
    by = 410
    p.append(check(96, by - 14))
    p.append(f'<text x="128" y="{by}" font-size="19" fill="#0B1533">DHI ships a <tspan {MONO} fill="#1E40AF">-fips</tspan> tag variant per image</text>')
    by += 52
    p.append(check(96, by - 14))
    p.append(f'<text x="128" y="{by}" font-size="19" fill="#0B1533">OpenSSL FIPS Provider - CMVP validated</text>')
    by += 52
    p.append(check(96, by - 14))
    p.append(f'<text x="128" y="{by}" font-size="19" fill="#0B1533">Signed FIPS attestation - machine-readable for auditors</text>')
    # right terminal
    tx, ty, tw, th = 975, 160, 555, 560
    p.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="14" fill="#0B1220"/>')
    ly = ty + 46
    for text, kind in TERM:
        if text:
            col = "#7FE0A0" if kind == "c" else "#FFFFFF"
            p.append(f'<text x="{tx+28}" y="{ly}" font-size="15" {MONO} xml:space="preserve" fill="{col}">{esc(text)}</text>')
        ly += 27
    p.append('</svg>')
    return "\n".join(p)

with open(f"{OUT}/fips.svg", "w") as f:
    f.write(svg())
subprocess.run(["rsvg-convert", "-w", "1600", "-h", "900", f"{OUT}/fips.svg", "-o", f"{OUT}/fips.png"], check=True)
subprocess.run(["cwebp", "-q", "90", f"{OUT}/fips.png", "-o", f"{OUT}/slide-28.webp"], check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["cp", f"{OUT}/slide-28.webp", f"{ROOT}/lab/securing-the-agentic-stack-slides/assets/slide-28.webp"], check=True)
print("rebuilt slide-28.webp")
