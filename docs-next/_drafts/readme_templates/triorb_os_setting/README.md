# triorb_os_setting

ホストコンピューター（Jetson）の設定のためのパッケージ

> version: `0.0.0` / maintainer: TriOrb <info@triorb.co.jp> / license: Apache License, Version 2.0

## Overview

TODO: このパッケージが提供する機能、起動タイミング、関連ノードとの連携を 2–4 文で。

## API Reference

> Source: migrated from the hand-written `API.md` in the submodule.

ホストコンピューター（Jetson）の設定のためのパッケージ

### OS制御、環境設定API
#### 有線ネットワーク設定取得
- Topic：(prefix)/get/os/setting/network/wire
- Node：(prefix)_os_setting
- Type：triorb_static_interface/srv/SettingIPv4
- Usage：
```bash
triorb@orin-nx-XXX:~/$ ros2 service call /get/os/setting/network/wire triorb_static_interface/srv/SettingIPv4
...
response:
triorb_static_interface.srv.SettingIPv4_Response(result=[triorb_static_interface.msg.SettingIPv4(device='eth0', method='auto', adress=[], mask=0, gateway=[], mac=[72, 176, 45, 216, 224, 9])])
```

#### 無線ネットワーク設定取得
- Topic：(prefix)/get/os/setting/network/wifi
- Node：(prefix)_os_setting
- Type：triorb_static_interface/srv/SettingIPv4
- Usage：
```bash
triorb@orin-nx-XXX:~/$ ros2 service call /get/os/setting/network/wifi triorb_static_interface/srv/SettingIPv4
...
response:
triorb_static_interface.srv.SettingIPv4_Response(result=[triorb_static_interface.msg.SettingIPv4(device='wlan0', method='auto', adress=[192, 168, 21, 25], mask=24, gateway=[192, 168, 21, 1], mac=[212, 216, 83, 169, 227, 214])])
```

#### 接続可能なアクセスポイント一覧取得
- Topic：(prefix)/get/os/setting/network/ssid
- Node：(prefix)_os_setting
- Type：triorb_static_interface/srv/SettingSSID
- Usage：
```bash
triorb@orin-nx-XXX:~/$ ros2 service call /get/os/setting/network/ssid triorb_static_interface/srv/SettingSSID 
...
response:
triorb_static_interface.srv.SettingSSID_Response(result=[triorb_static_interface.msg.SettingSSID(ssid='TriOrb-wifi', passphrase='', security='WPA2/WPA3', signal=100), triorb_static_interface.msg.SettingSSID(ssid='KIC-wifi', passphrase='', security='WPA2/WPA3', signal=90), …])
```

#### シャットダウン・再起動
- Topic：(prefix)/os/shutdown
- Node：(prefix)_os_setting
- Type：std_msgs/String
- Note: 即時実行
- Usage：
```bash
triorb@orin-nx-XXX:~/$ ros2 topic pub /os/shutdown std_msgs/String '{data: reboot}'
```

#### ROS環境変数取得
- Topic：(prefix)/get/os/setting/ros
- Node：(prefix)_os_setting
- Type：triorb_static_interface/srv/SettingROS
- Usage：
```bash
triorb@orin-nx-XXX:~/$ ros2 service call /get/os/setting/ros triorb_static_interface/srv/SettingROS
...
response:
triorb_static_interface.srv.SettingROS_Response(result=triorb_static_interface.msg.SettingROS(ros_localhost_only=True, ros_domain_id=0, ros_prefix=''))
```

#### ROS環境変数設定
- Topic：(prefix)/get/os/setting/ros
- Node：(prefix)_os_setting
- Type：triorb_static_interface/msg/SettingROS
- Note: 再起動後に有効化
- Usage：
```bash
triorb@orin-nx-XXX:~/$ ros2 topic pub -1 /os/setting/ros triorb_static_interface/msg/SettingROS '{ros_localhost_only: False, ros_domain_id: 33, ros_prefix: test}'
publisher: beginning loop
publishing #1: triorb_static_interface.msg.SettingROS(ros_localhost_only=False, ros_domain_id=33, ros_prefix='test')
```

#### アクセスポイントへ接続
- Topic：(prefix)/os/setting/network/ssid
- Node：(prefix)_os_setting
- Type：triorb_static_interface/msg/SettingSSID
- Note: 即時反映
- Usage：
```bash
triorb@orin-nx-XXX:~/$ ros2 topic pub -1 /os/setting/network/ssid triorb_static_interface/msg/SettingSSID '{ssid: TriOrb-wifi, passphrase: password}'
triorb@orin-nx-XXX:~/$ nmcli -f ALL dev wifi | grep yes # 確認
```

#### 有線ネットワークの設定を変更
- Topic：(prefix)/os/setting/network/wire
- Node：(prefix)_os_setting
- Type：triorb_static_interface/msg/SettingIPv4
- Note: 即時反映
- Usage：
```bash
triorb@orin-nx-XXX:~/$ ros2 topic pub -1 /os/setting/network/wire triorb_static_interface/msg/SettingIPv4 '{method: manual, adress: [192,168,21,155], mask: 24, gateway: [192,168,21,1]}' # 手動設定
triorb@orin-nx-XXX:~/$ ros2 topic pub -1 /os/setting/network/wire triorb_static_interface/msg/SettingIPv4 '{method: auto}' # 自動取得
triorb@orin-nx-XXX:~/$ ros2 topic pub -1 /os/setting/network/wire triorb_static_interface/msg/SettingIPv4 '{method: shared}' # DHCPサーバー化
```

#### Wi-Fiアクセスポイントを構築する
SSID設定をpublish後に無線ネットワークの設定を'{method: shared}'として設定することでアクセスポイントの構築が出来る
- Note: 即時反映
- Usage：
```bash
triorb@orin-nx-XXX:~/$ ros2 topic pub -1 /os/setting/network/ssid triorb_static_interface/msg/SettingSSID '{ssid: TriOrb-AMR, passphrase: triorb_base}' # SSIDを設定する
triorb@orin-nx-XXX:~/$ ros2 topic pub -1 /os/setting/network/wifi triorb_static_interface/msg/SettingIPv4 '{method: shared}' # APを立てる
triorb@orin-nx-XXX:~/$ ros2 topic pub -1 /os/setting/network/ssid triorb_static_interface/msg/SettingSSID '{ssid: TriOrb-wifi, passphrase: password}' # 元に戻す（数分かかる）
```

### [OS制御、環境設定Types](../TriOrb-ROS2-Types/triorb_static_interface/README.md)

## Related Packages

TODO: 上流・下流の関連パッケージを列挙。
