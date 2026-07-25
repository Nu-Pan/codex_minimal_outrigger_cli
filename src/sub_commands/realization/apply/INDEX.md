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
- `cmoc realization apply fork` の CLI 実行処理を担当する。realization apply agent を実行し、許可差分を検証・commit して run を joinable に更新し、fork report を保存する。失敗時は差分を rollback して error state と report を記録する。
- realization apply の run 作成、oracle 差分構築、Codex 実行、INDEX 更新、差分検査、状態遷移、エラー回収までの制御フローと補助処理への入口である。

## Read this when
- `cmoc realization apply fork` の CLI 挙動、run lifecycle、agent 実行、差分検証、commit、joinable/error state、fork report の処理を変更・調査するとき。
- apply fork の失敗時 rollback、開始直後の run 回収、想定外差分の扱いを確認するとき。

## Do not read this when
- realization apply agent のプロンプトや起動パラメータ生成だけを変更・調査するときは、起動パラメータ実装を直接読む。
- run 状態管理、差分取得、commit、INDEX 更新、report 生成の共通仕様や実装だけを確認するときは、対応する `commons.runtime_run*` または report 実装を直接読む。
- `cmoc realization apply fork` 以外のサブコマンドの CLI 本体を変更・調査するとき。

## hash
- fe6bf6326ac8a21538a5397a1c2f8814950b4e36b760cc95c08df010617a09b8
