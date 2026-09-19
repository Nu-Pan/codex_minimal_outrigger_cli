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
- editor_input_handoff は、MCP から受け取った依頼項目と送信元 TUI process の識別情報を、editor work file 用の Markdown 本文へ引き渡す正本定義の入口です。
- 送信元情報の必須識別子・絶対ログパス検証、依頼項目の節構成、任意コンテキストと oracle 参照の出力、機械値の JSON 文字列表記、コメント開始記号の可視化を確認する場合に進みます。
- 入力項目の許可構造・必須項目・文字列制約だけを確認したい場合は、ディレクトリ全体ではなく入力スキーマを直接参照します。

## Read this when
- editor input handoff の本文生成や、送信元コンテキストの扱いを変更・レビューするとき。
- 依頼本文に含める任意項目、oracle 参照、診断用ログ情報の構造を確認するとき。

## Do not read this when
- 特定の入力フィールドの JSON Schema 制約だけを確認したいとき。
- 送信元情報のデータ構造だけを確認したいとき。
- 本文生成や送信元情報に関係しない oracle の仕様を調べるとき。

## hash
- 5da37d594048cc0bdebcf702b6348abe238b5ce462efcb9b69b26ce965baf442

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
- cmoc のリポジトリ固有設定を表すデータモデル。並列実行数、Codex の provider・model・推論設定、ファイルアクセス規定違反時のリカバリ試行回数を集約する。
- パス表記とルートプレースホルダの基盤モデル。agent call の cwd から worktree・main repository を導出し、プレースホルダと絶対パスの相互変換を扱う。
- 階層化された文章要素、参照可能なタグ付きブロック、コードブロック、構造化ポリシーを保持し、Markdownへレンダリングするための型と処理を提供する。

## Read this when
- cmoc の設定項目や既定値、Codex call 種別ごとの provider・model・推論設定、JSON/TOML表現、並列数やリカバリ回数を確認・変更するとき。
- agent call の cwd、worktree root、main repository root、{{cmoc-root}}・{{repo-root}}・{{run-root}}・{{work-root}} の解決規則やパス変換を確認・変更するとき。
- 構造化文書のノード型、見出し深度、cmoc_ref／cmoc_block、コードフェンス、ポリシー、空行やインデントのMarkdownレンダリングを確認・変更するとき。

## Do not read this when
- 設定ファイルの永続化・生成・同期や doctor の挙動を確認したいときは、設定入出力を担う対象を読むべき。
- 個別の agent call、CLI、TUI、oracle、realization の実行フローを確認したいときは、それぞれの処理対象を直接読むべき。
- 個別のポリシー本文・文書テンプレート、またはMarkdown以外の出力形式や生成側の仕様を確認したいときは、該当する対象を直接読むべき。

## hash
- 4e0b3934e69f302d3c6e7691504546545c65bd697a2075c99ba4cd57455ef24d

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
