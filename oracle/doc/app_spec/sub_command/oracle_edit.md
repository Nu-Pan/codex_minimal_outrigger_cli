# `cmoc oracle edit`

## 目的

- oracle file の最終状態に関するユーザー指示を受け取り、その指示から導かれる目標状態への編集を、同じ目的・入力・設定の固定 2 回の agent call で直列に実行する。
- 各回を新しい Codex session で開始し、現在のリポジトリ状態と目標状態を照合し直すことで、残った不足を解消できるという仮説に基づく。汎用の反復回数設定や追加のレビュー工程は設けない。
- 人間が、最終的な差分の確認、追加修正、commit、および破棄に責任を持つ。差分の扱いは、本書の「終了と差分」で定める。
- このサブコマンドは編集 run ではない。fork、join、abandon lifecycle、run branch、linked worktree、および session state の `run` section は使用しない。

## 引数

- 引数なし。

## ユーザー指示と prompt の構築

- editor input handoff を含むエディタ入力は、`{{cmoc-root}}/oracle/doc/app_spec/prompt_editor_input.md` の「プロンプトのエディタ入力」が定める共通 lifecycle を使用する。
- editor 終了後に抽出して確定したオリジナルのユーザー指示から、両回で使用する完全 prompt と `AgentCallParameter` を一度だけ構築する。正確な prompt part、文面、workload 固有の起動パラメータ、およびその選択理由は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/oracle/edit/launch_exec.py` の `build_oracle_edit_main_launch_exec_parameter` へ委譲する。
- cmoc が自動構築する方針・指示文は、過去の agent の会話、最終回答、および実行ログへの参照について言及しない。この構築上の規則を、人間が入力した作業指示の内容を削除する処理として適用しない。
- handoff を受けた場合も、入力確定後は本書の「実行順序」に従って編集へ進み、送り元の TUI 終了や最終結果の確定を開始条件にしない。
- 両回で使用する完全 prompt と `AgentCallParameter` の構築時に、共通 builder に対応する `CmocConfigCodex.agent_calls` の既存 entry と、選択した provider の定義から、model provider、Model、Reasoning Effort、および使用する provider-local 設定の値を確定する。設定 key を維持し、人間が調整した値を両回へ引き継ぐ。設定の正確な定義は、`{{cmoc-root}}/oracle/src/oracle/other/cmoc_config.py` の `CmocConfigCodex` を参照する。
- `AgentCallParameter` の全内容と確定した設定値を変更せず両回で使用し、1 回目が cmoc 自身の builder や設定定義を編集しても、再構築・再取得しない。
- 構築済み prompt の受け渡しは、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「prompt の構築と受け渡し」を正本とする。
- prompt は両回に共通とし、実行回に依存する役割や前提を設けない。agent 向け文面に 2 回実行の内部制御や設計仮説を含めない。

## agent call 前の条件

- 本書の「実行順序」で定める時点で次の条件を検査し、満たさない場合は agent call を開始せずエラー終了する。
    - 呼び出し元の worktree が main worktree であり、`{{work-root}}` と `{{repo-root}}` が一致する。
    - `{{cmoc-root}}/oracle/doc/app_spec/session_state.md` の「active session context」の条件を満たす。
- git working tree または staging area に未コミット差分が存在しても、起動を拒否しない。
- 起動前に、既存差分を commit、stash、rollback、または退避して worktree を clean にしない。
- doctor preprocess と indexing による変更と commit は、それぞれ `{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` の「実行手順」と `{{cmoc-root}}/oracle/doc/app_spec/indexing.md` の「処理対象」に従う。
- 起動可否の判定では、session state の `run` section を読み書きしない。`run.state` を排他条件にしない。

## agent call の構成

- 各回は、別の新しい Codex session に対する `codex exec` の初回 call とする。2 回目を、1 回目の session に対する `codex exec resume` として起動してはならない。
- 各実行を独立して識別・管理するため、agent call ID、Codex call ID、session ID、ログ保存先、および call-scoped な管理情報を実行ごとに分ける。識別とログの共通規約は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「基本」「Codex CLI 呼び出し情報の保存」「Codex session ID」を参照する。
- 各 agent call 内の retry、quota 回復待ち後の resume、および失敗処理には、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「`codex exec` が失敗した場合」を適用し、正常系の 2 回実行とは区別する。
- 実行パラメータを決めるための追加 agent call は行わない。

## 編集目的と判断材料

- 各 agent は、ユーザー指示、現在の関連 oracle file、および oracle file に関する現在の Git 未コミット差分を照合し、目標状態との差を判断する。
- 作業範囲は目標状態の達成に必要な関連仕様のまとまりとし、指示に明記された箇所や既に差分がある箇所だけに限定せず、必要な追加・削除・統合・再構成を選べるようにする。ユーザー指示が要求する人間意図と実装差を許容しない境界を満たし、対象外の既存仕様の意味を維持する。
- 未コミット差分は起動前からの変更も含み得る判断材料であり、完成済みの成果や今回の呼び出しだけに由来する成果とはみなさない。
- 各 agent は、`{{work-root}}` の Git worktree で、staging area、working tree、および Git 未追跡の新規 oracle file の状態を含めて、現在の oracle file と未コミットの変更を取得する。参照入力の渡し方と取得失敗の扱いは、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「Git 差分の参照入力」に従う。
- 完了条件は、関連する oracle file が目標状態を満たしていることとする。既に満たしていれば不必要に変更せず完了することを目指す。2 回目の追加変更、文字数の削減、または品質の向上は完了条件にしない。
- oracle file と installed skill の共通判断基準は、`{{cmoc-root}}/oracle/doc/app_spec/oracle_and_realization.md` の「oracle file を扱う判断基準」に従う。file access、oracle、routing などの共通 policy は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「caller 固有の objective」が定める責務分担に従って組み込む。

## 実行順序

1. doctor preprocess を呼び出す。
2. prompt editor input の共通 lifecycle に従って、oracle file の最終状態に関するオリジナルのユーザー指示を確定する。
3. 本書の「ユーザー指示と prompt の構築」に従って、両回で共用する入力と設定を確定する。
4. oracle edit が 2 回の編集の外側で indexing を 1 回実行する。共通 builder は、各 agent call での indexing preflight を無効にする起動パラメータを構築する。
5. agent call 前の条件を検査する。
6. 1 回目の編集 agent call を実行する。
7. 1 回目が成功した場合は、追加変更の有無にかかわらず 2 回目の編集 agent call を実行する。2 回目は、1 回目の編集結果が残った同じ worktree の現在状態を読む。1 回目が失敗した場合は、2 回目を開始しない。
8. 最外側の `cmoc oracle edit` の primary report を保存して終了状態を確定し、共通の terminal result と Windows toast をそれぞれ 1 回だけ通知する。

- 2 回の編集の間に、indexing、自動 commit、または別の補完用 agent call を挟まない。

## agent の編集境界

- agent には oracle file だけを編集させる。realization file、`INDEX.md`、および `AGENTS.md` を編集させてはならない。
- agent には `git add`、`git commit`、`git stash`、branch 切替、および worktree 操作を禁止する。
- このサブコマンドの oracle file 編集権限によって、`cmoc oracle investigation` の file access 権限を拡張しない。

## 終了と差分

- 2 回の agent call が成功した場合だけ、`natural_completion` とする。いずれかが失敗した場合は `error` とする。
- 終了状態にかかわらず、それまでに filesystem 上へ残った差分を維持する。
- 起動前の既存未コミット差分と 2 回の agent call による変更を分離せず、report、console、およびログでも、差分、変更 path、または意味的な変更内容を invocation 固有の成果として認定しない。
- 終了後に自動 commit、rollback、stash、差分修正、branch または worktree の作成、変更 path の成果物認定、および indexing を行わない。
- oracle edit 固有の `result` または `completion_reason` を新設しない。

## primary report

- agent call 開始前を含むすべての終了経路で、oracle edit 実行要約を primary report として保存する。
- report は Markdown と YAML Front Matter で構成し、`{{repo-root}}/.cmoc/gu/report/oracle_edit/{{time-stamp}}.md` に保存する。
- front matter には、次の実行情報を含める。
    - command
    - 生成日時
    - repo root
    - terminal result の共通分類
    - 終了コード
    - 1 回目・2 回目の agent call の実行状況。それぞれについて、未開始、開始済み、成功、および失敗を判別可能にする。
- 本文には、各 agent call の実行状況と確定結果、terminal result の要約、warning またはエラー、必要な次の操作、診断用サブコマンドログ、および実行した agent call に対応する Codex call log を含める。

## console、ログ、および Windows toast

- console、サブコマンドログ、および terminal result は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「コンソール・ファイル、ログ出力規則」を正本とする。
- console とログで編集の実行状況を示す場合は、共通の agent call 種別とは別に、1 回目と 2 回目を識別できるようにする。
- Windows toast の通知境界と内容は、`{{cmoc-root}}/oracle/doc/app_spec/windows_toast_notification.md` の「Windows toast 通知」を正本とする。
- 共通 reporter が受理した feedback observation は oracle edit の差分または成果物ではない。`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` の「既存 workload との境界」に従う独立した実行記録とする。

## 中断と排他制御

- このサブコマンドは中断可能サブコマンドに含めない。
- lock file、process 重複検出、active または running 状態の永続化、および editor work file の排他的 writer 管理を導入しない。
- 他の cmoc process またはエディタとの並行操作から生じる競合や不整合は、人間が管理する。
