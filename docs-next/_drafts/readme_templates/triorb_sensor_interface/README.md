# triorb_sensor_interface

センサ関連（バッテリー、カメラ、CAN、距離センサ、IMU、障害物）の ROS 2 インターフェース定義パッケージ。

> package.xml の `<description>` は未記入（"TODO: Package description"）。必要に応じて更新してください。
>
> version: 1.0.0 / maintainer: tobata.masakazu@triorb.co.jp

## Interface Summary

| Kind | Name | 用途（記入要） |
| --- | --- | --- |
| msg | BatteryModuleStatus | TODO: 概要を記入（モジュール単位のバッテリー状態） |
| msg | BatteryStatus | TODO: 概要を記入（バッテリー全体の状態） |
| msg | CameraDevice | TODO: 概要を記入（カメラデバイスの定義／状態） |
| msg | CanFrame | TODO: 概要を記入（CAN フレーム） |
| msg | DistanceSensor | TODO: 概要を記入（距離センサ計測値） |
| msg | ImuSensor | TODO: 概要を記入（IMU 姿勢値） |
| msg | Obstacles | TODO: 概要を記入（前後左右の障害物距離） |
| srv | CameraCapture | TODO: 概要を記入（カメラキャプチャ指示） |
| srv | CameraDevice | TODO: 概要を記入（カメラ一覧取得） |
| srv | GetDistanceSensor | TODO: 概要を記入（距離センサ一覧取得） |
| srv | SetDistanceSensor | TODO: 概要を記入（距離センサの状態設定） |
| action | CameraCalibrationInternal | TODO: 概要を記入（カメラ内部パラメータ校正） |

## Messages

### BatteryModuleStatus

**Fields**:
```
# モジュール単位のバッテリー状態

uint8 module_id                 # モジュールID（1,2,...）

float32 voltage_v               # モジュール電圧 [V]

# モジュール電流 [A]
# 符号ルール:
#   充電 = +（プラス）
#   放電 = -（マイナス）
float32 current_a
```

TODO: モジュール構成数、publish 元（BMS ドライバノード）、サンプリング周期を記入。

### BatteryStatus

**Fields**:
```
std_msgs/Header header          # header.stamp: 計測/受信時刻
                                # header.frame_id: 任意（例 "battery"）

uint32 remaining_mah            # 現在の残量 [mAh]
float32 remaining_percent       # 残容量 [%] (0.0〜100.0)
float32 total_voltage_v         # バッテリー全体電圧 [V]
bool is_charging                # 充電Flag
BatteryModuleStatus[] modules
```

TODO: publish トピック名、更新周期、low-battery 判定閾値との関係を記入。

### CameraDevice

**Fields**:
```
#==カメラデバイス==
std_msgs/Header header      # Timestamp
string device               # Path of camera device
string topic                # Topic name of camera image
string id                   # Frame ID of the camera image topic
string state                # Camera device status (sleep | wakeup | awake)
int16 rotation              # Rotation of the camera image
int16 exposure              # Camera Exposure
float32 gamma               # Gamma correction value
float32 timer               # Data collection cycle [s]
```

TODO: 利用場面（Capture サービスの引数・戻り値としての使い方）、state 遷移を記入。

### CanFrame

**Fields**:
```
uint32 id
bool is_rtr
bool is_extended
bool is_error
uint8 dlc
uint8[8] data
```

TODO: どの CAN バスに流れるか、publish/subscribe するノード、解釈規約を記入。

### DistanceSensor

**Fields**:
```
#==距離センサ==
std_msgs/Header header      # Timestamp
float32 distance            # Distance to obstacle [m]
uint8 confidence            # Signal reliability (0-100)
float32 hfov                # Horizontal detectable angle [deg]
float32 vfov                # Vertical detectable angle [deg]
float32 max_dist            # Maximum detectable distance [m]
float32 min_dist            # Minimum detectable distance [m]
float32[] mount_xyz         # Mounting location [m]
float32[] mount_ypr         # Mounting orientation [deg]
```

TODO: ToF／超音波等のセンサ種別、座標系（base_link 相対か）、周期を記入。

### ImuSensor

**Fields**:
```
#==IMUセンサ==
std_msgs/Header header # Timestamp
float32 yaw
float32 pitch
float32 roll
```

TODO: 角度単位（deg / rad）と符号規約、publish 元ノードを記入。

### Obstacles

**Fields**:
```
#==障害物==
std_msgs/Header header      # Timestamp
float32 forward             # Distance to obstacle in forward [m]
float32 left                # Distance to obstacle in left [m]
float32 right               # Distance to obstacle in right [m]
float32 back                # Distance to obstacle in back [m]
```

TODO: 距離センサ群を集約するノード、障害物なし時の値（inf / 0 / max_dist）を記入。

## Services

### CameraCapture

**Request**:
```
#==[Service] カメラキャプチャ指示==
CameraDevice[] request
```

**Response**:
```
string[] result
```

TODO: 呼び出し元、result の意味（パス／ステータス文字列）、エラー条件を記入。

### CameraDevice

**Request**:
```
#==[Service] カメラキャプチャ一覧の取得==
std_msgs/Empty request
```

**Response**:
```
CameraDevice[] result
```

TODO: 一覧化対象（接続済のカメラ vs 設定ファイル定義）を記入。

### GetDistanceSensor

**Request**:
```
#==[Service] 距離センサ一覧の取得==
std_msgs/Empty request
```

**Response**:
```
string[] topic  # List of topic name
string[] state  # List of sensor state ( sleep | wakeup | awake )
```

TODO: 呼び出し元、topic と state の対応（同インデックス）を記入。

### SetDistanceSensor

**Request**:
```
#==[Service] 距離センサの設定指示==
string[] topic  # List of topic name
string[] state  # List of sensor state ( sleep | wakeup | awake )
```

**Response**:
```
string[] result
```

TODO: 典型的な利用場面（起動時一括 wakeup など）、冪等性を記入。

## Actions

### CameraCalibrationInternal

**Goal**:
```
# ==[Action] カメラ内部パラメーターキャリブレーションの実行==
# 参考：https://developer.mamezou-tech.com/robotics/vision/calibration-pattern/#asymmetry-circlegrid
# 参考：https://calib.io/pages/camera-calibration-pattern-generator
# > Width 280mm, Height 200mm, Rows 11, Cols 16, Spacing 20mm, Diameter 12mm

uint16 rows                             # Calibration board definition: Rows
uint16 cols                             # Calibration board definition: Columns
float32 spacing                         # Calibration board definition: Circle Spacing [mm]
float32 diameter                        # Calibration board definition: Diameter [mm]
string src                              # Calibration target (Topic / device path / directory path / movie file path)
```

**Result**:
```
sensor_msgs/CompressedImage image       # Calibration result
float32 fx
float32 fy
float32 cx
float32 cy
float32 k1
float32 k2
float32 k3
float32 k4
```

**Feedback**:
```
string progress
sensor_msgs/CompressedImage image       # Image on the way
```

TODO: 推奨ボード（非対称 circle grid など）、キャリブ所要時間、feedback 頻度、キャンセル時の挙動を記入。

## Dependencies

- `std_msgs`
- `geometry_msgs`
- `sensor_msgs`

## Related Packages

- TODO: カメラ／距離センサの publisher ノードを持つパッケージ
- TODO: `Obstacles` を subscribe するナビゲーション／衝突回避ノード
