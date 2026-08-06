# `launch_tui.py`

## Summary
- `cmoc oracle investigation` の TUI 起動パラメータを構築する関数を定義する正本実装。oracle file 調査用の完全プロンプトを生成し、cmoc 管理下のログへ保存したうえで、モデル・権限・作業ディレクトリなどを固定した `AgentCallParameter` を返す。

## Read this when
- `cmoc oracle investigation` の TUI 起動条件、調査用プロンプト、または起動パラメータの構成を変更・確認するとき。
- ユーザー指示を埋め込んだ完全プロンプトの生成と、起動前ログ保存の流れを確認するとき。

## Do not read this when
- oracle file 調査そのものの仕様や、完全プロンプト共通の構造を確認したいときは、対応する oracle 文書やプロンプト構築実装を直接読む。
- 一般的な `AgentCallParameter` の型定義やファイルアクセスモードの意味だけを確認したいときは、基礎型定義を直接読む。

## hash
- 42189e24aeca1ae0e6c98b20e17d53ec820d91c682da8c2fc2487e109ddc6034
