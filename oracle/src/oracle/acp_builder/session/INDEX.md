# `join`

## Summary
- `cmoc session join` の merge conflict marker 解消用 agent call parameter を組み立てる正本実装への入口。conflict 対象パス、例外的な oracle file 編集許可、作業範囲、禁止事項、完了条件を含む prompt 生成を扱う。

## Read this when
- `cmoc session join` の conflict marker 解消用 agent 呼び出し prompt の役割、制約、許可範囲を確認したいとき。
- conflict 対象ファイル一覧を agent prompt に渡す方法や、agent call parameter の model、reasoning effort、file access mode を確認したいとき。
- merge conflict 解消時に oracle file の最小編集を例外的に許可する条件を確認したいとき。

## Do not read this when
- 通常の session join 処理、git 操作、branch 統合、状態管理の実装を調べたいとき。
- merge conflict marker の検出方法や conflicted paths の収集方法を調べたいとき。
- 汎用 prompt builder、構造化 markdown レンダリング、path placeholder 解決の実装を調べたいとき。

## hash
- eb585ddb1728ef9de0710c043ecfb5fe3bbfd187ba73ade89d3a597511649b19
