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
- AI agent に渡す構造化プロンプト部品を構築する実装群をまとめるディレクトリ。基本概念、ファイルアクセス制限、ルーティング規則、oracle・realization・review・INDEX エントリーの各種標準、完全プロンプトの組み立てを扱う。
- 個別の prompt part 本文を生成する関数と、それらを agent call 用プロンプトへ順序付きに合成する処理への入口になる。

## Read this when
- agent call に含める標準プロンプト片の種類、注入条件、依存関係、結合順序を確認・変更したいとき。
- oracle file と realization file の基本説明、ファイルアクセス制約、INDEX.md を使う読み進め規則など、AI に提示する共通前提プロンプトの生成箇所を探すとき。
- oracle file、realization file、oracle review、apply review、INDEX.md エントリーについて、AI が従うべき標準・所見基準・品質基準の文書生成処理を確認したいとき。
- 構造化文書として標準や要求事項を agent 向けに渡す prompt part の責務分担を把握し、どの個別構築処理を読むべきか選びたいとき。

## Do not read this when
- StructDoc、Standard、Requirement などの基礎データ構造やレンダリング処理そのものを調べたいとき。
- CLI 引数、状態ファイル、入出力 schema、実際のレビュー実行フローなど、生成されたプロンプトを使う側の具体処理を確認したいとき。
- パスキーワード、作業ルート、oracle・memo の場所解決など、パスモデル自体の定義を確認したいとき。
- 特定の oracle file や realization file の本文を実際にレビュー・実装したいだけで、プロンプト部品や標準文書の生成処理を変更しないとき。
- 個別の標準本文だけを確認したい場合は、このディレクトリ全体ではなく該当する標準や規則を構築する対象へ直接進む。

## hash
- e45db61782d2b00f497dbd5c18f39c0751c879d4eaac52d71f9f0580f4ec9d3b
