# `oracle`

## Summary
- `oracle` 配下の正本仕様断片を用途別に辿るための入口。`acp_builder`、`other`、`prompt_builder` などの下位領域へ進む前に、どの責務を読むべきかを絞り込む。

## Read this when
- `oracle` 配下のどの領域を読むべきか、まず入口を絞りたい。
- builder 間で共有する概念、型、出力契約、各サブコマンドの prompt や実行条件のどれを確認すべきか整理したい。
- agent call 用プロンプトの構成要素や、共通規範の注入位置を確認したい。
- 設定、パス表現、文書モデル、Markdown レンダリング補助の基礎を確認したい。

## Do not read this when
- 個別の実装詳細やテストの中身だけを確認したい。
- `oracle` 以外の仕様を探している。
- 既に読む対象の下位領域が特定できていて、この入口で再度絞り込みたくない。

## hash
- 0b5d562c344b17a15c5eddf0854b51e172ce3685d96bf60da788b8d534c43199
