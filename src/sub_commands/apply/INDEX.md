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

- `src/sub_commands/apply/fork.py` は `cmoc apply fork` の本体実装です。
- session branch 上で専用 apply branch と worktree を作成し、不整合調査と修正反復を実行して report 生成までを担います。
- 起動前の state 検証、`.cmoc` の ignore 保証、apply start の排他制御、失敗時の状態更新とエラーレポート作成も含みます。

## Read this when

- `cmoc apply fork` の本体実装の責務と処理順を確認したいとき。
- session/apply state の検証、`.cmoc` の ignore 保証、apply start のロック、worktree 作成の流れを追いたいとき。
- 要修正点の Structured Output、調査・修正ループ、scope に応じた対象選定、commit の流れを確認したいとき。
- `INDEX.md` の保守、report / error report の生成、`running` / `completed` / `error` の状態遷移を確認したいとき。

## Do not read this when

- `cmoc apply` の入口ディレクトリ全体の役割分担だけを確認したいとき。
- `cmoc apply join` や `cmoc apply abandon` の終了・破棄処理だけを確認したいとき。
- `cmoc apply fork` の利用手順や引数仕様だけを確認したいとき。
- `oracles/docs/app_specs/sub_commands/apply_fork.md` の正本仕様を直接確認したいとき。

## hash

- 413f47324c667842b937c6453158c7ca007f739528a183e479df30dac0519d0e

# `join.py`

## Summary

- `src/sub_commands/apply/join.py` は `cmoc apply join` の本体実装で、完了済みの apply branch を session branch に取り込む処理を担います。
- session/apply state の検証、現在 branch と local branch の存在確認、未コミット差分の確認、想定外差分の `--force-resolve` 処理をまとめて扱います。
- merge 後の `apply.state=ready` への更新と、保存済み report/result を前提にした apply branch / worktree の cleanup まで含みます。

## Read this when

- `cmoc apply join` の実装・修正・レビュー・テストを行いたいとき。
- `session.state` / `apply.state` の前提条件や、`apply.state = error` を許容して進める条件を確認したいとき。
- `--force-resolve`、想定外差分、`INDEX.md` のコンフリクト自動解決、merge 後の cleanup 条件を追いたいとき。
- apply branch の取り込み後に `apply.state` を `ready` に更新し、report / result を前提に branch と worktree を削除する流れを確認したいとき。

## Do not read this when

- `cmoc apply fork` の調査・修正ループやレポート生成だけを確認したいとき。
- `cmoc apply abandon` や `cmoc session` 系の終了・破棄処理だけを確認したいとき。
- `cmoc apply join` の利用手順や正本仕様だけを確認したいときは、`oracles/docs/app_specs/sub_commands/apply_join.md` を読むべきです。

## hash

- 877db52c423a4f3e39239fdf27be8ce8649a7830c3aeaf6163aefd0d64f87510
