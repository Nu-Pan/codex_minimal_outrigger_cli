# `cmoc realization apply`

## 目的

realization apply は、直近の git commit 群から読み取れる oracle file の変更を realization file へ素早く反映する workload である。正常終了時には、少なくとも指定した commit 範囲から読み取れる oracle 変更について、oracle file と realization file の間に齟齬がない成果を、同じ invocation 内で session branch へ取り込む。追従を完了できなかった run の成果物を join しても、未追従の oracle 変更を次回 apply の比較範囲から外さない。

ファイル単位の網羅的な調査と継続的な改善は non-goal とし、`{{cmoc-root}}/spec/app_spec/sub_command/realization_refactor.md` の「目的」が定める realization refactor が担う。fork、join、abandon の共通 lifecycle は、`{{cmoc-root}}/spec/app_spec/sub_command/editing_run.md` の「編集 run の共通仕様」を正本とする。

## CLI 契約

- 引数なし。
- 公開入口と help・補完・command 表記は、`{{cmoc-root}}/spec/app_spec/sub_command/editing_run.md` の「公開コマンド名」に従う。

## 追従対象差分

- 差分の終点は、`{{cmoc-root}}/spec/app_spec/sub_command/editing_run.md` の「共通開始処理」で確定・保存した `run.fork_commit`（`{{cmoc-run-fork-commit}}`）とする。
- 差分の始点は以下とする。
    - `session.last_joined_apply_fork_commit` が `null` でない場合は、その commit。
    - `null` の場合は `session.session_fork_commit`。
