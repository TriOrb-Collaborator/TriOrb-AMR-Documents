# triorb_navigation_manager

TriOrb製移動ロボット向けのROS 2ノードで、CSVベースの経路ナビゲーションを制御します。
   通常走行、協調走行、リフター動作、地図切替、イベント処理、状態通知などを統合的に管理し、
   TriOrbのドライブ・SLAMシステムと連携可能です。

> version: `1.2.0` / maintainer: TriOrb <info@triorb.co.jp> / license: Apache License, Version 2.0

## Overview

TODO: このパッケージが提供する機能、起動タイミング、関連ノードとの連携を 2–4 文で。

## API Reference

> Source: migrated from the hand-written `API.md` in the submodule.

TriOrb製移動ロボット向けのROS 2ノードで、CSVベースの経路ナビゲーションを制御します。
   通常走行、協調走行、リフター動作、地図切替、イベント処理、状態通知などを統合的に管理し、
   TriOrbのドライブ・SLAMシステムと連携可能です。

#### 代表的な`type`と動作

| type | 内容 | 使用トピック |
| --- | --- | --- |
| `point` `into` | 絶対座標走行。`into`はTagSLAM側ポーズ設定。 | `/drive/set_pos` `/tagslam/drive/set_pos` |
| `collab*` | 協調搬送系。 | `/collab/request/set_pos` |
| `relative` | 相対移動。 | `/drive/run_pos` |
| `リフター` / `協調リフト` | 単体/協調リフター命令。 | `/drive/run_lifter` `/collab/run_lifter` |
| `一時停止` | 指定秒数待機。 | 内部タイマー |
| `イベント発行` / `イベント待ち` | `/action/event` によるイベント送受信。 | `/action/event` |
| `地図切替` / `地図遷移` | MQTTでVSLAM制御 または `/run_slam/set/enter_local_map_file_path` へ通知。 | `vslam/signal` 他 |
| `地図切替(TagSLAM)` | `/tagslam/load/map`へJSONを送信。 | `/tagslam/load/map` |
| `マーカー設定` | MarkerSetting(default/only/exclude)切替。 | `/run_slam/set/marker_only` `/run_slam/set/marker_exclude` |
| `安全装置起動/停止` | SLSブレーキ制御。 | `/sls/set/brake` |
| `減速範囲設定` | フィールドID(10進/0xNN)を`UInt8`変換して送出。 | `/sls/set/field` |

### ノードAPI

#### Subscriber

| Topic | 型 | 役割 |
| --- | --- | --- |
| `/nav/route_csv_name` | `std_msgs/msg/String` | CSVファイル名を受け取りWayPointを再ロード。 |
| `/nav/action` | `std_msgs/msg/String` | `start`/`stop`/`pause`/`resume`/`resume_failed` コマンド。 |
| `/drive/result` | `triorb_drive_interface/msg/TriorbRunResult` | 通常走行結果。 |
| `/collab/drive/completed` | `triorb_drive_interface/msg/TriorbRunResultStamped` | 協調走行結果。 |
| `/drive/run_pos/result` | `std_msgs/msg/String` | 相対移動結果（"done"等）。 |
| `/lifter/result` | `std_msgs/msg/String` | 単体リフター結果。 |
| `/collab/lifter/result` | `std_msgs/msg/String` | 協調リフター結果（JSON文字列）。 |
| `/action/event` | `std_msgs/msg/String` | イベント待ちモードで一致イベントを待受。 |
| `/triorb/request_nav_state` | `std_msgs/msg/Empty` | 状態再送指示。 |
| `/run_slam/map_file_changed` | `std_msgs/msg/String` | 地図ファイル変更通知、地図待機解除に使用。 |

##### 呼び出し例

```bash
## 経路CSVをsample_route.csvへ切替
ros2 topic pub /nav/route_csv_name std_msgs/msg/String "data: 'sample_route.csv'"

## 速度倍率1.0、精度バイアス0、1ループで走行開始
ros2 topic pub /nav/action std_msgs/msg/String "data: 'start,1.0,0.0,0.0,1'"

## 協調走行結果はechoで監視
ros2 topic echo /collab/drive/completed

## リフター完了通知を監視
ros2 topic echo /lifter/result

## イベント待ちアクションに合致させるイベントを送信
ros2 topic pub /action/event std_msgs/msg/String "data: 'door_opened'"

## 最新のナビゲーション状態をリクエスト
ros2 topic pub /triorb/request_nav_state std_msgs/msg/Empty "{}"
```

#### Publisher

