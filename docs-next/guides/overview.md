# Product Overview

TriOrb BASE is an autonomous mobile robot (AMR) platform built around a novel
**ball-drive omnidirectional motion mechanism** that addresses the "external
disturbance handling, positioning accuracy, and load capacity" trade-offs
that classical omnidirectional platforms have struggled with.

Representative specs: standard φ100 sphere, load up to ~300 kg. Refer to the
TriOrb website for the latest hardware figures.

This site provides:

- **Autonomous Navigation API**: ROS 2 topics / services / actions for driving the robot
- **Control ECU Library**: a Python library for sending commands to the TriOrb control ECU directly from a host PC
- **REST API**: browser-facing HTTP API for the robot controller ([separate site](https://triorb-inc.github.io/TriOrb-AMR-Robot-Controller/))
- **Changelog / Terms of Service / Privacy Policy**

## Before you start

For hardware setup and initial software installation, refer to the TriOrb
User Documents portal, which aggregates the **TriOrb BASE Operating Manual**,
**Autonomous Navigation Package User Manual**, and **Upgrade Procedures**:

- [TriOrb User Documents (Notion)](https://triorb.notion.site/2afb60b1eaf380dd8e6acade491a29d6?v=2afb60b1eaf381f4a558000ca9c9461d)

Detailed hardware manuals for non-standard models are distributed separately
on a per-project basis.

This site focuses on the public API surface and change history of the ROS 2 /
Python layer. The [REST API](https://triorb-inc.github.io/TriOrb-AMR-Robot-Controller/)
is also available when a browser-only integration is preferred.
