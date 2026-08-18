# `join`

## Summary
- `cmoc session join` の Git merge conflict marker 解消処理で使う AgentCallParameter を構築する実装。conflict 対象パスを実パスへ解決し、対象ファイルと編集方針を含む prompt、リポジトリ書き込み権限、main worktree の作業ディレクトリ、最高品質モデル・最大推論 effort などの起動設定をまとめる。

## Read this when
- `cmoc session join` の conflict marker 解消処理を変更・調査するとき
- conflict 解消エージェントへ渡す対象ファイル、prompt、作業ディレクトリ、モデルや推論設定を確認するとき

## Do not read this when
- session join の通常処理や conflict marker 解消以外の処理を確認するとき
- 共通 prompt 生成処理の仕様を確認するとき
- AgentCallParameter の一般的な型や設定値の仕様だけを確認するとき

## hash
- 4650582226c732aa9728d64d5c2bfed520fed7d44c4b5c4b4a482d5aaade9b8a