| Topic | 型 | 役割 |
| --- | --- | --- |
| `/nav/handling_task_csv_name` | `std_msgs/msg/String` | 現在処理中のCSV名を通知。 |
| `/triorb/nav/state` | `std_msgs/msg/Int32MultiArray` | ナビ状態／エラー／復帰情報。 |
| `/triorb/nav/result` | `std_msgs/msg/String` | `NavResult&&詳細` 形式の結果通知。 |
| `/drive/init_path_follow` `/collab/drive/init_path_follow` `/tagslam/drive/init_path_follow` | `std_msgs/msg/Empty` | 各経路制御モジュールの初期化。 |
| `/drive/set_pos` `/tagslam/drive/set_pos` `/collab/request/set_pos` | `triorb_drive_interface/msg/TriorbSetPos3` | 走行目標の送信。 |
| `/drive/run_pos` | `triorb_drive_interface/msg/TriorbRunPos3` | 相対移動指示。 |
| `/drive/pause` `/drive/restart` `/drive/stop` ほか`/collab/drive/*` | `std_msgs/msg/Empty` | 走行制御。 |
| `/drive/run_lifter` `/collab/run_lifter` | `std_msgs/msg/String` | リフター指示。 |
| `/action/event` | `std_msgs/msg/String` | イベント発行。 |
| `/run_slam/set/enter_local_map_file_path` | `std_msgs/msg/String` | 地図遷移時に使用。 |
| `/run_slam/set/marker_only` `/run_slam/set/marker_exclude` | `std_msgs/msg/Bool` | MarkerSetting切替。 |
| `/tagslam/load/map` | `std_msgs/msg/String` | TagSLAM用地図切替（JSON文字列）。 |
| `/sls/set/brake` | `std_msgs/msg/Bool` | SLSブレーキON/OFF。 |
| `/sls/set/field` | `std_msgs/msg/UInt8` | 減速エリア設定。 |
| `/except_handl/node/add` `/triorb/error/str/add` `/triorb/warn/str/add` | `std_msgs/msg/String` | 例外監視システムへの登録/エラー/警告送信。 |

#### Service

| Service | 型 | 内容 |
| --- | --- | --- |
| `/get/version/<node_name>` | `triorb_static_interface/srv/Version` | ノードバージョン（`1.2.2`）を配列で返却。 |

#### MQTT

| Topic | 向き | 内容 |
| --- | --- | --- |
| `/vslam/map_load_queuing_time_estimated` | Subscribe | マップ読込推定時間（秒）。 |
| `/vslam/map_skip_loading_request` | Subscribe | 地図読込スキップ要求。 |
| `vslam/signal` | Publish | `load_<map>` メッセージでVSLAMへ地図切替指示。 |

### コマンド/メッセージ仕様

#### `/nav/action`

- `start,<ratio_speed>,<bias_xy>,<bias_deg>,<loop>`  
  例: `start,1.0,0.0,0.0,1`。Start/End行間のWayPointをloop回だけ走行。
- `stop` / `pause` / `resume` は通常の停止および一時停止制御。
- `resume_failed` は失敗時に保持した`resume_pos_idx`から再開。`enter_failure_hold_state`で保持される。

#### `/triorb/nav/state` (`std_msgs/msg/Int32MultiArray`)

配列構造: `[state, loop_count, loop, pos_idx, markerSetting, error_pair_count, error_list..., resume_pos_idx, resume_available_flag]`

- `state`: `NavState` (`0:IDLE / 1:NAVIGATING / 2:PAUSED`)
- `markerSetting`: `0:default / 1:only / 2:exclude`
- `error_list`: 2要素で1組（WayPoint行番号, 種別コード 0:角度精度 1:XY精度 2:双方）
- `resume_available_flag`: 1の場合`resume_failed`で再開可

#### `/triorb/nav/result`

`<NavResult>&&<詳細>` 形式。代表値:

| NavResult | 意味 |
| --- | --- |
| `SUCCESS` | 経路完遂 |
| `NAV_FAILED` | 走行系エラー（`msg_to_json_string`で詳細付与） |
| `USER_CANCELLED` | `stop`指示で終了 |
| `ROUTE_ERROR` `WAYPOINT_SETTING_ERROR` など | 入力CSV関連 |
| `LIFTER_ERROR` | リフター失敗 |
| `MAP_LOAD_TIME_OUT_ERROR` | 地図切替タイムアウト |
| `UNKNOW_ACTION_ERROR` ほか | 想定外アクション |

アクション失敗時は`enter_failure_hold_state`で停止し、成功時は`check_compleated_operation`で次WayPointまたはLoop切り替えを実施。

## Related Packages

TODO: 上流・下流の関連パッケージを列挙。
