# `launch_tui.py`

## Summary
- `cmoc tui` が受け取ったオリジナルプロンプトから完全プロンプトを構築し、Codex CLI の TUI 起動に渡す固定パラメータを定義する。
- リポジトリルートを agent_call_cwd として確定し、モデル・推論強度・ファイルアクセスモード・起動前インデックス処理を設定する。
- TUI 起動パラメータの構築経路を確認する際の、`oracle/src/oracle/acp_builder/tui` 配下における実装上の入口である。

## Read this when
- `cmoc tui` の TUI 起動設定を変更・確認するとき。
- オリジナルプロンプトの埋め込み、完全プロンプト生成、または TUI 起動用 `AgentCallParameter` の固定値を調査するとき。
- agent_call_cwd、モデル設定、推論強度、ファイルアクセスモード、インデックス処理の設定根拠を確認するとき。

## Do not read this when
- 完全プロンプトの共通生成規則を確認したいときは、`build_complete_prompt` の定義を直接読む。
- TUI の画面表示、入力編集、対話操作の実装を確認したいときは、該当する TUI 実装を直接読む。
- `AgentCallParameter` や列挙型の一般的な仕様を確認したいときは、各型の定義を直接読む。

## hash
- d236a892d55e67917eccd8fff4ec7c654b7d9a20d9b00165213dfda56de18e44
