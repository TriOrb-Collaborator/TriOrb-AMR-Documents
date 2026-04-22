# triorb_camera_capture

カメラキャプチャーのためのパッケージ

> version: `1.2.0` / maintainer: triorb <yano.koichi@triorb.co.jp> / license: Apache-2.0

## Overview

TODO: このパッケージが提供する機能、起動タイミング、関連ノードとの連携を 2–4 文で。

## API Reference

> Source: migrated from the hand-written `API.md` in the submodule.

カメラキャプチャーのためのパッケージ

### camera_capture API
#### カメラ画像受信
- Topic：(prefix)/camera(0-N) # 末尾の整数はカメラのID
- Node：(prefix)_camera_capture
- Type：sensor_msgs/Image
- Frequency：最大1/0.02 Hz
- Usage：
```bash
root@orin-nx-XXX:~/$ ros2 topic info /camera0; ros2 topic hz /camera0
Type: sensor_msgs/msg/Image
Publisher count: 1
Subscription count: 0
average rate: 9.537
        min: 0.072s max: 0.240s std dev: 0.04572s window: 13
...
average rate: 10.766
        min: 0.064s max: 0.240s std dev: 0.02494s window: 266
```

#### カメラ情報受信
- Topic：(prefix)/camera(0-N)_device # 末尾の整数はカメラのID
- Node：(prefix)_camera_capture
- Type：triorb_sensor_interface/msg/CameraDevice
- Usage：
```bash
root@orin-nx-XXX:~/$ ros2 topic echo /camera0_device
header:
  stamp:
    sec: 1753408673
    nanosec: 447031540
  frame_id: cam0
device: /dev/video-csi0
topic: /camera0
id: cam0
state: sleep
rotation: 0
exposure: 0
gamma: 0.0
timer: 0.30000001192092896
```


#### カメラデバイス一覧取得
- Topic：(prefix)/get/camera/state
- Node：(prefix)_camera_capture
- Type：triorb_sensor_interface/srv/CameraDevice
- Usage：
```bash
root@orin-nx-XXX:~/$ ros2 service call /get/camera/state triorb_sensor_interface/srv/CameraDevice
...
response:
triorb_sensor_interface.srv.CameraDevice_Response(result=[triorb_sensor_interface.msg.CameraDevice(device='/dev/video0', topic='/camera0', id='cam0', state='awake', rotation=0, exposure=800, gamma=1.0, timer=0.02), ...])
```

#### カメラデバイスの起動・終了
- Topic：(prefix)/set/camera/state
- Node：(prefix)_camera_capture
- Type：triorb_sensor_interface/srv/CameraCapture
- Usage：
```bash
root@orin-nx-XXX:~/$ ros2 service call /set/camera/state triorb_sensor_interface/srv/CameraCapture '{request: [{device: /dev/video0, topic: /camera0, id: camera0, state: wakeup, rotation: 0, exposure: 500, gamma: 1.0, timer: 0.1}, {device: /dev/video2, topic: /camera1, id: camera1, state: wakeup, rotation: 0, exposure: 500, gamma: 1.0, timer: 0.1}]}'
...
response:
triorb_sensor_interface.srv.CameraCamture_Response(result=['success','success'])
```

#### オートゲイン目標値の設定
- Service：(prefix)/set/camera/auto_gain_target
- Node：(prefix)_camera_capture
- Type：triorb_camera_argus/srv/AutoGainTarget
- Note：`target` は EV 相当で、`[-2.0, 2.0]` にクランプされます
- Usage：
```bash
root@orin-nx-XXX:~/$ ros2 service call /set/camera/auto_gain_target triorb_camera_argus/srv/AutoGainTarget "{target: 0.5}"
```

## Related Packages

TODO: 上流・下流の関連パッケージを列挙。
