# `cmoc oracle investigation`

## 概要

- oracle file に関するユーザーの調査指示をエディタから受け取り、oracle file を根拠とする調査結果を回答する Codex CLI の TUI を起動する

## 引数

- なし

## 事前条件

- なし

## 実行手順

1. doctor preprocess を呼び出す
2. prompt editor input の lifecycle に従って、oracle file に関するユーザーの調査指示を受け取る
3. `build_oracle_investigation_launch_tui_parameter` で TUI 起動パラメータを構築する
4. 構築したパラメータで Codex CLI の TUI を起動する

## ユーザー指示の入力

- エディタ入力の仕組みは `{{cmoc-root}}/oracle/doc/app_spec/prompt_editor_input.md` を正本とする
- 初期表示文面と完全 prompt skeleton の正確な構築は、同文書が参照する oracle src を参照する

## TUI 起動パラメータ

- TUI の意味上の責務と調査境界は本書を正本とする。正確な prompt 文面、prompt part の選択、`AgentCallParameter`、および選択理由は、`oracle/src/oracle/acp_builder/oracle/investigation/launch_tui.py:15` の `build_oracle_investigation_launch_tui_parameter` へ委譲する
- `build_oracle_investigation_launch_tui_parameter` が返したパラメータを変更せずに TUI 起動へ渡す
- oracle file を扱う判断基準は `{{cmoc-root}}/oracle/doc/app_spec/oracle_and_realization.md:64` の「oracle file を扱う判断基準」を正本とする。正確な agent 向け文面は前述の builder を参照する
- `cmoc tui` のような実行パラメータ決定用 agent call は行わない

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
- 調査結果の自然言語部分は原則として日本語とする。識別子、path、command、log 原文、および引用は元の表記を維持してよい
- Codex CLI の TUI は oracle file を変更せず、realization file を読み書きしない
- Codex CLI の TUI は oracle file の変更結果を自動 commit しない
- TUI 起動前の indexing preflight による `INDEX.md` 更新および自動 commit は、前項の禁止対象に含めない
