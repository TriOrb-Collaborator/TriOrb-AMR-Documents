# MQTT API

```{warning}
MQTT API はアーリープレビューです。現時点では正式な外部仕様書ではなく、
`submodules/TriOrb-AMR-Package/params` 配下の YAML 定義から確認できる
ROS 2 - MQTT ブリッジ設定を掲載しています。topic 名、payload、QoS は今後変更される可能性があります。
```

MQTT API は、TriOrb BASE 内部の ROS 2 topic を MQTT broker 経由で送受信するためのインタフェースです。
`ros2mqtt` に定義された ROS 2 topic は MQTT へ配信され、`mqtt2ros` に定義された MQTT topic は購読されて
対応する ROS 2 topic へ publish されます。

## 接続先とtopic prefix

標準設定では、MQTT broker はロボット上の `localhost:1883` として定義されています。
実機で外部クライアントから接続できるかどうかは、起動構成、ネットワーク設定、firewall、broker の公開設定に依存します。

topic 名に含まれる placeholder は実行時に置換されます。

| placeholder | 意味 |
|---|---|
| `ROS_PREFIX` | ROS 2 topic prefix。`ros2_run_mqtt_client.sh` では `/params/ROS_PREFIX` から読み込まれます。 |
| `MQTT_PREFIX` | MQTT topic prefix。標準起動では `/params/ROS_PREFIX` と同じ値が使われます。 |
| `GROUP_NAME` | 協調制御用のグループ名です。 |
| `MQTT_PORT_TCP` | 協調制御用の broker TCP port です。 |

例えば `ROS_PREFIX=triorb01` の場合、`MQTT_PREFIX/robot/status` は
`triorb01/robot/status` として扱われます。

## payload

payload は `mqtt_client` のブリッジ実装に従います。`primitive: true` の定義では、文字列、数値、
真偽値などの primitive payload が対応する ROS 2 message へ変換されます。非 primitive の定義では、
ROS message の serialized payload と message type 情報を使うため、一般の MQTT クライアントから直接扱う用途では
互換性に注意してください。

## 標準定義

出典: `submodules/TriOrb-AMR-Package/params/params.ros2.yaml`

### 配信: ROS 2 to MQTT

