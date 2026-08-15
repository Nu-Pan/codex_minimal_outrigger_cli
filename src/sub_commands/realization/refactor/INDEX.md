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
- `realization refactor fork` の full-cycle workload を実行する CLI runtime。refactor state と INDEX を初期化し、対象 realization file ごとに agent による調査・修正、差分検証、state 更新、処理単位の commit を行う。
- current fork 内の unresolved finding、rename、agent commit、想定外差分、interrupt/error cleanup を管理し、investigation_required と unresolved target の一致を検査して完了理由を判定する。
- 正常完了・中断・エラー時に fork report と primary report を保存し、join または abandon へ進めるための TerminalResult を返す。realization refactor fork の lifecycle 全体を扱う入口であり、個別の builder、state 管理、run lifecycle の詳細確認より先に読む対象。

## Read this when
- realization refactor fork の実行順序、run state、interrupt/error cleanup、joinable 公開条件を確認するとき。
- 対象 realization file の agent call、変更 path 検証、git commit、unresolved finding の保持と rename reconciliation を確認するとき。
- refactor state の完了不変条件、completion reason、fork report、change summary の生成条件を確認するとき。

## Do not read this when
- 個別の agent prompt や change summary の出力契約だけを確認する場合は、対応する builder を直接読む。
- refactor target の state 同期・選択・永続化の仕様だけを確認する場合は、refactor state 実装を直接読む。
- editing run の一般的な開始・join・abandon・rollback lifecycle だけを確認する場合は、run lifecycle の実装または仕様を直接読む。

## hash
- d4d51c0019f329a98249c8d9c64e7182e429b4b5bfae35112c730a2411cb9cd4
