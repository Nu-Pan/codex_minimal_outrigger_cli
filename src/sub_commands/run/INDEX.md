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
- `cmoc run abandon` の active editing run を停止し、run worktree・run branch・state・process tracking を cleanup して ready 状態へ戻す lifecycle 実装。running、error、joinable の各状態に応じた process 停止と、worktree・branch の削除結果を primary report および lifecycle report に反映する。
- cleanup 対象が残った場合は branch を保持して再試行可能にし、失敗理由と警告を返す。run abandon の停止処理、cleanup、state 更新、最終 terminal result の流れを確認する入口。

## Read this when
- `cmoc run abandon` の実装経路、active run の停止方法、run 資源の cleanup 順序を調べるとき。
- running・error・joinable 状態ごとの process cleanup や、worktree・branch 削除失敗時の挙動を確認するとき。
- abandon 完了時の state、process tracking、primary report、lifecycle report の更新内容を確認するとき。

## Do not read this when
- `run abandon` の正本仕様や利用者向け仕様を確認する場合は、対応する app_spec・lifecycle 仕様を直接読むとき。
- run の作成、join、編集、merge など abandon 以外の lifecycle を調べる場合は、各サブコマンドの実装へ直接進むとき。
- worktree・branch の一般的な git 操作だけを確認する場合は、共通 runtime helper を直接読むとき。

## hash
- 9924a70203bbb39f9d7ac008a2285a850c13c5824d8ddf7b23a4866124ae71f1

# `join.py`

## Summary
- `cmoc run join` の active editing run を session branch に統合する一連の lifecycle を担う実装。join 前の doctor/refactor state 同期、run/session 差分と想定外変更の検査、force-resolve、merge conflict 処理、post-join の INDEX 再生成・state 同期・report 保存、失敗時 rollback/error 化、worktree と branch の cleanup を同じ不変条件のもとで扱う。この挙動や cleanup pending/error rollback を確認・変更するときの入口であり、個別の共通 Git 操作や report/state API の詳細だけを調べる場合はそれらの実装へ直接進む。

## Read this when
- `cmoc run join` の成功・失敗・再実行・`--force-resolve` の挙動を調査または変更するとき
- run branch の merge、INDEX.md conflict、post-join hook、refactor state 同期、lifecycle report、run resource cleanup の連鎖を確認するとき
- merge 後の rollback、error state、cleanup pending、abandon への引き継ぎ条件を確認するとき

## Do not read this when
- join lifecycle ではなく、run の開始・編集・abandon や active run 解決そのものを調べるとき
- Git 操作、state 永続化、process tracking、report 生成などの共通部品の仕様や実装だけを調べるとき
- INDEX.md の生成規則そのものや、join 以外の workload 固有 merge 処理を調べるとき

## hash
- 7d5accc8d71b75a7087447e9ff66439faa2db0b6107ae0dbc91d7966072ebbf3

# `lifecycle.py`

## Summary
- editing run のライフサイクル共通 helper を旧 import path から利用するための互換 shim。canonical 実装を commons.runtime_run_lifecycle に委譲し、旧 API 名と unexpected_session_paths の base 省略呼び出しを維持する。

## Read this when
- editing run のライフサイクル処理を旧 import path から参照するコード、または旧 API の互換性を確認・変更するとき。

## Do not read this when
- canonical な共通ライフサイクル実装の仕様や挙動を確認したいときは、直接 commons.runtime_run_lifecycle を読む。
- 旧 import path の互換 shim が不要かどうかに関係しない、他の CLI サブコマンドやプロンプト構築処理を扱うとき。

## hash
- 954fbbb80608b1840a22577f281660a3fe0f0e491352e8ec5f3c1b363b67a6ad

# `report.py`

## Summary
- `editing run report writer` の旧 import path を維持する互換 shim。
- 実装本体は `commons` 側にあり、この対象は `write_fork_report` と `write_lifecycle_report` を再公開する入口として機能する。互換性が不要になった場合は、canonical 実装への移行完了を確認してからこの shim と対応する INDEX entry を削除する。

## Read this when
- 旧 import path から run report writer を利用するコードの互換性や移行状況を確認するとき
- fork report または lifecycle report の writer の公開入口を確認するとき
- commons 側への移行完了後に旧 shim の削除可否を判断するとき

## Do not read this when
- run report writer の処理内容や挙動を変更・確認するとき
- 旧 import path と無関係な CLI サブコマンドを調べるとき
- canonical 実装の詳細を直接確認するとき

## hash
- bf4c9d035df1891f3e41bc9589a9140a0e7711c31ea141e7229d0463574a8f56
