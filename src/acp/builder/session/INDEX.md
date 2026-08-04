# `__init__.py`

## Summary
- oracle.acp_builder.session との互換性を保つための package 初期化ファイル。既存の acp.builder.session.* import を維持するためだけに残されている。

## Read this when
- acp.builder.session.* import の互換維持経路を確認する。
- oracle.acp_builder.session 参照への移行や、互換 package を削除できる条件を確認する。

## Do not read this when
- session 実装の挙動や構成要素を確認したい場合。
- 新規機能の入口や通常の公開 API を探している場合。

## hash
- 1c24d1b1720d385b0f3388d0c70ebd4fa053c26df3a40f54e8cb91484c901dc8

# `join`

## Summary
- session join の互換 package。既存の `acp.builder.session.join.*` import 経路を維持する初期化入口と、canonical な競合解決実装を再公開する薄いアダプターを含む。

## Read this when
- session join 配下の互換 import 経路や公開面を確認したいとき。
- 競合解決 parameter の互換ラッパー、競合 path の prompt 埋め込み、code block fence 保護の挙動を調査・変更するとき。
- oracle 側の canonical session join 実装から realization 側への互換 package 配置を確認するとき。

## Do not read this when
- session join の具体的な処理内容や canonical な conflict resolution 仕様を確認したいとき。
- 互換 import の利用箇所や、利用者向け公開面から参照が残っているかを調査したいとき。
- session join の競合解決以外の builder や prompt fence 処理を調査するとき。

## hash
- ebc0c76048ec2647e12567aa155c34d2c0ee22d698f112435015171a6b1d88ea
