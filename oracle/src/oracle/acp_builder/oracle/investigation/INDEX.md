# `launch_tui.py`

## Summary
- `cmoc oracle investigation` 用の TUI 起動パラメータと完全プロンプトを構築する実装。ユーザー指示を調査用プロンプトへ組み込み、oracle 調査向けの固定設定、作業パス、読み取り専用アクセス、構造化出力設定、インデックス事前処理をまとめて返す。oracle investigation の起動条件や prompt builder との連携を変更・確認する際の入口。

## Read this when
- `cmoc oracle investigation` の TUI 起動設定、モデル・推論設定、ファイルアクセスモード、作業ディレクトリ、インデックス事前処理を変更するとき。
- oracle file 調査用の完全プロンプトに、調査対象のユーザー指示や標準プロンプト設定を組み込む処理を確認するとき。
- oracle investigation の prompt 構築結果を起動パラメータへ渡す責務の所在を確認するとき。

## Do not read this when
- oracle file の内容自体や調査結果の正本仕様を確認したい場合は、`oracle` 配下の対象ファイルを直接読む。
- 一般的な TUI 起動処理や他の agent call 種別の設定を確認したい場合は、それぞれの起動パラメータ実装を直接読む。
- 完全プロンプトの共通構造やレンダリング規則だけを確認したい場合は、`complete_prompt` や構造文書の実装を直接読む。

## hash
- c318f97c4cbf1f30d5d3e6668e777ed064744b74663abca73ad31219be9da839
