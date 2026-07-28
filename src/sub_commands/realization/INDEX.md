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
- `__init__.py` は realization の apply workload を扱うモジュールで、apply workload 実装の入口となる。
- `fork.py` は `cmoc realization apply fork` の CLI サブコマンド実装で、agent 起動、oracle 差分、変更検査、INDEX 更新、commit・rollback、run 状態、fork report を扱う。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- `realization apply fork` の実行フロー、run 状態遷移、agent 差分の許可判定、commit・rollback、fork report を確認するとき。
- realization apply agent の起動条件、oracle 差分の受け渡し、INDEX 更新を含む処理単位を確認するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- realization apply の prompt 構築や agent parameter の詳細だけを確認するとき。
- run の共通ライフサイクル、プロセス追跡、report 出力の共通仕様だけを確認するとき。

## hash
- 186517b2c807ee9b332dd2edad16cd426f331f86f4a22d26f2273738341fbdd1

# `refactor`

## Summary
- realization のリファクタリング処理を扱うパッケージで、関連サブコマンドの実装入口となる。
- fork.py は realization refactor fork の実行ライフサイクル全体を管理し、対象選択、agent による調査・修正、差分検証、state 更新、commit、完了判定、unresolved 所見、report 保存、中断・エラー時の cleanup を担う。

## Read this when
- realization refactor の処理フロー、対象 file の反復、agent 出力検証、差分制約、commit 単位を確認するとき
- unresolved finding、investigation_required、完了判定、change summary、fork report の生成や保存を変更するとき
- KeyboardInterrupt や BaseException 発生時の子プロセス停止、rollback、run 回収、error report を調査するとき

## Do not read this when
- refactor state のデータ構造や対象選択を変更するときは、commons.runtime_refactor の実装を読む
- run の開始・join・abandon や一般的な worktree isolation の仕様を変更するときは、runtime_run 関連実装と対応する oracle 文書を読む
- file 単位の review agent parameter や change summary の Structured Output 定義だけを確認するときは、対応する parameter builder を直接読む

## hash
- 358f3992cf4e8276cb09e820463602d574beb705ddb8f1266bbd5ef5033a7e51
