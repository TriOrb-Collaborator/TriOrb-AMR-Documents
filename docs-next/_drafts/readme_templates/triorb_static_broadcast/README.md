# triorb_static_broadcast

ロボットの基本フレーム間（base_link, camera, imu 等）の固定変換を TF2 静的 TF として送出する C++ ノード。

> package.xml `<description>`: "ロボットの基本フレーム間の固定変換をTFとして送出する静的ブロードキャストノードです。"
>
> version: 1.1.0 / maintainer: info@triorb.co.jp
>
> executable: `triorb_tf_static`

## Overview

TODO: 設定 YAML / パラメータから `StaticTransformBroadcaster` で各種 TF を送出。起動直後に一度だけ publish される性質を記載。

## Public ROS 2 API

### Publishers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/except_handl/node/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/error/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/warn/str/add` | `std_msgs/String` | parameters | TODO |
| `/tf_static` | `tf2_msgs/TFMessage` | static (latched) | 固定 TF（`tf2_ros::StaticTransformBroadcaster` 経由） |

## Parameters

TODO: 静的 TF の定義（親/子フレーム名、translation, rotation）を与える YAML / パラメータを列挙。

## Launch / run

```bash
ros2 run triorb_static_broadcast triorb_tf_static
```

TODO: launch file / YAML のパスを記入。

## Related Packages

- 下流: TF2 を購読する全ノード（`triorb_navigation`, `triorb_dead_reckoning`, visual_slam など）
- インターフェース: 直接の msg/srv 依存は `std_msgs` / `geometry_msgs` のみ
