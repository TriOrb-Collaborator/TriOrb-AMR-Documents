# triorb_drive_vector

制御指令値からロボットの進行方向や停止・回転などの状態判定を行う

> version: `1.2.0` / maintainer: TriOrb Inc. <info@triorb.co.jp> / license: Apache-2.0

## Overview

TODO: このパッケージが提供する機能、起動タイミング、関連ノードとの連携を 2–4 文で。

## API Reference

> Source: migrated from the hand-written `API.md` in the submodule.

制御指令値からロボットの進行方向や停止・回転などの状態判定を行う

### Subscriber
#### 移動指令を取得
- Topic: /drive/run_pos
- Type: triorb_drive_interface/msg/TriorbRunPos3
- Usage:
```bash
ros2 topic pub --once /drive/run_pos triorb_drive_interface/msg/TriorbRunPos3 \
  '{position: {x: 0.1, y: 0.0, deg: 0.0}, speed: {acc: 300, dec: 300, xy: 0.2, w: 0.0}}'
```

#### 移動指令を取得
- Topic: /drive/run_vel
- Type: triorb_drive_interface/msg/TriorbRunPos3
- Usage:
```bash
ros2 topic pub --once /drive/run_vel triorb_drive_interface/msg/TriorbRunPos3 \
  '{position: {x: 0.0, y: 0.0, deg: 0.0}, speed: {acc: 0, dec: 0, xy: 0.0, w: 0.6}}'
```

### Publisher
#### 移動方向
- Topic: /drive/std_vector
- Type: Float32MultiArray
  - 配列フォーマット
  ```bash
  direction: 方向
  speed: 速度
  f_rotate: 時計回り 1 / 反時計回り -1
  f_stop: 停止と判定した際 1 / その他 -1
  ```
  - 例: 直進で停止判定なし
  ```bash
  ros2 topic echo --once /drive/std_vector
  data: [1.57, 0.35, -1.0, -1.0]
  ```
#### 移動方向2
- Topic: /drive/std_vector2
- Type: Float32MultiArray
  - 配列フォーマット
  ```bash
  direction: 並進方向 [deg] （-180～180. 正面が0, 右方向が正.）
  speed: 並進速度 [m/s]
  vw: 回転角速度 [rad/s] (CW: +, CCW: -)
  ```

#### ノードの動作開始通知
- Topic: (prefix)/_{ノード名}
- Type: std_msgs/msg/Empty
 - Usage:
```bash
ros2 topic echo --once /_triorb_drive_vector
```

### Service
#### ノードのバージョン情報を取得
- Topic: (prefix)/get/version/{ノード名}
- Type: triorb_static_interface/srv/Version
 - Usage:
```bash
ros2 service call /get/version/triorb_drive_vector triorb_static_interface/srv/Version {}
```

### Action
本パッケージではActionは利用していません。

## Related Packages

TODO: 上流・下流の関連パッケージを列挙。
