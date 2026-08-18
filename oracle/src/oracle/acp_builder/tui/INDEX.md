# `launch_tui.py`

## Summary
- `cmoc tui` サブコマンド向けに、作業プロンプトへ必要な動的情報と各種ポリシーを組み込み、Codex CLI の TUI 起動パラメータを固定値として構築するモジュール。プロンプト生成、リポジトリ作業ディレクトリの確定、モデル・推論設定、アクセスモード、インデックス前処理の設定を確認する入口。

## Read this when
- `cmoc tui` の TUI 起動設定、起動時に渡す完全プロンプト、モデルや推論強度などの固定パラメータを調査・変更するとき。
- TUI 用 agent call の作業ディレクトリ、リポジトリ書き込み権限、ルーティングや oracle/realization 関連ポリシーの組み込み方を確認するとき。

## Do not read this when
- TUI 起動パラメータではなく、完全プロンプトの共通生成規則そのものを調査するときは、`build_complete_prompt` の定義を直接読む。
- プロンプト本文の構造化ドキュメント表現だけを調査するときは、`SDTagBlock`、`SDHeader`、`render_sd_node_as_markdown` の定義を直接読む。
- agent call の基本パラメータ型や列挙値の仕様だけを調査するときは、`oracle.acp_builder.basic` を直接読む。
- エディタ入力のコメント除去や strip など、呼び出し側で完了すると仮定されている前処理を調査するときは、このモジュールではなく該当する呼び出し側を読む。

## hash
- b3549125e3df00ec177253d723e52f8b96846f1f022cfb4634ec7a98118534d6
