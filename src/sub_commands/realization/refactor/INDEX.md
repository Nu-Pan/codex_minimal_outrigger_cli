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
- realization refactor fork の CLI 実行単位を統括する full-cycle workload。run の開始・初期化、対象 file ごとの agent 調査と修正、state 同期、commit、unresolved 管理、完了判定、joinable/error/interruption cleanup、fork report 生成までを一貫して扱う。
- refactor state と run worktree の差分・HEAD・agent の commit・INDEX 更新後の想定外差分を検証し、current fork の進捗と unresolved finding を report に反映する。下位の file review、change summary、runtime lifecycle、state 管理の入口として機能する。

## Read this when
- `cmoc realization refactor fork` の実行フロー、処理単位、完了理由、unresolved target の扱いを確認するとき
- realization refactor fork における run state、割り込み・エラー時の rollback、Codex child の停止、joinable 公開、fork report の生成を変更・調査するとき
- refactor state と実際の realization 差分、agent commit、rename、INDEX refresh の整合性検証を確認するとき

## Do not read this when
- 単一 file の調査・修正 prompt や Structured Output 契約だけを確認したいときは、file review builder の実装を直接読む
- 正常完了時の変更概要生成だけを確認したいときは、change summary builder を直接読む
- 一般的な editing run の join・abandon・state 遷移だけを確認したいときは、runtime lifecycle や run isolation の仕様を直接読む

## hash
- 1fc722866cae61f7242fe52600be947a786fd71c33c59b3ba6d1e27dc4d3daf2
