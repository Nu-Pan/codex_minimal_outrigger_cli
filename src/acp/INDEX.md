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
- AI agent に渡すプロンプトを構成する個別部品を集めた領域。ファイルアクセス規則、INDEX.md ルーティング規則、oracle・realization・review・index entry の各標準、oracle と realization の基本概念、完全プロンプトへの組み立て入口を扱う。
- 各部品は、個別の規範や制約を構造化文書として生成する責務を持ち、上位の組み立て処理から必要な標準プロンプトとして選択・連結される。
- プロンプト全体の構成を追う場合と、特定の標準・規則の本文生成を確認する場合の入口になる。

## Read this when
- AI agent に渡すプロンプトへ、どの標準情報や規則文書を含めるか確認・変更したいとき。
- ファイル読み書き制約、INDEX.md による探索規則、oracle と realization の基本概念、各種レビュー基準、oracle・realization・INDEX.md エントリーの品質基準を生成する処理を探したいとき。
- 標準プロンプト群の依存関係、プロンプト部品の構成順、root token や呼称を実際の agent call 用文言へ正規化する流れを確認したいとき。
- レビューや実装作業の前提として agent に渡される規範文書の内容を、個別部品単位で調整したいとき。

## Do not read this when
- 構造化文書、標準、要求事項、コードブロックなどの基礎データ構造やレンダリング処理そのものを調べたいとき。
- パス概念、root token の定義、作業ルート解決、FileAccessMode など、プロンプト本文に埋め込まれる値や列挙値の基本定義を確認したいだけのとき。
- 個別 CLI コマンドの実行フロー、引数処理、入出力 schema、永続状態、保存処理など、生成されたプロンプトを使う側の実装を調べたいとき。
- 特定の oracle file、realization file、テスト、または INDEX.md エントリー本文そのものをレビュー・修正したいだけで、プロンプト部品や標準文書の生成処理を変更しないとき。

## hash
- 8c5c08f447065e33fb87f8bca5153543da7cb31398cf426fbe10c5477280c550
