# triorb_safe_run_cpp

C++ implementation of the TriOrb safe run velocity filter.

> version: `0.0.1` / maintainer: TriOrb <info@triorb.co.jp> / license: Apache License, Version 2.0

## Overview

TODO: このパッケージが提供する機能、起動タイミング、関連ノードとの連携を 2–4 文で。

## API Reference

> Source: migrated from the hand-written `API.md` in the submodule.

C++ implementation of the TriOrb safe run velocity filter.

### Node interface
| Direction | Topic | Type | Notes |
|-----------|-------|------|-------|
| Subscribe | `/<prefix>/sick/point2d/right` (configurable) | `sensor_msgs/msg/PointCloud` | Synchronized via ApproximateTime. `point2d_topics` can list two or more streams. |
| Subscribe | `/<prefix>/sick/point2d/left` (configurable) | `sensor_msgs/msg/PointCloud` | Same as above; add entries in config to change topics. |
| Subscribe | `/<prefix>/safe_drive/run_vel` | `triorb_drive_interface/msg/TriorbRunVel3` | Raw velocity command to be filtered. |
| Publish   | `/<prefix>/drive/run_vel` | `triorb_drive_interface/msg/TriorbRunVel3` | Safe velocity command after potential-field filtering. |
| Publish   | `/<prefix>/drive/set_life_time` | `std_msgs/msg/UInt16` | Optional watchdog lifetime (currently throttled). |
| Publish   | `/<prefix>/triorb_safe_run/config` | `std_msgs/msg/String` | 現在の設定をJSON文字列で3秒周期に配信。 |
| Publish   | `/<prefix>/triorb_safe_run/debug/image/compressed` | `sensor_msgs/msg/CompressedImage` | Enabled when `enable_image_pub=true`; shows occupancy & vectors. |
| Publish   | `/<prefix>/except_handl/node/add` etc. | `std_msgs/msg/String` | Registration and diagnostic topics inherited from Python node. |
| Service   | `/<prefix>/triorb_safe_run/set_config` | `triorb_static_interface/srv/SetString` | Pass a JSON string (first element of `request[]`) to replace the runtime configuration. |
| Service   | `/<prefix>/triorb_safe_run/set_param` | `triorb_static_interface/srv/SetString` | `request[0]`にJSONオブジェクトを渡すと複数パラメータをまとめて更新。`[キー1,値1(JSON),キー2,値2(JSON)...]`形式の偶数要素指定でも一括更新可。`[キー,値(JSON)]`形式は従来互換で1件更新。パース失敗時は例外を捕捉しエラー応答。 |
| Service   | `/<prefix>/triorb_safe_run/get_config` | `triorb_static_interface/srv/GetString` | Returns the current configuration as JSON text in `result`. |

## Related Packages

TODO: 上流・下流の関連パッケージを列挙。
