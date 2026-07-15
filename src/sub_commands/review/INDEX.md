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
- `review oracle` コマンドの実行全体を束ねる入口。実行前の前提確認、隔離 worktree の作成・削除、review ループの起動、結果レポートの出力までを扱う。

## Read this when
- `review oracle` の実行順序や失敗時の振る舞いを変えたいとき。
- session branch かどうかの判定、未コミット差分の拒否、interruption の扱いを確認したいとき。
- review 用 worktree のライフサイクルや、最終レポートに渡す実行結果の集約方法を見たいとき。

## Do not read this when
- 個別の oracle 対象の列挙条件を見たいときは、対象選択側の実装を直接読む。
- index 差分の解決や merge の詳細を変えたいときは、review index 側の実装を読む。
- レポートの描画形式だけを変えたいときは、report 側の実装を読む。

## hash
- 197fbdf3a58e85776b7ee77d93cb4ca1cbf94161be822d232a27ccd795127390
