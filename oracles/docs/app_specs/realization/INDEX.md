# `basics.md`

## Summary

- `realization files` の定義と、`oracles files` ではない cmoc の裁量で読み書きしてよいファイル群の基本仕様です。
- `realization code` / `realization implementation` / `realization test` / `realization ancillary` の区分を整理します。
- 例として `src/**/*.py`、`src/**/*.json`、`test/**/*.py`、`.gitignore`、`bin/**/*` を示します。

## Read this when

- `realization files` に該当するかどうかを判定したいとき。
- 実装・テスト・補助ファイルのどれに当たるかを切り分けたいとき。
- `realization standards.md` を読む前に、対象範囲の前提を確認したいとき。

## Do not read this when

- すでに `realization files` の定義が分かっていて、具体的な規範は `standards.md` を読むとき。
- 個別サブコマンドの手順や実装内容を確認したいとき。
- `oracles files` 側の定義や記述標準だけを確認したいとき。

## hash

- e81853bdaab0dc26d64833e5e71d39d98c6400300c408e9edef8c28eb3357791

# `standards.md`

## Summary

- realization files に適用する標準的な編集・設計方針をまとめた文書です。
- 実装・テスト・補助ファイル・設定・状態の肥大化を抑え、重複削減や抽象化の妥当性を確認する基準を扱います。
- `cmoc apply` などで realization files を変更する実装・レビュー時の判断材料になります。

## Read this when

- realization files を追加・修正・削除するときに、守るべき標準を確認したい場合。
- 実装、テスト、補助ファイル、公開面、永続状態を増やすべきか判断したい場合。
- 変更後に削除・統合できる余地がないか、最終確認の基準を見たい場合。
- `cmoc apply` などの realization files 編集処理を実装・レビューするとき。

## Do not read this when

- realization files の基本定義だけを確認したいときは `basics.md` を読むべきです。
- `standards_format.md` の記述形式や、他の開発規約だけを確認したいとき。
- `oracles` ファイルの記述標準や `INDEX.md` の生成ルールだけを確認したいとき。
- realization 以外のサブコマンド仕様や共通仕様を確認したいとき。

## hash

- 6d112ddab9c7d005eba3c03afa567439ea2e8e18709a94bb80e03ecf7c67c2e3
