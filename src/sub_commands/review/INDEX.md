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
- review oracle サブコマンドの実行入口と本体を実装するモジュール。active session branch の検証、隔離 review worktree の作成、oracle 対象の列挙・レビュー実行、INDEX 変更のマージ、割り込み・例外処理、レビュー結果レポート出力までを統括する。review サブコマンドの oracle 実行フローや、関連する review_loop・review_index・review_report・review_targets への入口として読む。

## Read this when
- review oracle の CLI 実行フロー、worktree・branch のライフサイクル、レビュー対象選定、割り込み・例外時のレポート処理を変更または調査するとき
- review oracle が active session branch と clean worktree を要求する理由や、レビュー後の INDEX 変更マージ処理を確認するとき

## Do not read this when
- レビュー判定ループの詳細だけを変更・調査する場合は review_loop の実装を直接読む
- レビュー対象の列挙規則だけを確認する場合は review_targets を直接読む
- 所見レポートの形式だけを確認する場合は review_report を直接読む
- レビュー用 INDEX の commit・merge・conflict 解決だけを確認する場合は review_index を直接読む

## hash
- ddfea47ce6ecdf8719fd28931cc2d29a280000123696a9a3463d92c366f1df2c
