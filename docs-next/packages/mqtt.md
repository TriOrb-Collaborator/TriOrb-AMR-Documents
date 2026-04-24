# MQTT API

```{warning}
MQTT API はアーリープレビューです。現時点では正式な外部仕様書ではなく、
TriOrb BASE の起動スクリプトで読み込まれる ROS 2 - MQTT ブリッジ設定から確認できる topic を掲載しています。
topic 名、payload、QoS は今後変更される可能性があります。
```

MQTT API は、TriOrb BASE 内部の ROS 2 topic を MQTT broker 経由で送受信するためのインタフェースです。
`ros2mqtt` に定義された ROS 2 topic は MQTT へ配信され、`mqtt2ros` に定義された MQTT topic は購読されて
対応する ROS 2 topic へ publish されます。

## broker と起動構成

実機では用途ごとに異なる MQTT broker / port が使われます。

| 用途 | broker | TCP port | WebSocket | Dashboard | 主な起動経路 |
|---|---|---:|---:|---:|---|
| 標準・ローカル連携 | local EMQX | `1883` | `8083` | `18083` | 標準 MQTT bridge、協調 local bridge、beacon bridge |
| 協調制御クラスタ | EMQX cluster | `1883 + PORT_OFFSET`。既定は `1893` | `8083 + PORT_OFFSET`。既定は `8093` | `18083 + PORT_OFFSET`。既定は `18093` | 協調 global bridge |

外部クライアントから接続できるかどうかは、起動構成、ネットワーク設定、firewall、broker の公開設定に依存します。

## topic prefix

topic 名に含まれる placeholder は実行時に置換されます。

| placeholder | 意味 |
|---|---|
| `ROS_PREFIX` | ROS 2 topic prefix。標準起動では `/params/ROS_PREFIX` から読み込まれます。 |
| `MQTT_PREFIX` | MQTT topic prefix。標準起動では `/params/ROS_PREFIX`、協調制御ではホスト名由来の prefix が使われます。 |
| `GROUP_NAME` | 協調制御用のグループ名です。 |
| `PORT_OFFSET` | 協調制御クラスタ broker の port offset です。既定値は `10` です。 |

例えば `ROS_PREFIX=triorb01` の場合、標準起動では `MQTT_PREFIX/robot/status` は
`triorb01/robot/status` として扱われます。

## payload

payload は `mqtt_client` のブリッジ実装に従います。`primitive: true` の定義では、文字列、数値、
真偽値などの primitive payload が対応する ROS 2 message へ変換されます。非 primitive の定義では、
ROS message の serialized payload と message type 情報を使うため、一般の MQTT クライアントから直接扱う用途では
互換性に注意してください。

## local broker: port 1883

標準機能、協調制御のローカル bridge、beacon bridge は local broker の `1883` 番ポートを使います。

### 標準 bridge: ROS 2 to MQTT

