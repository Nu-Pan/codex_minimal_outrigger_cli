# `__init__.py`

## Summary
- realization workload を builder に適応するための adapter。realization workload の builder 連携を扱う実装への入口。

## Read this when
- realization workload の builder adapter や、その連携箇所を確認・変更するとき。

## Do not read this when
- builder の共通処理や realization workload 自体の内容を直接確認・変更するとき。

## hash
- cd24953f9993d22add52453bee8a2c6dd9c2fc85ecd238c962f1cc82066eec92

# `apply`

## Summary
- realization apply 用の builder adapter を提供するモジュール。apply 処理の builder 実装へ進む入口となる。
- `cmoc realization apply fork` 向けの builder adapter を収めるディレクトリ。fork 適用時の launch_exec 用 builder の公開接続点を提供する。

## Read this when
- realization apply の builder adapter の責務や実装を確認するとき
- apply 処理の builder 実装を辿るとき
- `cmoc realization apply fork` の builder adapter、launch_exec parameter builder の prompt 生成、または公開 API を確認・変更するとき

## Do not read this when
- apply 処理以外の builder 実装を確認するとき
- builder adapter の詳細実装を直接確認する場合
- oracle 側の正本 builder の仕様や prompt 構成を確認するとき
- fork 適用処理そのもの、または fork 以外の apply 処理を調査するとき

## hash
- 0e33ebb9d1b31055cffac72f2ddcc5a658de4e89fc3c84bfac7c06914dd38047

# `refactor`

## Summary
- realization refactor の builder adapter パッケージ。refactor 処理の builder 関連実装への入口で、fork 用 builder の公開入口を含む。

## Read this when
- realization refactor における builder adapter の責務や実装入口を確認するとき。
- fork 用の change summary parameter builder または file review parameter builder の公開入口・接続先を確認するとき。

## Do not read this when
- builder adapter 以外の refactor 処理を確認するとき。
- builder の具体的な生成ロジックを確認・変更するとき。

## hash
- c858be059c1590289ceaf3b0e4157f0af24da7eadb5bb53293bad55c49d1a4bd
