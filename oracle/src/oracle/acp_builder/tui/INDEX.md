# `launch_tui.py`

## Summary
- `cmoc tui` の TUI 起動に必要な AgentCallParameter を構築する。
- ユーザー入力を埋め込んだ完全プロンプトを生成し、リポジトリ書き込み権限、リポジトリルートの作業ディレクトリ、インデックス事前処理を含む起動条件を定義する。

## Read this when
- `cmoc tui` が AI Agent CLI/TUI を起動する際のプロンプト文面と起動パラメータの生成経路を確認したいとき。
- オリジナルプロンプト、パスコンテキスト、ファイルアクセスモードなどを TUI 起動設定へ組み立てる処理を調べるとき。

## Do not read this when
- 完全プロンプトの共通構造や各種ポリシーの定義だけを確認したいときは、`build_complete_prompt` などのプロンプト構築側を直接読む。
- TUI 起動後の実行処理や、`cmoc tui` 以外のサブコマンドのパラメータ構築を確認したいとき。

## hash
- 0d56bd651b99cd6cccfcb1b10eba21609bd3bd9aeae6afc70ceb74f9bed26354
