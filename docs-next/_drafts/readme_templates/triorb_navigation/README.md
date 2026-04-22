# triorb_navigation

自律移動の中核ノード。経路追従、SLAM 連動のキーフレーム切替、PLC 状態参照に基づく安全制御を行う（C++）。

> package.xml `<description>`: "自律移動を行うためのパッケージ"
>
> version: 1.1.0 / maintainer: info@triorb.co.jp
>
> executable: `navigate`

## Overview

TODO: `triorb_navigation_manager` から経路・目標姿勢を受け取り、実速度指令（`/drive/run_vel` または `TriorbRunVel3Stamped`）を Pico に向けて出力。PLC 状態 (`/plc/basic_data/from_plc`) による安全減速、SLAM キーフレームとウェイポイントの同期、協調走行時のパス配信も担う。

## Public ROS 2 API

すべてのトピック名は `ROS_PREFIX` 環境変数がプレフィックスとして付与される（`GET_TOPIC_NAME` マクロ経由）。
一部 topic 名はパラメータ (`pub_run_pos`, `pub_run_vel`, `pub_safe_run_vel`, `pub_run_result`, `pub_set_life_time`, `set_enable_camera`, `sub_save_waypoint`, `sub_set_keyframe_by_waypoint` 等) でカスタマイズ可能。

### Publishers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/except_handl/node/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/error/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/warn/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/<pub_run_pos>` (default TBD) | `triorb_drive_interface/TriorbRunPos3` | parameters | TODO: 位置指令 |
| `<prefix>/<pub_run_vel>` (default TBD) | `triorb_drive_interface/TriorbRunVel3` or `TriorbRunVel3Stamped` | sensor_data depth=1 | TODO: 速度指令（stamped 版切替パラメータあり） |
| `<prefix>/<pub_safe_run_vel>` | `triorb_drive_interface/TriorbRunVel3` or `TriorbRunVel3Stamped` | sensor_data depth=1 | TODO: 安全フィルタ投入用 |
| `<prefix>/<pub_run_result>` | `triorb_drive_interface/TriorbRunResult` or `TriorbRunResultStamped` | parameters | TODO: 移動結果通知 |
| `<prefix>/<pub_set_life_time>` | `std_msgs/UInt16` | parameters | TODO: life_time 配信 |
| `<prefix>/<set_enable_camera>` | `std_msgs/Int8MultiArray` | parameters | TODO: カメラ選択 |
| `<prefix>/run_slam/set/manual_keyframes` | `triorb_slam_interface/KeyframeArray` | parameters | TODO: SLAM キーフレーム手動投入 |
| `<prefix>/set/robot/center` | `triorb_drive_interface/TriorbPos3` | sensor_data depth=1 | TODO: ホイールベース/重心設定 |
| `<prefix>/drive/state` | `triorb_drive_interface/TriorbRunState` | parameters | TODO: ナビ状態 |

### Subscribers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| (interrupt) stop/pause/restart topics (params) | `std_msgs/Empty` | parameters | TODO: 割り込み系（stop/pause/restart） |
| finish topic (param) | `std_msgs/Bool` | parameters | TODO: 完了通知 |
| set_pos | `triorb_drive_interface/TriorbSetPos3` | parameters | TODO: 絶対位置設定 |
| init_path_follow | `std_msgs/Empty` | parameters | TODO: 経路追従初期化 |
| `<prefix>/<gains topic>` | `triorb_drive_interface/DriveGains` | parameters | TODO: PID ゲイン設定 |
| `<prefix>/<sub_save_waypoint>` | `std_msgs/String` | parameters | TODO: ウェイポイント保存ハッシュ |
| `<prefix>/<sub_set_keyframe_by_waypoint>` | `std_msgs/String` | parameters | TODO: ウェイポイント指定キーフレーム切替 |
| `<prefix>/run_slam/current_keyframes` | `triorb_slam_interface/KeyframeArray` | sensor_data depth=1 | TODO: 現在 SLAM キーフレーム受信 |
| `<prefix>/plc/basic_data/from_plc` | `triorb_plc_interface/BasicDataFromPLC` | (TODO) | TODO: PLC 状態受信（安全判定） |
| `<prefix>/snr_mux/info` | `std_msgs/String` | sensor_data depth=1 | TODO: SNR-MUX 情報受信 |

### Services

| Service | Type | 用途（TODO） |
| --- | --- | --- |
| (param-named) set_pos srv | `triorb_drive_interface/TriorbSetPos3` | TODO: 同期的な絶対位置設定 |

### Actions

| Action | Type | 用途（TODO） |
| --- | --- | --- |
| (param-named) set_path action | `triorb_drive_interface/TriorbSetPath` | TODO: 経路追従アクション（goal: path, feedback: progress, result: 到達結果） |

## Parameters

多数。navigate.cpp で `declare_parameter` / `get_parameter` しているもの。主なもの:
- `pub_run_pos`, `pub_run_vel`, `pub_safe_run_vel`, `pub_run_result`, `pub_set_life_time`
- `set_enable_camera`
- `sub_save_waypoint`, `sub_set_keyframe_by_waypoint`
- TODO: 他の PID ゲイン、SLS 連携などの declare を列挙

## Launch / run

```bash
ros2 run triorb_navigation navigate
```

TODO: config YAML / launch file のパスを記入。

## Related Packages

- 上流: `triorb_navigation_manager`（割り込み・経路コマンドを publish）、`triorb_plc_interface`（PLC 状態）、`stella_vslam_ros` / tagslam（キーフレーム）
- 下流: `triorb_drive_pico`（`/drive/run_vel`, `/drive/run_pos` を subscribe）、`triorb_safe_run_cpp`（`/drive/run_vel` を再フィルタ）、`triorb_snr_mux_driver`
- インターフェース: `triorb_drive_interface`, `triorb_slam_interface`, `triorb_plc_interface`, `triorb_static_interface`
