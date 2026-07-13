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
- `cmoc review oracle` の実行入口で、CLI runtime 経由の起動、active session branch の検査、clean worktree 確認、isolated review worktree の作成と削除、review branch の必要時 merge、所見レポート出力までを一連で扱う。
- `_require_clean_worktree` は review 実行前提の git 未コミット差分チェックにだけ使う。対象選定は `review_targets`、所見ループは `review_loop`、INDEX.md 反映と merge は `review_index`、レポート描画は `review_report` に分かれているので、このファイルは全体制御の流れを追う入口として読む。

## Read this when
- `cmoc review oracle` の実行フロー全体を確認したいとき。
- isolated review worktree の作成・削除、review branch の merge 条件、レポート出力までの制御を追いたいとき。
- review 実行の前提条件として、active session branch かどうか、git 未コミット差分がないかを確認したいとき。
- 対象 oracle の列挙や所見処理そのものではなく、それらをどう組み合わせて実行しているかを見たいとき。

## Do not read this when
- review 対象 oracle file の選定規則だけを知りたいときは `review_targets` を読む。
- 所見の列挙・整理・擁護・反証の処理本体を追いたいときは `review_loop` 配下を読む。
- review branch の INDEX.md 反映や merge 失敗時の競合解決だけを確認したいときは `review_index` を読む。
- レポートの Markdown 形式や集計表示だけを確認したいときは `review_report` を読む。
- このサブコマンドの CLI 登録や引数定義だけを確認したいときは、より上位の CLI 構成側を見る。

## hash
- 3fe07833192e4c4b6893405f70bfcd8b2ac0f6d2b7838a6b3cc5e370b5b9fb61
