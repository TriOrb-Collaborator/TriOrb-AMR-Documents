# triorb_static_broadcast

ロボットの基本フレーム間の固定変換をTFとして送出する静的ブロードキャストノードです。

> version: `1.1.0` / maintainer: TriOrb Inc. <info@triorb.co.jp> / license: Apache-2.0

## Overview

TODO: このパッケージが提供する機能、起動タイミング、関連ノードとの連携を 2–4 文で。

## API Reference

> Source: migrated from the hand-written `API.md` in the submodule.

TriOrb 固有の `tf_static` を一括で生成するノードです。

### Active API

#### 静的TF(triorb_map→map)
- Topic：/tf_static
- Node：(prefix)_triorb_static_broadcast
- Type： tf2_msgs/msg/TFMessage
- Note：`rig_is_center` パラメータに応じて `triorb_map→map` と `rig→robot_center` の2本を送信
- Usage：
```
ros2 topic echo /tf_static --once
```

#### ノード登録通知
- Topic：/except_handl/node/add
- Node：(prefix)_triorb_static_broadcast
- Type： std_msgs/msg/String
- Note：ParametersQoS で `[instant]node_name` を送信し、例外監視ノードへ登録
- Usage：
```
ros2 topic echo /except_handl/node/add --once
```

## Related Packages

TODO: 上流・下流の関連パッケージを列挙。
