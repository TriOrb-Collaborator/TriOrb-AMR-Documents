# triorb_navigation

自律移動を行うためのパッケージ

> version: `1.1.0` / maintainer: TriOrb Inc. <info@triorb.co.jp> / license: Apache-2.0

## Overview

TODO: このパッケージが提供する機能、起動タイミング、関連ノードとの連携を 2–4 文で。

## API Reference

> Source: migrated from the hand-written `API.md` in the submodule.

自律移動を行うためのパッケージ

### 動作モード(forceフラグ)
各bitの組合せで指定
- フィードバック制御フラグ(0b00000001)
    - 0でフィードバック制御しない
    - 1でフィードバック制御する
    - 速度指示モードと事後フィードバック制御モードでは無効
- 事後フィードバック制御フラグ(0b00000010)
    - フィードバック制御しない場合、移動完了後にフィードバック制御を行う
    - おおまかに位置決めした後に精密位置合わせしたい場合に使用
- 回転モードフラグ(0b00001000)
    - 並進指示値が常に0になり、並進方向の精度を無視する
    - 並進モードフラグと併用できない（移動しないが常に成功判定になる）
- レーン維持モード(0b00010000)
    - 速度指示モードと同時に使用する(0b10010000)。
    - 経由点間を結ぶ直線に沿って移動する。
    - 回転を伴う移動中は、均等に回転させる。
- 並進モードフラグ(0b00010000)
    - 回転指示値が常に0になり、回転方向の精度を無視する
    - 何らかの原因でロボットが回転した場合でも元の角度に復帰することはない
    - 回転モードフラグと併用すると正常に動作しない
- 速度指示モード(0b10000000)
    - 速度指示モードになり、見た目上なめらかに動く
    - フィードバック制御フラグに関わらずフィードバック制御を行う

### 自律移動状態(state変数)
- 待機中(state=0)
  - 自律移動指示を一度も受け取っていない
  - /drive/stopトピックにより、自律移動が終了した
- 自律移動中(state=1)
  - 自律移動指示を受け移動中
- 中断(state=2)
  - /drive/pauseトピックにより、自律移動が中断した
- 成功終了(state=3)
  - 目標地点に到達した
  - ロボットがゴール地点から離れると、state=5に遷移する
- 失敗終了(state=4)
  - 目標地点に到達できなかった
  - force=0を除き、自己位置認識できないことが原因
- 目標地点から離脱(state=5)
  - 成功終了後、何らかの移動指示により目標地点から離れた


### Subscriber
#### 自律移動を終了する
- Topic: (prefix)/drive/stop
- Type: std_msgs/msg/Empty
- Usage: 
```bash
root@orin-nx-XXX:~/$ ros2 topic pub -1 /drive/stop std_msgs/msg/Empty 
```

#### 世界座標系目標位置指示による移動 
- Topic: (prefix)/drive/set_pos
- Type: triorb_drive_interface/msg/TriorbSetPos3
- Usage: 
```bash
```
#### 自律移動時のPIDゲインを設定する
- Topic: (prefix)/setting/drive/gains
- Type: triorb_drive_interface/msg/DriveGains
- Usage: 
```bash
```

### Publisher
#### 移動距離指示による相対移動
- Topic: (prefix)/drive/run_pos
- Type: triorb_drive_interface/msg/TriorbRunPos3
- 内容: Navigatorがロボット座標系の相対移動量を下位のdrive制御に指示する。標準ではタイマー周期0.15s（`timer_period`パラメータ）ごとに送信し、PLC側が自律移動を許可していない場合はPublishしない。
- フィールド:
  - `speed.acc / speed.dec` [ms], `speed.xy` [m/s], `speed.w` [rad/s]（安全速度`limited_speed_by_safety_plc_`でクリップ）
  - `position.x / position.y` [m], `position.deg` [deg]（`force`フラグに応じて回転のみ/並進のみやFEEDBACK時のクリッピングを実施）
- Usage: 
```bash
## 相対移動指示の監視
ros2 topic echo /drive/run_pos
```
#### 自律移動完結果
- Topic: (prefix)/drive/result
- Type: triorb_drive_interface/msg/TriorbRunResult
- 内容: 自律移動の完了・失敗・強制停止・リジェクト時に1度だけ通知される結果。`success`がtrueなら到達、falseなら失敗/中断。`position`には終了時の自己位置（map座標系換算）が入る。
- info値（`NAVIGATE_RESULT`に対応）:
  - 0: TIMEOUT_FAILED（タイムアウト）, 1: HALF_TIMEOUT, 2: TRANSFORM_FAILED, 3: NO_CHANGE_TIMESTAMP
  - 4: FORCE_STOP（/drive/stopなどで強制停止）, 5: NAVIGATION_FAILED, 6: NAVIGATION_SUCCESS, 7: PROGRESS
  - 8: FORCE_SUCCESS（force success指示）, 9: LOST_FAILED（ロスト判定）, 255: REJECT（移動中に来た指示や不正引数を拒否）
