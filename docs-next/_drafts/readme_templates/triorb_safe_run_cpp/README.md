# triorb_safe_run_cpp

速度指令に対して安全減速フィルタを適用する C++ ノード。PointCloud 障害物、PLC 状態、協調 alive 監視を統合し、`/drive/run_vel` へ減速後の指令を再配信する。

> package.xml `<description>`: "C++ implementation of the TriOrb safe run velocity filter."
>
> version: 0.0.1 / maintainer: info@triorb.co.jp
>
> executable: `safe_run_cpp_node`

## Overview

TODO: `/safe_drive/run_vel`（または設定された input topic）で受けた速度指令を、点群による前方障害物距離・PLC の SLS / emergency stop 状態・協調 alive によって減速/停止したうえで `/drive/run_vel` へ再配信。協調用の `/bc/collab/run_vel` → `/bc/collab/safed_run_vel` も同様にフィルタする。

## Public ROS 2 API

### Publishers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/except_handl/node/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/error/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/warn/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/drive/run_vel` | `triorb_drive_interface/TriorbRunVel3` | sensor_data depth=1 | TODO: 安全フィルタ適用後の速度指令 |
| `<prefix>/drive/set_life_time` | `std_msgs/UInt16` | parameters | TODO: life_time 再配信 |
| `<prefix>/triorb_safe_run/debug/image/compressed` | `sensor_msgs/CompressedImage` | sensor_data depth=1 | TODO: デバッグ可視化画像 |
| `<prefix>/triorb_safe_run/decelerating` | `std_msgs/Bool` | sensor_data depth=1 | TODO: 減速状態フラグ |
| `<prefix>/bc/collab/safed_run_vel` | `triorb_drive_interface/TriorbRunVel3Stamped` | sensor_data depth=1 | TODO: 協調走行時の安全化速度 |
| `<prefix>/<config_pub>` | `std_msgs/String` | (TODO) | TODO: 現在の config 通知（get_config 応答にも利用？） |

### Subscribers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| (safe_run input topic, param) | `triorb_drive_interface/TriorbRunVel3` | sensor_data depth=1 | TODO: 上流速度指令（`/safe_drive/run_vel` 等） |
| `<prefix>/bc/collab/run_vel` | `triorb_drive_interface/TriorbRunVel3Stamped` | sensor_data depth=1 | TODO: 協調走行速度入力 |
| (parent_bind topic, param) | `triorb_collaboration_interface/ParentBind` | (TODO) | TODO: 親子バインド |
| `<prefix>/collab/alive` | `std_msgs/Header` | parameters | TODO: 協調 alive 監視 |
| (PLC basic_data to_plc topic, param) | `triorb_plc_interface/BasicDataToPLC` | (TODO) | TODO: 自ノードから PLC への状態監視 |
| (複数の PointCloud topics, param) | `sensor_msgs/PointCloud2`（推定） | (TODO) | TODO: 障害物検知用点群（1〜N chan） |

### Services

| Service | Type | 用途（TODO） |
| --- | --- | --- |
| `<prefix>/<set_config>` | `triorb_static_interface/SetString` | TODO: config 全体をロード |
| `<prefix>/<set_param>` | `triorb_static_interface/SetString` | TODO: 単一パラメータ設定 |
| `<prefix>/<get_config>` | `triorb_static_interface/GetString` | TODO: 現在 config を返す |

## Parameters

多数。config YAML ファイルで与えるものが中心。主要カテゴリ（TODO: 具体名を列挙）:
- 入力トピック名（`input_topic`, `output_topic` 等）
- PointCloud ソース一覧
- 減速テーブル（距離→速度係数）
- PLC / collab 有効化フラグ

## Launch / run

```bash
ros2 run triorb_safe_run_cpp safe_run_cpp_node --ros-args --params-file <path/to/safe_run.yaml>
```

TODO: `launch/` 配下の launch file を参照。

## Related Packages

- 上流: `triorb_gamepad`, `triorb_navigation`（`/safe_drive/run_vel` を publish）、点群センサ、PLC (`triorb_sick_plc_wrapper` 等)
- 下流: `triorb_drive_pico`（`/drive/run_vel`）、`triorb_snr_mux_driver`（`/triorb_safe_run/decelerating`）
- インターフェース: `triorb_drive_interface`, `triorb_plc_interface`, `triorb_collaboration_interface`, `triorb_static_interface`
