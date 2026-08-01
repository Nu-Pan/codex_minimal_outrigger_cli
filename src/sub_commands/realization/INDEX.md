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
- realization の apply 処理に関する workload を扱うディレクトリ。apply workload の実装を確認する入口であり、fork サブコマンドの実行制御を含む。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- `cmoc realization apply fork` の実行フロー、成功時の joinable 化、fork report、差分検査、rollback、cleanup の挙動を確認するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- launch parameter の構築詳細だけを確認したいときは、`acp.builder.realization.apply.fork.launch_exec` を直接読む。
- 編集 run の共通ライフサイクル API や fork report の共通フォーマットだけを確認したいときは、対応する共通モジュールや oracle 文書を直接読む。

## hash
- e2c0db34d7b078e689b1736295ce767c5ba9cca7511bc999910f271298cbdc8c

# `refactor`

## Summary
- realization のリファクタリング処理を扱うパッケージ。fork の CLI 実行ライフサイクルと、関連するリファクタリング処理への入口を提供する。

## Read this when
- realization refactor の処理構成や fork の実行ライフサイクルを確認するとき
- run 初期化、対象 file 選択、agent call、差分検証、commit、state・report 管理を調査するとき
- 中断・例外時の停止、rollback、完了判定を調査するとき

## Do not read this when
- realization refactor の state 同期や target 選択の共通実装を調査するとき
- agent 入力 parameter や change summary の構築を調査するとき
- 一般的な run lifecycle や report 表示の共通仕様を確認するとき

## hash
- 581f980f2e2f64e6d839cc68b4ad2eab8a849e056194ec36014da63b4ecbedb8
