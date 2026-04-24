# TriOrb-AMR-Documents

TriOrb BASE 開発ガイドのソースリポジトリです。公開サイト: `gh-pages` ブランチ / `https://<pages-domain>/`

## ドキュメントパイプライン

現行は **`docs-next/` 配下の Sphinx + rosdoc2 + Furo** 構成です（`docs2/phase2` ブランチで進行中、Phase 4 で `v1.2.4/` を cutover 予定）。

| | パス | ビルドコマンド | 出力 |
| --- | --- | --- | --- |
| 手書き | `docs-next/index.md`, `docs-next/guides/*`, `docs-next/packages/index.md`, `docs-next/_handwritten/packages/visual_slam.md` | `make html` / `make html-ja` | `docs-next/_build/html/{en,ja}/` |
| API | `submodules/TriOrb-AMR-Package/**`（rosdoc2 → exhale + breathe） | `make rosdoc2`（Docker、約 30 分） | `docs-next/packages/<pkg>/**` |
| ランディング | `docs-next/_landing/index.html`（日英併記） | `make deploy-stage` | `docs-next/_build/deploy/index.html` |

レガシー MkDocs + mike パイプライン（`triorb-amr-docs/`）は `master` ブランチで保守のみ、Phase 4 以降は `/v1.2.2/`, `/v1.2.3/` を静的アーカイブとして残し、新デプロイでは上書きしません。

## 初回セットアップ

```bash
git clone git@github.com:TriOrb-Inc/TriOrb-AMR-Documents.git
cd TriOrb-AMR-Documents
git submodule update --init --recursive

python3 -m venv .venv-docs2
source .venv-docs2/bin/activate
pip install -r docs-next/requirements.txt
```

## よく使うコマンド

```bash
source .venv-docs2/bin/activate
cd docs-next

# ビルド
make html                # 英語（_build/html/en/）
make html-ja             # 日本語（_build/html/ja/）
SPHINXOPTS="-j 4" make html   # 並列化（-j auto は多数コアでクラッシュ実績あり、4 推奨）

# 翻訳ワークフロー（D1 — 手書き 7 ページのみ対象）
make gettext             # POT を _build/gettext/ に抽出（packages/ は自動除外）
make update-po           # POT から locale/ja/LC_MESSAGES/*.po を更新 + .mo 生成
python3 _scripts/fill_translations.py  # 辞書と legacy JP 原稿からの自動充填

# ローカルプレビュー
make serve               # 英語だけ、:8000
cd _build/html/ja && python3 -m http.server 18101 &  # 日本語、:18101
make deploy-stage-local  # landing + v1.2.4/{en,ja}/ + 過去版を _build/deploy/ に集約
make serve-deploy        # 上記を :18000 で配信（言語切替が正しく動く）

# API パッケージドキュメント（初回または rosdoc2 ソースが変わった時のみ）
make rosdoc2-image       # Docker イメージを一度だけビルド
make rosdoc2             # 全パッケージの API ドキュメントを rosdoc2 で生成

# GitHub Pages デプロイ（Fork テスト / 本番）
_scripts/deploy_ghpages.sh             # fork へ force-with-lease push（既定、確認プロンプト付き）
_scripts/deploy_ghpages.sh --skip-stage --yes          # 再ビルドせず再 push
_scripts/deploy_ghpages.sh --no-force origin           # 本番（fast-forward のみ）
# 詳細は docs-next/README.md 参照

# クリーンアップ
make clean               # _build/ を削除
```

## リポジトリ構成

```
.
├── CLAUDE.md                 # AI エージェント向け運用ガイド
├── README.md                 # 本ファイル
├── docs-next/                # 現行パイプライン（Sphinx + rosdoc2 + Furo）
│   ├── HANDOFF.md            # 作業引き継ぎドキュメント
│   ├── README.md             # docs-next 個別の README
│   ├── CI.md                 # CI 設計メモ
│   ├── conf.py               # Sphinx 設定
│   ├── Makefile
│   ├── index.md / guides/    # 手書き MyST
│   ├── packages/             # rosdoc2 生成物（gitignored、`make rosdoc2` で再生成）
│   ├── _handwritten/packages/ # 手書き package 補足（visual_slam 等、ビルド対象は packages/ 配下へコピー）
│   ├── _landing/             # ランディングページ HTML + 画像
│   ├── _static/              # Sphinx 静的資産（favicon, concept webp 等）
│   ├── _scripts/fill_translations.py  # D1 翻訳自動充填
│   ├── _templates/sidebar/language-switcher.html
│   ├── docker/               # rosdoc2 実行用 Docker イメージ
│   └── locale/ja/LC_MESSAGES/ # JA 翻訳 PO（D1 の 7 ドキュメントのみ。packages/** は gitignored）
├── submodules/
│   ├── TriOrb-AMR-Package/   # API ソース（rosdoc2 入力）
│   └── triorb-core/
├── triorb-amr-docs/          # レガシー MkDocs+mike（master 保守用、Phase 4 以降アーカイブ）
└── .github/workflows/
    ├── docs2.yml             # Sphinx ビルド + artifact（gh-pages デプロイは Phase 4 承認後）
    └── jekyll-gh-pages2.yml  # レガシー互換の stub（disabled）
```

## 運用上の注意

- **ブランチ使い分け**: `docs-next/` の変更は `docs2/phase2` ブランチへ。`triorb-amr-docs/` や `submodules/` のバージョン更新は `master` ブランチへ（ミックスしない）。詳細は `CLAUDE.md` と `docs-next/HANDOFF.md`。
- **翻訳範囲**: rosdoc2 生成の API ページは **英語固定**（Phase 4 "B 案"）。日本語翻訳は手書き 7 ページ（index, guides/*, packages/index, packages/visual_slam）のみ。背景は `docs-next/HANDOFF.md` を参照。
- **submodule の取り扱い**: `submodules/TriOrb-AMR-Package` と `submodules/triorb-core` は v1.2.x 系のリリース作業（`master`）でのみ bump。`docs2/*` ブランチでは触らない。

## 詳細ドキュメント

- `CLAUDE.md` — AI エージェント向け（パイプライン分離、よく踏む落とし穴）
- `docs-next/HANDOFF.md` — 最新の作業状態と再開手順
- `docs-next/CI.md` — CI 設計と GitHub Actions の設計意図
- `docs-next/PACKAGE_VISIBILITY_RULES.md` — 公開/非公開/名称変更ルールの集約