| ROS 2 topic | MQTT topic | ROS type | MQTT QoS |
|---|---|---|---|
| <a href="triorb_drive_pico/API.html"><code>/ROS_PREFIX/robot/status</code></a> | `MQTT_PREFIX/robot/status` | `triorb_static_interface/msg/RobotStatus` | `0` |
| `/ROS_PREFIX/vslam/rig_tf` | `MQTT_PREFIX/vslam/rig_tf` | `geometry_msgs/msg/TransformStamped` | `0` |
| `/ROS_PREFIX/vslam/robot_pose` | `MQTT_PREFIX/vslam/robot_pose` | `triorb_drive_interface/msg/TriorbPos3` | `0` |
| `/ROS_PREFIX/action/event` | `MQTT_PREFIX/action/event` | `std_msgs/msg/String` | `2` |
| <a href="triorb_navigation/API.html"><code>/ROS_PREFIX/drive/state</code></a> | `MQTT_PREFIX/drive/state` | `triorb_drive_interface/msg/TriorbRunState` | `2` |
| <a href="triorb_navigation/API.html"><code>/ROS_PREFIX/drive/result</code></a> | `MQTT_PREFIX/drive/result` | `triorb_drive_interface/msg/TriorbRunResult` | `2` |
| `/ROS_PREFIX/robot/vel_level` | `MQTT_PREFIX/robot/vel_level` | `std_msgs/msg/UInt8` | `0` |
| <a href="visual_slam/API.html"><code>/ROS_PREFIX/run_slam/enable_camera</code></a> | `MQTT_PREFIX/run_slam/enable_camera` | `std_msgs/msg/Int8MultiArray` | `0` |
| <a href="visual_slam/API.html"><code>/ROS_PREFIX/run_slam/map_file_path</code></a> | `MQTT_PREFIX/run_slam/map_file_path` | `std_msgs/msg/String` | `0` |
| <a href="visual_slam/API.html"><code>/ROS_PREFIX/run_slam/local_map_file_path</code></a> | `MQTT_PREFIX/run_slam/local_map_file_path` | `std_msgs/msg/String` | `0` |
| <a href="visual_slam/API.html"><code>/ROS_PREFIX/run_slam/map_freeze</code></a> | `MQTT_PREFIX/run_slam/map_freeze` | `std_msgs/msg/Bool` | `0` |
| <a href="visual_slam/API.html"><code>/ROS_PREFIX/run_slam/marker_only</code></a> | `MQTT_PREFIX/run_slam/marker_only` | `std_msgs/msg/Bool` | `0` |
| <a href="visual_slam/API.html"><code>/ROS_PREFIX/run_slam/marker_exclude</code></a> | `MQTT_PREFIX/run_slam/marker_exclude` | `std_msgs/msg/Bool` | `0` |
| <a href="visual_slam/API.html"><code>/ROS_PREFIX/run_slam/map_file_changed</code></a> | `MQTT_PREFIX/run_slam/map_file_changed` | `std_msgs/msg/String` | `2` |
| <a href="triorb_drive_pico/API.html"><code>/ROS_PREFIX/lifter/result</code></a> | `MQTT_PREFIX/lifter/result` | `std_msgs/msg/String` | `2` |
| <a href="visual_slam/API.html"><code>/ROS_PREFIX/run_slam/keyframe_landmarks</code></a> | `MQTT_PREFIX/run_slam/keyframe_landmarks` | `triorb_slam_interface/msg/UInt32MultiArrayStamped` | `0` |
| <a href="visual_slam/API.html"><code>/ROS_PREFIX/run_slam/matched_landmarks</code></a> | `MQTT_PREFIX/run_slam/matched_landmarks` | `triorb_slam_interface/msg/UInt32MultiArrayStamped` | `0` |
| `/ROS_PREFIX/ros2/pong` | `MQTT_PREFIX/ros2/pong` | `std_msgs/msg/String` | `0` |
| <a href="triorb_drive_pico/API.html"><code>/ROS_PREFIX/triorb/version/drive</code></a> | `MQTT_PREFIX/triorb/version/drive` | `std_msgs/msg/String` | `0` |
| <a href="triorb_drive_pico/API.html"><code>/ROS_PREFIX/triorb/version/pico</code></a> | `MQTT_PREFIX/triorb/version/pico` | `std_msgs/msg/String` | `0` |
| <a href="triorb_drive_pico/API.html"><code>/ROS_PREFIX/triorb/version/core</code></a> | `MQTT_PREFIX/triorb/version/core` | `std_msgs/msg/String` | `0` |
| `/ROS_PREFIX/triorb/error/log` | `MQTT_PREFIX/triorb/error/log` | `std_msgs/msg/UInt16MultiArray` | `0` |
| `/ROS_PREFIX/triorb/error/str/log` | `MQTT_PREFIX/triorb/error/str/log` | `std_msgs/msg/String` | `0` |
| `/ROS_PREFIX/triorb/warn/log` | `MQTT_PREFIX/triorb/warn/log` | `std_msgs/msg/UInt16MultiArray` | `0` |
| `/ROS_PREFIX/triorb/warn/str/log` | `MQTT_PREFIX/triorb/warn/str/log` | `std_msgs/msg/String` | `0` |
| <a href="triorb_navigation_manager/API.html"><code>/ROS_PREFIX/triorb/nav/state</code></a> | `MQTT_PREFIX/triorb/nav/state` | `std_msgs/msg/Int32MultiArray` | `2` |
| <a href="triorb_navigation_manager/API.html"><code>/ROS_PREFIX/nav/handling_task_csv_name</code></a> | `MQTT_PREFIX/nav/handling_task_csv_name` | `std_msgs/msg/String` | `2` |
| <a href="triorb_navigation_manager/API.html"><code>/ROS_PREFIX/triorb/nav/result</code></a> | `MQTT_PREFIX/triorb/nav/result` | `std_msgs/msg/String` | `2` |
| <a href="triorb_tagslam_manager/API.html"><code>/ROS_PREFIX/tagslam/rig_tf</code></a> | `MQTT_PREFIX/tagslam/rig_tf` | `geometry_msgs/msg/TransformStamped` | `0` |
| <a href="triorb_tagslam_manager/API.html"><code>/ROS_PREFIX/tagslam/tag_tf</code></a> | `MQTT_PREFIX/tagslam/tag_tf` | `geometry_msgs/msg/TransformStamped` | `0` |
| <a href="triorb_tagslam_manager/API.html"><code>/ROS_PREFIX/tagslam/state</code></a> | `MQTT_PREFIX/tagslam/state` | `std_msgs/msg/UInt8MultiArray` | `0` |
| <a href="triorb_tagslam_manager/API.html"><code>/ROS_PREFIX/tagslam/status</code></a> | `MQTT_PREFIX/tagslam/status` | `triorb_slam_interface/msg/SlamStatus` | `0` |
| `/ROS_PREFIX/triorb/text_voice` | `MQTT_PREFIX/triorb/text_voice` | `std_msgs/msg/String` | `0` |
| <a href="triorb_navigation_manager/API.html"><code>/ROS_PREFIX/drive/pause</code></a> | `MQTT_PREFIX/drive/pause` | `std_msgs/msg/Empty` | `2` |

