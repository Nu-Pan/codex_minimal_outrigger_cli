# `launch_tui.py`

## Summary
- `cmoc oracle investigation` の TUI 起動パラメータを構築する実装。ユーザー指示を完全プロンプトの調査対象へ組み込み、oracle 調査用の読み取り専用アクセス、作業コンテキスト、ルーティング設定、起動前インデックス処理を指定する。

## Read this when
- `cmoc oracle investigation` の TUI 起動時に、プロンプト、ファイルアクセスモード、作業ディレクトリ、構造化出力設定、または起動前処理がどう構成されるかを確認するとき。

## Do not read this when
- oracle file の調査プロンプト本文の共通構造や oracle 調査の一般規則を確認したいとき。完全プロンプト生成処理や oracle ポリシーの定義元を直接読む方が適切。

## hash
- 2f1d0f078c90abb501958afcc5a3d04789329b06d0996cb23c947535eb337b8b
