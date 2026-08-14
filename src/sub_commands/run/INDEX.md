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
- `cmoc run abandon` の workload 非依存 cleanup lifecycle を実装する。active editing run の状態を解決し、必要に応じて実行中プロセスや残存 Codex child を停止したうえで、run worktree・branch・state・process tracking を整理し、lifecycle report と terminal result を返す。
- run の状態別に process 停止処理を分け、worktree の削除に失敗した場合は branch を保持して再試行可能にする。cleanup 完了後にのみ state を ready へ更新し、停止・削除結果と警告を報告する。

## Read this when
- `cmoc run abandon` の停止・破棄処理、active run の cleanup 順序、run worktree や branch の削除挙動を確認または変更するとき。
- running・error・joinable の各 run state における process cleanup と、cleanup 失敗時の再実行可能性を確認するとき。
- abandon 後の state、process tracking、lifecycle report、terminal result の確定条件を確認するとき。

## Do not read this when
- run の開始・join・通常の編集処理を確認する場合は、この cleanup 実装ではなく、それぞれの subcommand や lifecycle 仕様を直接読む。
- worktree・branch・process 操作の共通実装そのものを変更または調査する場合は、この orchestration entry ではなく、インポート先の runtime 共通モジュールを直接読む。

## hash
- 89457453bb7165d74ec629a58c86070010f6e03eda2da15b2534407432f00a4a

# `join.py`

## Summary
- `cmoc run join` の workload 非依存な merge lifecycle を実装する入口。active run の検証、run branch の merge、INDEX 再生成、post-join の state 同期、lifecycle report、worktree・branch cleanup を一続きで扱う。merge conflict、想定外差分、post-join failure、cleanup pending/error state への rollback と再試行可能性もここで確認する。

## Read this when
- `cmoc run join` の実装を変更・レビューするとき
- active editing run の merge、post-join hook、refactor state 同期、report、cleanup の挙動を確認するとき
- run branch と session branch の差分検査、`--force-resolve`、INDEX.md conflict、失敗時 rollback、cleanup pending/error state を追跡するとき

## Do not read this when
- run の開始・abandon など、join lifecycle 以外のサブコマンドだけを確認するとき
- workload 固有の処理を確認するとき
- join から呼び出される共通 runtime helper の仕様を直接確認するとき

## hash
- 08f66cf28722fe9a1c3924f8407492114bab780c34c9ed8af8d2a1248e630b44

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
