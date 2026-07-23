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
- realization refactor fork の full-cycle CLI workload を実装する。対象選択、file 単位の調査・修正、refactor state の同期、差分検証と commit、unresolved 所見の current fork 内管理、完了判定、change summary と fork report の生成までを一つの lifecycle として扱う。
- `cmoc realization refactor fork` の実行入口であり、run state・worktree 差分・refactor state・agent Structured Output の整合性を検証する下位処理への入口でもある。

## Read this when
- realization refactor fork の CLI 動作、処理単位の実行順序、対象選択や unresolved 所見の扱いを変更・調査するとき
- refactor state の investigation_required と current fork の完了条件の関係を確認するとき
- realization refactor fork の commit、rollback、error、KeyboardInterrupt、report 生成を確認するとき
- refactor agent の findings または change summary の Structured Output 検証を調査するとき

## Do not read this when
- realization refactor の一般仕様だけを確認したいときは、oracle の realization_refactor 仕様を先に読む
- file 単位の agent パラメータ生成や個別 review・fix の挙動だけを確認するときは、対応する builder または file review 実装を直接読む
- run の共通 lifecycle、差分分類、state 更新、report の一般実装だけを確認するときは、対応する lifecycle・runtime・report モジュールを直接読む
- 他の realization refactor サブコマンドや fork 以外の処理を調査するとき

## hash
- 21d27f1c7b22d9234851e0b71c47ba3550b4aa2a11b6723bcb235443ac7503e6
