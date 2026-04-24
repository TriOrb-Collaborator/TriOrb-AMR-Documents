# REST API

REST API は、TriOrb BASE の Robot Controller が公開する HTTP API です。
ROS 2 の topic / service / action を直接扱う代わりに、HTTP 経由でロボットの状態取得、
地図操作、自律移動、直接制御、システム管理などを実行するためのインタフェースです。

## 実機でのアクセス

実機上では Robot Controller の REST API サーバーが `8080` 番ポートで起動します。
AMR の IP アドレスが `192.168.20.30` の場合、ベース URL は次の形式です。

```text
http://192.168.20.30:8080
```

例えば Robot Controller のバージョン情報は次の URL で確認できます。

```text
http://192.168.20.30:8080/system/version
```

## OpenAPI フロントエンド

実機でも OpenAPI フロントエンドが公開されています。ブラウザで次の URL を開くと、
エンドポイント一覧、リクエスト / レスポンス schema、各 API の説明を確認できます。

```text
http://<AMRのIPアドレス>:8080/docs
```

OpenAPI フロントエンドでは `Try it out` を使って、実機に対して API を試行できます。
ただし、`/control/*` や `/navigation/*` などの制御 API は実際にロボットを動作させるため、
周囲の安全と非常停止手段を確認した上で実行してください。

## 公開リファレンス

実機が手元にない場合でも、公開版の OpenAPI リファレンスで API 仕様を確認できます。
公開版は仕様確認用であり、実機に接続されていないため実行系の確認は実機側の
OpenAPI フロントエンドで行ってください。

- [TriOrb REST API Reference](https://triorb-inc.github.io/TriOrb-AMR-Robot-Controller/)
