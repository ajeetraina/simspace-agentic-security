#!/usr/bin/env python3
"""Rebuild "Wire the DHI MCP Server into the Sandbox" natively so the terminal
text is white and legible (was dark blue on near-black). Overwrites slide-50.webp."""
import subprocess, os

OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(OUT)
MONO = 'font-family="Courier New, monospace"'
CODE = "#FFFFFF"      # commands - white, high contrast
CMNT = "#7FE0A0"      # comments - light green, still clearly visible
TERM_BG = "#0B1220"

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")

def term(p, x, y, w, h, lines, size=15.5, lh=24):
    p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{TERM_BG}"/>')
    ty = y + 40
    for text, kind in lines:
        if text:
            col = CMNT if kind == "c" else CODE
            p.append(f'<text x="{x+26}" y="{ty}" font-size="{size}" {MONO} xml:space="preserve" fill="{col}">{esc(text)}</text>')
        ty += lh

LEFT1 = [
    ("# One-time host setup", "c"),
    ("brew install docker/tap/sbx", ""),
    ("export SBX_MCP_URL=https://gateway.docker.com", ""),
    ("", ""),
    ("# Start the sandbox daemon", "c"),
    ("sbx daemon stop && sbx daemon start -d", ""),
    ("", ""),
    ("# Nothing wired in yet", "c"),
    ("sbx mcp --help", ""),
    ("sbx mcp ls", ""),
]
LEFT2 = [
    ("# Register the DHI MCP server by URL", "c"),
    ("sbx mcp add remotedhi --url https://dhi.io/mcp", ""),
    ("sbx mcp inspect remotedhi", ""),
    ("Name:      remotedhi", ""),
    ("Type:      remote", ""),
    ("URL:       https://dhi.io/mcp", ""),
    ("Transport: streamable-http", ""),
]
RIGHT = [
    ("cd ~/workdemo", ""),
    ("sbx run codex --static-mcp remotedhi", ""),
    ("", ""),
    ("> /mcp", ""),
    ("MCP Tools - mcp-gateway (Auth: Unsupported)", ""),
    ("Tools: code-mode, mcp-exec,", ""),
    ("remotedhi__dhi_get_image_cves,", ""),
    ("remotedhi__dhi_get_image_details, + 8 more", ""),
]
CALLOUT_BODY = [
    "code-mode, mcp-exec, dhi_get_image_cves,",
    "dhi_get_image_details, + 6 more read-only queries.",
    "Mutating tools (dhi_create_mirror, dhi_remove_mirror)",
    "are the ones to scope with policy - next slide.",
]

def svg():
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" font-family="Helvetica, Arial, sans-serif">']
    p.append('<rect width="1600" height="900" fill="#FFFFFF"/>')
    p.append('<text x="95" y="96" font-size="42" font-weight="800" fill="#0B1533">Wire the DHI MCP Server into the Sandbox</text>')
    lx, rx, cw = 95, 830, 675
    # left
    p.append(f'<text x="{lx}" y="176" font-size="16" font-weight="800" fill="#0B1533" letter-spacing="0.6">1. SET UP THE SANDBOX</text>')
    term(p, lx, 190, cw, 336, LEFT1)
    term(p, lx, 540, cw, 228, LEFT2)
    # right
    p.append(f'<text x="{rx}" y="176" font-size="16" font-weight="800" fill="#0B1533" letter-spacing="0.6">2. QUERY IT FROM THE AGENT</text>')
    term(p, rx, 190, cw, 252, RIGHT)
    # callout
    ky, kh = 456, 300
    p.append(f'<rect x="{rx}" y="{ky}" width="{cw}" height="{kh}" rx="12" fill="#E7EFFE"/>')
    p.append(f'<text x="{rx+26}" y="{ky+40}" font-size="18" font-weight="800" fill="#2563EB">10 tools now available to the agent</text>')
    by = ky + 70
    for line in CALLOUT_BODY:
        p.append(f'<text x="{rx+26}" y="{by}" font-size="15" fill="#33415A">{esc(line)}</text>')
        by += 23
    # small terminal inside callout
    sx, sy, sw, sh = rx + 26, ky + 188, cw - 52, 74
    p.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="8" fill="{TERM_BG}"/>')
    p.append(f'<text x="{sx+22}" y="{sy+30}" font-size="15" {MONO} fill="{CODE}">$ sbx mcp ls</text>')
    p.append(f'<text x="{sx+22}" y="{sy+56}" font-size="15" {MONO} xml:space="preserve" fill="{CODE}">remotedhi   remote   streamable-http</text>')
    p.append('</svg>')
    return "\n".join(p)

with open(f"{OUT}/wire-mcp.svg", "w") as f:
    f.write(svg())
subprocess.run(["rsvg-convert", "-w", "1600", "-h", "900", f"{OUT}/wire-mcp.svg", "-o", f"{OUT}/wire-mcp.png"], check=True)
subprocess.run(["cwebp", "-q", "90", f"{OUT}/wire-mcp.png", "-o", f"{OUT}/slide-50.webp"], check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["cp", f"{OUT}/slide-50.webp", f"{ROOT}/lab/securing-the-agentic-stack-slides/assets/slide-50.webp"], check=True)
print("rebuilt slide-50.webp")
