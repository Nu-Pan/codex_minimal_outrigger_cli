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
- realization のリファクタリング処理を扱うパッケージ。リファクタリング関連の CLI 実行と処理構成を確認するための入口となる。
- 単一ファイルの調査・修正、変更概要生成、一般的な run lifecycle の詳細は、それぞれ専用の下位実装を直接確認する。

## Read this when
- realization のリファクタリング処理の構成や入口を確認するとき
- realization refactor fork の実行フロー、run 初期化、対象ファイル処理、state 同期、commit、unresolved 管理、完了判定を確認するとき
- 割り込み・エラー時の cleanup、Codex child の停止、joinable 公開、fork report 生成を調査するとき
- refactor state、realization 差分、agent commit、rename、INDEX 更新後の整合性検証を確認するとき

## Do not read this when
- realization のリファクタリング以外の処理を確認するとき
- 単一ファイルの調査・修正 prompt や Structured Output 契約だけを確認するとき
- 正常完了時の変更概要生成だけを確認するとき
- 一般的な editing run の join・abandon・state 遷移だけを確認するとき

## hash
- 40d944c7b3fe42c3676a2af6e3b3efb15bad5494da89c4146deed57d0df570c8