### 標準 bridge: MQTT to ROS 2

| MQTT topic | ROS 2 topic | ROS type | MQTT QoS |
|---|---|---|---|
| `MQTT_PREFIX/drive/wakeup` | <a href="triorb_drive_pico/API.html"><code>/ROS_PREFIX/drive/wakeup</code></a> | `std_msgs/msg/Empty` | `2` |
| `MQTT_PREFIX/drive/sleep` | <a href="triorb_drive_pico/API.html"><code>/ROS_PREFIX/drive/sleep</code></a> | `std_msgs/msg/Empty` | `2` |
| `MQTT_PREFIX/action/event` | <a href="triorb_navigation_manager/API.html"><code>/ROS_PREFIX/action/event</code></a> | `std_msgs/msg/String` | `2` |
| `MQTT_PREFIX/record/operate` | `/ROS_PREFIX/record/operate` | `std_msgs/msg/String` | `default` |
| `MQTT_PREFIX/drive/restart` | <a href="triorb_navigation_manager/API.html"><code>/ROS_PREFIX/drive/restart</code></a> | `std_msgs/msg/Empty` | `2` |
| `MQTT_PREFIX/drive/pause` | <a href="triorb_navigation_manager/API.html"><code>/ROS_PREFIX/drive/pause</code></a> | `std_msgs/msg/Empty` | `2` |
| `MQTT_PREFIX/drive/run_pos` | <a href="triorb_navigation_manager/API.html"><code>/ROS_PREFIX/drive/run_pos</code></a> | `triorb_drive_interface/msg/TriorbRunPos3` | `2` |
| `MQTT_PREFIX/drive/set_pos` | <a href="triorb_navigation/API.html"><code>/ROS_PREFIX/drive/set_pos</code></a> | `triorb_drive_interface/msg/TriorbSetPos3` | `2` |
| `MQTT_PREFIX/drive/run_vel` | <a href="triorb_drive_pico/API.html"><code>/ROS_PREFIX/drive/run_vel</code></a> | `triorb_drive_interface/msg/TriorbRunVel3` | `0` |
| `MQTT_PREFIX/drive/stop` | <a href="triorb_drive_pico/API.html"><code>/ROS_PREFIX/drive/stop</code></a> | `std_msgs/msg/Empty` | `2` |
| `MQTT_PREFIX/set/robot/vel_level` | `/ROS_PREFIX/set/robot/vel_level` | `std_msgs/msg/UInt8` | `2` |
| `MQTT_PREFIX/run_slam/set/enable_camera` | <a href="visual_slam/API.html"><code>/ROS_PREFIX/run_slam/set/enable_camera</code></a> | `std_msgs/msg/Int8MultiArray` | `2` |
| `MQTT_PREFIX/run_slam/set/change_map_file_path` | <a href="visual_slam/API.html"><code>/ROS_PREFIX/run_slam/set/change_map_file_path</code></a> | `std_msgs/msg/String` | `2` |
| `MQTT_PREFIX/run_slam/set/enter_local_map_file_path` | <a href="visual_slam/API.html"><code>/ROS_PREFIX/run_slam/set/enter_local_map_file_path</code></a> | `std_msgs/msg/String` | `2` |
| `MQTT_PREFIX/run_slam/set/map_freeze` | <a href="visual_slam/API.html"><code>/ROS_PREFIX/run_slam/set/map_freeze</code></a> | `std_msgs/msg/Bool` | `2` |
| `MQTT_PREFIX/run_slam/set/marker_only` | <a href="visual_slam/API.html"><code>/ROS_PREFIX/run_slam/set/marker_only</code></a> | `std_msgs/msg/Bool` | `2` |
| `MQTT_PREFIX/run_slam/set/marker_exclude` | <a href="visual_slam/API.html"><code>/ROS_PREFIX/run_slam/set/marker_exclude</code></a> | `std_msgs/msg/Bool` | `2` |
| `MQTT_PREFIX/drive/run_lifter` | <a href="triorb_drive_pico/API.html"><code>/ROS_PREFIX/drive/run_lifter</code></a> | `std_msgs/msg/String` | `2` |
| `MQTT_PREFIX/ros2/ping` | `/ROS_PREFIX/ros2/ping` | `std_msgs/msg/String` | `0` |
| `vslam/joy` | `/ROS_PREFIX/vslam/joy` | `std_msgs/msg/String` | `0` |
| `MQTT_PREFIX/triorb/error/add` | `/ROS_PREFIX/triorb/error/add` | `std_msgs/msg/UInt16MultiArray` | `2` |
| `MQTT_PREFIX/triorb/error/str/add` | <a href="triorb_navigation_manager/API.html"><code>/ROS_PREFIX/triorb/error/str/add</code></a> | `std_msgs/msg/String` | `2` |
| `MQTT_PREFIX/triorb/error/reset` | `/ROS_PREFIX/triorb/error/reset` | `std_msgs/msg/UInt8` | `2` |
| `MQTT_PREFIX/triorb/amr_pkg_restart/request` | `/ROS_PREFIX/triorb/amr_pkg_restart/request` | `std_msgs/msg/Empty` | `2` |
| `MQTT_PREFIX/nav/route_csv_name` | <a href="triorb_navigation_manager/API.html"><code>/ROS_PREFIX/nav/route_csv_name</code></a> | `std_msgs/msg/String` | `2` |
| `MQTT_PREFIX/nav/action` | <a href="triorb_navigation_manager/API.html"><code>/ROS_PREFIX/nav/action</code></a> | `std_msgs/msg/String` | `2` |
| `MQTT_PREFIX/triorb/request_nav_state` | <a href="triorb_navigation_manager/API.html"><code>/ROS_PREFIX/triorb/request_nav_state</code></a> | `std_msgs/msg/Empty` | `2` |
| `MQTT_PREFIX/path/navigate/set` | `/ROS_PREFIX/path/navigate/set` | `triorb_drive_interface/msg/Route` | `2` |
| `MQTT_PREFIX/tagslam/save/map` | <a href="triorb_tagslam_manager/API.html"><code>/ROS_PREFIX/tagslam/save/map</code></a> | `std_msgs/msg/String` | `2` |
| `MQTT_PREFIX/tagslam/load/map` | <a href="triorb_tagslam_manager/API.html"><code>/ROS_PREFIX/tagslam/load/map</code></a> | `std_msgs/msg/String` | `2` |
| `MQTT_PREFIX/tagslam/drive/set_pos` | <a href="triorb_navigation_manager/API.html"><code>/ROS_PREFIX/tagslam/drive/set_pos</code></a> | `triorb_drive_interface/msg/TriorbSetPos3` | `2` |
| `MQTT_PREFIX/drive/save_waypoint` | `/ROS_PREFIX/drive/save_waypoint` | `std_msgs/msg/String` | `2` |
| `MQTT_PREFIX/drive/set_life_time` | <a href="triorb_drive_pico/API.html"><code>/ROS_PREFIX/drive/set_life_time</code></a> | `std_msgs/msg/UInt16` | `2` |
| `MQTT_PREFIX/sls/set/brake` | <a href="triorb_navigation_manager/API.html"><code>/ROS_PREFIX/sls/set/brake</code></a> | `std_msgs/msg/Bool` | `2` |
| `MQTT_PREFIX/sls/set/field` | <a href="triorb_navigation_manager/API.html"><code>/ROS_PREFIX/sls/set/field</code></a> | `std_msgs/msg/UInt8` | `2` |
| `MQTT_PREFIX/collab/drive/stop` | <a href="triorb_gamepad/API.html"><code>/ROS_PREFIX/collab/drive/stop</code></a> | `std_msgs/msg/Empty` | `2` |

