# triorb_camera_capture

カメラキャプチャ用パッケージ（C++）。`triorb_camera_argus` の再実装または v4l2 ベースの別実装として、実行時に動的に画像トピックを追加・切替できるよう設計されている。

> package.xml `<description>`: "カメラキャプチャーのためのパッケージ"
>
> version: 1.2.0 / maintainer: yano.koichi@triorb.co.jp
>
> executable: `camera_capture`

## Overview

TODO: 起動時に静的にカメラを N 台 open し、`/set/camera/state` service で動的に topic 名を変更/追加可能。`/camera/stacked/image_raw` で連結画像も配信。自動露出は `/set/auto_exposure/enable` / `/set/auto_exposure/vcrop` で制御。

## Public ROS 2 API

すべてのトピック名は `ROS_PREFIX` 環境変数がプレフィックスとして付与される。

### Publishers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/except_handl/node/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/error/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/warn/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/error/camera` | `std_msgs/Empty` | parameters | TODO: カメラ異常通知 |
| `<prefix>/camera/stacked/image_raw` | `sensor_msgs/Image` | sensor_data depth=1 | TODO: 連結画像 |
| `<prefix>/<topic>` (params) | `sensor_msgs/Image` | sensor_data depth=1 | TODO: 各カメラ画像（topic 名パラメータ / 実行時に `SetCameraState` でも追加） |
| `<prefix>/<topic>_device` | `triorb_sensor_interface/CameraDevice` | sensor_data depth=1 | TODO: デバイス情報 |

### Subscribers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/<enable_auto_exposure>` | `std_msgs/Bool` | (TODO) | TODO: 自動露出 on/off（topic 名パラメータ） |
| `<prefix>/<auto_exposure_vcrop>` | `std_msgs/Float32MultiArray` | (TODO) | TODO: 自動露出 vertical crop 領域 |

### Services

| Service | Type | 用途（TODO） |
| --- | --- | --- |
| `<prefix>/get/camera/state` | `triorb_sensor_interface/srv/CameraDevice` | TODO: 現在のカメラ状態取得 |
| `<prefix>/set/camera/state` | `triorb_sensor_interface/srv/CameraCapture` | TODO: カメラ有効化 / topic 切替 |
| `<prefix>/<auto_gain_target>` | `triorb_camera_argus/srv/AutoGainTarget` | TODO: AutoGain ターゲット設定（`triorb_camera_argus` の srv を再利用） |

## Parameters

TODO: カメラ本数、device node マップ、トピック名配列、露出/ゲイン初期値を列挙。`cfg/` 配下の YAML を参照。

## Launch / run

```bash
ros2 launch triorb_camera_capture <launch_file>.launch.py
```

TODO: `launch/` 配下の具体ファイル名を記入。

## Related Packages

- 上流: カメラハードウェア（v4l2）
- 下流: visual_slam、`triorb_camera_calibration`, `triorb_calibration`, UI
- インターフェース: `triorb_sensor_interface`, `triorb_camera_argus`（srv 参照）、`triorb_static_interface`
