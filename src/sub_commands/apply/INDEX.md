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
- 現在の session に紐づく未 join の apply run を破棄し、必要に応じて実行中の apply プロセスを停止したうえで、apply branch と worktree を強制削除して `apply.state` を `ready` に戻します。
- 現在の branch から cleanup 基点を session branch へ移し、破棄結果と warning を標準出力へ出力し、次回の apply に向けて session state の補助情報を初期化します。

## Read this when

- `cmoc apply abandon` の役割と責務を素早く把握したいとき。
- `cmoc apply abandon` の実装・修正・レビュー・テストを始める前に、前提条件、状態検証、cleanup の流れを確認したいとき。
- 未 join の apply run の破棄条件、`session.state` / `apply.state` の検証、実行中プロセスの停止、apply branch / worktree の削除方針を追いたいとき。
- 破棄結果、warning の扱い、`apply.state` を `ready` に戻す後始末を確認したいとき。

## Do not read this when

- `cmoc apply fork` の要修正点調査や修正反映の仕様を確認したいとき。
- `cmoc apply join` や `cmoc session abandon` など、別サブコマンドの終了・統合・破棄処理だけを確認したいとき。
- `cmoc apply abandon` の利用手順や正本仕様だけを確認したいときは、実装コードではなく `oracles/docs/app_specs/sub_commands/apply_abandon.md` を読むべきとき。
- `src/sub_commands/apply` パッケージ全体の入口構造だけを確認したいとき。

## hash

- 62fe450290efc5bbee42fa14bd25d1ca4a223a9614b17e9f03d63de8fe73faad

# `fork.py`

## Summary

- `src/sub_commands/apply/fork.py` は `cmoc apply fork` の本体で、session branch 上に専用の apply branch と worktree を作成し、要修正点の調査・適用・レポート生成までをまとめて担当する。
- 起動前の state 検証、`--repeat-investigate-and-fix` / `--repeat-improove-fixing-list` / `--scope` の検証、`apply.state` の遷移、排他ロックと worktree 作成リトライを扱う。
- Structured Output による不整合調査、修正反映、commit、編集禁止領域の検査、YAML Front Matter 付き report 出力と変更要約生成までを含む。

## Read this when

- `cmoc apply fork` の処理順と責務の境界を確認したいとき。
- `session.state` / `apply.state` の検証条件、apply branch と worktree の作成条件、scope ごとの調査対象選定を確認したいとき。
- Structured Output による不整合調査、要修正点の整理、修正反映、commit、report 生成の流れを追いたいとき。
- 編集禁止領域の検査や report の検証条件を確認したいとき。

## Do not read this when

- `cmoc apply join` や `cmoc apply abandon` の実装・終了処理だけを確認したいとき。
- `cmoc apply fork` の利用手順や正本仕様だけを確認したいとき。
- `src/sub_commands/apply` パッケージ全体の入口だけを確認したいとき。
- `INDEX.md` の生成ルールだけを確認したいとき。

## hash

- b578e82041313343918f96291b0d2b90d95e8699ec8eedc6cdbd44218be0f6f0

# `join.py`

## Summary

- `src/sub_commands/apply/join.py` は `cmoc apply join` の本体で、完了済みの apply branch を session branch に取り込む処理を実装するモジュールです。
- session/apply state の検証、現在ブランチと local ブランチの存在確認、未コミット差分の検出、想定外差分の `--force-resolve` 処理をまとめています。
- merge 後の `apply.state=ready` への更新、`INDEX.md` conflict の自動解消、保存済み report/result を踏まえた apply branch / worktree の cleanup まで担います。

## Read this when

- `cmoc apply join` の処理順、前提条件、終了後の後始末を実装・修正・レビュー・テストしたいとき。
- `--force-resolve` を付けたときに、想定外差分をどう扱うか確認したいとき。
- `INDEX.md` conflict の自動解消条件や、merge 後に `apply.state` を `ready` に戻す流れを確認したいとき。
- apply report と result の保存状況に応じて、`<cmoc-apply-branch>` と `<cmoc-apply-worktree>` を削除してよい条件を確認したいとき。

## Do not read this when

- `cmoc apply fork` の調査・修正・レビューだけを確認したいとき。
- `cmoc apply abandon` の破棄手順や、実行中プロセスの停止だけを確認したいとき。
- `cmoc session join` や `cmoc session abandon` など、session 側の終了・統合・破棄だけを確認したいとき。
- `cmoc apply join` の利用手順ではなく、仕様断片だけを読みたいときは正本仕様を直接参照したいとき。

## hash

- 14303d5581db27bba3b4241b36937c4aba65beea650ba93c33e6e91c79926fe3
