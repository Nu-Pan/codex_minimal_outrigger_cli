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
- `cmoc oracle edit` 用の TUI 起動パラメータを構築する oracle src。完全な編集 prompt の生成・ログ保存と、モデル、権限、作業ディレクトリなど固定された起動条件の指定を担う。

## Read this when
- `cmoc oracle edit` の TUI 起動方法、編集 prompt の構成、または oracle file 編集用の agent 起動設定を変更・確認するとき。

## Do not read this when
- oracle file の編集処理そのもの、prompt の共通生成規則、パス解決、構造化文書のレンダリングを変更・確認するときは、それぞれの担当モジュールを直接読む。

## hash
- 8fb4ccce29dcf1b377a317fb58eaa990e443a90e5b1125f03c3e104593d8bcaf
