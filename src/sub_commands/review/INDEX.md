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
- review oracle サブコマンドの CLI 実行入口と orchestration を担う。active session branch の clean 状態を検証し、隔離 review worktree で oracle 対象を評価し、INDEX 変更の統合と review report 出力までを管理する。
- review oracle の中断・失敗時に、確定済み所見やエラーをレポートへ記録する。所見の検出・対象列挙・INDEX 変更・レポート描画の詳細実装は、インポート先の各モジュールが直接の入口になる。

## Read this when
- review oracle CLI の実行ライフサイクル、active session branch の前提、隔離 worktree の作成・破棄、review branch の統合を変更または調査するとき
- review oracle の中断時・例外時のレポート生成や、未コミット差分の検証を変更または調査するとき

## Do not read this when
- 所見検出ループの詳細を変更または調査するときは review_loop の実装を直接読む
- oracle 対象ファイルの列挙規則を変更または調査するときは review_targets の実装を直接読む
- review report の表示形式やファイル書き込みを変更または調査するときは review_report の実装を直接読む
- review branch の INDEX 変更の commit・merge・conflict 解決を変更または調査するときは review_index の実装を直接読む

## hash
- 801c1e124c658f8fafcd36eb37b5ca8faccd2e35c3b6ca08092eee07eb18ac16