- Git 差分の参照入力は、`{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「Git 差分の参照入力」に従う。
- cmoc は、始点と終点の commit ID を確定して agent に渡す。agent は既存の cwd と `{{work-root}}` を用い、その repository で指定された両 commit 間の差分を Git から取得する。
- 対象は、両端のいずれかで oracle file だった path とし、rename を考慮する。追加・削除と oracle 内外をまたぐ rename を含め、現在の oracle 配下だけを候補集合にしてはならない。
- 上記に該当しない realization file、その他の非 oracle file の変更は追従対象外とする。
- 差分に現れた file だけを作業範囲としてはいけない。関連する oracle file と realization file を `{{work-root}}` リポジトリ全体から調査する。
- 差分は今回追従すべき oracle 変更を特定する根拠であり、realization file の変更内容を正本仕様へ逆流させる根拠ではない。
- apply 実行中に session branch へ追加された oracle 変更は、join 準備で run に統合されても次回 apply の比較範囲に残す。準備完了 run HEAD を追従対象差分の終点や比較始点の保存値にしない。

## agent call と file access

本節の call 数と補完禁止は run 内の本命の追従作業に適用する。同じ invocation の自動 join または復旧用の手動 join に必要な競合解消 call は別に扱い、`{{cmoc-root}}/spec/app_spec/sub_command/editing_run.md` の「競合解消」に従う。join を、失敗した追従作業を補完して追従完了へ変更する処理にはしない。primary report の重要事項確認用 call は、`{{cmoc-root}}/spec/app_spec/console_and_file_log.md` の「重要事項確認用 call」に従う共通生成工程とする。

- 追従要否と適合性の判断基準は、`{{cmoc-root}}/spec/app_spec/oracle_and_realization.md` の「oracle file に対する realization file の適合性」を正本とする。
- 正確な prompt 文面、prompt part の選択、builder の引数、起動パラメータの構築方法と選択理由は、`{{cmoc-root}}/reference/src/oracle/acp_builder/realization/apply/fork/launch_exec.py` の `build_realization_apply_request` へ委譲する。
- `{{cmoc-run-worktree}}` を agent call の cwd とする `codex exec` を 1 回だけ本命 agent call として実行する。Codex CLI の TUI は起動しない。
- 本命の追従作業を複数の agent call に分割してはいけない。
- 収束判定のために同じ作業を反復してはいけない。
- 本命 agent call 終了後に、別の agent call で作業を補完してはいけない。
- installed skill の有無によって、追従要否、適合性、または完了の判定基準を変えてはいけない。
- agent が変更する作業成果物は realization file だけとし、oracle file を変更してはならない。
- 一時作業領域の利用は、`{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「一時作業領域」に従う。

## 想定内差分

本命の追従作業の想定内差分は、agent が変更する realization file とする。join では、`{{cmoc-root}}/spec/app_spec/sub_command/editing_run.md` の「差分検査」に従って統合前の成果を検査する。session 由来の変更と競合解消の付随編集には同節の責務別の検査を適用し、join に伴う refactor state 同期は cmoc の共通管理処理として扱う。本命 agent の編集範囲は広げない。

## 実行手順

1. doctor preprocess と編集 run の共通開始処理を行う。
2. 追従対象差分の始点と終点を commit ID に確定する。
3. `build_realization_apply_request` で AgentCallParameter を構築する。
4. その AgentCallParameter を変更せず、`{{cmoc-run-worktree}}` を agent call の cwd とする `codex exec` で実行する。
5. agent の realization file 差分を検査し、差分がある場合は run branch に commit する。差分がなければ空 commit を作らない。この時点で join 全体を no-op と判定せず、共通 join の準備へ進む。
6. `run.state=joinable` にして、`{{cmoc-root}}/spec/app_spec/sub_command/editing_run.md` の「正常終了時の自動 join」に従って自動 join する。本書の「join 後 hook」も適用する。
7. 共通 join の post-join、結果保存、state 初期化、および cleanup の結果を primary report に含め、最外側の invocation の終了を確定する。

## エラー

- 次のいずれかに該当する場合は、成立済み run の `run.state` を `error` にする。run 成立前の失敗では、存在しない run を作らない。
    - 本命 agent call を正常に開始または終了できない。
    - 差分を整合した単位として commit または rollback できない。
    - 自動 join または必要な後処理に失敗した。
- 本命処理が失敗した run は自動 join しない。エラー後の手動 join・abandon、取り込み前後の復旧、および残存資源の扱いは、`{{cmoc-root}}/spec/app_spec/sub_command/editing_run.md` の「join の失敗と復旧」に従う。

## report と終了コード

実行 ID と primary report の共通表示契約は、`{{cmoc-root}}/spec/app_spec/console_and_file_log.md` の「実行 ID の開始表示」「primary report」に従う。

- `natural_completion` と `error` のすべての終了経路で report を保存する。共通開始条件違反など、run branch、run worktree、または本命 agent call の開始前に確定したエラーも対象とする。
- 共通 run 項目に加え、terminal result の共通分類、差分の始点 commit、Codex CLI の終了結果、変更 path、エラー、および関連ログを含める。
- 実行情報には、この invocation で reporter が受理した feedback の情報を含める。
    - `feedback_observation_count` は件数を表す。0 件の場合も 0 を含める。
    - `feedback_observations` は、`observation_id` と raw observation file の full `path` を持つ object の配列とする。0 件の場合は空配列とする。
- 差分の終点は共通項目の `{{cmoc-run-fork-commit}}` で表し、同じ commit を別項目として重複掲載しない。
- AI による意味的な変更要約は生成しない。primary report の重要事項確認にも、この変更要約や追従成果の再認定を行わせない。
- `{{repo-root}}/.cmoc/gu/report/realization/apply/{{execution-id}}.md` に保存し、この report を primary report とする。自動 join と後処理の掲載内容は、`{{cmoc-root}}/spec/app_spec/sub_command/editing_run.md` の「workload の report」に従う。
- report 生成時点で確定していない共通 run 項目、差分の始点 commit、Codex CLI の終了結果、または変更 path は、`null` または未実行として記録する。
- 自動 join と必要な終了処理を終えて `ready` に戻った `natural_completion` は終了コード 0、`error` は非 0 とする。`joinable` への遷移だけでは正常終了しない。

自動 join の競合解消 call を含め、feedback の収集には `{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「feedback reporter と collector context」を適用する。apply 固有の Structured Output field、終了後の発見用 agent call、または feedback 件数による終了コード変更を追加してはならない。詳細は `{{cmoc-root}}/spec/app_spec/feedback.md` の「既存 workload との境界」と「non-goal」を正本とする。

## join 後 hook

`session.last_joined_apply_fork_commit` は、次の条件をすべて満たす自動 join または `cmoc run join` で、session への取り込み成立後に、対象 run の元の `run.fork_commit`（`{{cmoc-run-fork-commit}}`）に更新する。それ以外では値を保持する。

- `run.kind` が `realization_apply` である。
- その join が事前条件を検証して対象 run を確定する時点で、`run.state` が `joinable` である。最外側の workload の起動時点の state で代用しない。
- 共通 join が定める session への merge または no-op join が成立している。run 側の準備や同期の完了だけでは更新しない。

join 失敗で `run.state=error` になり比較始点を更新できなかった場合は、次の apply が以前の比較範囲を再確認することを許容する。失敗した apply の部分成果を `error` から手動 join しても比較始点は更新しない。過去の追従作業の成功を記録・復元して更新資格を判定する処理や、そのための永続 field、成功 flag、状態値を追加してはならない。

CLI の終了コードだけで join の成立や比較始点の更新を判定してはならない。資格を満たして更新済みの値は、その後の report 保存や cleanup の失敗だけを理由に戻さない。取り込み確定後の rollback・recovery は、`{{cmoc-root}}/spec/app_spec/sub_command/editing_run.md` の「join の失敗と復旧」「report と terminal result」に従う。
