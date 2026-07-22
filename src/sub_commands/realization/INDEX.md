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
- realization の apply workload を扱うディレクトリ。apply workload の入口と、`cmoc realization apply fork` の実行フローを確認するために読む。

## Read this when
- realization の apply workload を調査・変更するとき。
- `cmoc realization apply fork` の処理フロー、agent 実行、差分検査、commit、run 状態遷移、fork report を確認するとき。

## Do not read this when
- apply fork の launch parameter 構築だけを調査・変更するとき。
- run lifecycle の共通処理や report 形式だけを確認するとき。
- realization apply fork 以外のサブコマンドの実行フローを調査するとき。

## hash
- 3d86a47945ffd9b4cd81539a13dabff57ad1d09ca9730bbc46edef03f283b31c

# `refactor`

## Summary
- realization のリファクタリング処理を扱うパッケージ。リファクタリング関連 CLI の入口と、fork の実行ライフサイクルを提供する。
- fork モジュールでは、refactor run の初期化から realization file 単位の調査・修正、state 同期、commit、完了判定、変更要約、fork report 保存までを一連の処理として実装する。

## Read this when
- realization のリファクタリング処理の構成や実行フローを確認・変更するとき。
- refactor fork の unresolved finding 管理、state 更新、report 生成、割り込み・例外時の処理を確認するとき。

## Do not read this when
- realization refactor の state 操作だけを変更・調査する場合。
- 一般的な run lifecycle や report 共通処理だけを確認する場合。
- file 単位の agent parameter や change summary parameter の定義だけを確認する場合。

## hash
- 526fa2f23cd4b2e4506c55fd5ac012cf911f732ef4da68276a54376f9e47002e
