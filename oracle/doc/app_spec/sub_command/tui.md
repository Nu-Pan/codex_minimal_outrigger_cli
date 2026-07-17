
# `cmoc tui` サブコマンド

## 概要

- ユーザーから与えられたプロンプトと cmoc の自動生成プロンプトを注入した状態で AI Agent CLI/TUI を起動する
- cmoc に実装されている規則・規範の上で任意のプロンプトを実行するための仕組み

## 引数

- なし

## 事前条件

- なし

## 実行手順

1. doctor preprocess を呼び出す
2. オリジナルプロンプトをユーザーからエディタ入力
3. 必要なパラメータを agent call で決定
4. AI Agent CLI/TUI を起動

## 「オリジナルプロンプトをユーザーからエディタ入力」の詳細

- エディタ入力の仕組みは `{{cmoc-root}}/oracle/doc/app_spec/prompt_editor_input.md` を正本とする

## 「必要なパラメータを agent call で決定」の詳細

- `cmoc tui` で必要になるパラメータの大半は agent call で決定する
- agent call の詳細仕様は `build_tui_resolve_parameter_parameter` を正本とする

## 「AI Agent CLI/TUI を起動」の詳細

### 全バックエンド共通

- TUI 起動パラメータは `build_tui_launch_tui_parameter` を正本とする

### Codex CLI の場合

- 起動コマンドは `codex` とする (`codex exec` ではない)
- `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` から、以下の要素を持ち込む
    - 環境変数 `$CODEX_HOME`
    - preflight validation
    - Codex CLI 引数による設定上書き
