# `launch_tui.py`

## Summary
- `cmoc oracle investigation` の調査用 TUI 起動パラメータを構築する関数を定義する。リポジトリルートを作業ディレクトリとして確定し、ユーザー指示を埋め込んだ完全プロンプトを生成・ログ保存したうえで、モデル、推論強度、読み取り専用権限、構造化出力設定、インデックス事前処理を含む起動パラメータを返す。oracle 調査の起動経路を確認する必要がある場合の実装入口である。

## Read this when
- `cmoc oracle investigation` の TUI 起動設定を変更・確認するとき
- oracle file 調査用の完全プロンプト生成、保存先、または Codex CLI 起動パラメータの構築を追跡するとき
- 調査エージェントの作業ディレクトリ、ファイルアクセスモード、モデル設定、推論設定を確認するとき

## Do not read this when
- 通常の oracle file 調査内容や正本仕様を確認したいときは、まず対象の oracle file とそのルーティング情報を読む
- 一般的な TUI 起動や別の agent call のパラメータを確認するときは、該当する起動パラメータ実装へ直接進む
- プロンプト本文の共通構造を変更・確認するときは、この個別起動定義ではなく共通の prompt builder を読む

## hash
- 9f8e00c3ec2f32aeb2fd12ea98eb0eda857092600844f7ca405eaa069e5d8a5d
