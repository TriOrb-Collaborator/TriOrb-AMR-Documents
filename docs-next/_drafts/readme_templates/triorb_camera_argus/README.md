# triorb_camera_argus

JetsonのArgus API経由で複数カメラ映像を取得し、回転補正やデバイス割当を行って画像トピックとして配信するノードです。

> version: `0.0.0` / maintainer: TriOrb Inc. <info@triorb.co.jp> / license: Apache-2.0

## Overview

TODO: このパッケージが提供する機能、起動タイミング、関連ノードとの連携を 2–4 文で。

## API Reference

> Source: migrated from the hand-written `API.md` in the submodule.

Jetson Argus API を利用して複数カメラの画像・状態を配信するノード。

### Active API

#### Argusカメラ画像
- Topic：<pub[i]>
- Node：(prefix)_triorb_camera_argus
- Type： sensor_msgs/msg/Image
- Note：`pub` パラメータで定義した各トピックに `mono8` 画像を publish。失敗時は No Signal 画像
- Usage：
```
ros2 topic echo /camera0 --once
```

#### カメラデバイスメタ情報
- Topic：<pub[i]>_device
- Node：(prefix)_triorb_camera_argus
- Type： triorb_sensor_interface/msg/CameraDevice
- Note：デバイスファイル名・状態・周期などを同周期で送信
- Usage：
```
ros2 topic echo /camera0_device --once
```

#### カメラエラー通知
- Topic：/error/camera
- Node：(prefix)_triorb_camera_argus
- Type： std_msgs/msg/Empty
- Note：キャプチャ失敗を 1 秒間隔で通知。監視用途
- Usage：
```
ros2 topic echo /error/camera
```

#### オートゲイン目標明るさ設定
- Service：/set/camera/auto_gain_target
- Node：(prefix)_triorb_camera_argus
- Type： triorb_camera_argus/srv/AutoGainTarget
- Note：オートゲインの目標明るさ（-2.0〜2.0）を設定。範囲外はクランプ
- Usage：
```
ros2 service call /set/camera/auto_gain_target triorb_camera_argus/srv/AutoGainTarget "{target: 0.5}"
```

## Related Packages

TODO: 上流・下流の関連パッケージを列挙。
