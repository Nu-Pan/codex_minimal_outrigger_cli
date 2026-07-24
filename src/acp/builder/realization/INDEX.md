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
- realization apply 用の builder adapter を提供するディレクトリ。apply 処理の builder 実装や、fork 適用時の接続点・prompt 加工を確認する入口。

## Read this when
- realization apply の builder adapter の責務や実装を確認するとき
- `cmoc realization apply fork` の builder 接続点、launch_exec 呼び出し元、raw oracle diff のコードフェンス保護を変更・検証するとき

## Do not read this when
- apply 処理以外の builder 実装を確認するとき
- fork 適用処理そのものの実装詳細を調査するとき
- 正本 builder の仕様や prompt 内容を変更するとき
- builder adapter の詳細実装を直接確認する場合

## hash
- b300ffea7c1e9d9e098684d987aa02f5555f4558f2b09da1e59fe175d59c9f17

# `refactor`

## Summary
- realization refactor 用の builder adapter パッケージ。refactor 処理の builder 関連実装への入口で、fork 向けの builder adapter を下位要素として含む。

## Read this when
- realization refactor の builder adapter の責務や実装入口を確認するとき。
- realization refactor fork の builder adapter、change summary の prompt 生成、file review and fix の oracle builder 接続を調査・変更するとき。

## Do not read this when
- builder adapter 以外の refactor 処理を確認するとき。
- oracle 側の正本仕様や parameter 定義、fork 以外の builder 実装、一般的な prompt fence 処理を確認するとき。

## hash
- 09a4c6e29ef35e2beb3fb39ff297012a89995ad889430bef54a6ad46f9ec983c
