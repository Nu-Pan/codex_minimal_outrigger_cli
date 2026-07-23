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
- `cmoc run join` の workload 非依存な merge lifecycle を実装する。active run と session の差分・競合を検査し、run branch の merge、post-join hook、refactor state 同期、結果 report 保存、worktree・branch cleanup までを一連の処理として扱う。

## Read this when
- `cmoc run join` の merge、force-resolve、INDEX.md 競合処理、post-join 失敗時の復旧を変更・調査するとき。
- run lifecycle の error state、process 停止、report 保存、join 後 cleanup の挙動を確認するとき。

## Do not read this when
- run の開始・編集・abandon など、join lifecycle 以外の処理だけを変更・調査するとき。
- workload 固有の実装や一般的な run lifecycle helper の詳細を直接確認する必要があるとき。

## hash
- d46de047a915be589a45352ee72bf8788a1b7ac5f0d09bd2b4afac43dbe524c7

# `lifecycle.py`

## Summary
- editing run の開始・解決・状態更新、worktree 差分の commit/rollback、INDEX 更新、Git 変更 path の検査を担う共通ライフサイクル処理。run/session state、branch、worktree の整合性確認と、oracle・realization・INDEX の変更許可判定を提供する。

## Read this when
- editing run の開始、active run の解決、joinable/error への状態遷移を変更・調査するとき。
- run worktree の作成・削除、work unit の commit/rollback、INDEX 更新 commit の挙動を確認するとき。
- Git の rename/copy を含む変更列挙、agent/run/session の想定外 path 検出、oracle diff の扱いを変更・調査するとき。

## Do not read this when
- 個別の editing run サブコマンドの業務処理だけを確認する場合。
- state schema、Git 実行、path 解決、INDEX 生成の詳細実装を直接確認する場合は、それぞれの commons モジュールを読む。

## hash
- e8a5a8b7f53d61a24d8d87c004ea6f5f36391d070903c1e303ecec7cb28ff02e

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
