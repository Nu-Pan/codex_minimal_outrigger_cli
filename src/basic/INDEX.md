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
- oracle 側で定義された ACP のエージェント呼び出しパラメータ型とファイルアクセスモード型を、利用者向けの basic 名前空間から再公開する互換入口。正本型を複製せず、既存の oracle 定義を参照する。

## Read this when
- ACP のエージェント呼び出しパラメータ型またはファイルアクセスモード型を、basic 名前空間から利用・確認する必要があるとき。
- realization 側で basic.acp への参照を整理し、互換再公開層の削除可否を判断するとき。

## Do not read this when
- oracle 側にある ACP 型の定義や詳細仕様を確認したいとき。
- basic 名前空間以外の ACP 実装や、型を利用する具体的な処理を直接確認したいとき。

## hash
- 53332796af2860b66db15176a77da24eb3dc94d8c7a9cd5ac7c0976c131ceef3

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
- 対象は、正本の構造化文書実装を複製せずに再公開する旧 API 互換モジュールです。
- 構造化文書の型・タグブロック・コードブロック・テキスト整形関数を既存の正本実装へ委譲し、単一 root と root list の旧入力を canonical renderer に接続します。

## Read this when
- 旧 API の `basic.struct_doc` が提供する構造化文書型や Markdown 描画の公開面を確認したいとき。
- 正本実装を変更せず、旧 API 互換の import 名または単一/list 入力の描画委譲を追跡するとき。

## Do not read this when
- 正本の構造化文書の仕様・実装詳細そのものを確認したいときは、委譲先の `oracle.other.struct_doc` を直接読む。
- 旧 API の利用箇所や公開面から `basic.struct_doc` 参照の削除条件を調べるだけなら、利用者側または realization 側の参照を直接確認する。

## hash
- af43e040dd3486650a983758c3690bb793725619f88150162976d6f590e8b8ac
