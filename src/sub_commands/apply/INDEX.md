# `__init__.py`

## Summary

- `src/sub_commands/apply/__init__.py` は `cmoc apply` 系サブコマンドのパッケージ宣言だけを担う最小モジュールです。
- 公開 API、定数、実行ロジック、再エクスポートは持ちません。

## Read this when

- `src/sub_commands/apply` が Python パッケージとして宣言されていることを確認したいとき。
- `cmoc apply` 系サブコマンドの入口となるパッケージ構造を把握したいとき。

## Do not read this when

- 個別の `cmoc apply fork/join/abandon` の実行フローや状態遷移を確認したいときは、このファイルではなく各実装モジュールを読むべきです。
- `cmoc apply` の仕様断片や利用手順だけを確認したいときは、`oracles/docs/app_specs/sub_commands/` 側を読むべきです。

## hash

- 5646cb02b7ca8e507d8725e2d5f87e9580881d66ce1a67505595830d53c239d6

# `abandon.py`

## Summary

- `src/sub_commands/apply/abandon.py` は `cmoc apply abandon` の本体処理を実装するモジュールです。
- 現在の session に紐づく未 join の apply run を検証し、必要に応じて実行中の apply プロセスを停止したうえで、apply branch と worktree を強制削除して `apply.state` を `ready` に戻します。
- 現在の branch が apply branch の場合は cleanup 基点を session branch へ移し、破棄結果と warning を標準出力へ出力し、次回の apply に向けて session state の補助情報を初期化します。

## Read this when

- `cmoc apply abandon` の役割と責務を素早く把握したいとき。
- `session.state` / `apply.state` の前提条件、未 join の apply run の破棄条件、実行中プロセス停止の流れを確認したいとき。
- apply branch / worktree の強制削除、現在 branch から cleanup 基点を session branch へ移す処理を確認したいとき。
- 破棄結果、warning の出力、`apply.state` を `ready` に戻して補助情報を初期化する後始末を確認したいとき。
- `cmoc apply abandon` の実装・修正・レビュー・テストを始める前に、処理順と状態遷移を確認したいとき。

## Do not read this when

- `cmoc apply fork` の調査・修正ループや report 生成だけを追いたいとき。
- `cmoc apply join` の取り込み条件や merge 後 cleanup だけを確認したいとき。
- `cmoc session abandon` など、session 側の破棄処理だけを確認したいとき。
- `cmoc apply abandon` の利用手順や正本仕様だけを確認したいときは、実装ではなく `oracles/docs/app_specs/sub_commands/apply_abandon.md` を読むべきとき。

## hash

- bec22b07eb9dbd4f65bd37ab36391efed571f1ee57ee2d0b1f7ed706fb6b9a18

# `fork.py`

## Summary

- `src/sub_commands/apply/fork.py` は `cmoc apply fork` の本体実装で、session branch 上で apply run を開始し、不整合調査から修正反復、報告書作成までを担当するモジュールです。
- state 検証、apply worktree 作成、scope に応じた調査対象の絞り込み、Codex CLI への file 起点調査、修正適用、INDEX 保守、終了コード分岐をまとめています。

## Read this when

- `cmoc apply fork` の処理順や責務を追いたいとき。
- session/apply state の検証、apply worktree 作成、排他制御、`.cmoc` の ignore 保証を確認したいとき。
- 要修正点の Structured Output、調査・修正ループ、レポート出力、`INDEX.md` の自動メンテナンスを確認したいとき。
- 途中失敗時の error report と、収束・未収束の終了コードを確認したいとき。

## Do not read this when

- `cmoc apply` の利用手順や正本仕様だけを確認したいとき。
- `cmoc apply join` や `cmoc apply abandon` の終了・破棄処理だけを確認したいとき。
- `src/sub_commands/apply` 配下のパッケージ宣言や入口構造だけを確認したいとき。
- `apply_fork` とは無関係な `session` や `review` の実装を確認したいとき。

## hash

- 32d6a8303e10a035e0d204854cb69837fcb4a290225661f459c13ac7655a8305

# `join.py`

## Summary

- `/home/happy/codex_minimal_outrigger_cli_stage1/.cmoc/worktrees/apply/2026-05-31_08-51_06_000000872/2026-05-31_08-52_22_000000612/src/sub_commands/apply/join.py` は `cmoc apply join` の本体実装です。
- 完了済みの apply branch を session branch へ `git merge --no-ff` で取り込み、state 検証、想定外差分の判定、`INDEX.md` conflict の扱いまでまとめて実行します。
- merge 後は session state を `ready` に戻し、最後に joined した snapshot の記録、apply branch / worktree の安全な削除、warning の出力を行います。

## Read this when

- `cmoc apply join` の merge 手順、前提 state、現在 branch の検証を確認したいとき。
- 想定外差分の検出、`--force-resolve` による revert、`INDEX.md` conflict の自動解消条件を追いたいとき。
- join 後の session state 更新、apply branch / worktree の cleanup 条件、警告出力の流れを確認したいとき。

## Do not read this when

- `/home/happy/codex_minimal_outrigger_cli_stage1/.cmoc/worktrees/apply/2026-05-31_08-51_06_000000872/2026-05-31_08-52_22_000000612/src/sub_commands/apply/join.py` ではなく、`src/sub_commands/apply/__init__.py` だけで十分なとき。
- `cmoc apply fork` や `cmoc apply abandon` の実装だけを追いたいとき。
- 実装ではなく、`oracles/docs/app_specs/sub_commands/` 側の `cmoc apply join` 仕様断片だけを確認したいとき。

## hash

- f1f4573b646b46e0ea797e1f435ae2fd61d83a97c86c2c1a204cf4291c2fbf93
