# triorb_drive_vector

制御指令値からロボットの進行方向や停止・回転などの状態を判定し、単純なベクトル表現として再配信する軽量ノード（C++）。`triorb_snr_mux_driver` などが進行方向判定に利用する。

> package.xml `<description>`: "制御指令値からロボットの進行方向や停止・回転などの状態判定を行う"
>
> version: 1.2.0 / maintainer: info@triorb.co.jp
>
> executable: `drive_vector`

## Overview

TODO: `drive/run_pos` / `drive/run_vel` を購読して `Float32MultiArray` (2要素: 進行ベクトル) として再配信する。協調 (collab) 走行時は `bc/collab/run_vel` + `collab/parent_bind` と `robot/status` を参照し `/collab/drive/std_vector2` に再配信する、等を記入。

## Public ROS 2 API

すべてのトピック名は `ROS_PREFIX` 環境変数がプレフィックスとして付与される（`GET_TOPIC_NAME` マクロ経由）。

### Publishers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/drive/std_vector2` | `std_msgs/Float32MultiArray` | sensor_data depth=1 | TODO: 進行方向 2 次元ベクトル |
| `<prefix>/collab/drive/std_vector2` | `std_msgs/Float32MultiArray` | sensor_data depth=1 | TODO: 協調走行時の進行ベクトル |

### Subscribers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| (TODO: set_pos topic) | `triorb_drive_interface/TriorbRunPos3` | (TODO) | TODO: 位置指令入力（topic 名要確認） |
| (TODO: set_vel topic) | `triorb_drive_interface/TriorbRunVel3` | (TODO) | TODO: 速度指令入力（topic 名要確認） |
| (TODO: collab vel topic) | `triorb_drive_interface/TriorbRunVel3Stamped` | (TODO) | TODO: 協調走行速度入力 |
| (TODO: parent_bind topic) | `triorb_collaboration_interface/ParentBind` | (TODO) | TODO: 親子バインド情報 |
| (TODO: robot status topic) | `triorb_static_interface/RobotStatus` | (TODO) | TODO: ロボット状態 |

## Parameters

TODO: `declare_parameter` された項目を列挙（src/drive_vector.cpp 内部参照）。

## Launch / run

```bash
ros2 run triorb_drive_vector drive_vector
```

TODO: launch file / config YAML があれば記載。

## Related Packages

- 上流: `triorb_navigation`, `triorb_gamepad`（`/drive/run_vel` publish）
- 下流: `triorb_snr_mux_driver`（`/drive/std_vector2` subscribe）
- インターフェース: `triorb_drive_interface`, `triorb_static_interface`, `triorb_collaboration_interface`
