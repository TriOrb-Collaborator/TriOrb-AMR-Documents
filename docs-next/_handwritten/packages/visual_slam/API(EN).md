## Overview
This page summarizes the ROS 2 topics published and subscribed by the
`/run_slam` node inside `triorb_visual_slam`.

## Interface List

### Publishers

#### Camera pose output
- Topic: `/run_slam/camera_pose`
- Type: `nav_msgs::msg::Odometry`
- Note: Estimated camera pose.

#### Keyframe output
- Topic: `/run_slam/keyframes`, `/run_slam/keyframes_2d`
- Type: `geometry_msgs::msg::PoseArray`
- Note: Publishes keyframe arrays and their 2D projected representation.

#### Landmark match information
- Topic: `/run_slam/keyframe_landmarks`, `/run_slam/matched_landmarks`
- Type: `triorb_slam_interface::msg::UInt32MultiArrayStamped`
- Note: Publishes the number of landmarks per keyframe and the number of currently matched landmarks.

#### Matched feature points
- Topic: `/run_slam/matched_points`
- Type: `triorb_slam_interface::msg::PointArrayStamped`
- Note: Publishes matched 3D point clouds.

#### Detailed pose-estimation diagnostics
- Topic: `/run_slam/camera_pose_dev`
- Type: `triorb_slam_interface::msg::PoseDevStamped`
- Note: Diagnostic pose-estimation result with a `valid` flag.

#### Per-camera and multi-camera pose information
- Topic: `/run_slam/matched_landmarks_per_camera`, `/run_slam/cameras_pose`
- Type: `triorb_slam_interface::msg::CamerasLandmarkInfo`, `triorb_slam_interface::msg::CamerasPose`
- Note: Publishes per-camera landmark information and combined multi-camera poses.

#### SLAM status
- Topic: `/run_slam/status`
- Type: `triorb_slam_interface::msg::SlamStatus`
- Note: SLAM state including `map_name` and `state` bits (`bit0`: map fixed, `bit1`: localized).

#### Localization reliability
- Topic: `/run_slam/reliability`
- Type: `std_msgs::msg::Float32`
- Note: Estimated localization reliability derived from the number of matched landmarks.

#### Active camera state
- Topic: `/run_slam/enable_camera`
- Type: `std_msgs::msg::Int8MultiArray`
- Note: Current enabled/disabled state of each camera.

#### Marker mode state
- Topic: `/run_slam/marker_only`, `/run_slam/marker_exclude`
- Type: `std_msgs::msg::Bool`
- Note: Current marker-only and marker-exclusion state.

#### Map file state
- Topic: `/run_slam/map_file_path`, `/run_slam/map_file_changed`, `/run_slam/local_map_file_path`
- Type: `std_msgs::msg::String`
- Note: Current map file, change notification, and local-map file state.

#### Current keyframe information
- Topic: `/run_slam/current_keyframes`
- Type: `triorb_slam_interface::msg::KeyframeArray`
- Note: Current keyframe information held by the node.

#### Map-freeze state
- Topic: `/run_slam/map_freeze`
- Type: `std_msgs::msg::Bool`
- Note: Whether map-freeze mode is active.

#### Error notification
- Topic: `/triorb/error/str/add`
- Type: `std_msgs::msg::String`
- Note: Publishes error messages.

#### Warning notification
- Topic: `/triorb/warn/str/add`
- Type: `std_msgs::msg::String`
- Note: Publishes warning messages.

### Subscribers

#### Enable-camera switch
- Topic: `/run_slam/set/enable_camera`
- Type: `std_msgs::msg::Int8MultiArray`
- Note: Switches the enabled/disabled state of each camera.

#### Feature-mask settings
- Topic: `/run_slam/set/mask_positive`, `/run_slam/set/mask_negative`
- Type: `triorb_slam_interface::msg::XyArrayStamped`
- Note: Sets allowed and excluded feature masks.

#### Clear masks
- Topic: `/run_slam/set/clear_mask_all`
- Type: `std_msgs::msg::Empty`
- Note: Clears all feature masks.

#### Save mask YAML
- Topic: `/run_slam/set/save_mask_to_yaml`
- Type: `std_msgs::msg::Empty`
- Note: Saves the current mask configuration as YAML.

#### Marker-usage settings
- Topic: `/run_slam/set/marker_only`, `/run_slam/set/marker_exclude`
- Type: `std_msgs::msg::Bool`
- Note: Switches marker-only and marker-exclusion behavior.

#### Map-file switching
- Topic: `/run_slam/set/change_map_file_path`, `/run_slam/set/enter_local_map_file_path`
- Type: `std_msgs::msg::String`
- Note: Switches the active map file or local map file.

#### Map-freeze switching
- Topic: `/run_slam/set/map_freeze`
- Type: `std_msgs::msg::Bool`
- Note: Enables or disables map-freeze mode.

#### Manual relocalization request
- Topic: `/run_slam/set/manual_keyframes`
- Type: `triorb_slam_interface::msg::KeyframeArray`
- Note: Requests relocalization from manually supplied keyframes.

#### Odometry input
- Topic: `/triorb/odom`
- Type: `geometry_msgs::msg::Vector3Stamped`
- Note: Odometry input from Odomono / OdoRig.
