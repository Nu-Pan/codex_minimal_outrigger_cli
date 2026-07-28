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
- `cmoc run abandon` の実装。active editing run を特定し、状態に応じて実行中プロセスや Codex 子プロセスを停止したうえで、run worktree・branch・state・process tracking を cleanup し、lifecycle report と結果を出力する。run の停止処理、worktree/branch 削除処理の内部入口でもある。

## Read this when
- `cmoc run abandon` の挙動、active run の破棄、run 状態別の process 停止、worktree/branch cleanup、abandon report または CLI 出力を変更・調査するとき。

## Do not read this when
- `run abandon` 以外のサブコマンドの一般的な lifecycle 処理だけを調査するとき。process tracking や run lifecycle の共通仕様・共通 helper の詳細を確認する場合は、直接それらの実装または対応する oracle file を読む。

## hash
- 3329cf984cfdd1188cf7e00b65d12230cd27e50375805b10c75f4a5fc117d362

# `join.py`

## Summary
- `cmoc run join` の workload 非依存 merge lifecycle を実装する。active run の差分検査、merge、INDEX.md conflict 解決、post-join hook、state 同期、report 保存、failure rollback、worktree・branch cleanup を一つの lifecycle として扱う。

## Read this when
- `cmoc run join` の動作、merge 前後の差分検査、`--force-resolve`、post-join state 同期、report、cleanup、失敗時の error state と rollback を変更・調査するとき。
- run branch と session branch の merge conflict、想定外差分、run process tracking、merge 済み run の資源削除を確認するとき。

## Do not read this when
- workload 固有の apply・refactor 処理そのものを変更するとき。
- run の開始・実行・abandon など、join lifecycle に直接関係しない処理を変更するときは、対応する専用実装を先に確認する。

## hash
- 91adee51e4d259a0b72b2c9bfae089c0fb9e2c773d025782b56fa501a5123aa9

# `lifecycle.py`

## Summary
- editing run 共通 helper の旧 import path を維持する互換 shim。実体は commons.runtime_run_lifecycle にあり、関連する型・ライフサイクル操作を再公開する。

## Read this when
- editing run のライフサイクル処理や旧 import path との互換性を確認・変更するとき。

## Do not read this when
- 共通ライフサイクル処理そのものを実装・変更する場合は、commons 側の canonical 実装を直接読むとよい。

## hash
- 3de456333531bc878de445ccbaf683410ad0990c75f16028b6bcab36ac7d5939

# `report.py`

## Summary
- editing run report writer の旧 import path を維持する薄い互換 shim。共通実装を再公開し、対応する INDEX entry は互換性が不要になった時点で削除対象となる。

## Read this when
- 旧 import path から run report writer を利用するコードの互換性や移行を確認するとき。
- fork report または lifecycle report の writer の参照先を確認するとき。

## Do not read this when
- canonical な report writer の実装詳細を確認したいときは、commons 側の実装を直接読む。
- run サブコマンドの実行フローや report 生成仕様を調査するとき。

## hash
- 633bf26dd4d3ab3155dcddf2eb46c2b39b1617fa4914e30aeeca6e9cc0975d48
