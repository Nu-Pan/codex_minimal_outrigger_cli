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
- feedback issue の同一性判断 builder を既存の import 経路から利用するための互換層です。実装の正本ではなく、対応する oracle の builder を再公開します。

## Read this when
- feedback issue の同一性判断 builder をこの互換 import 経路経由で利用または追跡するとき。

## Do not read this when
- builder の本来の仕様や実装詳細を確認するときは、対応する oracle file を直接読みます。

## hash
- 5202e2148d7808b8f162a5e470d561a74476d8458b5984a569f9ed4b7cc110ec

# `verify_issue.py`

## Summary
- feedback issue 検証用 builder の互換 import 経路。実装本体は oracle 側にあり、このファイルは builder 関数を再公開して下位の import 利用者から参照できるようにする。

## Read this when
- feedback issue 検証用 builder の互換 import 経路や公開シンボルを確認するとき。

## Do not read this when
- builder の prompt 構築や起動パラメータの仕様・実装を確認するときは、対応する oracle 側の実装を直接読む。

## hash
- 9267c65850b6c1fe972e4a2e51019b4dc52c0677844e38bdfbf8740668bfc02a
