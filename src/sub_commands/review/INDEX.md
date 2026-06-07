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

- `src/sub_commands/review/oracles.py` は `cmoc review oracles` の本体実装で、session branch の前提検証から review worktree の作成、oracle スナップショット固定、所見の列挙・統合・検証・判定、レポート出力までを一連で担います。
- Structured Output を使う所見パイプライン、`INDEX.md` を根拠にした対象 oracle の選定、`INDEX.md` コンフリクトの機械的解消、失敗時の error report 生成までをまとめています。
- 所見の集約、評価メタデータ更新、結果集計、Markdown レポート整形を支える helper 群もこのモジュールに含まれます。

## Read this when

- `src/sub_commands/review/oracles.py` の実装・修正・レビュー・テストを行うとき。
- `cmoc review oracles` の実行前検証、review branch / worktree、oracle snapshot、所見パイプライン、レポートの流れを追いたいとき。
- 所見の列挙・マージ・検証・判定に使う Structured Output スキーマや、各 helper の役割を確認したいとき。
- merge conflict 中の `INDEX.md` 自動解消や、評価結果・エラーレポートの保存条件を確認したいとき。

## Do not read this when

- `cmoc review oracles` の利用手順、引数、出力仕様だけを確認したいときは、`oracles/docs/app_specs/sub_commands/review_oracles.md` を読むべきです。
- `src/sub_commands/review` のパッケージ宣言だけを確認したいときは、`src/sub_commands/review/__init__.py` を読むべきです。
- `cmoc review oracles` の CLI 登録や hidden alias だけを確認したいときは、`src/main.py` を読むべきです。
- `INDEX.md` の生成・更新ルールや、`oracles` 全体のルーティング方針だけを確認したいときは、`oracles/docs/app_specs/indexing.md` を読むべきです。

## hash

- 1497383b01ca423425a15a8db16ad46adecf82dbe5d21baaeb81045629e48e50
