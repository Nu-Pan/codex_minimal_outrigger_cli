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
- `cmoc oracle edit` の TUI 起動用パラメータを構築する oracle src。リポジトリルートを作業ディレクトリとして確定し、固定プロンプト、oracle 専用アクセスモード、モデル設定、構造化出力設定などを組み立てる。生成した完全プロンプトを cmoc 管理ログへ保存する処理も含む。

## Read this when
- `cmoc oracle edit` の TUI 起動パラメータ、完全プロンプトの構築内容、oracle 編集時のパスコンテキストやアクセスモードを確認・変更するとき。

## Do not read this when
- oracle file の編集内容や編集エージェントの一般的な役割を確認したいときは、生成対象の oracle file やプロンプト構築の共通実装を直接読む。
- realization 側の CLI 動作や TUI 実装を確認・変更するとき。

## hash
- bf23969eb867a0bbb2d86fa255abac221dfccc0177a2d673dfc398817bf2a110
