# run 作業隔離規則

## 用語

- run は、workload 固有の fork で開始し、join または abandon で終了する隔離作業の 1 instance である。
- workload は、run が行う作業の種類である。
- fork, join, abandon は run の lifecycle 操作を表す。公開 CLI のサブコマンド名と一致する場合に限らない。
- run が使用する branch、commit、および worktree の定義と命名は、`{{cmoc-root}}/oracle/doc/branch_model.md` の `{{cmoc-run-branch}}` 以降を正本とする。
- 永続化する run state は、`{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の「run field」を正本とする。

## lifecycle

- run は 1 回のサブコマンド呼び出し内で fork から join または abandon まで完了してよい。
- 明示的な確認を経て成果物を取り込む編集 run は、workload 固有の fork サブコマンドで開始し、後続の `cmoc run join` または `cmoc run abandon` で終了する。
- run とサブコマンド呼び出しを 1:1 の概念として扱ってはいけない。
- read-only の investigation、cmoc 自身による機械的更新、および session join の conflict 解消は、明示的な join を必要とする編集 run ではない。

## git branch

- fork は、branch model が定める分岐元 commit から `{{cmoc-run-branch}}` を作成する。
- run の成果物は `{{cmoc-run-branch}}` 上の commit として記録する。
- join は workload の規則に従って `{{cmoc-run-branch}}` を `{{cmoc-session-branch}}` へ merge する。
- abandon は `{{cmoc-session-branch}}` へ merge せず、run の隔離資源を破棄する。

## git worktree

- run の作業は、branch model が定める `{{cmoc-run-worktree}}` 上で行う。
- agent call の cwd は、個別仕様に別の定めがない限り `{{cmoc-run-worktree}}` とする。
- run 上の agent call の root path は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「agent call の path context」に従う。同節が正確な導出先の oracle src を定める。
- cmoc process の cwd が `{{repo-root}}` であっても、run 上の agent call の path context は `{{cmoc-run-worktree}}` から解決する。
- 人間が `{{cmoc-run-worktree}}` を直接編集することは想定しない。

## `{{run-root}}` 外への書き込み例外

- 原則として、run の作業は `{{run-root}}` ツリー内だけを読み書きする。
- 個別仕様が明示する cmoc 管理データは、例外として `{{repo-root}}` 側へ書き込んでよい。
- 実行ログの保存先は `{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「サブコマンドログファイル」、session state の保存先は `{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の「概要」を正本とする。
- feedback observation と feedback state の保存先および lifecycle は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の「raw observation の保存」と `{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「feedback の repository-local state」を正本とする。
- run の join または abandon と feedback state の境界は、`{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の「スキーマ設計の基本原則」に従う。
