# `__init__.py`

## Summary

- `src/sub_commands/apply/__init__.py` は `cmoc apply` 系サブコマンドのパッケージ宣言だけを担う最小モジュールです。
- 公開 API、定数、実行ロジック、再エクスポートは持ちません。

## Read this when

- `src/sub_commands/apply` が Python パッケージとして宣言されていることを確認したいとき。
- `cmoc apply` 系サブコマンドの入口となるパッケージ構造を把握したいとき。

## Do not read this when

- 個別の `cmoc apply fork/join/abandon` の実行フローや状態遷移を確認したいときは、このファイルではなく各実装モジュールを読むべきです。
- `cmoc apply` の仕様断片や利用手順だけを確認したいときは、`oracles/app_specs/sub_commands/` 側を読むべきです。

## hash

- 5646cb02b7ca8e507d8725e2d5f87e9580881d66ce1a67505595830d53c239d6

# `abandon.py`

## Summary

- `src/sub_commands/apply/abandon.py` は `cmoc apply abandon` の本体処理を実装するモジュールです。
- 現在の session に紐づく未 join の apply run を破棄し、`running` なら子プロセスを停止したうえで、apply branch と worktree を強制削除して `apply.state` を `ready` に戻します。
- 破棄前後の状態表示と warning 出力を行い、次回の apply 実行に支障が出ないよう session state の補助情報を初期化します。

## Read this when

- `cmoc apply abandon` の実装・修正・レビュー・テストを行いたいとき。
- 未 join の apply run を破棄する前提条件や、`session.state` / `apply.state` の検証条件を確認したいとき。
- `running` 中の apply を停止する挙動や、apply branch / worktree の cleanup 方針を確認したいとき。
- 破棄結果として標準出力に何を出し、warning をどう扱うかを確認したいとき。

## Do not read this when

- `cmoc apply fork` の調査・修正ループや要修正点の整理だけを確認したいとき。
- `cmoc apply join` や `cmoc session abandon` など、別サブコマンドの終了・統合・破棄手順だけを確認したいとき。
- `cmoc apply abandon` の仕様断片や利用手順だけを確認したいときは、`oracles/app_specs/sub_commands/apply_abandon.md` を直接読むべきです。
- `src/sub_commands/apply` パッケージ全体の役割だけを確認したいときは、`src/sub_commands/apply/INDEX.md` を読むべきです。

## hash

- cd85d274a1d46f32aa63514c5dd6bf035e94a4b75060c91f70cb6bf286e8ecd1

# `fork.py`

## Summary

- `src/sub_commands/apply/fork.py` は `cmoc apply fork` の本体実装で、session branch から専用の apply branch と worktree を作成し、調査・修正ループを回してレポートまで生成します。
- 事前条件の検証、スコープ判定、対象ファイルの列挙、要修正点の Structured Output 検証と整理、Codex CLI 呼び出し、コミット処理までをまとめています。
- apply 実行中の禁止パス検査、INDEX.md メンテナンス、成功時レポートと失敗時 error report の生成・保存もこのモジュールの責務です。

## Read this when

- `cmoc apply fork` の開始から終了までの処理順と、どの段階で state を更新するかを追いたいとき。
- session/apply state の検証、apply branch / worktree の作成、調査対象ファイルの選定、要修正点の改善・適用ループを確認したいとき。
- Structured Output のスキーマ検証、変更要約、レポート生成、例外時の復旧処理を実装・修正・レビューしたいとき。

## Do not read this when

- `cmoc apply join` や `cmoc apply abandon` だけを確認したいときは、このファイルではなく各実装モジュールを読むべきです。
- `cmoc apply fork` の利用手順や仕様断片だけを確認したいときは、`oracles/app_specs/sub_commands/apply_fork.md` を直接読むべきです。
- `src/sub_commands/apply` パッケージ全体の入口だけを確認したいときは、上位の `INDEX.md` を読むべきです。
- INDEX.md の生成ルールだけを確認したいときは、`oracles/.../indexing.md` 側を読むべきです。

## hash

- 361d081c50b58718f5b27b5d0a9f6c1cf92ae1b3a834d03653cedfa1b26d5df5
<!-- cmoc-index-kind: file -->

# `join.py`

## Summary

- `src/sub_commands/apply/join.py` は `cmoc apply join` の本体処理を実装するモジュールです。
- session/apply state の検証を行い、apply branch を session branch へ `git merge --no-ff` します。
- 想定外の差分を検出して通常は停止し、`--force-resolve` 指定時は差分を revert してから merge を試みます。
- merge 時の `INDEX.md` conflict は自動解消対象として扱い、merge 後は `apply.state` を ready に戻して、条件を満たす場合のみ apply branch と worktree を cleanup します。

## Read this when

- `src/sub_commands/apply/join.py` の実装・修正・レビュー・テストで、処理順や責務境界を確認したいとき。
- 完了済みの apply branch を session branch に取り込む前提条件や、`apply.state = completed` / `error` の扱いを確認したいとき。
- 想定外の差分の検出、`--force-resolve` による差分の戻し方、`INDEX.md` conflict の自動解消、cleanup 条件を追いたいとき。
- merge 後に `apply.state` を ready に戻し、条件を満たす場合だけ apply branch と worktree を削除する流れを確認したいとき。

## Do not read this when

- `cmoc apply fork` の調査・修正ループや要修正点の整理だけを確認したいとき。
- `cmoc apply abandon` や `cmoc session join` / `cmoc session abandon` など、別サブコマンドの終了・破棄・統合手順だけを確認したいとき。
- `INDEX.md` の生成ルールや `oracles` 全体のルーティング方針だけを確認したいとき。
- `cmoc apply join` の実装内容を既に把握していて、ソースコードだけを直接追えば足りるとき。

## hash

- 2682c1d21a99af9226ef78d2def4338951573c7c4499b295927a9536ed210c09
