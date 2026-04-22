# triorb_dead_reckoning

VSLAM・オドメトリ・IMU を統合し自己位置を推定するデッドレコニングパッケージ。IMU センサ確認用バイパスログ機能も含む。

> package.xml `<description>`: "VSLAM・オドメトリ・IMUを統合し自己位置を推定するデッドレコニングパッケージです。IMUセンサ確認用バイパスログ機能も含みます。"
>
> version: 1.2.0 / maintainer: info@triorb.co.jp
>
> executable(s): `dead_reckoning` (entry: `triorb_dead_reckoning.dead_reckoning:main`)

## Overview

TODO: このノードが提供する機能、起動タイミング、関連ノードとの連携を 2–4 文で記入。IMU シリアル接続・ISAM2 最適化・MQTT 連携の位置付けも要記述。

## Public ROS 2 API

すべてのトピック名は `ROS_PREFIX` 環境変数がプレフィックスとして付与される（例: `<prefix>/triorb/dead_reckoning`）。

### Publishers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/except_handl/node/add` | `std_msgs/String` | parameters | TODO: 例外ハンドラへのノード登録 |
| `<prefix>/triorb/error/str/add` | `std_msgs/String` | parameters | TODO: エラー通知 |
| `<prefix>/triorb/warn/str/add` | `std_msgs/String` | parameters | TODO: 警告通知 |
| `<prefix>/triorb/dead_reckoning` | `geometry_msgs/Vector3Stamped` | depth=1 | TODO: 統合自己位置（x, y, yaw） |
| `<prefix>/triorb/dead_reckoning/speed` | `triorb_drive_interface/TriorbVel3` | depth=1 | TODO: 統合速度 |

### Subscribers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/triorb/odom` | `geometry_msgs/Vector3Stamped` | depth=1 | TODO: 車輪オドメトリ入力 |
| `<prefix>/vslam/rig_tf` | `geometry_msgs/TransformStamped` | sensor_data | TODO: VSLAM 位置入力 |

### Services

| Service | Type | 用途（TODO） |
| --- | --- | --- |
| `<prefix>/get/version/dead_reckoning` | `triorb_static_interface/Version` | TODO: ノードバージョン取得 |

### Upstream dependencies (this node calls/subscribes to)

- subscribes: `triorb_drive_pico` (odometry), `triorb_vslam_tf` / stella_vslam (rig_tf)
- MQTT: `/dead_reckoning/stream`, `/dead_reckoning/debug/{start,end}`, `/dead_reckoning/{vslam,imu}/off` (非 ROS)
- TODO: MQTT Broker 経由で連携するダッシュボード等を記入

## Parameters

- `config` (string) — YAML 設定ファイルパス（必須）
- `mqtt_adress` (string, default `"localhost"`)
- `mqtt_port` (int, default `8083`, WebSocket)
- `mqtt_client_id` (string, default `triorb_dead_reckoning_stream_<random>`)
- `mqtt_topic` (string, default `/dead_reckoning/stream`)
- `mqtt_debug_start_topic`, `mqtt_debug_end_topic`
- `mqtt_vslam_off_topic`, `mqtt_imu_off_topic`
- TODO: YAML 設定内部の IMU ポート / マッピング等を記入

## Launch / run

```bash
ros2 run triorb_dead_reckoning dead_reckoning --ros-args -p config:=<path/to/config.yaml>
```

TODO: 標準の launch file があれば記載。

## Related Packages

- 上流: `triorb_drive_pico`（odom 配信）、VSLAM（`stella_vslam_ros` / `triorb_vslam_tf`）
- 下流: `triorb_navigation`, `triorb_navigation_manager`（dead_reckoning を subscribe）
- インターフェース: `triorb_drive_interface`, `triorb_static_interface`
