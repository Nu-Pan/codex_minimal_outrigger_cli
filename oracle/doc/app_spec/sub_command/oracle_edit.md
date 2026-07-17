# `cmoc oracle edit`

## 概要

- oracle file の最終状態に関するユーザー指示をエディタから受け取り、その指示を渡して Codex CLI の TUI を起動する

## 引数

- なし

## 事前条件

- なし

## 実行手順

1. doctor preprocess を呼び出す
2. oracle file の最終状態に関するユーザー指示をエディタから受け取る
3. `build_oracle_edit_launch_tui_parameter` で TUI 起動パラメータを構築する
4. 構築したパラメータで Codex CLI の TUI を起動する

## ユーザー指示の入力

- エディタ入力の仕組みは `{{cmoc-root}}/oracle/doc/app_spec/prompt_editor_input.md` を正本とする
- エディタ編集対象ファイルの初期値として、以下に示す `cmoc oracle edit` 固有コメントを追加注入する
    ```markdown
    <!--
    以下の指示は `cmoc oracle edit` で自動注入されるため、このファイルに書いてはいけない。

    - realization file の読み書き禁止
    - oracle file の規約・規範
    - TODO
    -->
    ```

## TUI 起動パラメータ

- TUI に渡す prompt と agent call parameter の詳細は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/oracle/edit/launch_tui.py` の `build_oracle_edit_launch_tui_parameter` を正本とし、この文書では重ねて定義しない
- `build_oracle_edit_launch_tui_parameter` が返したパラメータを変更せずに TUI 起動へ渡す
- `cmoc tui` のような実行パラメータ決定用 agent call は行わない

## Codex CLI の起動

- 起動コマンドは `codex` とする
- `codex exec` は使用しない
- `cmoc tui` の「Codex CLI の場合」と同じく、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` から以下の要素を持ち込む
    - 環境変数 `$CODEX_HOME`
    - preflight validation
    - Codex CLI 引数による設定上書き

## 変更の扱い

- Codex CLI の TUI が行った oracle file の変更は自動で commit しない
