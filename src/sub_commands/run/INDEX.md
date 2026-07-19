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
- `cmoc run abandon` の実装。active editing run を特定し、実行中プロセスを停止したうえで run worktree と branch を削除し、状態・process tracking・lifecycle report を更新する。cleanup 結果と警告を CLI に表示する。

## Read this when
- `cmoc run abandon` の cleanup lifecycle、実行中 run の停止、run worktree／branch の破棄、abandon 後の状態更新やレポート出力を変更・調査するとき。

## Do not read this when
- run の開始・join・完了など abandon 以外の lifecycle を変更するときは、各 lifecycle 実装を直接読む。
- workload 固有の処理や一般的な run 状態解決の仕様だけを調査するときは、対応する lifecycle・runtime モジュールを直接読む。

## hash
- cc9af9effc51e1e2874b0175611f454c70ad1f35b7b7edb468818c3ee3788f5a

# `join.py`

## Summary
- `cmoc run join` の実行本体を担い、active editing run の検査、run branch の session branch への merge、INDEX.md 限定の競合解決、post-join 処理、state 同期、report 保存、worktree・branch cleanup を管理する。join 前後の異常時には run を error 状態へ記録し、必要に応じて process 停止や force resolve を行う。

## Read this when
- `cmoc run join` の merge lifecycle、force resolve、post-join hook、run resource cleanup の挙動を変更・調査するとき。
- run branch と session branch の差分検査、INDEX.md 競合の扱い、join failure report、error run の復旧を確認するとき。

## Do not read this when
- join lifecycle の共通 context 解決、差分判定、commit、index refresh の詳細だけを確認したいときは、参照先の `sub_commands.run.lifecycle` を直接読む。
- lifecycle report の出力形式だけを確認したいときは、`sub_commands.run.report` を直接読む。
- run process の PID 管理やロックの実装だけを確認したいときは、`commons.runtime_run` を直接読む。

## hash
- d113167ba8a8481769d8f7e3568a9bba4b415820d0b524303b7a988b448c72d2

# `lifecycle.py`

## Summary
- editing run の開始・解決・状態更新を担う共通ライフサイクル処理。session/run の事前条件検査、専用 branch・worktree の作成と後始末、state file の更新を扱う。
- worktree 差分の rollback・commit、INDEX.md 更新、Git tree change の列挙、agent・run・session が変更可能な path の検証、oracle diff の抽出も提供する。
- editing run の各サブコマンドでライフサイクル管理、worktree commit、変更 path の許可判定、INDEX 更新の実装を確認する入口。

## Read this when
- editing run の開始、active run の解決、joinable/error state への遷移を変更または調査するとき
- run worktree や session worktree の作成・削除、rollback・commit、INDEX 更新の挙動を確認するとき
- Git の rename/copy を含む差分解析、oracle・realization・refactor state の変更許可判定を確認するとき

## Do not read this when
- 特定の editing run サブコマンド固有の workload 処理だけを変更または調査するとき
- session state のデータ構造や永続化形式そのものを確認するときは、runtime state の実装を直接読むとき
- 一般的な Git 操作や INDEX 生成の詳細だけを確認し、この共通 lifecycle 処理を利用していないとき

## hash
- 11524e925bbf5c52e99d1ef92c463ee25d05244e7f42a9d18658ca0122ca75c8

# `report.py`

## Summary
- editing run の fork report と lifecycle report を Markdown + YAML Front Matter として保存するモジュール。共通メタデータ、完了理由、変更パス、警告、詳細項目を組み立て、レポートの出力先・ファイル名・YAML scalar 表現を管理する。

## Read this when
- run の fork、join、abandon に伴うレポート生成や保存先を変更するとき
- レポートの Front Matter 項目、本文構成、警告・変更パスの出力形式を確認するとき
- レポート値の YAML scalar 変換や生成時刻の扱いを変更するとき

## Do not read this when
- run のライフサイクル状態遷移や EditingRunContext 自体の仕様を確認したいときは、ライフサイクル実装を直接読む
- レポート生成後の CLI 表示やレポートの利用側だけを変更するときは、対応する呼び出し元・利用側を直接読む
- 一般的なパス解決や時刻生成の仕様だけを確認するときは、commons.runtime_paths を直接読む

## hash
- 688ec81dbc99f58cbc14cc334ffdf3f86001b8903469d479c200d709621d158a
