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
- `cmoc oracle edit` の TUI 起動パラメータを構築し、固定済みの完全 prompt を cmoc 管理ログへ保存する oracle src。パスコンテキスト、アクセスモード、モデル・推論設定、prompt、構造化出力設定、インデックス事前処理の起動条件をまとめて定義する。

## Read this when
- `cmoc oracle edit` の TUI 起動動作、agent call パラメータ、完全 prompt の構築または保存処理を変更・調査するとき。
- oracle file 編集用 prompt の役割、ユーザー指示の埋め込み、ファイルアクセス制約を確認するとき。

## Do not read this when
- oracle file の編集処理そのものや、一般的な prompt 構築の詳細だけを調査するときは、該当する編集処理または prompt builder を直接読む。
- TUI を起動しない agent call や、`cmoc oracle edit` 以外のサブコマンドのパラメータを調査するとき。

## hash
- 2194e8ae7c82947d9c28c3c55b7bfe2bc4a8e2375f55a746fbb20c0b2de38c55
