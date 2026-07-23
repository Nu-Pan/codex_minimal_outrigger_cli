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
- `cmoc run abandon` の実行処理を担当する。active editing run を特定し、必要に応じて実行中プロセスを停止したうえで、run worktree と branch を削除し、状態と lifecycle report を更新して結果を表示する。

## Read this when
- `cmoc run abandon` の cleanup 処理、実行中 run の停止、run worktree・branch の破棄、abandon 後の状態更新や結果表示を変更・調査するとき。

## Do not read this when
- run の開始・join・完了など、abandon 以外の lifecycle 処理だけを変更・調査するとき。
- workload 自体の実行処理、doctor preprocess の詳細、プロセス停止や lifecycle report の共通実装を直接確認するとき。

## hash
- 524b743af9433d81d2887928d0b52f21d7ed8935add1c15e82d362c153534edf

# `join.py`

## Summary
- `cmoc run join` の workload 非依存な merge lifecycle を実装する。active run の検証、run branch の merge、INDEX.md 競合の限定的解決、post-join hook と state 同期、report 保存、worktree・branch cleanup、失敗時の error state 化を扱う。

## Read this when
- `cmoc run join` の merge、force-resolve、post-join 処理、state 同期、cleanup、失敗復旧の挙動を変更・調査するとき。
- run branch と session branch の想定外差分、INDEX.md 以外の merge conflict、run lifecycle report の生成を確認するとき。

## Do not read this when
- run の開始・実行・abandon など join 以外の lifecycle を変更するときは、それぞれの専用実装を直接読む。
- workload 固有の merge 処理や report 内容だけを変更する場合は、関連する workload・report 実装を直接確認する。

## hash
- 49c123afc8cee23b47da533f483716162dacb72c5cf6e936526112c613410efc

# `lifecycle.py`

## Summary
- editing run の開始・active run 解決・状態遷移・worktree 管理を共通化するライフサイクル処理を提供する。
- work unit の rollback/commit、INDEX.md 更新、Git 差分・変更 path の抽出、oracle・agent 想定外 path の検査も扱う。
- run lifecycle や変更 path の検査を実装・修正・調査する際の共通処理への入口となる。

## Read this when
- editing run の開始、joinable/error 遷移、session/run state の検証を変更または調査するとき
- run worktree・branch の生成、解決、削除や process id 管理の挙動を確認するとき
- work unit の commit/rollback、INDEX 更新、Git rename/copy を含む差分 path 処理を変更するとき
- agent・run・session が変更できる path の許可検査や oracle diff 抽出を確認するとき

## Do not read this when
- 個別の editing run サブコマンドの利用者向け仕様だけを確認したいときは、対応する app_spec を直接読む
- session state のデータ構造や永続化形式そのものを変更・調査するときは、runtime_state の実装を直接読む
- INDEX.md の生成アルゴリズム自体を変更するときは、commons.indexing の実装を直接読む

## hash
- f521916f0ab09518498271c81e47c2e667aab9b605435002a9c8ba871b9d8a97

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
