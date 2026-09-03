#!/usr/bin/env python3
"""Generate real-data stat cards as SVGs.

The public card services (github-profile-summary-cards, github-readme-stats) can only
see public repos, which for this account means they report JavaScript as the top
language off the back of old bootcamp projects. Anything accurate has to come from an
authenticated token, so these cards are rendered here and committed to the repo.

Two metrics are deliberately chosen:
  * language share is measured in BYTES, not repo count — by repo count JavaScript
    still wins purely because the 2023-era repos were numerous and tiny.
  * commit counts include restrictedContributionsCount, i.e. private-repo commits.

Each card is drawn twice per theme. A README image is sized with width="98%", so the
rendered text size is (font-size x container/viewBox): GitHub's markdown column is
~830px on a desktop but ~293px on a 375px phone, and one 920-wide card served to both
puts the labels at 3-4px on the phone. The mobile variants use a 400-wide canvas with
reflowed columns, and README.md picks between them with a `(max-width: 500px)` source.

Needs GH_TOKEN with `repo` scope. Stdlib only, so CI needs no pip install.
Writes Images/card-{languages,numbers,commits}[-mobile]-{dark,light}.svg
"""
import json
import os
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone

USER = os.environ.get("GH_USER", "sabbir-offc")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
OUT = "Images"

if not TOKEN:
    sys.exit("GH_TOKEN is required (needs `repo` scope to read private repositories)")

API = "https://api.github.com"
HDRS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "User-Agent": f"{USER}-profile-cards",
}

# ---------------------------------------------------------------- data fetching


def _req(url, data=None):
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HDRS)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"{e.code} for {url}\n{e.read().decode()[:400]}")


def graphql(query, **variables):
    out = _req(f"{API}/graphql", {"query": query, "variables": variables})
    if "errors" in out:
        sys.exit(json.dumps(out["errors"])[:600])
    return out["data"]


REPO_Q = """
query($login:String!, $cursor:String) {
  user(login:$login) {
    repositories(first:100, after:$cursor, ownerAffiliations:OWNER,
                 isFork:false, orderBy:{field:PUSHED_AT, direction:DESC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        name isPrivate stargazerCount
        languages(first:20, orderBy:{field:SIZE, direction:DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}
"""

CONTRIB_Q = """
query($login:String!, $from:DateTime!, $to:DateTime!) {
  user(login:$login) {
    contributionsCollection(from:$from, to:$to) {
      totalCommitContributions
      restrictedContributionsCount
    }
  }
}
"""


def collect():
    lang_bytes, lang_color = defaultdict(int), {}
    repos = private = stars = 0
    cursor = None
    while True:
        page = graphql(REPO_Q, login=USER, cursor=cursor)["user"]["repositories"]
        for r in page["nodes"]:
            repos += 1
            private += r["isPrivate"]
            stars += r["stargazerCount"]
            for e in r["languages"]["edges"]:
                name = e["node"]["name"]
                lang_bytes[name] += e["size"]
                lang_color.setdefault(name, e["node"]["color"] or "#8B949E")
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]

    joined = 2021
    now = datetime.now(timezone.utc)
    years = []
    for y in range(joined, now.year + 1):
        c = graphql(CONTRIB_Q, login=USER,
                    **{"from": f"{y}-01-01T00:00:00Z", "to": f"{y}-12-31T23:59:59Z"}
                    )["user"]["contributionsCollection"]
        pub, priv = c["totalCommitContributions"], c["restrictedContributionsCount"]
        if pub or priv:
            years.append({"year": y, "public": pub, "private": priv})

    return {
        "lang_bytes": dict(lang_bytes),
        "lang_color": lang_color,
        "repos": repos,
        "private_repos": private,
        "stars": stars,
        "years": years,
        "generated": now.strftime("%Y-%m-%d"),
    }


# --------------------------------------------------------------------- theming

