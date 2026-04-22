# triorb_drive_pico

ROS2メッセージを用いてモーター制御ECUと通信するためのパッケージ

> version: `1.2.0` / maintainer: TriOrb <info@triorb.co.jp> / license: Apache License, Version 2.0

## Overview

TODO: このパッケージが提供する機能、起動タイミング、関連ノードとの連携を 2–4 文で。

## API Reference

> Source: migrated from the hand-written `API.md` in the submodule.

ROS2メッセージを用いてモーター制御ECUと通信するためのパッケージ

### Subscriber

#### 励磁オン
- Topic: (prefix)/drive/wakeup
- Type: std_msgs/msg/Empty
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 topic pub -1 /drive/wakeup std_msgs/msg/Empty 
```

#### 励磁オフ
- Topic: (prefix)/drive/sleep
- Type: std_msgs/msg/Empty
```bash
root@orin-nx-XXX:~/$ ros2 topic pub -1 /drive/sleep std_msgs/msg/Empty
```

#### 速度ベクトル指示による移動
- Topic: (prefix)/drive/run_vel
- Type: triorb_drive_interface/msg/TriorbRunVel3
- Note: 前回適用された指示と比較して, 以下の条件を両方満たす場合はスキップする.
    - 0.2秒以下の間隔
    - 速度指示値velocityのx,y,wの差が0.001以下

#### 移動距離指示による相対移動
- Topic: (prefix)/drive/run_pos
- Type: triorb_drive_interface/msg/TriorbRunPos3

#### モータードライバの設定変更
- Topic: (prefix)/set/motor/params
- Type: triorb_drive_interface/msg/MotorParams
- Note: 全ての値を0にすると, 出荷時の設定を書き込む.

#### 移動停止
- Topic: (prefix)/drive/stop
- Type: std_msgs/msg/Empty
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 topic pub -1 /drive/stop std_msgs/msg/Empty
```

#### トルク設定変更
- Topic: (prefix)/set/motor/torque
- Type: std_msgs/msg/Float32
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 topic pub -1 /set/motor/torque std_msgs/msg/Float32 "data: 100.0" # 10%
```

#### ライフタイムの設定
- Topic: (prefix)/drive/set_life_time
- Type: std_msgs/msg/UInt16
- Note: ライフタイム[ms]を設定する. 速度ベクトル指示後, ロボットはライフタイム経過後にエラー扱いで停止する. この時間は速度ベクトル指示の度に0からカウントされる. 0を設定すると無効になる.
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 topic pub -1 /drive/set_life_time std_msgs/msg/UInt16 "data: 1000" # 1000ms
```

#### 運転モード
- Topic: (prefix)/mutex/set_drive_mode
- Type: std_msgs/msg/UInt8
- Note: 速度ベクトル指示での制御を変更する. 
 - 16: 速度制御. モーターは加速時間にしたがって加速し, 減速時間にしたがって減速する. 指示の与え方によっては意図しない回転成分が入るため非推奨.
 - 17: 押し当て制御. 負荷に押し当たった場合に加圧を続ける. トルクは100%に制限される.
 - 19: サイクリック制御（デフォルト）. 他の制御方式と比較して, 意図しない回転成分が入りにくい.
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 topic pub -1 /mutex/set_drive_mode std_msgs/msg/UInt8 "data: 16"
```

#### リフトアップ/リフトダウン
- Topic: (prefix)/drive/run_lifter
- Type: std_msgs/msg/String
- Note: リフター付きモデル限定.
  - "up": リフトを上昇させる
  - "down": リフトを下降させる
  - "stop": リフトの動作を停止する
  - "middle": リフトを中間点に移動させる
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 topic pub -1 /drive/run_lifter std_msgs/msg/String "data: up"
```

### Publisher

#### ロボットステータスの定期送信
- Topic: (prefix)/robot/status
- Type: triorb_static_interface/msg/RobotStatus
- Note: 1.5秒間隔で送信される.
- Note： Accepting move instruction, Generating mapフラグおよびvoltageは未実装 
```bash
triorb@orin-nx-XXX:~/$ ros2 topic echo --once /robot/status 
header: 
  stamp: 
    sec: 1717491443 
    nanosec: 313522765 
  frame_id: robot 
voltage: 0.0 
btns: 0 
state: 53248 
error: 0
```

#### オドメトリの定期送信
- Topic: (prefix)/triorb/odom
- Type: geometry_msgs/msg/Vector3Stamped
- Note: 0.2秒間隔で送信される.


#### バージョン情報の定期送信
- Topic: (prefix)/triorb/version/drive
- Topic: (prefix)/triorb/version/pico
- Topic: (prefix)/triorb/version/core
- Type: std_msgs/msg/String
- Note: 10秒間隔で送信される.

#### 現在の指令モードの定期送信
- Topic: (prefix)/drive/mode
- Type: std_msgs/msg/String
- Value:
    - "idle": 停止中
    - "run_vel": 速度ベクトル指示による移動中
    - "run_pos": 移動距離指示による相対移動中
    - "lift": リフター動作中
