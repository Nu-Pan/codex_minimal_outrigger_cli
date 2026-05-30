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

- 8bfed7fb89ac85ce255d8a910b02ca45356bfacae3c644da7acbedf040255c58

# `fork.py`

## Summary

- `src/sub_commands/apply/fork.py` は `cmoc apply fork` の本体実装で、session state の検証から apply 実行の開始までを担います。
- apply branch と専用 worktree の作成、要修正点の調査・適用ループ、`INDEX.md` の保守をまとめて扱います。
- 完了レポートとエラーレポートの生成、Structured Output の検証、禁止パスの確認もこのファイルに含まれます。

## Read this when

- `cmoc apply fork` の実装全体を追いたいとき。
- session state の検証、apply branch と専用 worktree の作成、調査・修正ループの流れを確認したいとき。
- `INDEX.md` の保守、要修正点の Structured Output 検証、レポート生成やエラー報告の処理を確認したいとき。

## Do not read this when

- `cmoc apply fork` の引数、前提条件、終了条件だけを確認したいとき。
- `cmoc apply join` や `cmoc apply abandon` の処理を確認したいとき。
- `INDEX.md` の生成ルールや `oracles` 側の仕様断片だけを確認したいとき。

## hash

- 3d2a1aac79247266c6aec206d6987d0040f143056bfd4846f3c59b59e815ed84

# `join.py`

## Summary

- `src/sub_commands/apply/join.py` は `cmoc apply join` の本体処理を実装するモジュールです。
- session state の検証を行い、apply branch を session branch へ merge します。
- 想定外の差分を検出して通常は停止し、`--force-resolve` 指定時は差分を revert してから merge を試みます。
- merge 時の `INDEX.md` conflict は自動解消対象として扱い、必要なら merge commit まで進めます。
- merge 後は `apply.state` を ready に戻し、条件を満たす場合のみ apply branch と worktree を cleanup します。

## Read this when

- `cmoc apply join` の実装・修正・レビュー・テストで、処理順や責務境界を確認したいとき。
- 完了済みの apply branch を session branch に取り込む前提条件や、`apply.state = completed` / `error` の扱いを確認したいとき。
- 想定外の差分の検出、`--force-resolve` による差分の戻し方、`INDEX.md` conflict の自動解消、cleanup 条件を追いたいとき。

## Do not read this when

- `cmoc apply fork` の調査・修正ループや要修正点の整理だけを確認したいとき。
- `cmoc apply abandon` や `cmoc session join` / `cmoc session abandon` など、別サブコマンドの終了・破棄・統合だけを確認したいとき。
- `INDEX.md` の生成ルールや `oracles` 全体のルーティング方針だけを確認したいとき。

## hash

- 35bf439bc0764fa805454e86adf997319140afaaa57b7b92405282b450612f30
