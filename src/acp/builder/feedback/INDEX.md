# `__init__.py`

## Summary
- feedback の issue 正規化・検証用 builder adapter への入口。対応する oracle 実装に基づく feedback 処理の役割を確認する。

## Read this when
- feedback issue の normalization または verification に関わる builder adapter の責務を確認するとき。

## Do not read this when
- feedback issue の具体的な正規化・remediation 仕様や実装詳細を直接確認したいときは、対応する oracle file を読む。

## hash
- 28770e46bfdfbe5d96dcfd77ca52a041aa67413166a532dc6aeebdce14f8e03c

# `normalize_issue.py`

## Summary
- 対象は feedback issue の同一性判断用 builder への互換 import 経路を提供する。実装内容や仕様を確認する必要があり、同じ feedback builder 領域で互換的な import 経路を探すときの入口になる。

## Read this when
- feedback issue の同一性判断 builder を利用するコードの import 経路や互換性を確認するとき
- この互換モジュールがどの builder を再公開しているかを確認するとき

## Do not read this when
- issue 同一性判断 builder の実装仕様やパラメータ生成ロジックを確認したいときは、対応する oracle の実装を直接読む
- feedback issue 以外の builder や、互換 import 経路に関係しない処理を調べるとき

## hash
- 5202e2148d7808b8f162a5e470d561a74476d8458b5984a569f9ed4b7cc110ec

# `remediate_issue.py`

## Summary
- 互換 import 経路として、feedback issue remediation builder の公開関数を oracle 実装から利用できるようにする入口。

## Read this when
- feedback issue remediation のパラメータ builder を利用する際に、src 側の互換 import 経路を確認したいとき。
- feedback 配下で issue remediation builder の import 境界や公開関数を確認するとき。

## Do not read this when
- 実際の feedback issue remediation パラメータ生成ロジックや仕様を確認・変更するときは、対応する oracle 実装を直接読む。
- feedback issue remediation 以外の builder、または一般的な feedback 処理の責務を調べるとき。

## hash
- 9c21670b2d21e244b4018e41ef35f89e7ea83dc64c90d34ccc86e1861ba3a318
