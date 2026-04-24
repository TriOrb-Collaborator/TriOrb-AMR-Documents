# triorb_visual_slam

Package that groups the stereo keyframe-based mapping and self-localization engine
(Visual SLAM) used in TriOrb BASE. Internal wrapper APIs are treated as implementation
details and are not published on this reference site.

## Role on TriOrb BASE

| Responsibility | Description |
|---|---|
| Map building | Builds a 3D keyframe-based map while the robot is driven through the environment |
| Self-localization | Estimates the runtime 6-DoF pose by matching stereo features against the stored map |
| Map export | Exports the map to a 2D occupancy representation used by downstream navigation |
| Map I/O | Saves and loads map files between the robot controller and a PC |

## Related Packages

Higher-level public components consume Visual SLAM output:

| Package | Role |
|---|---|
| `triorb_vslam_tf` | Internal pose-publication component used by the navigation stack |
| `triorb_vslam_tf_bridge` | Internal bridge between SLAM output and navigation pose handling |
| `triorb_dead_reckoning` | Internal pose-fusion component that combines VSLAM, odometry, and IMU |
| [REST API](https://triorb-inc.github.io/TriOrb-AMR-Robot-Controller/) | HTTP interface for map save/load/switch operations |

The internal components above are not published on this documentation site.
