# docs-next (Sphinx + rosdoc2 + Furo)

TriOrb BASE 開発者ガイドの現行ビルド基盤です。`master` に残るレガシー MkDocs+mike
パイプライン (`triorb-amr-docs/`) とは**独立**しており、同時に触らない運用です
（ブランチ分離ルールは `../CLAUDE.md` と `HANDOFF.md` を参照）。

## 初回セットアップ

```bash
cd ..  # repo root
python3 -m venv .venv-docs2
source .venv-docs2/bin/activate
pip install -r docs-next/requirements.txt
```

## ビルド・プレビュー

```bash
source ../.venv-docs2/bin/activate
cd docs-next

# EN / JA 個別ビルド（SPHINXOPTS は空か -j 4 を推奨。-j auto は本リポ規模でクラッシュ実績あり）
make html                       # 英語 → _build/html/en/
make html-ja                    # 日本語 → _build/html/ja/

# ローカルプレビュー
make serve                      # EN のみ :8000（make html 経由）
cd _build/html/ja && python3 -m http.server 18101 &   # JA を :18101 で配信

# Phase 4 配信レイアウトを丸ごとプレビュー（landing + v1.2.4 + 過去版）
make deploy-stage-local         # _build/deploy/ を構築（gh-pages v1.2.2/3 を git archive で引き込み）
make serve-deploy               # :18000 で配信、/ja ⇄ /en 言語切替が動く
```

## 翻訳ワークフロー

**Phase 4 B 案**: 翻訳対象は**手書きページのみ**（`index.md`, `guides/*`,
`packages/index.md`, `packages/visual_slam.md` の計 7 ドキュメント）。
rosdoc2 生成の API ページ（`packages/<pkg>/...`）は英語固定、日本語 PO は保持しません。
背景は `HANDOFF.md` および `~/.claude/.../memory/project_docs2_migration.md`。

```bash
source ../.venv-docs2/bin/activate

# 1) 英語ソース編集 → POT 抽出（Makefile 内で packages/ は自動除外）
make gettext
make update-po                  # sphinx-intl update + build

# 2) 辞書を更新（_scripts/fill_translations.py の INDEX_MD_DICT 等）+ 自動充填
python3 _scripts/fill_translations.py
sphinx-intl build -l ja         # .mo 再生成

# 3) JA ビルド
make html-ja
```

`fill_translations.py` は:
- D1 辞書（手書き 7 ページ分）適用
- `triorb-amr-docs/docs/{Terms,PrivacyPolicy}{,.en}.md` から段落対応で自動翻訳
- D2（rosdoc2 ラベル）は **retired**（`_RETIRED_ROSDOC2_LABEL_DICT` として型だけ保存）

小さなソース変更でも `exclude_patterns` / `version` / `html_*` 等の conf.py 変更があると
env.pickle が全無効化されます。辞書編集程度であれば 5〜15 分の差分ビルド、
conf.py を触るとスクラッチ相当の 1〜2 時間になります（`make clean && make html-ja` も同じ）。

## API パッケージドキュメント (rosdoc2)

```bash
make rosdoc2-image              # ROS 2 Humble + rosdoc2 Docker イメージを一度だけビルド
make rosdoc2                    # 全パッケージの API ドキュメントを再生成（約 30 分）
```

`docker/run_rosdoc2.sh` が submodule 配下のパッケージを自動検出し、`_rosdoc2_out/` で
ビルドした成果物から `packages/` を再構築します。`packages/_manifest.json` に
各パッケージの Doxygen XML パスが記録され、`conf.py` から breathe に渡されます。

公開対象パッケージの選別は `packages/index.md` で行います（`gather_md.py` の
`EXCLUDE_KWDS` に準じた手動メンテ）。

公開/非公開/名称変更ルールの説明は `PACKAGE_VISIBILITY_RULES.md` を参照してください。

## GitHub Pages へデプロイ

`_scripts/deploy_ghpages.sh` が **build → orphan commit → push** を 1 コマンド化。

