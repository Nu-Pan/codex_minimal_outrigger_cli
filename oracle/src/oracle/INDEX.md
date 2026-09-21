# `acp_builder`

## Summary
- Codex CLI／TUI を呼び出すための AgentCallParameter と prompt を構築する oracle 実装群。
- 共通のファイルアクセスモードや呼び出し設定に加え、oracle 操作、INDEX 生成、realization 追従・修正、feedback 処理、TUI、quota probe、conflict 解消の各用途を扱う。
- 下位ディレクトリは用途別の起動パラメータ定義と Structured Output schema の入口になっている。

## Read this when
- ACP builder の共通呼び出しパラメータ、prompt 構築、アクセスモード、indexing preflight の設定を確認したいとき。
- 特定のサブコマンドがどの agent call 設定や schema を使うかを用途別に調査したいとき。
- oracle と realization の編集・調査経路、feedback remediation、session join conflict 解消の呼び出し境界を確認したいとき。

## Do not read this when
- 特定用途の詳細な prompt や出力 schema だけを確認したい場合は、該当する下位ディレクトリのファイルを直接読むとき。
- agent call の実行そのものや、正本仕様の意味を調べる場合は、この builder 群ではなく実行経路または oracle/doc の該当仕様を読むとき。
- INDEX エントリー生成の出力形式だけを確認したい場合は、indexing 配下の schema を直接読むとき。

## hash
- 0781e495a5330d8e854e6c252d0d48e9d64d26d3a163700b22cc842730efa045

# `editor_input_handoff`

## Summary
- エディター入力の引き渡しガイドを、受信先プロンプト雛形から構築する処理と入力仕様を扱う。
- 目標・依頼内容・背景・決定事項・未確定事項・oracle参照・送信元情報から、引き渡し本文を生成する正本実装を扱う。
- 引き渡し本文の上書き入力と、target指定によるガイド取得結果のJSON Schemaを提供する。

## Read this when
- エディター入力のhandoffガイドや本文の生成・構成を変更または確認するとき。
- handoff入力の必須項目、空白禁止、oracle参照、target IDの検証条件を確認するとき。
- 送信元のサブコマンド名・実行ID・Codex call ID・絶対ログパスの扱いを確認するとき。

## Do not read this when
- 受信先プロンプト雛形そのものの仕様だけを確認したいとき。
- handoff以外のMCP入力や一般的なJSON Schemaの設計を確認するとき。
- 生成済みeditor work fileの利用方法や、送信側・受信側の外部処理を直接確認したいとき。

## hash
- 81d54f916ad10b2fde754c477225f9ad30fefa2c05abfe95bc96a49d8e98575b

# `feedback`

## Summary
- フィードバック問題報告入力の正本スキーマを扱う領域で、分類・重要度・影響・未解消制約・原因・再確認用根拠・継続状態の入力契約への入口。

## Read this when
- cmoc_feedback.submit_observation に送る問題報告の入力項目、許容値、文字数制約、根拠に応じた path 条件を確認するとき。
- 問題報告を JSON として組み立てる際に、reporter input の形式と根拠記述の要件を確認するとき。

## Do not read this when
- 問題報告の送信手順や collector の処理を確認したいとき。
- reporter input のスキーマではなく、フィードバック収集結果や重複判定の実装を確認したいとき。

## hash
- 709d2b0ca7660b1772a43fe8fdaed710d40142564511ba28a435a49b6776aa67

# `other`

## Summary
- cmoc の周辺データモデルと Markdown 表現をまとめた基盤モジュール群。構造化文書ノードのレンダリング、agent call のルートパスとプレースホルダー解決、cmoc/Codex 設定の型定義、文書参照の検証・Markdown 化を扱う。これらの共通モデルや変換処理を調査・変更するときの入口となる。

## Read this when
- 構造化された文書・規定・コードブロックを Markdown に変換する処理を確認したいとき。
- agent call の cwd、Git worktree、{{repo-root}} などのパスプレースホルダー解決を確認したいとき。
- cmoc の並列数、Codex provider、model、reasoning effort などの設定データ構造を確認したいとき。
- 文書参照の絶対パス要件や、参照箇所を含む Markdown 表現を確認したいとき。

## Do not read this when
- 対象の個別機能の意味仕様や運用手順を確認したい場合は、まず oracle/doc 配下の対応する正本仕様を読む。
- 実際の agent 呼び出し、設定ファイル入出力、文書編集フローの統合動作を確認したい場合は、これらのモデルを利用する上位モジュールを直接読む。

## hash
- 132f6ad70f74df3ce03caecf2ade0c806c7a578a1a6f5d56b18719fce0863031

# `prompt_builder`

## Summary
- agent 向け完全 prompt の構築を担い、基本情報・oracle/realization の責務・ファイルアクセス・routing・INDEX.md 作成・各種作業ポリシーを選択的に組み立てる。
- 配下の部品は、共通のプレースホルダ型、完全 prompt の統合、エディタ案内、oracle/realization 基礎説明、および個別ポリシー文面の構築を分担する。

## Read this when
- agent call に渡す prompt の構成、ポリシーの有効化、プレースホルダ定義の統合方法を変更・確認するとき。
- INDEX.md 用エントリー、routing、oracle/realization、ファイルアクセス、feedback 報告などの指示文面の責務や生成内容を確認するとき。
- prompt_builder 配下の個別ポリシーや構築部品のどれを起点に読むべきか判断するとき。

## Do not read this when
- prompt の意味仕様そのものや人間向けの正本仕様を確認する場合は、参照先の oracle/doc を直接読む。
- 生成された prompt の実行時挙動や製品側の実装を確認する場合は、対応する realization 実装・テストを直接読む。
- エディタ入力の内容だけを確認する場合は、prompt_builder 全体ではなく editor_input の構築定義またはその参照仕様を読む。

## hash
- 1a0f39daf96a3386bb5d4bff3dbc311e774ddd3381795ddd4210912264c57d0f
