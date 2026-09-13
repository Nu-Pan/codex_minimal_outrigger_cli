# `cmoc oracle edit`

## 目的

- oracle file の最終状態に関するユーザー指示を受け取り、本命と仕様削減の 2 回の `codex exec` agent call を直列に実行する。
- 本命 agent call は、ユーザー指示を oracle file へ反映する。仕様削減 agent call は、本命 agent call の成功後の状態を起点に、過剰な仕様を削減する。
- 人間が、最終的な差分の確認、追加修正、commit、および破棄に責任を持つ。差分の扱いは、本書の「終了と差分」で定める。
- このサブコマンドは編集 run ではない。fork、join、abandon lifecycle、run branch、linked worktree、および session state の `run` section は使用しない。

## 引数

- 引数なし。

## ユーザー指示と prompt の構築

- editor input handoff を含むエディタ入力は、`{{cmoc-root}}/oracle/doc/app_spec/prompt_editor_input.md` の「プロンプトのエディタ入力」が定める共通 lifecycle を使用する。
- editor 終了後に抽出した同じオリジナルのユーザー指示を、本命用と仕様削減用の builder に渡す。正確な prompt part、文面、workload 固有の起動パラメータ、およびその選択理由は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/oracle/edit/launch_exec.py` の `build_oracle_edit_main_launch_exec_parameter` と `build_oracle_edit_reduction_launch_exec_parameter` へ委譲する。
- 構築済み prompt の受け渡しは、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「prompt の構築と受け渡し」を正本とする。

## agent call 前の条件

- doctor preprocess の後、本命 agent call の直前に indexing preflight を 1 回だけ実行する。
- indexing preflight の後、本命 agent call を起動する直前に次の条件を検査する。条件を満たさない場合は、agent call を開始せずエラー終了する。
    - 呼び出し元の worktree が main worktree であり、`{{work-root}}` と `{{repo-root}}` が一致する。
    - `{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の「active session context」の条件を満たす。
- git working tree または staging area に未コミット差分が存在しても、起動を拒否しない。
- 起動前に、既存差分を commit、stash、rollback、または退避して worktree を clean にしない。
- doctor preprocess と indexing preflight による変更と commit は、それぞれ `{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` の「実行手順」と `{{cmoc-root}}/oracle/doc/app_spec/indexing.md` の「処理対象」に従う。
- 起動可否の判定では、session state の `run` section を読み書きしない。`run.state` を排他条件にしない。

## agent call の構成

- 本命と仕様削減は、それぞれ新しい `codex exec` session の初回 call とする。仕様削減を、本命 session に対する `codex exec resume` として起動してはならない。
- 各 agent call 内の retry、quota 回復待ち後の resume、および失敗処理には、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「`codex exec` が失敗した場合」を適用する。
- builder が構築した `AgentCallParameter` は変更せず、既存の `codex exec` 入力経路へ渡す。実行パラメータを決めるための追加 agent call は行わない。
- oracle file を扱う判断基準は、`{{cmoc-root}}/oracle/doc/app_spec/oracle_and_realization.md` の「oracle file を扱う判断基準」を正本とする。

## 仕様削減 agent call の判断材料

- 直前の本命 agent call が oracle file を変更したことを伝える。その変更は起動前の既存差分と分離されず、現在の Git 未コミット差分に含まれていることも伝える。
- オリジナルのユーザー指示、現在の oracle file、および oracle file に関する現在の Git 未コミット差分だけを本命成果の判断材料とする。
- 過剰な仕様文言を削除して仕様を簡素化させる。関連する仕様および規定への違反も修正させる。
- オリジナルのユーザー指示が要求する人間意図、実装差を許容しない境界、および対象外の既存仕様の意味を維持させる。固定の削減率または文字数目標は設けない。
- installed skill は補助規定として使用してよいが、この prompt、オリジナルのユーザー指示、cmoc 固有契約、および関連する oracle file を優先し、skill の有無を完了条件にしない。
- 仕様削減用 prompt を、本命用 prompt、本命 agent の stdout、stderr、最終回答、call metadata、session ID、またはその他の session log から派生させてはならない。これらを仕様削減 agent に読ませたり、判断根拠にさせたりしてはならない。

## 実行順序

1. doctor preprocess を呼び出す。
2. prompt editor input の共通 lifecycle に従って、oracle file の最終状態に関するオリジナルのユーザー指示を確定する。
3. オリジナルのユーザー指示から、本命用 `AgentCallParameter` を構築する。
4. indexing preflight を 1 回実行する。
5. agent call 前の条件を検査する。
6. 本命 agent call を新しい `codex exec` session で実行する。
7. 本命 agent call が成功した場合だけ、同じオリジナルのユーザー指示から仕様削減用 `AgentCallParameter` を構築し、新しい `codex exec` session で実行する。
8. 最外側の `cmoc oracle edit` の primary report を保存して終了状態を確定し、共通の terminal result と Windows toast をそれぞれ 1 回だけ通知する。

- 本命 agent call と仕様削減 agent call の間に、indexing agent call、自動 commit、または別の補完用 agent call を挟まない。

## agent の編集境界

- agent には oracle file だけを編集させる。realization file、`INDEX.md`、および `AGENTS.md` を編集させてはならない。
- agent には `git add`、`git commit`、`git stash`、branch 切替、および worktree 操作を禁止する。
- このサブコマンドの oracle file 編集権限によって、`cmoc oracle investigation` の file access 権限を拡張しない。

## 終了と差分

- 2 回の agent call が成功した場合だけ、`natural_completion` とする。本命または仕様削減が失敗した場合は `error` とする。
- 終了状態にかかわらず、それまでに filesystem 上へ残った差分を維持する。
- 起動前の既存未コミット差分と 2 回の agent call による変更を、invocation 固有の成果物として分離しない。
- report、console、およびログでは、agent call 前後の Git 差分、変更 path、または意味的な変更内容を、この invocation 固有の成果として断定しない。
- 終了後に自動 commit、rollback、stash、差分修正、branch または worktree の作成、変更 path の成果物認定、および indexing を行わない。
- oracle edit 固有の `result` または `completion_reason` を新設しない。

## primary report

- `natural_completion` と `error` のすべての終了経路で、oracle edit 実行要約を primary report として保存する。doctor preprocess、エディタ入力、indexing preflight、または agent call 前の条件で終了した場合も対象とする。
- report は Markdown と YAML Front Matter で構成し、`{{repo-root}}/.cmoc/gu/report/oracle_edit/{{time-stamp}}.md` に保存する。
- front matter には、次の実行情報を含める。
    - command
    - 生成日時
    - repo root
    - terminal result の共通分類
    - 終了コード
    - 本命・仕様削減 agent call の実行状況。それぞれについて、未開始、開始済み、成功、および失敗を判別可能にする。
- 本文には、各 agent call の実行状況と確定結果、terminal result の要約、warning またはエラー、必要な次の操作、診断用サブコマンドログ、および実行した agent call に対応する Codex call log を含める。

## console、ログ、および Windows toast

- console、サブコマンドログ、および terminal result は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「コンソール・ファイル、ログ出力規則」を正本とする。
- Windows toast の通知境界と内容は、`{{cmoc-root}}/oracle/doc/app_spec/windows_toast_notification.md` の「Windows toast 通知」を正本とする。
- 共通 reporter が受理した feedback observation は oracle edit の差分または成果物ではない。`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` の「既存 workload との境界」に従う独立した実行記録とする。

## 中断と排他制御

- このサブコマンドは中断可能サブコマンドに含めない。
- lock file、process 重複検出、active または running 状態の永続化、および editor work file の排他的 writer 管理を導入しない。
- 他の cmoc process またはエディタとの並行操作から生じる競合や不整合は、人間が管理する。
