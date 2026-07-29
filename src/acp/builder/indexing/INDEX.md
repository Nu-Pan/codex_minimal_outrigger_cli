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
- oracle 側の INDEX.md エントリー生成 parameter を再利用し、対象本文に含まれるコードフェンスを保護した互換入口。既存の `acp.builder.indexing.index_entry` 参照を維持するための薄いラッパーで、利用者向け公開面と realization 側から参照がなくなるまで残す。

## Read this when
- INDEX.md エントリー生成処理の互換入口や参照維持の挙動を変更・確認するとき。
- 対象本文のコードフェンス保護や、oracle builder parameter の再公開処理を調査するとき。

## Do not read this when
- INDEX.md エントリー生成の正本仕様や本体 builder の実装を確認したいときは、oracle 側の対応ファイルを直接読む。
- INDEX.md のルーティング内容だけを確認する場合や、indexing 以外の ACP builder を扱う場合。

## hash
- 1fa7430b1e8ef3c930f0126fd6f48b9ed9571a5fa725bdf6a1dbaf45254540f9
