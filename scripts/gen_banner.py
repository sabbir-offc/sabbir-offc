#!/usr/bin/env python3
"""Generate the profile banner as SVG, in both themes and both widths.

The banner was a single 1280x420 PNG. GitHub lays a README image out at the width
of the markdown column, so that canvas rendered at 0.23x on a 375px phone and put
the technology row at 3.2px -- the same scale problem the stat cards had, and for
the same reason. It was also the one hero image not wrapped in a <picture>, so a
light-mode reader got dark artwork.

So: vector instead of raster (crisp at any size, ~2KB instead of 86KB), a light
variant alongside the dark one, and a 520-wide portrait variant whose type is sized
for a phone column rather than scaled down into it.

Content lives in CONTENT below -- edit that, re-run, commit the SVGs.
Stdlib only. Takes no token and hits no network, unlike gen_cards.py.

Writes Images/banner[-mobile]-{dark,light}.svg
"""
import os

OUT = "Images"

CONTENT = {
    "eyebrow": "FULL-STACK ENGINEER",
    "name": "Md. Sabbir Howlader",
    "tagline": "Building multi-tenant platforms at NeXbit LTD",
    # Kept to six on desktop; the mobile variant splits them across two rows.
    "tags": ["TypeScript", "Next.js", "Go", "Postgres", "Electron", "Linux"],
}

THEMES = {
    "dark": dict(
        bg0="#0D1117", bg1="#0B0E14",
        accent_a="#58A6FF", accent_b="#BF91F3",
        eyebrow="#58A6FF", name="#E6EDF3", tagline="#8B949E", tag="#6E7681",
        dot="#FFFFFF", dot_op="0.05",
        glow_a="#1F6FEB", glow_b="#8957E5", glow_op="0.30",
    ),
    "light": dict(
        bg0="#FFFFFF", bg1="#F0F3F7",
        accent_a="#0969DA", accent_b="#8250DF",
        eyebrow="#0969DA", name="#1F2328", tagline="#57606A", tag="#6E7781",
        dot="#1F2328", dot_op="0.055",
        glow_a="#54AEFF", glow_b="#C297FF", glow_op="0.26",
    ),
}

SANS = ("-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,"
        "'Liberation Sans',sans-serif")
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"


def _defs(c, uid, w, h):
    """Background wash, accent gradient, dot grid and the two corner glows."""
    return f"""  <defs>
    <linearGradient id="bg{uid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{c['bg0']}"/>
      <stop offset="1" stop-color="{c['bg1']}"/>
    </linearGradient>
    <linearGradient id="acc{uid}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{c['accent_a']}"/>
      <stop offset="1" stop-color="{c['accent_b']}"/>
    </linearGradient>
    <linearGradient id="rule{uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{c['accent_a']}"/>
      <stop offset="1" stop-color="{c['accent_b']}"/>
    </linearGradient>
    <radialGradient id="g1{uid}">
      <stop offset="0" stop-color="{c['glow_a']}" stop-opacity="{c['glow_op']}"/>
      <stop offset="1" stop-color="{c['glow_a']}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="g2{uid}">
      <stop offset="0" stop-color="{c['glow_b']}" stop-opacity="{c['glow_op']}"/>
      <stop offset="1" stop-color="{c['glow_b']}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="dots{uid}" width="16" height="16" patternUnits="userSpaceOnUse">
      <circle cx="1.5" cy="1.5" r="1.5" fill="{c['dot']}" fill-opacity="{c['dot_op']}"/>
    </pattern>
  </defs>"""


def banner(theme, mobile=False):
    c = THEMES[theme]
    uid = ("m" if mobile else "d") + theme[0]

    if mobile:
        # 420 wide renders at ~0.70x in a 293px phone column. Every size below is
        # the largest that still fits 360px of usable width at that scale -- 520
        # was roomier to lay out but only reached 0.56x, which put the eyebrow and
        # the technology rows back down at 8.5px.
        # SVG text clips at the viewBox rather than wrapping, and the font stack
        # resolves differently per OS (Segoe UI / -apple-system / Liberation Sans),
        # so every line is kept under ~90% of usable width rather than to the pixel.
        w, h, pad, bar = 420, 270, 26, 7
        fs_eyebrow, fs_name, fs_tagline, fs_tag = 15, 34, 16, 15
        y_eyebrow, y_name, y_rule, y_tagline = 62, 118, 138, 174
        tag_rows = [CONTENT["tags"][:3], CONTENT["tags"][3:]]
        tag_ys = [212, 238]
        rule_w = 88
        glows = [(w - 34, 54, 165), (w - 60, h - 26, 150)]
    else:
        w, h, pad, bar = 1280, 420, 80, 8
        fs_eyebrow, fs_name, fs_tagline, fs_tag = 17, 62, 22, 16
        y_eyebrow, y_name, y_rule, y_tagline = 108, 196, 224, 278
        tag_rows = [CONTENT["tags"]]
        tag_ys = [325]
        rule_w = 104
        glows = [(w - 230, 95, 300), (w - 110, h - 40, 260)]

    parts = [_defs(c, uid, w, h)]
    parts.append(f'  <rect width="{w}" height="{h}" fill="url(#bg{uid})"/>')
    # dot field on the right third only, so it never sits behind the type
    dots_x = int(w * 0.58)
    parts.append(f'  <rect x="{dots_x}" y="0" width="{w - dots_x}" height="{h}" '
                 f'fill="url(#dots{uid})"/>')
    for i, (cx, cy, r) in enumerate(glows):
        parts.append(f'  <circle cx="{cx}" cy="{cy}" r="{r}" '
                     f'fill="url(#g{i + 1}{uid})"/>')
    parts.append(f'  <rect x="0" y="0" width="{bar}" height="{h}" '
                 f'fill="url(#acc{uid})"/>')

    parts.append(
        f'  <text x="{pad}" y="{y_eyebrow}" font-family="{SANS}" '
        f'font-size="{fs_eyebrow}" font-weight="600" letter-spacing="0.19em" '
        f'fill="{c["eyebrow"]}">{CONTENT["eyebrow"]}</text>')
    parts.append(
        f'  <text x="{pad}" y="{y_name}" font-family="{SANS}" '
        f'font-size="{fs_name}" font-weight="700" letter-spacing="-0.015em" '
        f'fill="{c["name"]}">{CONTENT["name"]}</text>')
    parts.append(
        f'  <rect x="{pad}" y="{y_rule}" width="{rule_w}" height="4" rx="2" '
        f'fill="url(#rule{uid})"/>')
    parts.append(
        f'  <text x="{pad}" y="{y_tagline}" font-family="{SANS}" '
        f'font-size="{fs_tagline}" fill="{c["tagline"]}">'
        f'{CONTENT["tagline"]}</text>')

    for row, ty in zip(tag_rows, tag_ys):
        parts.append(
            f'  <text x="{pad}" y="{ty}" font-family="{MONO}" '
            f'font-size="{fs_tag}" fill="{c["tag"]}" letter-spacing="0.02em">'
            f'{"  ·  ".join(row)}</text>')

    label = f'{CONTENT["name"]} — {CONTENT["eyebrow"].title()}'
    body = "\n".join(parts)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{label}">\n'
            f'{body}\n</svg>\n')


def main():
    os.makedirs(OUT, exist_ok=True)
    for theme in ("dark", "light"):
        for mobile in (False, True):
            suffix = f'{"-mobile" if mobile else ""}-{theme}'
            path = os.path.join(OUT, f"banner{suffix}.svg")
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(banner(theme, mobile))
            print("wrote", path)


if __name__ == "__main__":
    main()
