#!/usr/bin/env python3
"""Rebuild the "DHI MCP Server - the agent chooses wisely" slide natively, with
clean spacing so the subtitle no longer crowds the section heading. Same palette
and fonts as the other generated slides. Overwrites assets/slide-48.webp."""
import subprocess, os

OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(OUT)

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")

CODE = [
    ("# Claude Desktop - claude_desktop_config.json", True),
    ("{", False),
    ('  "mcpServers": {', False),
    ('    "dhi": {', False),
    ('      "url": "https://dhi.io/mcp"', False),
    ("    }", False),
    ("  }", False),
    ("}", False),
    ("", False),
    ("# Claude Code", True),
    ("claude mcp add dhi --url https://dhi.io/mcp", False),
]

QUESTIONS = [
    "Find the Node.js hardened image with the fewest CVEs",
    "Does dhi.io/node:24-debian13 have FIPS and STIG attestations?",
    "What packages are in catalog-service:dhi and do any have known exploits?",
]

# (name, description) in column-major reading order per row
TOOLS = [
    ("dhi_list_repositories", "Search catalog by name, FIPS, STIG"),
    ("dhi_get_image_cves", "CVEs with CVSS, EPSS, fix version"),
    ("dhi_get_image_packages", "Full SBOM - packages, licenses, purls"),
    ("dhi_get_image_attestations", "SBOM, provenance, FIPS, STIG"),
    ("dhi_get_repository", "Tags, platforms, vuln counts"),
    ("dhi_create_mirror", "Mirror DHI repo to your org"),
]

def svg():
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" font-family="Helvetica, Arial, sans-serif">']
    p.append('<rect width="1600" height="900" fill="#FFFFFF"/>')
    # title + subtitle (subtitle kept to one line, with a real gap before content)
    p.append('<text x="70" y="74" font-size="40" font-weight="800" fill="#0B1533">DHI MCP Server - the agent chooses wisely</text>')
    p.append('<text x="70" y="112" font-size="19" fill="#64748B">The agent that introduced vulnerabilities can now query what\'s secure - before picking a base image.</text>')

    # ---- LEFT column ----
    p.append('<text x="70" y="196" font-size="15" font-weight="800" fill="#0B1533" letter-spacing="0.6">CONNECT YOUR AI ASSISTANT (ONE CONFIG)</text>')
    cx, cy, cw, ch = 70, 212, 690, 372
    p.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="12" fill="#0B1220"/>')
    ty = cy + 40
    mono = 'font-family="Courier New, monospace"'
    for line, is_comment in CODE:
        col = "#7C8BA5" if is_comment else "#E6EAF2"
        if line:
            p.append(f'<text x="{cx+26}" y="{ty}" font-size="15" {mono} xml:space="preserve" fill="{col}">{esc(line)}</text>')
        ty += 25

    p.append('<text x="70" y="622" font-size="15" font-weight="800" fill="#0B1533" letter-spacing="0.6">WHAT YOU CAN ASK</text>')
    qy = 636
    for q in QUESTIONS:
        p.append(f'<rect x="70" y="{qy}" width="690" height="44" rx="8" fill="#F3F5FA"/>')
        p.append(f'<text x="90" y="{qy+28}" font-size="14.5" font-style="italic" fill="#475569">"{esc(q)}"</text>')
        qy += 50

    # ---- RIGHT column ----
    rx = 800
    p.append(f'<text x="{rx}" y="196" font-size="15" font-weight="800" fill="#0B1533" letter-spacing="0.6">10 TOOLS AVAILABLE TO THE AGENT</text>')
    colw, gap = 355, 20
    cols = [rx, rx + colw + gap]
    rowy = [212, 300, 388]
    ch2 = 80
    for i, (name, desc) in enumerate(TOOLS):
        col = cols[i % 2]
        row = rowy[i // 2]
        p.append(f'<rect x="{col}" y="{row}" width="{colw}" height="{ch2}" rx="10" fill="#EAF1FE"/>')
        p.append(f'<text x="{col+22}" y="{row+34}" font-size="15" font-weight="700" {mono} fill="#2563EB">{esc(name)}</text>')
        p.append(f'<text x="{col+22}" y="{row+60}" font-size="13.5" fill="#334155">{esc(desc)}</text>')

    # callout
    ky, kh = 484, 104
    p.append(f'<rect x="{rx}" y="{ky}" width="730" height="{kh}" rx="12" fill="#0B1533"/>')
    p.append(f'<text x="{rx+26}" y="{ky+42}" font-size="17" fill="#FFFFFF">The agent that triggered vulnerabilities now has the tools to '
             '<tspan font-weight="800">never make</tspan></text>')
    p.append(f'<text x="{rx+26}" y="{ky+70}" font-size="17" fill="#FFFFFF"><tspan font-weight="800">that mistake again</tspan> - by querying DHI before every FROM line.</text>')

    p.append('</svg>')
    return "\n".join(p)

with open(f"{OUT}/dhi-mcp.svg", "w") as f:
    f.write(svg())
subprocess.run(["rsvg-convert", "-w", "1600", "-h", "900", f"{OUT}/dhi-mcp.svg", "-o", f"{OUT}/dhi-mcp.png"], check=True)
subprocess.run(["cwebp", "-q", "90", f"{OUT}/dhi-mcp.png", "-o", f"{OUT}/slide-48.webp"], check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["cp", f"{OUT}/slide-48.webp", f"{ROOT}/lab/securing-the-agentic-stack-slides/assets/slide-48.webp"], check=True)
print("rebuilt slide-48.webp")
