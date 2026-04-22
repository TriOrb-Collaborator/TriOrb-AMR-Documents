# triorb_collaboration_interface

協調搬送（複数ロボットによる連携動作）に関わる ROS 2 インターフェース定義パッケージ。

> package.xml の `<description>` は未記入（"TODO: Package description"）。必要に応じて更新してください。
>
> version: 1.0.0 / maintainer: tobata.masakazu@triorb.co.jp

## Interface Summary

| Kind | Name | 用途（記入要） |
| --- | --- | --- |
| msg | GroupCreate | TODO: 概要を記入（協調グループの構築情報） |
| msg | ParentBind | TODO: 概要を記入（仮想原点に対する相対姿勢） |

## Messages

### GroupCreate

**Fields**:
```
# ==[協調搬送] グループ構築情報==
std_msgs/Header header                              # Header
string master                                       # Master
triorb_collaboration_interface/ParentBind[] robots  # Robot informations
```

TODO: master の識別子形式（名前 / IP）、グループ構築タイミング、publish 元ノードを記入。

### ParentBind

**Fields**:
```
# ==[協調搬送] 仮想（荷物など）原点に対するロボットの相対姿勢==
std_msgs/Header header      # Header
string parent               # Parent name
string you                  # Your name or ip
float32 x                   # Relative position of the parent from you [m]
float32 y                   # Relative position of the parent from you [m]
float32 deg                 # Relative position of the parent from you [deg]
```

TODO: 座標系（you 基準で parent の相対位置）、deg の符号規約、更新周期を記入。

## Dependencies

- `std_msgs`
- `geometry_msgs`
- `sensor_msgs`

## Related Packages

- TODO: 協調搬送を制御するノード（`triorb-drive` 系の collaboration モジュール等）
- TODO: `RobotStatus.collab_id` との対応を記入（`triorb_static_interface`）