- Usage:
```bash
ros2 topic echo /drive/result
```

#### 自律移動状態
- Topic: (prefix)/drive/state
- Type: triorb_drive_interface/msg/TriorbRunState
- 内容: 1秒周期の状態通知。`goal_pos`は最後に受け付けた目標、`cap_vxy/cap_vw`は現在設定されている速度上限（ロボット上限でクリップ済み）。
- state値: 0=待機(STAND_BY), 1=自律移動中, 2=中断(/drive/pause), 3=成功終了, 4=失敗終了, 5=目標離脱（成功後にゴールから外れた場合）。
- Usage:
```bash
ros2 topic echo /drive/state
```

### Service
#### 世界座標系目標位置指示による移動（移動完了結果報告あり） 
- Topic: (prefix)/srv/drive/set_pos
- Type: triorb_drive_interface/srv/TriorbSetPos3
- Usage: 
```bash
triorb@orin-nx-XXX:~/$ ros2 service call /srv/drive/set_pos \ 
triorb_drive_interface/srv/TriorbSetPos3 "{pos: { setting: { tx: 0.01, ty: 0.01, tr: 1.0, force: 1} , pos: {speed: {acc: 500, dec: 500, xy: 0.1, w: 0.0}, position: {x: 0.6037, y: 0.3599, deg: 0.3176}}}}" 
## コマンド以上 

waiting for service to become available... 
requester: making request: 
triorb_drive_interface.srv.TriorbSetPos3_Request(pos=triorb_drive_interface.msg.TriorbSetPos3(pos=triorb_drive_interface.msg.TriorbRunPos3(speed=triorb_drive_interface.msg.TriorbSpeed(acc=500, dec=500, xy=0.1, w=0.0), position=triorb_drive_interface.msg.TriorbPos3(x=0.6037, y=0.3599, deg=0.3176)), setting=triorb_drive_interface.msg.TriorbRunSetting(tx=0.01, ty=0.01, tr=1.0, force=1))) 

response: 
triorb_drive_interface.srv.TriorbSetPos3_Response(result=triorb_drive_interface.msg.TriorbRunResult(success=True, position=triorb_drive_interface.msg.TriorbPos3(x=0.5981971025466919, y=0.3542609214782715, deg=0.3284424841403961)))
```

### Action
#### 世界座標系目標経路指示による移動（途中経過、移動完了結果報告あり） 
- Topic: (prefix)/action/drive/set_path
- Type: triorb_drive_interface/action/TriorbSetPath
- Usage: 
```bash
triorb@orin-nx-XXX:~/$ ros2 action send_goal /action/drive/set_path \ 
triorb_drive_interface/action/TriorbSetPath "{path: \ 
  [ \ 
    { \ 
      setting: {tx: 0.01, ty: 0.01, tr: 1.0, force: 1}, \ 
      pos: { \ 
        speed: {acc: 500, dec: 500, xy: 0.1, w: 0.0}, \ 
        position: {x: 0.6033, y: 0.3756, deg: 0.3506} \ 
      } \ 
    }, \ 
    { \ 
      setting: {tx: 0.01, ty: 0.01, tr: 1.0, force: 1}, \ 
      pos: { \ 
        speed: {acc: 500, dec: 500, xy: 0.1, w: 0.0}, \ 
        position: {x: 0.2765, y: -0.3236, deg: 0.7407} \ 
      } \ 
    }, \ 
    { \ 
      setting: {tx: 0.01, ty: 0.01, tr: 1.0, force: 1}, \ 
      pos: { \ 
        speed: {acc: 500, dec: 500, xy: 0.1, w: 0.0}, \ 
        position: {x: 0.6033, y: 0.3756, deg: 0.3506} \ 
      } \ 
    } \ 
  ] \ 
}" --feedback 
## コマンド以上 

Goal accepted with ID: cd019fbfa70349789c87ea90fdd10239 

Feedback: 
    way_idx: 0 
now: 
  x: 0.6081861257553101 
  y: 0.38933515548706055 
  deg: 0.1585390269756317 
## ---- (フィードバック略) ---- 

Feedback: 
    way_idx: 2 
now: 
  x: 0.5898382663726807 
  y: 0.35128170251846313 
  deg: -0.009930066764354706 

Result: 
    result: 
  success: true 
  position: 
    x: 0.5965888500213623 
    y: 0.3684644103050232 
    deg: 0.07557345926761627 

Goal finished with status: SUCCEEDED 
```

## Related Packages

TODO: 上流・下流の関連パッケージを列挙。
