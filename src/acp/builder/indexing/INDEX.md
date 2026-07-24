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
- 正本の index entry builder を互換入口として再公開し、既存の `acp.builder.indexing.index_entry` 参照を維持するモジュール。対象本文をプロンプトへ埋め込む際にコードフェンスを保護する。

## Read this when
- index entry 生成処理の互換入口、正本 builder の再公開、または対象本文のコードフェンス保護を変更・調査するとき。

## Do not read this when
- 正本 builder 自体の仕様や実装を確認したいときは、この互換入口ではなく oracle 側の index entry builder を直接読む。
- index entry 生成と無関係な ACP builder や prompt fence 処理を調査するとき。

## hash
- 0e020616ad4552c8af03a682a96792fd0f240cf4d1599abe1ed34c2d4e6308c5
