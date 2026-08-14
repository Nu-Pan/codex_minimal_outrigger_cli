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
- `realization apply` に関する実装をまとめたディレクトリ。apply workload の実装入口と、fork 実行のライフサイクル管理を確認するための対象。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- `cmoc realization apply fork` の実行フロー、run 状態遷移、差分検査、INDEX 生成、rollback、fork report の挙動を確認するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- apply agent のプロンプト生成や launch parameter だけを調査・変更するとき。
- run の共通ライフサイクルや `cmoc run join`／`cmoc run abandon` の処理だけを確認するとき。

## hash
- 38ca6e669e7abf551589b9c2b78fa166d1661d83f710d46c90880c07181b0bfe

# `refactor`

## Summary
- realization のリファクタリング処理をまとめるパッケージです。`cmoc realization refactor fork` の実行入口を提供し、run の初期化から対象ファイルごとの調査・修正、状態同期、検証、未解決事項の追跡、完了判定、エラー時の後処理、fork report の保存までを扱います。
- リファクタリング処理の全体フローや lifecycle を確認する際の入口であり、個別の agent prompt、共通 runtime、state、INDEX 更新仕様などの詳細は専用の下位対象へ進みます。

## Read this when
- realization のリファクタリング機能の構成や実行入口を確認するとき
- `cmoc realization refactor fork` の実行フロー、run 状態、対象ファイル処理、完了・中断・エラー処理を調査するとき
- リファクタリング結果の検証、未解決 finding の追跡、commit、report 保存の流れを確認するとき

## Do not read this when
- 個別の realization file review や change summary 用 agent prompt の詳細だけを確認するとき
- run 作成、commit、rollback、process tracking、report rendering など共通 lifecycle の実装だけを確認するとき
- INDEX 更新の一般規則や realization refactor の永続 state 契約だけを確認するとき

## hash
- cd5cf75e27fff6b667452ebaecfd0046ae8de238da33a775529a3a1a9eac9c27
