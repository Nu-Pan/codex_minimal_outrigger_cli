# `__init__.py`

## Summary
- feedback の issue 正規化・検証に対応する builder adapter パッケージ。対応する oracle 実装を起点に、feedback の normalize／verify 処理を確認する際の入口となる。

## Read this when
- feedback issue の normalization または verification に関する builder adapter の構成を確認するとき
- 対応する oracle の normalize_issue／verify_issue 実装との対応関係を確認するとき

## Do not read this when
- feedback 以外の builder adapter を調べるとき
- 正規化・検証処理そのものの詳細を確認する場合は、対応する oracle file を直接読む

## hash
- 5be652524e2cf162bcb1e9f7afa2fb8fff79cfa9828f6648565cc06ee9728f4c

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

# `verify_issue.py`

## Summary
- 対象は feedback issue verification builder の互換 import 経路を提供する薄いラッパーであり、対応する oracle 実装への入口として扱う。
- feedback issue の verification parameter builder を利用・変更・挙動確認する作業で、互換 import 経路の役割を確認するために読む。
- oracle 側の実装内容や verification builder の詳細な仕様を確認する必要がある場合は、この対象ではなく対応する oracle file を直接読む。

## Read this when
- feedback issue verification parameter builder の import 経路や互換ラッパーの責務を確認するとき。
- この互換経路を利用するコードの参照先を判断するとき。

## Do not read this when
- verification parameter builder の実装ロジック、入力検証、出力仕様を確認するとき。
- 互換 import 経路を経由せず、oracle 実装を直接調査・変更できるとき。

## hash
- 9267c65850b6c1fe972e4a2e51019b4dc52c0677844e38bdfbf8740668bfc02a
