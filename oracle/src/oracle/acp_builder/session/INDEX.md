# `join`

## Summary
- `cmoc session join` の merge conflict marker 解消に用いる AI エージェント呼び出しパラメータを構築する。対象パス、専用プロンプト、モデル・推論設定、リポジトリ書き込み権限、作業ディレクトリ、preflight 実行設定をまとめて返す。

## Read this when
- `cmoc session join` の merge conflict 解消フローや agent call パラメータを変更・調査するとき
- 競合対象ファイルのパス解決、プロンプト、モデル・推論設定、preflight 実行設定を確認するとき

## Do not read this when
- merge conflict の実際の解消ロジックや git 操作そのものを調査するとき
- `session join` と無関係な agent call パラメータやプロンプト生成処理を調査するとき

## hash
- 3d057a13d4707bd9002173b98cb25026c6f71e7ff9c9ea16ebda62e6b73eff33
