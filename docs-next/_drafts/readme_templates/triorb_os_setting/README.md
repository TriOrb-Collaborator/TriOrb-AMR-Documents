# triorb_os_setting

ホストコンピュータ（Jetson）の OS 設定を ROS 2 経由で読み書きするためのパッケージ（Python）。ネットワーク・ROS 環境変数・シャットダウンを扱うサブノード群を含む。

> package.xml `<description>`: "ホストコンピューター（Jetson）の設定のためのパッケージ"
>
> version: 0.0.0 / maintainer: info@triorb.co.jp
>
> executable(s): `os_setting` (entry: `triorb_os_setting.os_setting:main`)
>
> 内部モジュール: `os_setting_nw.py` (ネットワーク), `os_setting_ros.py` (ROS 環境変数), `os_setting_shutdown.py` (シャットダウン)

## Overview

TODO: `os_setting` 単一プロセスが複数のサブノードを起動し、有線/無線ネットワーク設定、SSID/パスフレーズ設定、ROS_DOMAIN_ID 等の環境変数、シャットダウン要求を ROS 2 API として公開する。

## Public ROS 2 API

> 注: トピック名は `ROS_PREFIX` 環境変数が付与される（`get_topic_name` 相当を直接 `os.getenv('ROS_PREFIX', '') + <path>` で構成）。

### Publishers (main `os_setting` ノード)

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/except_handl/node/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/error/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/warn/str/add` | `std_msgs/String` | parameters | TODO |

### Network サブノード (`os_setting_nw`)

#### Subscribers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/os/setting/network/wire` | `triorb_static_interface/MsgSettingIPv4`（推定） | parameters | TODO: 有線 IPv4 設定 |
| `<prefix>/os/setting/network/wifi` | `triorb_static_interface/MsgSettingIPv4`（推定） | parameters | TODO: 無線 IPv4 設定 |
| `<prefix>/os/setting/network/ssid` | `triorb_static_interface/MsgSettingSSID`（推定） | parameters | TODO: SSID / passphrase 設定 |

#### Services

| Service | Type | 用途（TODO） |
| --- | --- | --- |
| `<prefix>/get/os/setting/network/wire` | `triorb_static_interface/SrvSettingIPv4` | TODO |
| `<prefix>/get/os/setting/network/wifi` | `triorb_static_interface/SrvSettingIPv4` | TODO |
| `<prefix>/get/os/setting/network/ssid` | `triorb_static_interface/SrvSettingSSID` | TODO |

### ROS 環境変数サブノード (`os_setting_ros`)

#### Subscribers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/os/setting/ros` | `triorb_static_interface/MsgSettingROS` | parameters | TODO: ROS_DOMAIN_ID 等 |

#### Services

| Service | Type | 用途（TODO） |
| --- | --- | --- |
| `<prefix>/get/os/setting/ros` | `triorb_static_interface/SrvSettingROS` | TODO: 現在値取得 |

### Shutdown サブノード (`os_setting_shutdown`)

#### Subscribers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/os/shutdown` | `std_msgs/String` | parameters | TODO: `"shutdown"` / `"reboot"` 等のコマンド受信 |

## Parameters

TODO: サブノード毎の有効化フラグ、設定ファイルパスを列挙。

## Launch / run

```bash
ros2 run triorb_os_setting os_setting
```

TODO: launch file / systemd 常駐設定。

## Related Packages

- 上流: UI / Web フロント（設定投入）
- 下流: なし（実 OS 設定ファイルを書き換える）
- インターフェース: `triorb_static_interface`（`MsgSettingIPv4`, `MsgSettingSSID`, `MsgSettingROS`, `SrvSettingIPv4`, `SrvSettingSSID`, `SrvSettingROS`）
