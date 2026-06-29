# `conflict_resolution.py`

## Summary
- `cmoc session join` で merge conflict marker を解消する AI エージェント呼び出しパラメータの正本仕様断片。対象パス一覧、作業範囲、ファイルアクセス権限、禁止事項を含む complete prompt を組み立てる。

## Read this when
- session join の merge conflict marker 解消用 agent call の役割、goal、許可される編集範囲を確認したいとき。
- conflict marker 解消作業で oracle file の編集を例外的に許可する条件を確認したいとき。
- merge conflict 解消用 prompt に渡す対象ファイル一覧や file access profile の構成意図を確認したいとき。

## Do not read this when
- 通常の session join 処理や git 操作全般の実装を確認したいとき。
- merge conflict marker の検出方法や conflicted path の収集処理を確認したいとき。
- complete prompt の共通組み立て仕様、構造化ドキュメント表現、パス解決の詳細を確認したいとき。

## hash
- 9b416d5963fe8758027f83c7bc6667ae94a50d65e5a06652e58f49eeac25db2b
