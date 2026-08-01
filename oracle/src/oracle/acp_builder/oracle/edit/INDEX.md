# `fork`

## Summary
- 現時点で本文ファイルを含まない空のディレクトリです。

## Read this when
- このディレクトリにファイルが追加され、その内容や用途を確認する必要があるとき。

## Do not read this when
- このディレクトリ配下の具体的なファイルを直接確認できる場合。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `launch_tui.py`

## Summary
- `cmoc oracle edit` の TUI 起動用パラメータを構築する oracle src。リポジトリルートを作業ディレクトリとして確定し、ユーザー指示を埋め込んだ完全 prompt を生成・保存して、固定モデル設定とともに Codex CLI 起動用の AgentCallParameter を返す。

## Read this when
- `cmoc oracle edit` の TUI 起動条件、完全 prompt の構成、prompt ログ保存先、または起動パラメータを変更・確認するとき。
- oracle file 編集用 agent call の role、summary、goal、アクセスモード、モデル、推論設定を確認するとき。

## Do not read this when
- oracle file 編集そのものの仕様や編集処理を確認したいときは、生成される完全 prompt や対象の oracle file を直接読む。
- 一般的な prompt 構築処理、構造化文書のレンダリング、パス解決の実装を確認したいときは、それぞれの担当モジュールを直接読む。

## hash
- 6908bbefb338c0ca16f4d90a22f97fa862f2690f9140558b702dfc6dc50474e0
