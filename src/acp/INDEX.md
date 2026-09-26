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
- `oracle.acp_builder` のビルダーを既存の ACP import 経路から再公開する互換アダプター群。quota probe では既存の引数形式を正本ビルダー向けに変換する。

## Read this when
- 既存の ACP ビルダー import 経路の互換性や公開方法を調べる、またはアダプターの追加・変更・削除を検討するとき。
- quota probe の互換引数から正本ビルダーを呼び出す流れを確認するとき。

## Do not read this when
- ビルダーの正本実装や動作を変更・調査するときは、正本側の実装へ進む。
- ビルダーを呼び出す側の処理を変更・調査するときは、その呼び出し元を直接確認する。

## hash
- 56a7f15d3b8ac83772664acb3eaaef91439f04ce5d0f2c4fa4be8196bebdd806
