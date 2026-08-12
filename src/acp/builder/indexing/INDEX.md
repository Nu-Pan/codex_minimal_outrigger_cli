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
- `oracle` 側の index-entry パラメータ生成機能を `acp.builder.indexing.index_entry` から利用するための互換入口。旧参照を維持する必要がある場合に、公開される生成関数の再公開内容を確認する起点となる。

## Read this when
- `acp.builder.indexing.index_entry` の互換性維持や旧参照の削除条件を確認するとき。

## Do not read this when
- index-entry 生成の実装詳細を確認したいときは、再公開元の `oracle` 側実装を直接読む。
- `acp.builder.indexing` の別機能や、旧参照の利用状況を調査しないとき。

## hash
- 6250929e8aef3d4fa7e09a0b2b69e1cecb8c2ee1b53aa26c9604fbc5fc86d631
