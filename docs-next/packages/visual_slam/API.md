# API

このページは、triorb_visual_slam の `/run_slam` ノードが ROS 2 に公開する Publish / Subscribe トピックの一覧です。

## Active API

### Publish トピック一覧

| トピック名 | メッセージ型 | 説明 |
|------------|---------------|------|
| `/run_slam/camera_pose` | `nav_msgs::msg::Odometry` | 推定されたカメラ姿勢 |
| `/run_slam/keyframes` | `geometry_msgs::msg::PoseArray` | キーフレーム群 |
| `/run_slam/keyframes_2d` | `geometry_msgs::msg::PoseArray` | 平面に投影されたキーフレーム |
| `/run_slam/keyframe_landmarks` | `triorb_slam_interface::msg::UInt32MultiArrayStamped` | キーフレームごとのランドマーク数 |
| `/run_slam/matched_landmarks` | `triorb_slam_interface::msg::UInt32MultiArrayStamped` | マッチしたランドマーク数 |
| `/run_slam/matched_points` | `triorb_slam_interface::msg::PointArrayStamped` | マッチした3D点群 |
| `/run_slam/camera_pose_dev` | `triorb_slam_interface::msg::PoseDevStamped` | カメラ姿勢推定結果（validフラグ付き） |
| `/run_slam/matched_landmarks_per_camera` | `triorb_slam_interface::msg::CamerasLandmarkInfo` | カメラごとのランドマーク情報 |
| `/run_slam/cameras_pose` | `triorb_slam_interface::msg::CamerasPose` | 複数カメラの姿勢 |
| `/run_slam/status` | `triorb_slam_interface::msg::SlamStatus` | `map_name` と `state`（bit0:地図固定, bit1:自己位置特定）を含むSLAM状態 |
| `/run_slam/reliability` | `std_msgs::msg::Float32` | マッチランドマーク数に基づく自己位置推定の信頼度（0.0〜1.0目安） |
| `/run_slam/enable_camera` | `std_msgs::msg::Int8MultiArray` | 使用カメラの有効/無効状態 |
| `/run_slam/marker_only` | `std_msgs::msg::Bool` | マーカーのみを使うか |
| `/run_slam/marker_exclude` | `std_msgs::msg::Bool` | マーカー領域の除外フラグ |
| `/run_slam/map_file_path` | `std_msgs::msg::String` | 現在のマップファイルパス |
| `/run_slam/map_file_changed` | `std_msgs::msg::String` | マップファイル変更通知 |
| `/run_slam/local_map_file_path` | `std_msgs::msg::String` | ローカルマップファイルパス |
| `/run_slam/current_keyframes` | `triorb_slam_interface::msg::KeyframeArray` | 現在のキーフレーム情報 |
| `/run_slam/map_freeze` | `std_msgs::msg::Bool` | 地図固定モードの状態 |
| `/except_handl/node/add` | `std_msgs::msg::String` | 例外発生ノード通知 |
| `/triorb/error/str/add` | `std_msgs::msg::String` | エラーメッセージ通知 |
| `/triorb/warn/str/add` | `std_msgs::msg::String` | ワーニング通知 |

### Subscribe トピック一覧

| トピック名 | メッセージ型 | 説明 |
|------------|---------------|------|
| `/run_slam/set/enable_camera` | `std_msgs::msg::Int8MultiArray` | 使用カメラ切り替え |
| `/run_slam/set/mask_positive` | `triorb_slam_interface::msg::XyArrayStamped` | 特徴点マスク（許容） |
| `/run_slam/set/mask_negative` | `triorb_slam_interface::msg::XyArrayStamped` | 特徴点マスク（除外） |
| `/run_slam/set/clear_mask_all` | `std_msgs::msg::Empty` | マスク初期化 |
| `/run_slam/set/save_mask_to_yaml` | `std_msgs::msg::Empty` | マスクYAML保存指示 |
| `/run_slam/set/marker_only` | `std_msgs::msg::Bool` | マーカーのみ利用設定 |
| `/run_slam/set/marker_exclude` | `std_msgs::msg::Bool` | マーカー領域除外設定 |
| `/run_slam/set/change_map_file_path` | `std_msgs::msg::String` | 地図ファイル変更指示 |
| `/run_slam/set/enter_local_map_file_path` | `std_msgs::msg::String` | ローカル地図ファイル切替 |
| `/run_slam/set/map_freeze` | `std_msgs::msg::Bool` | 地図固定切替 |
| `/run_slam/set/manual_keyframes` | `triorb_slam_interface::msg::KeyframeArray` | 手動リローカライズ要求 |
| `/triorb/odom` | `geometry_msgs::msg::Vector3Stamped` | オドメトリ情報（Odomono/OdoRig） |
