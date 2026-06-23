# `builder`

## Summary
- AI agent 呼び出しの prompt 構築仕様と Structured Output schema を、用途別にまとめる領域。
- fork 適用時のレビュー所見処理と変更要約、INDEX.md エントリー生成、oracle レビュー工程、セッション合流時の conflict marker 解消について、どの下位領域を読むべきか判断する入口になる。
- 各用途で AI に渡す role・summary・goal・補助文脈・標準類・対象本文・アクセス制約・モデル設定・構造化出力契約を確認するための案内を担う。

## Read this when
- cmoc のサブコマンドが AI agent を呼び出す際の prompt、入力文脈、file access mode、model/reasoning 設定、Structured Output schema の読む先を選びたいとき。
- fork 適用後の所見列挙・所見精査・修正担当 agent 呼び出し・変更要約生成に関する agent 呼び出し仕様へ進みたいとき。
- INDEX.md 用エントリー生成について、対象本文を AI にどう渡すか、読み取り専用制約や出力契約をどう固定するか確認したいとき。
- oracle レビューの新規所見生成、既存所見の理由調査、採否判定、所見整理など、レビュー工程ごとの AI 呼び出し仕様を切り分けたいとき。
- セッション合流時に merge conflict marker 解消 agent を呼び出すための prompt、対象パス、編集許可範囲、禁止事項を確認したいとき。

## Do not read this when
- CLI 解析、git 操作、fork 作成、merge 実行、diff 取得、永続化、表示など、AI agent の prompt 構築や応答 schema 以外の実行制御を調べたいとき。
- oracle file、realization file、path keyword、standard、complete prompt 構築部品などの共通概念や共通 helper の定義そのものを確認したいとき。
- 個別の oracle file や realization file の本文を読んで、具体的な仕様問題、修正内容、実装差分、conflict 解消判断を行いたいとき。
- 生成済み INDEX.md の内容や各階層のルーティング情報を確認したいだけのとき。
- AI 呼び出しの用途が fork 適用、INDEX.md エントリー生成、oracle レビュー、セッション合流時 conflict 解消のいずれにも当てはまらないとき。

## hash
- b4c1c5ea3b0ae86e6cc68b12d633d32b9701ad987be878e1cdf21f9cd4449a47

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
