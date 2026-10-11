# ちぬのいけす

ちぬの無料ブラウザゲームをまとめたプロモーションサイト。GitHub Pages（`https://saint-chinu.github.io/`）で公開。

| ページ | 場所 |
|---|---|
| トップ | `index.html` |
| チヌクエスト2 | `games/chinu-quest2/` |
| ドッペル鬼ごっこ | `games/doppel-tag/` |
| 資本主義の権化 | `games/capitalism/` |
| 海の回廊 | `games/umi-no-kairo/` |

ゲーム本体は各リポジトリ／Cloudflare Workers にあり、このサイトはリンクするだけ。`/chinu-quest2/` は別リポジトリ（chinu-quest2）の Pages なので、このリポジトリに同名フォルダを作らないこと。

## 更新のしかた

1. 文言・URL・SNSリンクは `tools/games.py` を書き換える（X・noteのURLは `SITE["links"]` に入れると自動で表示される）
2. `python3 tools/build.py` で全ページを作り直す
3. 画像は `assets/img/`（webp）、SNS共有用画像は `assets/ogp/`（1200×630）
4. コミットしてpushすると1〜2分で反映

フォント：Dela Gothic One / Zen Kaku Gothic New（SIL Open Font License 1.1、@fontsource から同梱）。