| ROS 2 topic | MQTT topic | ROS type | MQTT QoS |
|---|---|---|---|
| `/ROS_PREFIX/robot/status` | `MQTT_PREFIX/robot/status` | `triorb_static_interface/msg/RobotStatus` | `0` |
| `/ROS_PREFIX/vslam/rig_tf` | `MQTT_PREFIX/vslam/rig_tf` | `geometry_msgs/msg/TransformStamped` | `0` |
| `/ROS_PREFIX/vslam/robot_pose` | `MQTT_PREFIX/vslam/robot_pose` | `triorb_drive_interface/msg/TriorbPos3` | `0` |
| `/ROS_PREFIX/action/event` | `MQTT_PREFIX/action/event` | `std_msgs/msg/String` | `2` |
| `/ROS_PREFIX/drive/state` | `MQTT_PREFIX/drive/state` | `triorb_drive_interface/msg/TriorbRunState` | `2` |
| `/ROS_PREFIX/drive/result` | `MQTT_PREFIX/drive/result` | `triorb_drive_interface/msg/TriorbRunResult` | `2` |
| `/ROS_PREFIX/robot/vel_level` | `MQTT_PREFIX/robot/vel_level` | `std_msgs/msg/UInt8` | `0` |
| `/ROS_PREFIX/run_slam/enable_camera` | `MQTT_PREFIX/run_slam/enable_camera` | `std_msgs/msg/Int8MultiArray` | `0` |
| `/ROS_PREFIX/run_slam/map_file_path` | `MQTT_PREFIX/run_slam/map_file_path` | `std_msgs/msg/String` | `0` |
| `/ROS_PREFIX/run_slam/local_map_file_path` | `MQTT_PREFIX/run_slam/local_map_file_path` | `std_msgs/msg/String` | `0` |
| `/ROS_PREFIX/run_slam/map_freeze` | `MQTT_PREFIX/run_slam/map_freeze` | `std_msgs/msg/Bool` | `0` |
| `/ROS_PREFIX/run_slam/marker_only` | `MQTT_PREFIX/run_slam/marker_only` | `std_msgs/msg/Bool` | `0` |
| `/ROS_PREFIX/run_slam/marker_exclude` | `MQTT_PREFIX/run_slam/marker_exclude` | `std_msgs/msg/Bool` | `0` |
| `/ROS_PREFIX/run_slam/map_file_changed` | `MQTT_PREFIX/run_slam/map_file_changed` | `std_msgs/msg/String` | `2` |
| `/ROS_PREFIX/lifter/result` | `MQTT_PREFIX/lifter/result` | `std_msgs/msg/String` | `2` |
| `/ROS_PREFIX/run_slam/keyframe_landmarks` | `MQTT_PREFIX/run_slam/keyframe_landmarks` | `triorb_slam_interface/msg/UInt32MultiArrayStamped` | `0` |
| `/ROS_PREFIX/run_slam/matched_landmarks` | `MQTT_PREFIX/run_slam/matched_landmarks` | `triorb_slam_interface/msg/UInt32MultiArrayStamped` | `0` |
| `/ROS_PREFIX/ros2/pong` | `MQTT_PREFIX/ros2/pong` | `std_msgs/msg/String` | `0` |
| `/ROS_PREFIX/triorb/version/drive` | `MQTT_PREFIX/triorb/version/drive` | `std_msgs/msg/String` | `0` |
| `/ROS_PREFIX/triorb/version/pico` | `MQTT_PREFIX/triorb/version/pico` | `std_msgs/msg/String` | `0` |
| `/ROS_PREFIX/triorb/version/core` | `MQTT_PREFIX/triorb/version/core` | `std_msgs/msg/String` | `0` |
| `/ROS_PREFIX/triorb/error/log` | `MQTT_PREFIX/triorb/error/log` | `std_msgs/msg/UInt16MultiArray` | `0` |
| `/ROS_PREFIX/triorb/error/str/log` | `MQTT_PREFIX/triorb/error/str/log` | `std_msgs/msg/String` | `0` |
| `/ROS_PREFIX/triorb/warn/log` | `MQTT_PREFIX/triorb/warn/log` | `std_msgs/msg/UInt16MultiArray` | `0` |
| `/ROS_PREFIX/triorb/warn/str/log` | `MQTT_PREFIX/triorb/warn/str/log` | `std_msgs/msg/String` | `0` |
| `/ROS_PREFIX/triorb/nav/state` | `MQTT_PREFIX/triorb/nav/state` | `std_msgs/msg/Int32MultiArray` | `2` |
| `/ROS_PREFIX/nav/handling_task_csv_name` | `MQTT_PREFIX/nav/handling_task_csv_name` | `std_msgs/msg/String` | `2` |
| `/ROS_PREFIX/triorb/nav/result` | `MQTT_PREFIX/triorb/nav/result` | `std_msgs/msg/String` | `2` |
| `/ROS_PREFIX/tagslam/rig_tf` | `MQTT_PREFIX/tagslam/rig_tf` | `geometry_msgs/msg/TransformStamped` | `0` |
| `/ROS_PREFIX/tagslam/tag_tf` | `MQTT_PREFIX/tagslam/tag_tf` | `geometry_msgs/msg/TransformStamped` | `0` |
| `/ROS_PREFIX/tagslam/state` | `MQTT_PREFIX/tagslam/state` | `std_msgs/msg/UInt8MultiArray` | `0` |
| `/ROS_PREFIX/tagslam/status` | `MQTT_PREFIX/tagslam/status` | `triorb_slam_interface/msg/SlamStatus` | `0` |
| `/ROS_PREFIX/triorb/text_voice` | `MQTT_PREFIX/triorb/text_voice` | `std_msgs/msg/String` | `0` |
| `/ROS_PREFIX/drive/pause` | `MQTT_PREFIX/drive/pause` | `std_msgs/msg/Empty` | `2` |

