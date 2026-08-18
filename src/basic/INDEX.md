# `__init__.py`

## Summary
- `basic.*` の互換 import を維持するための入口。実体の実装や正本型を複製せず、`basic` という公開面だけを残している。

## Read this when
- `basic.*` 参照を残す必要があるか、削除できるかを判断したいとき。
- 利用者向け公開面の移行先を確認したいとき。
- 互換 import の維持条件や廃止条件を確認したいとき。

## Do not read this when
- `basic.acp`、`basic.path_model`、`basic.struct_doc` の個別実装や再公開内容を確認したいときは、各モジュールを直接読む。
- ACP 基本型や path model の正本仕様そのものを確認したいときは、`basic` ではなく正本側を読む。

## hash
- 8a9d153c30f1ec0c568fd2702b1580077d56f027401c802ee1cca9b03f7b76bb

# `acp.py`

## Summary
- oracle 側で定義された ACP 型を realization 側から再公開する互換層。型定義自体は保持せず、既存の `basic.acp` 参照を維持するための入口である。

## Read this when
- ACP 型の import 経路、`basic.acp` 参照、または realization 側の公開面を変更・調査するとき
- oracle 側の ACP 型と realization 側の再公開関係を確認するとき

## Do not read this when
- ACP 型の正本定義や仕様を確認したいときは、直接 oracle 側の定義を読む
- ACP 型や `basic.acp` の参照経路に関係しない処理を変更・調査するとき

## hash
- b6c1a325e0018a7ea29e9f189cdea64a1bf8ad87c15afcbd45cd971c888337fb

# `path_model.py`

## Summary
- 正本の path model を realization 側で再公開する互換用モジュール。path context・placeholder・path 解決関数の入口であり、実装内容の確認は正本側を読む。

## Read this when
- basic.path_model の公開 import、互換参照、利用者向け path model API の入口を確認するとき。

## Do not read this when
- path model の仕様や実装詳細を確認するときは、再公開元の oracle 側実装を直接読む。basic.path_model と無関係な path 処理を調べるとき。

## hash
- f80137559e09b7e85d1b92c22df5d0ef5f82420f970ee0de34e7b4a5a58eabf3

# `struct_doc.py`

## Summary
- canonical な構造化文書実装を再公開する旧 API 互換モジュール。構造化文書型の旧名エイリアス、タグ生成、Markdown 描画を扱い、実装の入口として下位の canonical renderer 参照へつなぐ。
- 単一 root または root list を受ける旧来の描画 API が必要な場合に読む対象であり、描画処理そのものの仕様や canonical な型定義を確認する場合は参照先の正本実装を直接読む。

## Read this when
- 旧 API の構造化文書型名や Markdown 描画関数の互換インターフェースを確認するとき
- 構造化文書の利用者向け公開面や realization 側に残る旧参照を調査するとき

## Do not read this when
- canonical な構造化文書の型定義、タグ生成、描画仕様を確認したいとき
- 旧 API 互換層を経由せず canonical renderer の利用方法を確認できるとき

## hash
- a211733e9b2de8e38da96c29745f4bd4d5a209692d9dbd59734c1e92cd9a4687
