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
- realization refactor fork の一連の実行ライフサイクルを管理する CLI 実装。対象選択、file 単位の agent 調査・修正、差分検証、state 更新、処理単位の commit、完了判定、unresolved 所見管理、change summary と fork report の保存を一体として扱う。
- 中断時・エラー時には Codex 子プロセス停止、rollback、run state 更新、進捗と cleanup 警告を含む report 保存までを行う。realization refactor の fork 動作や run isolation、完了状態、report 内容を変更・検証する際の実装入口。

## Read this when
- realization refactor fork サブコマンドの処理フロー、対象 file の反復処理、agent 出力の検証、差分制約、commit 単位を確認するとき
- unresolved finding、investigation_required state、自然完了・未解決完了の判定、fork report や change summary の生成を変更するとき
- KeyboardInterrupt や BaseException 発生時の run 回収、子プロセス停止、rollback、error report の挙動を調査するとき

## Do not read this when
- refactor state のデータ構造や対象選択そのものを変更する場合は、先に commons.runtime_refactor の実装を読む
- run の開始・join・abandon や一般的な worktree isolation の仕様を変更する場合は、runtime_run 関連実装と対応する oracle 文書を直接読む
- file 単位の review agent parameter や change summary の Structured Output 定義だけを確認する場合は、対応する parameter builder を直接読む

## hash
- 165ba73867d16506ab5b0429eef022ac88c703be43b675d78072ccd579a10b91
