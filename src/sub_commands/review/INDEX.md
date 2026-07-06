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
- review oracle サブコマンドの実行入口。active session branch と clean worktree を前提に、isolated review worktree を作成して oracle review 対象列挙、Codex review loop、INDEX 変更の commit/merge、report 出力、作業用 worktree/branch の後片付けまでを統括する。
- review oracle の個別処理は対象列挙、review loop、INDEX merge、report 生成の各下位モジュールへ委譲し、このファイルは CLI runtime との接続、session 状態検証、review 用 branch/worktree のライフサイクル管理を担う。

## Read this when
- review oracle サブコマンド全体の実行順序、事前条件、失敗時 report 出力、review 用 branch/worktree の作成・削除タイミングを確認したいとき。
- oracle review の対象列挙、review loop、INDEX 変更 merge、report 生成がどの順で呼ばれ、どの値を受け渡すかを追いたいとき。
- review oracle が active session branch 以外や dirty worktree で停止する条件、または一時 review branch を session branch に merge する条件を確認したいとき。

## Do not read this when
- oracle file の列挙条件や scope ごとの対象選択だけを確認したい場合は、対象列挙を担う下位モジュールを読む。
- Codex に渡す review prompt、finding の検出・merge 操作、review loop の詳細だけを確認したい場合は、review loop 側の下位モジュールを読む。
- review report の本文整形、finding section、report file の書き込み形式だけを確認したい場合は、report 生成側の下位モジュールを読む。

## hash
- f9020ad738275494fed154893d216a8081b977211c2f438f1627200c490de69b
