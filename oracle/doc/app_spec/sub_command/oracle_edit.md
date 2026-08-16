# `cmoc oracle edit`

## 目的

- oracle file の最終状態に関するユーザー指示を受け取り、本命と仕様削減の 2 回の `codex exec` agent call を直列に実行する。
- 本命 agent call はユーザー指示を oracle file へ反映する。仕様削減 agent call は、本命成功後の現在状態から過剰な仕様を削減する。
- 起動前から存在する未コミット差分と 2 回の agent call による変更は分離しない。人間が、最終的な差分の確認、追加修正、commit、および破棄に責任を持つ。
- このサブコマンドは編集 run ではない。fork、join、abandon lifecycle、run branch、linked worktree、および session state の `run` section は使用しない。

## 引数

- 引数なし。

## ユーザー指示と prompt の構築

- エディタ入力の仕組みは `{{cmoc-root}}/oracle/doc/app_spec/prompt_editor_input.md` を正本とする。
- エディタ編集対象 file の初期値は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/editor_input.py` の `build_prompt_editor_input_initial_text` で構築する。
- `{{cmoc-root}}/oracle/src/oracle/acp_builder/oracle/edit/launch_exec.py` の `build_oracle_edit_main_launch_exec_parameter` へ `{{original-prompt-here}}` を渡し、editor の初期表示用 skeleton を構築する。
- editor 終了後に抽出した同じオリジナルのユーザー指示を、本命用と仕様削減用の builder に渡す。各 builder は、担当固有の完全 prompt 本文を `AgentCallParameter.prompt` に設定する。
- prompt の意味、文面、および受け渡しの共通規定は、`{{cmoc-root}}/oracle/doc/app_spec/prompt_policy.md` と `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` を正本とする。
- editor work file の排他的 writer は管理しない。他の TUI やエディタとの並行操作から生じる競合や不整合は、人間が管理する。

## agent call 前の条件

- doctor preprocess の後、本命 agent call の直前に indexing preflight を 1 回だけ実行する。
- indexing preflight の後、本命 agent call を起動する直前に次の条件を検査する。条件を満たさない場合は、agent call を開始せずエラー終了する。
    - 呼び出し元の worktree が main worktree であり、`{{work-root}}` と `{{repo-root}}` が一致する。
    - 現在の branch が、対応する session state で `active` な `{{cmoc-session-branch}}` である。
- git working tree または staging area に未コミット差分が存在しても、起動を拒否しない。
- 起動前に、既存差分を commit、stash、rollback、または退避して worktree を clean にしない。
- doctor preprocess と indexing preflight による変更と commit は、それぞれ `{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` と `{{cmoc-root}}/oracle/doc/app_spec/indexing.md` に従う。indexing 開始時点の既存 `INDEX.md` 差分は、indexing の自動 commit に含まれてよい。
- 起動可否の判定では、session state の `run` section を読み書きしない。`run.state` を排他条件にしない。

## agent call の構成

- 本命と仕様削減は、それぞれ新しい `codex exec` session の初回 call とする。仕様削減を、本命 session に対する `codex exec resume` として起動してはならない。
- 各 agent call 内の retry、quota 回復待ち後の resume、および失敗処理には、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の共通規約を適用する。
- 2 回の agent call は、次の起動パラメータを共通とする。
    - `AgentCallParameter.agent_call_cwd` は `{{repo-root}}`。
    - model class は `FLAGSHIP`。
    - reasoning effort は `MAX`。
    - file access mode は `PURE_ORACLE_WRITE`。
    - Structured Output は要求しない。
- 本命用 `AgentCallParameter.run_indexing_preflight` は `True`、仕様削減用は `False` とする。
- builder が構築した `AgentCallParameter` は変更せず、既存の `codex exec` 入力経路へ渡す。実行パラメータを決めるための追加 agent call は行わない。
- oracle file を扱う判断基準は、`{{cmoc-root}}/oracle/doc/app_spec/misc_spec.md` を正本とする。各 builder は、担当に必要な同基準の文面を固定で prompt へ注入する。

## 仕様削減 agent call の判断材料

- 直前の本命 agent call が oracle file を変更し、その変更が起動前の既存差分と分離されず、現在の Git 未コミット差分に含まれていることを伝える。
- オリジナルのユーザー指示、現在の oracle file、および oracle file に関する現在の Git 未コミット差分だけを本命成果の判断材料とする。
- 過剰な仕様文言を削除し、仕様を簡素化し、関連する仕様および規定への違反を修正させる。
- オリジナルのユーザー指示が要求する人間意図、実装差を許容しない境界、および対象外の既存仕様の意味を維持させる。固定の削減率または文字数目標は設けない。
- 適用できる installed skill は補助規定として使用してよい。installed skill がこの prompt、オリジナルのユーザー指示、cmoc 固有契約、または関連する oracle file と競合する場合は、installed skill 以外を優先する。installed skill の有無を完了条件にしてはならない。
- 仕様削減用 prompt を、本命用 prompt、本命 agent の stdout、stderr、最終回答、call metadata、session ID、またはその他の session log から派生させてはならない。これらを仕様削減 agent に読ませたり、判断根拠にさせたりしてはならない。

## 実行順序

1. doctor preprocess を呼び出す。
2. `build_oracle_edit_main_launch_exec_parameter` で、本命用の完全 prompt の skeleton を構築する。
3. skeleton を初期値として、oracle file の最終状態に関するユーザー指示をエディタから受け取る。
4. editor work file の一回の最終読み取り結果を保存し、オリジナルのユーザー指示を抽出する。
5. オリジナルのユーザー指示から、本命用 `AgentCallParameter` を構築する。
6. indexing preflight を 1 回実行する。
7. agent call 前の条件を検査する。
8. 本命 agent call を新しい `codex exec` session で実行する。
9. 本命 agent call が成功した場合だけ、同じオリジナルのユーザー指示から仕様削減用 `AgentCallParameter` を構築し、新しい `codex exec` session で実行する。
10. 最外側の `cmoc oracle edit` の primary report を保存して終了状態を確定し、共通の terminal result と Windows toast をそれぞれ 1 回だけ通知する。

- 本命 agent call と仕様削減 agent call の間に、indexing agent call、自動 commit、または別の補完用 agent call を挟まない。
- 本命 agent call が失敗した場合は、仕様削減 agent call を開始せずエラー終了する。
- 仕様削減 agent call が失敗した場合も、エラー終了する。

## agent の編集境界

- agent には oracle file だけを編集させる。realization file、`INDEX.md`、および `AGENTS.md` を編集させてはならない。
- agent には `git add`、`git commit`、`git stash`、branch 切替、および worktree 操作を禁止する。
- `PURE_ORACLE_WRITE` はこのサブコマンドだけの権限とする。`cmoc oracle investigation` の file access 権限は拡張しない。

## 終了と差分

- 2 回の agent call が成功した場合だけ、`natural_completion` とする。本命または仕様削減が失敗した場合は `error` とする。
- 終了状態にかかわらず、それまでに filesystem 上へ残った差分を維持する。
- 起動前の既存未コミット差分と 2 回の agent call による変更を、invocation 固有の成果物として分離しない。
- 終了後に自動 commit、rollback、stash、差分修正、branch または worktree の作成、変更 path の成果物認定、および indexing を行わない。
- oracle edit 固有の `result` または `completion_reason` を新設しない。

## primary report

- `natural_completion` と `error` のすべての終了経路で、oracle edit 実行要約を primary report として保存する。doctor preprocess、エディタ入力、indexing preflight、または agent call 前の条件で終了した場合も対象とする。
- report は Markdown と YAML Front Matter で構成し、`{{repo-root}}/.cmoc/gu/ar/report/oracle_edit/{{time-stamp}}.md` に保存する。
- front matter には、command、生成日時、repo root、terminal result の共通分類、終了コード、および本命・仕様削減 agent call の実行状況を含める。各実行状況から、未開始、開始済み、成功、および失敗を判別可能にする。
- 本文には、各 agent call の実行状況と確定結果、terminal result の要約、warning またはエラー、必要な次の操作、診断用サブコマンドログ、および実行した agent call に対応する Codex call log を含める。
- 起動前の既存未コミット差分と agent call による変更を分離しない。report では、変更 path または意味的な変更内容をこの invocation 固有の成果として断定しない。

## console、ログ、および Windows toast

- console、サブコマンドログ、および terminal result は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` を正本とする。
- サブコマンドログは、2 回の agent call、対応する Codex call log、経過時間、戻り値、および最終的な terminal result を追跡可能にする。
- 各 agent call の完全 prompt 本文の保存と stdin 渡しは、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` に従う。
- 内部の各 `codex exec` は、独立した terminal result または Windows toast を通知しない。
- 最外側の `cmoc oracle edit` は、終了状態を確定した後に terminal result と Windows toast をそれぞれ 1 回だけ通知する。Windows toast の詳細は、`{{cmoc-root}}/oracle/doc/app_spec/windows_toast_notification.md` を正本とする。
- agent call 前後の Git 差分または変更 path を、この invocation 固有の成果物として断定してはならない。
- 共通 reporter が受理した feedback observation は oracle edit の差分または成果物ではない。`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` に従う独立した実行記録とする。

## 中断と排他制御

- このサブコマンドは中断可能サブコマンドに含めない。
- lock file、process 重複検出、active または running 状態の永続化、および editor work file の排他的 writer 管理を導入しない。
- 他の cmoc process またはエディタとの並行操作から生じる競合や不整合は、人間が管理する。
