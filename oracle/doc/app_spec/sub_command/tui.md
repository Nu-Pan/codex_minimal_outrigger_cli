
# `cmoc tui` サブコマンド

## 概要

- ユーザーから与えられたプロンプトへ cmoc 固有の契約を注入し、AI Agent CLI/TUI を起動する
- installed skill の有無にかかわらず解釈できる、適用条件付きの cmoc 基本規定を固定で注入する
- 実行パラメータまたは注入規定を選定するための agent call は行わない

## 引数

- なし

## 事前条件

- git working tree と staging area が clean であることを事前条件にせず、いずれかに未コミット差分が存在しても実行する

## 実行手順

1. doctor preprocess を呼び出す
2. `build_tui_launch_tui_parameter` へ `{{original-prompt-here}}` を渡し、初期表示用の完全プロンプトの skeleton を構築する
3. skeleton を初期値として、オリジナルプロンプトをユーザーからエディタ入力する
4. 抽出したオリジナルプロンプトを `build_tui_launch_tui_parameter` へ渡し、完全プロンプト本文を含む起動パラメータを構築する
5. 構築した起動パラメータで AI Agent CLI/TUI を起動する

## 「オリジナルプロンプトをユーザーからエディタ入力」の詳細

- エディタ入力の仕組みは `{{cmoc-root}}/oracle/doc/app_spec/prompt_editor_input.md` を正本とする
- エディタ編集対象ファイルの初期値は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/editor_input.py` の `build_prompt_editor_input_initial_text` で構築する

## 「AI Agent CLI/TUI を起動」の詳細

### 全バックエンド共通

- ユーザーのプロンプト入力後に `build_tui_launch_tui_parameter` で構築したパラメータを変更せず、TUI を直接起動する
- TUI の意味上の責務と起動条件は本書を正本とする。`build_tui_launch_tui_parameter` は、正確な prompt 文面と TUI 起動パラメータを構築する
- builder は次の規定を、オリジナルプロンプトの内容によらず固定で注入する
    - `build_oracle_policy`
    - `build_realization_policy`
    - `build_oracle_findings_policy`
    - `build_apply_review_policy`
    - `build_realization_oracle_reference_policy`
- 各規定は自身が明示する適用条件に該当する場合だけ、オリジナルプロンプトの作業へ適用する
- oracle file と realization file の責務および適合性は `{{cmoc-root}}/oracle/doc/app_spec/misc_spec.md`、oracle review の所見成立条件は `{{cmoc-root}}/oracle/doc/app_spec/sub_command/oracle_review.md` を意味仕様の正本とする
- installed skill は任意の追加規定として利用してよいが、cmoc 固有契約と競合する場合は cmoc 固有契約を優先する
- builder は model class を `FLAGSHIP`、reasoning effort を `MAX`、file access mode を `REPO_WRITE` とする
- Structured Output は要求しない
- TUI 起動前の indexing preflight は `{{cmoc-root}}/oracle/doc/app_spec/indexing.md` に従い、git working tree または staging area に既存差分があっても実行する
- 共通 feedback instruction、TUI process の collector context、および accepted observation の保持は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` に従う
- このサブコマンドの TUI agent turn と終了時の Windows toast 通知は、`{{cmoc-root}}/oracle/doc/app_spec/windows_toast_notification.md` を正本とする

### Codex CLI の場合

- 起動コマンドは `codex` とする (`codex exec` ではない)
- `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` から、以下の要素を持ち込む
    - 環境変数 `$CODEX_HOME`
    - preflight validation
    - Codex CLI 引数による設定上書き
