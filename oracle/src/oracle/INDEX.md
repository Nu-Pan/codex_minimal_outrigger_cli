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
- エディター入力 handoff の正本実装と入出力スキーマをまとめるディレクトリ。
- 受信先 prompt の雛形から handoff ガイドを構築し、項目別依頼と送信元情報から editor work file 用 Markdown 本文を生成する。
- target ID、依頼項目、oracle 参照、handoff ガイド取得結果の検証形式も定義する。

## Read this when
- エディター入力 handoff のガイド生成、本文構成、送信元情報の検証・埋め込みを確認するとき。
- handoff 関連ツールの入力・出力 JSON スキーマを確認するとき。
- editor work file を置換する本文のセクションや必須入力を調べるとき。

## Do not read this when
- handoff 以外の入力経路や、生成された editor work file の後続処理だけを調べるとき。
- 正本仕様書の意味を確認することが目的で、実装やスキーマの具体化を読む必要がないときは、関連する oracle/doc を直接読む。

## hash
- 68bf245bcf970263c4224cc2131ea1718c36c112f9d15a08df975aed88f86b3e

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
- agent 向け完全 prompt の構築、editor input 初期文面、placeholder 型、および各種 policy 文面の oracle 定義をまとめるディレクトリ。
- `policy` 配下には file access、routing、oracle／realization、feedback、conflict resolution、INDEX エントリー生成、editor input handoff など、選択的に prompt へ組み込む規定がある。
- `parts` 配下には oracle file と realization file の基本概念・分類を説明する prompt 部品がある。

## Read this when
- 完全 prompt の構成、policy の有効化、placeholder の統合、または agent call に渡す規定文面を確認・変更するとき。
- prompt_builder 配下の policy や部品を横断して、どの規定が prompt に組み込まれるかを調べるとき。
- editor input の初期文面や、oracle／realization の基本説明を生成する処理を確認するとき。

## Do not read this when
- 単一の policy や部品の具体的な規定だけが必要な場合は、その配下の該当ファイルを直接読むとよい。
- prompt の生成や oracle／realization の規定と無関係な機能を調べるとき。

## hash
- a41a39cfb1731bbc7eb3a0ea1c1285a2407a90af77c5a289ff6affa8a2d34e52
