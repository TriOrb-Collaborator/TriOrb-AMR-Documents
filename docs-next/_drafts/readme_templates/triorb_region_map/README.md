# triorb_region_map

走行領域・禁止エリア・動的障害物を統合したマップを管理し、ROS / 画像 / OccupancyGrid として配信する C++ ノード。

> package.xml `<description>`: "走行領域や禁止エリアなどのマップ情報を管理し、経路計画向けにJSON/ROSメッセージで提供するユーティリティノードです。"
>
> version: 0.0.2 / maintainer: info@triorb.co.jp
>
> executable: `region_map`

## Overview

TODO: JSON / YAML で与えた領域定義と、距離センサ入力を重ねてマップを構築。`/region/grid_map` (OccupancyGrid) を経路計画用に、`/region/image/compressed` を UI 可視化用に配信。`/vslam/rig_tf` も再配信（座標系）。

## Public ROS 2 API

すべてのトピック名は `ROS_PREFIX` 環境変数がプレフィックスとして付与される。

### Publishers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/except_handl/node/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/error/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/warn/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/region/image/compressed` | `sensor_msgs/CompressedImage` | sensor_data depth=1 | TODO: マップ可視化画像 |
| `<prefix>/region/grid_map` | `nav_msgs/OccupancyGrid` | sensor_data depth=1 | TODO: 占有グリッドマップ（経路計画用） |
| `<prefix>/vslam/rig_tf` | `geometry_msgs/TransformStamped` | sensor_data depth=1 | TODO: VSLAM 座標系 TF の再配信（要確認） |

### Subscribers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/region/load_map` | `sensor_msgs/CompressedImage` | parameters | TODO: マップ画像注入 |
| `<prefix>/sensor/distance` | `triorb_sensor_interface/DistanceSensor` | sensor_data depth=1 | TODO: 距離センサ入力（障害物反映） |

### Services

| Service | Type | 用途（TODO） |
| --- | --- | --- |
| `<prefix>/region/dump` | `std_srvs/Trigger` | TODO: 現在のマップをファイルに保存 |
| `<prefix>/region/freeze` | `std_srvs/SetBool` | TODO: マップ凍結（動的更新停止） |

## Parameters

TODO: マップサイズ、解像度、領域 JSON/YAML ファイルパスを列挙。

## Launch / run

```bash
ros2 run triorb_region_map region_map
```

TODO: マップ JSON / config のパスを示す launch file があれば記載。

## Related Packages

- 上流: `triorb_obstacle_sensor` / 距離センサ系（`/sensor/distance` を publish）
- 下流: `triorb_path_search_server`（`/region/grid_map` を subscribe）、UI（`/region/image/compressed`）
- インターフェース: `triorb_sensor_interface`, `triorb_static_interface`