### 購読: MQTT to ROS 2

| MQTT topic | ROS 2 topic | ROS type | MQTT QoS |
|---|---|---|---|
| `MQTT_PREFIX/drive/wakeup` | `/ROS_PREFIX/drive/wakeup` | `std_msgs/msg/Empty` | `2` |
| `MQTT_PREFIX/drive/sleep` | `/ROS_PREFIX/drive/sleep` | `std_msgs/msg/Empty` | `2` |
| `MQTT_PREFIX/action/event` | `/ROS_PREFIX/action/event` | `std_msgs/msg/String` | `2` |
| `MQTT_PREFIX/record/operate` | `/ROS_PREFIX/record/operate` | `std_msgs/msg/String` | default |
| `MQTT_PREFIX/drive/restart` | `/ROS_PREFIX/drive/restart` | `std_msgs/msg/Empty` | `2` |
| `MQTT_PREFIX/drive/pause` | `/ROS_PREFIX/drive/pause` | `std_msgs/msg/Empty` | `2` |
| `MQTT_PREFIX/drive/run_pos` | `/ROS_PREFIX/drive/run_pos` | `triorb_drive_interface/msg/TriorbRunPos3` | `2` |
| `MQTT_PREFIX/drive/set_pos` | `/ROS_PREFIX/drive/set_pos` | `triorb_drive_interface/msg/TriorbSetPos3` | `2` |
| `MQTT_PREFIX/drive/run_vel` | `/ROS_PREFIX/drive/run_vel` | `triorb_drive_interface/msg/TriorbRunVel3` | `0` |
| `MQTT_PREFIX/drive/stop` | `/ROS_PREFIX/drive/stop` | `std_msgs/msg/Empty` | `2` |
| `MQTT_PREFIX/set/robot/vel_level` | `/ROS_PREFIX/set/robot/vel_level` | `std_msgs/msg/UInt8` | `2` |
| `MQTT_PREFIX/run_slam/set/enable_camera` | `/ROS_PREFIX/run_slam/set/enable_camera` | `std_msgs/msg/Int8MultiArray` | `2` |
| `MQTT_PREFIX/run_slam/set/change_map_file_path` | `/ROS_PREFIX/run_slam/set/change_map_file_path` | `std_msgs/msg/String` | `2` |
| `MQTT_PREFIX/run_slam/set/enter_local_map_file_path` | `/ROS_PREFIX/run_slam/set/enter_local_map_file_path` | `std_msgs/msg/String` | `2` |
| `MQTT_PREFIX/run_slam/set/map_freeze` | `/ROS_PREFIX/run_slam/set/map_freeze` | `std_msgs/msg/Bool` | `2` |
| `MQTT_PREFIX/run_slam/set/marker_only` | `/ROS_PREFIX/run_slam/set/marker_only` | `std_msgs/msg/Bool` | `2` |
| `MQTT_PREFIX/run_slam/set/marker_exclude` | `/ROS_PREFIX/run_slam/set/marker_exclude` | `std_msgs/msg/Bool` | `2` |
| `MQTT_PREFIX/drive/run_lifter` | `/ROS_PREFIX/drive/run_lifter` | `std_msgs/msg/String` | `2` |
| `MQTT_PREFIX/ros2/ping` | `/ROS_PREFIX/ros2/ping` | `std_msgs/msg/String` | `0` |
| `vslam/joy` | `/ROS_PREFIX/vslam/joy` | `std_msgs/msg/String` | `0` |
| `MQTT_PREFIX/triorb/error/add` | `/ROS_PREFIX/triorb/error/add` | `std_msgs/msg/UInt16MultiArray` | `2` |
| `MQTT_PREFIX/triorb/error/str/add` | `/ROS_PREFIX/triorb/error/str/add` | `std_msgs/msg/String` | `2` |
| `MQTT_PREFIX/triorb/error/reset` | `/ROS_PREFIX/triorb/error/reset` | `std_msgs/msg/UInt8` | `2` |
| `MQTT_PREFIX/triorb/amr_pkg_restart/request` | `/ROS_PREFIX/triorb/amr_pkg_restart/request` | `std_msgs/msg/Empty` | `2` |
| `MQTT_PREFIX/nav/route_csv_name` | `/ROS_PREFIX/nav/route_csv_name` | `std_msgs/msg/String` | `2` |
| `MQTT_PREFIX/nav/action` | `/ROS_PREFIX/nav/action` | `std_msgs/msg/String` | `2` |
| `MQTT_PREFIX/triorb/request_nav_state` | `/ROS_PREFIX/triorb/request_nav_state` | `std_msgs/msg/Empty` | `2` |
| `MQTT_PREFIX/path/navigate/set` | `/ROS_PREFIX/path/navigate/set` | `triorb_drive_interface/msg/Route` | `2` |
| `MQTT_PREFIX/tagslam/save/map` | `/ROS_PREFIX/tagslam/save/map` | `std_msgs/msg/String` | `2` |
| `MQTT_PREFIX/tagslam/load/map` | `/ROS_PREFIX/tagslam/load/map` | `std_msgs/msg/String` | `2` |
| `MQTT_PREFIX/tagslam/drive/set_pos` | `/ROS_PREFIX/tagslam/drive/set_pos` | `triorb_drive_interface/msg/TriorbSetPos3` | `2` |
| `MQTT_PREFIX/drive/save_waypoint` | `/ROS_PREFIX/drive/save_waypoint` | `std_msgs/msg/String` | `2` |
| `MQTT_PREFIX/drive/set_life_time` | `/ROS_PREFIX/drive/set_life_time` | `std_msgs/msg/UInt16` | `2` |
| `MQTT_PREFIX/sls/set/brake` | `/ROS_PREFIX/sls/set/brake` | `std_msgs/msg/Bool` | `2` |
| `MQTT_PREFIX/sls/set/field` | `/ROS_PREFIX/sls/set/field` | `std_msgs/msg/UInt8` | `2` |
| `MQTT_PREFIX/collab/drive/stop` | `/ROS_PREFIX/collab/drive/stop` | `std_msgs/msg/Empty` | `2` |

