# `__init__.py`

## Summary
- realization の apply 処理に関する workload を扱うモジュール。apply workload の実装を確認する入口となる。

## Read this when
- realization の apply workload の内容を調査・変更するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。

## hash
- d6d2ca470e50cfd6872e3d6ceaaf3a134b7f0dc8205826c843ca70d79352d5f7

# `fork.py`

## Summary
- `realization apply fork` の実行全体を管理し、差分追従 agent の起動結果を検査して joinable または error 状態の run として公開する CLI 実装。
- editing run の作成、oracle raw diff の構築、agent 実行、想定外変更と agent commit の検出、INDEX 再生成、処理単位の commit、rollback、fork report 保存を一つの処理単位として扱う。
- apply 固有の差分始点と accepted feedback observation を fork report に記録する。

## Read this when
- `cmoc realization apply fork` の CLI 挙動や run の成功・失敗状態を確認するとき。
- realization apply agent の変更許可範囲、commit 防止、INDEX 再生成、tracked Codex child の停止、差分の commit・rollback を調査するとき。
- fork report の完了理由、変更パス、return code、cleanup warning、feedback 情報の記録方法を確認するとき。

## Do not read this when
- agent 起動パラメータの構築方法だけを確認する場合は、launch parameter の実装を直接読む。
- editing run の共通ライフサイクルや git 差分操作の詳細だけを確認する場合は、共通 runtime lifecycle 実装を直接読む。
- apply の正本仕様や利用者向け手順だけを確認する場合は、対応する仕様書を直接読む。

## hash
- 9f6a8b4bf311f2bedd98f6202973ee9860609d4ff20043e38d32fa9658b983b9
