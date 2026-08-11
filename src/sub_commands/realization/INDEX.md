# `__init__.py`

## Summary
- realization workload サブコマンドのパッケージ入口。

## Read this when
- realization workload サブコマンドの実装や構成を確認するとき。

## Do not read this when
- realization workload サブコマンドに関係しない処理を確認するとき。

## hash
- 45f2cdf62d9edd181a1f1cc14734db2757e556059630746b1486c1bd5d1101b4

# `apply`

## Summary
- 指定ディレクトリは realization の apply 処理を担い、apply workload の実装と `realization apply fork` の実行ライフサイクルを確認する入口です。
- `fork.py` は editing run の作成から agent 実行、変更検査、INDEX 再生成、commit または rollback、fork report 保存までを一体として管理し、apply 固有の差分始点と feedback 情報も扱います。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- `cmoc realization apply fork` の CLI 挙動、run の完了状態、agent の変更許可範囲、commit 防止、INDEX 再生成、差分の commit・rollback を確認するとき。
- fork report に記録される完了理由、変更パス、return code、cleanup warning、feedback 情報を確認するとき。

## Do not read this when
- apply workload や `realization apply fork` の実行全体ではなく、agent 起動パラメータの構築方法だけを確認する場合。
- editing run の共通ライフサイクルや git 差分操作の詳細だけを確認する場合。
- apply の正本仕様や利用者向け手順を確認する場合。

## hash
- 88043850330809edcca17aedfb1ed1a7c1aeb3364f4c249070277512dd6b758e

# `refactor`

## Summary
- realization のリファクタリング処理を構成するパッケージ。関連するリファクタリング処理の構成と、refactor fork の実行フローを確認するための入口となる。

## Read this when
- realization のリファクタリング処理の構成を確認するとき
- realization refactor fork の lifecycle、状態遷移、進捗管理、完了判定、report 生成を調査または変更するとき

## Do not read this when
- realization のリファクタリング以外の処理を確認するとき
- agent 用入力パラメータや所見 schema、refactor state の一般構造、共通 runtime の仕様、fork report の共通レンダリング形式だけを確認するときは、対応する下位実装または共通仕様を直接読む

## hash
- 5085c3766e84d37f77ab0a1eb68b7635159eb78bb36e8ff04659257ed8156faa
