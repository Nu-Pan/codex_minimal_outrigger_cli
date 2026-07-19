# run 作業隔離規則

## 用語

- run は、workload 固有の fork で開始し、join または abandon で終了する隔離作業の 1 instance である。
- workload は、run が行う作業の種類である。
- fork, join, abandon は run の lifecycle 操作を表す。公開 CLI のサブコマンド名と一致する場合に限らない。

## lifecycle

- run は 1 回のサブコマンド呼び出し内で fork から join または abandon まで完了してよい。
- 明示的な確認を経て成果物を取り込む編集 run は、workload 固有の fork サブコマンドで開始し、後続の `cmoc run join` または `cmoc run abandon` で終了する。
- run とサブコマンド呼び出しを 1:1 の概念として扱ってはいけない。
- read-only の investigation/review、cmoc 自身による機械的更新、および session join の conflict 解消は、明示的な join を必要とする編集 run ではない。

## git branch

- fork は開始時点の `{{cmoc-session-branch}}` HEAD を `{{cmoc-run-fork-commit}}` とし、そこから `{{cmoc-run-branch}}` を作成する。
- run の成果物は `{{cmoc-run-branch}}` 上の commit として記録する。
- workload の種類は branch 用の別概念を作らず、run state と report で判別する。
- join は workload の規則に従って `{{cmoc-run-branch}}` を `{{cmoc-session-branch}}` へ merge する。
- abandon は `{{cmoc-session-branch}}` へ merge せず、run の隔離資源を破棄する。

## git worktree

- run の作業は、`{{cmoc-run-branch}}` を checkout した git linked worktree である `{{cmoc-run-worktree}}` 上で行う。
- agent call の cwd は、個別仕様に別の定めがない限り `{{cmoc-run-worktree}}` とする。
- 人間が `{{cmoc-run-worktree}}` を直接編集することは想定しない。

## `{{run-root}}` 外への書き込み例外

- 原則として、run の作業は `{{run-root}}` ツリー内だけを読み書きする。
- 個別仕様が明示する cmoc 管理データは、例外として `{{repo-root}}` 側へ書き込んでよい。
    - e.g. 実行ログと session state は `{{run-root}}/.cmoc/gu` ではなく `{{repo-root}}/.cmoc/gu` に保存する。
