# triorb_navigation_manager

CSV ベースの経路ナビゲーションを統合管理する上位ノード。通常走行、協調走行、リフタ動作、地図切替、イベント処理、PLC 状態連動、SLS 連動などを取りまとめる。

> package.xml `<description>`: "TriOrb製移動ロボット向けのROS 2ノードで、CSVベースの経路ナビゲーションを制御します。通常走行、協調走行、リフター動作、地図切替、イベント処理、状態通知などを統合的に管理し、TriOrbのドライブ・SLAMシステムと連携可能です。"
>
> version: 1.2.0 / maintainer: info@triorb.co.jp
>
> executable(s): `navigation_manager` (entry: `triorb_navigation_manager.navigation_manager:main`)

## Overview

TODO: CSV ルート（ウェイポイント列）を読み込み、`triorb_navigation` (navigate) に対して init/set_pos/run_pos/pause/stop/restart を順次発行。状態は `/navigation/state`、結果は `/navigation/result` として配信。協調 (`/collab/...`) / TagSLAM (`/tagslam/...`) 並行系もカバー。

## Public ROS 2 API

すべてのトピック名は `ROS_PREFIX` 環境変数がプレフィックスとして付与される。

### Publishers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/except_handl/node/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/error/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/warn/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/<route_csv_handle>` | (TODO) | parameters | TODO: 処理中 CSV 名通知 |
| `<prefix>/drive/run_lifter` | `std_msgs/String` | parameters | TODO: リフタ指令 |
| `<prefix>/collab/run_lifter` | `std_msgs/String` | parameters | TODO: 協調リフタ指令 |
| `<prefix>/<nav_action_topic>` | `std_msgs/String` | parameters | TODO: ナビアクション通知 |
| `<prefix>/<enter_local_map>` | `std_msgs/String` | parameters | TODO: ローカルマップ切替 |
| `<prefix>/<set_marker_only>` | (TODO) | parameters | TODO: マーカ対象指定 |
| `<prefix>/<set_marker_exclude>` | (TODO) | parameters | TODO: マーカ除外指定 |
| `<prefix>/navigation/state` | (TODO: Int32MultiArray?) | parameters | TODO: ナビ状態通知 |
| `<prefix>/navigation/result` | `std_msgs/String` | parameters | TODO: ナビ結果通知 |
| `<prefix>/navigation/start` | `std_msgs/String` | parameters | TODO: ナビ開始通知 |
| `<prefix>/drive/init_path` | `std_msgs/Empty` | parameters | TODO: path 初期化指示 |
| `<prefix>/drive/set_pos` | `triorb_drive_interface/TriorbSetPos3` | parameters | TODO: 絶対位置設定 |
| `<prefix>/drive/run_pos` | `triorb_drive_interface/TriorbRunPos3` | parameters | TODO: 位置指令 |
| `<prefix>/drive/pause` | `std_msgs/Empty` | parameters | TODO |
| `<prefix>/drive/resume` | `std_msgs/Empty` | parameters | TODO |
| `<prefix>/drive/stop` | `std_msgs/Empty` | parameters | TODO |
| `<prefix>/collab/init_path` | `std_msgs/Empty` | parameters | TODO |
| `<prefix>/collab/set_pos` | `triorb_drive_interface/TriorbSetPos3` | parameters | TODO |
| `<prefix>/collab/pause` | `std_msgs/Empty` | parameters | TODO |
| `<prefix>/collab/resume` | `std_msgs/Empty` | parameters | TODO |
| `<prefix>/collab/stop` | `std_msgs/Empty` | parameters | TODO |
| `<prefix>/tagslam/init_path` | `std_msgs/Empty` | parameters | TODO |
| `<prefix>/aux/event` | `std_msgs/String` | parameters | TODO: 補助イベント（音声/ランプ等） |
| `<prefix>/collab/aux/event` | `std_msgs/String` | parameters | TODO |
| `<prefix>/tagslam/drive/set_pos` | `triorb_drive_interface/TriorbSetPos3` | depth=10 | TODO |
| `<prefix>/tagslam/load/map` | `std_msgs/String` | depth=10 | TODO: TagSLAM マップ切替 |
| `<prefix>/sls/set/brake` | `std_msgs/Bool` | depth=10 | TODO: SLS ブレーキ指示 |
| `<prefix>/sls/set/field` | `std_msgs/UInt8` | depth=10 | TODO: SLS 監視フィールド切替 |
| `<prefix>/triorb/error/reset` | `std_msgs/UInt8` | depth=10 | TODO: エラーリセット |

### Subscribers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/<route_csv_name>` | `std_msgs/String` | parameters | TODO: ルート CSV 指定入力 |
| `<prefix>/<nav_action>` | (TODO) | parameters | TODO: ナビアクション要求 |
| `<prefix>/<move_result>` | (TODO) | parameters | TODO: 移動結果受信（navigate から） |
| `<prefix>/<collab_move_result>` | (TODO) | parameters | TODO: 協調移動結果 |
| `<prefix>/<request_nav_state>` | (TODO) | parameters | TODO: ナビ状態問い合わせ |
| `<prefix>/lifter/result` | `std_msgs/String` | parameters | TODO: リフタ結果受信 |
| `<prefix>/collab/lifter/result` | `std_msgs/String` | parameters | TODO: 協調リフタ結果 |
| `<prefix>/<nav_action_topic>` (re-subscribe) | `std_msgs/String` | parameters | TODO |
| `<prefix>/<map_file_change>` | (TODO) | parameters | TODO: マップファイル切替通知 |
| `<prefix>/<tag_map_change>` | (TODO) | parameters | TODO: TagSLAM マップ切替通知 |
| `<prefix>/drive/run_pos/result` | `std_msgs/String` | parameters | TODO: 位置移動結果 |
| `<prefix>/plc/basic_data/from_plc` | `triorb_plc_interface/BasicDataFromPLC` | best_effort depth=1 | TODO: PLC 入力 |
| `<prefix>/snr_mux/info` | `std_msgs/String` | best_effort depth=1 | TODO: SNR-MUX 情報 |
| `<prefix>/triorb/error/num` | `std_msgs/UInt8` | best_effort depth=1 | TODO: エラー番号 |

### Services

| Service | Type | 用途（TODO） |
| --- | --- | --- |
| `<prefix>/get/version/navigation_manager` | `triorb_static_interface/Version` | TODO: バージョン取得 |

## Parameters

TODO: `declare_parameter` 項目（route CSV パス、ルート名、協調/TagSLAM 切替フラグ等）を列挙。

## Launch / run

```bash
ros2 run triorb_navigation_manager navigation_manager
```

TODO: 実運用の launch file と設定投入手順。

## Related Packages

- 上流（イベント送信元）: UI / 外部コマンド（`/navigation/action` 等を publish）、`triorb_sls_drive_manager`, `triorb_snr_mux_driver`, PLC
- 下流（制御先）: `triorb_navigation`（navigate）、`triorb_drive_pico`、`triorb_sls_drive_manager`（`/sls/set/*`）、tagslam
- インターフェース: `triorb_drive_interface`, `triorb_plc_interface`, `triorb_static_interface`, `triorb_camera_argus`