THEMES = {
    "dark": dict(bg="#0D1117", border="#30363D", title="#58A6FF", text="#E6EDF3",
                 muted="#8B949E", dim="#6E7681", track="#21262D", accent="#BF91F3"),
    "light": dict(bg="#FFFFFF", border="#D0D7DE", title="#0969DA", text="#1F2328",
                  muted="#57606A", dim="#6E7781", track="#EAEEF2", accent="#8250DF"),
}
FONT = ("-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,"
        "'Liberation Sans',sans-serif")


def _lum(hex_color):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def readable(hex_color, theme):
    """Lift near-black language colours so they stay visible on the dark canvas."""
    h = hex_color.lstrip("#")
    if len(h) != 6:
        return "#8B949E"
    if theme == "dark" and _lum(f"#{h}") < 0.16:
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        r, g, b = (min(255, int(c + (255 - c) * 0.42)) for c in (r, g, b))
        return f"#{r:02x}{g:02x}{b:02x}"
    if theme == "light" and _lum(f"#{h}") > 0.86:
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        r, g, b = (int(c * 0.72) for c in (r, g, b))
        return f"#{r:02x}{g:02x}{b:02x}"
    return f"#{h}"


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# Type scales. A README image is laid out with width="98%", so the rendered text size
# is (font-size x container/viewBox) — the viewBox width sets the scale, not the font.
# GitHub's markdown column is ~830px on a desktop but only ~293px on a 375px phone, so
# one 920-wide card cannot serve both: at 0.32x the desktop labels land at 3-4px. The
# mobile variants below are drawn on a 400-wide canvas instead, which renders at ~0.73x
# and puts the same labels back above 10px.
SCALES = {
    "desktop": dict(pad=22, t=15, s=10.5, ll=11.5, m=11, n=27, k=10,
                    title_y=30, sub_y=48),
    "mobile": dict(pad=18, t=19, s=13, ll=15, m=14, n=30, k=13,
                   title_y=28, sub_y=50),
}