## 協調制御向け追加定義

出典: `submodules/TriOrb-AMR-Package/params/mqtt.collab.workers.local.yaml`

### local: ROS 2 to MQTT

| ROS 2 topic | MQTT topic | ROS type | MQTT QoS |
|---|---|---|---|
| `/ROS_PREFIX/collab/bind/info` | `GROUP_NAME/collab/bind/info` | `triorb_collaboration_interface/msg/ParentBind` | `0` |
| `/ROS_PREFIX/bc/collab/bind/info` | `GROUP_NAME/collab/bind/info` | `triorb_collaboration_interface/msg/ParentBind` | `0` |
| `/ROS_PREFIX/collab/group_pose` | `GROUP_NAME/collab/group_pose` | `triorb_drive_interface/msg/TriorbPos3Stamped` | `0` |
| `/ROS_PREFIX/collab/drive/result` | `GROUP_NAME/collab/drive/result` | `triorb_drive_interface/msg/TriorbRunResultStamped` | `2` |
| `/ROS_PREFIX/collab/vel_max` | `GROUP_NAME/collab/vel_max` | `triorb_drive_interface/msg/TriorbVel3` | `0` |

### local: MQTT to ROS 2

| MQTT topic | ROS 2 topic | ROS type | MQTT QoS |
|---|---|---|---|
| `GROUP_NAME/collab/bind/set_entry` | `/ROS_PREFIX/collab/bind/set_entry` | `triorb_collaboration_interface/msg/ParentBind` | `2` |
| `GROUP_NAME/collab/save_waypoint_hash` | `/ROS_PREFIX/collab/save_waypoint_hash` | `std_msgs/msg/String` | `2` |

