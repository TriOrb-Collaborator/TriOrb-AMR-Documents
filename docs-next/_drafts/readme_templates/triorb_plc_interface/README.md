# triorb_plc_interface

PLC との EIP 通信に用いる共通インターフェース定義パッケージ。

> package.xml `<description>`: "PLCとのEIP通信に用いる共通インターフェース"
>
> version: 1.0.0 / maintainer: tobata.masakazu@triorb.co.jp

## Interface Summary

| Kind | Name | 用途（記入要） |
| --- | --- | --- |
| msg | BasicDataFromPLC | TODO: 概要を記入（PLC から受信する基本データ） |
| msg | BasicDataToPLC | TODO: 概要を記入（PLC へ送信する基本データ） |

## Messages

### BasicDataFromPLC

**Fields**:
```
#==PLCから受信した基本データ==
std_msgs/Header header              # timestamp
uint8 index                         # Assembly index of the byte array
bool watchdog_request_from_plc      # PLCからのウォッチドッグ要求
bool watchdog_response_from_plc     # PLCからのウォッチドッグ応答
bool emergency_stop_from_plc        # PLCが非常停止中(B接点)
bool power_cut_from_plc             # PLCが動力遮断中(B接点)
bool unknown_error_from_plc         # PLCからの不明なエラー(A接点)
bool permit_auto_move_from_plc      # PLCからの自動移動許可信号(B接点)
bool permit_manual_move_from_plc    # PLCからの自動移動許可信号(B接点)
bool sls_off_from_plc               # PLCからのSLS監視停止状態信号(A接点)
```

TODO: PLC 接続ノード（publisher）、subscribe 側の安全ロジック、A/B 接点の扱い（論理反転）を記入。`permit_manual_move_from_plc` のコメントが `permit_auto_move` と重複しているように見える点も要確認。

### BasicDataToPLC

**Fields**:
```
#==PLCへ送信する基本データ==
std_msgs/Header header              # timestamp
uint8 index                         # Assembly index of the byte array
bool watchdog_request_from_jetson   # JetsonからPLCへのウォッチドッグ要求
bool watchdog_response_to_plc       # PLCへのウォッチドッグ応答
bool emergency_stop_to_plc          # PLCへの非常停止要求(B接点)
bool deactivate_request_to_plc      # PLCへの管理停止要求(A接点)
bool sls_off_request_to_plc         # PLCへのSLS監視停止要求(A接点)
bool error_reset_request_to_plc    # PLCへのエラーリセット要求(A接点)
uint8 reserved                      # 予約（未使用ビット）
```

TODO: publish 元ノード、送信周期、ウォッチドッグ規約（タイムアウト値等）を記入。

## Dependencies

- `std_msgs`
- `geometry_msgs`
- `sensor_msgs`

## Related Packages

- TODO: EIP クライアント実装パッケージ（PLC ラッパノード）
- TODO: 安全系・状態監視ノード（`triorb_static_interface` の RobotStatus との連携）
