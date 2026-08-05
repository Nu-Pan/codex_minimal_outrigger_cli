# `__init__.py`

## Summary
- realization workload サブコマンドのパッケージ入口。

## Read this when
- realization workload サブコマンドの実装や構成を確認するとき。

## Do not read this when
- realization workload サブコマンドに関係しない処理を確認するとき。

## hash
- 45f2cdf62d9edd181a1f1cc14734db2757e556059630746b1486c1bd5d1101b4

# `apply`

## Summary
- realization の apply 処理を構成するモジュール群。apply workload の実装入口と、`cmoc realization apply fork` の実行・run lifecycle・差分検査・commit・状態遷移・fork report 保存を扱う。

## Read this when
- realization の apply workload の内容を調査または変更するとき。
- `cmoc realization apply fork` の CLI 動作、run lifecycle、agent 差分の許可範囲、commit・joinable/error 遷移、fork report の生成を確認または変更するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- apply agent に渡す launch parameter だけを確認するとき。
- run の join・abandon 処理や共通 lifecycle の実装を確認するとき。
- realization apply の正本仕様を確認するとき。

## hash
- 6328a3fb5fd66ea735889bff8f471e4af11f51a9b873ee20bec41d585ea8b27e

# `refactor`

## Summary
- realization のリファクタリング処理を扱うパッケージで、関連するリファクタリング処理への入口となる。
- realization refactor fork の CLI 実行全体を担い、run の初期化、対象 realization file ごとの調査・修正、差分・commit 検証、state 更新、unresolved finding の追跡、完了判定、report 保存、割り込み・エラー時の rollback までを一つの lifecycle として実装する。

## Read this when
- realization のリファクタリング作業の内容や構成を確認するとき。
- `cmoc realization refactor fork` の起動から完了または失敗までの制御フローを変更・調査するとき。
- 対象選択、処理単位の commit、agent call、refactor state、unresolved finding、完了理由、fork report の整合性を確認するとき。
- KeyboardInterrupt、agent error、cleanup failure、run の joinable/error 遷移に関する挙動を確認するとき。

## Do not read this when
- realization のリファクタリング以外の処理を確認するとき。
- refactor agent に渡すプロンプトや Structured Output の仕様だけを確認したいとき。
- refactor state の選択・同期ロジックだけを確認したいとき。
- run の一般的な isolation、state、join/abandon 契約だけを確認したいとき。

## hash
- d4e6955da20c078f4106e7b2b8a0c260f1ed63f936eef65139f23f7c0140a610
