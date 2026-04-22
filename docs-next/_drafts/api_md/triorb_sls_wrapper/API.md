# triorb_sls_wrapper

Convert SICK SLS RawMicroScanData topics into sensor_msgs/PointCloud messages.

## triorb_sls_wrapper API

### RawMicroScanData 購読 (OccupancyGrid 変換)
- Topic：(prefix)/sick/raw_data （`input_topic` パラメータで変更可）
- Node：(prefix)_sls_occupancy
- Type：sick_safetyscanners2_interfaces/msg/RawMicroScanData
- Note：SensorDataQoS (depth=1)。`serial_number` / `filter_by_serial` パラメータおよび config JSON に基づきセンサーを選別
- Usage：
```bash
ros2 topic echo /sick/raw_data
```

### OccupancyGrid 配信
- Topic：(prefix)/sick/occupancy （`occupancy_topic` / config JSON で変更可）
- Node：(prefix)_sls_occupancy
- Type：nav_msgs/msg/OccupancyGrid
- Frequency：入力 RawMicroScanData 受信ごと
- Note：SensorDataQoS (depth=1)。シリアル番号ごとに publisher を動的生成し、キャリブレーションに沿って 2D 投影
- Usage：
```bash
ros2 topic echo /sick/occupancy
```

### RawMicroScanData 購読 (PointCloud 変換)
- Topic：(prefix)/sick/raw_data （`input_topic` パラメータで変更可）
- Node：(prefix)_sls_point2d
- Type：sick_safetyscanners2_interfaces/msg/RawMicroScanData
- Note：`serial_number` / `filter_by_serial` / `mask_angles` によりフィルタリング
- Usage：
```bash
ros2 topic echo /sick/raw_data
```

### PointCloud 配信
- Topic：(prefix)/sick/point2d52 （`pointcloud_topic` / config JSON で変更可）
- Node：(prefix)_sls_point2d
- Type：sensor_msgs/msg/PointCloud
- Frequency：入力 RawMicroScanData 受信ごと
- Note：SensorDataQoS (depth=1)。Z 成分に反射強度を格納。シリアル番号ごとに publisher を動的生成
- Usage：
```bash
ros2 topic echo /sick/point2d52
```

### デバッグプロット画像配信
- Topic：(prefix)/sick/pointcloud_debug/image （`debug_plot_image_topic` で変更可）
- Node：(prefix)_sls_point2d
- Type：sensor_msgs/msg/CompressedImage
- Frequency：`enable_pointcloud_debug_plot=true` 時のみ、PointCloud と同周期
- Note：`debug_plot_image_size_px` / `debug_plot_xy_limit` / `debug_plot_point_radius_px` で描画を調整
- Usage：
```bash
ros2 topic echo /sick/pointcloud_debug/image --no-arr
```
