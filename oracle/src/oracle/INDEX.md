# `acp_builder`

## Summary
- Agent call 用の正本ソースをまとめる領域です。共通パラメータ定義、feedback・indexing・oracle・realization・session・tui 各用途の起動条件や prompt 構築、Structured Output 連携を扱い、各サブ領域の実装を確認する入口になります。

## Read this when
- Agent call の共通パラメータやモデル・推論強度・ファイルアクセスモードを確認するとき。
- 特定用途の agent call における prompt、実行条件、Structured Output 設定の実装入口を探すとき。
- indexing、oracle、realization、session、tui、feedback の agent call 構築を調査・変更するとき。

## Do not read this when
- 実際の agent call 実行フローや CLI・TUI の上位制御を調査するとき。
- 正本仕様そのもの、Codex CLI の sandbox・permission profile の詳細、または Structured Output schema の本文だけを確認するとき。
- 通常の realization 実装・テストや issue の保存・取得・表示など、agent call パラメータ構築以外の処理を調べるとき。

## hash
- 693ef7698194df195757d31f2e2d2d40ee74c317fef720c65de889208b737e7d

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
