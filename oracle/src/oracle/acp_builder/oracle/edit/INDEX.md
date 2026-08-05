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
- `cmoc oracle edit` の TUI 起動用パラメータを構築する oracle src。パスコンテキスト、固定完全 prompt、ログ保存、モデル・権限・起動設定を組み立てる実装であり、oracle 編集起動フローの入口となる。

## Read this when
- `cmoc oracle edit` の TUI 起動処理、起動時 prompt、oracle 編集用ファイルアクセス権限、モデルや実行設定を確認・変更するとき。

## Do not read this when
- oracle file の編集内容や編集 agent の一般的な prompt 仕様だけを確認したいときは、関連する prompt builder や oracle 仕様ファイルを直接読む。
- TUI 起動後の agent 処理、oracle file の編集ロジック、ログ解析を調べるとき。

## hash
- dfcda7b79c338ddff78034ac5ad94f9c26210703cfa05d6d6fee565f2d8d8a42
