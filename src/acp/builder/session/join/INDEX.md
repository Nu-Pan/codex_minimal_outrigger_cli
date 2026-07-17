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
- session join の conflict resolution parameter builder への互換 import 経路を提供する薄い委譲モジュール。canonical 実装は oracle 側にあり、既存 caller の移行期間だけ参照する入口。

## Read this when
- `acp.builder.session.join.conflict_resolution` からの互換 import を維持・変更・削除するとき
- session join の conflict resolution builder の canonical 実装や caller 移行状況を確認するとき

## Do not read this when
- canonical な conflict resolution の仕様や実装そのものを確認したいときは、oracle 側の実装を直接読む
- session join の conflict resolution と無関係な builder や import 経路を調査するとき

## hash
- a2fdf006a9bd704c87163fcbcbc578e6489317021efbb9c0ccbd988ad1483632
