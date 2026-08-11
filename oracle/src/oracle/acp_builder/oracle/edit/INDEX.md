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
- `cmoc oracle edit` の TUI 起動に必要な agent call パラメータを構築する。oracle 編集用の完全 prompt を生成して管理ログへ保存し、モデル、推論強度、作業ディレクトリ、ファイルアクセス権限、インデックス事前処理を固定する。

## Read this when
- `cmoc oracle edit` の TUI 起動パラメータや完全 prompt の生成処理を確認するとき。
- oracle 編集フローで agent call の作業ディレクトリ、モデル設定、ファイルアクセスモード、prompt ログ保存を確認するとき。

## Do not read this when
- oracle file の具体的な編集内容や仕様を確認するとき。
- prompt の共通構築規則や agent call パラメータの型定義を確認するときは、それぞれの担当モジュールを直接読む。

## hash
- 0372a2c28b46dc307516e2815b601aef506801d9e38295629c9e630970a2bb00
