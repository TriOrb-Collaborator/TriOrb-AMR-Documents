# sick_safetyscanners2

ROS2 Driver for the SICK safetyscanners

> version: `1.0.4` / maintainer: Lennart Puck <puck@fzi.de> / license: ALv2

## Overview

TODO: このパッケージが提供する機能、起動タイミング、関連ノードとの連携を 2–4 文で。

## API Reference

> Source: migrated from the hand-written `API.md` in the submodule.

SICK safety scanner の UDP データを ROS2 トピック／サービスへ変換します。
`topic_prefix`（既定 `sick`）でプレフィクスを切り替えます。

### Active API

#### LaserScan出力
- Topic：<prefix>/scan
- Node：(prefix)_sick_safetyscanners2
- Type： sensor_msgs/msg/LaserScan
- Note：SensorDataQoS。診断ラッパー付き `DiagnosedLaserScanPublisher` を通過したデータ
- Usage：
```
ros2 topic echo sick/scan
```

#### Extended LaserScan出力
- Topic：<prefix>/extended_scan
- Node：(prefix)_sick_safetyscanners2
- Type： sick_safetyscanners2_interfaces/msg/ExtendedLaserScan
- Note：強度・派生値など拡張フィールドを含む
- Usage：
```
ros2 topic echo sick/extended_scan
```

#### RawMicroScanData出力
- Topic：<prefix>/raw_data
- Node：(prefix)_sick_safetyscanners2
- Type： sick_safetyscanners2_interfaces/msg/RawMicroScanData
- Note：後段の `triorb_sick_sls_wrapper` が参照する生データ
- Usage：
```
ros2 topic echo sick/raw_data
```

#### フィールドデータ取得
- Topic：<prefix>/field_data
- Node：(prefix)_sick_safetyscanners2
- Type： sick_safetyscanners2_interfaces/srv/FieldData
- Note：サービス呼び出しでセンサの保護フィールド設定を取得
- Usage：
```
ros2 service call sick/field_data sick_safetyscanners2_interfaces/srv/FieldData "{}"
```

#### ステータス概要取得
- Topic：<prefix>/status_overview
- Node：(prefix)_sick_safetyscanners2
- Type： sick_safetyscanners2_interfaces/srv/StatusOverview
- Note：動作状態や診断情報を取得
- Usage：
```
ros2 service call sick/status_overview sick_safetyscanners2_interfaces/srv/StatusOverview "{}"
```

## Related Packages

TODO: 上流・下流の関連パッケージを列挙。
