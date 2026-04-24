# Package Visibility Rules

`docs-next/` における package 公開可否と名称変更ルールの集約メモです。

対象デプロイ:

- `https://triorb-collaborator.github.io/TriOrb-AMR-Documents/v1.2.4/ja/`

実装上の正本:

- 公開 package 一覧: `docs-next/docker/run_rosdoc2.sh` の `PUBLIC_PACKAGE_NAMES`
- 非公開判定の補助: `docs-next/docker/run_rosdoc2.sh` の `EXCLUDE_PREFIXES`
- 手書き差し替え: `docs-next/_handwritten/packages/`
- カテゴリ割当: `docs-next/docker/run_rosdoc2.sh` の `categorize()` と `docs-next/_handwritten/packages/_categories.json`

このファイルは運用ルールの説明用です。実際のビルド結果は必ず上記実装に従います。

ルール確定の根拠:

- 実装の正本: `docs-next/docker/run_rosdoc2.sh`
- 公開中サイトの実績値: `https://triorb-collaborator.github.io/TriOrb-AMR-Documents/v1.2.4/ja/index.html`
- 追加運用指示: Claude Code CLI ログ
  - `path_planning_serverも除去。その他にもgather_md.pyでEXCLUDEしているものは全て除外。`

補足:

- `docs-next` の現行運用では、単に `gather_md.py` を機械的に踏襲するのではなく、公開中 `v1.2.4` の package 一覧に一致することも確認基準とする
- `triorb_dead_reckoning` は公開中 `v1.2.4` には含まれていたが、現行方針では非公開とする

## 1. 基本方針

- 公開対象は、外部利用者に見せる ROS 2 API / Interface のみ
- 内部実装、社内運用向け package、協調移動系、3rd-party 内部依存は公開しない
- upstream 名をそのまま見せたくないもの、または内部 API をそのまま露出したくないものは、手書きページで差し替える
- package 一覧そのものは `PUBLIC_PACKAGE_NAMES` の allowlist を最優先とし、部分更新時に古い manifest や残骸ディレクトリから package が復活しないようにする

## 2. 現在の公開対象

`PUBLIC_PACKAGE_NAMES` に列挙する package だけを公開する。

- `triorb_drive_pico`
- `triorb_drive_vector`
- `triorb_navigation`
- `triorb_navigation_manager`
- `triorb_safe_run_cpp`
- `triorb_snr_mux_driver`
- `triorb_tagslam_manager`
- `triorb_camera_argus`
- `triorb_camera_capture`
- `triorb_gamepad`
- `triorb_sick_plc_wrapper`
- `triorb_sls_wrapper`
- `triorb_battery_info`
- `triorb_gpio`
- `triorb_host_info`
- `triorb_os_setting`
- `visual_slam`（hand-written 差し替え）

補足:

- `EXCLUDE_PREFIXES` は「なぜ非公開なのか」を明文化する補助ルールとして残す
- 実際の package 一覧の最終決定は allowlist で行う

## 3. 非公開ルール

以下は `docs-next/docker/run_rosdoc2.sh` の `EXCLUDE_PREFIXES` で除外する。

### 3.1 内部 package

- `pkgs/triorb_navi_bridge`
- `pkgs/triorb_drive/path_planning_server`
- `pkgs/triorb_drive/triorb_dead_reckoning`
- `pkgs/triorb_drive/triorb_automove_task`
- `pkgs/triorb_drive/triorb_follow_path_planner`
- `pkgs/triorb_drive/triorb_linear_path_planner`
- `pkgs/triorb_drive/triorb_navigation_utils`
- `pkgs/triorb_drive/triorb_navigation_vslam_tf`
- `pkgs/triorb_drive/triorb_path_controller_interface`
- `pkgs/triorb_drive/triorb_path_follow_controller`
- `pkgs/triorb_drive/triorb_path_search_server`
- `pkgs/triorb_drive/triorb_pid_pos_controller`
- `pkgs/triorb_drive/triorb_pid_vel_controller`
- `pkgs/triorb_drive/triorb_region_map`
- `pkgs/triorb_drive/triorb_towing_path_planner`
- `pkgs/triorb_drive/triorb_vslam_tf`
- `pkgs/triorb_drive/triorb_vslam_tf_bridge`
- `pkgs/triorb_navigation_pkgs/`
- `pkgs/triorb_fleet/`
- `pkgs/triorb_service/`
- `pkgs/triorb_sensor/triorb_calibration`
- `pkgs/triorb_sensor/triorb_camera_calibration`
- `pkgs/triorb_sensor/triorb_can`
- `pkgs/triorb_sensor/triorb_sls_drive_manager`
- `pkgs/triorb_sensor/triorb_streaming_images`
- `pkgs/triorb_os/triorb_socket`