```bash
# Fork テスト（既定）: 確認プロンプト付き、force-with-lease で push
_scripts/deploy_ghpages.sh
# = _scripts/deploy_ghpages.sh fork gh-pages

# Fork に最新ビルド成果物をそのまま再デプロイ（rebuild スキップ + 確認スキップ）
_scripts/deploy_ghpages.sh --skip-stage --yes

# 本番（origin）デプロイ: --no-force 必須、fast-forward でないと拒否
_scripts/deploy_ghpages.sh --no-force origin

# ヘルプ
_scripts/deploy_ghpages.sh --help
```

### 安全機構（組み込み）

| チェック | 挙動 |
| --- | --- |
| `origin` に force push | **拒否** — `--no-force` 明示必須 |
| `ct.hpp` / `sha256*` が tree に存在 | **拒否**（ライセンス漏洩防止） |
| Working tree を汚さない | 一時 worktree + orphan branch で作業、終了時に自動クリーン |
| Force push | `--force-with-lease`（他者の同時 push を踏まない） |
| 確認プロンプト | 既定 ON、`--yes` で skip |
| Deploy commit message | `source_sha` / `source_branch` / `deploy_ts` を記録 |

### 初回セットアップ（Fork を使う場合）

```bash
# リモート登録
git remote add fork git@github.com:TriOrb-Collaborator/TriOrb-AMR-Documents.git

# 初回デプロイ
_scripts/deploy_ghpages.sh fork

# GitHub GUI: Settings → Pages
#   Source: Deploy from a branch
#   Branch: gh-pages / (root)
# 成功時 URL 例: https://triorb-collaborator.github.io/TriOrb-AMR-Documents/
```

### 本番デプロイの流れ

```bash
# 1) Fork テスト再現で視覚検証（上記）
_scripts/deploy_ghpages.sh

# 2) 問題なければ本番へ
_scripts/deploy_ghpages.sh --no-force origin
```

`--no-force` 付きで push が reject されたら **他者が既に origin/gh-pages を進めている**。その場合は
`git fetch origin gh-pages` で差分を確認、必要なら一時 worktree で merge → 再 push。

---

## Phase 4 配信レイアウト

```
_build/deploy/
├── index.html               # 日英併記 landing（_landing/index.html を sed テンプレート）
├── favicon.png, TriOrb_concept.webp
├── v1.2.4/
│   ├── en/                  # Sphinx EN 出力から .doctrees, _sources を除外
│   └── ja/
└── v1.2.2/, v1.2.3/         # deploy-stage-local が gh-pages から git archive で引き込み
```

`deploy-stage` は `v1.2.4/{en,ja}/` と landing のみ出力。CI の本番デプロイは
gh-pages 上で `v1.2.2/` `v1.2.3/` と mike 共有アセット (`assets/`, `stylesheets/` 等)
を残したまま `v1.2.4/` だけ上書きすればよい設計です（実 deploy step は Phase 4
承認時に `docs2.yml` に追記予定）。

## ディレクトリ構成

| パス | 用途 |
| --- | --- |
| `conf.py` | Sphinx 設定（release, Furo Lapis ブランド、favicon 等） |
| `index.md` | サイトルート（MyST Markdown） |
| `guides/{overview,history,terms,privacy}.md` | 手書きガイド |
| `packages/` | **rosdoc2 生成物**（gitignored、`make rosdoc2` で再生成） |
| `packages/index.md`, `packages/visual_slam.md` | 手書きの index と Visual SLAM 解説 |
| `_handwritten/packages/visual_slam.md` | authoring source（ビルド時に `packages/` にコピー） |
| `_landing/` | 日英併記ランディング + favicon + concept 画像 |
| `_static/` | Sphinx 静的資産（favicon, concept） |
| `_scripts/fill_translations.py` | D1 翻訳自動充填 |
| `_templates/sidebar/language-switcher.html` | Furo サイドバーの JA⇄EN ドロップダウン |
| `docker/{Dockerfile.rosdoc2,run_rosdoc2.sh}` | rosdoc2 Docker 実行環境 |
| `locale/ja/LC_MESSAGES/` | 手書き 7 ドキュメントの JA PO/MO |
| `_build/` | Sphinx 出力（gitignored） |

## 関連ドキュメント

- `../CLAUDE.md` — パイプライン分離ルールと踏みやすい落とし穴
- `HANDOFF.md` — 最新のセッション引き継ぎ、作業状態
- `CI.md` — CI 設計メモ
