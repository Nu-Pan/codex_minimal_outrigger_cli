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
- 既存の acp.builder.indexing.index_entry 参照を維持する互換入口。正本 builder へ委譲し、対象本文のコードフェンスを保護した AgentCallParameter を生成する。

## Read this when
- index_entry の互換参照、正本 builder への委譲、または対象本文のプロンプト埋め込み時のコードフェンス保護を変更・確認するとき。

## Do not read this when
- 正本の builder 仕様やプロンプト構築自体を変更・確認するときは、oracle 側の対応ファイルを直接読む。
- index 作成処理や他の prompt fence 保護処理だけを変更・確認するとき。

## hash
- b092e2255012c464484aedf6665543543a554ff95e2f4508e91e063858237730
