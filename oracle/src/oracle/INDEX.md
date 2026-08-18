# `acp_builder`

## Summary
- AI agent call の論理モデル、feedback 判定、INDEX.md 生成、oracle 処理、quota probe、realization fork、session conflict 解消、TUI 起動に関する prompt・起動パラメータ・Structured Output schema をまとめたディレクトリ。各機能の agent call 契約や設定を調べる際の上位入口となり、具体的な処理は配下の機能別実装へ進む。

## Read this when
- agent call を利用する機能の prompt、モデル・推論設定、ファイルアクセス、作業ディレクトリ、indexing preflight、Structured Output 契約の入口を判断するとき
- acp_builder 配下で basic、feedback、indexing、oracle、quota probe、realization、session、tui のどの機能別定義を読むべきか確認するとき

## Do not read this when
- 特定機能の具体的な prompt 構築、AgentCallParameter 実装、実行処理、schema の詳細を調べる場合は、配下の対応する実装や schema を直接読むとき
- 共通の agent call 型、prompt 生成規則、Codex CLI sandbox 仕様、実際の oracle・realization 実装や INDEX.md の内容を調べる場合は、それぞれの定義元・正本仕様・対象ファイルを直接読むとき

## hash
- 6cc1deb100197bdb350784053578f05269453afc2686c42c4d31ca9b5587e5c2

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
- cmoc の共通基盤モデルと文書生成ヘルパーをまとめたディレクトリ。リポジトリ固有設定、agent call のパスコンテキストと root placeholder 解決、構造化文書の Markdown レンダリングを扱う。
- 設定項目や既定値を確認する場合は `cmoc_config.py`、パス表記・worktree root・repository root の解決を確認する場合は `path_model.py`、構造化文書ノードと Markdown 出力を確認する場合は `struct_doc.py` を入口にする。

## Read this when
- cmoc の設定モデル、Codex CLI 設定、oracle review のループ上限を確認または変更するとき
- agent call における `{{repo-root}}`・`{{work-root}}`・`{{run-root}}` などのパス表記と実パス解決を確認または変更するとき
- 構造化された文書ノード、タグ付きブロック、コードブロック、規定、Markdown レンダリングの挙動を確認または変更するとき

## Do not read this when
- Codex CLI の呼び出し処理や個別の oracle・realization 機能の責務を確認したいとき
- 設定ファイルの実際の保存内容や人間による調整結果だけを確認したいとき
- 構造化文書ヘルパーの利用箇所や個別機能の具体的な prompt 構成を確認したいとき

## hash
- b62b04a432383d9b162fc91b0e7d7a9e3bc6ee49a1f048fe67eff8589b1d06b5

# `prompt_builder`

## Summary
- agent call 向けプロンプトの構成部品を集約するディレクトリ。placeholder 型、完全プロンプト構築、エディタ入力文面、共通 prompt parts、目的別 policy を扱い、下位モジュールへの入口となる。
- 完全プロンプトの構成順序や各種ポリシー・placeholder の統合を確認する場合は `complete_prompt.py`、エディタ入力形式は `editor_input.py`、placeholder の型定義は `basic.py`、共通説明や制約は `parts`、目的別 instruction は `policy` から読み始める。

## Read this when
- prompt builder が生成する agent call 向けプロンプトの構成部品や policy の組み合わせを追加・変更・調査するとき
- oracle／realization の責務境界、ファイル分類、アクセス規則、レビュー、handoff、routing などをプロンプトへ組み込む経路を確認するとき
- 完全プロンプト、エディタ入力文面、placeholder 定義、共通 parts、目的別 policy のどこを読むべきか判断するとき

## Do not read this when
- oracle または realization の正本仕様・実装・テスト本文を確認したいとき
- CLI 本体や共通型など、prompt builder の構成文面以外の実装責務を調査するとき
- 特定の policy や prompt の内容だけを確認したい場合は、このディレクトリ全体ではなく対応する下位ファイルへ直接進めるとき

## hash
- 4e643dec887906fa9a4b0b9e398bd41476630af54c4f738b2e3fb5777f269232
