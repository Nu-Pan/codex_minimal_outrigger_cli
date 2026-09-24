# `__init__.py`

## Summary
- feedback issue の正規化と remediation に関する builder adapter の入口で、各処理の構築定義は対応する oracle 実装へ委譲される。

## Read this when
- 互換 builder 経路から feedback issue の同一性判断や remediation の agent call をたどり、正本実装への入口を確認するとき。

## Do not read this when
- prompt の内容や parameter 構築の根拠が必要な場合は、正規化または remediation を担う oracle builder 実装を直接読む。
- feedback issue 以外の builder の役割を調べる場合は、該当する builder の項目へ進む。

## hash
- 28770e46bfdfbe5d96dcfd77ca52a041aa67413166a532dc6aeebdce14f8e03c

# `normalize_issue.py`

## Summary
- フィードバック observation と既存候補の issue 同一性を判断する builder を oracle 定義から再公開する互換 adapter。prompt と起動 parameter の生成は oracle 側に委譲する。

## Read this when
- フィードバック報告処理から同一性判断用 builder への import 経路や、この adapter の役割を確認するとき。

## Do not read this when
- 同一性判断の prompt や parameter の内容を確認・変更するときは oracle 側の定義へ進む。remediation builder の経路を調べるときは remediation 側へ進む。

## hash
- 5202e2148d7808b8f162a5e470d561a74476d8458b5984a569f9ed4b7cc110ec

# `remediate_issue.py`

## Summary
- feedback issue の修復用 builder を公開する互換 import 層で、prompt や起動 parameter の組み立ては oracle 側の実装が担う。

## Read this when
- 既存 caller が修復用 builder を互換 import 経由で参照する仕組みを確認するとき。

## Do not read this when
- 修復用 prompt や起動 parameter の生成動作を調べる・変更するときは、oracle 側の実装へ進む。
- feedback issue の正規化用 builder を調べるときは、正規化を担う対象へ進む。

## hash
- 9c21670b2d21e244b4018e41ef35f89e7ea83dc64c90d34ccc86e1861ba3a318
