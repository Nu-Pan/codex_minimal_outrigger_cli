# `conflict_resolution.py`

## Summary
- `cmoc session join` で検出された merge conflict marker を解消するための agent call parameter を組み立てる正本実装。対象パス一覧、追加の oracle file 編集許可、作業範囲、禁止事項、完了条件を含む prompt を生成する。

## Read this when
- `cmoc session join` の conflict marker 解消用 agent 呼び出し prompt の役割・制約・許可範囲を確認したいとき。
- conflict 対象ファイル一覧を prompt に渡す方法や、agent call parameter の model・reasoning effort・file access mode を確認したいとき。
- merge conflict 解消時に oracle file の最小編集を例外的に許可する条件を確認したいとき。

## Do not read this when
- 通常の session join 処理、git 操作、branch 統合、状態管理の実装を調べたいとき。
- merge conflict marker の検出方法や conflicted paths の収集方法を調べたいとき。
- 汎用 prompt builder、構造化 markdown レンダリング、path placeholder 解決の実装を調べたいとき。

## hash
- cabeb6ea53bbb3b884eec3dc2e6313d19604e19479e67bda5e1c115b33065555
