# triorb_calibration

チェッカーボード画像を取り込みカメラ内部パラメータを推定するキャリブレーション C++ アクションノード。

> package.xml `<description>`: "チェッカーボード画像を取り込みカメラ内部パラメータを推定するキャリブレーションアクションノードです。"
>
> version: 0.0.0 / maintainer: info@triorb.co.jp
>
> executable: `camera_calibration`

## Overview

TODO: 画像トピックを subscribe し、クライアントからの action goal（チェッカーボード仕様 / サンプル枚数等）に応じて内部パラメータを推定して result で返すアクションサーバ。推定結果の永続化先 (YAML 出力) とクライアント想定 (GUI) を記載。

## Public ROS 2 API

### Publishers

| Topic | Type | QoS | 用途（TODO） |
| --- | --- | --- | --- |
| `<prefix>/except_handl/node/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/error/str/add` | `std_msgs/String` | parameters | TODO |
| `<prefix>/triorb/warn/str/add` | `std_msgs/String` | parameters | TODO |

### Actions

| Action | Type | 用途（TODO） |
| --- | --- | --- |
| (内部パラメータ推定, 名前 TODO) | `triorb_sensor_interface/action/CameraCalibrationInternal` | TODO: goal にチェッカーボード仕様、feedback に検出枚数、result に camera_matrix / distortion |

### Upstream dependencies (this node calls/subscribes to)

- TODO: 実画像入力の subscribe 先 topic（ソース内別ファイルに存在する可能性あり、`src/camera_calibration_internal.cpp` 参照）
- 画像取得元: `triorb_camera_capture` / `triorb_camera_argus` の `/camera*`

## Parameters

TODO: チェッカーボード寸法、出力パスなどの declare_parameter を列挙。

## Launch / run

```bash
ros2 run triorb_calibration camera_calibration
```

TODO: launch file / config を記載。

## Related Packages

- 上流: `triorb_camera_capture`, `triorb_camera_argus`
- 下流: `triorb_camera_calibration`（Python 実装との使い分けを要確認）、`triorb_camera_capture`（歪み除去に camera_matrix 利用）
- インターフェース: `triorb_sensor_interface` (action), `triorb_static_interface`
