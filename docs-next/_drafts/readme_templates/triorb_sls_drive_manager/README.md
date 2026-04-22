# triorb_sls_drive_manager

SICK SLS（Safety Laser Scanner）用ドライバマネージャ（Python）。SLS のブレーキ状態や監視フィールド切替を drive 系に連動させ、速度制限を適用する。

> package.xml `<description>`: "SICK SLS用ドライバマネージャ"
>
> version: 1.2.0 / maintainer: info@triorb.co.jp
>
> executable(s): `sls_drive_manager` (entry: `triorb_sls_drive_manager.sls_drive_manager:main`)

## Overview

TODO: EtherNet/IP (pycomm3) 経由で SLS と通信し、`/sls/set/brake` / `/sls/set/field` を受けて SLS に反映、SLS の状態を `/sls/info/*` として ROS 側に通知する。`triorb_drive_vector` 出力を参照して速度制限要否を判断し、必要時に `/drive/pause` / `/drive/wakeup` / `/drive/restart`（それぞれ現行ソースでは pause/wakeup/restart に相当する publisher 変数）をトリガ。

## Public ROS 2 API

すべてのトピック名は `ROS_PREFIX` 環境変数がプレフィックスとして付与される。

### Publishers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/except_handl/node/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/error/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/warn/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/<pause topic>` | `std_msgs/Empty`（推定） | (TODO) | TODO: drive pause 指令（topic 名要確認） |
| `<prefix>/<wakeup topic>` | `std_msgs/Empty`（推定） | (TODO) | TODO: drive wakeup 指令 |
| `<prefix>/<restart topic>` | `std_msgs/Empty`（推定） | (TODO) | TODO: drive restart 指令 |
| `<prefix>/<speed_limited topic>` | (TODO) | (TODO) | TODO: 速度制限通知 |
| `<prefix>/sls/info/field` | `std_msgs/UInt8` | parameters | TODO: 現在の監視フィールド |
| `<prefix>/sls/info/state` | `std_msgs/UInt16` | parameters | TODO: SLS 状態コード |

### Subscribers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/<set_pos topic>` | (TODO) | (TODO) | TODO: 位置設定入力 |
| `<prefix>/drive/std_vector2` | `std_msgs/Float32MultiArray`（推定） | (TODO) | TODO: 進行方向ベクトル |
| `<prefix>/robot/status` | `triorb_static_interface/RobotStatus`（推定） | (TODO) | TODO: ロボット状態 |
| `<prefix>/sls/set/brake` | `std_msgs/Bool` | depth=1 | TODO: ブレーキ指示（navigation_manager 発） |
| `<prefix>/sls/set/field` | `std_msgs/UInt8` | depth=1 | TODO: 監視フィールド切替指示 |

### Services

| Service | Type | 用途（TODO） |
| --- | --- | --- |
| `<prefix>/get/version/sls_drive_manager` | `triorb_static_interface/Version` | TODO |

## Parameters

TODO: SLS の IP アドレス、EIP タグ名、フィールド切替マップ等を列挙。

## Launch / run

systemd サービス `triorb-sls-drive-manager.service` として起動される前提。

```bash
ros2 run triorb_sls_drive_manager sls_drive_manager
# or
sudo systemctl start triorb-sls-drive-manager
```

TODO: `install_sls_drive_manager.sh`, `run_sls_drive_manager.sh` の役割を明記。

## Related Packages

- 上流: `triorb_navigation_manager`（`/sls/set/*` publish）、`triorb_drive_vector`
- 下流: `triorb_drive_pico`（pause/wakeup/restart）、UI（`/sls/info/*`）
- インターフェース: `triorb_sensor_interface`, `triorb_static_interface`
- 外部ライブラリ: `pycomm3`（EtherNet/IP）
