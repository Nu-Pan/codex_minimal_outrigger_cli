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
- realization の apply 処理を構成するモジュール群。apply workload の入口と、`cmoc realization apply fork` サブコマンドの実行処理を扱う。

## Read this when
- realization apply workload の内容を調査・変更するとき。
- `cmoc realization apply fork` の挙動、run lifecycle、Codex agent 実行、差分検査、commit、rollback、fork report 生成を扱うとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- realization apply の join や abandon の処理だけを扱うとき。
- 共通 run lifecycle の詳細や fork 起動パラメータの構築を直接確認するとき。

## hash
- 03606c2b385311047e1739eb9635cca715ba3102d05729e470faa5de2578c15f

# `refactor`

## Summary
- realization のリファクタリング処理を扱うパッケージで、関連する fork 実行フローへの入口となる。
- 対象選択から Codex による file 単位の調査・修正、state 更新、commit、完了判定、エラー処理、report 生成までの realization refactor fork の実行を管理する。

## Read this when
- realization のリファクタリング処理の構成や入口を確認するとき
- cmoc realization refactor fork の実行フロー、進捗管理、割り込み・エラー処理、差分検証、unresolved finding 管理を調査・変更するとき

## Do not read this when
- refactor state の保存・同期や target 選択そのものを確認するときは commons.runtime_refactor を読む
- 単一 realization file の調査・修正用 agent parameter を確認するときは file_review_and_fix を読む
- fork report の共通出力形式だけを確認するときは commons.runtime_run_report を読む

## hash
- 59911e629bd635bba903127350bda7894e576dbc4952e9e50ddc41f930d05c7b
