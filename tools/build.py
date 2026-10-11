# -*- coding: utf-8 -*-
"""ちぬのいけす：静的ページ生成。 python3 tools/build.py で index.html と games/*/index.html を書き出す。"""
import html
import json
import os
import sys
from datetime import date
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(__file__))
from games import SITE, GAMES, CAST  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
TODAY = date.today().isoformat()


def head(title, desc, path, ogp, theme_color, depth):
    up = "../" * depth
    url = SITE["url"] + path
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="{theme_color}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{E(SITE['name'])}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE['url']}/assets/ogp/{ogp}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="ja_JP">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{up}favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{up}apple-touch-icon.png">
<link rel="preload" href="{up}assets/fonts/fonts.css" as="style">
<link rel="stylesheet" href="{up}assets/fonts/fonts.css">
<link rel="stylesheet" href="{up}assets/css/site.css">
"""


def share_block(text, url, hashtags):
    x = f"https://x.com/intent/post?text={quote(text)}&url={quote(url)}&hashtags={quote(hashtags)}"
    line = f"https://social-plugins.line.me/lineit/share?url={quote(url)}"
    return f"""<div class="share">
  <p class="share-label">おもろかったら、広めてな</p>
  <div class="share-buttons">
    <a class="btn btn-ghost" href="{x}" target="_blank" rel="noopener">Xでポスト</a>
    <a class="btn btn-ghost" href="{line}" target="_blank" rel="noopener">LINEで送る</a>
    <button class="btn btn-ghost" type="button" data-copy="{url}">リンクをコピー</button>
  </div>
</div>"""


def social_links(up):
    out = []
    labels = {"x": "X", "note": "note", "github": "GitHub"}
    for k, v in SITE["links"].items():
        if v:
            out.append(f'<a href="{E(v)}" target="_blank" rel="noopener">{labels.get(k, k)}</a>')
    return "".join(out)


def footer(up):
    return f"""<footer class="site-footer">
  <div class="wrap footer-inner">
    <a class="footer-mark" href="{up}"><img src="{up}assets/img/chinu-pixel.webp" alt="" width="40" height="40">{E(SITE['name'])}</a>
    <nav class="footer-links" aria-label="外部リンク">{social_links(up)}</nav>
    <p class="fine">掲載しているゲームはすべて個人制作の非公式作品です。作中の名称・人物はフィクションまたはパロディで、実在の個人・団体・作品とは関係ありません。各ゲームは予告なく仕様変更・公開終了する場合があります。</p>
  </div>
</footer>
<script src="{up}assets/js/site.js" defer></script>
</body>
</html>
"""


def tag_hang(games, up):
    items = []
    for i, g in enumerate(games):
        items.append(f"""<li class="tag tag-{i}">
      <a href="#{g['slug']}">
        <span class="tag-hole" aria-hidden="true"></span>
        <span class="tag-name">{E(g['tag_name'])}</span>
        <span class="tag-price">無料</span>
      </a>
    </li>""")
    return "\n    ".join(items)


def catch_row(g, i, up):
    page = f"{up}games/{g['slug']}/"
    side = "flip" if i % 2 else ""
    sub = f'<span class="catch-sub">{E(g["subtitle"])}</span>' if g.get("subtitle") else ""
    return f"""<article class="catch {side}" id="{g['slug']}" data-theme="{g['theme']}">
  <a class="catch-visual" href="{page}" tabindex="-1" aria-hidden="true">
    <img src="{up}assets/img/{g['list_image']}" alt="" loading="lazy" width="1600" height="900">
  </a>
  <div class="catch-body">
    <p class="catch-genre">{E(g['genre'])}</p>
    <h3 class="catch-name"><a href="{page}">{E(g.get('short_name', g['name']))}</a>{sub}</h3>
    <p class="catch-copy">{E(g['catch'])}</p>
    <p class="catch-lead">{E(g['lead'])}</p>
    <dl class="catch-meta">
      <div><dt>人数</dt><dd>{E(g['players'])}</dd></div>
      <div><dt>状態</dt><dd>{E(g['status'])}</dd></div>
      <div><dt>値段</dt><dd class="free">無料</dd></div>
    </dl>
    <div class="catch-actions">
      <a class="btn btn-play" href="{g['play_url']}" target="_blank" rel="noopener">いますぐ遊ぶ</a>
      <a class="btn btn-ghost" href="{page}">くわしく見る</a>
    </div>
  </div>
