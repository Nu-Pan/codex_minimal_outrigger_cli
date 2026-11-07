# `cmoc session join`

## 概要

`cmoc session join` は、`{{cmoc-session-branch}}` で home の変更を統合・検証し、その結果を `{{cmoc-session-home-branch}}` へ取り込んで session を完了するコマンドである。通常の実行は現在 checkout している session を対象とし、取り込み後の復旧は同じ worktree の home からも行える。通常の git branch 同士の汎用 merge wrapper としては使用しない。

merge source、merge target、および `{{repository-default-branch}}` の扱いは、`{{cmoc-root}}/spec/branch_model.md` の「git branch」と「git commit」を正本とする。

## 引数

引数は受け取らず、merge source と merge target は session から決定する。

## 事前条件

新しい join は、`{{cmoc-root}}/spec/app_spec/session_state.md` の「active session context と編集 run 開始・session 終了の共通事前条件」を満たす。未完了の join がある場合は、同じ session と worktree の復旧情報を先に照合する。未取り込みなら安全に準備を戻してから条件を確認し、取り込み済みなら削除済み session branch や `active` state の再成立を要求しない。復旧対象が一意に定まらない場合は停止する。

対応する `{{cmoc-session-state-file}}` から `{{cmoc-session-home-branch}}` を特定できない場合、またはその local branch が存在しない場合は、エラー終了する。remote-tracking branch から推測して作成しない。session ごとの排他と復旧情報の再確認により、同じ join の同時実行を防ぐ。

## 実行手順

準備、取り込み、失敗時の取消、および再試行の共通処理は、`{{cmoc-root}}/spec/app_spec/merge_conflict_resolution.md` の「共通の準備・取り込み・復旧」に従う。

1. 対象 session と復旧情報を確認する。取り込み済みなら、doctor・準備・merge を繰り返さず後処理へ進む。
2. 事前条件を確認し、準備前の session HEAD を記録する。doctor preprocess を呼び出し、refactor state の entry 同期は統合後まで遅延する。
3. session branch 上で基準 home HEAD を merge し、競合解消後の機械検査、および管理物の同期を完了する。
4. 同じ worktree を home branch へ切り替え、準備完了の session を取り込む。未取り込み commit がなければ共通の no-op 条件を適用する。
5. `{{cmoc-session-state-file}}` の `session.state` を `joined` にする。
6. 安全に削除できる場合のみ session branch を削除する。実際の state と cleanup 結果を primary report に保存した後、join の完了を記録する。

## `{{cmoc-session-home-branch}}` が進んでいた場合

`{{cmoc-session-home-branch}}` が session 作成後に進んでいてもエラーにはせず、その回の基準 home HEAD として session 側で統合する。準備中に home がさらに更新された場合は、その回の取り込みを停止し、共通の復旧と再試行に従う。

## feedback state との境界

session join と repository-local feedback state の境界は、`{{cmoc-root}}/spec/app_spec/feedback_state.md` の「所有範囲と配置」を正本とする。

## `git merge` がコンフリクトした場合

判断基準、agent と cmoc の責務、受理、および報告は、`{{cmoc-root}}/spec/app_spec/merge_conflict_resolution.md` の「join の競合解消」に従う。準備 merge の source は基準 home HEAD、target は home 統合直前の session HEAD とする。

競合解消 call または機械検査が失敗した場合は、home への取り込み、`session.state=joined` への更新、および session branch の削除を行わない。共通の復旧処理で準備を取り消し、本書の「その他、コマンドが想定外に失敗した場合」に従い停止する。

## 競合解消用の agent call

agent は、home を session branch へ統合中の worktree を cwd として、decision・reference を読み取り専用で参照し、アクセス境界内の spec file と realization file を編集する。session join のために新しい editing run は作らない。

session 固有の入力対応は、`{{cmoc-root}}/reference/src/reference/request_builder/session/join/conflict_resolution.py` の `build_session_join_conflict_resolution_request` へ委譲する。この builder は共通 request builder を呼び出す。共通 policy、指示文と起動条件の構築は、`{{cmoc-root}}/spec/app_spec/merge_conflict_resolution.md` の「agent への入力と正確な定義の委譲」に従う。

## その他、コマンドが想定外に失敗した場合

取り込み前に安全な取消を完了できた場合は、session branch を準備前の成果へ戻し、`session.state=active` として保持する。未解消理由への対応や通常の編集を行った後、`cmoc session join` で新しい試行を開始できる。

復旧を完了できない場合は `session.state=error` として残存状態と復旧情報を保持する。home への取り込み成立後の失敗も `error` とし、確定した home commit を取り消さない。同じ worktree から `cmoc session join` を再実行すると、session branch が削除済みでも未完了の後処理を再開する。`joined` の保存後に停止した場合も、完了記録がなければ復旧対象とする。

未完了の join を通常の doctor、編集 run の開始、session fork、または session abandon で上書きしない。復旧を先に行うよう案内する。エラー分類とスタックトレースは、`{{cmoc-root}}/spec/app_spec/error_handling.md` の「エラーハンドリング規則」に従い、必要な手動操作を terminal result に示す。重要事項確認の未完了は、`{{cmoc-root}}/spec/app_spec/console_and_file_log.md` の「確認結果と終了結果の分離」に従う。

## `{{cmoc-session-branch}}` 削除の条件

- 残存する session branch が準備完了 HEAD を指し、その成果が home から到達可能であると確認できた場合に限り、`{{cmoc-session-branch}}` を削除する
- 確認に失敗した場合は、`{{cmoc-session-branch}}` を削除せず、warning としてユーザーに通知して続行する

## primary report

実行 ID と primary report の共通表示契約は、`{{cmoc-root}}/spec/app_spec/console_and_file_log.md` の「実行 ID の開始表示」「primary report」に従う。

- `natural_completion` と `error` のすべての終了経路で、session join 実行要約を primary report として保存する。doctor preprocess または事前条件で終了した場合も対象とする。
- report は `{{repo-root}}/.cmoc/gu/report/session/join/{{execution-id}}.md` に保存する。
- 実行情報には、command、生成日時、repo root、terminal result の共通分類、終了コード、session branch、home branch、準備前の session HEAD、基準 home HEAD、作成した merge commit、および session state の実行前後の値を含める。確定できなかった値は `null` とする。
- 詳細結果には、事前検証、準備完了 session HEAD、取り込み成立の commit と tree、branch 切替、merge 結果、準備の取消と復旧結果、conflict path、conflict 解消用 agent call の実行状態と機械検査後の merge の確定、state 遷移、session branch の cleanup、warning またはエラー、および Codex call log を含める。
- 競合解消 call の回答原文と cmoc が観測した付随編集・処理結果は、`{{cmoc-root}}/spec/app_spec/merge_conflict_resolution.md` の「受理と報告」に従って記録する。
- 実行しなかった merge、conflict 解消、state 更新、または cleanup は未実行として扱う。確定していない解消結果を作ってはならない。
