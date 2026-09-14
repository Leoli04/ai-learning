#!/usr/bin/env python3
"""Health check for ai-learning docs: fence pairing, HTML tag balance, meta lines."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent / "docs"
issues = []

for md in sorted(ROOT.rglob("*.md")):
    if ".vitepress" in md.parts or md.name == "index.md":
        continue
    text = md.read_text(encoding="utf-8")
    lines = text.splitlines()
    rel = md.relative_to(ROOT)

    # 1. Fence pairing (``` count must be even)
    fence_count = sum(1 for l in lines if l.strip().startswith("```"))
    if fence_count % 2 != 0:
        issues.append(f"{rel}: unbalanced code fences ({fence_count} backtick-fence lines)")

    # Strip fenced code blocks before structural checks (H1 / container checks)
    in_fence = False
    outside = []
    for l in lines:
        if l.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            outside.append(l)
    text_outside = "\n".join(outside)

    # 2. Required frontmatter title
    if not text.startswith("---\ntitle:"):
        issues.append(f"{rel}: missing frontmatter title")

    # 3. Required meta line (约 X 分钟 · 关键词)
    if not re.search(r"^> 约 \d+ 分钟 · 关键词：", text, re.MULTILINE):
        issues.append(f"{rel}: missing meta line (约 X 分钟 · 关键词)")

    # 4. Figure/figcaption balance
    fig_open = len(re.findall(r"<figure", text))
    fig_cap = len(re.findall(r"<figcaption", text))
    if fig_open != fig_cap:
        issues.append(f"{rel}: figure({fig_open}) != figcaption({fig_cap})")

    # 5. Container balance (opener vs closer, excluding fenced code)
    openers = len(re.findall(r"^::: [a-z]+", text_outside, re.MULTILINE))
    closers = len(re.findall(r"^:::\s*$", text_outside, re.MULTILINE))
    if openers != closers:
        issues.append(f"{rel}: container openers({openers}) != closers({closers})")

    # 6. SVG open/close balance
    svg_open = len(re.findall(r"<svg\b", text))
    svg_close = len(re.findall(r"</svg>", text))
    if svg_open != svg_close:
        issues.append(f"{rel}: <svg>({svg_open}) != </svg>({svg_close})")

    # 7. H1 must exist exactly once (excluding fenced code)
    h1_count = len(re.findall(r"^# \S", text_outside, re.MULTILINE))
    if h1_count != 1:
        issues.append(f"{rel}: H1 count = {h1_count} (expect 1)")

    # 8. No legacy <pre><code> blocks (should be ``` fences)
    if "<pre><code>" in text:
        issues.append(f"{rel}: legacy <pre><code> block (convert to ``` fence)")

    # 9. No hardcoded hex colors on SVG elements
    hex_colors = re.findall(r'(?:fill|stroke)="#[0-9a-fA-F]{3,8}"', text)
    if hex_colors:
        issues.append(f"{rel}: {len(hex_colors)} hardcoded SVG hex color(s): {hex_colors[:3]}")

if issues:
    print(f"FOUND {len(issues)} issues:")
    for i in issues:
        print(" -", i)
else:
    print("ALL CLEAN")