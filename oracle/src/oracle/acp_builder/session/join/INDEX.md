# `conflict_resolution.py`

## Summary
- `cmoc session join` における Git merge conflict marker 解消用の AgentCallParameter を構築する。対象パスを実パスへ解決し、conflict 対象ファイル一覧を含む prompt と、リポジトリ書き込み・最高品質モデル・最大推論 effort などの起動設定を組み立てる。

## Read this when
- `cmoc session join` の conflict marker 解消処理を変更・調査するとき
- conflict 解消エージェントへ渡す prompt、対象ファイル、作業ディレクトリ、モデル設定を確認するとき

## Do not read this when
- session join の通常処理や conflict 解消以外のサブコマンドを確認するとき
- prompt の共通生成仕様を確認したいときは、先に `build_complete_prompt` の定義を読むべき場合
- AgentCallParameter の一般的な型・列挙値の仕様だけを確認するとき

## hash
- 608a8335ede1b9cd287a4360068a4812776871888030c8c0a62dd6ebfbd84eaa
