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
- `cmoc run abandon` の CLI 実装。active editing run を特定し、実行中プロセスを停止したうえで run worktree・branch・state・process tracking を cleanup し、ライフサイクルレポートと結果を表示する。run の停止・cleanup 警告や失敗も扱う。

## Read this when
- `cmoc run abandon` の挙動、active run の停止処理、run worktree/branch の削除、cleanup 後の state 更新やレポート出力を変更・調査するとき。

## Do not read this when
- run の開始・join・完了など、abandon 以外の editing run lifecycle を変更・調査するとき。
- 共通の process tracking、active run 解決、worktree 操作の汎用実装そのものを確認するときは、対応する `commons` または runtime 実装を直接読む。

## hash
- ecf34cd6c11152d99d80cfef1f1267561bbff147d1d5d378646849dfda35fe25

# `join.py`

## Summary
- `cmoc run join` の active run 統合ライフサイクルを担当する。run branch と session branch の差分検査、merge、INDEX.md conflict の解決、post-join state 同期、report 保存、worktree・branch cleanup、および失敗時 rollback/error 化を扱う。run join の処理全体を確認する入口であり、個別の git・state・report helper の実装そのものを調べる対象ではない。

## Read this when
- `cmoc run join` の成功・失敗時の制御フローを調査または変更するとき
- run branch の想定外差分、merge conflict、`--force-resolve` の挙動を確認するとき
- post-join hook、state 同期、lifecycle report、run 資源 cleanup の連携を確認するとき
- merge または post-join 処理の失敗後に session を復元して error state にする挙動を確認するとき

## Do not read this when
- run join 以外のサブコマンドのライフサイクルだけを調べるとき
- git 操作、state 操作、process tracking、report 出力の共通実装だけを調べるときは、それぞれの helper module を直接読む
- join の利用者向け仕様や state の正本定義を確認するときは、対応する oracle doc を先に読む

## hash
- 7df92d2ceb682e728f9430beec54b772292d83a7d9d6df570b62cd52f276b8a8

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
