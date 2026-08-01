# `__init__.py`

## Summary
- oracle.acp_builder.session.join 互換の package 初期化ファイル。既存の acp.builder.session.join.* import を維持するためだけに残る互換入口であり、実装本体は持たない。

## Read this when
- acp.builder.session.join 配下の import 互換性や公開面維持のために、この package が存在する理由を確認したいとき。
- oracle.acp_builder.session.join から realization 側への互換 package 配置を調べているとき。

## Do not read this when
- session join の具体的な処理内容や振る舞いを確認したいとき。
- 互換 import の利用箇所を探したいとき。
- realization 側と利用者向け公開面から参照がなくなったかを判断するために、実際の参照元を調査したいとき。

## hash
- 072255c777a758fe7fa412dab9c417d50fc420b5871fae782e550e97a8c1b483

# `conflict_resolution.py`

## Summary
- session join の競合解決用パラメータを再公開する互換 import 経路。canonical 実装を呼び出し、競合 path を prompt に安全に埋め込むための fence 保護を追加する。

## Read this when
- session join の競合解決パラメータ生成や、旧 import 経路との互換性を確認・変更するとき。
- 競合 path の prompt 埋め込みと code block fence 保護の挙動を確認するとき。

## Do not read this when
- canonical な競合解決パラメータ生成そのものを変更するときは、oracle 側の canonical 実装を直接読む。
- session join の競合解決と無関係な builder や prompt 処理を扱うとき。

## hash
- de65cce597118bf119865b66ea413acfbcafb953c0a48e462279853faf6ae505
