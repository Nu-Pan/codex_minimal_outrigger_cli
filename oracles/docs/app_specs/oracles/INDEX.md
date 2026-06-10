# `basic_definitions.md`

## Summary

- `oracles ファイル` の定義、役割、構成、Codex CLI による読み書き可否を定めた基本仕様断片です。
- `<work-root>/oracles` 配下で `INDEX.md` ではないファイルを `oracles ファイル` とみなす条件と、AI と人間の責任分担を示します。
- Codex CLI 実行後に `oracles` の未コミット差分やコミット範囲内の変更を検査する前提も扱います。

## Read this when

- `oracles ファイル` に該当するかどうかを判定したいとき。
- AI が `oracles` を読んでよいが編集してはいけない、という境界を確認したいとき。
- Codex CLI 実行後の `oracles` 検査規則や、`.gitignore` / `INDEX.md` との関係を確認したいとき。

## Do not read this when

- oracles ファイル記述標準そのものや、より具体的な記述ルールを知りたいときは `writing_standards.md` を読むべきです。
- `INDEX.md` の生成・更新ルールや全体のインデクシング仕様を確認したいときは `indexing.md` を読むべきです。
- すでに `oracles ファイル` の定義が分かっていて、個別の仕様断片や実装コードへ直接進むとき。

## hash

- 0ddbbdd8781386cc38af18e3e4920e76c3ad643ac1605b8e71e1be7ee1a7ac3e

# `writing_standards.md`

## Summary

- `oracles` ファイルの記述標準をまとめた文書で、正本仕様断片をどう書くかの原則と規則を案内します。
- 人間意図のテキスト化、総文字数の最小化、論理的整合、用語統一、命名の整合を重視します。
- 基本定義を踏まえたうえで、`oracles` ファイルを書く・直す・レビューするための入口です。

## Read this when

- oracles ファイルをどう書くべきか、原則や規則をまとめて確認したいとき。
- 仕様断片を小さく保つ方針、未定義動作の扱い、論理矛盾の回避方針を確認したいとき。
- 用語・表記の統一や命名の整合、goal/non-goal の書き分けを確認したいとき。

## Do not read this when

- `oracles` ファイルの定義や役割だけを確認したいときは、先に `basic_definitions.md` を読むべきです。
- `INDEX.md` の生成・更新ルールだけを確認したいときは、この文書ではなく `indexing.md` を参照すべきです。
- この配下の個別仕様の入口だけをたどりたいときは、ここではなく該当ファイルを直接読むべきです。

## hash

- d531dbb39e84a4597839cb565aa3bf3f5d5712059ad63804f8cee1204b2514e2
