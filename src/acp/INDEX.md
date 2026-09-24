# `__init__.py`

## Summary
- oracle 側の acp_builder を複製せず、既存の `acp.*` 参照を保つ互換 import 入口として残されている。

## Read this when
- `acp.*` 参照の互換性や、この入口の削除条件を確認するとき。

## Do not read this when
- `acp.builder` 以下の機能や個別モジュールの import 実装を調べるときは、builder パッケージまたは対象モジュールへ進む。

## hash
- fe0939ab61e919bfb5ae35264e02859ee36efb102a15498d95fcbd45f9670e76

# `builder`

## Summary
- 既存の `acp.builder.*` import 経路を保つ互換 adapter 群で、parameter builder の実装は oracle 側へ委譲します。旧 import の追跡や移行の入口です。
- feedback、indexing、oracle、realization、session、TUI の builder 公開経路をまとめ、一部では既存 API の入力を oracle 側の builder に合わせます。

## Read this when
- 既存の `acp.builder.*` 参照を追跡し、互換経路の修正や削除を検討するとき。
- 各 command 領域の builder adapter がどの oracle builder を公開しているか確認するとき。

## Do not read this when
- parameter の正本実装や組み立て内容を調べるときは、対応する oracle builder を直接読む。
- CLI command の dispatch、実行フロー、表示を調べるときは、command 実装から確認する。

## hash
- 29f5fc681339276305cbb34e003cc06ed4eb507b13dc60f0b579bc3c25a40e0c
