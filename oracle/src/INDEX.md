# `oracle`

## Summary
- cmoc の正本実装断片を扱う領域。AI agent call parameter、prompt 構築、リポジトリ設定、パス表記、規範データ構造、Markdown レンダリングなど、複数の realization 実装が参照する仕様断片への入口になる。
- CLI サブコマンドの実行制御そのものではなく、agent call の入力契約・出力契約、共通プロンプト部品、横断的な補助概念を確認するためのまとまり。

## Read this when
- cmoc が AI agent call に渡す prompt、Structured Output schema、モデル設定、reasoning effort、cwd、ファイルアクセス権限、preflight 設定を確認したいとき。
- agent call 用プロンプトの構築順序、静的部分と動的部分の分離、ファイルアクセス規則や各種標準文書の注入方法を確認したいとき。
- リポジトリ別設定、ルートパスプレースホルダ、正本文書モデル、構造化文書から Markdown へのレンダリング helper など、横断的な正本実装断片を探すとき。
- INDEX.md エントリー生成、oracle file レビュー、fork 適用後レビュー、session join の conflict marker 解消、TUI 起動前後の agent call parameter 選定に関する正本仕様断片を確認したいとき。

## Do not read this when
- CLI 引数処理、branch 操作、diff 取得、merge 実行、保存処理、表示整形など、サブコマンドの実行制御実装を直接調べたいとき。
- oracle file と realization file の管理方針、文書品質基準、レビュー基準などの標準文書本文だけを確認したいとき。
- バックエンド API へ送る実際のリクエスト形式、具体的なモデル名解決、agent CLI 実行処理など realization implementation 側の詳細を調べたいとき。
- 実装ファイルやテストファイルの現在構造を把握して直接修正したいだけで、正本実装断片や prompt 生成に関係しないとき。

## hash
- 2ec6e1274c29243bfdaf28e69ce5a714889a8ad7db4c796e43f0cb99f5a69432
