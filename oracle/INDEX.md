# `doc`

## Summary
- `oracle/doc` は、cmoc の正本仕様・設計・開発ルールを機能別に参照するための上位入口。アプリケーション仕様、branch model、採用しなかった代替案、開発ルールへ進み、実装・テスト・環境・運用上の判断に必要な根拠を探すために使う。

## Read this when
- cmoc の正本仕様や設計・開発ルールの入口を探すとき
- アプリケーションの挙動、session/run と branch の関係、採用しなかった設計案、Python 実装・環境・テストの規約を確認するとき
- 個別の仕様書や開発ルール文書へ進む先を判断するとき

## Do not read this when
- 特定機能の詳細仕様や具体的な実装・テスト手順だけを確認する場合は、対応する下位文書を直接読む
- 実行時に生成された report やその他の生成物の具体的内容だけを調査する場合は、該当する生成物を直接調べる

## hash
- aa7e5f3d1f73847735d33a8a381558edd4b8a8d23395f5527b7cc6707d3f5d97

# `src`

## Summary
- oracle の Python 実装と Structured Output 定義を集約し、agent call の起動パラメータ、prompt、policy、共通モデルを提供する。
- 下位の `acp_builder` は indexing・feedback・oracle・realization・session・TUI など用途別の agent call 構築、`prompt_builder` は共通 prompt と policy の構築、`other` はパス・設定・構造化文書の共通モデルを担う。

## Read this when
- agent call の用途別起動パラメータや Structured Output 定義を調べ、該当する `acp_builder` 配下の入口を特定するとき
- oracle／realization、ファイルアクセス、routing、feedback reporting などの共通 prompt policy を確認するとき
- agent call 間で共有される root path、設定モデル、構造化 Markdown の挙動を確認するとき

## Do not read this when
- 個別の oracle file や realization file の正本仕様を確認したいときは、対象の oracle／realization 配下を直接読む
- 特定の用途の prompt 部品や policy 本文だけを確認したいときは、`prompt_builder` 配下の担当対象を直接読む
- パス解決・設定・構造化文書の個別実装詳細だけを確認したいときは、`other` 配下の担当対象を直接読む
- 既存の INDEX.md の内容や TUI の画面表示そのものを確認したいとき

## hash
- eff4d305ece788b743c4dd47807a178030e0a03ba97b0637c0e10e6882e34e29
