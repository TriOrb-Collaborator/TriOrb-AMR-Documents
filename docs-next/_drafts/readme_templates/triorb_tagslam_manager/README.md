# triorb_tagslam_manager

TagSLAM用の地図保存・読込・初期化を一括管理し、tagslam系ノードの再起動や状態通知を行う管理ノードです。

> version: `0.0.0` / maintainer: TriOrb <info@triorb.co.jp> / license: Apache License, Version 2.0

## Overview

TODO: このパッケージが提供する機能、起動タイミング、関連ノードとの連携を 2–4 文で。

## API Reference

> Source: migrated from the hand-written `API.md` in the submodule.

TagSLAM用の地図保存・読込・初期化を一括管理し、tagslam系ノードの再起動や状態通知を行う管理ノードです。


### Subscriber（外部からの呼び出し例付き）
各トピック名は`ROS_PREFIX`が設定されていれば`/<prefix>/...`に変換されます。以下のコマンド例では`ROS_PREFIX=/robot`を想定しています。

#### `/tagslam/save/map` (`std_msgs/msg/String`)
- 地図保存要求。msg.dataを地図ディレクトリ名として`/data/tagslam_map/<名前>`に保存します。`/`は`_`に置換されます。
- 外部送信例:
  ```bash
  ROS_PREFIX=/robot ros2 topic pub --once /robot/tagslam/save/map std_msgs/msg/String '{data: "warehouse_202405"}'
  ```

#### `/tagslam/load/map` (`std_msgs/msg/String`)
- JSONまたは単純文字列で地図操作モードを受付けます。`mode`により動作が変わります。
  - `load`: 既存地図を読み込み、`tagslam`/`sync_and_detect`を再起動。`is_static`(bool)、`slow_mode`(bool)、`amnesia`(bool)、`map_name`(string)を指定。
  - `initialize`: `/params/tagslam/tagslam_original.yaml`を元に初期タグ情報を生成し直して再起動。後述のパラメータを任意指定可能。
  - `remove`: `map_name`配下の保存済み地図を削除。
- 外部送信例（地図読込）:
  ```bash
  ROS_PREFIX=/robot ros2 topic pub --once /robot/tagslam/load/map std_msgs/msg/String \
    "{data: '{\"mode\":\"load\",\"map_name\":\"warehouse_202405\",\"is_static\":true,\"slow_mode\":false,\"amnesia\":true}'}"
  ```
- 外部送信例（初期化）:
  ```bash
  ROS_PREFIX=/robot ros2 topic pub --once /robot/tagslam/load/map std_msgs/msg/String \
    "{data: '{\"mode\":\"initialize\",\"origin_tag_id\":1,\"origin_tag_size\":150,\"origin_tag_pos_z\":0,\"origin_tag_pos_deg\":0,\"default_tag_size\":120,\"optimizer_mode\":\"fast\"}'}"
  ```
- 外部送信例（削除）:
  ```bash
  ROS_PREFIX=/robot ros2 topic pub --once /robot/tagslam/load/map std_msgs/msg/String \
    "{data: '{\"mode\":\"remove\",\"map_name\":\"warehouse_202405\"}'}"
  ```

#### `/odom/body_t_rig` (`nav_msgs/msg/Odometry`)
- ボディ座標系に対するリグ座標系のOdometry。受信すると`/tagslam/rig_tf`へ`TransformStamped`として流し、SLAMロスト判定用のタイマも更新します。
- 外部送信例（静的姿勢を一度だけ送る）:
  ```bash
  ROS_PREFIX=/robot ros2 topic pub --once /robot/odom/body_t_rig nav_msgs/msg/Odometry \
    '{pose: {pose: {position: {x: 0.0, y: 0.0, z: 0.0}, orientation: {w: 1.0, x: 0.0, y: 0.0, z: 0.0}}}}'
  ```

