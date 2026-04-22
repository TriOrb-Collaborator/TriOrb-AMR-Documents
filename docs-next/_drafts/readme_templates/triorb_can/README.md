# triorb_can

SocketCAN を用いて CAN バスと ROS 2 トピック（`/can_bridge/rx`, `/can_bridge/tx`）を相互接続するブリッジパッケージ（C++）。

> package.xml `<description>`: "SocketCANを用いてCANバスとROS 2トピック（/can_bridge/rx, /can_bridge/tx）を相互接続するブリッジパッケージです。"
>
> version: 1.2.3 / maintainer: info@triorb.co.jp
>
> executable: `can_bridge`

## Overview

TODO: 設定された CAN インターフェース名 (`can0` 等) を open し、受信フレームを `/<rx_topic>` に publish、`/<tx_topic>` から受信したメッセージを CAN 送信する。

## Public ROS 2 API

すべてのトピック名は `ROS_PREFIX` 環境変数がプレフィックスとして付与される。実際のトピック名は `rx_topic_` / `tx_topic_` パラメータから取得。

### Publishers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/except_handl/node/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/error/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/warn/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/<rx_topic>` (default `/can_bridge/rx`) | `triorb_sensor_interface/CanFrame` | sensor_data depth=1 | TODO: CAN 受信フレーム |

### Subscribers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/<tx_topic>` (default `/can_bridge/tx`) | `triorb_sensor_interface/CanFrame` | (TODO) | TODO: CAN 送信用フレーム入力 |

## Parameters

- `rx_topic` (string) — TODO: 受信側トピック名
- `tx_topic` (string) — TODO: 送信側トピック名
- TODO: CAN インターフェース名、bitrate 等

## Launch / run

```bash
ros2 run triorb_can can_bridge
```

TODO: launch file があれば記載。

## Related Packages

- 上流/下流: `triorb_battery_info`（`/can_bridge/rx` を subscribe）、その他 CAN 機器ドライバ
- インターフェース: `triorb_sensor_interface` (CanFrame), `triorb_static_interface`
