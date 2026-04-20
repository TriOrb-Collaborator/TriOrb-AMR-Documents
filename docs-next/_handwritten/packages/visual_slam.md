# Visual SLAM

Visual SLAM is TriOrb BASE's map building and self-localization engine based on
stereo keyframe features. The implementation wraps the open-source
[stella_vslam](https://github.com/stella-cv/stella_vslam) library — its internal
API is considered implementation detail and is not covered in this reference.

## Role on TriOrb BASE

| Responsibility | Description |
|---|---|
| Map building | Builds a 3D keyframe-based map while the robot is driven through the environment |
| Self-localization | Estimates 6-DoF robot pose at runtime by matching stereo features against the stored map |
| Map export | Exports the 3D map to a 2D occupancy representation used by downstream navigation |
| Map I/O | Saves / loads map files to the robot controller and PC |

## Interfaces you care about

Day-to-day interaction is through higher-level APIs, not through Visual SLAM
directly:

- `triorb_vslam_tf` — publishes VSLAM-derived pose as TF
- `trirob_vslam_tf_bridge` — bridges VSLAM to navigation pose
- `triorb_dead_reckoning` — fuses VSLAM, odometry, and IMU for robust pose
- The WebAPI's map save / load / switch operations

See those packages for the public topic / service surface.

## Related

- [triorb_vslam_tf](triorb_vslam_tf/index.md)
- [trirob_vslam_tf_bridge](trirob_vslam_tf_bridge/index.md)
- [triorb_dead_reckoning](triorb_dead_reckoning/index.md)
