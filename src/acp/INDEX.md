# `builder`

## Summary
- AI エージェント呼び出し用のパラメータ構築実装を集めた領域。各サブコマンドや処理段階ごとに、complete prompt、補助入力、ファイルアクセス権限、モデル・reasoning、Structured Output schema の指定を組み立てる入口になる。
- 対象は、変更要約・実装所見調査・所見対応、目次エントリー生成、oracle レビュー、merge conflict marker 解消、TUI 実行パラメータ選定など、AI に依頼する作業の呼び出し条件と応答契約である。
- 実際の CLI 制御、git 操作、ファイル更新処理、レビュー結果の保存や表示ではなく、それらの処理から AI を呼び出す直前に渡すプロンプトと構造化出力 schema の対応関係を扱う。

## Read this when
- cmoc の各機能が AI エージェントへ渡す AgentCallParameter をどのように構築しているか、処理領域ごとに入口を探したいとき。
- AI 呼び出しで使う role、summary、goal、aux_prompt、標準文書の参照有無、file access mode、model class、reasoning effort、Structured Output schema の対応を確認または変更したいとき。
- 変更差分の要約、ファイル単位の所見列挙、所見に基づく realization file 修正依頼のような apply fork 向け AI 呼び出し設定を追いたいとき。
- INDEX.md 用エントリー生成、oracle file レビュー所見の列挙・検証・採否・整理、merge conflict marker 解消、TUI の権限・標準参照選定など、個別の AI 作業依頼のプロンプト設計へ進みたいとき。
- Structured Output schema がどの AI 呼び出しビルダーから参照され、その schema がどの段階の応答を機械処理可能に固定しているかを確認したいとき。

## Do not read this when
- サブコマンド登録、CLI 引数解析、実行順序、状態管理、git branch 操作、merge 実行、ファイルシステム走査や保存など、AI 呼び出し前後の制御フローだけを調べたいとき。
- complete prompt の共通構築規則、StructDoc や Markdown rendering、path model、AgentCallParameter や FileAccessMode などの基礎型そのものを確認したいとき。
- oracle file や realization file の本文、標準文書の内容、または実際に修正・レビューされる対象ファイルの仕様や実装を直接読みたいとき。
- AI 応答を受け取った後の結果集約、保存、表示、適用可否判断、テスト実行、ユーザー通知などの後続処理を調べたいとき。
- 生成済み INDEX.md の描画・更新・保存や、リポジトリ全体のルーティング文書管理だけを確認したいとき。

## hash
- 2fa7d3217c15a26c90e074c17bfdf5257f83b909cb8438de8523b0f8a4d778ee

# `prompt_parts`

## Summary
- ACP agent call に渡すプロンプト断片を構築する realization implementation 群であり、完全プロンプトの組み立て、ファイルアクセス制約、ルーティング規則、oracle/realization の基本概念、各種レビュー・品質規範、INDEX エントリー規範を扱う。
- 各ファイルは `StructDoc` と標準・要求事項の構造を使って、AI に提示する規範文書や基本文書を生成する責務を持つ。
- agent call 用プロンプトに含める標準セクションの内容や注入条件、レビュー所見の分類基準、oracle/realization/INDEX エントリーに関する判断基準を調べる入口になる。

## Read this when
- agent call 用の完全なプロンプトに、基本情報・アクセス制限・ルーティング規則・追加プロンプト・標準プロンプト片をどう組み込むか確認したいとき。
- AI に提示するファイル読み書き制約や、INDEX.md を使った本文探索ルールの文面・構造を確認または変更したいとき。
- oracle file と realization file の役割分担、編集責任、生成方向、下位分類をプロンプトへ含める処理を調べたいとき。
- oracle file、realization file、INDEX.md エントリーが従うべき品質規範や記述規範を生成する処理を確認したいとき。
- oracle review や oracle-to-realization review で、どの問題を所見にするか、fatal/minor や対象外条件をどう定義するか調べたいとき。

## Do not read this when
- 個別機能の CLI 挙動、状態ファイル形式、パス解決、入出力 schema など、生成されるプロンプト本文ではなくプロダクト実装の詳細を調べたいとき。
- `StructDoc`、`Standard`、`Requirement` などの基礎データ構造や、構造化文書の汎用レンダリング処理そのものを調べたいとき。
- 特定の oracle file や realization file の本文内容をレビュー・実装したいだけで、レビュー基準や品質規範のプロンプト生成処理を変更しないとき。
- 生成済みの INDEX.md エントリー文面やルーティング文書の保存・更新フローだけを確認したいとき。
- 特定の標準プロンプト片だけを変更することが分かっているときは、このディレクトリ全体ではなく該当する個別構築ファイルへ直接進む。

## hash
- 1ea0aaba9f797fdcfc41f1e16260d01c9f975e500f6195af2abc58d6c80016a7