### 協調 local bridge: ROS 2 to MQTT

| ROS 2 topic | MQTT topic | ROS type | MQTT QoS |
|---|---|---|---|
| `/ROS_PREFIX/collab/bind/info` | `GROUP_NAME/collab/bind/info` | `triorb_collaboration_interface/msg/ParentBind` | `0` |
| `/ROS_PREFIX/bc/collab/bind/info` | `GROUP_NAME/collab/bind/info` | `triorb_collaboration_interface/msg/ParentBind` | `0` |
| `/ROS_PREFIX/collab/group_pose` | `GROUP_NAME/collab/group_pose` | `triorb_drive_interface/msg/TriorbPos3Stamped` | `0` |
| `/ROS_PREFIX/collab/drive/result` | `GROUP_NAME/collab/drive/result` | `triorb_drive_interface/msg/TriorbRunResultStamped` | `2` |
| `/ROS_PREFIX/collab/vel_max` | `GROUP_NAME/collab/vel_max` | `triorb_drive_interface/msg/TriorbVel3` | `0` |

### 協調 local bridge: MQTT to ROS 2

| MQTT topic | ROS 2 topic | ROS type | MQTT QoS |
|---|---|---|---|
| `GROUP_NAME/collab/bind/set_entry` | `/ROS_PREFIX/collab/bind/set_entry` | `triorb_collaboration_interface/msg/ParentBind` | `2` |
| `GROUP_NAME/collab/save_waypoint_hash` | `/ROS_PREFIX/collab/save_waypoint_hash` | `std_msgs/msg/String` | `2` |

