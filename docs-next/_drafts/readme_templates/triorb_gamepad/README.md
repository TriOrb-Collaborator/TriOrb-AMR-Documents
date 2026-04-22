# triorb_gamepad

ゲームパッド入力を監視し、走行・リフタ・非常停止などのコマンドをROS 2トピックへ出力するテレオペ用ノードです。

> version: `0.0.0` / maintainer: TriOrb Inc. <info@triorb.co.jp> / license: Apache-2.0

## Overview

TODO: このパッケージが提供する機能、起動タイミング、関連ノードとの連携を 2–4 文で。

## API Reference

> Source: migrated from the hand-written `API.md` in the submodule.

ゲームパッド入力を監視し、走行・リフタ・非常停止などのコマンドをROS 2トピックへ出力するテレオペ用ノードです。

### 発行トピック
#### 走行関連（標準モード）
- `/drive/run_vel` (`triorb_drive_interface/msg/TriorbRunVel3`): 並進/回転速度と加減速設定。`safe_run_mode` が true の場合は代わりに `/safe_drive/run_vel` を使用。
- `/safe_drive/run_vel` (`triorb_drive_interface/msg/TriorbRunVel3`): SafeRun 対応先への速度通知。
- `/drive/stop` (`std_msgs/msg/Empty`): 非常停止（E-Stop）要求。
- `/drive/sleep` (`std_msgs/msg/Empty`): 走行停止＆スリープ。
- `/drive/wakeup` (`std_msgs/msg/Empty`): 走行再開。
- `/drive/run_lifter` (`std_msgs/msg/String`): `"up"`, `"down"`, `"stop"` を通知。
- `/drive/set_life_time` (`std_msgs/msg/UInt16`): 予備。現状コマンド割当は定義されていません。

#### 走行関連（コラボレーションモード）
`/collab/drive/stop`, `/collab/sleep`, `/collab/wakeup`, `/collab/run_lifter`, `/collab/set_life_time`, `/collab/run_vel` を標準モードと同じメッセージ型で発行します。

## Related Packages

TODO: 上流・下流の関連パッケージを列挙。