### 3.2 協調移動系

- `pkgs-collab/`

理由:

- 協調移動 API は別系統で扱う
- `docs-next` の公開 API サイトでは露出しない
- Claude Code CLI の追加指示でも、`gather_md.py` で除外していたものは `docs-next` 側でも除外する運用になっている

### 3.3 Interface のうち非公開のもの

- `pkgs/TriOrb-ROS2-Types/triorb_collaboration_interface`
- `pkgs/TriOrb-ROS2-Types/triorb_cv_interface`
- `pkgs/TriOrb-ROS2-Types/triorb_field_interface`
- `pkgs/TriOrb-ROS2-Types/triorb_project_interface`

### 3.4 3rd-party / upstream 依存

- `pkgs/rosbridge_suite/`
- `pkgs/stella_vslam_ros/`
- `pkgs/triorb_sensor/sick/sick_safetyscanners2`
- `pkgs/triorb_sensor/sick/sick_safetyscanners_base`
- `pkgs/triorb_sensor/sick/sick_Flexi-Soft_ROS2`

## 4. 名称変更 / 差し替えルール

### 4.1 Visual SLAM

- ソース上の upstream / internal package:
  - `pkgs/stella_vslam_ros/`
- 公開上の見せ方:
  - `triorb_visual_slam`
- 実体:
  - `docs-next/_handwritten/packages/visual_slam/index.md`
  - `docs-next/_handwritten/packages/visual_slam/API.md`

意図:

- `stella_vslam_ros` をそのまま公開しない
- Visual SLAM は TriOrb BASE 上の機能単位として説明する
- 内部 wrapper の API は実装詳細として扱い、必要な公開情報だけ手書きで出す

## 5. 現在の公開カテゴリ

`packages/index.md` では以下のカテゴリで公開する。

- `Drive & Navigation`
- `SLAM`
- `Sensor I/O`
- `Safety Sensors`
- `OS / Infrastructure`
- `Interfaces`
- `Other`

補足:

- `Fleet` と `Service` はカテゴリ定義自体はコードに残っていても、現行ルールでは公開対象を除外しているため通常は出ない

## 6. 変更手順

### 6.1 package を非公開にする

1. `docs-next/docker/run_rosdoc2.sh` の `PUBLIC_PACKAGE_NAMES` から削除
2. 必要なら `EXCLUDE_PREFIXES` にも追加
3. `make rosdoc2`
4. `make html` / `make html-ja`
5. `make deploy-stage-local`
6. `v1.2.4/ja` と `v1.2.4/en` のナビから消えていることを確認

### 6.2 package を公開に戻す

1. `docs-next/docker/run_rosdoc2.sh` の `PUBLIC_PACKAGE_NAMES` に追加
2. 必要なら `EXCLUDE_PREFIXES` から削除
3. 必要ならカテゴリ判定 `categorize()` を確認
4. `make rosdoc2`
5. `make html` / `make html-ja`
6. `make deploy-stage-local`

### 6.3 名称を変えて公開する

1. 元 package を `PUBLIC_PACKAGE_NAMES` に入れない
2. 必要なら `EXCLUDE_PREFIXES` にも追加
3. `docs-next/_handwritten/packages/<public_name>/` を作成
4. 必要なら `docs-next/_handwritten/packages/_categories.json` にカテゴリを追加
5. `make rosdoc2`
6. `make html` / `make html-ja`
7. `make deploy-stage-local`

## 7. 関連ファイル

- `docs-next/docker/run_rosdoc2.sh`
- `docs-next/_handwritten/packages/visual_slam/`
- `docs-next/_handwritten/packages/_categories.json`
- `docs-next/packages/index.md`
- `docs-next/HANDOFF.md`

## 8. 注意

- `gather_md.py` の `EXCLUDE_KWDS` は legacy `triorb-amr-docs/` 向けであり、`docs-next` の現行ルールと完全には一致しない
- `docs-next` 側の運用判断は `gather_md.py` ではなく `docs-next/docker/run_rosdoc2.sh` を正本とする
- package 一覧の最終決定は `PUBLIC_PACKAGE_NAMES` を優先する
- ただし `v1.2.4` 移行時には、Claude Code CLI 上で `gather_md.py` の除外方針を `docs-next` にも適用する追加判断が入っている
- 公開/非公開ルールを変更したら、`make deploy-stage-local` 後に Playwright で公開中 `v1.2.4/ja/index.html` と package 一覧を比較して差分を確認する
