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
- AI agent に渡す標準 prompt 断片と、その断片群を統合して完全な prompt 文書列を構築する実装をまとめた領域。
- ファイルアクセス制約、INDEX.md ルーティング規則、oracle/realization の基本概念、oracle・realization・review・index entry の各規範など、agent call の前提文書として注入される文章を構造化文書として生成する。
- 個別の規範本文を変更する入口と、複数の標準 prompt の有効化依存・挿入順序・root token 置換を確認する入口の両方を含む。

## Read this when
- agent call に含める標準 prompt の文面、構成順序、依存関係、または Codex CLI に渡す直前の文書列生成を確認・変更したいとき。
- ファイル読み書き制約、INDEX.md の読み進め方、oracle と realization の責務境界、oracle file の記述規範、realization file の品質規範を prompt としてどう生成しているか調べたいとき。
- oracle review や apply review で、所見に含めるべき問題と対象外にすべき推測・未定義部分・品質改善案の境界を prompt 文面として確認したいとき。
- INDEX.md エントリー作成時に従うべき標準や、エントリーをルーティング情報として機能させるための要求事項を実装側で確認・変更したいとき。

## Do not read this when
- 特定の CLI コマンド、状態ファイル、path model、入出力 schema など、個別機能の仕様や実装を調べたいとき。
- 生成された prompt を使う上位の agent 実行フロー、保存処理、レビュー実行処理、または CLI 引数処理そのものを調べたいとき。
- 構造化文書の基礎データ型、標準・要求事項の汎用変換処理、root token や work root の定義そのものを変更したいとき。
- 特定の oracle file や realization file の本文内容を調査したいだけで、agent に渡す標準 prompt の文面や統合順序に関心がないとき。

## hash
- 7d3376e91a5e0de3f0c927fac38d9133fa6ec1d7c781fde26a5cf52e26d901a5
