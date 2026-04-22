# triorb_snr_mux_driver

SNR-MUX ボードとシリアル通信し、音声再生状態・発進待ち時間などを ROS 2 トピックへ配信するドライバ。navigate / navigation_manager の停止・一時停止の遅延を音声再生と連動させる。

> package.xml `<description>`: "SNR-MUXボードとシリアル通信し、音声再生状態・発進待ち時間などを ROS 2 トピックへ配信するドライバです。navigate / navigation_manager の停止・一時停止の遅延を音声再生と連動させます。"
>
> version: 1.2.3 / maintainer: info@triorb.co.jp
>
> executable(s): `snr_mux_driver` (entry: `triorb_snr_mux_driver.snr_mux_driver:main`)

## Overview

TODO: SNR-MUX (音声再生 / ブザー / 発進遅延タイマ) とのシリアル接続を管理し、robot status / drive vector / PLC 状態 / battery を集約して音声トリガを決定、`/snr_mux/info` として各種ノードへ通知する。

## Public ROS 2 API

すべてのトピック名は `ROS_PREFIX` 環境変数がプレフィックスとして付与される。

### Publishers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/except_handl/node/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/error/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/warn/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/snr_mux/info` | `std_msgs/String` | sensor_data | TODO: 再生状態 / 発進待ち時間等を含む JSON 文字列 |

### Subscribers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/drive/std_vector2` | `std_msgs/Float32MultiArray` | sensor_data | TODO: 進行方向ベクトル（`triorb_drive_vector` 配信） |
| `<prefix>/collab/drive/std_vector2` | `std_msgs/Float32MultiArray` | sensor_data | TODO: 協調進行方向ベクトル |
| `<prefix>/aux/event` | `std_msgs/String` | parameters | TODO: ナビマネージャからの補助イベント（音声トリガ） |
| `<prefix>/bc/collab/aux/event` | `std_msgs/String` | parameters | TODO: 協調補助イベント |
| `<prefix>/robot/status` | `triorb_static_interface/RobotStatus` | parameters | TODO: ロボット状態（エラー色等） |
| `<prefix>/plc/basic_data/from_plc` | `triorb_plc_interface/BasicDataFromPLC` | sensor_data | TODO: PLC 基本状態 |
| `<prefix>/plc/app_data/from_plc` | `triorb_plc_interface/AppDataFromPLC` | sensor_data | TODO: PLC アプリデータ |
| `<prefix>/plc/estop_detail/from_plc` | `triorb_plc_interface/EstopDetailFromPLC` | sensor_data | TODO: PLC 非常停止詳細 |
| `<prefix>/battery/status` | `triorb_sensor_interface/BatteryStatus` | sensor_data | TODO: バッテリ残量 |
| `<prefix>/triorb_safe_run/decelerating` | `std_msgs/Bool` | sensor_data | TODO: 安全減速状態 |
| `<prefix>/triorb/amr_pkg_restart/request` | `std_msgs/Empty` | parameters | TODO: AMR パッケージ再起動要求 |

### Services

| Service | Type | 用途（TODO） |
| --- | --- | --- |
| `<prefix>/get/version/snr_mux_driver` | `triorb_static_interface/Version` | TODO: バージョン取得 |

## Parameters

TODO: シリアルポート、音声テーブル、発進遅延時間等の YAML 設定。

## Launch / run

```bash
ros2 run triorb_snr_mux_driver snr_mux_driver
```

TODO: launch file と config YAML のパスを記入。

## Related Packages

- 上流: `triorb_drive_vector`, `triorb_navigation_manager`, PLC wrapper, `triorb_safe_run_cpp`, バッテリ監視系
- 下流: `triorb_navigation`, `triorb_navigation_manager`（`/snr_mux/info` を subscribe）
- インターフェース: `triorb_plc_interface`, `triorb_sensor_interface`, `triorb_static_interface`
