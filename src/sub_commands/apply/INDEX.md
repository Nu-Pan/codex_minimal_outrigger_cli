# `__init__.py`

## Summary

- `<work-root>/src/sub_commands/apply/__init__.py` は `cmoc apply` 系サブコマンドのパッケージ宣言だけを担う最小モジュールです。
- 公開 API、定数、実行ロジック、再エクスポートは持ちません。

## Read this when

- `<work-root>/src/sub_commands/apply` が Python パッケージとして宣言されていることを確認したいとき。
- `cmoc apply` 系サブコマンドの入口となるパッケージ構造を把握したいとき。

## Do not read this when

- `<work-root>/src/sub_commands/apply` 配下の個別実装ファイルや実行フローを確認したいとき。
- `cmoc apply fork`、`cmoc apply join`、`cmoc apply abandon` の各処理本体を追いたいとき。
- `<work-root>/src/sub_commands/apply` のパッケージ宣言ではなく、利用手順や仕様断片を確認したいとき。

## hash

- 5646cb02b7ca8e507d8725e2d5f87e9580881d66ce1a67505595830d53c239d6

# `abandon.py`

## Summary

- `<work-root>/src/sub_commands/apply/abandon.py` は `cmoc apply abandon` の本体処理を実装するモジュールです。
- 現在の session に紐づく未 join の apply run を検証し、必要に応じて実行中の apply プロセスを停止したうえで、apply branch と worktree を強制削除して `apply.state` を `ready` に戻します。
- 現在の branch が apply branch の場合は cleanup 基点を session branch へ移し、破棄結果と warning を標準出力へ出力し、次回の apply に向けて session state の補助情報を初期化します。

## Read this when

- `cmoc apply abandon` の役割と責務を確認したいとき。
- `session.state` と `apply.state` の前提条件、未 join の apply run の破棄条件、実行中プロセス停止の流れを確認したいとき。
- apply branch や apply worktree の強制削除、現在 branch が apply branch の場合に cleanup 基点を session branch へ移す処理を確認したいとき。
- 破棄結果や warning の出力、`apply.state` を `ready` に戻して補助情報を初期化する後始末を確認したいとき。
- `cmoc apply abandon` の実装・修正・レビュー・テストを始める前に、処理順と状態遷移を確認したいとき。

## Do not read this when

- `cmoc apply fork` の調査・修正・レビューだけをしたいとき。
- `cmoc apply join` の取り込み条件や merge 後の cleanup だけを確認したいとき。
- `cmoc session abandon` や `cmoc session join` など、session 側の終了・統合・破棄フローだけを確認したいとき。
- `cmoc apply abandon` の利用手順や正本仕様だけを確認したいときは、`<work-root>/oracles/docs/app_specs/sub_commands/apply_abandon.md` を読むべきです。

## hash

- 5ff6fbf3380dbb4d969a6a4ce0643de7901071b75964644787a81466e78e9212

# `fork.py`

## Summary

- `<cmoc-root>/src/sub_commands/apply/fork.py` は `cmoc apply fork` の本体実装モジュールで、apply 実行の全体制御を担います。
- session/apply の状態検証、apply worktree 作成、`.cmoc` の非追跡保証、調査・修正ループ、レポート出力までをまとめて扱います。
- 不整合調査用 Structured Output schema、要修正点の整理、コミット確定、成功時と失敗時の報告分岐もこのファイルの役割です。

## Read this when

- `<cmoc-root>/src/sub_commands/apply/fork.py` の実装・修正・レビュー・テストを行いたいとき。
- `session.state` / `apply.state` の前提条件や、`--scope` と反復回数オプションの扱いを確認したいとき。
- apply worktree の作成、`.cmoc` の非追跡保証、不整合調査から修正適用までの流れを追いたいとき。
- 要修正点リストの Structured Output schema、改善ループ、エラー時のフォールバックを確認したいとき。

## Do not read this when

- `cmoc apply fork` の利用手順や完了条件だけを確認したいとき。
- `<work-root>/src/sub_commands/apply` 配下の入口構造だけを確認したく、親階層の `INDEX.md` で足りるとき。
- `cmoc apply join` や `cmoc apply abandon` の開始・統合・破棄フローだけを確認したいとき。
- `apply` の実行制御ではなく、`oracles` 側の仕様断片や利用手順だけを確認したいとき。

## hash

- 5a9105294fa4c4b263d1225a3700b58a2abc422ae4562e1c7218228437d1b7c9

# `join.py`

## Summary

- `<cmoc-root>/src/sub_commands/apply/join.py` は `cmoc apply join` の本体実装で、完了済みの apply branch を session branch に取り込む処理を担います。
- session/apply state の検証、未コミット差分の確認、想定外差分の扱い、`--force-resolve` による強制解消をまとめています。
- マージ時の `INDEX.md` conflict 自動解消、merge 後の state 更新、apply branch / worktree の後始末と warning 出力までを扱います。

## Read this when

- `<cmoc-root>/src/sub_commands/apply/join.py` の実装・修正・レビュー・テストを行うとき。
- 完了済みの apply branch を session branch へ取り込む手順と、その前提条件を確認したいとき。
- `apply.state` が `completed` または `error` のときの扱い、想定外差分の検出と `--force-resolve` の分岐を追いたいとき。
- `INDEX.md` conflict の自動解消条件や、join 後に apply branch / worktree を削除してよい条件を確認したいとき。

## Do not read this when

- `cmoc apply fork` や `cmoc apply abandon` の開始・破棄フローだけを確認したいとき。
- `cmoc session` 系サブコマンドの開始・統合・破棄だけを確認したいとき。
- `cmoc apply join` の利用手順や正本仕様だけを確認したいときは、`<work-root>/oracles/docs/app_specs/sub_commands/apply_join.md` を読むべきとき。
- `<work-root>/src/sub_commands/apply` 配下の入口構造だけを確認したく、`join.py` の処理本体が不要なとき。

## hash

- fc12fe60a37eb92f4d9fa3feb0af083cb45d13ff8eff61fb24d24cd8e49e03b6
