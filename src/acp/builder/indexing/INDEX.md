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
- `acp.builder.indexing.index_entry` の互換入口を保つための再公開層。実体ではなく、既存参照を切らさずに oracle 側の実装へつなぐ役割を持つ。

## Read this when
- `acp.builder.indexing.index_entry` への既存の利用経路を維持したいとき。
- 互換入口として残すか、削除条件を判断したいとき。

## Do not read this when
- 実体の実装内容や振る舞いを確認したいときは、再公開先の oracle 側を読む。
- 新しい機能追加や索引処理の設計変更を考えるだけなら、この互換入口ではなく実装側を読む。

## hash
- e9117a11bed4e8ab8054372ace27e1b8b6a68446bd98cdd03ad65d4dcd81ea24
