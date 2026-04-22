# triorb_static_interface

ロボット／ホストの静的情報（ステータス、ネットワーク設定、ノード情報、エラー等）に関わる ROS 2 インターフェース定義パッケージ。

> package.xml の `<description>` は未記入（"TODO: Package description"）。必要に応じて更新してください。
>
> version: 1.0.0 / maintainer: tobata.masakazu@triorb.co.jp

## Interface Summary

| Kind | Name | 用途（記入要） |
| --- | --- | --- |
| msg | ClockSync | TODO: 概要を記入（2 ヘッダによる時計同期） |
| msg | HostStatus | TODO: 概要を記入（ホスト CPU/MEM/WLAN 状態） |
| msg | NodeInfo | TODO: 概要を記入（ROS 2 ノードの状態） |
| msg | RobotError | TODO: 概要を記入（ロボットのエラー） |
| msg | RobotStatus | TODO: 概要を記入（ロボットの動作状態） |
| msg | SettingIPv4 | TODO: 概要を記入（TCP/IPv4 設定） |
| msg | SettingROS | TODO: 概要を記入（ROS 2 環境変数設定） |
| msg | SettingSSID | TODO: 概要を記入（無線 LAN 設定） |
| msg | StringList | TODO: 概要を記入（文字列配列） |
| srv | ErrorList | TODO: 概要を記入（エラー一覧取得） |
| srv | GetImage | TODO: 概要を記入（画像取得） |
| srv | GetString | TODO: 概要を記入（文字列取得） |
| srv | GetStringList | TODO: 概要を記入（文字列リスト取得） |
| srv | NodeInfo | TODO: 概要を記入（ROS 2 ノード情報取得） |
| srv | SetImage | TODO: 概要を記入（画像入力） |
| srv | SetString | TODO: 概要を記入（文字列入力） |
| srv | SettingIPv4 | TODO: 概要を記入（IPv4 設定取得） |
| srv | SettingROS | TODO: 概要を記入（ROS 2 環境設定取得） |
| srv | SettingSSID | TODO: 概要を記入（無線 LAN 設定取得） |
| srv | Version | TODO: 概要を記入（バージョン取得） |

## Messages

### ClockSync

**Fields**:
```
#==時計同期のためのメッセージ==
std_msgs/Header header1     # Header 1
std_msgs/Header header2     # Header 2
```

TODO: header1/header2 の役割（送信時／受信時など）、RTT 計測手順を記入。

### HostStatus

**Fields**:
```
#==ホストコンピューターのモニター==
std_msgs/Header header      # Timestamp
float32 memory_percent      # Memory usage
float32 cpu_percent         # CPU usage
float32 host_temperature    # Temperature of the host computer
string wlan_ssid            # SSID of the access point
uint8 wlan_signal           # Signal strength of the access point
uint32 wlan_freq            # Communication speed of the access point
float32 ping                # Ping speed to the default gateway
uint8[] gateway             # Address of the default gateway
```

TODO: 更新周期、UI ダッシュボードとの対応を記入。

### NodeInfo

**Fields**:
```
#==ROS2ノードの状態==
string name # Node name
string state # Node state ( sleep | wakeup | awake )
```

TODO: state 遷移ルール、NodeInfo.srv との対応を記入。

### RobotError

**Fields**:
```
std_msgs/Header header      # Timestamp
uint8 error                 # error code
```

TODO: error code 一覧／マッピング表への参照を記入（RobotStatus の error bit flag と別物か要注意）。

### RobotStatus

**Fields**:
```
#==ロボットの状態==
std_msgs/Header header  # timestamp
float32 voltage         # main power supply voltage
uint16 btns             # Remote control operation status (bit flag)
uint16 state            # Robot operation state (bit flag)
uint16 error            # Error status of the robot (bit flag)
float32 battery         # Battery level (0.0 - 1.0)
string collab_id        # collab group id (empty: no group)
bool manual_mode        # enable manual drive
bool auto_mode          # enable auto drive

#---Remote control operation status (bit flag)---
# 0x8000: Remote control Y button
# 0x4000: Remote control B button
# 0x2000: Remote control A button
# 0x1000: Remote control X button

#---Robot operation state (bit flag)---
# 0x8000: Motor is being excited
# 0x4000: Accepting move instruction (not implemented)
# 0x2000: Moving
# 0x1000: Self-position recognition in progress
# 0x0800: Generating map (not implemented)
# 0x0400: During anti-collision control (option)
# 0x0200: Position control move completed
# 0x0100: Stopped due to anti-collision control (option)
# 0x0010: Emergency stop is working
# 0x0001: Status obtained successfully

#---Error status of the robot (bit flag)---
# 0x8000: Motor connection error
# 0x4000: IMU and distance sensor connection error
# 0x2000: Camera connection error
# 0x1000: Main power supply voltage abnormal
# 0x0001: Control ECU connection error
```

