# ROS2 API

```{important}
ROS 2 API を利用するには、[TriOrb-ROS2-Types](https://github.com/TriOrb-Inc/TriOrb-ROS2-Types)
の install が必要です。対象ワークスペースで `git clone` してから `colcon build`
してください。各 package の topic / service / action は、この repository で配布されている
interface 定義に依存しています。
```

Auto-generated API reference for ROS 2 packages under TriOrb-AMR-Package,
produced by rosdoc2. Packages are grouped by subsystem; within each group
they are sorted alphabetically.

## Drive & Navigation

```{toctree}
:maxdepth: 1
:titlesonly:

triorb_drive_pico/index
triorb_drive_vector/index
triorb_navigation/index
triorb_navigation_manager/index
triorb_safe_run_cpp/index
triorb_snr_mux_driver/index
```

## SLAM

```{toctree}
:maxdepth: 1
:titlesonly:

triorb_tagslam_manager/index
visual_slam/index
```

## Sensor I/O

```{toctree}
:maxdepth: 1
:titlesonly:

triorb_camera_argus/index
triorb_camera_capture/index
triorb_gamepad/index
```

## Safety Sensors

```{toctree}
:maxdepth: 1
:titlesonly:

triorb_sick_plc_wrapper/index
triorb_sls_wrapper/index
```

## OS / Infrastructure

```{toctree}
:maxdepth: 1
:titlesonly:

triorb_battery_info/index
triorb_gpio/index
triorb_host_info/index
triorb_os_setting/index
```
