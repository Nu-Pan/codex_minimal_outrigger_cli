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
- oracle.acp_builder.session.join 互換の package 初期化ファイル。既存の import 互換性を維持するための入口で、実装本体は持たない。
- session join の競合解消パラメータ生成を canonical 実装へ委譲する互換 import 経路。競合 path を prompt に埋め込む際の code fence 保護を補う。

## Read this when
- acp.builder.session.join 配下の import 互換性や package 配置を確認するとき。
- session join の競合 path prompt 生成や、その互換 import 経路を確認・変更するとき。

## Do not read this when
- session join の具体的な処理内容や振る舞いを確認したいとき。
- canonical な競合解消パラメータ生成の仕様・実装本体を確認したいとき。
- 互換 import の利用箇所や、利用者向け公開面から参照がなくなったかを調査したいとき。

## hash
- b78ac1774e072a4c4edadc55b484e4a181c4fdfaa41c55e1307bb3086f69b906
