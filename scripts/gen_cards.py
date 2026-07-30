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

Needs GH_TOKEN with `repo` scope. Stdlib only, so CI needs no pip install.
Writes Images/card-{languages,numbers,commits}-{dark,light}.svg
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


def frame(w, h, t, body, title, subtitle):
    c = THEMES[t]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" \
viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
  <style>
    text {{ font-family: {FONT}; }}
    .t {{ font-size: 15px; font-weight: 600; fill: {c['title']}; }}
    .s {{ font-size: 10.5px; fill: {c['dim']}; }}
    .l {{ font-size: 11.5px; fill: {c['text']}; }}
    .m {{ font-size: 11px; fill: {c['muted']}; }}
    .n {{ font-size: 27px; font-weight: 700; fill: {c['text']}; }}
    .k {{ font-size: 10px; fill: {c['dim']}; letter-spacing: .04em; }}
  </style>
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="6"
        fill="{c['bg']}" stroke="{c['border']}"/>
  <text class="t" x="22" y="30">{esc(title)}</text>
  <text class="s" x="22" y="48">{esc(subtitle)}</text>
{body}
</svg>
"""


# ----------------------------------------------------------------- card bodies

# All cards are the same full width. GitHub wraps <picture> in a <themed-picture>
# custom element, so two cards at width="49%" stack instead of sitting side by side —
# laying the columns out inside the SVG is the only way to control this reliably.
W_CARD = 920


def card_languages(d, t, cols=3):
    c = THEMES[t]
    W = W_CARD
    total = sum(d["lang_bytes"].values()) or 1
    ranked = sorted(d["lang_bytes"].items(), key=lambda kv: -kv[1])

    bx, bw, by, bh = 22, W - 44, 66, 11
    segs, x = [], float(bx)
    for name, n in ranked:
        seg = bw * n / total
        segs.append(f'<rect x="{x:.2f}" y="{by}" width="{max(seg, 0.6):.2f}" '
                    f'height="{bh}" fill="{readable(d["lang_color"][name], t)}"/>')
        x += seg
    if x < bx + bw - 0.5:
        segs.append(f'<rect x="{x:.2f}" y="{by}" width="{bx + bw - x:.2f}" '
                    f'height="{bh}" fill="{c["track"]}"/>')

    rows, ry, col_w = [], 102, (W - 44) / cols
    for i, (name, n) in enumerate(ranked):
        cx = 22 + (i % cols) * col_w
        cy = ry + (i // cols) * 23
        pct = n / total * 100
        pct_s = f"{pct:.2f}%" if pct < 1 else f"{pct:.1f}%"
        rows.append(
            f'<circle cx="{cx + 5:.0f}" cy="{cy - 4:.0f}" r="5" '
            f'fill="{readable(d["lang_color"][name], t)}"/>'
            f'<text class="l" x="{cx + 17:.0f}" y="{cy}">{esc(name)}</text>'
            f'<text class="m" x="{cx + col_w - 26:.0f}" y="{cy}" '
            f'text-anchor="end">{pct_s}</text>'
        )

    H = ry + ((len(ranked) + cols - 1) // cols) * 23 + 12
    body = "\n".join(f"  {s}" for s in segs + rows)
    return W, H, frame(
        W, H, t, body, "Languages",
        f"{total / 1e6:,.1f} MB of code across all {d['repos']} repositories "
        f"· measured in bytes, not repository count",
    )


def card_numbers(d, t):
    W, H = W_CARD, 158
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
    out, col_w = [], (W - 44) / len(stats)
    for i, (num, label) in enumerate(stats):
        x = 22 + i * col_w
        out.append(f'<text class="n" x="{x:.0f}" y="112">{esc(num)}</text>'
                   f'<text class="k" x="{x:.0f}" y="131">{esc(label)}</text>')
    body = "\n".join(f"  {s}" for s in out)
    return W, H, frame(W, H, t, body, "By the numbers",
                       f"every repository, public and private · as of {d['generated']}")


def card_commits(d, t):
    c = THEMES[t]
    W, H = W_CARD, 216
    ys = d["years"]
    peak = max((y["public"] + y["private"]) for y in ys) or 1

    top, floor = 78, 168
    span = floor - top
    left, right = 40, W - 40
    slot = (right - left) / len(ys)
    bw = min(96, slot * 0.5)

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
        out.append(f'<text class="k" x="{cx:.1f}" y="{floor + 18}" '
                   f'text-anchor="middle">{y["year"]}</text>')

    ly = H - 14
    out.append(f'<rect x="{left}" y="{ly - 8}" width="9" height="9" '
               f'fill="{c["title"]}"/>'
               f'<text class="m" x="{left + 15}" y="{ly}">private</text>'
               f'<rect x="{left + 74}" y="{ly - 8}" width="9" height="9" '
               f'fill="{c["accent"]}"/>'
               f'<text class="m" x="{left + 89}" y="{ly}">public</text>')

    body = "\n".join(f"  {s}" for s in out)
    return W, H, frame(
        W, H, t, body, "Commits per year",
        f"public + private · {ys[-1]['year']} is year-to-date",
    )


# ------------------------------------------------------------------------ main

def main():
    d = collect()
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (("languages", card_languages), ("numbers", card_numbers),
                     ("commits", card_commits)):
        for theme in ("dark", "light"):
            _, _, svg = fn(d, theme)
            path = os.path.join(OUT, f"card-{name}-{theme}.svg")
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
