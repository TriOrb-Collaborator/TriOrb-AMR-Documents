# triorb_visual_slam

TriOrb BASE のステレオキーフレーム特徴量ベースの地図生成・自己位置推定エンジン
（Visual SLAM）をまとめたパッケージです。内部ラッパーの API は実装詳細として扱い、
本リファレンスでは公開していません。

```{toctree}
:maxdepth: 1
:titlesonly:

API
```

## Role on TriOrb BASE

| Responsibility | Description |
|---|---|
| Map building | Builds a 3D keyframe-based map while the robot is driven through the environment |
| Self-localization | Estimates 6-DoF robot pose at runtime by matching stereo features against the stored map |
| Map export | Exports the 3D map to a 2D occupancy representation used by downstream navigation |
| Map I/O | Saves / loads map files to the robot controller and PC |

## Related packages

Higher-level packages consume Visual SLAM's output:

| Package | Role |
|---|---|
| [`triorb_vslam_tf`](../triorb_vslam_tf/index.md) | Publishes VSLAM-derived pose as TF. |
| [`trirob_vslam_tf_bridge`](../trirob_vslam_tf_bridge/index.md) | Bridges VSLAM to navigation pose. |
| [`triorb_dead_reckoning`](../triorb_dead_reckoning/index.md) | Fuses VSLAM, odometry, and IMU for robust pose. |
| [WebAPI](https://triorb-inc.github.io/TriOrb-AMR-Robot-Controller/) | Map save / load / switch operations over HTTP. |

See each package's API page for its public topics, services, and actions.
