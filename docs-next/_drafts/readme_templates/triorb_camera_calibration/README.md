# triorb_camera_calibration

カメラ画像を受信してチェッカーボード検出と内部パラメータ計算を行い、補正結果やリマップ画像を提供する Python ノード。

> package.xml `<description>`: "カメラ画像を受信してチェッカーボード検出と内部パラメータ計算を行い、補正結果やリマップ画像を提供するPythonノードです。"
>
> version: 0.0.0 / maintainer: info@triorb.co.jp
>
> executable(s):
> - `camera_calibration` (entry: `triorb_camera_calibration.camera_calibration:main`)
> - `camera_remap` (entry: `triorb_camera_calibration.camera_remap:main`)

## Overview

TODO: 2 つの実行ファイル。`camera_calibration` はチェッカーボード検出 → 内部パラメータ算出、`camera_remap` は算出したパラメータで `/camera0..4` を undistort して `/camera` に再配信する。`triorb_calibration` (C++) との使い分けを記入。

## Public ROS 2 API

> 注: このパッケージのトピック名は `ROS_PREFIX` を明示的には付加せず絶対名を用いる (`/camera0` 等)。要確認。

### `camera_calibration`

#### Publishers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/except_handl/node/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/error/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/warn/str/add` | `std_msgs/String` | parameters | TODO |
| `/calib` | `sensor_msgs/Image` | best_effort depth=1 | TODO: チェッカーボード検出結果画像 |
| `/calib_result` | `std_msgs/Float32MultiArray` | parameters | TODO: camera_matrix / distortion 配列 |

#### Subscribers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `/camera0` | `sensor_msgs/Image` | best_effort depth=1 | TODO: 入力画像 |
| `/trig_intrinsic` | `std_msgs/Bool` | parameters | TODO: 検出開始/停止トリガ |

### `camera_remap`

#### Publishers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `/camera` | `sensor_msgs/Image` | best_effort depth=1 | TODO: undistort 後の統合出力 |

#### Subscribers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `/camera0`–`/camera4` | `sensor_msgs/Image` | best_effort depth=1 | TODO: 各カメラ入力 |
| `/remap` | `std_msgs/UInt8` | best_effort depth=1 | TODO: 選択カメラインデックス |

## Parameters

TODO: チェッカーボードサイズ、出力 YAML パス等を列挙。

## Launch / run

```bash
ros2 run triorb_camera_calibration camera_calibration
ros2 run triorb_camera_calibration camera_remap
```

TODO: launch ファイルがあれば記載。

## Related Packages

- 上流: `triorb_camera_argus`, `triorb_camera_capture`（`/camera0..4` を publish）
- 下流: TODO（`/calib_result` の consumer を確認）
- インターフェース: `triorb_sensor_interface`, `triorb_static_interface`
