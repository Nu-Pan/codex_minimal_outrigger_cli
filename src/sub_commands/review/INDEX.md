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

- `src/sub_commands/review/oracles.py` は `cmoc review oracles` の本体処理を担うモジュールです。
- 開始時点の `oracles` ツリーを snapshot として固定し、部分評価・全体評価の切り替え、`INDEX.md` メンテナンス、oracle ファイルごとの評価、問題点リスト改善を順に実行します。
- 評価結果やエラー時の代替レポートを `.cmoc/reports/review_oracles` に保存し、Structured Output の妥当性確認も行います。

## Read this when

- `cmoc review oracles` の本体処理を実装・修正・レビューしたいとき。
- 開始時点の `oracles` スナップショット固定、`INDEX.md` の反映、oracle ファイルごとの並列評価、問題点リスト改善、レポート保存の流れを確認したいとき。
- Structured Output の検証条件や、参照してよい `oracles` 配下ファイルの制約を確認したいとき。
- 評価失敗時のエラーレポート生成や、` .cmoc/reports/review_oracles` への出力規則を確認したいとき。

## Do not read this when

- `cmoc review oracles` の利用手順や引数、仕様断片だけを確認したいときは、`oracles/docs/app_specs/sub_commands/review_oracles.md` を読むべきです。
- `cmoc review` の CLI 登録や隠し別名だけを確認したいときは、`src/main.py` を読むべきです。
- `src/sub_commands/review` ディレクトリ全体の入口構造や `__init__.py` だけを確認したいときは、このファイルではなくディレクトリの `INDEX.md` を読むべきです。

## hash

- dcdfcbeda439e56148eb3d4317d8aae90d9eaa8a4ceffd6d8b3b82175cd6d11a
