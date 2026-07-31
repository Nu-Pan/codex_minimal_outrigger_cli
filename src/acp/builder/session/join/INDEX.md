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
- session join の競合解消パラメータ生成を再公開する互換 import 経路。canonical 実装へ委譲し、競合 path を prompt に埋め込む際の code fence 保護を補う。

## Read this when
- `acp.builder.session.join.conflict_resolution` の import 互換性や、session join の競合 path prompt 生成を確認・変更するとき。

## Do not read this when
- canonical な競合解消パラメータ生成の仕様や実装本体を確認するとき。oracle 側の canonical path を直接読む。

## hash
- 5716153998dadc61c97eb12b63f0518a34c1111910b718b090ce9f8a249557da
