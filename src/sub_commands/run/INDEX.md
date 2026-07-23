# `__init__.py`

## Summary
- editing run の共通 lifecycle サブコマンドをまとめるパッケージの入口。関連する run サブコマンドの共通処理を確認する際に読む。

## Read this when
- editing run サブコマンドの共通 lifecycle や、その配下の実装を調査・変更するとき。

## Do not read this when
- editing run 以外のサブコマンドを扱うとき。具体的な処理の実装を確認する場合は、この入口ではなく配下の該当ファイルを直接読む。

## hash
- ee750515c16235f73dd57b6cd7864576f1957fe840d0ceb82b9658c56c959115

# `abandon.py`

## Summary
- `cmoc run abandon` の実行本体を担当する。active editing run を特定し、running 状態なら追跡プロセスを停止したうえで、run worktree・branch・state・process ID を cleanup し、ライフサイクルレポートと結果を表示する。run abandon の cleanup 挙動を確認する入口。

## Read this when
- `cmoc run abandon` の実装、active run の停止、worktree・branch・state の cleanup、abandon レポートや表示結果を調査・変更するとき。

## Do not read this when
- run の作成・開始・join・通常完了の処理を調べるとき。プロセス追跡やライフサイクルレポートの共通処理そのものを調べる場合は、対応する `commons` モジュールを直接読む。

## hash
- 5270f073a167a652b085c5c13b05e520fdc704e36d2f603e3fc03110e6a0674d

# `join.py`

## Summary
- `cmoc run join` の active run を session branch に統合する CLI 実装。merge 前の doctor 処理、差分検査、想定外変更の拒否または `--force-resolve` による復元、merge conflict 処理を担う。
- merge 後の post-join hook、INDEX と refactor state の同期、state・report の保存、run process tracking の削除、worktree と branch の cleanup、および失敗時の error state への復旧を一連の lifecycle として実装している。
- `run join` の挙動、merge・cleanup・失敗復旧・想定外差分・INDEX.md conflict の変更や調査を行う際の主要な入口である。

## Read this when
- `cmoc run join` の実装や active run の merge lifecycle を変更・調査するとき
- run branch と session branch の差分検査、`--force-resolve`、merge conflict の扱いを確認するとき
- post-join の state 同期、report 保存、process tracking、worktree・branch cleanup、失敗時復旧を確認するとき

## Do not read this when
- run の開始・実行・abandon など、join lifecycle 以外の処理だけを扱うとき
- 共通の run state、git 操作、report 生成の詳細だけを調べる場合は、直接それぞれの共通 runtime module を読むとき
- INDEX.md の生成・更新ロジック自体だけを調べるとき

## hash
- 765e0b05ef27b90e0ad42e701b9fee191738960f402109ea0639eb722624047a

# `lifecycle.py`

## Summary
- editing run のライフサイクル共通処理を旧 import path から利用できるようにする薄い互換 shim。実装本体は commons.runtime_run_lifecycle にあり、このファイルは公開対象の名前を再エクスポートする入口である。

## Read this when
- editing run lifecycle の旧 import path との互換性や、ここから再エクスポートされる実行状態・変更管理 API を確認するとき。

## Do not read this when
- 共通処理の実装詳細を確認したいときは、直接 commons.runtime_run_lifecycle を読む。run コマンド固有の処理や CLI 動作を調べるときは、対応する上位モジュールを読む。

## hash
- ac74f8c26aea9338a8142da59b7160da9c35f4dbaa8a5a97290d6743d6308ee7

# `report.py`

## Summary
- run report writer の旧 import path として、commons.runtime_run_report の fork/lifecycle レポート出力関数を再公開する薄い互換 shim。独自のレポート処理は持たず、canonical 実装への入口を提供する。

## Read this when
- run サブコマンドのレポート出力関数の旧 import path、互換性、または commons 側の canonical 実装への委譲関係を確認するとき。

## Do not read this when
- レポート出力の具体的な処理内容を確認するときは、直接 commons.runtime_run_report を読む。run レポート以外のサブコマンド実装を調査するとき。

## hash
- 0a058d7e3b3fd263920ff32392c54d0a4ce3509672ac59ce07a5e30f78e1aac7
