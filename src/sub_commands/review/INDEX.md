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

- `src/sub_commands/review/oracles.py` は `cmoc review oracles` の本体実装です。
- session branch の前提条件確認、`.cmoc` の ignore 保証、review 用 branch / worktree の作成と merge をまとめて担います。
- oracle tree の snapshot 固定、`INDEX.md` を起点にした評価対象の選定、所見パイプライン、評価結果レポートと error report の出力を扱います。
- Structured Output schema の読込・検証、所見の列挙 / 統合 / 検証 / 判定、および関連ヘルパー群もこのファイルに含まれます。

## Read this when

- `src/sub_commands/review/oracles.py` の実装・修正・レビュー・テストを行いたいとき。
- session branch 前提の検証、clean worktree 確認、review worktree 作成と merge の流れを追いたいとき。
- oracle snapshot の固定、`INDEX.md` を基準にした対象ファイル選定、所見の列挙・統合・検証・判定の処理順を確認したいとき。
- Structured Output schema の読み込みと payload 検証、失敗時を含む report 生成の流れを把握したいとき。

## Do not read this when

- `src/sub_commands/review` 配下の入口構造だけを把握したいときで、個別の評価フローまでは不要なとき。
- `cmoc review oracles` の利用手順、引数、出力仕様だけを確認したいとき。
- `cmoc review` の CLI 登録や hidden alias だけを確認したいとき。
- `apply` や `session` など、review 以外のサブコマンド実装を追いたいとき。

## hash

- 87c5d09edec2fc697a818012ccd31eb47a7b0969d8acf53a884ce7da442fcc42
