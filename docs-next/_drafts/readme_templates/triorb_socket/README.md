# triorb_socket

TCPソケット通信のためのパッケージ

> version: `0.0.0` / maintainer: root <root@todo.todo> / license: TODO: License declaration

## Overview

TODO: このパッケージが提供する機能、起動タイミング、関連ノードとの連携を 2–4 文で。

## API Reference

> Source: migrated from the hand-written `API.md` in the submodule.

WebSocket 経由の JSON JOY データを ROS トピックへ変換します。

### Active API

#### JSON Joy購読
- Topic：(prefix)/vslam/joy （`joy_topic` パラメータで変更可）
- Node：(prefix)_triorb_socket
- Type： std_msgs/msg/String
- Note：BestEffortOneQoS (KeepLast=1, Reliability=BestEffort, Durability=Volatile)。`{"target":"self","axes":[...],"buttons":<uint32>}` 形式で受信
- Usage：
```
ros2 topic pub /vslam/joy std_msgs/msg/String "{data: '{\"target\":\"self\",\"buttons\":3,\"axes\":[0.1,0.2,0.0] }'}" --once
```

#### コラボレーションJoy配信
- Topic：(prefix)/collab/joy
- Node：(prefix)_triorb_socket
- Type： sensor_msgs/msg/Joy
- Note：`target != self` の入力をそのまま publish。`header.frame_id` には target を格納
- Usage：
```
ros2 topic echo /collab/joy
```

#### 自律走行速度コマンド
- Topic：(prefix)/drive/run_vel
- Node：(prefix)_triorb_socket
- Type： triorb_drive_interface/msg/TriorbRunVel3
- Note：`target=self` の場合に速度を計算して publish（現在は安全のため実送信を抑止中）
- Usage：
```
ros2 topic echo /drive/run_vel
```

## Related Packages

TODO: 上流・下流の関連パッケージを列挙。
