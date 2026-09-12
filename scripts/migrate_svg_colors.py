"""把 docs 下所有 .md 里 SVG 的硬编码颜色改成双主题自适应的 class。

规则：
  填充 #161b22 / #1c2128 -> cell
  浅色 rgba 填充 -> cell-em
  强调色硬色 -> accent-*-fill
  描边 #30363d -> cell；强调色描边 -> link / link-* 等
  类名 svg-text 删；svg-dim 改 dim；svg-blue/green/orange/purple/red 改 accent-*
"""
import re
from pathlib import Path

ROOT = Path("F:/lixiaofei/WorkBuddy/技术/ai-learning/docs")

FILL_MAP = [
    ("#161b22",         "cell"),
    ("#1c2128",         "cell"),
    ("rgba(91,140,255,0.10)", "cell-em"),
    ("rgba(91,140,255,0.12)", "cell-em"),
    ("rgba(91,140,255,0.08)", "cell-em"),
    ("rgba(91,140,255,0.14)", "cell-em"),
    ("rgba(63,185,80,0.08)",  "cell-em"),
    ("rgba(63,185,80,0.10)",  "cell-em"),
    ("rgba(240,136,62,0.08)", "cell-em"),
    ("rgba(240,136,62,0.10)", "cell-em"),
    ("rgba(188,140,255,0.08)","cell-em"),
    ("rgba(188,140,255,0.10)","cell-em"),
    ("#5b8cff",  "accent-blue-fill"),
    ("#3fb950",  "accent-green-fill"),
    ("#f0883e",  "accent-orange-fill"),
    ("#bc8cff",  "accent-purple-fill"),
    ("#e5534b",  "accent-red-fill"),
]

STROKE_MAP = [
    ("#30363d", "cell"),
    ("#5b8cff", "link"),
    ("#3fb950", "link-green"),
    ("#f0883e", "link-orange"),
    ("#bc8cff", "link-purple"),
]

LEGACY_CLASSES = {
    "svg-text":  None,
    "svg-dim":   "dim",
    "svg-blue":  "accent-blue",
    "svg-green": "accent-green",
    "svg-orange":"accent-orange",
    "svg-purple":"accent-purple",
    "svg-red":   "accent-red",
}


def norm_classes(s):
    parts = []
    for tok in s.replace(",", " ").split():
        for piece in tok.split():
            mapped = LEGACY_CLASSES.get(piece, piece)
            if mapped:
                parts.append(mapped)
    seen, out = set(), []
    for p in parts:
        if p not in seen:
            seen.add(p); out.append(p)
    return " ".join(out)


def transform_attrs(tag, attrs):
    fill_m   = re.search(r'fill="([^"]*)"',   attrs)
    stroke_m = re.search(r'stroke="([^"]*)"', attrs)
    class_m  = re.search(r'class="([^"]*)"',  attrs)

    classes = class_m.group(1).split() if class_m else []

    if fill_m:
        fv = fill_m.group(1).strip()
        if fv != "none":
            for code, cls in FILL_MAP:
                if fv.lower() == code.lower():
                    classes.append(cls); break
    if stroke_m:
        sv = stroke_m.group(1).strip()
        if sv != "none":
            for code, cls in STROKE_MAP:
                if sv.lower() == code.lower():
                    classes.append(cls); break

    nc = norm_classes(" ".join(classes))

    new_attrs = re.sub(r'\s*fill="[^"]*"',   '', attrs)
    new_attrs = re.sub(r'\s*stroke="[^"]*"', '', new_attrs)
    new_attrs = re.sub(r'\s*class="[^"]*"',  '', new_attrs)
    if nc:
        new_attrs += f' class="{nc}"'
    return f"<{tag}{new_attrs}"


TAG_RE = re.compile(
    r'<(rect|text|circle|line|g|ellipse|polyline|path)([^>/]*?)(\s*/?>)',
    re.S,
)


def transform_svg(svg):
    def repl(m):
        tag, attrs, end = m.group(1), m.group(2), m.group(3)
        new = transform_attrs(tag, attrs)
        return new + (end if end.strip() == "/>" else ">")
    return TAG_RE.sub(repl, svg)


def process_md(md):
    n, chunks, last = 0, [], 0
    for m in re.finditer(r'<svg[\s\S]*?</svg>', md):
        chunks.append(md[last:m.start()])
        chunks.append(transform_svg(m.group(0)))
        last = m.end(); n += 1
    chunks.append(md[last:])
    return "".join(chunks), n


def main():
    changed, total = 0, 0
    for p in ROOT.rglob("*.md"):
        txt = p.read_text(encoding="utf-8")
        if "<svg" not in txt: continue
        new, n = process_md(txt)
        if n and new != txt:
            p.write_text(new, encoding="utf-8")
            print(f"  {p.relative_to(ROOT.parent)} : {n} svg(s)")
            changed += 1; total += n
    print(f"--- {changed} files, {total} svgs migrated ---")


if __name__ == "__main__":
    main()
