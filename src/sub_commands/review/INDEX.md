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
- review oracle コマンドの実行入口であり、active session branch 上の clean な worktree を前提に、isolated review worktree を作成して oracle review を実行し、INDEX 変更の commit/merge、後片付け、report 出力までを統括する。
- review 対象列挙、review loop、report 描画・保存、review branch の merge/conflict 処理は下位モジュールから再公開し、このファイル自体は CLI runtime と一連の orchestration を束ねる位置にある。

## Read this when
- review oracle サブコマンドの全体フロー、実行前条件、run worktree の作成・削除、review branch の生成・merge、report 出力の制御を確認または変更したいとき。
- review oracle 関連 helper の公開入口や、どの下位モジュールが target 列挙・loop・report・index commit/merge を担当しているかを把握したいとき。
- active session branch 以外での拒否、clean worktree 要求、cmoc ignore 確保、失敗時にも report を書く挙動に関わる変更を行うとき。

## Do not read this when
- 個別 oracle file の列挙条件や scope 解釈だけを確認したい場合は、review target 列挙を担当する下位モジュールを直接読む方がよい。
- findings の生成手順や Codex review loop の詳細だけを確認したい場合は、review loop を担当する下位モジュールを直接読む方がよい。
- report の markdown 表現、section 描画、保存内容だけを確認したい場合は、review report を担当する下位モジュールを直接読む方がよい。

## hash
- 968833adfb39a8697ddebcdb1cb2c9816d6cff18420f2e9033674cd6f17d4f63
