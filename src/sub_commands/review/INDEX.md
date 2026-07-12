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
- `review/oracle.py` は、現在の session branch に対して review oracle を isolated review worktree 上で実行し、所見収集・レビュー用 index の反映・必要なら review branch の merge・レポート出力までをまとめて扱う実行入口です。

## Read this when
- `review oracle` CLI の実行フロー、review worktree の作成/削除、review branch の merge 条件、所見レポートの出力経路を確認したいとき。
- review 対象の oracle ファイル列挙や scope に応じた対象選択、レビュー処理ループ、失敗時のレポート生成を追いたいとき。

## Do not read this when
- 通常の subcommand 実行基盤や汎用 runtime 操作だけを追いたいときは、より下位の runtime / helper 側を読むべきです。
- oracle 対象の列挙規則やレビュー index の衝突解決だけを確認したいときは、この入口より対応する helper モジュールを直接読むべきです。

## hash
- a386908f0bf6383e71e8d8e418272efa36acadbcb9dc7958d48680b0f62849e8
