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
- realization の apply 処理に関する workload を扱い、apply workload 実装への入口となる。
- realization apply fork の実行管理を担い、oracle 差分の追従、agent 実行、変更検査、commit、run state・fork report 反映までを扱う。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- oracle 差分を追従する apply fork の開始条件、差分固定、agent 実行、変更検査、commit、joinable 公開の流れを確認するとき。
- apply fork の失敗時の rollback、error report、cleanup warning の保存方法を確認するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- 通常の realization apply の agent 指示や仕様を確認するときは、対応する realization apply の仕様・launch 定義を直接読む。
- 既存 run の join／abandon 操作や一般的な editing run ライフサイクルだけを調べるときは、共通 run ライフサイクルの対象を読む。

## hash
- 34f5bd87eebd7912ce893b5903b7f5ad75593ab25165f531e8f24f2407149894

# `refactor`

## Summary
- realization refactor package の処理をまとめる入口。fork による full-cycle の run lifecycle、対象 file の調査・修正、unresolved findings と state の管理、完了判定、report 公開までを扱う。

## Read this when
- realization refactor fork の実行 lifecycle、処理単位、完了判定、report 公開の流れを確認・変更するとき。
- 対象 file への agent 呼び出し、Structured Output、変更 path・commit の検証、refactor state や INDEX 同期を確認するとき。
- unresolved findings の追跡、rename、中断・例外時の cleanup、rollback、error state の扱いを調査するとき。

## Do not read this when
- refactor 対象の選定や state 永続化そのものを確認したいとき。
- 単一 realization file の agent 用 prompt や出力契約だけを確認したいとき。
- 変更概要の生成・分類だけ、または共通 runtime の report、editing run、Git commit、process tracking の一般仕様だけを確認したいとき。

## hash
- 960468530a809af0978896b822d4814954ef3617dc5966ae0ab5315ddeab7e52
