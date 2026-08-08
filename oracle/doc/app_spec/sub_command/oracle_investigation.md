# `cmoc oracle investigation`

## 概要

- oracle file に関するユーザーの調査指示をエディタから受け取り、oracle file を根拠とする調査結果を回答する Codex CLI の TUI を起動する

## 引数

- なし

## 事前条件

- なし

## 実行手順

1. doctor preprocess を呼び出す
2. `build_oracle_investigation_launch_tui_parameter` へ `{{original-prompt-here}}` を渡し、完全プロンプトの skeleton と TUI 起動パラメータを構築する
3. skeleton を初期値として、oracle file に関するユーザーの調査指示をエディタから受け取る
4. ユーザー指示を skeleton へ挿入し、完全プロンプトを確定する
5. 構築済みのパラメータで Codex CLI の TUI を起動する

## ユーザー指示の入力

- エディタ入力の仕組みは `{{cmoc-root}}/oracle/doc/app_spec/prompt_editor_input.md` を正本とする
- エディタ編集対象ファイルの初期値は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/editor_input.py` の `build_prompt_editor_input_initial_text` で構築する
- `build_oracle_investigation_launch_tui_parameter` へ `{{original-prompt-here}}` を渡し、oracle file の読み取り専用、realization file の読み書き禁止、および oracle file の調査に必要な cmoc 固有契約を含む完全プロンプトの skeleton を構築する
- 初期値へ渡す skeleton と、編集後に確定する完全プロンプトは、`build_oracle_investigation_launch_tui_parameter` が構築した同じ完全プロンプトを使用する
- 汎用規範と動的プロンプトの責務境界は、`{{cmoc-root}}/oracle/doc/app_spec/prompt_standard.md` を正本とする

## TUI 起動パラメータ

- TUI に渡す prompt と agent call parameter の詳細は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/oracle/investigation/launch_tui.py` の `build_oracle_investigation_launch_tui_parameter` を正本とし、この文書では重ねて定義しない
- `build_oracle_investigation_launch_tui_parameter` が返したパラメータを変更せずに TUI 起動へ渡す
- builder は `build_oracle_standard` の規範を固定で prompt へ注入する
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
- Codex CLI の TUI は oracle file を読み取り専用として扱い、realization file を読み書きしない
- oracle file の変更および自動 commit は行わない
