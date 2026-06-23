# `builder`

## Summary
- cmoc の各サブコマンドで AI agent を呼び出すためのパラメータ構築仕様と、対応する Structured Output schema を集めた領域。
- INDEX.md エントリー生成、apply fork の所見列挙・精査・修正依頼・変更要約、review oracle の所見生成・検証・採否・整理、session join の conflict marker 解消、TUI の resolve parameter について、prompt に渡す役割・目標・補助文脈・標準類・モデル設定・ファイルアクセス制約・出力契約を確認する入口になる。
- サブコマンド本体の制御フローではなく、AI 呼び出しに渡す prompt と応答 schema の正本断片へ進むためのルーティング対象である。

## Read this when
- cmoc の機能が AI agent をどの role、summary、goal、補助文脈、標準文書、file access mode で呼び出すかを確認したいとき。
- AI 呼び出しで使う model class、reasoning effort、読み取り専用・realization write・pure oracle read などのアクセス制約、Structured Output schema の接続先を追いたいとき。
- INDEX.md エントリー生成、apply fork のレビュー所見処理や変更要約、review oracle の所見レビュー工程、session join の conflict marker 解消など、用途ごとの prompt builder と schema の読む先を切り分けたいとき。
- 生成結果を検証する実装やテストで、AI 呼び出しパラメータと応答 JSON の意味的契約がどの工程に対応するか確認したいとき。

## Do not read this when
- CLI 解析、サブコマンドの実行制御、fork 作成、git 操作、merge 実行、差分取得、結果保存、画面表示など、AI 呼び出しパラメータや応答 schema 以外の処理を調べたいとき。
- oracle file、realization file、path keyword、standard、complete prompt 構築部品、AgentCallParameter などの共通概念や共通 helper の基礎定義を確認したいだけのとき。
- 個別の oracle file や realization file の本文を読んで、具体的な仕様問題・実装修正内容・conflict 解消判断・変更差分そのものを判断したいとき。
- Structured Output schema の項目定義だけ、または特定サブコマンドの単一工程だけを確認したい場合で、すでに該当する下位対象が分かっているとき。

## hash
- eec572682f4f01ff31ba38c9f910552a891741a1a1728cbabb64808a485a1f9b

# `prompt_parts`

## Summary
- ACP の agent call に渡す標準プロンプト断片を構築する領域。完全なプロンプト組み立て、ファイルアクセス規則、ルーティング規則、oracle / realization の基本概念と品質規範、レビュー所見の判断基準、INDEX.md エントリー品質基準などを扱う。
- 個別機能の仕様本文ではなく、AI に作業前提・制約・判断基準を渡すための共通文章を生成する入口として位置づけられる。

## Read this when
- agent call 用の完全なプロンプトに、どの標準断片がどの順序や依存関係で含まれるかを確認したいとき。
- ファイル読み書き制約、INDEX.md を使ったルーティング規則、oracle file と realization file の基本概念を ACP 向けプロンプトとしてどう表現するか確認したいとき。
- oracle file の書き方、realization file の実装品質、oracle レビュー、oracle と realization の比較レビューなど、共通の判断規範をプロンプト断片として確認または変更したいとき。
- INDEX.md エントリーを生成・レビューする際に、読むべき条件や読まなくてよい境界をどう書くべきか確認したいとき。

## Do not read this when
- 特定の CLI サブコマンド、出力 schema、状態ファイル、パスモデルなど、cmoc の個別機能仕様を探しているとき。
- 生成されたプロンプトを実際にどの agent 実行経路へ渡すか、ACP 呼び出し側の制御フローを確認したいとき。
- StructDoc そのもののデータ構造や基本動作を確認したいとき。
- 既存 realization implementation や realization test の現在のコード内容を調査したいだけで、AI に渡す標準プロンプトや共通規範を確認する必要がないとき。

## hash
- 2a334ead7e1b73698817f37e5c3325171129fc902e90dc14935e133df2f4c73e
