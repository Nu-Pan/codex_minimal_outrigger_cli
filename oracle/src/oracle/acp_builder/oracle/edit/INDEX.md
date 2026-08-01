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
- `cmoc oracle edit` の TUI 起動パラメータを構築する実装。リポジトリルートを作業ディレクトリとして確定し、固定要件とユーザー指示を含む完全 prompt を生成・保存したうえで、Codex CLI 起動用のパラメータを返す。

## Read this when
- `cmoc oracle edit` の TUI 起動処理、起動時 prompt、oracle file 編集用の agent call パラメータを変更・調査するとき。
- 完全 prompt の構成、保存先、モデル・推論設定、ファイルアクセスモード、作業ディレクトリの指定を確認するとき。

## Do not read this when
- oracle file の編集内容や仕様そのものを変更・調査するときは、対象となる `oracle` 側の仕様ファイルを直接読む。
- TUI 起動以外の agent call や prompt 構築処理を変更・調査するときは、それぞれの担当モジュールを直接読む。

## hash
- a80dc9e253f62767faf3ea83df60dc35528bbe5801af38eeb061d883360665d0
