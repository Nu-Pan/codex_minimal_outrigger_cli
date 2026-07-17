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
- oracle review サブコマンドの CLI 実行入口と本体処理を担う実装。active session branch の検証、隔離 review worktree の作成・レビュー実行・結果マージ・後始末・レポート出力を統括し、公開される review 関連 API も再エクスポートする。

## Read this when
- oracle review の起動条件、session branch 検証、隔離 worktree のライフサイクルを確認・変更するとき
- review loop、finding のマージ、レビュー結果レポートへの接続箇所を確認するとき
- oracle review の中断・例外・未コミット差分時の挙動を確認するとき

## Do not read this when
- review の対象列挙、ループ内部の判定、finding 操作の詳細だけを変更するときは、対応する review_targets または review_loop の実装を直接読む
- レビュー結果の表示形式やレポート生成だけを変更するときは、review_report の実装を直接読む
- INDEX 更新処理だけを変更するときは、review_index の実装を直接読む

## hash
- a81d54d64504704d5522ca4e7db7cf6c854416ba2d596e8ffb76204997e09889
