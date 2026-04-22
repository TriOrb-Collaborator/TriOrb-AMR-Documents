# triorb_host_info

ホストコンピュータ（Jetson）関連の情報を表示するためのノード（Python）。

> package.xml `<description>`: "ホストコンピューター（Jetson）関連の情報を表示するためのパッケージ"
>
> version: 0.0.0 / maintainer: info@triorb.co.jp
>
> executable(s): `device` (entry: `triorb_host_info.device:main`)

## Overview

TODO: CPU/GPU 温度、メモリ使用量、ディスク使用量、IP アドレス等の Jetson ホスト情報を定期取得し、`/host/status` トピックに配信する。

## Public ROS 2 API

すべてのトピック名は `ROS_PREFIX` 環境変数がプレフィックスとして付与される。

### Publishers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/except_handl/node/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/error/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/warn/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/host/status` | `triorb_static_interface/HostStatus`（要確認） | parameters | TODO: CPU/メモリ/温度/IP 等 |

## Parameters

TODO: 取得周期、項目 on/off フラグを列挙。

## Launch / run

```bash
ros2 run triorb_host_info device
```

## Related Packages

- 下流: 監視 UI（`/host/status` を subscribe）
- インターフェース: `triorb_static_interface` (`HostStatus`)
