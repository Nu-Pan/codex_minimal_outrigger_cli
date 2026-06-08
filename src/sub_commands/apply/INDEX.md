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

- `src/sub_commands/apply/fork.py` は `cmoc apply fork` の本体実装モジュールで、session state の検証から apply worktree の作成、不整合調査と修正適用、最終レポート生成までをまとめて担当します。
- このモジュールには、`apply` 開始時の状態遷移、`.cmoc` の追跡対象外保証、scope / repeat オプションの検証、dirty path の管理、報告書の書き込みまでを支える主要ヘルパー群が含まれます。
- 不整合調査の Structured Output schema、要修正点リストの改善、変更要約の生成、エラーレポートのフォールバックなど、`cmoc apply fork` の実行制御と診断処理の中核を担うファイルです。

## Read this when

- `src/sub_commands/apply/fork.py` の実装・修正・レビュー・テストを行いたいとき。
- `cmoc apply fork` の開始条件、`session.state` / `apply.state` の検証、`--scope` や反復回数オプションの扱いを確認したいとき。
- apply worktree の作成、`.cmoc` の追跡対象外保証、不整合調査・修正ループ、レポート出力までの一連の処理順を追いたいとき。
- Structured Output の schema、要修正点リストの改善、change summary の生成、payload 検証、commit や forbidden path の扱いを確認したいとき。

## Do not read this when

- `cmoc apply fork` の利用手順、引数の意味、完了条件だけを確認したいときは、実装ではなく `oracles/docs/app_specs/sub_commands/apply_fork.md` を読むとき。
- `src/sub_commands/apply` 配下の入口構造だけを確認したいときは、このファイルではなく `src/sub_commands/apply/INDEX.md` を読むとき。
- `cmoc apply join` や `cmoc apply abandon` の開始・統合・破棄フローだけを確認したいとき。
- `INDEX.md` の生成ルールや共通のルーティング仕様だけを確認したいときは、この実装ファイルではなく `src/commons/indexing.py` や `oracles/docs/app_specs/` 側を読むとき。

## hash

- dbf4b3e80831edec639011a67cdca2564ca2fa0e6a18c9b30297b0357c6248c7

# `join.py`

## Summary

- `src/sub_commands/apply/join.py` は `cmoc apply join` の本体実装モジュールで、完了済みの apply branch を session branch へ取り込む処理を担います。
- `session.state` / `apply.state` の検証、想定外差分の判定と `--force-resolve`、`INDEX.md` conflict の自動解消、merge 後の cleanup と warning 出力をまとめています。
- 保存済み report の確認、apply branch と worktree の削除条件、join 後の session state 更新もこのモジュールの責務です。

## Read this when

- `src/sub_commands/apply/join.py` の実装・修正・レビュー・テストを行いたいとき。
- 完了済みの apply branch を session branch へ取り込む処理順、state 更新、cleanup 条件を確認したいとき。
- `--force-resolve`、未コミット差分チェック、想定外差分の扱い、`INDEX.md` conflict の自動解消を追いたいとき。
- 保存済み report の有無や apply worktree / branch 削除の安全条件を確認したいとき。

## Do not read this when

- `cmoc apply fork` や `cmoc apply abandon` の開始・破棄フローだけを確認したいとき。
- `cmoc session` 系の開始・統合・破棄だけを確認したいとき。
- `cmoc apply join` の利用手順や正本仕様だけを確認したいとき。
- `src/sub_commands/apply` 配下の入口構造だけを確認したくて、`join.py` の処理本体は不要なとき。

## hash

- 8322fdb7a5db9421fcf5b60f07aa219868b4c00343fc76e8cf45b7b7d4dc035a
