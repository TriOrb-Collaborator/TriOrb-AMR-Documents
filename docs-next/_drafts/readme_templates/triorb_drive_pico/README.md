# triorb_drive_pico

ROS 2 メッセージを用いてモーター制御 ECU (Pico) と通信するためのドライバパッケージ。

> package.xml `<description>`: "ROS2メッセージを用いてモーター制御ECUと通信するためのパッケージ"
>
> version: 1.2.0 / maintainer: info@triorb.co.jp
>
> executable(s): `drive` (entry: `triorb_drive_pico.drive:main`)

## Overview

TODO: Pico (モーター制御 ECU) とのシリアル/CAN 通信、速度・位置指令のパススルー、オドメトリと状態の ROS 2 配信を担う中核ノード。起動タイミングと依存ノード（`triorb_navigation`, `triorb_gamepad` 等）との関係を 2–4 文で記入。

## Public ROS 2 API

すべてのトピック名は `ROS_PREFIX` 環境変数がプレフィックスとして付与される。

### Publishers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/except_handl/node/add` | `std_msgs/String` | parameters | TODO: 例外ハンドラへのノード登録 |
| `<prefix>/triorb/error/str/add` | `std_msgs/String` | parameters | TODO: エラー通知 |
| `<prefix>/triorb/warn/str/add` | `std_msgs/String` | parameters | TODO: 警告通知 |
| `<prefix>/robot/status` | `triorb_static_interface/RobotStatus` | parameters | TODO: ロボット全体状態 |
| `<prefix>/drive/max_vel` | `triorb_drive_interface/RobotParams` | best_effort depth=1 | TODO: 最大速度通知 |
| `<prefix>/triorb/version/drive` | `std_msgs/String` | depth=1 | TODO: drive ノードバージョン |
| `<prefix>/triorb/version/pico` | `std_msgs/String` | depth=1 | TODO: Pico FW バージョン |
| `<prefix>/triorb/version/core` | `std_msgs/String` | depth=1 | TODO: core バージョン |
| `<prefix>/drive/mode` | `std_msgs/String` | best_effort depth=1 | TODO: 現在の drive mode |
| `<prefix>/lifter/state` | `std_msgs/String` | parameters | TODO: リフタ状態 |
| `<prefix>/lifter/result` | `std_msgs/String` | parameters | TODO: リフタ動作結果 |
| `<prefix>/drive/run_pos/result` | `std_msgs/String` | parameters | TODO: 位置移動結果 |
| `<prefix>/mutex/mode_switch` | `std_msgs/Empty` | parameters | TODO: mutex モード切替通知 |
| `<prefix>/robot/vel_level` | `std_msgs/UInt8` | parameters | TODO: 速度レベル通知 |
| `<prefix>/robot/lifter_state` | `std_msgs/UInt8` | parameters | TODO: リフタ状態（数値表現） |
| `<prefix>/triorb/odom` | `geometry_msgs/Vector3Stamped` | parameters | TODO: 車輪オドメトリ出力 |
| `<prefix>/drive/pause` | `std_msgs/Empty` | parameters | TODO: navigate への pause 通知（再配信） |

