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
- oracle.acp_builder.session.join 互換の package 初期化ファイル。既存の acp.builder.session.join.* import を維持する互換入口で、実装本体は持たない。
- session join の競合解決パラメータ生成における互換 import 経路を提供し、canonical 実装を呼び出して競合 path を含む prompt の code fence を保護する。

## Read this when
- acp.builder.session.join 配下の import 互換性や公開面を確認するとき。
- session join の競合解決パラメータ生成、旧来の import 経路、prompt 内の競合 path 処理を変更・調査するとき。

## Do not read this when
- session join の具体的な処理内容や canonical な競合解決仕様を確認したいとき。
- 互換 import の利用箇所や、実際の参照元を調査したいとき。
- session join の競合解決と無関係な builder 処理を調査するとき。

## hash
- 43d74feddd2b7ae3e05419a6e0a5e15a7c277843546474ac3a149f313b4464ae
