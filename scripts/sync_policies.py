#!/usr/bin/env python3
"""Mirror Skywolf Game Studios policy pages from itch.io into native, styled
pages on the GitHub Pages site.

Run by the Pages deploy workflow (on every deploy and on a daily schedule), so
the on-site pages stay in sync with whatever is edited on itch.io — itch remains
the single source of truth.

Resilient by design: if a page can't be fetched/parsed, the existing local file
is left untouched and the script still exits 0 so the deploy is never blocked.
"""
import sys
import urllib.request
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("beautifulsoup4 not installed; skipping policy sync.", file=sys.stderr)
    sys.exit(0)

ROOT = Path(__file__).resolve().parent.parent

# (output file, page title, itch source url)
PAGES = [
    ("privacy.html",    "Privacy Policy",                       "https://skywolfgamestudios.itch.io/sgsprivacypolicy"),
    ("datasafety.html", "Data Safety Policy",                   "https://skywolfgamestudios.itch.io/sgsdatasafetypolicy"),
    ("tos.html",        "Terms of Service",                     "https://skywolfgamestudios.itch.io/sgstos"),
    ("license.html",    "Royalty-Free Asset License Agreement", "https://skywolfgamestudios.itch.io/sgsofficialroyaltyfreeassetlicenseagreement"),
]

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%%TITLE%% &mdash; Skywolf Game Studios</title>
<meta name="description" content="%%TITLE%% for Skywolf Game Studios.">
<link rel="icon" type="image/png" href="assets/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Montserrat:ital,wght@0,800;1,800&display=swap" rel="stylesheet">
<style>
  :root{--bg:#05070b;--surface:#111823;--border:#1f2b3a;--cyan:#1cb0f6;--cyan-bright:#3ec6ff;
    --orange:#ff9f1c;--text:#eaf1f8;--muted:#93a3b5;--maxw:820px}
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--bg);color:var(--text);font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
    line-height:1.6;-webkit-font-smoothing:antialiased;min-height:100vh;display:flex;flex-direction:column}
  a{color:inherit;text-decoration:none}
  .wrap{max-width:var(--maxw);margin:0 auto;padding:0 24px;width:100%}
  header.nav{border-bottom:1px solid var(--border);background:rgba(5,7,11,.9)}
  .nav-inner{display:flex;align-items:center;justify-content:space-between;height:68px}
  .nav-brand{display:flex;align-items:center;gap:12px;font-family:'Montserrat';font-weight:800;
    font-style:italic;text-transform:uppercase;letter-spacing:1px;font-size:1.1rem}
  .nav-brand img{width:38px;height:38px;border-radius:50%}
  .nav-brand b{color:var(--cyan)}
  .nav-back{color:var(--muted);font-weight:500;font-size:.95rem;transition:color .2s}
  .nav-back:hover{color:var(--cyan-bright)}
  main{flex:1;padding:56px 0 72px}
  .kicker{color:var(--cyan);font-weight:600;font-size:.82rem;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px}
  h1.page-title{font-family:'Montserrat';font-weight:800;font-style:italic;text-transform:uppercase;
    font-size:clamp(1.7rem,4.5vw,2.6rem);letter-spacing:.5px;margin-bottom:24px}
  .policy-body{color:#c9d5e2;font-size:1rem;line-height:1.75}
  .policy-body h1,.policy-body h2,.policy-body h3,.policy-body h4{font-family:'Inter';color:var(--text);
    font-weight:700;margin:28px 0 10px;line-height:1.3}
  .policy-body h1{font-size:1.5rem}
  .policy-body h2{font-size:1.3rem}
  .policy-body h3{font-size:1.12rem}
  .policy-body p{margin:0 0 14px}
  .policy-body ul,.policy-body ol{margin:0 0 14px 22px}
  .policy-body li{margin:0 0 6px}
  .policy-body a{color:var(--cyan-bright);font-weight:600}
  .policy-body a:hover{text-decoration:underline}
  .policy-body strong,.policy-body b{color:var(--text)}
  .policy-body hr{border:0;border-top:1px solid var(--border);margin:24px 0}
  .policy-body img{max-width:100%;height:auto;border-radius:8px}
  .policy-body table{border-collapse:collapse;margin:0 0 16px;width:100%}
  .policy-body td,.policy-body th{border:1px solid var(--border);padding:8px 10px;text-align:left}
  .src{margin-top:34px;color:var(--muted);font-size:.88rem;border-top:1px solid var(--border);padding-top:20px}
  .src a{color:var(--cyan-bright);font-weight:600}
  .backhome{display:inline-flex;align-items:center;gap:8px;margin-top:26px;font-weight:600;color:var(--cyan-bright)}
  .backhome:hover{text-decoration:underline}
  footer{border-top:1px solid var(--border);padding:32px 0;color:var(--muted);font-size:.9rem}
  .foot-inner{display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap}
  .foot-brand{display:flex;align-items:center;gap:10px;font-family:'Montserrat';font-weight:800;
    font-style:italic;text-transform:uppercase;color:var(--text)}
  .foot-brand img{width:28px;height:28px;border-radius:50%}
</style>
</head>
<body>
<header class="nav">
  <div class="wrap nav-inner">
    <a href="index.html" class="nav-brand">
      <img src="assets/logo.png" alt="Skywolf Game Studios logo">
      <span>Sky<b>wolf</b></span>
    </a>
    <a href="legal.html" class="nav-back">&larr; All policies</a>
  </div>
</header>
<main>
  <div class="wrap">
    <div class="kicker">Skywolf Game Studios</div>
    <h1 class="page-title">%%TITLE%%</h1>
    <div class="policy-body">
<!--CONTENT_START-->
%%CONTENT%%
<!--CONTENT_END-->
    </div>
    <p class="src">This page mirrors our official document on itch.io &mdash; <a href="%%SOURCE%%" target="_blank" rel="noopener">view the source</a>. It updates automatically when the itch.io version changes.</p>
    <a class="backhome" href="legal.html">&larr; All Legal &amp; Policies</a>
  </div>
</main>
<footer>
  <div class="wrap foot-inner">
    <div class="foot-brand">
      <img src="assets/logo.png" alt="">
      <span>Skywolf Game Studios</span>
    </div>
    <div>&copy; <span id="year"></span> Skywolf Game Studios &middot; Palm Bay, FL</div>
  </div>
</footer>
<script>document.getElementById('year').textContent=new Date().getFullYear();</script>
</body>
</html>
"""


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (SkywolfPolicySync)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def extract(html):
    soup = BeautifulSoup(html, "html.parser")
    div = soup.select_one("div.formatted_description")
    if div is None:
        return None
    # Make any relative links/images absolute so they still work off-site.
    for a in div.find_all("a", href=True):
        if a["href"].startswith("/"):
            a["href"] = "https://itch.io" + a["href"]
    for img in div.find_all("img", src=True):
        if img["src"].startswith("//"):
            img["src"] = "https:" + img["src"]
        elif img["src"].startswith("/"):
            img["src"] = "https://itch.io" + img["src"]
    return div.decode_contents().strip()


def main():
    ok, failed = 0, 0
    for fname, title, url in PAGES:
        try:
            content = extract(fetch(url))
            if not content:
                raise ValueError("no .formatted_description content found")
        except Exception as e:  # noqa: BLE001 - never block the deploy
            print(f"WARN: {fname}: {e} (keeping existing file)", file=sys.stderr)
            failed += 1
            continue
        page = (TEMPLATE
                .replace("%%TITLE%%", title)
                .replace("%%SOURCE%%", url)
                .replace("%%CONTENT%%", content))
        (ROOT / fname).write_text(page, encoding="utf-8")
        print(f"OK: {fname} <- {url} ({len(content)} chars)")
        ok += 1
    print(f"Done. {ok} synced, {failed} failed.")


if __name__ == "__main__":
    main()