出典: `submodules/TriOrb-AMR-Package/params/mqtt.collab.workers.global.yaml`

### global: ROS 2 to MQTT

| ROS 2 topic | MQTT topic | ROS type | MQTT QoS |
|---|---|---|---|
| `/ROS_PREFIX/drive/max_vel` | `GROUP_NAME/collab/max_vel` | `triorb_drive_interface/msg/RobotParams` | `0` |
| `/ROS_PREFIX/drive/result` | `GROUP_NAME/drive/result` | `triorb_drive_interface/msg/TriorbRunResult` | `2` |
| `/ROS_PREFIX/lifter/result` | `GROUP_NAME/collab/lifter/result` | `std_msgs/msg/String` | `2` |
| `/ROS_PREFIX/collab/bind/set_entry` | `GROUP_NAME/collab/bind/set_entry` | `triorb_collaboration_interface/msg/ParentBind` | `2` |
| `/ROS_PREFIX/collab/bind/info` | `GROUP_NAME/collab/bind/info` | `triorb_collaboration_interface/msg/ParentBind` | `0` |
| `/ROS_PREFIX/collab/wakeup` | `GROUP_NAME/collab/wakeup` | `std_msgs/msg/Empty` | `2` |
| `/ROS_PREFIX/collab/sleep` | `GROUP_NAME/collab/sleep` | `std_msgs/msg/Empty` | `2` |
| `/ROS_PREFIX/collab/run_vel` | `GROUP_NAME/collab/run_vel` | `triorb_drive_interface/msg/TriorbRunVel3Stamped` | `0` |
| `/ROS_PREFIX/collab/run_lifter` | `GROUP_NAME/collab/run_lifter` | `std_msgs/msg/String` | `2` |
| `/ROS_PREFIX/collab/robot_pose` | `GROUP_NAME/collab/robot_pose` | `triorb_drive_interface/msg/TriorbPos3Stamped` | `0` |
| `/ROS_PREFIX/collab/robot/status` | `GROUP_NAME/collab/robot/status` | `triorb_static_interface/msg/RobotStatus` | `0` |
| `/ROS_PREFIX/collab/set_life_time` | `GROUP_NAME/collab/set_life_time` | `std_msgs/msg/UInt16` | `2` |
| `/ROS_PREFIX/collab/save_waypoint_hash` | `GROUP_NAME/collab/save_waypoint_hash` | `std_msgs/msg/String` | `2` |
| `/ROS_PREFIX/collab/run_slam/map_file_path` | `GROUP_NAME/collab/run_slam/map_file_path` | `std_msgs/msg/String` | `0` |
| `/ROS_PREFIX/collab/run_slam/map_file_changed` | `GROUP_NAME/collab/run_slam/map_file_changed` | `std_msgs/msg/String` | `2` |
| `/ROS_PREFIX/collab/drive/stop` | `GROUP_NAME/collab/drive/stop` | `std_msgs/msg/Empty` | `2` |
| `/ROS_PREFIX/collab/drive/pause` | `GROUP_NAME/collab/drive/pause` | `std_msgs/msg/Empty` | `2` |
| `/ROS_PREFIX/collab/drive/restart` | `GROUP_NAME/collab/drive/restart` | `std_msgs/msg/Empty` | `2` |
| `/ROS_PREFIX/collab/drive/set_pos` | `GROUP_NAME/collab/drive/set_pos` | `triorb_drive_interface/msg/TriorbSetPos3` | `2` |
| `/ROS_PREFIX/collab/drive/result` | `GROUP_NAME/collab/drive/result` | `triorb_drive_interface/msg/TriorbRunResultStamped` | `2` |
| `/ROS_PREFIX/collab/drive/finish` | `GROUP_NAME/collab/drive/finish` | `std_msgs/msg/Bool` | `2` |
| `/ROS_PREFIX/collab/request/set_pos` | `GROUP_NAME/collab/request/set_pos` | `triorb_drive_interface/msg/TriorbSetPos3` | `2` |
| `/ROS_PREFIX/collab/drive/init_path_follow` | `GROUP_NAME/collab/drive/init_path_follow` | `std_msgs/msg/Empty` | `2` |
| `/ROS_PREFIX/collab/emergency_state` | `GROUP_NAME/collab/emergency_state` | `std_msgs/msg/Bool` | `2` |
| `/ROS_PREFIX/collab/aux/event` | `GROUP_NAME/collab/aux/event` | `std_msgs/msg/String` | `2` |
| `/ROS_PREFIX/sls/change_to_sls_off` | `GROUP_NAME/sls/change_to_sls_off` | `std_msgs/msg/Bool` | `2` |
| `/ROS_PREFIX/collab/drive/estop` | `GROUP_NAME/collab/drive/estop` | `std_msgs/msg/Empty` | `2` |
| `/ROS_PREFIX/triorb/error/reset` | `GROUP_NAME/triorb/error/reset` | `std_msgs/msg/UInt8` | `2` |
| `/ROS_PREFIX/collab/alive` | `GROUP_NAME/collab/alive` | `std_msgs/msg/Header` | `2` |
| `/ROS_PREFIX/triorb/error/str/log` | `GROUP_NAME/triorb/error/str/log` | `std_msgs/msg/String` | `0` |

