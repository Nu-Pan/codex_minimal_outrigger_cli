# `join`

## Summary
- `cmoc session join` が merge conflict marker 解消エージェントへ渡す呼び出しパラメータと prompt 制約を定める正本仕様断片の置き場。conflict 対象パスの実パス解決、prompt への列挙、編集範囲の限定、oracle file 例外、git add/commit 禁止、marker 残存禁止、model class・reasoning effort・file access mode などを確認する入口になる。

## Read this when
- `cmoc session join` の merge conflict marker 解消用エージェント呼び出しや prompt の仕様を確認・変更したいとき。
- conflict 対象ファイル一覧がどの path 解決を経由して prompt に渡されるかを確認したいとき。
- conflict 解消作業に課される編集範囲、oracle file 例外、git add/commit 禁止、marker 残存禁止などの制約を確認したいとき。
- session join が conflict marker 解消エージェントに指定する model class、reasoning effort、file access mode を確認したいとき。

## Do not read this when
- `cmoc session join` 全体の制御フロー、ブランチ操作、merge 実行、conflict 検出を調べたいだけのとき。
- path keyword、実パス、work-root 解決の一般仕様を調べたいとき。
- 完全 prompt の共通組み立て処理、構造化 markdown rendering、agent parameter 型そのものを調べたいとき。
- merge conflict の内容をどう選んで解消するかという編集判断ルールを、session join 用 prompt 以外から調べたいとき。

## hash
- eb585ddb1728ef9de0710c043ecfb5fe3bbfd187ba73ade89d3a597511649b19
