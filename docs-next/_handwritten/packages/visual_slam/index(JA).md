# triorb_visual_slam

TriOrb BASE のステレオキーフレーム特徴量ベースの地図生成・自己位置推定エンジン
（Visual SLAM）をまとめたパッケージです。内部ラッパーの API は実装詳細として扱い、
本リファレンスでは公開していません。

## TriOrb BASE における役割

| Responsibility | Description |
|---|---|
| 地図生成 | ロボット走行中に 3D キーフレーム地図を生成します |
| 自己位置推定 | 保存済み地図とステレオ特徴を照合し、実行時の 6DoF 姿勢を推定します |
| 地図エクスポート | 下流のナビゲーションで使う 2D 占有表現へ地図を変換します |
| 地図 I/O | ロボットコントローラや PC との間で地図を保存 / 読込します |

## 関連パッケージ

上位の公開コンポーネントは Visual SLAM の出力を利用します。

| Package | Role |
|---|---|
| `triorb_vslam_tf` | ナビゲーションスタックで使う内部姿勢 publish コンポーネントです。 |
| `triorb_vslam_tf_bridge` | SLAM 出力とナビゲーション姿勢処理をつなぐ内部 bridge です。 |
| `triorb_dead_reckoning` | VSLAM、オドメトリ、IMU を統合する内部姿勢融合コンポーネントです。 |
| [REST API](https://triorb-inc.github.io/TriOrb-AMR-Robot-Controller/) | HTTP 経由の地図保存 / 読込 / 切替操作です。 |

上記の内部コンポーネントは、このドキュメントサイトでは公開していません。