### global: MQTT to ROS 2

| MQTT topic | ROS 2 topic | ROS type | MQTT QoS |
|---|---|---|---|
| `GROUP_NAME/drive/result` | `/ROS_PREFIX/bc/drive/result` | `triorb_drive_interface/msg/TriorbRunResult` | `2` |
| `GROUP_NAME/collab/joy` | `/ROS_PREFIX/bc/collab/joy` | `sensor_msgs/msg/Joy` | `0` |
| `GROUP_NAME/collab/bind/info` | `/ROS_PREFIX/bc/collab/bind/info` | `triorb_collaboration_interface/msg/ParentBind` | `0` |
| `GROUP_NAME/collab/bind/set_entry` | `/ROS_PREFIX/bc/collab/bind/set` | `triorb_collaboration_interface/msg/ParentBind` | `2` |
| `GROUP_NAME/collab/max_vel` | `/ROS_PREFIX/bc/collab/max_vel` | `triorb_drive_interface/msg/RobotParams` | `0` |
| `GROUP_NAME/collab/wakeup` | `/ROS_PREFIX/drive/wakeup` | `std_msgs/msg/Empty` | `2` |
| `GROUP_NAME/collab/sleep` | `/ROS_PREFIX/drive/sleep` | `std_msgs/msg/Empty` | `2` |
| `GROUP_NAME/collab/run_vel` | `/ROS_PREFIX/bc/collab/run_vel` | `triorb_drive_interface/msg/TriorbRunVel3Stamped` | `0` |
| `GROUP_NAME/collab/run_lifter` | `/ROS_PREFIX/bc/collab/run_lifter` | `std_msgs/msg/String` | `2` |
| `GROUP_NAME/collab/robot_pose` | `/ROS_PREFIX/bc/collab/robot_pose` | `triorb_drive_interface/msg/TriorbPos3Stamped` | `0` |
| `GROUP_NAME/collab/robot/status` | `/ROS_PREFIX/bc/collab/robot/status` | `triorb_static_interface/msg/RobotStatus` | `0` |
| `GROUP_NAME/collab/set_life_time` | `/ROS_PREFIX/bc/collab/set_life_time` | `std_msgs/msg/UInt16` | `2` |
| `GROUP_NAME/collab/save_waypoint_hash` | `/ROS_PREFIX/bc/collab/save_waypoint_hash` | `std_msgs/msg/String` | `2` |
| `GROUP_NAME/collab/run_slam/map_file_path` | `/ROS_PREFIX/bc/collab/run_slam/map_file_path` | `std_msgs/msg/String` | `0` |
| `GROUP_NAME/collab/run_slam/map_file_changed` | `/ROS_PREFIX/bc/collab/run_slam/map_file_changed` | `std_msgs/msg/String` | `2` |
| `GROUP_NAME/collab/last_will` | `/ROS_PREFIX/bc/collab/last_will` | `std_msgs/msg/String` | `2` |
| `GROUP_NAME/collab/drive/stop` | `/ROS_PREFIX/bc/collab/drive/stop` | `std_msgs/msg/Empty` | `2` |
| `GROUP_NAME/collab/drive/pause` | `/ROS_PREFIX/bc/collab/drive/pause` | `std_msgs/msg/Empty` | `2` |
| `GROUP_NAME/collab/drive/restart` | `/ROS_PREFIX/bc/collab/drive/restart` | `std_msgs/msg/Empty` | `2` |
| `GROUP_NAME/collab/drive/set_pos` | `/ROS_PREFIX/bc/collab/drive/set_pos` | `triorb_drive_interface/msg/TriorbSetPos3` | `2` |
| `GROUP_NAME/collab/drive/result` | `/ROS_PREFIX/bc/collab/drive/result` | `triorb_drive_interface/msg/TriorbRunResultStamped` | `2` |
| `GROUP_NAME/collab/drive/finish` | `/ROS_PREFIX/bc/collab/drive/finish` | `std_msgs/msg/Bool` | `2` |
| `GROUP_NAME/collab/lifter/result` | `/ROS_PREFIX/bc/collab/lifter/result` | `std_msgs/msg/String` | `2` |
| `GROUP_NAME/collab/request/set_pos` | `/ROS_PREFIX/bc/collab/request/set_pos` | `triorb_drive_interface/msg/TriorbSetPos3` | `2` |
| `GROUP_NAME/collab/drive/init_path_follow` | `/ROS_PREFIX/bc/collab/drive/init_path_follow` | `std_msgs/msg/Empty` | `2` |
| `GROUP_NAME/collab/emergency_state` | `/ROS_PREFIX/bc/collab/emergency_state` | `std_msgs/msg/Bool` | `2` |
| `GROUP_NAME/collab/aux/event` | `/ROS_PREFIX/bc/collab/aux/event` | `std_msgs/msg/String` | `2` |
| `GROUP_NAME/sls/change_to_sls_off` | `/ROS_PREFIX/bc/sls/change_to_sls_off` | `std_msgs/msg/Bool` | `2` |
| `GROUP_NAME/collab/drive/estop` | `/ROS_PREFIX/bc/collab/drive/estop` | `std_msgs/msg/Empty` | `2` |
| `GROUP_NAME/triorb/error/reset` | `/ROS_PREFIX/bc/triorb/error/reset` | `std_msgs/msg/UInt8` | `2` |
| `GROUP_NAME/collab/alive` | `/ROS_PREFIX/bc/collab/alive` | `std_msgs/msg/Header` | `2` |
| `GROUP_NAME/triorb/error/str/log` | `/ROS_PREFIX/bc/triorb/error/str/log` | `std_msgs/msg/String` | `0` |

## 一時ビーコン定義

出典: `submodules/TriOrb-AMR-Package/params/tmp_beacon.params.ros2.yaml`

| ROS 2 topic | MQTT topic | ROS type | MQTT QoS |
|---|---|---|---|
| `/triorb/beacon` | `triorb/beacon` | `std_msgs/msg/String` | `0` |
