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
- 正本の index-entry builder を互換入口として再公開し、既存の acp.builder.indexing.index_entry 参照を維持する。正本 builder の parameter 生成結果を利用しつつ、対象本文を prompt に埋め込む際のコードフェンスを保護する。
- index-entry 生成処理の互換参照を調査・変更するときの入口であり、実装の正本や prompt 受け渡し仕様そのものを確認する場合は、再公開先の正本 builder または prompt 標準仕様へ進む。

## Read this when
- 既存の acp.builder.indexing.index_entry 参照を維持する互換入口の挙動を確認・変更するとき
- index-entry 生成 prompt に対象本文を受け渡す際のコードフェンス保護を確認するとき

## Do not read this when
- 正本の index-entry builder の実装や仕様を確認する場合
- prompt の受け渡し規則そのものを確認する場合
- 互換参照が不要になった後の公開面・削除条件を判断する場合

## hash
- df469394274b0fb7e906f0ba973dc2d44e79a45555d08d3ec02d0794e5ff72dd
