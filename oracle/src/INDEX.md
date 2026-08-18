# `oracle`

## Summary
- cmoc の oracle src 実装をまとめるディレクトリ。AI エージェント呼び出しのパラメータ契約、用途別の起動定義、prompt の構築、パスと設定の共通モデル、構造化 Markdown 生成を扱う。特定の agent call、prompt policy、oracle／realization 関連処理の入口として、まずこの階層から下位ディレクトリへ進む。

## Read this when
- AI エージェント呼び出しのモデル、reasoning effort、ファイルアクセス、cwd、Structured Output、preflight の定義を調査・変更するとき
- 完全 prompt の構築、共通 policy、placeholder、エディタ入力文面を調査・変更するとき
- agent call 間で共有するリポジトリ設定、パス解決、構造化 Markdown モデルを調査・変更するとき
- 用途別の oracle、realization、feedback、session、TUI、indexing 定義の入口を確認するとき

## Do not read this when
- oracle の正本仕様や利用規約そのものを確認したいとき
- 実際の CLI サブコマンドの処理フローや agent call 実行機構を確認したいとき
- 特定の用途別定義、prompt policy、共通モデルの本文を直接確認できる場合
- 既存 INDEX.md のルーティング情報だけを確認したいとき

## hash
- 8ea10dd9ea16c774d42861b5e02e82e65aae6f2ad7eb0e8bd4b9073d49a9ed44