#### `cameras[*].tag_topic` (`apriltag_msgs/msg/AprilTagDetectionArray`)
- `/params/tagslam/cameras.yaml`に記述された全カメラの`tag_topic`へ動的にSubscriberを張り、検出中タグIDを追跡します。`set_tag_size_from_file`で読みだしたサイズと合わせて`/tagslam/tag_tf`のメタ情報として利用されます。
- 外部送信例（例: `/robot/camera0/detector/tags`へダミー配信）:
  ```bash
  ROS_PREFIX=/robot ros2 topic pub --once /robot/camera0/detector/tags apriltag_msgs/msg/AprilTagDetectionArray \
    '{detections: [{id: 100}]}' 
  ```

### Publisher
| Topic | 型 | 内容 |
| --- | --- | --- |
| `/tagslam/rig_tf` | `geometry_msgs/msg/TransformStamped` | `/odom/body_t_rig`で受信した姿勢をTF互換形式に変換。 |
| `/tagslam/tag_tf` | `geometry_msgs/msg/TransformStamped` | `tf_buffer`に存在するタグ姿勢を周期送信。`header.frame_id`にはタグサイズ、`child_frame_id`の末尾には`look`/`known`を追記。 |
| `/tagslam/state` | `std_msgs/msg/UInt8MultiArray` | `StateCode`（WORKING/SAVE_MAP/LOAD_MAP）の進捗。`StateValue`(0:STANDBY,1:PROCESSING,2:SUCCESS,3:LOST)または`64+ErrorValue`を格納。 |
| `/tagslam/map_name` | `std_msgs/msg/String` | 現在ロード済みの地図名。 |
| `/tagslam/status` | `triorb_slam_interface/msg/SlamStatus` | ビットフラグでSLAM状態/エラーを通知。state: bit0=FIXマップ、bit1=ローカライズ成功、bit2=保存処理中、bit3=読込処理中。error: bit0=tagslam停止、bit1=既知タグ未検出、bit2=保存失敗、bit3=読込失敗。 |

### Service
| Service | 型 | 説明 |
| --- | --- | --- |
| `/get/version/tagslam_manager_node` | `triorb_static_interface/srv/Version` | ノードバージョン(現在`0.0.0`)を返却。`ROS_PREFIX`が付与された名前空間に配置されます。 |

### 地図操作の詳細
- **保存**: `/tagslam/save/map`受信後`/dump`サービス(Trigger)を呼び出し、`poses.yaml`と`camera_poses.yaml`を取得。`tagslam.yaml`の`bodies`以降を`poses.yaml`で置き換え、`/data/tagslam_map/<name>/tagslam_map.yaml`に書き出します。完了/エラーを`/tagslam/state`および`/tagslam/status`で通知。
- **読込**: `/tagslam/load/map`で`mode=load`を受けると、保存済み地図を`/params/tagslam/target_map.yaml`へ複写しながら`is_static`指定やノイズ置換を実施。完了後`tmux`セッション`detect`と`tagslam`を再起動し、tfバッファをリセットしてタグサイズ辞書を再生成します。
- **初期化**: `mode=initialize`では`tagslam_original.yaml`を基にタグID/サイズ/高さ/姿勢/デフォルトサイズ、`optimizer_mode`(`fast|slow|full`)、`minimum_viewing_angle`、`minimum_tag_area`などを上書きして`tagslam.yaml`を生成。再起動後は地図名を空にします。
- **削除**: `mode=remove`では`/data/tagslam_map/<map_name>`を再帰的に削除します。

### 状態監視
- `check_state()`が1秒周期で`tagslam`/`sync_and_detect`ノードの生存確認とロスト判定（2秒以内に`/odom/body_t_rig`更新が無い場合は`LOST`）を行い、`/tagslam/state`と`/tagslam/status`へ反映します。
- `check_tf_tree()`が1秒周期で`tf_buffer`から既知タグ一覧を取得し、`/tagslam/tag_tf`に送出します。
- `check_srv_call_result()`が地図保存のサービス応答を監視し、`ErrorValue`（BUSY/ TIMEOUT/ NOT_FOUND/ UNKNOWN）を付与します。

## Related Packages

TODO: 上流・下流の関連パッケージを列挙。
