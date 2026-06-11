# `basics.md`

## Summary

- `oracles files` の定義、役割、構成、Codex CLI による読み書き可否を定めた基本仕様の入口です。
- `<work-root>/oracles` 配下で `INDEX.md` ではないファイルを `oracles files` とみなす条件と、人間と AI の責任分担を整理します。
- `oracles` 配下で何が正本仕様断片に当たるかを素早く確認するための目次です。

## Read this when

- `oracles files` に該当する条件を確認したいとき。
- AI が `oracles` を読んでよいが編集してはいけない、という境界を確認したいとき。
- Codex CLI 実行後の `oracles` 検査規則や、`.gitignore` / `INDEX.md` との関係を確認したいとき。

## Do not read this when

- `oracles files` の記述標準や、より具体的な書き方を確認したいとき。
- `INDEX.md` の生成・更新ルールや、`oracles` 全体のインデクシング仕様を確認したいとき。
- すでに `oracles files` の定義が分かっていて、個別の仕様断片へ直接進みたいとき。

## hash

- 63737a40000192913da32dea3208e0c41b9d3305464c7b84f5b53444280c6c7d

# `standards.md`

## Summary

- `oracles files` の記述標準をまとめた文書です。
- 人間意図の明示、認知負荷の節約、正本仕様断片としての扱い、未定義部分の許容、総文字数の最小化、論理整合、用語統一、命名の妥当性を扱います。
- ベストプラクティスよりも `oracles standards` を優先する前提と、`goal` と `non-goal` の書き分け方針も案内します。

## Read this when

- `oracles files` をどう書くべきか、原則や規則をまとめて確認したいとき。
- 仕様断片を小さく保つこと、未定義部分の扱い、論理矛盾の回避、用語・命名の統一を確認したいとき。
- `oracles files` のレビューや修正で、標準に照らして妥当か判断したいとき。

## Do not read this when

- `oracles files` の定義や読み書き可否だけを確認したいときは、先に `basics.md` を読むとき。
- `INDEX.md` の生成・更新ルールやインデクシング仕様だけを確認したいときは、`indexing.md` を読むとき。
- この配下の個別仕様へ直接進む前提で、記述標準の確認が不要なとき。

## hash

- 6f046254b705a5cd800738deea028523fa1cf9196cb02751da9b1311630b0302
