
# `cmoc tui` サブコマンド

## 概要

- ユーザーから与えられたプロンプトへ cmoc 固有の契約を注入し、AI Agent CLI/TUI を起動する
- installed skill の有無にかかわらず解釈できる、適用条件付きの cmoc 基本規範を固定で注入する
- 実行パラメータまたは注入規範を選定するための agent call は行わない

## 引数

- なし

## 事前条件

- なし

## 実行手順

1. doctor preprocess を呼び出す
2. `build_tui_launch_tui_parameter` へ `{{original-prompt-here}}` を渡し、完全プロンプトの skeleton と固定起動パラメータを構築する
3. skeleton を初期値として、オリジナルプロンプトをユーザーからエディタ入力する
4. オリジナルプロンプトを skeleton へ挿入し、完全プロンプトを確定する
5. 固定起動パラメータで AI Agent CLI/TUI を起動する

## 「オリジナルプロンプトをユーザーからエディタ入力」の詳細

- エディタ入力の仕組みは `{{cmoc-root}}/oracle/doc/app_spec/prompt_editor_input.md` を正本とする
- エディタ編集対象ファイルの初期値は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/editor_input.py` の `build_prompt_editor_input_initial_text` で構築する
- 初期値へ渡す skeleton と、編集後に確定する完全プロンプトは、`build_tui_launch_tui_parameter` が構築した同じ完全プロンプトを使用する

## 「AI Agent CLI/TUI を起動」の詳細

### 全バックエンド共通

- ユーザーのプロンプト入力前に `build_tui_launch_tui_parameter` で構築した固定パラメータを、完全プロンプトの確定後に使用して TUI を直接起動する
- TUI 起動パラメータは `build_tui_launch_tui_parameter` を正本とする
- builder は次の規範を、オリジナルプロンプトの内容によらず固定で注入する
    - `build_oracle_standard`
    - `build_realization_standard`
    - `build_oracle_review_standard`
    - `build_apply_review_standard`
    - `build_realization_oracle_reference_rule`
- 各規範は自身が明示する適用条件に該当する場合だけ、オリジナルプロンプトの作業へ適用する
- installed skill は任意の追加規範として利用してよいが、cmoc 固有契約と競合する場合は cmoc 固有契約を優先する
- builder は model class を `FLAGSHIP`、reasoning effort を `MAX`、file access mode を `REPO_WRITE` とする
- Structured Output は要求しない
- TUI 起動前の indexing preflight を行う
- 共通 feedback instruction、TUI process の collector context、および accepted observation の保持は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` に従う
- このサブコマンドの TUI agent turn と終了時の Windows toast 通知は、`{{cmoc-root}}/oracle/doc/app_spec/windows_toast_notification.md` を正本とする

### Codex CLI の場合

- 起動コマンドは `codex` とする (`codex exec` ではない)
- `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` から、以下の要素を持ち込む
    - 環境変数 `$CODEX_HOME`
    - preflight validation
    - Codex CLI 引数による設定上書き
