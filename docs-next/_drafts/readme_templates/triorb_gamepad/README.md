# triorb_gamepad

ゲームパッド入力を監視し、走行・リフタ・非常停止などのコマンドを ROS 2 トピックへ出力するテレオペ用ノード（C++、rclcpp_lifecycle 対応）。

> package.xml `<description>`: "ゲームパッド入力を監視し、走行・リフタ・非常停止などのコマンドをROS 2トピックへ出力するテレオペ用ノードです。"
>
> version: 0.0.0 / maintainer: info@triorb.co.jp
>
> executable: `triorb_gamepad`

## Overview

TODO: /dev/input/jsN を直接 open し、ボタン/スティック入力を `TriorbRunVel3` や `/drive/stop` 等に変換。PLC 状態 (`/plc/basic_data/from_plc`) を参照した安全抑制、協調走行時の `/collab/*` への切替、Nav 状態 (`/drive/state`) の受信による状態表示も行う。

## Public ROS 2 API

すべてのトピック名は `ROS_PREFIX` 環境変数がプレフィックスとして付与される。

### Publishers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/except_handl/node/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/error/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/warn/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/error/reset` | `std_msgs/UInt8` | parameters | TODO: エラーリセット |
| `<prefix>/drive/stop` | `std_msgs/Empty` | parameters | TODO: 停止 |
| `<prefix>/drive/estop` | `std_msgs/Empty` | parameters | TODO: 非常停止 |
| `<prefix>/drive/sleep` | `std_msgs/Empty` | parameters | TODO: スリープ |
| `<prefix>/drive/wakeup` | `std_msgs/Empty` | parameters | TODO: 復帰 |
| `<prefix>/drive/run_lifter` | `std_msgs/String` | parameters | TODO: リフタ操作 |
| `<prefix>/drive/set_life_time` | `std_msgs/UInt16` | parameters | TODO: life_time |
| `<prefix>/drive/run_vel` | `triorb_drive_interface/TriorbRunVel3` | sensor_data depth=1 | TODO: 速度指令 |
| `<prefix>/safe_drive/run_vel` | `triorb_drive_interface/TriorbRunVel3` | sensor_data depth=1 | TODO: 安全フィルタ経路の速度指令 |
| `<prefix>/collab/drive/stop` | `std_msgs/Empty` | parameters | TODO |
| `<prefix>/collab/drive/estop` | `std_msgs/Empty` | parameters | TODO |
| `<prefix>/collab/sleep` | `std_msgs/Empty` | parameters | TODO |
| `<prefix>/collab/wakeup` | `std_msgs/Empty` | parameters | TODO |
| `<prefix>/collab/run_lifter` | `std_msgs/String` | parameters | TODO |
| `<prefix>/collab/set_life_time` | `std_msgs/UInt16` | parameters | TODO |
| `<prefix>/collab/run_vel` | `triorb_drive_interface/TriorbRunVel3Stamped` | sensor_data depth=1 | TODO |

### Subscribers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/collab/alive` (topic name TODO) | `std_msgs/Header` | (TODO) | TODO: 協調 alive 監視 |
| `<prefix>/<nav_state topic>` | `std_msgs/Int32MultiArray` | (TODO) | TODO: ナビ状態表示用 |
| `<prefix>/plc/basic_data/from_plc` | `triorb_plc_interface/BasicDataFromPLC` | (TODO) | TODO: PLC 入力（PLC enable 設定時のみ） |
| `<prefix>/drive/state` | `triorb_drive_interface/TriorbRunState` | (TODO) | TODO: ナビ状態受信 |

## Parameters

TODO: joystick デバイスパス、軸/ボタンマッピング、速度スケーリング、PLC 連動有効化などを列挙（`params/` 配下 YAML 参照）。

## Launch / run

```bash
ros2 run triorb_gamepad triorb_gamepad
```

TODO: params yaml / launch ファイル指定を記入。

## Related Packages

- 下流: `triorb_drive_pico`, `triorb_safe_run_cpp`, `triorb_navigation_manager`（各 `/drive/*`, `/collab/*` を subscribe）
- 上流: PLC wrapper (`triorb_sick_plc_wrapper` など)
- インターフェース: `triorb_drive_interface`, `triorb_plc_interface`
