# `cmoc oracle investigation`

## 概要

- oracle file に関するユーザーの調査指示をエディタから受け取り、oracle file を根拠とする調査結果を回答する Codex CLI の TUI を起動する

## 引数

- なし

## 事前条件

- なし

## 実行手順

1. doctor preprocess を呼び出す
2. `build_oracle_investigation_launch_tui_parameter` へ `{{original-prompt-here}}` を渡し、初期表示用の完全プロンプトの skeleton を構築する
3. skeleton を初期値として、oracle file に関するユーザーの調査指示をエディタから受け取る
4. 抽出したユーザー指示を `build_oracle_investigation_launch_tui_parameter` へ渡し、完全プロンプト本文を含む TUI 起動パラメータを構築する
5. 構築したパラメータで Codex CLI の TUI を起動する

## ユーザー指示の入力

- エディタ入力の仕組みは `{{cmoc-root}}/oracle/doc/app_spec/prompt_editor_input.md` を正本とする
- エディタ編集対象ファイルの初期値は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/editor_input.py` の `build_prompt_editor_input_initial_text` で構築する
- `build_oracle_investigation_launch_tui_parameter` へ `{{original-prompt-here}}` を渡し、oracle file の読み取り専用、realization file の読み書き禁止、および oracle file の調査に必要な cmoc 固有契約を含む完全プロンプトの skeleton を構築する
- 汎用規定と動的プロンプトの責務境界は、`{{cmoc-root}}/oracle/doc/app_spec/prompt_policy.md` を正本とする

## TUI 起動パラメータ

- TUI の意味上の責務と調査境界は本書を正本とする。`{{cmoc-root}}/oracle/src/oracle/acp_builder/oracle/investigation/launch_tui.py` の `build_oracle_investigation_launch_tui_parameter` は、TUI に渡す正確な prompt 文面と agent call parameter を構築する
- `build_oracle_investigation_launch_tui_parameter` が返したパラメータを変更せずに TUI 起動へ渡す
- oracle file を扱う判断基準は `{{cmoc-root}}/oracle/doc/app_spec/misc_spec.md` を正本とする。builder は同基準を agent へ伝える文面を固定で prompt へ注入する
- `cmoc tui` のような実行パラメータ決定用 agent call は行わない

## investigation から edit への handoff

oracle investigation で editor handoff を行う場合は、共通の editor handoff policy を適用する。

- handoff file への書き込みは、Codex CLI の TUI で調査結果を回答する責務を置き換えない。
- file access mode は `PURE_ORACLE_READ`、Codex CLI sandbox は `read-only` のまま維持する。
- agent は、handoff file への書き込みに必要な command だけについて、対象 path と理由を限定した command 単位の sandbox escalation を要求してよい。

## Codex CLI の起動

- 起動コマンドは `codex` とする
- `codex exec` は使用しない
- `cmoc tui` の「Codex CLI の場合」と同じく、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` から以下の要素を持ち込む
    - 環境変数 `$CODEX_HOME`
    - preflight validation
    - Codex CLI 引数による設定上書き
- このサブコマンドの TUI agent turn と終了時の Windows toast 通知は、`{{cmoc-root}}/oracle/doc/app_spec/windows_toast_notification.md` を正本とする

## 調査結果と変更の扱い

- 調査結果は Codex CLI の TUI でユーザーへ回答する
- Codex CLI の TUI は oracle file を変更せず、realization file を読み書きしない
- Codex CLI の TUI は oracle file の変更結果を自動 commit しない
- `run_indexing_preflight=True` による indexing preflight の `INDEX.md` 更新および自動 commit は、前項の禁止対象に含めない
