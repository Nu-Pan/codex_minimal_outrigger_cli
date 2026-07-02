# `conflict_resolution.py`

## Summary
- `cmoc session join` で検出された merge conflict marker の解消を AI エージェントに依頼するための呼び出しパラメータを組み立てる oracle src。conflict 対象パスを実パスへ解決し、解消対象一覧・追加アクセス規則・oracle/realization 標準を含む完全 prompt を生成する。

## Read this when
- `cmoc session join` の conflict marker 解消用 agent call の role、summary、goal、アクセス権限、対象ファイル提示の意図を確認したいとき。
- merge conflict marker 解消作業で oracle file の最小編集を例外的に許可する条件や、git add/git commit を禁止する prompt 仕様を確認したいとき。
- conflicted_paths から prompt 内の対象ファイル一覧を作る処理や、生成される AgentCallParameter の model・reasoning・file access mode を確認したいとき。

## Do not read this when
- 通常の `cmoc session join` 全体の制御フロー、merge 実行、conflict 検出、作業結果の取り込みを確認したいとき。
- merge conflict marker の具体的な解消アルゴリズムや、個別ファイル内容のマージ方針を確認したいとき。
- agent call parameter の基礎データ構造、prompt builder、パスモデル自体の定義を確認したいとき。

## hash
- cabeb6ea53bbb3b884eec3dc2e6313d19604e19479e67bda5e1c115b33065555
