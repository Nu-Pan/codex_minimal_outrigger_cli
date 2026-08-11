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
- `cmoc run abandon` の CLI 実装。active editing run を特定し、状態に応じて追跡プロセスや Codex 子プロセスを停止した後、run worktree・branch・state・process tracking を cleanup し、ライフサイクルレポートと結果を表示する。cleanup 失敗時は資源を保持してエラーにする。

## Read this when
- `cmoc run abandon` の停止・破棄処理を変更または調査するとき
- active run の running・error・joinable 各状態における process 停止や cleanup 挙動を確認するとき
- run worktree、branch、state、process tracking、ライフサイクルレポートの連携を追跡するとき

## Do not read this when
- `cmoc run` の通常作成・編集・join 処理だけを調査するとき
- abandon の共通 run 状態解決や process 操作の詳細を確認したい場合は、先にそれぞれの共通 runtime module を読むとき

## hash
- fb8470db00c117fcd931bf2bb8a8da7731594cf84b6c2b24b54a3b0eb11be56d

# `join.py`

## Summary
- `cmoc run join` の workload 非依存な active editing run 終了処理を担う。
- run/session worktree の状態と差分を検査し、必要に応じて unexpected run paths の force-resolve、run branch の merge、INDEX.md conflict の再生成を行う。
- post-join hook、refactor state 同期、lifecycle report 保存、run worktree と branch の cleanup までを一続きの lifecycle として処理する。
- merge、post-join、report、cleanup の失敗時には session の復旧、error state、再試行可能な run resource 保持を行う。

## Read this when
- `cmoc run join` の成功経路または failure rollback を変更・調査するとき。
- run branch と session branch の差分検査、想定外差分の force-resolve、merge conflict の扱いを確認するとき。
- post-join の INDEX.md 再生成、refactor state 同期、lifecycle report、run resource cleanup の責務を確認するとき。

## Do not read this when
- workload 固有の run 処理や、join 前の run 作成・編集処理を調べるとき。
- 通常の state 読み書き、Git 共通操作、report 共通形式の詳細だけを確認する場合は、それぞれの共通実装を直接読む。
- INDEX.md の routing 規則や生成アルゴリズムそのものを調べる場合は、この join lifecycle 実装を入口にしない。

## hash
- 78e84f3cfaa4b7c7d3ed473a295a8e3d671276dfd3f187a60f1ea4ce941cd158

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
