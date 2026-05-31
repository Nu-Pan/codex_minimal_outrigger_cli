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

- `src/sub_commands/review` は `cmoc review` 系サブコマンドの入口ディレクトリです。
- `__init__.py` はパッケージ宣言だけを担う最小モジュールです。
- `oracles.py` は `cmoc review oracles` の本体処理を担い、snapshot 固定、評価、改善、レポート出力までを実行します。

## Read this when

- `src/sub_commands/review` が Python パッケージとして宣言されていることを確認したいとき。
- `cmoc review` 系サブコマンドの入口構造を把握したいとき。
- `cmoc review oracles` の本体処理、開始時点の `oracles` スナップショット固定、`INDEX.md` メンテナンス、oracle ファイルごとの評価、問題点リスト改善、レポート保存の流れを確認したいとき。

## Do not read this when

- `cmoc review oracles` の利用手順や引数だけを確認したいときは、`oracles/docs/app_specs/sub_commands/review_oracles.md` を読むべきです。
- `cmoc review` の CLI 登録や hidden alias だけを確認したいときは、`src/main.py` を読むべきです。
- `oracles` 側の正本仕様を直接確認したいときは、このディレクトリではなく該当する `oracles/docs/app_specs/sub_commands/review_oracles.md` を読むべきです。

## hash

- ba96158499db8bdaddc7b53e80af57c4cbdb7d04609576116de1117fa85c8a42
