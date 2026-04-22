# triorb_streaming_images

映像配信のためのパッケージ

## triorb_streaming_images API

### カメラ画像購読
- Topic：(prefix)/camera0 （`topic_name_raw` パラメータで変更可）
- Node：(prefix)_streaming_image_node
- Type：sensor_msgs/Image
- Note：BEST_EFFORT QoS・depth=1。`fps` パラメータで間引き、`scale` で縮小、`quality` で WebP エンコード品質を調整
- Usage：
```bash
ros2 topic echo /camera0 --no-arr
```

### MQTT 配信
- Broker：`mqtt_adress`:`mqtt_port`（デフォルト `localhost:1883`）
- Topic：`mqtt_topic`（デフォルト `camera/stream`）
- Node：(prefix)_streaming_image_node
- Type：Base64 エンコード済み WebP バイト列（payload は文字列）
- Frequency：`fps` パラメータ（Hz）
- Note：ROS2 ではなく MQTT ブローカー経由で配信。WebSocket 版は無効化済み
- Usage：
```bash
# TODO: record sample output
mosquitto_sub -h localhost -t camera/stream | head -n1
```

### ノード登録通知
- Topic：(prefix)/except_handl/node/add
- Node：(prefix)_streaming_image_node
- Type：std_msgs/String
- Frequency：起動時 1 回
- Usage：
```bash
ros2 topic echo /except_handl/node/add
```

### エラー文字列通知
- Topic：(prefix)/triorb/error/str/add
- Node：(prefix)_streaming_image_node
- Type：std_msgs/String
- Frequency：イベント発火時
- Usage：
```bash
ros2 topic echo /triorb/error/str/add
```

### 警告文字列通知
- Topic：(prefix)/triorb/warn/str/add
- Node：(prefix)_streaming_image_node
- Type：std_msgs/String
- Frequency：イベント発火時
- Usage：
```bash
ros2 topic echo /triorb/warn/str/add
```