def frame(w, h, t, body, title, subtitle, scale="desktop"):
    c = THEMES[t]
    z = SCALES[scale]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" \
viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
  <style>
    text {{ font-family: {FONT}; }}
    .t {{ font-size: {z['t']}px; font-weight: 600; fill: {c['title']}; }}
    .s {{ font-size: {z['s']}px; fill: {c['dim']}; }}
    .l {{ font-size: {z['ll']}px; fill: {c['text']}; }}
    .m {{ font-size: {z['m']}px; fill: {c['muted']}; }}
    .n {{ font-size: {z['n']}px; font-weight: 700; fill: {c['text']}; }}
    .k {{ font-size: {z['k']}px; fill: {c['dim']}; letter-spacing: .04em; }}
  </style>
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="6"
        fill="{c['bg']}" stroke="{c['border']}"/>
  <text class="t" x="{z['pad']}" y="{z['title_y']}">{esc(title)}</text>
  <text class="s" x="{z['pad']}" y="{z['sub_y']}">{esc(subtitle)}</text>
{body}
</svg>
"""


# ----------------------------------------------------------------- card bodies

# All cards are the same full width. GitHub wraps <picture> in a <themed-picture>
# custom element, so two cards at width="49%" stack instead of sitting side by side —
# laying the columns out inside the SVG is the only way to control this reliably.
W_CARD = 920
W_MOBILE = 400


def card_languages(d, t, scale="desktop"):
    c = THEMES[t]
    mob = scale == "mobile"
    z = SCALES[scale]
    W = W_MOBILE if mob else W_CARD
    pad = z["pad"]
    # One column on a phone: three columns of 130px cannot hold "JavaScript  10.5%".
    cols = 1 if mob else 3
    bar_y, bar_h = (72, 13) if mob else (66, 11)
    ry, step, dot = (114, 27, 6) if mob else (102, 23, 5)

    total = sum(d["lang_bytes"].values()) or 1
    ranked = sorted(d["lang_bytes"].items(), key=lambda kv: -kv[1])

    bx, bw = pad, W - pad * 2
    segs, x = [], float(bx)
    for name, n in ranked:
        seg = bw * n / total
        segs.append(f'<rect x="{x:.2f}" y="{bar_y}" width="{max(seg, 0.6):.2f}" '
                    f'height="{bar_h}" fill="{readable(d["lang_color"][name], t)}"/>')
        x += seg
    if x < bx + bw - 0.5:
        segs.append(f'<rect x="{x:.2f}" y="{bar_y}" width="{bx + bw - x:.2f}" '
                    f'height="{bar_h}" fill="{c["track"]}"/>')

    # The bar always shows every language. The list does too on desktop, but a phone
    # column spends a whole 27px row on "Swift 0.00%" — below 0.1% they become a count.
    listed = [kv for kv in ranked if kv[1] / total * 100 >= 0.1] if mob else ranked
    hidden = len(ranked) - len(listed)

    rows, col_w = [], (W - pad * 2) / cols
    for i, (name, n) in enumerate(listed):
        cx = pad + (i % cols) * col_w
        cy = ry + (i // cols) * step
        pct = n / total * 100
        pct_s = f"{pct:.2f}%" if pct < 1 else f"{pct:.1f}%"
        rows.append(
            f'<circle cx="{cx + dot:.0f}" cy="{cy - 4:.0f}" r="{dot}" '
            f'fill="{readable(d["lang_color"][name], t)}"/>'
            f'<text class="l" x="{cx + dot * 2 + 8:.0f}" y="{cy}">{esc(name)}</text>'
            f'<text class="m" x="{cx + col_w - (2 if mob else 26):.0f}" y="{cy}" '
            f'text-anchor="end">{pct_s}</text>'
        )

    H = ry + ((len(listed) + cols - 1) // cols) * step + (10 if mob else 12)
    if hidden:
        rows.append(f'<text class="k" x="{pad}" y="{H + 4}">'
                    f'+{hidden} MORE UNDER 0.1%</text>')
        H += 20
    body = "\n".join(f"  {s}" for s in segs + rows)
    sub = (f"{total / 1e6:,.1f} MB across {d['repos']} repos · by bytes" if mob else
           f"{total / 1e6:,.1f} MB of code across all {d['repos']} repositories "
           f"· measured in bytes, not repository count")
    return W, H, frame(W, H, t, body, "Languages", sub, scale)


def card_numbers(d, t, scale="desktop"):
    mob = scale == "mobile"
    z = SCALES[scale]
    pad = z["pad"]
    total_b = sum(d["lang_bytes"].values()) or 1
    top_lang, top_b = max(d["lang_bytes"].items(), key=lambda kv: kv[1])
    commits = sum(y["public"] + y["private"] for y in d["years"])
    priv = sum(y["private"] for y in d["years"])

    stats = [
        (f"{commits:,}", "COMMITS, ALL TIME"),
        (f"{priv / commits * 100:.0f}%", "OF THEM PRIVATE"),
        (f"{d['repos']}", "REPOSITORIES"),
        (f"{d['private_repos']}", "PRIVATE REPOS"),
        (f"{top_b / total_b * 100:.0f}%", top_lang.upper()),
    ]

    out = []
    if mob:
        # Five figures across a 400px canvas would leave 73px per column; 2x3 instead.
        W, cols, row_h, y0 = W_MOBILE, 2, 60, 104
        col_w = (W - pad * 2) / cols
        for i, (num, label) in enumerate(stats):
            x = pad + (i % cols) * col_w
            y = y0 + (i // cols) * row_h
            out.append(f'<text class="n" x="{x:.0f}" y="{y}">{esc(num)}</text>'
                       f'<text class="k" x="{x:.0f}" y="{y + 20}">{esc(label)}</text>')
        H = y0 + ((len(stats) + cols - 1) // cols - 1) * row_h + 38
    else:
        W, H = W_CARD, 158
        col_w = (W - pad * 2) / len(stats)
        for i, (num, label) in enumerate(stats):
            x = pad + i * col_w
            out.append(f'<text class="n" x="{x:.0f}" y="112">{esc(num)}</text>'
                       f'<text class="k" x="{x:.0f}" y="131">{esc(label)}</text>')

    body = "\n".join(f"  {s}" for s in out)
    sub = (f"public and private · {d['generated']}" if mob else
           f"every repository, public and private · as of {d['generated']}")
    return W, H, frame(W, H, t, body, "By the numbers", sub, scale)


def card_commits(d, t, scale="desktop"):
    c = THEMES[t]
    mob = scale == "mobile"
    # Mobile is taller than the bars need: the legend must clear the year labels by
    # more than a line, or "2023" and "private" stack into one reading.
    W, H = (W_MOBILE, 266) if mob else (W_CARD, 216)
    ys = d["years"]
    peak = max((y["public"] + y["private"]) for y in ys) or 1

    top, floor = (92, 196) if mob else (78, 168)
    span = floor - top
    left, right = (30, W - 30) if mob else (40, W - 40)
    slot = (right - left) / len(ys)
    bw = min(46 if mob else 96, slot * 0.5)

    out = [f'<line x1="{left}" y1="{floor}.5" x2="{right}" y2="{floor}.5" '
           f'stroke="{c["border"]}"/>']
    for i, y in enumerate(ys):
        tot = y["public"] + y["private"]
        cx = left + slot * i + slot / 2
        bx = cx - bw / 2
        h = span * tot / peak
        hp = h * y["private"] / tot if tot else 0
        # private below, public stacked above — private is the bulk of the work
        out.append(f'<rect x="{bx:.1f}" y="{floor - hp:.1f}" width="{bw:.1f}" '
                   f'height="{hp:.1f}" fill="{c["title"]}"/>')
        out.append(f'<rect x="{bx:.1f}" y="{floor - h:.1f}" width="{bw:.1f}" '
                   f'height="{max(h - hp, 0):.1f}" fill="{c["accent"]}"/>')
        out.append(f'<text class="l" x="{cx:.1f}" y="{floor - h - 9:.1f}" '
                   f'text-anchor="middle">{tot:,}</text>')
        out.append(f'<text class="k" x="{cx:.1f}" y="{floor + (22 if mob else 18)}" '
                   f'text-anchor="middle">{y["year"]}</text>')

    ly = H - (16 if mob else 14)
    sw, gap = (11, 96) if mob else (9, 74)
    out.append(f'<rect x="{left}" y="{ly - sw + 1}" width="{sw}" height="{sw}" '
               f'fill="{c["title"]}"/>'
               f'<text class="m" x="{left + sw + 6}" y="{ly}">private</text>'
               f'<rect x="{left + gap}" y="{ly - sw + 1}" width="{sw}" height="{sw}" '
               f'fill="{c["accent"]}"/>'
               f'<text class="m" x="{left + gap + sw + 6}" y="{ly}">public</text>')

    body = "\n".join(f"  {s}" for s in out)
    sub = (f"public + private · {ys[-1]['year']} to date" if mob else
           f"public + private · {ys[-1]['year']} is year-to-date")
    return W, H, frame(W, H, t, body, "Commits per year", sub, scale)


# ------------------------------------------------------------------------ main

def main():
    d = collect()
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (("languages", card_languages), ("numbers", card_numbers),
                     ("commits", card_commits)):
        for theme in ("dark", "light"):
            for scale in ("desktop", "mobile"):
                _, _, svg = fn(d, theme, scale)
                suffix = f"-{theme}" if scale == "desktop" else f"-mobile-{theme}"
                path = os.path.join(OUT, f"card-{name}{suffix}.svg")
                with open(path, "w", encoding="utf-8", newline="\n") as f:
                    f.write(svg)
                print("wrote", path)

    total = sum(d["lang_bytes"].values())
    top = sorted(d["lang_bytes"].items(), key=lambda kv: -kv[1])[:4]
    commits = sum(y["public"] + y["private"] for y in d["years"])
    print(f"\n{d['repos']} repos ({d['private_repos']} private) · {commits:,} commits")
    print("  " + " · ".join(f"{k} {v / total * 100:.1f}%" for k, v in top))


if __name__ == "__main__":
    main()