### beacon bridge: ROS 2 to MQTT

| ROS 2 topic | MQTT topic | ROS type | MQTT QoS |
|---|---|---|---|
| `/triorb/beacon2` | `MQTT_PREFIX/triorb/beacon` | `std_msgs/msg/String` | `0` |
| `/group/beacon2` | `MQTT_PREFIX/group/beacon` | `std_msgs/msg/String` | `0` |

## cluster broker: port 1883 + PORT_OFFSET

協調制御の global bridge は EMQX cluster に接続します。既定では `PORT_OFFSET=10` のため、
TCP port は `1893` です。

### 協調 global bridge: ROS 2 to MQTT

| ROS 2 topic | MQTT topic | ROS type | MQTT QoS |
|---|---|---|---|
| <a href="triorb_drive_pico/API.html"><code>/ROS_PREFIX/drive/max_vel</code></a> | `GROUP_NAME/collab/max_vel` | `triorb_drive_interface/msg/RobotParams` | `0` |
| <a href="triorb_navigation/API.html"><code>/ROS_PREFIX/drive/result</code></a> | `GROUP_NAME/drive/result` | `triorb_drive_interface/msg/TriorbRunResult` | `2` |
| <a href="triorb_drive_pico/API.html"><code>/ROS_PREFIX/lifter/result</code></a> | `GROUP_NAME/collab/lifter/result` | `std_msgs/msg/String` | `2` |
| `/ROS_PREFIX/collab/bind/set_entry` | `GROUP_NAME/collab/bind/set_entry` | `triorb_collaboration_interface/msg/ParentBind` | `2` |
| `/ROS_PREFIX/collab/bind/info` | `GROUP_NAME/collab/bind/info` | `triorb_collaboration_interface/msg/ParentBind` | `0` |
| <a href="triorb_gamepad/API.html"><code>/ROS_PREFIX/collab/wakeup</code></a> | `GROUP_NAME/collab/wakeup` | `std_msgs/msg/Empty` | `2` |
| <a href="triorb_gamepad/API.html"><code>/ROS_PREFIX/collab/sleep</code></a> | `GROUP_NAME/collab/sleep` | `std_msgs/msg/Empty` | `2` |
| <a href="triorb_gamepad/API.html"><code>/ROS_PREFIX/collab/run_vel</code></a> | `GROUP_NAME/collab/run_vel` | `triorb_drive_interface/msg/TriorbRunVel3Stamped` | `0` |
| <a href="triorb_navigation_manager/API.html"><code>/ROS_PREFIX/collab/run_lifter</code></a> | `GROUP_NAME/collab/run_lifter` | `std_msgs/msg/String` | `2` |
| `/ROS_PREFIX/collab/robot_pose` | `GROUP_NAME/collab/robot_pose` | `triorb_drive_interface/msg/TriorbPos3Stamped` | `0` |
| `/ROS_PREFIX/collab/robot/status` | `GROUP_NAME/collab/robot/status` | `triorb_static_interface/msg/RobotStatus` | `0` |
| <a href="triorb_gamepad/API.html"><code>/ROS_PREFIX/collab/set_life_time</code></a> | `GROUP_NAME/collab/set_life_time` | `std_msgs/msg/UInt16` | `2` |
| `/ROS_PREFIX/collab/save_waypoint_hash` | `GROUP_NAME/collab/save_waypoint_hash` | `std_msgs/msg/String` | `2` |
| `/ROS_PREFIX/collab/run_slam/map_file_path` | `GROUP_NAME/collab/run_slam/map_file_path` | `std_msgs/msg/String` | `0` |
| `/ROS_PREFIX/collab/run_slam/map_file_changed` | `GROUP_NAME/collab/run_slam/map_file_changed` | `std_msgs/msg/String` | `2` |
| <a href="triorb_gamepad/API.html"><code>/ROS_PREFIX/collab/drive/stop</code></a> | `GROUP_NAME/collab/drive/stop` | `std_msgs/msg/Empty` | `2` |
| `/ROS_PREFIX/collab/drive/pause` | `GROUP_NAME/collab/drive/pause` | `std_msgs/msg/Empty` | `2` |
| `/ROS_PREFIX/collab/drive/restart` | `GROUP_NAME/collab/drive/restart` | `std_msgs/msg/Empty` | `2` |
| `/ROS_PREFIX/collab/drive/set_pos` | `GROUP_NAME/collab/drive/set_pos` | `triorb_drive_interface/msg/TriorbSetPos3` | `2` |
| `/ROS_PREFIX/collab/drive/result` | `GROUP_NAME/collab/drive/result` | `triorb_drive_interface/msg/TriorbRunResultStamped` | `2` |
| `/ROS_PREFIX/collab/drive/finish` | `GROUP_NAME/collab/drive/finish` | `std_msgs/msg/Bool` | `2` |
| <a href="triorb_navigation_manager/API.html"><code>/ROS_PREFIX/collab/request/set_pos</code></a> | `GROUP_NAME/collab/request/set_pos` | `triorb_drive_interface/msg/TriorbSetPos3` | `2` |
| <a href="triorb_navigation_manager/API.html"><code>/ROS_PREFIX/collab/drive/init_path_follow</code></a> | `GROUP_NAME/collab/drive/init_path_follow` | `std_msgs/msg/Empty` | `2` |
| `/ROS_PREFIX/collab/emergency_state` | `GROUP_NAME/collab/emergency_state` | `std_msgs/msg/Bool` | `2` |
| `/ROS_PREFIX/collab/aux/event` | `GROUP_NAME/collab/aux/event` | `std_msgs/msg/String` | `2` |
| `/ROS_PREFIX/sls/change_to_sls_off` | `GROUP_NAME/sls/change_to_sls_off` | `std_msgs/msg/Bool` | `2` |
| `/ROS_PREFIX/collab/drive/estop` | `GROUP_NAME/collab/drive/estop` | `std_msgs/msg/Empty` | `2` |
| `/ROS_PREFIX/triorb/error/reset` | `GROUP_NAME/triorb/error/reset` | `std_msgs/msg/UInt8` | `2` |
| <a href="triorb_sick_plc_wrapper/API.html"><code>/ROS_PREFIX/collab/alive</code></a> | `GROUP_NAME/collab/alive` | `std_msgs/msg/Header` | `2` |
| `/ROS_PREFIX/triorb/error/str/log` | `GROUP_NAME/triorb/error/str/log` | `std_msgs/msg/String` | `0` |

