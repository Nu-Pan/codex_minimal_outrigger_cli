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

- `cmoc apply fork` の利用手順だけを確認したいときは、このファイルではなく `oracles/docs/app_specs/sub_commands/apply_fork.md` を読むべきです。
- `cmoc apply join` や `cmoc apply abandon` の実装・状態遷移だけを追いたいときは、このファイルではなく各モジュール本体へ進むべきです。
- `src/sub_commands/apply` 配下の入口構造だけを確認したいときは、このファイルではなく `src/sub_commands/apply/INDEX.md` を読むべきです。
- `INDEX.md` の生成ルールや `oracles` 側の共通仕様だけを確認したいときは、このファイルではなく `src/commons/indexing.py` や `oracles/docs/app_specs/` 側を読むべきです。

## hash

- 8683ba3792627173b9ea56042659da112adf8e95a5b39312655d7b0af6ed6939

# `join.py`

## Summary

- `src/sub_commands/apply/join.py` は `cmoc apply join` の本体実装です。
- 完了済み apply branch を session branch へ `git merge --no-ff` で取り込み、state 検証、想定外差分の判定、`INDEX.md` conflict の自動解消まで扱います。
- merge 後に session state を `ready` に戻し、保存済みレポートと結果の確認を前提に apply branch / worktree の削除と warning 出力を行います。

## Read this when

- `cmoc apply join` の merge 手順、前提 state、現在 branch の検証を確認したいとき。
- 想定外差分の検出と `--force-resolve` による revert の挙動を追いたいとき。
- `INDEX.md` conflict の自動解消条件や、merge 後の session state 更新・cleanup 条件を確認したいとき。
- apply branch / worktree の削除可否や warning の出力を把握したいとき。
- `src/sub_commands/apply/join.py` の実装・修正・レビュー・テストを始める前に、処理順と状態遷移を確認したいとき。

## Do not read this when

- `src/sub_commands/apply/join.py` ではなく、`cmoc apply fork` や `cmoc apply abandon` の実装を確認したいとき。
- `cmoc apply join` の利用手順や正本仕様だけを確認したいときは、`oracles/docs/app_specs/sub_commands/apply_join.md` を直接読むべきとき。
- `src/sub_commands/apply/__init__.py` のようなパッケージ宣言や、`cmoc apply` の入口構造だけを確認したいとき。
- `cmoc session` や `cmoc review` など、別サブコマンド群の実装を追いたいとき。

## hash

- 05b64815ab4ec9fd70535e8b3868aa04a65a838082258550654ee9678b02ddf0
