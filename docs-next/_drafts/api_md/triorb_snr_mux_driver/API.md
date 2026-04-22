# triorb_snr_mux_driver

SNR-MUXボードとシリアル通信し、音声再生状態・発進待ち時間などを ROS 2 トピックへ配信するドライバです。navigate / navigation_manager の停止・一時停止の遅延を音声再生と連動させます。

## triorb_snr_mux_driver API

### 駆動ベクトル購読（標準）
- Topic：(prefix)/drive/std_vector2
- Node：(prefix)_snr_mux_driver
- Type：std_msgs/Float32MultiArray
- Usage：
```bash
root@orin-nx-XXX:~/$ ros2 topic info /drive/std_vector2
Type: std_msgs/msg/Float32MultiArray
Publisher count: 1
Subscription count: 1
```

### 駆動ベクトル購読（協調走行）
- Topic：(prefix)/collab/drive/std_vector2
- Node：(prefix)_snr_mux_driver
- Type：std_msgs/Float32MultiArray
- Usage：
```bash
# TODO: record sample output
ros2 topic echo /collab/drive/std_vector2
```

### AUXイベント購読
- Topic：(prefix)/aux/event
- Node：(prefix)_snr_mux_driver
- Type：std_msgs/String
- Note：`pause` / `start_move` / `resume` / `finish` / `abnormal_occurred` 等の状態遷移イベント文字列を受信。`&&<code>` や `||tag_nav` といったサフィックスで追加情報を渡せる
- Usage：
```bash
ros2 topic pub /aux/event std_msgs/String "{data: 'start_move'}" --once
```

### AUXイベント購読（協調走行）
- Topic：(prefix)/bc/collab/aux/event
- Node：(prefix)_snr_mux_driver
- Type：std_msgs/String
- Usage：
```bash
# TODO: record sample output
ros2 topic echo /bc/collab/aux/event
```

### ロボット状態購読
- Topic：(prefix)/robot/status
- Node：(prefix)_snr_mux_driver
- Type：triorb_static_interface/msg/RobotStatus
- Note：`error` ビットマスクからカメラ異常 (0x2000) / モータECU異常 (0x0001) を検出し、LCD 表示へ反映
- Usage：
```bash
ros2 topic echo /robot/status
```

### PLC基本データ購読
- Topic：(prefix)/plc/basic_data/from_plc
- Node：(prefix)_snr_mux_driver
- Type：triorb_plc_interface/msg/BasicDataFromPLC
- Note：`permit_manual_move_from_plc` / `permit_auto_move_from_plc` を参照して LCD/LED を切り替え
- Usage：
```bash
ros2 topic echo /plc/basic_data/from_plc
```

### PLCアプリデータ購読
- Topic：(prefix)/plc/app_data/from_plc
- Node：(prefix)_snr_mux_driver
- Type：triorb_sick_plc_wrapper/msg/AppDataFromPLC
- Note：`ready_to_drive` / `selected_auto_drive_mode` / `selected_manual_drive_mode` / `error_reset_from_plc` を参照
- Usage：
```bash
ros2 topic echo /plc/app_data/from_plc
```

### PLC非常停止詳細購読
- Topic：(prefix)/plc/estop_detail/from_plc
- Node：(prefix)_snr_mux_driver
- Type：triorb_sick_plc_wrapper/msg/EstopDetailFromPLC
- Note：`switch_pushed` / `remote_switch_disabled` / `sls_detected` を参照
- Usage：
```bash
ros2 topic echo /plc/estop_detail/from_plc
```

### バッテリー残量購読
- Topic：(prefix)/battery/status
- Node：(prefix)_snr_mux_driver
- Type：triorb_sensor_interface/msg/BatteryStatus
- Note：LCD 上段に残量を表示、`is_charging` が HOLD 時間継続で充電中と判定
- Usage：
```bash
ros2 topic echo /battery/status
```

### 減速フラグ購読
- Topic：(prefix)/triorb_safe_run/decelerating
- Node：(prefix)_snr_mux_driver
- Type：std_msgs/Bool
- Note：true の間 LED は黄色・LCD は "Automoving Limited" 表示
- Usage：
```bash
ros2 topic pub /triorb_safe_run/decelerating std_msgs/Bool "{data: true}" --once
```

### AMRパッケージ再起動要求
- Topic：(prefix)/triorb/amr_pkg_restart/request
- Node：(prefix)_snr_mux_driver
- Type：std_msgs/Empty
- Note：受信で RESTART 状態に遷移し LCD に "Restarting..." を表示
- Usage：
```bash
ros2 topic pub /triorb/amr_pkg_restart/request std_msgs/Empty --once
```

### ノード登録通知
- Topic：(prefix)/except_handl/node/add
- Node：(prefix)_snr_mux_driver
- Type：std_msgs/String
- Frequency：起動時 1 回
- Usage：
```bash
ros2 topic echo /except_handl/node/add
```

### エラー文字列通知
- Topic：(prefix)/triorb/error/str/add
- Node：(prefix)_snr_mux_driver
- Type：std_msgs/String
- Frequency：イベント発火時
- Usage：
```bash
ros2 topic echo /triorb/error/str/add
```

### 警告文字列通知
- Topic：(prefix)/triorb/warn/str/add
- Node：(prefix)_snr_mux_driver
- Type：std_msgs/String
- Frequency：イベント発火時
- Usage：
```bash
ros2 topic echo /triorb/warn/str/add
```

### SNR-MUX 情報配信
- Topic：(prefix)/snr_mux/info
- Node：(prefix)_snr_mux_driver
- Type：std_msgs/String
- Frequency：1/2.5 Hz（シリアル接続成功後に有効）
- Note：JSON 文字列。`config` / `status` セクションに LED・LCD 設定とロボット状態変数を格納
- Usage：
```bash
root@orin-nx-XXX:~/$ ros2 topic echo /snr_mux/info
data: '{"config": {"autonomous_start_hold_sec": 3.0, ...}, "status": {"battery_level": 87.0, "is_charging": false, "switch_pushed": false, ...}}'
```

### バージョン取得サービス
- Service：(prefix)/get/version/snr_mux_driver
- Node：(prefix)_snr_mux_driver
- Type：triorb_static_interface/srv/Version
- Usage：
```bash
root@orin-nx-XXX:~/$ ros2 service call /get/version/snr_mux_driver triorb_static_interface/srv/Version
response:
triorb_static_interface.srv.Version_Response(version=[1, 2, 3])
```
