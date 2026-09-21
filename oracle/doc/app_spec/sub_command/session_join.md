# `cmoc session join`

## 概要

`cmoc session join` は、現在 checkout している `{{cmoc-session-branch}}` を `{{cmoc-session-home-branch}}` へ merge し、session を完了して home branch へ戻すコマンドである。通常の git branch 同士の汎用 merge wrapper としては使用しない。

merge source、merge target、および `{{repository-default-branch}}` の扱いは、`{{cmoc-root}}/oracle/doc/branch_model.md` の「git branch」と「git commit」を正本とする。

## 引数

引数は受け取らず、merge source と merge target は session から決定する。

## 事前条件

`{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の「active session context と編集 run 開始・session 終了の共通事前条件」を満たす。

以下の場合はエラー終了する。

- 対応する `{{cmoc-session-state-file}}` から `{{cmoc-session-home-branch}}` を特定できない

## 実行手順

1. doctor preprocess を呼び出す
2. 事前検証
    - 事前条件を満たしていることを確認する
3. マージ処理
    1. `git switch {{cmoc-session-home-branch}}` を実行する
    2. `git merge --no-ff {{cmoc-session-branch}}` を実行する
    3. conflict が発生した場合は、Codex CLI に conflict marker 解消を依頼する
4. 後始末
    1. `{{cmoc-session-state-file}}` の `session.state` を `joined` にする
    2. 安全に削除できる場合のみ `{{cmoc-session-branch}}` を削除する

## `{{cmoc-session-home-branch}}` が進んでいた場合

`{{cmoc-session-home-branch}}` が session 作成後に進んでいてもエラーにはしない。
`cmoc session join` は、実行時点の `{{cmoc-session-home-branch}}` HEAD に `{{cmoc-session-branch}}` を merge する。

merge conflict が発生した場合は通常の conflict として扱う。

## feedback state との境界

session join と repository-local feedback state の境界は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「所有範囲と配置」を正本とする。

## `git merge` がコンフリクトした場合

### 解決手順

1. cmoc は conflict 対象ファイルを列挙する
2. conflict marker 解消用の agent call を行う
3. cmoc は conflict marker が残っていないことを確認する
4. cmoc は conflict 対象ファイルを `git add` する
5. unmerged path が残っていないことを確認する
6. cmoc が merge commit を作成する

## conflict marker 解消用の agent call

- conflict 解消の意味仕様は、本書の「oracle file 規定と conflict 解消の優先順位」を正本とする
- call 固有の正確な prompt 文面、prompt part の選択、workload 固有の起動パラメータ、およびその選択理由は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/session/join/conflict_resolution.py` の `build_session_join_conflict_resolution_parameter` へ委譲する
- マージ固有の規定を agent に伝える正確な policy 文面は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/policy/conflict_resolution.py` の `build_conflict_resolution_policy` へ委譲する
- この agent call は `{{work-root}}` に対する編集操作を伴うため、必ず直列に実行すること

### oracle file 規定と conflict 解消の優先順位

session join の conflict 解消結果は、共通の oracle・realization 規定と、本節のマージ固有の成果条件を同時に満たさなければならない。共通規定による整理・検証を適用し、ファイルアクセス境界の下で付随する編集の要否・範囲を agent の判断に委ねる。

共通規定は、次の正本を参照する。

- `{{cmoc-root}}/oracle/doc/app_spec/oracle_and_realization.md` の「oracle doc と oracle src の正本責務」から「正本責務に基づく優先関係」まで、および「oracle file を扱う判断基準」「realization file を扱う判断基準」：正本責務・優先関係と、oracle・realization file の判断基準。
- `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「詳細なファイルアクセス制限」「書き込み主体の責任分界」「SDPolicy の例外」：共通のアクセス境界と、例外の適用範囲。

マージ固有の成果条件は、次のとおりとする。

- conflict の両側と関連する oracle file を確認し、両 branch の両立する意図と挙動を解消結果に保持する
- 両側の意味を両立できず人間意図の選択が必要な場合は、推測で一方を破棄せず未解消事項として報告する
- 規定に違反する解消結果を解消完了として扱い、merge を成立させてはいけない

## その他、コマンドが想定外に失敗した場合

- その時点で処理を打ち切り、ロールバック等はしない
- エラー分類とスタックトレースは、`{{cmoc-root}}/oracle/doc/app_spec/error_handling.md` の「エラーハンドリング規則」に従う
- 手動解決が必要な場合は、実際に必要な操作をエラー terminal result の次の操作として示す

## `{{cmoc-session-branch}}` 削除の条件

- ブランチを削除しても作業結果が失われないと確認できた場合に限り、`{{cmoc-session-branch}}` を削除する
- 確認に失敗した場合は、`{{cmoc-session-branch}}` を削除せず、warning としてユーザーに通知して続行する

## primary report

- `natural_completion` と `error` のすべての終了経路で、session join 実行要約を primary report として保存する。doctor preprocess または事前条件で終了した場合も対象とする。
- report は Markdown と YAML Front Matter で構成し、`{{repo-root}}/.cmoc/gu/report/session/join/{{time-stamp}}.md` に保存する。
- front matter には、command、生成日時、repo root、terminal result の共通分類、終了コード、session branch、home branch、merge 前の両 branch の HEAD commit、作成した merge commit、および session state の実行前後の値を含める。確定できなかった値は `null` とする。
- 本文には、事前検証、branch 切替、merge 結果、conflict path、conflict 解消用 agent call と確定した解消結果、state 遷移、session branch の cleanup、warning またはエラー、必要な次の操作、および関連する診断用サブコマンドログと Codex call log を要約する。
- 実行しなかった merge、conflict 解消、state 更新、または cleanup は未実行として扱う。確定していない解消結果を作ってはならない。
