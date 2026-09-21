# `acp_builder`

## Summary
- ACP builder の oracle 実装群。agent 呼び出し用のアクセス境界・prompt・作業ディレクトリ・Structured Output・indexing 実行条件を組み立てる共通パラメータ定義を中心に、quota probe、INDEX エントリー生成、oracle 編集・調査、realization 反映・レビュー・要約、feedback 処理、session conflict 解消、TUI 起動の各経路を扱う。

## Read this when
- ACP builder の agent 呼び出し経路について、どの作業を要求し、どのファイル境界・出力形式・実行条件で起動するかを確認したいとき。
- 特定の cmoc サブコマンドが agent に渡す prompt と AgentCallParameter の構築元を調査・変更するとき。

## Do not read this when
- agent 呼び出しの意味仕様やサブコマンド仕様そのものを確認したいときは、対応する oracle/doc を直接読む。
- 実際の realization 実装やテストの挙動を確認したいときは、src または test の対応対象を直接読む。
- INDEX.md エントリー生成の Structured Output schema だけを確認したいときは、indexing/index_entry.json を直接読む。

## hash
- d2d161d8be6b60ce45b9a741d529ef03d94012b0e87c5915587929641315e373

# `editor_input_handoff`

## Summary
- エディタ入力を handoff 用 Markdown 本文へ変換する正本実装と、その初期ガイド取得・入力上書き MCP 入出力スキーマをまとめたディレクトリ。
- 自由記述項目、oracle 参照、送信元 TUI process 情報を検証・配置し、生成本文の構造と送信元識別情報の要件を定義する。

## Read this when
- エディタ入力の handoff 本文の生成規則、送信元情報の必須条件、または入力上書き処理の引数・結果形式を確認したいとき。
- 初期ガイドの取得対象や、target ID を指定した入力引き渡しのインターフェースを確認するとき。

## Do not read this when
- エディタ入力の意味仕様そのものや、呼び出し側が担う target 検証・ファイル書き込みの実装を確認したいとき。
- handoff ではなく一般的な文書参照、構造化文書レンダリング、または別の TUI 処理だけを調べたいとき。

## hash
- 592e58465f3236999d26bf4377b0ea61d23d53f9f9f4ff1e78900dedfa8e4d38

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
- agent 向け完全 prompt の構築と、placeholder 定義の統合を担う実装群です。共通の基礎規定、選択式 policy、作業目的、追加 prompt を構造化して組み立てます。
- editor 経由で入力する prompt の初期文面を構築し、入力位置や記入上の注意を提示する機能を含みます。
- prompt に埋め込む oracle・realization の基本説明と、ファイルアクセス、routing、feedback 報告、oracle・realization の扱い、conflict 解消、INDEX エントリー生成などの個別規定を構成要素として提供します。

## Read this when
- agent call に渡す完全 prompt の構成、policy の有効化、placeholder の衝突処理を確認・変更するとき。
- prompt builder の共通規定や個別 policy の文面を追加・修正するとき。
- editor 経由の prompt 入力初期文面や、oracle・realization の基本説明を確認するとき。

## Do not read this when
- prompt builder の個別 policy の詳細だけを確認したい場合は、その policy 実装を直接読む。
- prompt の利用側における agent call 実行、path context の生成、または構造化文書のレンダリングだけを調べる場合。
- 正本仕様そのものや realization 側の実装を確認する場合。

## hash
- bae927033440968c87c65a3c2ba1bb819d3d317bffc7a3cfb9ce2d92aee46613
