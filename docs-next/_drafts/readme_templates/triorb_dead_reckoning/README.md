# triorb_dead_reckoning

VSLAM・オドメトリ・IMUを統合し自己位置を推定するデッドレコニングパッケージです。IMUセンサ確認用バイパスログ機能も含みます。

> version: `1.2.0` / maintainer: TriOrb <info@triorb.co.jp> / license: Apache License, Version 2.0

## Overview

TODO: このパッケージが提供する機能、起動タイミング、関連ノードとの連携を 2–4 文で。

## API Reference

> Source: migrated from the hand-written `API.md` in the submodule.

vslam・odometry・imuデータからisam2で位置情報を推定する

### Subscriber
#### オドメトリデータを受信して自己位置推定に利用
- Topic: (prefix)/triorb/odom
- Type: geometry_msgs/msg/Vector3Stamped

#### VSLAM推定姿勢データを受信して自己位置推定に利用
- Topic: (prefix)/vslam/rig_tf
- Type: geometry_msgs/msg/TransformStamped

### Publisher
#### デッドレコニング推定結果を配信
- Topic: (prefix)/triorb/dead_reckoning
- Type: geometry_msgs/msg/Vector3Stamped

#### ノードの動作開始通知
- Topic: (prefix)/_{ノード名}
Type: std_msgs/msg/Empty

### Service
#### ノードのバージョン情報を取得
- Topic: (prefix)/get/version/{ノード名}
- Type: triorb_static_interface/srv/Version

### Action
本パッケージではActionは利用していません。

### MQTT
#### id
- triorb_dead_reckoning_stream_{random.randint(0, 10000)}
#### Publish
- Topic: /dead_reckoning/stream
    - jeson format
    ```bash
    {
    "imu_acc":[x,x,z]
    "imu_gyro":[x,x,z]
    "odometry":[x,x,w]
    "vslam":[x,x,w]
    "gtsam":[x,x,w]
    "serial_status":"状態をstring"
    "vslam_off":"状態をTrue/False"
    }
    ```
#### Subscribe
- Topic: /dead_reckoning/debug/start
    - デバッグモード開始 Emptyメッセージ
- Topic: /dead_reckoning/debug/end
    - デバッグモード終了 Emptyメッセージ
- Topic: /dead_reckoning/vslam/off
    - vslam/rig_tfを無視 Emptyメッセージ

## Related Packages

TODO: 上流・下流の関連パッケージを列挙。
