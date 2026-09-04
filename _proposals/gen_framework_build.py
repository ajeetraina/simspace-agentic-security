#!/usr/bin/env python3
"""Turn the four-questions framework slide into a 4-frame spotlight build:
each frame keeps one card (Evidence / Baseline / Gate / Boundary) at full blue
and fades the other three toward white. Deck is image-per-slide, so the presenter
arrows through slide-framework-1..4 and it reads as highlighting each in turn.
Operates on the existing raster (assets/slide-framework.webp) so it matches exactly."""
import os
from PIL import Image
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "lab/securing-the-agentic-stack-slides/assets/slide-framework.webp")
OUT_ASSETS = os.path.dirname(BASE)
OUT_PROP = os.path.dirname(os.path.abspath(__file__))

CARDS = [(66, 415), (440, 789), (814, 1164), (1188, 1538)]  # x-bounds per card
Y0, Y1 = 183, 650
FADE = 0.65  # how far dimmed cards blend toward white (0=none, 1=white)

base = Image.open(BASE).convert("RGB")

for i in range(4):
    frame = np.asarray(base).astype(np.float32).copy()
    white = np.float32(255.0)
    for j, (x0, x1) in enumerate(CARDS):
        if j == i:
            continue  # active card stays full colour
        region = frame[Y0:Y1, x0:x1]
        frame[Y0:Y1, x0:x1] = region * (1 - FADE) + white * FADE
    img = Image.fromarray(frame.clip(0, 255).astype("uint8"))
    name = f"slide-framework-{i+1}"
    img.save(os.path.join(OUT_ASSETS, f"{name}.webp"), "WEBP", quality=90, method=6)
    img.save(os.path.join(OUT_PROP, f"{name}.webp"), "WEBP", quality=90, method=6)
    print("wrote", name)
print("DONE")
