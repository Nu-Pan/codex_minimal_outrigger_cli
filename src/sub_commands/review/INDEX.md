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
- `review oracle` コマンドの実行本体を扱う。セッション branch の妥当性確認、隔離 review worktree の作成と削除、oracle 対象の列挙、review loop 実行、所見の集約、report 出力までを一連で追うときに読む。
- 個別の所見抽出や report 生成の細部ではなく、このコマンド全体の制御フローと終了時の扱いを確認したいときに進む。内部の補助処理だけを知りたい場合は、ここではなく参照先の各 helper を読む。

## Read this when
- `review oracle` の実行手順、分岐、エラー終了、ユーザー中断時の扱いを確認したい。
- review 対象の選定や worktree での隔離実行が、どの責務で結び付いているかを知りたい。
- 実行結果の report がどのタイミングで書かれるか、またどの条件でレビュー branch の変更を join するかを見たい。

## Do not read this when
- 所見本文のレンダリングだけを追いたいときは、report 系の helper を直接読む。
- review 対象の列挙規則だけを見たいときは、targets 側を読む。
- review index の衝突解決や merge の個別操作だけを見たいときは、review index 系の helper を読む。

## hash
- 5938ab5b69cb4bb408162a9405cdab10be3655d81de1129cf96c943fedb70b10