</article>"""


def build_index():
    up = ""
    games_ld = [{"@type": "VideoGame", "name": g["name"], "url": g["play_url"], "genre": g["genre"],
                 "gamePlatform": "Web browser", "offers": {"@type": "Offer", "price": 0, "priceCurrency": "JPY"},
                 "author": {"@type": "Person", "name": SITE["author"]}} for g in GAMES]
    ld = {"@context": "https://schema.org", "@type": "ItemList",
          "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": x} for i, x in enumerate(games_ld)]}
    cast = "\n".join(f"""<li class="cast-item">
      <img src="assets/img/{c['image']}" alt="{E(c['name'])}" loading="lazy">
      <h3>{E(c['name'])}</h3>
      <p class="cast-line">{E(c['line'])}</p>
      <ul class="cast-in">{''.join(f'<li>{E(x)}</li>' for x in c['in'])}</ul>
    </li>""" for c in CAST)
    rows = "\n".join(catch_row(g, i, up) for i, g in enumerate(GAMES))
    body = f"""<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body class="portal">
<a class="skip" href="#catch">本文へ</a>
<header class="hero">
  <div class="wrap hero-inner">
    <div class="hero-text">
      <p class="brand"><img src="assets/img/chinu-pixel.webp" alt="" width="56" height="56">{E(SITE['name'])}</p>
      <h1 class="hero-title">今日の水揚げ、<br>4本。</h1>
      <p class="hero-sub">ぜんぶブラウザで遊べて、ぜんぶタダ。<br>インストールもいらん。</p>
    </div>
    <div class="hang">
      <div class="rope" aria-hidden="true"></div>
      <ul class="tags" aria-label="ゲーム一覧">
        {tag_hang(GAMES, up)}
      </ul>
    </div>
  </div>
</header>

<main id="catch">
  <section class="section catches" aria-labelledby="catch-h">
    <div class="wrap">
      <h2 id="catch-h" class="section-title">本日の品書き</h2>
      {rows}
    </div>
  </section>

  <section class="section cast" aria-labelledby="cast-h">
    <div class="wrap">
      <h2 id="cast-h" class="section-title">同じ海の、同じ顔ぶれ</h2>
      <p class="section-lead">ジャンルはバラバラでも、出てくる魚はだいたい同じ。あっちで敵だったやつが、こっちでは仲間やったりします。</p>
      <ul class="cast-list">
      {cast}
      </ul>
    </div>
  </section>

  <section class="section maker" aria-labelledby="maker-h">
    <div class="wrap"><div class="maker-inner">
      <h2 id="maker-h" class="section-title">作ってる人</h2>
      <p>ちぬが、AIと組んで夜な夜な作ってます。どれも作りかけで、遊んでもらうたびに直してる最中。感想も不具合も、どこからでも気軽に投げてください。</p>
      <p class="maker-links">{social_links(up)}</p>
    </div></div>
  </section>
