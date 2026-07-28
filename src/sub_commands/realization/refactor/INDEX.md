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
- realization refactor fork の一連の実行ライフサイクルを管理する CLI サブコマンド実装。対象選択、agent call による調査・修正、差分検証、refactor state 更新、処理単位の commit、完了判定、変更概要生成、fork report 保存までを同一 run として扱う。
- 中断時・エラー時には Codex 子プロセス停止、rollback、run state 更新、report 保存を行い、確定済み処理単位と unresolved finding を追跡可能な状態で公開する。

## Read this when
- realization refactor fork の実行フロー、対象処理単位、agent call 後の差分検証、state 更新、commit、完了条件を変更・調査するとき
- fork report の内容、unresolved finding の管理、正常完了・中断・エラー時の cleanup と run state 遷移を確認するとき

## Do not read this when
- realization refactor の単一ファイルに対する調査・修正 agent parameter の生成だけを確認するときは、file review and fix の実装を読む
- 変更概要の Structured Output 生成仕様だけを確認するときは、change summary の実装を直接読む
- 一般的な editing run のライフサイクルや共通 Git 差分処理だけを確認するときは、対応する runtime lifecycle 実装を直接読む

## hash
- 74a038f4f57d80d46b9fa5c5febf8994061f43bd58473fb476a9ce2d7f1a5a25
