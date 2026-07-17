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
- oracle.acp_builder.session.join 互換の session join package。既存 import 経路を維持するための初期化入口と、conflict resolution builder への薄い委譲経路を含む。

## Read this when
- acp.builder.session.join 配下の互換 import 経路を維持・変更・削除するとき。
- session join の conflict resolution builder の canonical 実装や caller の移行状況を確認するとき。

## Do not read this when
- session join の具体的な処理仕様や canonical 実装を確認したいとき。
- 互換 import の利用箇所や公開面からの参照有無を調査したいとき。

## hash
- d78771836a227f47b04324ae77ae1d2d397b5711294d372ce6341f3bc19c694b
