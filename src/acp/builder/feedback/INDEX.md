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
- feedback issue の同一性判断用パラメータ builder を、正本実装から ACP builder 側へ再公開する薄い adapter。実際の判断ロジックは持たず、対応する oracle 実装への入口を提供する。

## Read this when
- ACP builder から feedback issue の同一性判断用パラメータ生成を参照・追跡するとき
- この builder の公開名や再公開元を確認するとき

## Do not read this when
- feedback issue の正本となる同一性判断ロジックを理解・変更するときは、対応する oracle 実装を直接読む
- feedback 以外の ACP builder や、別の feedback 処理の責務を調べるとき

## hash
- a778c211293705ae8907658cee05b702ed4eebb56e7d1792d319d6b5824afc33

# `verify_issue.py`

## Summary
- feedback issue verification の正本 builder を再公開する adapter。対応する oracle 実装から、feedback issue 検証用パラメータ builder を利用するための入口を提供する。

## Read this when
- feedback issue verification の builder の利用箇所や公開入口を確認するとき。
- feedback issue 検証用パラメータ builder の import/export 経路を確認するとき。

## Do not read this when
- feedback issue verification の正本ロジックや仕様を確認するときは、対応する oracle 実装を直接読む。
- feedback 以外の ACP builder を調査するとき。

## hash
- 33965a551ca9170b82e3525d1bbe5fe09f5ccefd6b48fb6c228dfa80ca16a667
