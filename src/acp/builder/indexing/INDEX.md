# `__init__.py`

## Summary
- `acp.builder.indexing` を既存の参照点として維持し、正本実装 `oracle.acp_builder.indexing` への互換入口だけを提供するための層。実体の実装内容ではなく、既存の利用者がこの名前空間を通して index 関連機能へ到達する必要がある場合に読む。

## Read this when
- `acp.builder.indexing.*` という既存参照を壊さずに index 関連機能へ進む必要がある。
- 正本側の実装をそのまま移すのではなく、互換入口としてどこに残すべきかを判断したい。

## Do not read this when
- index 関連の正本実装そのものを変更したい場合は、互換入口ではなく `oracle.acp_builder.indexing` 側を読む。
- この名前空間をもう参照しない前提で整理・削除したい場合は、互換維持ではなく利用側の参照先を確認する。

## hash
- fd4b0dd11238195b4ce76273d3ffc692eb9e441764952be0b436ba20f60452bf

# `index_entry.py`

## Summary
- `oracle.acp_builder.indexing.index_entry` の builder を互換入口として再公開する薄いラッパー。既存の `acp.builder.indexing.index_entry` 参照を維持しつつ、生成された prompt の対象本文セクションに含まれるコードフェンスを保護する。

## Read this when
- インデックスエントリー生成用 builder の互換入口や再公開処理を変更・調査するとき
- 対象本文のコードフェンス保護や prompt 境界の扱いを確認するとき

## Do not read this when
- 正本 builder 自体の仕様や実装を確認したいときは、再公開元の `oracle.acp_builder.indexing.index_entry` を直接読む
- インデックス生成以外の builder や一般的な prompt 処理だけを調査するとき

## hash
- 30dcff94d180dd53dc10991b5d4ad184e44508ba2463dfcb9f43c23560850a7f
