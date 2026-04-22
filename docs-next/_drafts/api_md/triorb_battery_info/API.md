# triorb_battery_info

CAN経由で受信したバッテリーSOC・各モジュール電圧/電流を集約し、/battery/status として配信するパッケージです。

## triorb_battery_info API

### CAN フレーム購読
- Topic：(prefix)/can_bridge/rx （`rx_topic` パラメータで変更可）
- Node：(prefix)_battery_status
- Type：triorb_sensor_interface/msg/CanFrame
- Note：SensorDataQoS (depth=1)。`id_soc` (既定 0x053) で SOC、`module_iv_ids` (既定 [0x056, 0x076]) で各モジュールの I/V を取得
- Usage：
```bash
ros2 topic echo /can_bridge/rx
```

### バッテリー状態配信
- Topic：(prefix)/battery/status （`battery_topic` パラメータで変更可）
- Node：(prefix)_battery_status
- Type：triorb_sensor_interface/msg/BatteryStatus
- Frequency：1 Hz（定期タイマー）
- Note：`pack_topology`（series/parallel）と `parallel_voltage_method`（avg/max/min/first）で合計電圧の算出方式を切り替え。いずれかのモジュール電流が正の場合 `is_charging=true` を配信
- Usage：
```bash
root@orin-nx-XXX:~/$ ros2 topic echo /battery/status
# TODO: record sample output
```

### ノード登録通知
- Topic：(prefix)/except_handl/node/add
- Node：(prefix)_battery_status
- Type：std_msgs/String
- Frequency：起動時 1 回
- Usage：
```bash
ros2 topic echo /except_handl/node/add
```

### エラー文字列通知
- Topic：(prefix)/triorb/error/str/add
- Node：(prefix)_battery_status
- Type：std_msgs/String
- Frequency：パラメータ検証失敗時・CSV オープン失敗時
- Usage：
```bash
ros2 topic echo /triorb/error/str/add
```

### 警告文字列通知
- Topic：(prefix)/triorb/warn/str/add
- Node：(prefix)_battery_status
- Type：std_msgs/String
- Frequency：イベント発火時
- Usage：
```bash
ros2 topic echo /triorb/warn/str/add
```
