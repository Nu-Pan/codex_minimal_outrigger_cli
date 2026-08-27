# `oracle`

## Summary
- cmoc の oracle 関連実装を集約するソースルート。agent call のパラメータ、prompt、oracle／realization／feedback／indexing／session／TUI 向けの起動定義、共通設定・パス解決・構造化文書レンダリングを扱う。
- `acp_builder` は機能別の AgentCallParameter と Structured Output schema、`prompt_builder` は完全 prompt と各種 policy、`other` は設定・パスモデル・構造化文書、`feedback` は feedback 入力契約への入口を提供する。

## Read this when
- oracle 関連 agent call の prompt、モデル・推論設定、ファイルアクセス、cwd、indexing preflight、Structured Output schema の定義を調査または変更するとき。
- oracle、realization、feedback、indexing、session、TUI、quota probe の起動パラメータ構築を確認するとき。
- 共通 prompt の組み立て、oracle／realization policy、placeholder、設定値、パス解決、構造化 Markdown レンダリングの実装箇所を確認するとき。

## Do not read this when
- Codex CLI の実行処理やサブコマンドの外部インターフェースそのものを確認したいとき。
- oracle 文書や realization 文書の正本仕様、または個別の oracle／realization ファイルの内容を確認したいとき。
- feedback issue の検出・保存・集約や、既存 INDEX.md のルーティング内容だけを確認したいとき。

## hash
- 9330cebbd63476cdea29d656d0f418f6db253535be49f1f924147079f69e96c9
