# docs-next (PoC)

Sphinx + Furo + rosdoc2 ベースの新ドキュメント基盤の PoC です。
既存の [`triorb-amr-docs/`](../triorb-amr-docs/) (MkDocs + mike) とは独立して構築されています。

## ローカルビルド

```bash
# 初回のみ
python3 -m venv ../.venv-docs2
source ../.venv-docs2/bin/activate
pip install -r requirements.txt

# 日本語ビルド
make html              # _build/html/ja/ に出力
make serve             # http://localhost:8000 でプレビュー

# 英語ビルド (翻訳追加後)
make html-en           # _build/html/en/

# 翻訳ワークフロー
make gettext           # POT を _build/gettext/ に抽出
make update-po         # locale/en/LC_MESSAGES/*.po を生成・更新
# .po を編集後、再度 make html-en
```

## ディレクトリ

| パス | 用途 |
|---|---|
| `conf.py` | Sphinx 設定 |
| `index.md` | ルートページ (MyST Markdown) |
| `guides/` | 手書きガイド (overview, history, terms, privacy, …) |
| `packages/` | rosdoc2 生成物の取り込み先 (Phase 1 後半で整備) |
| `_templates/sidebar/language-switcher.html` | Furo サイドバー内の言語切替 UI |
| `_static/` | 画像・CSS |
| `locale/en/LC_MESSAGES/*.po` | 英訳 |
| `_build/` | ビルド出力 (git 管理外) |

## デプロイ戦略

- 新サイト (v1.2.5+) は `gh-pages` の `/v1.2.5/{ja,en}/...` 以下に配置
- 既存 mike サイト (v1.2.2, v1.2.3, v1.2.4) はそのままアーカイブとして残置
- ルート `/` に版・言語ピッカーの簡易ランディングを設置 (Phase 4)
