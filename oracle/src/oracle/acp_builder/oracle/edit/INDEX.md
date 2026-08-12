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
- `cmoc oracle edit` の TUI 起動パラメータと、oracle 編集用の完全プロンプト生成・ログ保存を定義する。
- oracle 編集コマンドの起動設定や、編集担当 agent call のプロンプト・権限・実行環境を確認する際の入口となる。

## Read this when
- `cmoc oracle edit` の TUI 起動パラメータを確認・変更するとき
- oracle 編集用完全プロンプトの生成内容やユーザー指示の組み込み方を確認するとき
- 編集担当 agent call のモデル、推論強度、ファイルアクセス範囲、作業ディレクトリ、インデックス事前処理、プロンプトログ保存を確認するとき

## Do not read this when
- oracle file の具体的な編集内容や realization 実装を確認するとき
- `cmoc oracle edit` 以外のコマンドの起動パラメータを確認するとき
- agent call の共通データ型や TUI の一般実装だけを確認するとき

## hash
- d317aa6ec6136f46d58c0d115dcb64ee38d6f34a305da897895017fedbc31fb8
