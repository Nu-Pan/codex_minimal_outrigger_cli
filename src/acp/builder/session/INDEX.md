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
- oracle.acp_builder.session.join 由来の互換入口を収める package。既存の acp.builder.session.join 配下 import を維持するための初期化ファイルと、正本側実装を再 export する conflict resolution 旧 import 経路を扱い、この階層自体は session join の実装本体を持たない。

## Read this when
- acp.builder.session.join 配下の互換 package や旧 import 経路が残っている理由を確認したいとき。
- session join conflict resolution の呼び出し元移行、互換 import の削除可否、または正本側実装への再 export の存在理由を確認したいとき。
- oracle.acp_builder.session.join から realization 側へ置かれた互換入口の配置を調べているとき。

## Do not read this when
- session join の具体的な処理内容、衝突解決の挙動、API、判定内容、実装詳細を確認・変更したいときは、実体を持つ正本側実装へ進む。
- 互換 import の実際の利用箇所や移行状況を調査したいときは、参照元検索を行う。
- 旧 import 経路や公開面維持に関係しない session join 作業では読む必要はない。

## hash
- c4f82f00262fb4c596f742c2dceb9dad9ae15cd0753c5e96470101c3a529da82
