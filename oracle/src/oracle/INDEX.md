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
- 項目別の依頼内容と送信元コンテキストから、editor work file に置き換える Markdown 本文を構築する正本実装と、その入力検証定義をまとめたディレクトリです。
- 入力項目の検証、oracle 参照の本文変換、送信元識別情報と絶対ログパスの保持、および本文セクションのレンダリングを確認するときの入口です。

## Read this when
- editor input handoff の本文生成規則や、送信元情報の必須条件を確認したいとき。
- overwrite 処理へ渡す入力の必須項目・空白禁止・oracle 参照形式を確認したいとき。
- 入力検証後にどの情報が本文へ配置されるかを追いたいとき。

## Do not read this when
- editor input handoff の意味仕様そのものや運用フローを確認したい場合は、参照されている oracle の仕様文書を先に読むべきとき。
- 本文生成や overwrite 入力の仕様ではなく、送信側・受信側の TUI process の呼び出し処理を調べるとき。
- すでに検証済みの本文だけを扱い、生成規則や入力制約を確認する必要がないとき。

## hash
- eb8b1b4663c10cb6d1b7d99365d3c0c73a1c0c047264abc56d933bea5b69965b

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
- agent 向けの完全な構造化 prompt を、共通ポリシー、選択的ポリシー、追加文面、目的、プレースホルダー定義の順に組み立てる実装群。
- prompt のプレースホルダー定義を型として表し、同名異値の衝突を検出して一貫性を保つ。
- oracle／realization の基本知識、ファイルアクセス、routing、feedback 報告、INDEX エントリー、oracle／realization の扱いなど、個別の指示文面を構築する部品群。
- エディタ経由で入力するプロンプトの初期表示文面を、使用説明・記入目安・完全 prompt のテンプレートから生成する。

## Read this when
- agent 呼び出しへ渡す完全 prompt の構成順序、ポリシーの有効化条件、追加 prompt、目的、またはプレースホルダー統合を確認・変更するとき。
- agent に埋め込む個別の作業規定や、oracle／realization の基本説明、routing、feedback、アクセス制限、INDEX エントリー規定の構築を確認・変更するとき。
- エディタ入力用の初期文面や、完全 prompt のテンプレートを HTML コメント内へ配置する処理を確認・変更するとき。

## Do not read this when
- 正本仕様そのもの、実際のファイル分類、agent 呼び出しの実行制御、または prompt_builder を呼び出す上位処理を調べるとき。
- 個別ポリシーの意味仕様や、個別機能の実装・テストの挙動を直接確認する場合は、対応する oracle または呼び出し側・テストを読むとき。

## hash
- 2ef6c993df27b5ca069f795dd99d2ca7d4d110b7d4bc199b22d5205da4cb418e