</main>
"""
    out = head(f"{SITE['name']}｜ちぬの無料ブラウザゲーム", SITE["description"], "/", "portal.jpg", "#0f2c3f", 0) + body + footer(up)
    write("index.html", out)


def build_game(g):
    up = "../../"
    path = f"/games/{g['slug']}/"
    url = SITE["url"] + path
    others = [o for o in GAMES if o["slug"] != g["slug"]]
    feats = "\n".join(f"""<section class="feature{' flip' if i % 2 else ''}">
      <figure class="feature-shot"><img src="{up}assets/img/{f['image']}" alt="{E(f['alt'])}" loading="lazy"></figure>
      <div class="feature-text">
        <h3>{E(f['title'])}</h3>
        <p>{E(f['text'])}</p>
      </div>
    </section>""" for i, f in enumerate(g["features"]))
    cards = ""
    if g.get("cards"):
        imgs = "".join(f'<li><img src="{up}assets/img/cq2/card-{c}.webp" alt="" loading="lazy"></li>' for c in g["cards"])
        cards = f"""<section class="cardfan" aria-label="カードイラストの一部">
    <ul>{imgs}</ul>
  </section>"""
    steps = "".join(f"<li>{E(s)}</li>" for s in g["steps"])
    spec = "".join(f"<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>" for k, v in g["spec"])
    note = f'<p class="game-note">{E(g["note"])}</p>' if g.get("note") else ""
    logo = f'<img class="hero-logo" src="{up}assets/img/{g["logo"]}" alt="{E(g["name"])}">' if g.get("logo") else ""
    title_cls = " visually-hidden" if g.get("logo") else ""
    sub = f'<span class="game-sub">{E(g["subtitle"])}</span>' if g.get("subtitle") else ""
    other = "".join(f"""<li><a href="{up}games/{o['slug']}/">
      <img src="{up}assets/img/{o['list_image']}" alt="" loading="lazy">
      <span class="other-name">{E(o['name'])}</span>
      <span class="other-genre">{E(o['genre'])}</span></a></li>""" for o in others)
    ld = {"@context": "https://schema.org", "@type": "VideoGame", "name": g["name"], "url": g["play_url"],
          "description": g["lead"], "genre": g["genre"], "gamePlatform": "Web browser", "inLanguage": "ja",
          "image": f"{SITE['url']}/assets/ogp/{g['slug']}.jpg",
          "offers": {"@type": "Offer", "price": 0, "priceCurrency": "JPY"},
          "author": {"@type": "Person", "name": SITE["author"]}}
    theme_colors = {"cq2": "#16245a", "doppel": "#07110d", "cap": "#12324a", "umi": "#081b24"}
    body = f"""<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body class="game theme-{g['theme']}">
<a class="skip" href="#main">本文へ</a>
<nav class="topbar">
  <a class="back" href="{up}"><img src="{up}assets/img/chinu-pixel.webp" alt="" width="32" height="32">{E(SITE['name'])}</a>
  <a class="btn btn-play btn-small" href="{g['play_url']}" target="_blank" rel="noopener">遊ぶ</a>
</nav>
<header class="game-hero">
  <img class="game-hero-bg" src="{up}assets/img/{g['key']}" alt="" fetchpriority="high">
  <div class="game-hero-inner">
    {logo}
    <h1 class="game-title{title_cls}">{E(g.get('short_name', g['name']))}{sub}</h1>
    <p class="game-catch">{E(g['catch'])}</p>
    <a class="btn btn-play btn-big" href="{g['play_url']}" target="_blank" rel="noopener">無料で遊ぶ</a>
    <p class="game-status">{E(g['status'])}　ブラウザでそのまま遊べます</p>
  </div>
</header>
<main id="main">
  <section class="game-lead wrap-narrow"><p>{E(g['lead'])}</p></section>
  {cards}
  <div class="features wrap">
    {feats}
  </div>
  <section class="howto wrap-narrow" aria-labelledby="howto-h">
    <h2 id="howto-h">はじめかた</h2>
    <ol class="steps">{steps}</ol>
    <a class="btn btn-play btn-big" href="{g['play_url']}" target="_blank" rel="noopener">無料で遊ぶ</a>
  </section>
  <section class="spec wrap-narrow" aria-labelledby="spec-h">
    <h2 id="spec-h">遊ぶ前に</h2>
    <dl>{spec}</dl>
    {note}
  </section>
  <section class="wrap-narrow">{share_block(g['share'], url, g['hashtags'])}</section>
  <section class="others wrap" aria-labelledby="others-h">
    <h2 id="others-h">ほかの水揚げ</h2>
    <ul>{other}</ul>
  </section>
</main>
"""
    out = head(f"{g['name']}｜{g['catch']}", g["lead"], path, f"{g['slug']}.jpg", theme_colors[g["theme"]], 2) + body + footer(up)
    write(f"games/{g['slug']}/index.html", out)


def build_meta():
    urls = ["/"] + [f"/games/{g['slug']}/" for g in GAMES]
    sm = "\n".join(f"  <url><loc>{SITE['url']}{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}\n</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n")


def write(rel, text):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("wrote", rel)


if __name__ == "__main__":
    build_index()
    for g in GAMES:
        build_game(g)
    build_meta()
