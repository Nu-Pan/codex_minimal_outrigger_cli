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
- AI agent に渡すプロンプトを構成するための個別 prompt part 群を収める領域。oracle/realization の基本説明、ファイルアクセス規則、ルーティング規則、各種レビュー・記述品質標準、INDEX エントリー作成標準などを構造化文書として生成する実装がまとまっている。
- 完全な agent call 用プロンプトを組み立てる処理から参照される標準セクションの本文生成箇所であり、個々の規範文書の内容や注入対象となる基本プロンプト片を確認する入口になる。

## Read this when
- AI agent に提示する標準プロンプト片の本文、責務、構成順序、または注入条件を確認・変更したいとき。
- oracle file と realization file の基本概念、oracle 記述規範、realization 品質規範、レビュー所見の判定基準、ルーティング規則、INDEX エントリー作成基準のいずれかをプロンプトとしてどう生成しているか調べたいとき。
- 完全プロンプトに含める標準セクションの依存関係や、追加プロンプトと標準プロンプト片の結合位置を確認したいとき。
- AI 向けのファイルアクセス制約や読み進め規則を、構造化文書としてどの文言で渡しているか確認したいとき。

## Do not read this when
- 個別機能の CLI 挙動、状態ファイル、出力 schema、パス解決、実際のレビュー実行処理など、プロンプト本文生成以外の実装詳細を調べたいとき。
- 構造化文書、標準、要求事項などの基礎データ構造やレンダリング共通処理そのものを確認したいとき。
- 特定の oracle file や realization file の本文内容をレビュー・実装したいだけで、標準プロンプト片の生成内容や判断基準を変更しないとき。
- 実際の INDEX.md エントリー本文を作成・更新する対象ファイルや対象ディレクトリの内容を調べたいだけのとき。

## hash
- 5c666b5f744d6e2fd22a9a20c00e896f11bc406b2fff9c8258559a841a89e223
