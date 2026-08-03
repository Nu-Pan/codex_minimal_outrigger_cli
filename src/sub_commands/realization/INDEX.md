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
- realization のリファクタリング処理を扱うパッケージ。関連するリファクタリング処理への入口となる。
- refactor fork の実行フローとして、run 初期化、対象 realization file の選択、Codex による調査・修正、差分と所見の検証、state 更新、commit、unresolved 管理、完了判定、cleanup、report 保存を一貫して処理する。
- refactor fork のライフサイクル、run worktree、process tracking、INDEX 更新、Git commit の整合性を確認する際の主要な実装入口であり、個別の所見生成や report の詳細は呼び出される実装へ進む。

## Read this when
- realization のリファクタリング処理の構成や CLI 挙動を確認・変更するとき
- 対象選択から完了までの refactor fork の処理フローを調査するとき
- 差分検証、agent commit、rename、refactor state、unresolved finding の整合性を確認するとき
- 正常完了・中断・例外時の run state、rollback、child process 停止、report 保存を調査するとき

## Do not read this when
- 個別の refactor agent prompt や change summary の Structured Output 定義だけを確認したいとき
- 一般的な editing run の仕様、run isolation、INDEX 更新規則だけを確認したいとき
- fork report の Markdown 表現や共通 report 書き込み処理だけを確認したいとき

## hash
- b8bf9e4967fe97c3caf02bddbdb4746baca8396548d5b5f8caab74171f04627b
