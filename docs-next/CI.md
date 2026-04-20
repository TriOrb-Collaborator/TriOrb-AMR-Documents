# docs2 CI 概要

[`.github/workflows/docs2.yml`](../.github/workflows/docs2.yml) の設計メモです。

## トリガ

| イベント | ブランチ | 目的 |
|---|---|---|
| push | `docs2-poc`, `docs2/**` | PoC / ステージング用 |
| pull_request | `docs2-poc`, `docs2/**` | レビュー時のプレビュービルド |
| workflow_dispatch | 任意 | 手動再実行 |

現在 `master` では発火しません。v1.2.5 リリース時（Phase 4 cutover）で master/release branches をトリガに追加する予定です。

## ジョブ構成 (1 job)

```
Checkout ─► Python setup (cached pip)
       ─► Install Sphinx/breathe/playwright
       ─► Docker Buildx setup
       ─► Build triorb-rosdoc2 image  (GHA layer cache: scope=rosdoc2)
       ─► Run rosdoc2 on packages → docs-next/packages/
       ─► Sphinx build (JP)
       ─► sphinx-intl update-po
       ─► Sphinx build (EN)
       ─► Playwright visual check
       ─► Artifact: docs2-site, docs2-screenshots
```

## キャッシュ戦略

| 対象 | 方法 | 想定短縮効果 |
|---|---|---|
| pip deps | `actions/setup-python` の `cache: pip` | 毎回約 30 秒 |
| Docker image layers | `docker/build-push-action` + `cache-from/to: type=gha` (scope=rosdoc2) | 初回 5〜10 分 → 2 回目以降 ~1 分 |
| colcon build | 未キャッシュ (Phase 3 で検討) | 初回と同条件 ~2 分/pkg |
| rosdoc2 生成物 (`packages/`) | 未キャッシュ (常に再生成) | 常に ~数分 |

## 現時点の想定所要時間

| 状態 | 所要時間 (目安) |
|---|---|
| cold (全 cache miss) | 20〜30 分 |
| warm (image cache hit) | 8〜12 分 |
| small diff (Python only 変更) | 3〜5 分 |

## デプロイは別ステップ

Phase 4 cutover 以前:
- workflow が artifact を吐くだけ。`gh-pages` への push は**しない**。
- 既存 `master` の mike pipeline (`triorb-amr-docs/`) は触らない。

Phase 4 以降の追加ステップ案:
- `gh-pages` の `/v1.2.5/` 配下へ rsync デプロイ
- `versions.json` を編集して legacy (v1.2.2〜v1.2.4) と共存させる
- 言語ごと `/v1.2.5/ja/`, `/v1.2.5/en/` に配置

## 改善候補 (Phase 2 後半 〜 Phase 3)

1. **colcon build のキャッシュ**: submodule HEAD ハッシュをキーに `/ws/install`, `/ws/build` を GHA cache へ。1 パッケージでも 2 分短縮
2. **rosdoc2 出力のキャッシュ**: submodule のパッケージ単位のハッシュをキーに `packages/<pkg>/` を cache。変更なしパッケージは再生成スキップ
3. **matrix ビルド**: 各 ROS 2 パッケージを並列ジョブに分解（ただし umbrella build はシリアル化が必要）
4. **PR プレビュー**: artifact を Netlify / Cloudflare Pages / GitHub Pages preview に publish するアクション追加
5. **リリース時のブランチ方針**: `release/docs2.v1.2.5` タグで cutover 用ワークフローを分ける（通常 CI と完全分離）

## セキュリティ

- submodule チェックアウトに PAT は不要 (public submodule 前提)
  - Private submodule 化した場合は `actions/checkout` に `token` 追加
- Dockerfile は ROS 公式 image ベース、追加 apt / pip のみで自己完結
- rosdoc2 container は読み取り専用で submodule を mount し、書き込みは `/ws/output` のみ

## ローカル再現

CI と同じ流れを手元で回す:
```bash
make -C docs-next rosdoc2-image          # 初回のみ
make -C docs-next rosdoc2                # packages/ 再生成
make -C docs-next html                   # JP
make -C docs-next update-po              # PO 更新
make -C docs-next html-en                # EN
python3 docs-next/_shot.py               # Playwright visual check
```
