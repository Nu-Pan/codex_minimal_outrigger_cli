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
- 明示的な join を必要とする editing run のライフサイクル共通処理を提供する。session の事前条件確認、run worktree・branch の作成と state 管理、active run 解決、state 更新、差分の commit・rollback、INDEX 更新、Git tree change の解析、許可外 path の検出を扱う。run 関連の各 workload 実装から利用される共通基盤である。

## Read this when
- editing run の開始・終了・joinable/error 遷移、session state と run worktree の整合性検証を変更または調査するとき
- run worktree の commit、rollback、INDEX 更新、Git rename/copy を含む差分解析を変更または調査するとき
- oracle・realization・INDEX・memo の path 制約や workload の変更許可判定を変更または調査するとき

## Do not read this when
- 個別の editing run workload の業務処理だけを変更・調査する場合
- session state のデータ構造や永続化形式だけを確認する場合は、まず runtime_state の実装を読む
- CLI のサブコマンド入口や利用者向け引数の挙動だけを確認する場合は、対応する command 実装を直接読む

## hash
- 1344955ed33a92f1dbf8f4fbfb008bf3b8e3ba77f5cbdb92a51db02e2e7a5aa3

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