- Note: 1.5秒間隔で送信される.
- Node: [注意] モーターライフタイムタイムアウト時は"idle"に戻らない

#### リフター状態の定期送信
- Topic: (prefix)/robot/lifter_state
- Type: std_msgs/msg/UInt8
- Value:
    -  0: 位置不明(起動直後など)
    -  1: 停止命令時
    -  2: リフトアップ状態
    -  3: リフトダウン状態
    -  4: リフトアップ中
    -  5: リフトダウン中
    -  6: 中間点移動中
    -  7: 中間点到達状態
    -  8: STOP_ONWAY 
    -  9: リフトアップ状態、荷物偏り
    - 10: リフトアップ状態、空荷
    - 11: モータエラー（alarm）
    - 12: モータエラー（qstop）
    - 13: モータエラー（watchdog）
    - 14: IO接続異常
- Note: 1.5秒間隔で送信される.

### Service

#### 速度ベクトル指示による移動（速度到達確認あり）
- Topic: (prefix)/srv/drive/run_vel
- Type: triorb_drive_interface/srv/TriorbRunVel3
- Usage： 
```bash
triorb@orin-nx-XXX:~/$ ros2 service call /get/motor/status triorb_drive_interface/srv/MotorStatus  
requester: making request: triorb_drive_interface.srv.MotorStatus_Request(request=std_msgs.msg.Empty()) 

response: 
triorb_drive_interface.srv.MotorStatus_Response(result=triorb_drive_interface.msg.MotorStatus(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1709711017, nanosec=956667335), frame_id='serial'), last_error_value=0, last_error_motor=255, voltage=0.0, state=0, power=0.0)) 
```
 
#### 移動距離指示による相対移動（移動完了確認あり）
- Topic: (prefix)/srv/drive/run_pos
- Type: triorb_drive_interface/srv/TriorbRunPos3
- Usage： 
```bash
triorb@orin-nx-XXX:~/$ ros2 service call /srv/drive/run_pos \
triorb_drive_interface/srv/TriorbRunPos3 "{request: {speed: {acc: 500, dec: 500, xy: 0.1, w: 0.0}, position: {x: 0.0, y: 1.0, deg: 0.0} }  }" 
## コマンド以上 

waiting for service to become available... 
requester: making request: 
triorb_drive_interface.srv.TriorbRunPos3_Request(request=triorb_drive_interface.msg.TriorbRunPos3(speed=triorb_drive_interface.msg.TriorbSpeed(acc=500, dec=500, xy=0.1, w=0.0), position=triorb_drive_interface.msg.TriorbPos3(x=0.0, y=1.0, deg=0.0))) 

response: 
triorb_drive_interface.srv.TriorbRunPos3_Response(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1717490931, nanosec=365277011), frame_id='serial'), result=2) 
```

#### モーターステータス取得
- Topic：(prefix)/get/motor/status
- Type： triorb_drive_interface/srv/MotorStatus
- Usage：
```bash
triorb@orin-nx-XXX:~/$ ros2 service call /get/motor/status triorb_drive_interface/srv/MotorStatus 
requester: making request: triorb_drive_interface.srv.MotorStatus_Request(request=std_msgs.msg.Empty())

response:
triorb_drive_interface.srv.MotorStatus_Response(result=triorb_drive_interface.msg.MotorStatus(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1709711017, nanosec=956667335), frame_id='serial'), last_error_value=0, last_error_motor=255, voltage=0.0, state=0, power=0.0))
```

#### エラー履歴の取得
- Topic：(prefix)/get/error/history
- Type： triorb_static_interface/srv/ErrorList
- Note: Responseに表示されるstampはpicoが起動してから経過した時間を表しており, Jetson内のタイムスタンプとは関係がない.
- Usage：
```bash
triorb@orin-nx-XXX:~/$ ros2 service call /get/error/history triorb_static_interface/srv/ErrorList
waiting for service to become available...
requester: making request: triorb_static_interface.srv.ErrorList_Request(request=std_msgs.msg.Empty())

response:
triorb_static_interface.srv.ErrorList_Response(errors=[triorb_static_interface.msg.RobotError(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=0, nanosec=0), frame_id='pico_error0'), error=0), triorb_static_interface.msg.RobotError(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=0, nanosec=0), frame_id='pico_error1'), error=0), triorb_static_interface.msg.RobotError(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=0, nanosec=0), frame_id='pico_error2'), error=0), triorb_static_interface.msg.RobotError(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=0, nanosec=0), frame_id='pico_error3'), error=0), triorb_static_interface.msg.RobotError(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=0, nanosec=0), frame_id='pico_error4'), error=0)])
```

#### 励磁オン
- Topic: (prefix)/srv/drive/wakeup
- Type: std_srvs/srv/Empty
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 service call /srv/drive/wakeup std_srvs/srv/Empty
```

#### 励磁オフ
- Topic: (prefix)/srv/drive/sleep
- Type: std_srvs/srv/Empty
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 service call /srv/drive/sleep std_srvs/srv/Empty
```

## Related Packages

TODO: 上流・下流の関連パッケージを列挙。
