# `acp_builder`

## Summary
- 対象ディレクトリには、各種 cmoc フローで AI Agent 呼び出しに使う正本ソースが配置されている。共通の呼び出しパラメータ定義、feedback・indexing・oracle・realization・session・tui など用途別の prompt／起動設定、Structured Output schema の定義が下位要素への入口となる。

## Read this when
- cmoc の特定フローで使われる AI Agent 呼び出しの prompt、モデル・推論設定、アクセス権限、作業ディレクトリ、実行前設定を調査・変更するとき。
- Agent call の出力契約や用途別の Structured Output schema の定義を確認するとき。
- 共通パラメータ定義または feedback、indexing、oracle、realization、session、tui の呼び出し設定の入口を探すとき。

## Do not read this when
- 通常の realization 実装・テストや CLI／TUI の実行フローそのものを調査するときは、対応する realization 側または呼び出し側を直接読む。
- 正本仕様そのもの、Codex CLI sandbox・permission profile の一般規則、共通 prompt 構築の詳細だけを調査するときは、それぞれの専用仕様・実装を直接読む。
- 特定用途の prompt や schema 以外の agent call を調査するときは、該当する下位ディレクトリまたは共通定義を直接読む。

## hash
- b035301cb336018a668b3f20fcad66aa0c4fc4ddf0a8ec9c30a1d86b6b47e214

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
- リポジトリ設定、パスモデル、規範モデル、構造化文書レンダラーを担う Python ソース群。設定値や永続化構造、root 解決、規範の構造化、Markdown 出力を調査・変更する際の入口となる。

## Read this when
- CmocConfig や Codex 設定、oracle review の上限、JSON/TOML シリアライズを確認するとき
- agent call の cwd・work/repository/run root、root placeholder、パス変換や検証を確認するとき
- Standard・Requirement の構造や StructDoc への変換を確認するとき
- StructDoc の階層、Markdown レンダリング、cmoc_ref 検証、コードブロックや空行処理を確認するとき

## Do not read this when
- CLI の実行フロー、設定ファイルの生成・同期、agent call prompt 生成などの利用側処理だけを調査するとき
- ModelClass、ReasoningEffort、StructDoc 自体など、別ファイルに定義された概念の詳細だけを確認するとき
- 個別の規範本文や、Markdown レンダリングを通らない他の oracle 文書の仕様だけを確認するとき

## hash
- 01ecbe8fd695e08e7b934d3c8c596ce87ab0fd7d09615d8dc1fb9728229c4da7

# `prompt_builder`

## Summary
- プレースホルダ名と実パス・文字列の対応を表す型定義。置換対象を共通の型で扱うための入口。
- 固定・動的なプロンプト部品と規範を統合し、エージェント呼び出し用の完全なプロンプトを組み立てる中核ビルダー。
- ユーザー入力エディタに表示する初期テキストと、サブコマンド固有の自動注入指示を構築する実装。
- oracle・realization、レビュー、アクセス制約、INDEX.md ルーティングなど、エージェントプロンプトへ組み込む各種規範を生成する部品群。

## Read this when
- プレースホルダ展開用の型、文字列と Path を混在させる置換対象の表現を確認するとき。
- 完全なエージェントプロンプトの構成、注入される規範や動的情報、部品の統合順序、プレースホルダ定義を確認・変更するとき。
- ユーザー入力エディタの初期表示、品質案内、HTML コメントによる自動注入指示を確認・変更するとき。
- prompt builder に組み込む共通規則の生成元や、oracle・realization・レビュー・アクセス制約・ルーティングなど特定の規範の実装を調査するとき。

## Do not read this when
- プロンプト本文の生成手順や置換ロジックの詳細を確認するときは、実装側を直接読む。
- プレースホルダや設定値の表現に関係しない処理を調査するとき。
- 特定の静的プロンプト本文や個別規則だけを確認するときは、対応する parts 配下または定義・規則のファイルを直接読む。
- prompt builder 以外の CLI 機能や session 処理、個別の oracle 文書・realization 実装を調査するとき。
- INDEX.md のエントリー内容だけを確認するとき。

## hash
- 70d16b3f12e8fdba097c0bf88dc9fb5089c8c2fd767ffdad097d5c5ce7c0409b
