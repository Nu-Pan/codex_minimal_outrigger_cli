# `__init__.py`

## Summary
- realization apply 用の builder adapter を提供するモジュール。apply 処理の builder 実装へ進む入口となる。

## Read this when
- realization apply の builder adapter の責務や実装を確認するとき
- apply 処理の builder 実装を辿るとき

## Do not read this when
- apply 処理以外の builder 実装を確認するとき
- builder adapter の詳細実装を直接確認する場合

## hash
- f826a5bac8bd998fa3b25c1e1a4faaebe0a1a1fe62de19e3062e0f78c2b14d60

# `fork`

## Summary
- `cmoc realization apply fork` 用の builder adapter を収める初期化モジュールと、正本 builder を再公開して raw oracle diff のコードフェンスを保護する launch_exec adapter を扱う。fork 適用時の builder 接続点や prompt 加工を確認する入口。

## Read this when
- `cmoc realization apply fork` の builder adapter の責務や配置を確認するとき
- apply fork の launch_exec 呼び出し元、または raw oracle diff のコードフェンス保護を変更・検証するとき

## Do not read this when
- fork 適用処理そのものの実装詳細を調査するとき
- apply fork 以外の builder adapter や一般的な prompt fence 処理を調査するとき
- 正本 builder の仕様や prompt 内容を変更するとき

## hash
- 816032b626582de0e40a550c4da8cd59ddf15241b047f88a550c7d8f3ed007ab
