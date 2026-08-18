# `launch_tui.py`

## Summary
- `cmoc oracle investigation` 用の TUI 起動パラメータを構築する実装。ユーザー指示を固定の完全プロンプトへ組み込み、oracle 調査向けの読み取り専用設定、パスコンテキスト、モデル・推論設定、インデックス事前処理を備えた `AgentCallParameter` を返す。oracle 調査起動のパラメータ仕様や完全プロンプト生成経路を確認するときの入口。

## Read this when
- `cmoc oracle investigation` の TUI 起動設定を変更・調査するとき
- oracle file 調査用プロンプトへのユーザー指示の組み込み方や、起動時のアクセスモード・モデル・作業ディレクトリを確認するとき

## Do not read this when
- 完全プロンプトの共通構造だけを調べる場合は `build_complete_prompt` の定義を直接読むとよい
- エージェント呼び出しパラメータの型や列挙値の一般仕様だけを調べる場合は `oracle.acp_builder.basic` を直接読むとよい
- oracle 調査そのものの正本仕様や対象ファイルの内容を調べる場合は、この起動ラッパーではなく該当する oracle file を直接読むとよい

## hash
- 191b4ea2d2e41b61f980111534c693af7923c9313ab587cfa227beebe53e1217
