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
- realization refactor fork の一連の実行単位を管理する CLI runtime。対象 realization file の選択、agent による調査・修正、差分と commit の検証、refactor state の更新、unresolved 所見の追跡、完了判定、変更概要・fork report の生成を担う。
- 正常終了・中断・エラー時の run lifecycle、子プロセス停止、rollback、state 更新、report 保存を一貫して処理する下位実装への入口。

## Read this when
- `cmoc realization refactor fork` の実行フロー、処理単位の commit、unresolved 所見、完了理由、fork report を変更・調査するとき
- refactor agent の変更範囲検証、commit 禁止、INDEX refresh 後の差分検査、run の中断・エラー cleanup を確認するとき

## Do not read this when
- realization refactor の agent prompt や Structured Output schema 自体だけを確認したいときは、対応する builder 実装を直接読む
- run lifecycle 共通処理、refactor state 管理、report 表示の共通仕様だけを調べるときは、それぞれの `commons` 実装または oracle 文書を直接読む
- 他の realization refactor サブコマンドの処理を調べるとき

## hash
- cb9b45502918d3ff133da9b9042a76580df6167e635a756f30f82e8ee944a5e7
