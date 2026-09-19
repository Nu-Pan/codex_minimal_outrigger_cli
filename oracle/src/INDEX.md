# `oracle`

## Summary
- cmoc の oracle 実装を構成する Python モジュールと Structured Output schema の入口。agent 呼び出しパラメータ、プロンプト生成、パス・設定・構造化文書モデル、フィードバック報告、エディタ入力引き渡しを扱う。
- acp_builder は agent call のパラメータ構築と、oracle 編集・調査、realization、session、TUI、feedback、indexing 各処理の呼び出し定義をまとめる。
- prompt_builder は agent に渡す完全 prompt と、ファイルアクセス・oracle/realization・routing・index entry などのポリシー文面を組み立てる。
- other は cmoc 設定、Git worktree を含むパスモデル、構造化文書のデータモデルと Markdown レンダリングを提供する。
- editor_input_handoff は MCP 経由の入力を送信元情報付き Markdown 本文へ変換し、overwrite_input.json が入力形式を定義する。
- feedback は feedback reporter の Structured Output schema を提供し、問題分類・影響・根拠・継続状態の入力形式を定義する。

## Read this when
- oracle 実装全体の責務分担や、agent call・prompt・設定・パスモデルの入口を確認するとき
- oracle/src/oracle 配下のどの領域を読むべきか判断するとき

## Do not read this when
- 特定の agent call 実装、prompt policy、設定値、パス解決、入力本文生成の詳細を確認したいときは、該当する下位ディレクトリを直接読む
- 正本仕様文書や realization 実装・テストの内容を確認するとき

## hash
- 917c8ed879151c5799e1d0a3452c49c375cdd5f07531de71ab28f4ba69863e15
