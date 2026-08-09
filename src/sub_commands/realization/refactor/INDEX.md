# `__init__.py`

## Summary
- realization のリファクタリング作業を扱うパッケージ。関連するリファクタリング処理への入口となる。

## Read this when
- realization のリファクタリング作業の内容や構成を確認するとき。

## Do not read this when
- realization のリファクタリング以外の処理を確認するとき。

## hash
- d070e139f0ebc38e439ff4bf3b37f76a7a536a3424248e4afcc0525de0573746

# `fork.py`

## Summary
- `realization refactor fork` CLI の full-cycle workload を実行する中核実装。対象選択、file 単位の agent 呼び出し、差分・commit・state の検証、unresolved finding の追跡、完了判定、interruption/error cleanup、fork report の生成までを一つの lifecycle として扱う。

## Read this when
- `cmoc realization refactor fork` の実行フロー、処理単位の commit、refactor state の更新、unresolved finding の完了条件を調査・変更するとき。
- realization refactor fork における agent の変更検証、git commit 禁止、INDEX 更新、run の joinable/error/interruption 処理を確認するとき。
- fork report の内容、完了理由、変更概要、cleanup warning の生成元を追跡するとき。

## Do not read this when
- realization refactor の agent prompt や change summary の入力形式だけを確認するときは、対応する builder 実装を直接読む。
- 編集 run の一般的な状態遷移や worktree isolation の正本仕様だけを確認するときは、対応する oracle doc を直接読む。
- 別の CLI subcommand や refactor fork 以外の処理の実装を調査するとき。

## hash
- efa28f51af82485c8669dd9c16ae2518a2f7b3f4c8f5d3c0fcace3a47365f678
