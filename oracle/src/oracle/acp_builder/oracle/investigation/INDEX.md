# `launch_tui.py`

## Summary
- `cmoc oracle investigation` の TUI 起動パラメータを構築する関数。ユーザー指示を完全プロンプトへ組み込み、oracle 調査用の固定モデル・最大推論強度・読み取り専用 oracle 範囲・リポジトリルート起点・インデックス事前処理を設定する。

## Read this when
- `cmoc oracle investigation` の TUI 起動設定や、oracle file 調査用エージェントの起動パラメータを確認・変更するとき。
- ユーザー指示を調査用の完全プロンプトへ渡す構築経路を確認するとき。

## Do not read this when
- oracle 調査プロンプトの一般仕様を確認するときは、完全プロンプトを構築する定義元を直接読む。
- TUI 起動以外の prompt builder、パス解決、構造化文書レンダリングの仕様を確認するときは、それぞれの定義元を直接読む。

## hash
- 78ca332d21909a72e08b9a1994b770a94922c2853da76a3eb1b2ff6b4fa51298
