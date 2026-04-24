## 概要
このページは、`triorb_visual_slam` の `/run_slam` ノードが ROS 2 に公開する topic の一覧です。

## インタフェース一覧

### Publishers

#### カメラ姿勢出力
- Topic: `/run_slam/camera_pose`
- Type: `nav_msgs::msg::Odometry`
- Note: 推定されたカメラ姿勢です。

#### キーフレーム出力
- Topic: `/run_slam/keyframes`, `/run_slam/keyframes_2d`
- Type: `geometry_msgs::msg::PoseArray`
- Note: キーフレーム群と、その平面投影結果を出力します。

#### ランドマーク対応情報
- Topic: `/run_slam/keyframe_landmarks`, `/run_slam/matched_landmarks`
- Type: `triorb_slam_interface::msg::UInt32MultiArrayStamped`
- Note: キーフレームごとのランドマーク数と、現在マッチしたランドマーク数を通知します。

#### マッチした特徴点群
- Topic: `/run_slam/matched_points`
- Type: `triorb_slam_interface::msg::PointArrayStamped`
- Note: マッチした 3D 点群を出力します。

#### 姿勢推定の詳細診断
- Topic: `/run_slam/camera_pose_dev`
- Type: `triorb_slam_interface::msg::PoseDevStamped`
- Note: 姿勢推定結果に `valid` フラグを付けた診断用出力です。

#### カメラ別・全カメラ姿勢情報
- Topic: `/run_slam/matched_landmarks_per_camera`, `/run_slam/cameras_pose`
- Type: `triorb_slam_interface::msg::CamerasLandmarkInfo`, `triorb_slam_interface::msg::CamerasPose`
- Note: カメラごとのランドマーク情報と、複数カメラの姿勢を通知します。

#### SLAM 状態通知
- Topic: `/run_slam/status`
- Type: `triorb_slam_interface::msg::SlamStatus`
- Note: `map_name` と `state`（bit0: 地図固定, bit1: 自己位置特定）を含む SLAM 状態です。

#### 自己位置推定の信頼度
- Topic: `/run_slam/reliability`
- Type: `std_msgs::msg::Float32`
- Note: マッチランドマーク数に基づく自己位置推定の信頼度を 0.0〜1.0 目安で通知します。

#### 使用カメラ状態
- Topic: `/run_slam/enable_camera`
- Type: `std_msgs::msg::Int8MultiArray`
- Note: 使用カメラの有効 / 無効状態です。

#### マーカーモード状態
- Topic: `/run_slam/marker_only`, `/run_slam/marker_exclude`
- Type: `std_msgs::msg::Bool`
- Note: マーカーのみ利用するか、マーカー領域を除外するかの現在状態を通知します。

#### マップファイル状態
- Topic: `/run_slam/map_file_path`, `/run_slam/map_file_changed`, `/run_slam/local_map_file_path`
- Type: `std_msgs::msg::String`
- Note: 現在のマップファイル、変更通知、ローカルマップファイルの状態を通知します。

#### 現在のキーフレーム情報
- Topic: `/run_slam/current_keyframes`
- Type: `triorb_slam_interface::msg::KeyframeArray`
- Note: 現在保持しているキーフレーム情報です。

#### 地図固定モード状態
- Topic: `/run_slam/map_freeze`
- Type: `std_msgs::msg::Bool`
- Note: 地図固定モードが有効かを通知します。

#### エラー通知
- Topic: `/triorb/error/str/add`
- Type: `std_msgs::msg::String`
- Note: エラーメッセージを通知します。

#### ワーニング通知
- Topic: `/triorb/warn/str/add`
- Type: `std_msgs::msg::String`
- Note: ワーニングメッセージを通知します。

### Subscribers

#### 使用カメラ切り替え
- Topic: `/run_slam/set/enable_camera`
- Type: `std_msgs::msg::Int8MultiArray`
- Note: 使用カメラの有効 / 無効を切り替えます。

#### 特徴点マスク設定
- Topic: `/run_slam/set/mask_positive`, `/run_slam/set/mask_negative`
- Type: `triorb_slam_interface::msg::XyArrayStamped`
- Note: 許容マスクと除外マスクを設定します。

#### マスク初期化
- Topic: `/run_slam/set/clear_mask_all`
- Type: `std_msgs::msg::Empty`
- Note: すべての特徴点マスクをクリアします。

#### マスク YAML 保存
- Topic: `/run_slam/set/save_mask_to_yaml`
- Type: `std_msgs::msg::Empty`
- Note: 現在のマスク設定を YAML として保存します。

#### マーカー利用設定
- Topic: `/run_slam/set/marker_only`, `/run_slam/set/marker_exclude`
- Type: `std_msgs::msg::Bool`
- Note: マーカーのみ利用するか、マーカー領域を除外するかを切り替えます。

#### マップファイル切り替え
- Topic: `/run_slam/set/change_map_file_path`, `/run_slam/set/enter_local_map_file_path`
- Type: `std_msgs::msg::String`
- Note: 使用するマップファイルやローカルマップファイルを切り替えます。

#### 地図固定モード切り替え
- Topic: `/run_slam/set/map_freeze`
- Type: `std_msgs::msg::Bool`
- Note: 地図固定モードを切り替えます。

#### 手動リローカライズ要求
- Topic: `/run_slam/set/manual_keyframes`
- Type: `triorb_slam_interface::msg::KeyframeArray`
- Note: 手動でキーフレーム列を与えてリローカライズを要求します。

#### オドメトリ入力
- Topic: `/triorb/odom`
- Type: `geometry_msgs::msg::Vector3Stamped`
- Note: Odomono / OdoRig 由来のオドメトリ情報を入力します。
