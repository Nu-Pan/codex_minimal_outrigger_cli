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
- 互換性維持のため、旧来の `acp.builder.indexing.index_entry` 参照から正本のインデックスエントリー生成 builder を再公開する入口。対象パス・内容・agent の実行ディレクトリを受け取り、正本 builder が作る agent call parameter をそのまま返す。

## Read this when
- 旧来の `acp.builder.indexing.index_entry` 参照の互換性、移行状況、またはインデックスエントリー生成用の agent call parameter の受け渡しを確認するとき。
- この互換入口の削除可否を判断するとき。realization 側と利用者向け公開面から旧参照がなくなったことを確認する必要がある。

## Do not read this when
- 正本のインデックスエントリー生成 builder の実装や prompt 受け渡し仕様を確認したいときは、再公開入口ではなく正本側を直接読む。
- インデックスエントリーの内容や routing 規則を確認したいだけで、旧参照の互換性を扱わないとき。

## hash
- 80bfd6581aaad9c0f9890bd39041a8165fac751a9246c4787922de033dbcd812
