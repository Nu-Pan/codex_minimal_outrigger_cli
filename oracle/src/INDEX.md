# `oracle`

## Summary
- cmoc の oracle 資産を集約するディレクトリ。feedback の入力契約、agent call の起動パラメータと用途別 Structured Output schema、oracle／realization 用 prompt policy、パス・設定・構造化 Markdown の共通実装を扱う。
- 下位の `acp_builder` は用途別 agent call の具体的な起動入口、`prompt_builder` は共通 prompt と policy の構築、`other` は設定・パス解決・構造化文書モデル、`feedback` は feedback reporter 入力契約の入口として利用する。

## Read this when
- oracle／realization、feedback、indexing、session、TUI などの agent call 経路を横断して、どの下位ディレクトリの起動定義・prompt・出力契約を読むべきか判断するとき
- agent call の prompt に共通で適用される oracle／realization／file access／routing などの policy 構成を確認するとき
- root placeholder を含むパス解決、agent call の work root・repository root、cmoc 設定モデル、構造化 Markdown ノードの共通挙動を確認するとき
- feedback reporter が collector に渡す問題分類・重要度・影響・原因・根拠・継続状態の入力形式を確認するとき

## Do not read this when
- 具体的な oracle file や realization 実装・テストの正本仕様だけを確認したいときは、該当する oracle／realization 対象を直接読む
- 個別 agent call の詳細な起動パラメータ、prompt、Structured Output schema を確認したいときは、`acp_builder` 配下の担当対象を直接読む
- 共通 prompt の部品・policy の本文や prompt 生成・placeholder 統合ロジックだけを確認したいときは、`prompt_builder` 配下を直接読む
- 設定値・パス解決・構造化 Markdown の実装詳細だけを確認したいときは、`other` 配下を直接読む
- feedback の保存・集約・重複判定や、問題検出後の継続判断だけを確認したいときは、このディレクトリの入力契約ではなく担当処理を読む
- 既存 INDEX.md の内容や、TUI の画面表示そのものを確認したいとき

## hash
- c0aebf2a1271834717b651222aa3afa45a51ba6c3eb044735ba61010b6de2a31
