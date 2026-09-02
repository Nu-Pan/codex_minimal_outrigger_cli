# `cmoc session join`

## 概要

- `cmoc session join` は、session を完了して `{{cmoc-session-home-branch}}` へ戻すためのコマンドである。
- i.e. `cmoc session join` は、現在 checkout している `{{cmoc-session-branch}}` を `{{cmoc-session-home-branch}}` へ merge する。
- 通常の git branch 同士の汎用 merge wrapper ではない。
- merge source、merge target、および `{{repository-default-branch}}` の扱いは、`{{cmoc-root}}/oracle/doc/branch_model.md` の「概要」を正本とする。

## 引数

- 引数なし
- merge source も merge target も引数では受け取らない

## 事前条件

`{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の「active session context と編集 run 開始・session 終了の共通事前条件」を満たす。

以下の場合はエラー終了する。

- 対応する `{{cmoc-session-state-file}}` から `{{cmoc-session-home-branch}}` を特定出来ない

## 実行手順

1. doctor preprocess を呼び出す
2. 事前検証
    - 事前条件を満たしている事を確認する
3. マージ処理
    1. `git switch {{session-home-branch}}` を実行する
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
3. cmoc は conflict marker が残っていない事を確認する
4. cmoc は conflict 対象ファイルを `git add` する
5. unmerged path が残っていないことを確認する
6. cmoc が merge commit を作成する

## conflict marker 解消用の agent call

- conflict 解消の意味仕様は、本書の「oracle file 規定と conflict 解消の優先順位」を正本とする
- 正確な prompt 文面、prompt part の選択、workload 固有の起動パラメータ、およびその選択理由は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/session/join/conflict_resolution.py` の `build_session_join_conflict_resolution_parameter` へ委譲する
- この agent call は `{{work-root}}` に対する編集操作を伴うため、必ず直列に実行すること
- oracle edit または realization refactor のための規定を conflict 解消へ転用してはいけない

### oracle file 規定と conflict 解消の優先順位

session join の conflict 解消は、両 branch の意味を保ったまま merge を完了するための作業であり、仕様変更または refactor を行う作業ではない。このため、conflict 対象 oracle file は marker 解消に必要な範囲だけ例外的に編集してよい。

- conflict の両側と関連する oracle file を確認し、両 branch の両立する意図と挙動を解消結果に保持する
- conflict 解消後も oracle file は realization file の正本であり、realization file の都合に合わせて oracle file の意味を変更してはいけない
- conflict marker の解消に不要な仕様変更、実装改善、または別 file の変更を行ってはいけない
- 両側の意味を両立できず人間意図の選択が必要な場合は、推測で一方を破棄せず未解消事項として報告する

## その他、コマンドが想定外に失敗した場合

- その時点で処理を打ち切り、ロールバック等はしない
- エラー分類とスタックトレースは、`{{cmoc-root}}/oracle/doc/app_spec/error_handling.md` に従う
- 手動解決が必要な場合は、実際に必要な操作をエラー terminal result の次の操作として示す

## `{{cmoc-managed-branch}}` 削除の条件

- 安全であること（ブランチ削除により作業結果が失われないこと）の裏付けが取れた場合のみ `{{cmoc-session-branch}}` の削除を実行する
- 確認に失敗した場合 `{{cmoc-managed-branch}}` は削除せず、 warning 扱いでユーザーに通知して続行する

## primary report

- `natural_completion` と `error` のすべての終了経路で、session join 実行要約を primary report として保存する。doctor preprocess または事前条件で終了した場合も対象とする。
- report は Markdown と YAML Front Matter で構成し、`{{repo-root}}/.cmoc/gu/ar/report/session/join/{{time-stamp}}.md` に保存する。
- front matter には、command、生成日時、repo root、terminal result の共通分類、終了コード、session branch、home branch、merge 前の両 branch の HEAD commit、作成した merge commit、および session state の実行前後の値を含める。確定できなかった値は `null` とする。
- 本文には、事前検証、branch 切替、merge 結果、conflict path、conflict 解消用 agent call と確定した解消結果、state 遷移、session branch の cleanup、warning またはエラー、必要な次の操作、および関連する診断用サブコマンドログと Codex call log を要約する。
- 実行しなかった merge、conflict 解消、state 更新、または cleanup は未実行として扱う。確定していない解消結果を作ってはならない。
