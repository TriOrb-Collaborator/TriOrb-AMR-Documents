# triorb_slam_interface

SLAM 関連 Interface 定義パッケージ（キーフレーム、姿勢、特徴点等）。

> package.xml `<description>`: "SLAM関連Interface"
>
> version: 1.2.0 / maintainer: tobata.masakazu@triorb.co.jp

## Interface Summary

| Kind | Name | 用途（記入要） |
| --- | --- | --- |
| msg | CamerasLandmarkInfo | TODO: 概要を記入（各カメラの特徴点情報） |
| msg | CamerasPose | TODO: 概要を記入（各カメラの姿勢情報） |
| msg | Keyframe | TODO: 概要を記入（Keyframe ID） |
| msg | KeyframeArray | TODO: 概要を記入（Keyframe のリスト） |
| msg | PointArrayStamped | TODO: 概要を記入（Header 付き点群） |
| msg | PoseDevStamped | TODO: 概要を記入（有効フラグ付き姿勢） |
| msg | SlamStatus | TODO: 概要を記入（SLAM 実行状況） |
| msg | UInt32MultiArrayStamped | TODO: 概要を記入（Header 付き uint32 配列） |
| msg | XyArrayStamped | TODO: 概要を記入（Header 付き XY 配列） |

## Messages

### CamerasLandmarkInfo

**Fields**:
```
#==各カメラの特徴点情報==
std_msgs/Header header            # header
PointArrayStamped[] camera        # points array per camera
```

TODO: カメラ配列の順序規約、publish 元 SLAM ノードを記入。

### CamerasPose

**Fields**:
```
#==各カメラの姿勢情報==
std_msgs/Header header         # header
PoseDevStamped[] camera        # pose info
```

TODO: 姿勢の基準フレーム（map / base_link）、カメラ順序規約を記入。

### Keyframe

**Fields**:
```
#==Keyframe ID（header付きのint32データ）==
std_msgs/Header header         # header
int32 id                       # keyframe id
```

TODO: id の割り当てルール、publish タイミングを記入。

### KeyframeArray

**Fields**:
```
#==Keyframeリスト==
std_msgs/Header header         # header
Keyframe[] keyframes           # keyframes
```

TODO: 全 keyframe を配信するか差分か、更新タイミングを記入。

### PointArrayStamped

**Fields**:
```
#==point array（Header付）==
std_msgs/Header header              # header
geometry_msgs/Point[] points        # points array
```

TODO: points の座標系（カメラローカル vs map）を記入。

### PoseDevStamped

**Fields**:
```
#==姿勢情報（有効フラグ付き）==
std_msgs/Header header              # header
geometry_msgs/Pose pose             # pose array
bool valid                          # valid
```

TODO: valid=false の条件（ロスト時など）を記入。

### SlamStatus

**Fields**:
```
#==SLAMの実行状況==
string map_name  # map name
uint8 state      # mapping now, fix map... etc
uint8 error      # not working, map load failed... etc

#---slam operation status (bit flag)---
# 0b00000001: mapping mode(0), fix map(1)
# 0b00000010: lost(0), localize(1)
# 0b00000100: processing save map
# 0b00001000: processing load map

#---error state (bit flag)---
# 0b00000001: slam is not working
# 0b00000010: Never detected a known landmark
# 0b00000100: save map failed
# 0b00001000: load map failed (cannot find map)
```

TODO: publish 周期、UI 側の state/error 表示との対応を記入。

### UInt32MultiArrayStamped

**Fields**:
```
#==uint32 array（Header付）==
std_msgs/Header header  # header
uint32[] data           # data array
```

TODO: data の意味（ID 列挙など）を記入。

### XyArrayStamped

**Fields**:
```
#==（u16）X arrayと（u16）Y arrayの混合（Header付）==
std_msgs/Header header  # header
uint16[] x              # x array
uint16[] y              # y array
```

TODO: x/y の単位（px / grid cell）、座標系を記入。

## Dependencies

- `std_msgs`
- `geometry_msgs`
- `sensor_msgs`

## Related Packages

- TODO: SLAM エンジン本体のパッケージ（publisher）
- TODO: ナビゲーション／UI（subscriber）
