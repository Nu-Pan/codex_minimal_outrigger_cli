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
- editor input の handoff を構成する正本群。受信先 prompt から参照ガイドを生成し、項目別依頼内容・oracle参照・送信元識別情報から handoff 本文を構築するほか、入力とガイド取得結果の JSON Schema を定義する。

## Read this when
- editor input の handoff ガイド生成、handoff 本文の構成、送信元情報の検証、または関連 MCP 入出力のスキーマを確認するとき
- 自由記述項目や oracle 参照、target ID、実行 ID など handoff データの形式・必須条件を調べるとき

## Do not read this when
- handoff 以外の editor input 処理を調べるとき
- 実際の TUI 呼び出し、MCP の検証・参照変換・ファイル書き込みの実装を確認したいとき。このディレクトリはそれらを呼び出し側の責務として扱う

## hash
- a2a1263148e18bfbd7bc09d014034824d810a0f333b5cb8c958c0676e6ec0ee8

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
- agent向け完全promptを構築する定義群の入口。タスクやパス文脈からプレースホルダーを統合し、選択された基本規定・各種ポリシー・目的・追加文面を構造化されたpromptへ組み立てる。
- 共通のプレースホルダー型、エディタ入力案内、oracle/realizationの基本説明、およびファイルアクセス・routing・正本仕様・実装・所見・conflict解消・handoffなどの個別ポリシー構築を扱う。下位のpolicyやpartsは、特定の規定本文や基本説明の構築方法を確認するための入口である。

## Read this when
- agent callへ渡す完全promptの構成、規定の有効化、目的や追加文面の配置、プレースホルダー統合の挙動を確認したい場合。
- prompt_builder配下の共通型、エディタ入力案内、または複数のpromptポリシーがどのように構築されるかを調べたい場合。
- 個別ポリシーの選択肢を横断して、prompt構築全体の責務や組み立て順を把握したい場合。

## Do not read this when
- 単一のポリシー本文や基本説明の具体的な要求だけを確認したい場合は、配下の対応するpolicyまたはpartsを直接読む。
- プロンプト構築ではなく、参照先の意味仕様や実際のagent実行処理を調べる場合は、それぞれのoracle/docまたは呼び出し側実装を直接読む。

## hash
- 8b52d93dc0305b481c83f78a1dc2d855eafb7d4fd2b5b7526c53bba7fe695609
