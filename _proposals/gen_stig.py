#!/usr/bin/env python3
"""Rebuild the STIG slide natively with clear title/sub-heading/paragraph spacing,
matching the FIPS rebuild. Overwrites assets/slide-29.webp."""
import subprocess, os

OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(OUT)
MONO = 'font-family="Courier New, monospace"'

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")

PARA = [
    ("STIGs define secure configuration baselines published by DISA", None),
    ("for DoD environments. DISA has not yet published a", None),
    ("container-specific STIG - Docker creates custom profiles based", None),
    ("on the ", "GPOS SRG + DoD Container Hardening Process Guide."),
]

BULLETS = [
    "DHI ships signed STIG scan attestations",
    "Reduces false positives common in container STIG scans",
    "STIG variant requires a Docker subscription",
]

TERM = [
    ("# Inspect the signed STIG attestation", "c"),
    ("docker scout attest get \\", ""),
    ("  --predicate-type https://docker.com/dhi/stig/v0.1 \\", ""),
    ("  --verify \\", ""),
    ("  dhi.io/node:24-debian13-fips", ""),
    ("", ""),
    ("# View all attestations on a DHI image", "c"),
    ("docker scout attest list \\", ""),
    ("  dhi.io/node:24-debian13", ""),
    ("", ""),
    ("# Attestation types you'll see:", "c"),
    ("# SBOM · OpenVEX · SLSA · FIPS · STIG", "c"),
    ("# Scout health · Secrets scan", "c"),
]

def check(x, y):
    return (f'<path d="M{x},{y} l6,7 l12,-15" stroke="#16A34A" stroke-width="3.5" '
            'fill="none" stroke-linecap="round" stroke-linejoin="round"/>')

def svg():
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" font-family="Helvetica, Arial, sans-serif">']
    p.append('<rect width="1600" height="900" fill="#FFFFFF"/>')
    # shield icon (purple)
    p.append('<rect x="95" y="92" width="48" height="48" rx="12" fill="#EDE9FE"/>')
    p.append('<path d="M119,101 L131,106 L131,116 Q131,127 119,132 Q107,127 107,116 L107,106 Z" fill="#7C3AED"/>')
    p.append('<path d="M119,111 v9 M114.5,115.5 h9" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round"/>')
    # title
    p.append('<text x="160" y="132" font-size="46" font-weight="800" fill="#0B1533">STIG</text>')
    # sub-heading
    p.append('<text x="95" y="205" font-size="21" fill="#64748B">Security Technical Implementation Guide - DoD hardening standard</text>')
    # paragraph
    py = 260
    for line, bold in PARA:
        if bold:
            p.append(f'<text x="95" y="{py}" font-size="20" fill="#334155">{esc(line)}<tspan font-weight="800" fill="#0B1533">{esc(bold)}</tspan></text>')
        else:
            p.append(f'<text x="95" y="{py}" font-size="20" fill="#334155">{esc(line)}</text>')
        py += 31
    # bullets
    by = 420
    for b in BULLETS:
        p.append(check(96, by - 14))
        p.append(f'<text x="128" y="{by}" font-size="19" fill="#0B1533">{esc(b)}</text>')
        by += 52
    # terminal
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

with open(f"{OUT}/stig.svg", "w") as f:
    f.write(svg())
subprocess.run(["rsvg-convert", "-w", "1600", "-h", "900", f"{OUT}/stig.svg", "-o", f"{OUT}/stig.png"], check=True)
subprocess.run(["cwebp", "-q", "90", f"{OUT}/stig.png", "-o", f"{OUT}/slide-29.webp"], check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["cp", f"{OUT}/slide-29.webp", f"{ROOT}/lab/securing-the-agentic-stack-slides/assets/slide-29.webp"], check=True)
print("rebuilt slide-29.webp")
