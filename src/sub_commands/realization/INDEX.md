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
- realization の apply 処理に関する workload を扱うモジュール群。apply workload の実装を確認する入口となる。
- `cmoc realization apply fork` の実行本体を担い、realization apply agent の差分追従処理を run として管理する。oracle diff の構築、agent 実行、差分検査、INDEX 更新を含む commit、run state 更新、fork report 保存までを扱う。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- `cmoc realization apply fork` の実行フロー、成功時の commit・joinable 化、失敗時の rollback・error report を調査または変更するとき。
- realization apply agent の差分範囲検査、Codex child process の停止、run state の復旧処理を確認するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- realization apply agent が生成する prompt や launch parameter の詳細だけを確認したいとき。
- run の共通状態管理・差分操作・process tracking の実装だけを確認したいとき。
- 別の realization apply サブコマンドや fork report の一般仕様だけを確認したいとき。

## hash
- 76e687491af355d531d50d3ea40b5c2def36d0b4a2bceb7276e5095f7a6a260f

# `refactor`

## Summary
- realization のリファクタリング処理を扱うパッケージで、関連する fork 実行ライフサイクルやリファクタリング処理への入口を提供する。

## Read this when
- realization のリファクタリング実行フロー、対象選択、agent call 後の差分検証、state 更新、commit、完了判定を確認するとき
- 中断・エラー時の cleanup、unresolved finding、fork report の保存と run state 遷移を確認するとき

## Do not read this when
- 単一ファイルの調査・修正 agent parameter 生成だけを確認するとき
- 変更概要の Structured Output 仕様だけを確認するとき
- 一般的な editing run のライフサイクルや共通 Git 差分処理だけを確認するとき

## hash
- 3a2e0746d40b9164ab454388960e45ebb640143c712ebc343f4c47e7f5635478
