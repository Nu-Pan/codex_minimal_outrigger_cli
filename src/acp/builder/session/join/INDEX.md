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
- session join の競合解決パラメータ生成における互換 import 経路を提供する。canonical 実装を呼び出し、競合 path を含む prompt の code fence を保護して既存 caller へ再公開する。

## Read this when
- session join の競合解決パラメータ生成を変更・調査するとき
- 旧来の `acp.builder.session.join.conflict_resolution` import 経路や prompt 内の競合 path 処理を確認するとき

## Do not read this when
- canonical な競合解決仕様や実装そのものを確認したいときは、oracle 側の canonical 実装を直接読む
- session join の競合解決と無関係な builder 処理を調査するとき

## hash
- 4dcfb44b13ca6c1fe3331adce20cd02ca3ec0d0ae3da8b8d44e7c95fffacd882
