# `cmoc oracle edit`

## 目的

- oracle file の最終状態に関するユーザー指示を受け取り、`{{repo-root}}` を agent call の cwd とする Codex CLI の TUI で oracle file を直接編集する。
- TUI 起動時点の既存未コミット差分と TUI の変更は分離せず、TUI 終了時に filesystem 上に残る差分を維持する。人間が差分の確認、追加修正、commit、破棄に責任を持つ。
- このサブコマンドは編集 run ではなく、fork, join, abandon lifecycle、run branch、linked worktree、session state の `run` section を使用しない。

## 引数

- 引数なし。

## ユーザー指示の入力

- エディタ入力の仕組みは `{{cmoc-root}}/oracle/doc/app_spec/prompt_editor_input.md` を正本とする。
- エディタ編集対象 file の初期値は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/editor_input.py` の `build_prompt_editor_input_initial_text` で構築する。
- `build_oracle_edit_launch_tui_parameter` へ `{{original-prompt-here}}` を渡し、realization file の読み書き禁止と oracle file の編集に必要な cmoc 固有契約を含む完全プロンプトの skeleton を構築する。
- 初期値へ渡す skeleton と、編集後に確定する完全プロンプトは、`build_oracle_edit_launch_tui_parameter` が構築した同じ完全プロンプトを使用する。
- 汎用規範と動的プロンプトの責務境界は、`{{cmoc-root}}/oracle/doc/app_spec/prompt_standard.md` を正本とする。

- cmoc は original prompt file の編集主体をこのサブコマンドに限定せず、排他的 writer を管理しない。他の TUI やエディタによる更新と、その並行操作から生じる競合や不整合は人間が管理する。

## TUI 起動直前の事前条件

- doctor preprocess と TUI 起動前の indexing preflight の後、TUI を起動する直前に以下を検査し、満たさない場合はエラー終了する。
    - 呼び出し元の worktree が main worktree であり、`{{work-root}}` と `{{repo-root}}` が一致する。
    - 現在の branch が、対応する session state で `active` な `{{cmoc-session-branch}}` である。
- git working tree または staging area に未コミット差分が存在しても、それを理由に TUI の起動を拒否しない。
- cmoc は TUI を起動するために、既存差分を commit, stash, rollback, または退避して worktree を clean にしない。
- doctor preprocess と indexing preflight による変更と commit は、それぞれ `{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` と `{{cmoc-root}}/oracle/doc/app_spec/indexing.md` に従う。indexing 開始時点の既存 `INDEX.md` 差分は、indexing の自動 commit に含まれてよい。
- 起動可否の判定では session state の `run` section を読み書きせず、`run.state` を排他条件にしない。

## TUI 起動パラメータ

- TUI の意味上の責務と編集境界は本書を正本とする。`{{cmoc-root}}/oracle/src/oracle/acp_builder/oracle/edit/launch_tui.py` の `build_oracle_edit_launch_tui_parameter` は、TUI に渡す正確な prompt 文面と `AgentCallParameter` を構築する。
- builder が返したパラメータを変更せずに TUI 起動へ渡し、実行パラメータ決定用の追加 agent call は行わない。
- oracle file を扱う判断基準は `{{cmoc-root}}/oracle/doc/app_spec/misc_spec.md` を正本とする。builder は同基準を agent へ伝える文面を固定で prompt へ注入する。
- builder は少なくとも以下を固定する。
    - `AgentCallParameter.agent_call_cwd` は `{{repo-root}}`。
    - model class は `FLAGSHIP`、reasoning effort は `MAX`。
    - file access mode は `PURE_ORACLE_WRITE`。
    - Structured Output は要求しない。
    - TUI 起動前の indexing preflight を行う。
- 起動コマンドは `codex` とし、`codex exec` は使用しない。
- 1 つの TUI process 内で複数 turn の対話を許容する。
- このサブコマンドの TUI agent turn と終了時の Windows toast 通知は、`{{cmoc-root}}/oracle/doc/app_spec/windows_toast_notification.md` を正本とする。
- Codex CLI の起動には `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` から以下だけを持ち込む。
    - 環境変数 `$CODEX_HOME`
    - preflight validation
    - Codex CLI 引数による設定上書き
    - file access mode に対応する sandbox とネットワーク設定

## 実行順序

1. doctor preprocess を呼び出す。
2. `build_oracle_edit_launch_tui_parameter` へ `{{original-prompt-here}}` を渡し、完全プロンプトの skeleton と TUI 起動パラメータを構築する。
3. skeleton を初期値として、oracle file の最終状態に関するユーザー指示をエディタから受け取る。
4. ユーザー指示を skeleton へ挿入し、完全プロンプトを確定する。
5. 過去の変更に対する遅延 indexing として、TUI 起動前の indexing preflight を行う。
6. TUI 起動直前の事前条件を検査する。
7. 1 つの Codex CLI TUI process を起動し、その終了コードでサブコマンドを終了する。

## TUI agent の編集境界

- agent には oracle file だけを編集し、realization file、`INDEX.md`、`AGENTS.md` を編集しないよう指示する。
- agent には `git add`, `git commit`, `git stash`, branch 切替、worktree 操作を禁止する。
- `PURE_ORACLE_WRITE` はこのサブコマンドだけの権限であり、`cmoc oracle investigation` の file access 権限は拡張しない。

## 終了と差分

- TUI が終了コード 0 を返した場合は正常終了し、非 0 を返した場合はエラー終了する。
- 終了コードにかかわらず、TUI が filesystem 上に残した差分をそのまま維持する。
- TUI 起動時点の既存未コミット差分と TUI による変更を、この invocation ごとの成果物として分離しない。
- cmoc は TUI 終了後に自動 commit, rollback, stash, 差分修正、branch または worktree の作成、変更 path の成果物認定を行わない。
- TUI 終了後の indexing は行わず、agent による `INDEX.md` 更新も禁止する。更新は、次に indexing preflight を伴う cmoc コマンドが呼ばれるまで遅延してよい。

## 中断と排他制御

- このサブコマンドは中断可能サブコマンドに含めない。
- cmoc 独自の Ctrl+C 処理、checkpoint、部分結果確定、retry、quota 待機、Codex session resume は行わず、TUI 起動中の入力と signal 処理は Codex CLI に委ねる。
- lock file、process 重複検出、他の cmoc TUI が起動中であることを理由とする拒否、active または running 状態の永続化、original prompt file の排他的 writer 管理を導入しない。
- 並行操作による競合や不整合は人間が管理する。

## ログ

- oracle edit 固有の fork report は作成しない。
- 共通のサブコマンドログには prompt file、TUI の開始と終了、終了コードを記録してよい。
- TUI 前後の git 差分または変更 path を、この invocation の成果物として断定してはならない。
- 共通 reporter が受理した feedback observation は oracle edit の差分または成果物ではなく、`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` に従う独立した実行記録とする。