TODO: publish 周期、主要な subscriber（UI / collaboration）、bit flag の組合せ規約を記入。

### SettingIPv4

**Fields**:
```
#==TCP/IPv4==
string device # device name
string method # device mode: auto | manual | shared | disabled
uint8[] adress # IP adress
uint8 mask # Subnet mask
uint8[] gateway # Default gateway adress
uint8[] mac # Hardware adress
```

TODO: adress 配列長（4）, mask の表現（prefix length か）を記入。`adress` のスペルミス注意。

### SettingROS

**Fields**:
```
#==ROS2環境==
bool ros_localhost_only # ROS_LOCALHOST_ONLY
uint16 ros_domain_id # ROS_DOMAIN_ID
string ros_prefix # ROS_PREFIX
```

TODO: ros_prefix の用途（トピック名前空間）を記入。

### SettingSSID

**Fields**:
```
#==無線LAN設定==
string ssid # Wi-Fi SSID name
string passphrase # Wi-Fi passphrase
string security # Wi-Fi security type
uint8 signal # Signal strength (0-100)
```

TODO: security の取り得る値（WPA2/WPA3 等）、passphrase の取り扱い（ログ抑制）を記入。

### StringList

**Fields**:
```
string[] strings
```

TODO: 汎用ユーティリティ。主な利用先を記入。

## Services

### ErrorList

**Request**:
```
#==[Service] エラー一覧の取得==
std_msgs/Empty request
```

**Response**:
```
RobotError[] errors
```

TODO: 呼び出し元、取得対象（現在有効なエラー vs 履歴）を記入。

### GetImage

**Request**:
```
#==[Service] 画像の取得==
std_msgs/Empty request
```

**Response**:
```
sensor_msgs/Image image
```

TODO: どの画像が返るか（最新フレーム等）、呼び出し元を記入。

### GetString

**Request**:
```
#==[Service] 文字列の取得==
std_msgs/Empty request
```

**Response**:
```
string result
```

TODO: どのノードに実装されるか（例: ロボット名取得など）を記入。

### GetStringList

**Request**:
```
#==[Service] 文字列リストの取得==
std_msgs/Empty request
```

**Response**:
```
string[] result
```

TODO: 取得対象（マップ一覧、ファイル一覧等）を記入。

### NodeInfo

**Request**:
```
#==[Service] ROS2ノード情報の取得==
std_msgs/Empty request
```

**Response**:
```
NodeInfo[] result
```

TODO: どのノードが応答するか（ライフサイクル管理ノード等）を記入。

### SetImage

**Request**:
```
#==[Service] 画像の入力==
sensor_msgs/Image image
```

**Response**:
```
string result
```

TODO: 入力画像の用途（認識サービス等）、result のフォーマットを記入。

### SetString

**Request**:
```
#==[Service] 文字列の入力==
string[] request
```

**Response**:
```
string result
```

TODO: 用途（設定書込み等）、result のフォーマット（成功可否）を記入。

### SettingIPv4

**Request**:
```
#==[Service] TCP/IPv4設定の取得==
std_msgs/Empty request
```

**Response**:
```
SettingIPv4[] result
```

TODO: マルチ NIC 対応（配列）を記入。

### SettingROS

**Request**:
```
#==[Service] ROS2環境設定の取得==
std_msgs/Empty request
```

**Response**:
```
SettingROS result
```

TODO: 呼び出し元を記入。

### SettingSSID

**Request**:
```
#==[Service] 無線LAN設定の取得==
std_msgs/Empty request
```

**Response**:
```
SettingSSID[] result
```

TODO: 配列の意味（複数 SSID プロファイル？）を記入。

### Version

**Request**:
```
#==[Service] Version情報の取得==
std_msgs/Empty request
```

**Response**:
```
uint8[] version
```

TODO: version の符号化（semver bytes / ASCII）を記入。

## Dependencies

- `std_msgs`
- `geometry_msgs`
- `sensor_msgs`

## Related Packages

- TODO: ステータスを publish する `triorb-os` 系ノード
- TODO: 設定／状態を subscribe する UI／モニタリングノード
