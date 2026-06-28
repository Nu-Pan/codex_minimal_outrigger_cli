# `conflict_resolution.py`

## Summary
- `cmoc session join` で merge conflict marker を解消する AI エージェント呼び出しパラメータを組み立てる正本仕様断片。
- conflict 対象パスを実パスへ解決して prompt に列挙し、作業範囲を conflict marker 解消に限定する goal、oracle file への最小編集例外、git add/commit 禁止、作業後に marker を残さない条件を与える。
- 呼び出しモデル、reasoning effort、file access mode、完全 prompt 生成時に含める basic/standard 系の前提を確認する入口になる。

## Read this when
- `cmoc session join` の conflict marker 解消用エージェント prompt や呼び出しパラメータを確認・変更したいとき。
- conflict 対象ファイル一覧が prompt にどのように渡されるか、また対象パスがどの path 解決を経由するかを確認したいとき。
- merge conflict 解消作業において、編集範囲、oracle file 例外、git add/commit 禁止、marker 残存禁止などの制約を確認したいとき。
- session join が conflict marker 解消エージェントにどの model class、reasoning effort、file access mode を指定するか確認したいとき。

## Do not read this when
- `cmoc session join` 全体の制御フロー、ブランチ操作、merge 実行、conflict 検出の仕様を調べたいだけのとき。
- path keyword や実パス・work-root 解決の一般仕様を調べたいとき。
- 完全 prompt の共通組み立て処理、構造化 markdown rendering、agent parameter 型そのものの定義を調べたいとき。
- merge conflict の内容を実際にどう選んで解消するかという人間・AI の編集判断ルールを、session join 用 prompt 以外から調べたいとき。

## hash
- cabeb6ea53bbb3b884eec3dc2e6313d19604e19479e67bda5e1c115b33065555
