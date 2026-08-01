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
- session join の互換 import 入口と、競合解決パラメータ生成の互換経路をまとめた realization package。具体的な session join 処理は持たず、canonical 実装への接続と旧 import 経路の維持を担う。

## Read this when
- acp.builder.session.join 配下の互換 import 経路や公開面を確認・変更するとき。
- 競合 path の prompt 埋め込み時に code fence 保護が必要な挙動を確認するとき。

## Do not read this when
- session join の具体的な処理や振る舞いを確認するとき。
- canonical な競合解決パラメータ生成を変更するとき。
- 互換 package の実際の参照元や利用箇所を調査するとき。

## hash
- 1ba81f951b4287b36cc38d6e50eaf6ccc5b0eafe9449c675c1415603e03cb050
