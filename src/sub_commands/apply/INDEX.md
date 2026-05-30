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
- 未 join の apply run を破棄する前提条件や、`session.state` / `apply.state` の検証条件を確認したいとき。
- running 中の apply を停止する挙動や、apply worktree / apply branch の cleanup 方針を確認したいとき。
- 破棄結果として標準出力に何を出し、warning をどう扱うかを確認したいとき。

## Do not read this when

- `cmoc apply fork` の修正点一覧、調査・修正ループ、レポート生成を確認したいときは、このモジュールではなく `fork.py` を読むべきです。
- `cmoc apply join` や `cmoc session abandon` など、別サブコマンドの終了・統合・破棄手順だけを確認したいときは、このモジュールではなく該当モジュールを読むべきです。
- `cmoc apply abandon` の仕様断片や利用手順だけを確認したいときは、`oracles/app_specs/sub_commands/apply_abandon.md` を直接読むべきです。
- `src/sub_commands/apply` パッケージ全体の役割だけを確認したいときは、`src/sub_commands/apply/INDEX.md` を読むべきです。

## hash

- b45f20e131c92c70266770d4883e18ad802ecabecfc9630c56c0dc3a582b6566

# `fork.py`

## Summary

- `src/sub_commands/apply/fork.py` は `cmoc apply fork` の本体実装で、session branch から専用 apply branch / worktree を作成し、調査・修正ループを完遂するまでの全体制御を担います。
- session state の事前検証、apply 開始の直列化、`running` / `completed` / `error` への状態更新、再実行回数や scope オプションの検証を扱います。
- 要修正点の抽出・改善・適用、禁止パス検査、`INDEX.md` 保守、apply report と変更要約の生成・検証まで含む運用中枢です。

## Read this when

- `cmoc apply fork` の実装全体、処理順、終了条件を確認したいとき。
- session state の検証、apply branch / worktree の生成、`--repeat-investigate-and-fix` / `--repeat-improove-fixing-list` / `--scope` の扱いを確認したいとき。
- 要修正点の Structured Output schema、Codex CLI への調査・修正依頼、report 保存や変更要約の流れを追いたいとき。

## Do not read this when

- `cmoc apply join` や `cmoc apply abandon` の処理だけを確認したいとき。
- `cmoc session fork/join/abandon` など、apply 以外のサブコマンド仕様だけを確認したいとき。
- `oracles` 側の個別仕様断片や `INDEX.md` の生成ルールだけを確認したいとき。

## hash

- 417bf2a9d3ff0b0266a80b939e493d7b6eb1fcbd4361b6bccff917958b5e0fa9
<!-- cmoc-index-kind: file -->

# `join.py`

## Summary

- `src/sub_commands/apply/join.py` は `cmoc apply join` の本体処理を実装するモジュールです。
- session/apply state の検証を行い、apply branch を session branch へ merge します。
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

- f0467aa037cc581f4e619997aae152d40374f7fc01ef3570d864f1a354991b9b
<!-- cmoc-index-kind: file -->
