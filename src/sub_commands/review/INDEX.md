# `__init__.py`

## Summary
- review 系サブコマンド群の package 境界を示す最小の package 初期化モジュール。
- 具体的な処理や公開 API は持たず、この階層が review 系サブコマンドのまとまりであることだけを表す。

## Read this when
- review 系サブコマンド群の package 境界そのものを確認したいとき。
- この階層が review 系サブコマンド用の Python package として扱われる根拠を確認したいとき。

## Do not read this when
- review 系サブコマンドの具体的な CLI 挙動、引数、出力、制御フローを調べたいとき。
- review 系サブコマンド内の個別機能や実装詳細を調べたいとき。
- package 初期化時の import、副作用、公開シンボルを調べたいとき。ただし現在内容からはそのような責務は読み取れない。

## hash
- 6eae64139b4951465b5b7ea5834aa77b1eeeaf892115aeaac7cbf14deb7ea1e2

# `oracle.py`

## Summary
- active session branch 上で oracle review を実行する CLI 実装の入口。preflight、session/state 検証、clean worktree 確認、isolated review worktree 作成、対象 oracle file 列挙、review loop 実行、INDEX 変更の commit/merge、worktree/branch 後片付け、report 出力までの制御フローを束ねる。
- review 対象列挙、review loop、report 描画、INDEX merge/conflict 処理などの個別責務は下位 module へ委譲し、この対象はそれらを CLI 実行単位として接続する orchestration 層である。

## Read this when
- review oracle サブコマンドの実行順序、session branch 制約、clean worktree 要件、run worktree の作成・削除、review branch の merge 条件、失敗時 report 出力の扱いを確認または変更したいとき。
- review oracle がどの helper module を呼び出し、対象列挙から findings 生成、INDEX 変更反映、report 書き込みまでをどう接続しているかを追いたいとき。
- review oracle 実行時の公開入口や import/export される review 関連 API の集約点を確認したいとき。

## Do not read this when
- oracle file の列挙条件や scope ごとの対象選定だけを変更したいときは、対象列挙を担う module を直接読む。
- review loop 内で Codex に渡す prompt、finding の merge 操作、反復制御だけを扱うときは、review loop を担う module を直接読む。
- report の本文構成、finding section の描画、report path の決定だけを扱うときは、report 生成を担う module を直接読む。
- INDEX 変更の commit、review branch merge、conflict 解決、status path 取得だけを扱うときは、INDEX 統合処理を担う module を直接読む。

## hash
- 126e80a595c4eb9b059f539a8c38eab361dbe838dbfb24a31479464eb24bb50d
