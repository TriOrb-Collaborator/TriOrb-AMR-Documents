# triorb_gpio

GPIO を通じて AMR の外部デバイス（ランプ、ブザー、トリガ等）を制御する Python ノード。

> package.xml `<description>`: "GPIOを通じてAMRの外部デバイス（ランプ・ブザー・トリガ等）を制御するためのノードを提供するパッケージです。"
>
> version: 1.0.0 / maintainer: info@triorb.co.jp
>
> executable(s): `gpio` (entry: `triorb_gpio.gpio:main`)

## Overview

TODO: Jetson GPIO ヘッダのピンを初期化し、`/gpios/set_direction` で入出力方向、`/gpios/set_value` で出力値を設定。入力ピンの現在値を `/gpios/value` に定期配信する。

## Public ROS 2 API

すべてのトピック名は `ROS_PREFIX` 環境変数がプレフィックスとして付与される。

### Publishers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/except_handl/node/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/error/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/warn/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/gpios/value` | `std_msgs/Int8MultiArray` | parameters | TODO: 現在の GPIO 値（配列長 = 管理ピン数） |

### Subscribers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/gpios/set_direction` | `std_msgs/Int8MultiArray` | parameters | TODO: ピン方向設定（0=IN, 1=OUT 等） |
| `<prefix>/gpios/set_value` | `std_msgs/Int8MultiArray` | parameters | TODO: ピン出力値設定 |

## Parameters

TODO: 管理対象ピン番号のリスト、ポーリング周期、デフォルト方向を列挙。

## Launch / run

```bash
ros2 run triorb_gpio gpio
```

TODO: launch file があれば記載。

## Related Packages

- 上流/下流: 外部 HMI（ランプ制御・物理スイッチ読取）
- インターフェース: `std_msgs` のみ