### 協調 global bridge: MQTT to ROS 2

| MQTT topic | ROS 2 topic | ROS type | MQTT QoS |
|---|---|---|---|
| `GROUP_NAME/drive/result` | `/ROS_PREFIX/bc/drive/result` | `triorb_drive_interface/msg/TriorbRunResult` | `2` |
| `GROUP_NAME/collab/joy` | `/ROS_PREFIX/bc/collab/joy` | `sensor_msgs/msg/Joy` | `0` |
| `GROUP_NAME/collab/bind/info` | `/ROS_PREFIX/bc/collab/bind/info` | `triorb_collaboration_interface/msg/ParentBind` | `0` |
| `GROUP_NAME/collab/bind/set_entry` | `/ROS_PREFIX/bc/collab/bind/set` | `triorb_collaboration_interface/msg/ParentBind` | `2` |
| `GROUP_NAME/collab/max_vel` | `/ROS_PREFIX/bc/collab/max_vel` | `triorb_drive_interface/msg/RobotParams` | `0` |
| `GROUP_NAME/collab/wakeup` | <a href="triorb_drive_pico/API.html"><code>/ROS_PREFIX/drive/wakeup</code></a> | `std_msgs/msg/Empty` | `2` |
| `GROUP_NAME/collab/sleep` | <a href="triorb_drive_pico/API.html"><code>/ROS_PREFIX/drive/sleep</code></a> | `std_msgs/msg/Empty` | `2` |
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
| `GROUP_NAME/collab/aux/event` | <a href="triorb_snr_mux_driver/API.html"><code>/ROS_PREFIX/bc/collab/aux/event</code></a> | `std_msgs/msg/String` | `2` |
| `GROUP_NAME/sls/change_to_sls_off` | `/ROS_PREFIX/bc/sls/change_to_sls_off` | `std_msgs/msg/Bool` | `2` |
| `GROUP_NAME/collab/drive/estop` | `/ROS_PREFIX/bc/collab/drive/estop` | `std_msgs/msg/Empty` | `2` |
| `GROUP_NAME/triorb/error/reset` | `/ROS_PREFIX/bc/triorb/error/reset` | `std_msgs/msg/UInt8` | `2` |
| `GROUP_NAME/collab/alive` | `/ROS_PREFIX/bc/collab/alive` | `std_msgs/msg/Header` | `2` |
| `GROUP_NAME/triorb/error/str/log` | `/ROS_PREFIX/bc/triorb/error/str/log` | `std_msgs/msg/String` | `0` |
