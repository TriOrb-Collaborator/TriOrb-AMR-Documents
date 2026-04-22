# triorb_camera_argus

Jetson の Argus API 経由で複数カメラ映像を取得し、回転補正やデバイス割当を行って画像トピックとして配信する C++ ノード。`AutoGainTarget.srv` の自パッケージ定義も含む (`rosidl_default_generators`)。

> package.xml `<description>`: "JetsonのArgus API経由で複数カメラ映像を取得し、回転補正やデバイス割当を行って画像トピックとして配信するノードです。"
>
> version: 0.0.0 / maintainer: info@triorb.co.jp
>
> executable: `triorb_camera_argus_node`

## Overview

TODO: Argus で最大 N 台のカメラをオープンし、各カメラに対して `/camera<idx>/image_raw`（またはパラメータ由来の topic）と `<topic>_device` を配信。stacked 画像も `/camera/stacked/image_raw` として配信する。設定される出力トピック群はパラメータファイル (`topic_str_` 配列) に依存。

## Public ROS 2 API

すべてのトピック名は `ROS_PREFIX` 環境変数がプレフィックスとして付与される。

### Publishers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/except_handl/node/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/error/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/warn/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/error/camera` | `std_msgs/Empty` | parameters | TODO: カメラ異常検知時のトリガ |
| `<prefix>/camera/stacked/image_raw` | `sensor_msgs/Image` | sensor_data depth=1 | TODO: 全カメラ垂直/水平連結画像 |
| `<prefix>/<topic_str_[i]>` (i=0..N-1) | `sensor_msgs/Image` | sensor_data depth=1 | TODO: 各カメラ画像（トピック名は `topic_str_` パラメータで指定） |
| `<prefix>/<topic_str_[i]>_device` | `triorb_sensor_interface/CameraDevice` | sensor_data depth=1 | TODO: 各カメラのデバイス情報（device node, idx） |

### Services

| Service | Type | 用途（TODO） |
| --- | --- | --- |
| `<prefix>/get/version/<node_name>` | `triorb_static_interface/Version` | TODO: バージョン取得 |
| `<prefix>/<auto_gain_target>` | `triorb_camera_argus/srv/AutoGainTarget` | TODO: 自動ゲイン目標値設定（このパッケージで定義） |

## Parameters

TODO: カメラ本数、`topic_str_` 配列、回転角、露出モード、gamma、gain 等を列挙。

## Launch / run

```bash
ros2 run triorb_camera_argus triorb_camera_argus_node
```

TODO: `/opt/triorb/...` 配下等の config パスと launch ファイル。

## Related Packages

- 上流: なし（Jetson Argus ハードウェア直叩き）
- 下流: `triorb_camera_capture`, `triorb_camera_calibration`, `triorb_calibration`, visual_slam（`/camera*` を subscribe）
- インターフェース: `triorb_sensor_interface`, `triorb_static_interface`, （自パッケージの `srv/AutoGainTarget`）
