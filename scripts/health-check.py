#!/usr/bin/env python3
"""Health check for ai-learning docs: fence pairing, HTML tag balance, meta lines."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent / "docs"
issues = []

SVG_RE = re.compile(r'<svg\b[^>]*viewBox="([^"]+)"[^>]*>(.*?)</svg>', re.S)
TEXT_RE = re.compile(r"<text\b([^>]*)>(.*?)</text>", re.S)
GFONT_RE = re.compile(r'<g\b[^>]*font-size="([\d.]+)"')
ROT_RE = re.compile(r"rotate\(\s*(-?[\d.]+)")


def _char_w(ch):
    """Rough advance width in em: CJK/fullwidth 1.0, alnum 0.55, space 0.3, punctuation 0.5."""
    if ord(ch) > 0x2E80:
        return 1.0
    if ch == " ":
        return 0.30
    if ch.isalnum():
        return 0.55
    return 0.50


def _text_width(s, fs):
    return sum(_char_w(c) for c in s) * fs

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

    # 10. SVG text overflow: text extending past the viewBox gets visually clipped
    for fig_no, (vb, body) in enumerate(SVG_RE.findall(text), 1):
        parts = vb.split()
        if len(parts) != 4:
            continue
        W, H = float(parts[2]), float(parts[3])
        gm = GFONT_RE.search(body)
        default_fs = float(gm.group(1)) if gm else 13.0
        for attrs, raw in TEXT_RE.findall(body):
            content = re.sub(r"<[^>]+>", "", raw)
            for ent, ch in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"')):
                content = content.replace(ent, ch)
            content = content.strip()
            if not content:
                continue
            fsm = re.search(r'font-size="([\d.]+)"', attrs)
            fs = float(fsm.group(1)) if fsm else default_fs
            xm = re.search(r'\bx="(-?[\d.]+)"', attrs)
            if not xm:
                continue
            x = float(xm.group(1))
            ym = re.search(r'\by="(-?[\d.]+)"', attrs)
            y = float(ym.group(1)) if ym else 0.0
            am = re.search(r'text-anchor="(\w+)"', attrs)
            anchor = am.group(1) if am else "start"
            rm = ROT_RE.search(attrs)
            rot = float(rm.group(1)) if rm else 0.0
            w = _text_width(content, fs)

            if abs(abs(rot) - 90) < 1:
                # Vertical text: length runs along y, height occupies about one line on x
                if anchor == "middle":
                    y0, y1 = y - w / 2, y + w / 2
                elif anchor == "end":
                    y0, y1 = y - w, y
                else:
                    y0, y1 = y, y + w
                x0, x1 = x, x + fs * 0.9
            else:
                if anchor == "end":
                    x0, x1 = x - w, x
                elif anchor == "middle":
                    x0, x1 = x - w / 2, x + w / 2
                else:
                    x0, x1 = x, x + w
                y0, y1 = y - fs * 0.8, y + fs * 0.25

            if x1 > W - 1:
                issues.append(
                    f'{rel}: 图{fig_no} 文字超出右边界 (x {x0:.0f}~{x1:.0f} > viewBox 宽 {W:.0f}): "{content[:30]}"'
                )
            if x0 < 1:
                issues.append(
                    f'{rel}: 图{fig_no} 文字超出左边界 (x {x0:.0f} < 0): "{content[:30]}"'
                )
            if y1 > H - 1:
                issues.append(
                    f'{rel}: 图{fig_no} 文字超出下边界 (y {y0:.0f}~{y1:.0f} > viewBox 高 {H:.0f}): "{content[:30]}"'
                )
            if y0 < 1:
                issues.append(
                    f'{rel}: 图{fig_no} 文字超出上边界 (y {y0:.0f} < 0): "{content[:30]}"'
                )

if issues:
    print(f"FOUND {len(issues)} issues:")
    for i in issues:
        print(" -", i)
else:
    print("ALL CLEAN")