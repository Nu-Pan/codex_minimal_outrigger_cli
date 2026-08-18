# `launch_tui.py`

## Summary
- `cmoc oracle investigation` の TUI 起動用パラメータを構築する関数を提供する。ユーザーの oracle file 調査指示を完全プロンプトへ組み込み、oracle 調査向けの読み取り専用設定、モデル、推論強度、作業ディレクトリ、インデックス事前処理を含む `AgentCallParameter` を返す。
- oracle 調査コマンドの起動条件や、調査プロンプトと TUI 起動パラメータの固定定義を確認するための入口である。

## Read this when
- `cmoc oracle investigation` の TUI 起動設定を変更・確認するとき
- oracle file 調査用プロンプトの組み立て方や、ユーザー指示の埋め込み位置を確認するとき
- oracle 調査用のファイルアクセスモード、作業ディレクトリ、モデル設定、インデックス事前処理の構成を確認するとき

## Do not read this when
- oracle file 自体の内容や調査結果を確認したい場合は、対象の oracle file を直接読むとき
- 完全プロンプトの共通生成規則だけを確認したい場合は、`build_complete_prompt` の定義を直接読むとき
- `AgentCallParameter` など起動パラメータの型定義だけを確認したい場合は、該当する基本定義を直接読むとき

## hash
- ae85204b05c27b75a3d5957860372cf0f9ec40a4d5590edd3d829902a0552c2d
