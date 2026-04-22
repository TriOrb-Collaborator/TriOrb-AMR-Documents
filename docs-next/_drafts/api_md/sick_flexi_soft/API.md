# sick_flexi_soft

SICK PLCとEIP通信するためのパッケージ

## sick_flexi_soft API

### Flexi Soft 入力バッファ配信
- Topic：flexisoft/&lt;assembly&gt;/in_raw
- Node：eip_scanner_node
- Type：std_msgs/UInt8MultiArray
- Frequency：`rpi_us` パラメータ（既定 4000 us）
- Note：SensorDataQoS (depth=1)。EDS で検出した全 Input アセンブリ分の Raw バイト列を配信。`<assembly>` は EDS 名から生成した safe topic 名（例 `standard_input`）
- Usage：
```bash
ros2 topic echo flexisoft/standard_input/in_raw
```

### Flexi Soft 出力バッファ受付
- Topic：flexisoft/&lt;assembly&gt;/out_raw
- Node：eip_scanner_node
- Type：std_msgs/UInt8MultiArray
- Note：ParametersQoS。O->T データを書き戻すと PLC の出力マップに反映される
- Usage：
```bash
ros2 topic pub flexisoft/standard_output/out_raw std_msgs/UInt8MultiArray "{data: [1,0,0,0]}" --once
```

### ノード登録通知
- Topic：/except_handl/node/add
- Node：eip_scanner_node
- Type：std_msgs/String
- Frequency：起動時 1 回
- Note：他ノードと異なり ROS_PREFIX が適用されない実装（トピック文字列リテラル直書き）
- Usage：
```bash
ros2 topic echo /except_handl/node/add
```

### エラー文字列通知
- Topic：/triorb/error/str/add
- Node：eip_scanner_node
- Type：std_msgs/String
- Frequency：EDS パス解決失敗・EIP 通信失敗時
- Usage：
```bash
ros2 topic echo /triorb/error/str/add
```

### 警告文字列通知
- Topic：/triorb/warn/str/add
- Node：eip_scanner_node
- Type：std_msgs/String
- Frequency：`handleConnections()` 例外時や Assembly 名ミスマッチ時
- Usage：
```bash
ros2 topic echo /triorb/warn/str/add
```
