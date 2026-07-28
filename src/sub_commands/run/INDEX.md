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
- `cmoc run abandon` の実装入口。active editing run の process 停止、run worktree・branch の削除、state 更新、lifecycle report 出力と結果表示を担う。停止状態ごとの cleanup 分岐も含む。

## Read this when
- `cmoc run abandon` の挙動、active run の破棄、process・worktree・branch cleanup、abandon report を変更または調査するとき。

## Do not read this when
- run lifecycle の共通状態解決や process 操作の仕様・実装だけを確認するときは、対応する `commons` モジュールや oracle file を直接読む。
- `run abandon` 以外のサブコマンドの処理を変更または調査するとき。

## hash
- fbf50cc4db02d82f3f79ddd58554534d6a466073c443a973f47d9886e7f053e3

# `join.py`

## Summary
- `cmoc run join` の workload 非依存な merge lifecycle を担当する。active run の差分検査、session branch への merge、INDEX.md conflict の処理、post-join state 同期、report 保存、失敗時 rollback、run worktree・branch cleanup までを一続きで扱う。

## Read this when
- `cmoc run join` の実装や挙動を変更・調査するとき
- run branch と session branch の差分検査、merge conflict、force-resolve の処理を確認するとき
- post-join の state 同期、report、失敗時の error state・rollback、cleanup pending を確認するとき

## Do not read this when
- `run join` 以外の run lifecycle や workload 固有処理だけを変更・調査するとき
- run の開始・実行・abandon・status 表示の処理を直接確認したいとき
- 共通 runtime helper の詳細実装を確認する場合は、まず該当する共通モジュールを読むとき

## hash
- 79d4e6065b62a4a0a604d5350b8d82edcd1022f7cbae557409e4dd9672924430

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
