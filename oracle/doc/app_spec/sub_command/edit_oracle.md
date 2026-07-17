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
3. `build_edit_oracle_launch_tui_parameter` で TUI 起動パラメータを構築する
4. 構築したパラメータで Codex CLI の TUI を起動する

## ユーザー指示の入力

- エディタの選択、`code` に付けるオプション、編集対象ファイル、入力完了の判定、コメント除去、前後の空白文字除去は、`cmoc tui` の「オリジナルプロンプトをユーザーからエディタ入力」と同じとする
- 編集対象ファイルの初期値だけは、`cmoc tui` の初期値に代えて以下を使う
    ```markdown
    <!-- 最終的に oracle file がどうあるべきかを書いてください。 -->
    ```
- コメント除去と前後の空白文字除去を行った結果が空の場合はエラー終了する

## TUI 起動パラメータ

- TUI に渡す prompt と agent call parameter の詳細は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/edit/oracle/launch_tui.py` の `build_edit_oracle_launch_tui_parameter` を正本とし、この文書では重ねて定義しない
- `build_edit_oracle_launch_tui_parameter` が返したパラメータを変更せずに TUI 起動へ渡す
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
