# triorb_path_search_server

占有マップや経由地情報から走行経路を計算し、ナビゲーション用の Path/Route を返す経路探索サーバーノード。

> package.xml `<description>`: "占有マップや経由地情報から走行経路を計算し、ナビゲーション用のPath/Routeを返す経路探索サーバーノードです。"
>
> version: 0.0.0 / maintainer: info@triorb.co.jp
>
> executable(s): `PathSearch_Server` (entry: `triorb_path_search_server.PathSearch_Server:main`)

## Overview

TODO: `triorb_region_map` が生成する `/region/grid_map` (OccupancyGrid) を subscribe し、`/global_path` サービス呼び出しに対して経路を返す。利用アルゴリズム（A*, Dijkstra 等）と呼び出し元を 2–4 文で記入。

## Public ROS 2 API

すべてのトピック名は `ROS_PREFIX` 環境変数がプレフィックスとして付与される。

### Publishers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/except_handl/node/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/error/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/warn/str/add` | `std_msgs/String` | parameters | TODO |

### Subscribers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/region/grid_map` | `nav_msgs/OccupancyGrid` | best_effort depth=1 | TODO: 占有グリッドマップ入力（`triorb_region_map` 配信） |

### Services

| Service | Type | 用途（TODO） |
| --- | --- | --- |
| `<prefix>/global_path` | `triorb_drive_interface/GetPath`（要確認） | TODO: 経路探索リクエスト（start, goal, 制約 → Path 応答） |

## Parameters

TODO: A* のコストパラメータ、探索グリッド解像度等があれば列挙。

## Launch / run

```bash
ros2 run triorb_path_search_server PathSearch_Server
```

TODO: launch file / config があれば追記。

## Related Packages

- 上流: `triorb_region_map`（OccupancyGrid 配信）
- 下流: `triorb_navigation_manager`（`/global_path` を call）
- インターフェース: `triorb_drive_interface`（GetPath service）、`triorb_static_interface`
