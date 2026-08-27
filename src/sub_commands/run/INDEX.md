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
- `cmoc run join` の workload 非依存な merge lifecycle を一括して担う realization file。active run の検証、差分検査、merge、INDEX 再生成、post-join state 同期、report 保存、失敗時 rollback、worktree・branch cleanup までを扱う。
- joinable または error 状態の active run を session branch に統合し、想定外差分や merge conflict を検出する。`--force-resolve` による run branch 側の想定外差分の復元、および INDEX.md だけの conflict の再生成もここで処理する。
- merge 後の refactor state 同期、primary report と lifecycle report の更新、cleanup 失敗時の error state 保持を含み、run join の成功・失敗・cleanup pending に関する状態遷移を確認する入口である。

## Read this when
- `cmoc run join` の実装、merge 前後の差分検査、`--force-resolve` の挙動を確認するとき
- run join 後の INDEX 再生成、post-join hook、refactor state 同期、report 保存を調査するとき
- merge conflict、post-join failure、rollback、error state、worktree・branch cleanup の不変条件を確認するとき

## Do not read this when
- workload 固有の編集・apply・refactor 処理そのものを確認するときは、対応する workload 固有の realization file を直接読む
- run join の正本仕様や状態遷移の定義を確認するときは、対応する oracle の仕様書を先に読む
- 一般的な Git 操作や共通 runtime helper の実装だけを確認するときは、import 先の共通 runtime file を直接読む

## hash
- 23788546f2780854b953b77a98c9a713e695c501a3cd77c9e5a6f3b4bd10dd93

# `lifecycle.py`

## Summary
- editing run のライフサイクル処理について、旧 `src.sub_commands.run.lifecycle` import path との互換性を保つための薄い委譲層。実体は `commons.runtime_run_lifecycle` にあり、このファイルは公開されていた helper と `unexpected_session_paths` の旧呼び出し形を再公開する。
- 旧 import path の互換性、既存利用者の移行、または shim の削除可否を確認するときの入口であり、ライフサイクル処理そのものを変更・理解する場合は canonical 実装へ進む。

## Read this when
- 旧 `src.sub_commands.run.lifecycle` を参照するコードの互換性を確認するとき
- 旧 import path から commons 側への移行や、この shim の削除条件を検討するとき

## Do not read this when
- editing run ライフサイクル処理の本体や挙動を調査・変更するとき
- canonical helper の実装を直接確認できる場合
- 旧 import path との互換性が関係しない作業

## hash
- afea30cef15ff82115474870214a86f23715b484f0a0978114eab5bd12af41c6

# `report.py`

## Summary
- 旧 import path から利用される editing run report writer の互換 shim。
- 共通処理の canonical 実装を再公開し、旧利用者が commons 側へ移行するまで互換性を保つ。
- 旧 import path の互換性や shim の削除条件を確認する際の入口であり、実装本体は commons 側にある。

## Read this when
- 旧 import path から run report writer を利用するコードの互換性を確認するとき。
- fork report または lifecycle report の writer の公開元を追跡するとき。
- commons 側への移行完了後に、この shim と対応する INDEX entry の削除可否を判断するとき。

## Do not read this when
- fork report または lifecycle report の具体的な実装内容を確認したいとき。
- 共通処理の挙動を調査・変更するとき。
- 旧 import path の互換性に関係しない run サブコマンドの処理を確認するとき。

## hash
- 79d887b69a865829ca361e6b448106bb8eb6e3635afa5c7300dc31a99beb8385
