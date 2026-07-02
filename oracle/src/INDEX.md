# `oracle`

## Summary
- cmoc の正本実装断片を収める領域で、agent call parameter、完全プロンプト構築、設定・パス・規範文書・Markdown レンダリングなどの基礎モデルへの入口になる。
- AI 呼び出し仕様を扱う領域、複数領域から参照される補助モデル、プロンプト組み立て規範を扱う領域へ進むための分岐点になる。

## Read this when
- cmoc の oracle src として記述された実装・設定・型・builder・helper の正本仕様断片を確認・変更したいとき。
- AI agent 呼び出しに渡す AgentCallParameter、Structured Output schema、モデル設定、推論強度、prompt、ファイルアクセスモードの仕様入口を探したいとき。
- 完全プロンプトの構成、oracle/realization standard や file access rule などの規範注入、プレースホルダ定義の扱いを確認したいとき。
- cmoc の設定既定値、リポジトリ別設定、ルートプレースホルダ付きパス、規範文書モデル、構造化 Markdown レンダリング helper を確認したいとき。

## Do not read this when
- oracle src ではなく、利用者向け CLI の実行フロー、プロセス起動、git 操作、状態管理、結果表示など realization implementation を調べたいとき。
- 自然言語の正本仕様文書、oracle/realization/index entry/file access rule などの規範本文そのものを読みたいとき。
- 個別の修正 diff、実際のパッチ内容、レビュー結果の集約、TUI 入力処理、merge conflict marker 検出などの実装箇所を探しているとき。

## hash
- 8f6d36dfb45a1b4240b4f91e89bcbe6ebf55cfcdafaf84500fdbae302013b2cf
