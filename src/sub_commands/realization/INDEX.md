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
- realization の apply 処理に関する workload を扱うモジュール。apply workload の実装を確認する入口となる。
- `cmoc realization apply fork` サブコマンドの実行処理を担う。差分の始点特定、oracle diff 構築、realization apply agent の実行、変更検査・commit、run の joinable 更新、fork report 保存までを管理する。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- realization apply fork の実行フロー、run の joinable/error 遷移、agent 差分の検査や commit、fork report の生成を変更・調査するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- realization apply の prompt 構築だけを変更・調査するときは、launch parameter builder を直接読む。run の共通ライフサイクルや状態管理だけを変更・調査するときは、commons の runtime lifecycle 実装を直接読む。

## hash
- 433885d3f3ddd4ccb2b128466bfba4252746073331fdee9ef6162bb6684dd05a

# `refactor`

## Summary
- realization のリファクタリング処理をまとめるパッケージ。対象選択から file 単位の調査・修正、差分検証、状態更新、commit、未解決事項管理、完了判定、report 保存までの実行入口を提供する。
- 処理全体の lifecycle や fork report の挙動を確認する場合は fork 実装が主な入口となる。

## Read this when
- realization refactor の実行フロー、処理単位の commit、中断・例外時の cleanup、unresolved finding、完了条件を確認または変更するとき。
- refactor state、INDEX 更新、Codex child process の停止、run state の joinable/error 遷移を調査するとき。

## Do not read this when
- realization refactor の agent call 内部仕様や finding 生成形式だけを確認する場合。
- change summary の Structured Output や差分要約だけを確認する場合。
- 一般的な run lifecycle、state 管理、report 出力の共通処理だけを確認する場合。

## hash
- 558427076488df3aaea742bda88322d60ae7fa693502e3a54c6beaaf8a71c4aa
