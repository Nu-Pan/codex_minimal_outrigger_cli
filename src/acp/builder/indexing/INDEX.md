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
- 既存の `acp.builder.indexing.index_entry` 参照を維持する互換入口。正本 builder が生成した agent call parameter を再公開し、対象本文に含まれる連続 backtick が外側の fence を閉じないよう prompt の本文 fence を調整する。

## Read this when
- index entry 生成処理の互換入口や既存参照の維持条件を確認するとき
- 対象本文を埋め込む prompt の fence 保護処理を変更・検証するとき

## Do not read this when
- 正本の index entry parameter 生成仕様そのものを確認したいときは、対応する oracle builder を直接読む
- index entry 生成とは無関係な ACP builder や一般的な indexing 処理を調べるとき

## hash
- a1005ece30faba73ae96f6965a5954e9f85a4a0d720a2726b9a15b0e234fa312
