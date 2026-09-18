#!/usr/bin/env python3
"""Deterministic SWIR Progress SVG generator/check for Image to TXT."""
from __future__ import annotations
import argparse, re
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "assets" / "readme"
LEGACY = re.compile(r"(?:[█▓▒░]{4,}|\[(?:[#=\-]){6,}\])")
CARD = (ASSET / "progress-card.svg").read_text(encoding="utf-8") if (ASSET / "progress-card.svg").exists() else ""
MINI = (ASSET / "progress-mini.svg").read_text(encoding="utf-8") if (ASSET / "progress-mini.svg").exists() else ""

def canonical_card() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="180" viewBox="0 0 1200 180" role="img" aria-labelledby="title desc"><title id="title">Image to TXT product progress</title><desc id="desc">Product progress is N/A because there is no authoritative measurable roadmap.</desc><defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#02050A"/><stop offset="1" stop-color="#07111C"/></linearGradient><pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="#62E5FF" stroke-opacity=".05"/></pattern></defs><rect x="1" y="1" width="1198" height="178" rx="22" fill="url(#bg)" stroke="#62E5FF" stroke-opacity=".25"/><rect x="1" y="1" width="1198" height="178" rx="22" fill="url(#grid)"/><text x="50" y="38" fill="#62E5FF" font-family="Segoe UI,Arial,sans-serif" font-size="15" font-weight="700" letter-spacing="3">SWIR PROGRESS</text><text x="50" y="72" fill="#F4FAFF" font-family="Segoe UI,Arial,sans-serif" font-size="26" font-weight="800">Image to TXT</text><text x="50" y="98" fill="#8DA8B8" font-family="Segoe UI,Arial,sans-serif" font-size="14">Product progress · no authoritative roadmap</text><text x="1110" y="72" text-anchor="end" fill="#F4FAFF" font-family="Segoe UI,Arial,sans-serif" font-size="30" font-weight="800">N/A</text><text x="1110" y="98" text-anchor="end" fill="#62E5FF" font-family="Segoe UI,Arial,sans-serif" font-size="13" font-weight="700">N/A</text><rect x="50" y="116" width="1100" height="18" rx="9" fill="#08131F" stroke="#62E5FF" stroke-opacity=".15"/><text x="50" y="158" fill="#8DA8B8" font-family="Segoe UI,Arial,sans-serif" font-size="12">Product completion: N/A · no measurable completion denominator is documented</text></svg>\n'''

def canonical_mini() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="72" viewBox="0 0 900 72" role="img" aria-labelledby="title desc"><title id="title">Image to TXT compact product progress</title><desc id="desc">Product progress is N/A because there is no authoritative measurable roadmap.</desc><rect x="1" y="1" width="898" height="70" rx="16" fill="#02050A" stroke="#62E5FF" stroke-opacity=".24"/><text x="24" y="28" fill="#F4FAFF" font-family="Segoe UI,Arial,sans-serif" font-size="14" font-weight="700">Image to TXT · Product progress</text><text x="24" y="51" fill="#8DA8B8" font-family="Segoe UI,Arial,sans-serif" font-size="12">Product completion: N/A</text><rect x="590" y="27" width="220" height="14" rx="7" fill="#08131F" stroke="#62E5FF" stroke-opacity=".15"/><text x="866" y="40" text-anchor="end" fill="#62E5FF" font-family="Segoe UI,Arial,sans-serif" font-size="14" font-weight="800">N/A</text></svg>\n'''

def check() -> int:
    for name, expected in (("progress-card.svg", canonical_card()), ("progress-mini.svg", canonical_mini())):
        ET.fromstring(expected)
        path = ASSET / name
        if not path.exists() or path.read_text(encoding="utf-8") != expected:
            print(f"stale or missing: {path}"); return 1
    template = ASSET / "progress-template.svg"
    if not template.exists(): print("missing progress-template.svg"); return 1
    ET.fromstring(template.read_text(encoding="utf-8"))
    if LEGACY.search((ROOT / "README.md").read_text(encoding="utf-8")):
        print("legacy progress meter found in README.md"); return 1
    print("SWIR progress check: OK"); return 0

def main() -> int:
    p = argparse.ArgumentParser(); p.add_argument("--check", action="store_true"); a = p.parse_args()
    if not a.check:
        ASSET.mkdir(parents=True, exist_ok=True)
        (ASSET / "progress-card.svg").write_text(canonical_card(), encoding="utf-8")
        (ASSET / "progress-mini.svg").write_text(canonical_mini(), encoding="utf-8")
    return check()

if __name__ == "__main__": raise SystemExit(main())
