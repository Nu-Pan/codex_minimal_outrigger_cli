# `acp_builder`

## Summary
- AI エージェント呼び出しに必要な共通データモデルと、indexing・oracle・realization・session・TUI・quota probe など用途別の起動定義を扱う領域。各用途の prompt、Structured Output、実行権限、作業ディレクトリ、モデル・推論設定を確認するための入口。

## Read this when
- AI エージェント呼び出しの共通パラメータや用途別の起動条件を調査・変更するとき
- 特定用途の prompt、出力契約、アクセスモード、モデル、推論強度、cwd、preflight 設定を確認するとき
- 配下の用途別定義へ進む前に、どの領域を読むべきか判断するとき

## Do not read this when
- 対象用途の具体的な prompt や Structured Output の詳細を直接確認できるとき
- 共通 prompt 生成規則だけを調べるとき
- 実際の agent call 実行処理、対象ファイルの仕様、または通常の session join 処理を調べるとき

## hash
- c7c42a03da38420de26179d512fb58089a41df5d20b9b01745203e40f9345d89

# `feedback`

## Summary
- 対象ディレクトリは、agent が検出した問題を feedback reporter から collector へ渡すための入力契約を扱う領域です。問題の分類・重要度・影響、人間の対応が必要な理由、原因の確信度、再確認可能な根拠、作業継続状態を表現・検証する下位要素への入口になります。

## Read this when
- feedback reporter の入力形式や、検出した問題を人間向け feedback として構造化する処理を確認するとき。
- 入力契約を構成するスキーマや関連する検証定義を調査・変更するとき。

## Do not read this when
- collector 側の保存、集約、重複判定の仕様だけを確認したいとき。
- feedback の検出方法や、agent が作業を継続するかどうかの判断ロジックだけを確認したいとき。

## hash
- a86d0e0a2687a4eed300cd97383ba6e521f2347418e4446a2bfba702aedcd9ba

# `other`

## Summary
- cmoc の設定、パス解決、標準定義、構造化 Markdown 生成という、oracle 実装を支える共通モデル群の入口。設定値や agent call の root context、instruction 標準の合成、StructDoc のレンダリングを扱う対象へ進む際に読む。

## Read this when
- cmoc のリポジトリ固有設定、Codex CLI 設定、oracle review のループ設定を確認・変更するとき。
- agent call の work root・repository root、root placeholder、実パスとの相互変換や Git worktree 探索を調査するとき。
- agent 向け標準の検証・合成・決定的順序・instruction 文面化を確認するとき。
- 構造化文書を Markdown に変換する見出し、cmoc_block／cmoc_ref、コードブロック、参照検証の挙動を確認するとき。

## Do not read this when
- 永続化された設定ファイルの生成・同期・編集処理だけを確認するときは、対象の設定ファイルや doctor 実装を直接読む。
- ModelClass、ReasoningEffort、その他の参照元型の具体的な列挙値だけを確認するときは、その型定義を直接読む。
- 個別機能における設定・パスモデル・標準・構造化文書の利用方法だけを確認するときは、利用元を直接読む。
- oracle や realization の仕様、通常の Markdown 記法、構造化文書を利用しない文書生成を確認するときは、この共通モデル群を読まない。

## hash
- 4c5b20c8577c323ed7c92e402386e4484cc0bb06bdd7bc756378e57a67568e16

# `prompt_builder`

## Summary
- agent call 用の完全 prompt を組み立てる定義群。placeholder、動的な概要・完了条件、feedback、oracle・realization 規範、ファイルアクセス制約、INDEX.md の routing 規則を統合する入口で、prompt の構築順序や適用条件を調べるときに読む。
- 個別の standard、oracle・realization の基本概念、アクセス規則、routing 規則は下位の定義へ分かれており、必要な規範や部品を特定した後の入口として機能する。
- エディタ経由で後続 agent に渡す初期入力文面の構築も扱い、入力説明と完全 prompt の差し込み構造を確認できる。

## Read this when
- agent call の完全 prompt を構成する部品、注入順序、placeholder 統合、standard の依存関係を変更または調査するとき。
- oracle・realization、review、conflict 解消、feedback 報告、ファイルアクセス、INDEX.md routing の prompt 規則を探すとき。
- エディタ経由のユーザー入力文面や、後続 agent に渡す prompt template の構造を確認するとき。

## Do not read this when
- 個別の oracle file、realization file、仕様書、実装、テストの内容を調査するときは、対象本文へ直接進む。
- 特定の standard の判定基準だけを確認するときは、対応する standard 定義へ直接進む。
- 実際の agent call の利用側や CLI の実行手順だけを確認するときは、呼び出し側または該当する手順書を読む。

## hash
- b88406699fc73da0afc5c2183cd8b779b6a82cfc31f40b69b8fa6f8ca2fb58b3
