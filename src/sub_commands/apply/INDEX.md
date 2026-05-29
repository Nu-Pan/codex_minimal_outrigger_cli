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
- 現在の session に紐づく未 join の apply run を破棄し、running 中なら子プロセスごと停止したうえで、apply worktree と apply branch を強制削除して `apply.state` を `ready` に戻します。
- 破棄前後の状態表示と warning 出力を行い、次回の apply 実行に支障がないよう session state の補助情報を初期化します。

## Read this when

- `cmoc apply abandon` の実装・修正・レビュー・テストを行いたいとき。
- 未 join の apply run を破棄する前提条件や、`apply.state` の検証条件を確認したいとき。
- running 中の apply を停止する挙動や、apply worktree / apply branch の cleanup 方針を確認したいとき。
- 破棄結果として標準出力に何を出し、warning をどう扱うかを確認したいとき。

## Do not read this when

- `cmoc apply fork` の調査・修正ループや要修正点一覧だけを確認したいときは、このモジュールではなく `fork.py` を読むべきです。
- `cmoc apply join` や `cmoc session abandon` など、別サブコマンドの終了・統合・破棄手順だけを確認したいときは、このモジュールではなく該当モジュールを読むべきです。
- `cmoc apply abandon` の仕様断片や利用手順だけを確認したいときは、`oracles/app_specs/sub_commands/apply_abandon.md` を直接読むべきです。

## hash

- 2fbcf4ed4920da13bdf2307bf69d4ac60a26b15d4d47034249758e079a3922f9

# `fork.py`

## Summary

- `cmoc apply fork` の本体実装で、session state の前提確認から apply branch と worktree の作成、調査・修正ループ、レポート生成までを担当します。
- oracle と実装の差分を調べるための Structured Output スキーマ、Codex CLI への prompt 生成、要修正点の整理、`INDEX.md` の保守をまとめています。
- 失敗時の `apply.state` 更新、編集禁止パスの検査、apply report と error report の検証・出力もここに含まれます。

## Read this when

- cmoc apply fork の実装・修正・レビュー・テストで、処理全体の流れを追いたいとき。
- session state の前提条件、apply branch / worktree の作成、ロック制御、調査・修正ループを確認したいとき。
- 不整合調査の Structured Output 検証、要修正点の整理、`INDEX.md` 保守、レポート出力の経路を確認したいとき。

## Do not read this when

- cmoc apply fork の利用手順、引数、終了条件だけを確認したいときは、`oracles/app_specs/sub_commands/apply_fork.md` を読むべきです。
- cmoc apply join や cmoc apply abandon、cmoc session 系の処理だけを確認したいときは、このファイルではなく該当モジュールを読むべきです。
- `INDEX.md` の生成・更新ルールや、`branch_model`・`error_handling`・`codex_call` などの共通仕様だけを確認したいときは、別の仕様文書を読むべきです。

## hash

- dc1d0484ffeb812009fffe5497b6051a55e2fd5ef7fe59b9b8410e670937501f

# `join.py`

## Summary

- `src/sub_commands/apply/join.py` は `cmoc apply join` の本体処理を実装するモジュールです。
- session state の検証、apply branch から session branch への merge、想定外差分の判定と強制解決、`INDEX.md` conflict の自動解消を扱います。
- merge 後の `apply.state` 更新と、条件を満たす場合の apply branch / worktree の cleanup までをまとめています。

## Read this when

- `cmoc apply join` の実装・修正・レビュー・テストで、処理順や責務境界を確認したいとき。
- 完了済みの apply branch を session branch に取り込む前提条件や、`apply.state` の検証条件を確認したいとき。
- 想定外の差分の検出方法と、`--force-resolve` による revert 分岐を追いたいとき。
- `git merge --no-ff` の後に `apply.state` を `ready` に戻す処理や、apply branch / worktree の削除条件を確認したいとき。

## Do not read this when

- `cmoc apply fork` の調査・修正ループや要修正点の収集だけを確認したいときは、このファイルではなく `fork.py` を読むべきです。
- `cmoc apply abandon` の破棄処理や cleanup 方針だけを確認したいときは、このファイルではなく `abandon.py` を読むべきです。
- `cmoc session join` や `cmoc session abandon` など、session 側の開始・終了・統合だけを確認したいときは、このファイルではなく該当モジュールを読むべきです。
- `cmoc apply join` の仕様断片や利用手順だけを確認したいときは、`oracles/app_specs/sub_commands/apply_join.md` を直接読むべきです。

## hash

- 86a816ef54dd6c6c170face1f591b99484d7a35eb45c15007646b67cf1062370
