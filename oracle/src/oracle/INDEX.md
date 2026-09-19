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
- editor_input_handoff の正本ソース群です。overwrite_input.json は上書き入力の必須・任意項目と oracle 参照の入力構造を定義し、body.py は検証済み項目と送信元識別情報から editor work file 用 Markdown 本文を生成します。

## Read this when
- editor input handoff の入力形式、必須項目、任意項目、oracle 参照の指定方法を確認するとき。
- handoff 本文の見出し構成、参照ファイルの挿入、送信元情報の出力、送信元識別情報や絶対ログパスの検証を確認するとき。

## Do not read this when
- 実際の editor work file の書き込み、target 検証、TUI への引き渡し手順や実行時ライフサイクルを調査するとき。
- handoff の意味仕様そのものを確認するときは、参照されている oracle 文書を直接読むとき。

## hash
- dfd27325f2bb27ac022266eb66f6023a5b83bbee7ec9aa54b1bb49c3c3c90d2f

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
- cmoc の共通モデルと文書生成補助を担う oracle 実装群。agent call のルートパス解決、構造化文書の Markdown 化、文書参照の表現、リポジトリ単位の cmoc/Codex 設定モデルを扱う。

## Read this when
- agent call の cwd から repo/work/run/cmoc の各ルートを導出する処理や、プレースホルダ付きパスの解決を確認・変更するとき。
- 見出し・タグブロック・コードブロック・規定文を構造化して Markdown にレンダリングする処理を確認・変更するとき。
- 文書参照の保持や、単一・複数参照の Markdown 表現を確認・変更するとき。
- cmoc の並列数、Codex provider、agent call ごとの model/reasoning 設定などの設定モデルを確認・変更するとき。

## Do not read this when
- 上記の共通モデルや補助処理ではなく、特定の agent call、CLI コマンド、ドキュメント仕様の実装だけを直接確認すれば足りるとき。
- oracle の正本ドキュメントやテストの内容を確認するときは、それぞれ oracle/doc または oracle/test を直接読むとき。

## hash
- d1ba1b3dd508b475bbe1e860ce3af41b36c5cebe3c2a454474648de9144876c2

# `prompt_builder`

## Summary
- agent 向け完全プロンプトの構築、プレースホルダー統合、共通規定・選択式ポリシー・目的・追加文面の配置を担う prompt_builder の実装群。
- エディタ入力用の初期文面を、利用手順と完全プロンプトの埋め込み位置を含む構造化テキストとして生成する。
- policy はファイルアクセス、oracle/realization、routing、feedback、conflict 解消、editor handoff など個別規定の生成入口であり、parts は共通の oracle/realization 基礎説明などの文面部品を提供する。
- basic.py はプレースホルダー名と置換値の型を定義し、complete_prompt.py が各 builder を選択的に組み合わせて最終プロンプトを構成する。

## Read this when
- agent 呼び出しへ渡す完全プロンプトの構造、規定の有効化、目的・追加文面・プレースホルダーの配置を変更または調査するとき。
- プロンプト生成に含める個別ポリシーや共通説明の責務を確認し、policy または parts 配下の該当 builder へ進むとき。
- エディタ経由の入力初期文面や、完全プロンプト内の入力埋め込み位置を変更または確認するとき。

## Do not read this when
- 完成済みプロンプトを利用する呼び出し側の挙動だけを調べ、生成定義自体を変更しないとき。
- 特定の個別規定の本文だけが必要で、該当する policy または parts のファイルが既に特定できているとき。
- プレースホルダーの値を提供するパスコンテキストや、構造化文書のレンダリング実装だけを調べるとき。

## hash
- 10462f3b8a39801a408529fa5d0b0252d4b1988557e3ee0982d96cbb82f06a72
