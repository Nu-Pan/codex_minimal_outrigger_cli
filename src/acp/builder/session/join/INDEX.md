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
- session join の競合解決パラメータ生成関数を、旧来の import 経路から利用するための互換モジュール。canonical 実装を呼び出した後、競合ファイル一覧を prompt に追加する際の code fence を保護する。

## Read this when
- `acp.builder.session.join.conflict_resolution` からの互換 import や、session join の競合 path prompt 生成を確認・変更するとき。

## Do not read this when
- canonical 実装の仕様や本体ロジックを確認するときは、`{{work-root}}/oracle/src/oracle/acp_builder/session/join/conflict_resolution.py` を直接読む。
- 全 caller が canonical oracle path を直接利用し、この互換経路の削除可否だけを判断するとき。

## hash
- 6559a5e1d28524b6cae11536f0708bc90fc8ecebcf69a0fd3f9877eeee379818