### Subscribers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/drive/stop` | `std_msgs/Empty` | parameters | TODO: 停止指令 |
| `<prefix>/drive/pause` | `std_msgs/Empty` | parameters | TODO: 一時停止 |
| `<prefix>/drive/run_pos` | `triorb_drive_interface/TriorbRunPos3` | parameters | TODO: 位置指令 |
| `<prefix>/drive/run_vel` | `triorb_drive_interface/TriorbRunVel3` | best_effort depth=1 | TODO: 速度指令 |
| `<prefix>/drive/sleep` | `std_msgs/Empty` | parameters | TODO: モータースリープ |
| `<prefix>/drive/wakeup` | `std_msgs/Empty` | parameters | TODO: モーター復帰 |
| `<prefix>/drive/run_lifter` | `std_msgs/String` | parameters | TODO: リフタ操作コマンド |
| `<prefix>/drive/set_life_time` | `std_msgs/UInt16` | parameters | TODO: 速度指令のライフタイム |
| `<prefix>/mutex/set_drive_mode` | `std_msgs/UInt8` | parameters | TODO: drive mode 切替 |
| `<prefix>/triorb/error/num` | `std_msgs/UInt8` | best_effort depth=1 | TODO: エラー番号入力 |
| `<prefix>/error/camera` | `std_msgs/Empty` | parameters | TODO: カメラ異常通知 |
| `<prefix>/error/sensor` | `std_msgs/Empty` | parameters | TODO: センサ異常通知 |
| `<prefix>/set/robot/vel_level` | `std_msgs/UInt8` | parameters | TODO: 速度レベル入力 |
| `<prefix>/run_slam/status` | `triorb_slam_interface/SlamStatus` | parameters | TODO: SLAM 状態 |
| `<prefix>/drive/state` | `triorb_drive_interface/TriorbRunState` | parameters | TODO: ナビ状態入力 |
| `<prefix>/tagslam/drive/state` | `triorb_drive_interface/TriorbRunState` | parameters | TODO: TagSLAM ナビ状態 |
| `<prefix>/drive/manual_mode` | `std_msgs/Bool` | best_effort depth=1 | TODO: 手動モード切替 |
| `<prefix>/drive/auto_mode` | `std_msgs/Bool` | best_effort depth=1 | TODO: 自動モード切替 |
| `<prefix>/drive/reboot_test` | `std_msgs/Empty` | parameters | TODO: 再起動テスト |
| `<prefix>/battery/status` | `triorb_sensor_interface/BatteryStatus` | best_effort depth=1 | TODO: バッテリ情報 |
| `<prefix>/collab/alive` | `std_msgs/Header` | parameters | TODO: 協調 alive 監視 |
| `<prefix>/set/motor/params` | `triorb_drive_interface/MotorParams` | parameters | TODO: モーターパラメータ設定 |
| `<prefix>/set/motor/torque` | `std_msgs/Float32` | parameters | TODO: モータートルク設定 |
| `<prefix>/set/robot/center` | `triorb_drive_interface/TriorbPos3` | best_effort depth=1 | TODO: ロボット重心/ホイールベース設定 |

### Services

| Service | Type | 用途（TODO） |
| --- | --- | --- |
| `<prefix>/srv/drive/sleep` | `std_srvs/Empty` | TODO: モータースリープ同期要求 |
| `<prefix>/srv/drive/wakeup` | `std_srvs/Empty` | TODO: モーター復帰同期要求 |
| `<prefix>/srv/drive/run_pos` | `triorb_drive_interface/SrvTriorbRunPos3` | TODO: 位置指令同期要求 |
| `<prefix>/srv/drive/run_vel` | `triorb_drive_interface/SrvTriorbRunVel3` | TODO: 速度指令同期要求 |
| `<prefix>/get/motor/status` | `triorb_drive_interface/SrvMotorStatus` | TODO: モーター状態取得 |
| `<prefix>/get/error/history` | `triorb_static_interface/ErrorList` | TODO: エラー履歴取得 |

## Parameters

- `config` (string) — TODO: Pico シリアルポート・PID ゲイン等を含む YAML 設定ファイルパス

TODO: 他に `declare_parameter` された項目があれば追記。

## Launch / run

```bash
ros2 run triorb_drive_pico drive --ros-args -p config:=<path/to/config.yaml>
```

TODO: 標準 launch file があれば記載。

## Related Packages

- 上流: `triorb_navigation`, `triorb_safe_run_cpp`, `triorb_gamepad`, `triorb_socket`（速度/位置指令を publish）
- 下流: `triorb_dead_reckoning`（`/triorb/odom` を subscribe）、`triorb_navigation_manager`（result を subscribe）
- インターフェース: `triorb_drive_interface`, `triorb_static_interface`, `triorb_sensor_interface`, `triorb_slam_interface`
