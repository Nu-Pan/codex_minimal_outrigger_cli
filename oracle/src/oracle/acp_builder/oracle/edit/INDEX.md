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
- `cmoc oracle edit` の TUI 起動パラメータを構築する実装。リポジトリルートを作業ディレクトリとして確定し、固定の完全 prompt を生成・ログ保存したうえで、Codex CLI 起動用の agent call パラメータを返す。prompt 構成、oracle 限定のアクセスモード、モデル・推論設定、indexing preflight の指定を確認したい場合の入口。

## Read this when
- `cmoc oracle edit` の TUI 起動設定や agent call パラメータの生成を変更・確認するとき。
- 完全 prompt の保存先、prompt の動的ブロック、または起動時の作業ディレクトリと実行設定を確認するとき。

## Do not read this when
- oracle file の編集内容や realization 側の実装を確認するだけの場合。
- prompt の共通構築ロジック自体を確認する場合は、prompt builder の対象ファイルを直接読む。

## hash
- 8451420acd74cd23f7e6c4b0533e2e32b6fc808c5d6ceac0131a95fe07df22c3
