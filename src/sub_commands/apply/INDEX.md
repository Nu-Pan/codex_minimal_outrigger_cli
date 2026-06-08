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

- `src/sub_commands/apply/fork.py` のルーティング目次で、`cmoc apply fork` の本体実装へ進む入口です。
- session state 検証、apply worktree 作成、`.cmoc` の追跡対象外保証、不整合調査・修正ループ、レポート生成を担当する主要処理群へ案内します。
- Structured Output の検証、dirty path 管理、commit と error report の分岐など、apply 実行制御の中核を整理します。

## Read this when

- `src/sub_commands/apply/fork.py` の実装・修正・レビュー・テストを始めるとき。
- `session.state` / `apply.state` の前提条件や、`--scope` と反復回数オプションの扱いを確認したいとき。
- apply worktree 作成、`.cmoc` の非追跡保証、不整合調査・修正ループ、レポート生成までの流れを追いたいとき。
- 不整合調査用の Structured Output schema、要修正点の整理、change summary、エラー時のフォールバックを確認したいとき。

## Do not read this when

- `cmoc apply fork` の利用手順や完了条件だけを確認したいときは、実装ではなく `oracles/docs/app_specs/sub_commands/apply_fork.md` を読むべきです。
- `src/sub_commands/apply` 配下の入口構造だけを確認したいときは、`src/sub_commands/apply/INDEX.md` を読むべきです。
- `cmoc apply join` や `cmoc apply abandon` の開始・統合・破棄フローだけを確認したいときは、このファイルではなく各実装モジュールへ進むべきです。
- `apply` 本体の実行制御ではなく、`oracles` 側の仕様断片や利用手順だけを確認したいときには、この目次は不要です。

## hash

- 78820ca01231f912a9b2007048e09892df94e1684e94ec5fcd732b38d350da34

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
- `cmoc session` 系サブコマンドの開始・統合・破棄だけを確認したいとき。
- `src/sub_commands/apply` 配下の入口構造だけを確認したくて、`join.py` の処理本体は不要なとき。
- `cmoc apply join` の利用手順や正本仕様断片だけを確認したいとき。

## hash

- 6008f07de4a859416448e20eeacdf97252412bcd0a61f8877baaec4d5452f5fb
