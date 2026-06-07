# `__init__.py`

## Summary

- `src/sub_commands/review/__init__.py` は `cmoc review` 系サブコマンドのパッケージ宣言だけを担う最小モジュールです。
- 公開 API、定数、実行ロジック、再エクスポートは持ちません。

## Read this when

- `src/sub_commands/review` が Python パッケージとして宣言されていることを確認したいとき。
- `cmoc review` 系サブコマンドの入口となるパッケージ構造を把握したいとき。

## Do not read this when

- `cmoc review oracles` の実行フローや評価ロジックを確認したいときは、このファイルではなく `oracles.py` を読むべきです。
- `cmoc review oracles` の CLI 引数や hidden alias 登録だけを確認したいときは、`src/main.py` を読むべきです。

## hash

- d432dc21ecc8d2cabf968eac490bb998f303e6d3e7411b90260759ccd587f07d

# `oracles.py`

## Summary

- `src/sub_commands/review/oracles.py` は `cmoc review oracles` の本体実装で、session branch の前提検証から review worktree の作成、oracle スナップショット固定、所見パイプラインの実行までをまとめて担います。
- 所見の列挙・統合・検証・判定を Structured Output 付きで進め、評価用 `INDEX.md` のメンテナンス反映、review branch の merge、Markdown レポート出力までを一連で処理します。
- レビュー対象の oracle 選定、部分評価と全体評価の切り替え、merge conflict 中の `INDEX.md` 自動解消、失敗時のエラーレポート生成もこのモジュールの役割です。

## Read this when

- `cmoc review oracles` の実装・修正・レビュー・テストを行いたいとき。
- session branch 前提の検証、`.cmoc` の ignore / clean 状態確認、review worktree 作成の流れを追いたいとき。
- oracle スナップショット固定、`INDEX.md` メンテナンス反映、所見の列挙・統合・検証・判定のパイプラインを確認したいとき。
- review branch を session branch へ merge する処理や、レポート / エラーレポートの保存仕様を確認したいとき。

## Do not read this when

- `cmoc review oracles` の利用手順、引数仕様、出力仕様だけを確認したいときは、実装ではなく `oracles/docs/app_specs/sub_commands/review_oracles.md` を読むべきです。
- `src/sub_commands/review` のパッケージ宣言だけを確認したいときは、`src/sub_commands/review/__init__.py` を読むべきです。
- `cmoc` 全体の `INDEX.md` 生成・更新ルールだけを確認したいときは、`oracles/docs/app_specs/indexing.md` を読むべきです。
- oracles 側の正本仕様断片そのものを確認したいときは、`oracles/INDEX.md` から仕様をたどるべきです。

## hash

- b3b7a57baaf5e669bb120fe20242d336e8ac018c964e8cda1bd17875d52703b6
