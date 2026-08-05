# `conflict_resolution.py`

## Summary
- `cmoc session join` における merge conflict marker 解消用の AI エージェント呼び出しパラメータを構築する。対象パスを解決し、競合解消専用プロンプト、最高品質のモデル設定、リポジトリ書き込み権限、作業ディレクトリなどをまとめて返す。

## Read this when
- `cmoc session join` の merge conflict 解消フローや、その agent call パラメータを変更・調査するとき
- 競合対象ファイルのパス解決、プロンプト内容、モデル・推論設定、preflight 実行設定を確認するとき

## Do not read this when
- merge conflict の実際の解消ロジックや git 操作そのものを調査するとき
- `session join` と無関係な agent call パラメータやプロンプト生成処理を調査するとき

## hash
- 298180d01535b5ff6cd3f62add67a2daeadcaecf749325c48db17b9ddbaf7a9e
