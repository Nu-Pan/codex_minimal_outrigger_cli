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
- realization のリファクタリング処理をまとめるパッケージで、関連するリファクタリング機能への入口を提供する。
- realization refactor fork の CLI ライフサイクル全体を管理し、state・INDEX の初期化、対象ファイルごとの調査・修正、差分検証、commit、完了判定、変更概要、fork report 保存を扱う。未解決 finding、処理済み target、investigation_required、および自然完了・未解決付き完了・中断・error の結果を追跡する。

## Read this when
- realization のリファクタリング処理の構成や入口を確認するときは、このパッケージを読む。
- realization refactor fork の CLI 実行フロー、対象ファイル単位の調査・修正、Structured Output 検証、差分拒否、commit、state 更新、完了判定を変更または調査するとき。
- 中断・例外時の rollback、run state 更新、fork report 生成、未解決 finding の追跡を確認するとき。

## Do not read this when
- refactor agent の parameter を変更するときは、file review 用または change summary 用の builder を直接読む。
- refactor state のデータ構造や target 選択ロジックだけを変更するときは、commons.runtime_refactor を直接読む。
- run lifecycle、process tracking、report の共通形式だけを確認するときは、対応する commons runtime module を直接読む。

## hash
- 940fada598989cb5c09d93422390abb8028c493ae6c2c75d210dc3e422aa061a
