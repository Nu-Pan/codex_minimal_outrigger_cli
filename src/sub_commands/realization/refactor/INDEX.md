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
- realization refactor fork の CLI 実行全体を管理するエントリポイント。編集 run の初期化、対象ファイルごとの Codex 調査・修正、差分と state の検証・commit、自然完了または中断・エラー時の rollback、joinable 化、fork report 保存までを担当する。

## Read this when
- realization refactor fork の実行フロー、対象選択、findings の検証、run state 遷移、差分検証、report 生成を変更・調査するとき
- refactor loop の中断・エラー処理や unresolved finding の扱いを確認するとき

## Do not read this when
- file 単位の調査・修正 agent の prompt や findings schema 自体を変更するときは、対応する builder 実装を直接読む
- refactor state の保存・同期・対象選択の共通処理を変更するときは、commons.runtime_refactor を直接読む
- run の lifecycle、差分分類、commit、rollback の共通処理を変更するときは、sub_commands.run.lifecycle を直接読む

## hash
- dae2d73cf6373ffedd8889edcbaaf2f8dc8f3fba9434fcb238fa8175227c5dc3
