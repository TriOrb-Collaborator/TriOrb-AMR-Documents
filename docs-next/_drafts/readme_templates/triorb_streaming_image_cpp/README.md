# triorb_streaming_image_cpp

カメラのImageトピックを購読し、JPEG/WEBP等へ圧縮してMQTTへ送出する軽量ストリーミングノードのC++実装です。

> version: `0.0.0` / maintainer: TriOrb Inc. <info@triorb.co.jp> / license: Apache-2.0

## Overview

TODO: このパッケージが提供する機能、起動タイミング、関連ノードとの連携を 2–4 文で。

## API Reference

> Source: migrated from the hand-written `API.md` in the submodule.

カメラのImageトピックを購読し、JPEG/WEBP等へ圧縮してMQTTへ送出する軽量ストリーミングノードのC++実装です。

### Subscriber
####  `sensor_msgs/msg/Image`
- Topic: (可変)
- Type: sensor_msgs/msg/Image

### Publisher
####  MQTT 出力
- **Payload**: `.webp`, `.jpg`, `.png` 形式に圧縮 → Base64 文字列にエンコード
- **Topic**: `camera/stream`
- **Protocol**: `paho-mqtt` による MQTT publish

## Related Packages

TODO: 上流・下流の関連パッケージを列挙。
