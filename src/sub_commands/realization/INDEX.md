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
- realization の apply 処理に関する workload を扱うディレクトリ。apply workload の実装を確認する入口となる。
- `cmoc realization apply fork` の実行処理を担当し、agent 起動から差分検査、INDEX 更新、commit、run lifecycle、fork report 保存までを管理する。異常時の cleanup、rollback、error 化にも対応する。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- `cmoc realization apply fork` の挙動、run lifecycle、agent 起動、差分検査、commit、異常時処理、fork report を調査・変更するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- apply fork の prompt 構築だけを変更・調査するとき。
- run の join、abandon、共通 lifecycle 処理、report 形式そのものを変更・調査するとき。

## hash
- 6fe0dfe0b7c6204fe253087f04ebeae4cea6e52605da9bcc768b9455177adf32

# `refactor`

## Summary
- realization のリファクタリング処理を扱うパッケージ。リファクタリング処理の構成確認や、fork lifecycle 全体の調査・変更に進む入口となる。

## Read this when
- realization のリファクタリング作業の内容や構成を確認するとき。
- realization refactor fork の開始から完了・中断・エラー処理までを調査または変更するとき。
- 対象ファイル選択、agent 出力検証、state 更新、commit、変更概要、fork report の処理を確認するとき。

## Do not read this when
- 単一ファイルの refactor agent 用 prompt や所見 schema の詳細だけを確認したいとき。
- refactor state の永続化や target 選択そのものを調査したいとき。
- run lifecycle の共通操作や report の共通形式だけを確認したいとき。
- realization のリファクタリング以外の処理を確認するとき。

## hash
- 9942620495be0ce2cf9d09c1daa98105831dbcf02d85f689c4648fe99d539504
