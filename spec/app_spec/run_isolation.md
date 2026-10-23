# run 作業隔離規則

## 用語

run は、workload が branch と worktree を分岐させて開始し、join または abandon で終了する隔離作業の 1 instance である。workload は、その run が行う作業の種類を表す。fork、join、abandon は run の lifecycle 操作を指し、公開 CLI のサブコマンド名と一致するとは限らない。

run が使用する branch、commit、および worktree の定義と命名は、`{{cmoc-root}}/spec/branch_model.md` の「`{{cmoc-run-branch}}`」「git commit」「`{{cmoc-run-worktree}}`」を正本とする。run ID の識別単位・発行・保持は、`{{cmoc-root}}/spec/app_spec/sub_command/editing_run.md` の「共通開始処理」、永続化する run state は、`{{cmoc-root}}/spec/app_spec/session_state.md` の「run field」を正本とする。

## lifecycle

編集 run は、正常終了前に同じ invocation 内で自動 join する。対象 workload、正常中断、失敗時の明示 join・abandon、および workload 固有 recovery の境界は、`{{cmoc-root}}/spec/app_spec/sub_command/editing_run.md` の「対象」「正常終了時の自動 join」「join の失敗と復旧」に従う。復旧が別 invocation になるため、run とサブコマンド呼び出しを 1:1 の概念として扱ってはいけない。

session を直接編集する oracle edit、read-only の investigation、run を作らない cmoc 自身の機械的更新、および session join の conflict 解消は、編集 run ではない。

## git branch

- fork は、branch model が定める分岐元 commit から `{{cmoc-run-branch}}` を作成する。
- run の成果物は `{{cmoc-run-branch}}` 上の commit として記録する。
- join の統合順序は、`{{cmoc-root}}/spec/app_spec/sub_command/editing_run.md` の「merge と post-join」に従う。
- abandon は `{{cmoc-session-branch}}` へ merge せず、run の隔離資源を破棄する。

## git worktree

- run の作業は、branch model が定める `{{cmoc-run-worktree}}` 上で行う。
- 作成した run worktree の初回利用に先立つ配置先の準備は、`{{cmoc-root}}/spec/app_spec/doctor_preprocess.md` の「作業用配置先の存在保証」に従う。
- agent call の cwd は、個別仕様に別の定めがない限り `{{cmoc-run-worktree}}` とする。
- run join の準備と競合解消は、session の変更を統合する run worktree で行う。編集範囲と復旧は、`{{cmoc-root}}/spec/app_spec/sub_command/editing_run.md` の「競合解消」「join の失敗と復旧」を正本とし、そのために別の run は作らない。
- run 上の agent call の root path は、`{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「agent call の path context」に従う。同節が正確な導出先の oracle src を定める。
- cmoc process の cwd が `{{repo-root}}` であっても、run 上の agent call の path context は `{{cmoc-run-worktree}}` から解決する。
- 人間が `{{cmoc-run-worktree}}` を直接編集することは想定しない。

## run のアクセス境界と cmoc の管理処理

- run 上のファイルアクセスは、`{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「詳細なファイルアクセス制限」と「書き込み主体の責任分界」に従う。
- 個別仕様が明示する cmoc 管理データは、cmoc が `{{repo-root}}` 側へ書き込んでよい。
- 実行ログの保存先は `{{cmoc-root}}/spec/app_spec/console_and_file_log.md` の「サブコマンドログファイル」、session state の保存先は `{{cmoc-root}}/spec/app_spec/session_state.md` の「概要」を正本とする。
- feedback observation と feedback state の保存先および lifecycle は、`{{cmoc-root}}/spec/app_spec/feedback_observation.md` の「raw observation の保存」と `{{cmoc-root}}/spec/app_spec/feedback_state.md` の「feedback の repository-local state」を正本とする。
- run の join または abandon と feedback state の境界は、`{{cmoc-root}}/spec/app_spec/session_state.md` の「スキーマ設計の基本原則」に従う。
- 文書検索の配置、非公開化、および worktree 終了時の回収は、`{{cmoc-root}}/spec/app_spec/document_search.md` の「identity と保存先」「排他、期限、終了」に従う。
