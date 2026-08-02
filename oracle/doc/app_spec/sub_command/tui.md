
# `cmoc tui` サブコマンド

## 概要

- ユーザーから与えられたプロンプトへ cmoc 固有の契約を注入し、AI Agent CLI/TUI を起動する
- 汎用規範は installed skill に委ね、実行パラメータ選定用の agent call は行わない

## 引数

- なし

## 事前条件

- なし

## 実行手順

1. doctor preprocess を呼び出す
2. オリジナルプロンプトをユーザーからエディタ入力
3. AI Agent CLI/TUI を起動

## 「オリジナルプロンプトをユーザーからエディタ入力」の詳細

- エディタ入力の仕組みは `{{cmoc-root}}/oracle/doc/app_spec/prompt_editor_input.md` を正本とする
- エディタ編集対象ファイルの初期値は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/editor_input.py` の `build_prompt_editor_input_initial_text` で構築する
- `automatically_injected_instruction` の具体的な文面と追加内容は realization file 側の実装裁量とする

## 「AI Agent CLI/TUI を起動」の詳細

### 全バックエンド共通

- ユーザーのプロンプト入力後、`build_tui_launch_tui_parameter` で構築した固定パラメータを使用して TUI を直接起動する
- TUI 起動パラメータは `build_tui_launch_tui_parameter` を正本とする

### Codex CLI の場合

- 起動コマンドは `codex` とする (`codex exec` ではない)
- `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` から、以下の要素を持ち込む
    - 環境変数 `$CODEX_HOME`
    - preflight validation
    - Codex CLI 引数による設定上書き
