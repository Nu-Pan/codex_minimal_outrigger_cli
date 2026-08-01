# `launch_tui.py`

## Summary
- `cmoc oracle investigation` の TUI 起動用パラメータを構築する oracle src。ユーザー指示を埋め込んだ完全プロンプトを生成・ログ保存し、固定のモデル、権限、作業ディレクトリ、インデックス事前処理を指定した `AgentCallParameter` を返す。oracle investigation の起動仕様を確認・変更する際の実装入口。

## Read this when
- `cmoc oracle investigation` の TUI 起動動作、起動パラメータ、完全プロンプトの構築・保存方法を調査するとき
- oracle investigation の起動時に使われるモデル、推論強度、ファイルアクセスモード、cwd、構造化出力設定、インデックス事前処理を確認するとき
- ユーザー指示のプロンプトへの埋め込みや、cmoc 管理ログへの保存処理を変更するとき

## Do not read this when
- oracle investigation の調査内容そのものや oracle file の正本仕様を確認したいときは、`oracle` 配下の調査対象文書を直接読む
- TUI 起動以外の agent call パラメータ生成や、共通プロンプト構築の仕様だけを確認したいときは、それぞれの担当モジュールを直接読む

## hash
- 03905eaf2e173c2e064519f4b8299b598d3c85cfb6c29fde3fdf8e1170f84ce5
