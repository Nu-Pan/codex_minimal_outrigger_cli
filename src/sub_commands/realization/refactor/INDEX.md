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
- `realization refactor fork` の CLI 実行全体を担う workload 実装。refactor run の初期化、対象 realization file ごとの agent 調査・修正、差分と commit の検証、refactor state の更新、unresolved finding の追跡、完了判定、report 保存、割り込み・エラー時の rollback と run state 更新を一つの lifecycle として扱う。
- realization refactor fork の実行制御、処理単位の commit、agent が作成した想定外差分や commit の拒否、変更概要と unresolved finding の report 出力を確認したい場合の実装上の入口である。

## Read this when
- `cmoc realization refactor fork` の起動から完了または失敗までの制御フローを変更・調査するとき。
- 対象選択、処理単位の commit、agent call 境界、refactor state、unresolved finding、完了理由、fork report の整合性を確認するとき。
- KeyboardInterrupt、agent error、cleanup failure、run の joinable/error 遷移に関する挙動を確認するとき。

## Do not read this when
- refactor agent に渡すプロンプトや Structured Output の仕様だけを確認したい場合は、file review builder の実装を直接読む。
- refactor state の選択・同期ロジックだけを確認したい場合は、runtime refactor 共通実装を直接読む。
- run の一般的な isolation、state、join/abandon 契約だけを確認したい場合は、対応する editing run / run isolation の正本仕様を読む。

## hash
- 266484a2dc49590c168afc052fe7b25355852c67414036d5e3d06b65b46fd92f
