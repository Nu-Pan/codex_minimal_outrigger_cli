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
- AI agent に渡す各種標準プロンプト部品を構築する realization implementation 群を収めるディレクトリ。ファイルアクセス規則、ルーティング規則、oracle / realization の基本概念、oracle 記述規範、realization 品質規範、oracle review / apply review / INDEX.md エントリー生成の判定基準などを、構造化文書として生成する責務を持つ。
- 完全な agent call 用プロンプトを組み立てる統合処理と、その構成要素になる個別の規範文書生成処理の入口になる。標準プロンプトの有効化、注入順序、root token 置換、各 prompt part の本文や責務境界を調べる際に参照する。

## Read this when
- AI agent に渡す標準プロンプトや規範文書が、どの prompt part から生成されるか確認したいとき。
- ファイルアクセス規則、ルーティング規則、oracle / realization の基本概念、oracle 標準、realization 標準、review 標準、apply review 標準、INDEX.md エントリー標準のいずれかの本文を変更したいとき。
- agent call 用の完全なプロンプトに、基本プロンプト、追加文書、各種標準プロンプト、root token 置換処理がどの順序で組み込まれるか追いたいとき。
- oracle file や realization file を扱う AI の判断基準、編集境界、品質基準、レビュー所見の分類基準をプロンプトとしてどう提示しているか調べたいとき。
- INDEX.md を使った読む先の選び方や、INDEX.md エントリー自体の生成品質基準をプロンプト部品として確認・調整したいとき。

## Do not read this when
- 個別 CLI コマンド、入出力 schema、状態ファイル、path model など、プロンプト規範ではない機能仕様や実装を調べたいとき。
- 構造化文書の基礎型、Standard / Requirement のデータ構造、レンダリング処理そのものを確認したいとき。
- 特定の oracle file 本文や realization implementation 本文を調査したいだけで、AI に渡す規範プロンプトの生成処理を変更しないとき。
- 生成済みの実際の INDEX.md エントリー内容や、特定ディレクトリのルーティング結果だけを確認したいとき。
- 作業ルートや root token の基礎的な定義・解決規則だけを調べたいとき。

## hash
- 960324e0ce9ec8e2a1297f6414f95e079a12203206e6046dc59e8981ee6404bd
