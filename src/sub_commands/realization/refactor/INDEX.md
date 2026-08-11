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
- realization の refactor fork 全体を単一の lifecycle として実行する CLI サブコマンド実装。run の初期化、refactor state と INDEX の同期、realization file 単位の agent 調査・修正、差分と commit の検証、current fork 内の unresolved 管理、完了判定、joinable/error/interruption 状態の cleanup、fork report と完了ログの生成を担う。refactor fork の実行フロー、処理単位の進捗、完了不変条件、agent の commit・想定外変更・遅延 descendant に対する安全検査を確認する際の入口である。

## Read this when
- realization refactor fork サブコマンドの実行 lifecycle、処理単位の選択と commit、unresolved finding の追跡、自然完了または unresolved 完了の判定を調査するとき
- refactor fork における interruption/error cleanup、run state の更新、rollback、Codex child 停止、fork report の内容を確認するとき
- agent が変更できる path、agent commit の拒否、INDEX refresh 後の差分検証、rename と refactor state の対応付けを確認するとき
- refactor fork の完了ログ、変更概要、state 集計、report 出力を変更またはレビューするとき

## Do not read this when
- realization refactor の正本仕様や CLI 契約だけを確認する場合は、対応する app_spec の仕様文書を直接読む
- 単一処理単位の agent prompt／Structured Output parameter の内容だけを確認する場合は、file review builder の実装を直接読む
- change summary の入力契約や生成規則だけを確認する場合は、change summary builder を直接読む
- 共通の editing run、process tracking、INDEX refresh、git 差分分類の一般仕様だけを調査する場合は、各共通 runtime module または対応する正本仕様を直接読む

## hash
- e3de3b6bc2648c36de48673ab417cc25152c43458b03958519731371facbd93a
