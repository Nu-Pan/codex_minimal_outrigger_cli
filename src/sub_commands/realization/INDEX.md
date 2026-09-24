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
- realization の refactor fork サブコマンドを実行する単一ワークロードで、対象選択、ファイル単位の調査・修正、未解決 finding 管理、完了判定、run 状態更新、割り込み時の後処理、fork report 保存までの lifecycle を担う。

## Read this when
- realization refactor fork の実行フロー、run の joinable/error/interrupted 遷移、対象ファイルの修正処理、完了報告を確認したいとき。

## Do not read this when
- refactor fork の内部 lifecycle ではなく、別の realization サブコマンドや個別の change summary／file review builder の仕様を確認したいとき。

## hash
- 3ce928d565a11c0b77ec274c84a07ee75ebf6e61799aaa1112966ce4aa056db6
