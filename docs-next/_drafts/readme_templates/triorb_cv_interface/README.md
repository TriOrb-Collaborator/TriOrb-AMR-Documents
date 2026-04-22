# triorb_cv_interface

コンピュータビジョン（物体検出、画像取得など）関連の ROS 2 インターフェース定義パッケージ。

> package.xml の `<description>` は未記入（"TODO: Package description"）。必要に応じて更新してください。
>
> version: 1.0.0 / maintainer: tobata.masakazu@triorb.co.jp

## Interface Summary

| Kind | Name | 用途（記入要） |
| --- | --- | --- |
| msg | BoundingBox | TODO: 概要を記入（検出結果の矩形座標） |
| msg | Detection | TODO: 概要を記入（物体検出結果のまとめ） |
| srv | GetImage | TODO: 概要を記入（画像ファイルの取得） |
| srv | Version | TODO: 概要を記入（バージョン問い合わせ） |

## Messages

### BoundingBox

**Fields**:
```
# ==バウンディングボックス座標==
float32[] xtl_ytl_xbr_ybr       # [Left-top-x, Left-top-y, Right-bottom-x, Right-bottom-y] [pix]
```

TODO: フィールドの意味、使い方、典型的な publish 元ノード・subscribe 先ノードを記入。

### Detection

**Fields**:
```
# ==物体検出結果==
std_msgs/Header header      # Timestamp
uint32 det_num              # Number of detections
BoundingBox[] boxes         # BoundingBoxs
float64[] scores            # Detection scores
string[] labels             # Object types
```

TODO: 検出器ノード（どの nodeがpublishするか）、下流の利用先、座標系を記入。

## Services

### GetImage

**Request**:
```
# ==画像取得サービス==
string fname
```

**Response**:
```
sensor_msgs/Image image
```

TODO: 呼び出し元、`fname` の解釈（ファイルパスか、カメラ ID か等）、エラー条件を記入。

### Version

**Request**:
```
# ==バージョン取得サービス==
std_msgs/Empty request
```

**Response**:
```
uint8[] version
```

TODO: version の符号化ルール（semver bytes か ASCII か）、呼び出しタイミングを記入。

## Dependencies

- `std_msgs`
- `geometry_msgs`
- `sensor_msgs`

## Related Packages

- TODO: 画像を publish するカメラノード（`triorb_sensor_interface` 系）
- TODO: `Detection` を subscribe する下流ノード（ナビゲーション等）
