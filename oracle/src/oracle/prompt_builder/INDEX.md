# `basic.py`

## Summary
- プロンプト生成などで使うプレースホルダ名と置換先文字列の対応表を表す型 alias を定義する、ごく小さな基本型定義モジュール。
- プレースホルダの key は `repo-root` のような名前、value は文字列または Path として扱う、という境界だけを示す入口。

## Read this when
- プレースホルダ置換用の mapping の型を確認したいとき。
- プロンプト構築処理で、プレースホルダ名から実際のパスや文字列へ置換するデータ構造を受け渡しする箇所を読む前に、基本型の意味を確認したいとき。
- 置換先 value に文字列だけでなく Path を許容するかどうかを確認したいとき。

## Do not read this when
- プレースホルダを実際に展開・置換する処理の流れを知りたいとき。この対象は型 alias だけを定義しており、変換ロジックは含まない。
- cmoc のパス概念そのもの、または `<cmoc-root>` や `<work-root>` などの意味を調べたいとき。パスモデルの定義を直接読む方が適切。
- プロンプト全体の組み立て順、出力文面、テンプレート内容を確認したいとき。

## hash
- 532a5fb5a99a36149361894ddf13e6db0e3e84ba0bb3b2193d7f9651a9b5b684

# `complete_prompt.py`

## Summary
- agent call に渡す完全なプロンプトを、役割・概要・ゴール・ファイルアクセス制限・任意の補助プロンプトから組み立てる処理を定義する。
- oracle/realization/review/index entry などの標準プロンプト注入フラグの依存関係を補正し、静的プロンプトを先に、動的プロンプトとプレースホルダ定義を後に配置する責務を持つ。
- プロンプトキャッシュヒット率を意識したパーツ順序、プレースホルダ化、ルーティングルール注入の入口となる。

## Read this when
- agent call 用の完全なプロンプトがどの順序で構築されるかを確認したいとき。
- oracle standard、realization standard、review standard、index entry standard の注入フラグが互いにどの標準を要求するかを確認したいとき。
- 静的プロンプト、動的プロンプト、補助プロンプト、プレースホルダ定義、ファイルアクセスルールの統合位置を変更したいとき。
- プロンプトキャッシュヒット率を考慮した完全プロンプト構成の入口を探しているとき。

## Do not read this when
- 個別の標準プロンプト本文や各パーツの文面を確認したいだけなら、それぞれのパーツ定義を読む。
- 構造化ドキュメントのデータ構造そのものを確認したいだけなら、その型定義を読む。
- ファイルアクセスモードの列挙値や意味を確認したいだけなら、アクセスモード定義を読む。
- ルーティングルール本文だけを確認したい場合は、ルーティングルールを構築するパーツ定義を読む。

## hash
- caffb52a359ecd72639f03068e088910fe905f00058d9b8ce366cbe1ee4521f8

# `parts`

## Summary
- oracle file、realization file、ルーティング文書、ファイルアクセス、レビュー所見に関する標準文書をプロンプト部品として組み立てる領域。
- 正本仕様断片と実装成果物の責務境界、oracle 側・realization 側それぞれの品質基準、INDEX.md エントリー規範、読み書き制限、レビュー時の所見判定規範を生成する入口になる。
- 各部品は、AI に渡す構造化された規範文書や placeholder を作るためのものであり、個別 CLI 機能や状態ファイルの詳細仕様ではなく、作業全体に適用される共通規範を扱う。

## Read this when
- AI に注入するプロンプト部品として、oracle file と realization file の基本概念や責務境界を確認・変更したいとき。
- oracle file の記述量、未定義部分、矛盾、用語統一、実装から仕様への逆流禁止など、正本仕様断片の一般規範を確認したいとき。
- realization file の品質、肥大化抑制、コメント、分割統合、抽象化、公開面、依存、テスト整理に関する一般規範を確認したいとき。
- INDEX.md エントリーやルーティング規則について、読む対象を選ぶための情報として何を書くか、どの順序で読む先を選ぶかを確認したいとき。
- AI エージェントへ渡すファイル読み書き規則や、アクセスモードごとの禁止対象を確認・変更したいとき。
- oracle file または realization file をレビューするとき、どの問題を所見として扱い、どの問題を所見から外すかの判定規範を確認したいとき。

## Do not read this when
- 特定の CLI サブコマンド、入出力形式、状態ファイル、パスモデルなど、個別プロダクト仕様の内容を調べたいとき。
- StructDoc、Standard、Requirement、PlaceholderMap などの基礎データ構造や汎用変換処理そのものを確認したいとき。
- 実装ファイルやテストファイルの現在構造を把握して直接修正したいだけで、共通規範プロンプトの生成内容に関係しないとき。
- oracle file と realization file の分類だけを確認したい場合で、詳細な標準やレビュー規範までは不要なとき。
- レビュー結果の保存形式、表示形式、JSON schema、またはプロンプト全体の結合順だけを調べたいとき。

## hash
- 6539a05f5db918886786eccafc295d3223ce2d64b3b00bea2f8d5a853e71b202

# `prompt_.py`

## Summary
- agent call に渡す完全なプロンプトを、基本ロール・目的・ファイルアクセス制限・ルーティング規則・任意の静的/動的プロンプトから組み立てる実装。
- oracle/realization 基本、各種 standard、review/apply/index entry standard などの注入フラグ間の依存を調整し、必要なプロンプトパーツを一定順序で追加する。
- プレースホルダー定義を収集・統合し、最後に動的な placeholder definition として追加するプロンプト構築処理の入口。

## Read this when
- agent call 用の完全なプロンプト生成順序、静的プロンプトと動的プロンプトの分離、またはプロンプトキャッシュを意識した構成を確認・変更したいとき。
- oracle_standard、realization_standard、review_oracle_standard、apply_review_standard、index_entry_standard などの指定が、他のプロンプトパーツ注入へどう波及するかを確認したいとき。
- role、summary、goal、file_access_mode、aux_static_prompt、aux_dynamic_prompt、aux_placeholder_def を受け取る高水準の prompt builder を探しているとき。
- 生成される StructDoc の並びや、プレースホルダーマップの統合タイミングを確認したいとき。

## Do not read this when
- 個別の oracle standard、realization standard、routing rule、file access rule など、各プロンプトパーツ本文の内容を確認したいだけのときは、それぞれの parts 実装を直接読む。
- PlaceholderMap や StructDoc のデータ構造そのものを確認したいときは、それらの定義元を読む。
- 生成済みプロンプトを実際にどこで agent call へ渡しているかを追いたいときは、呼び出し側の実装を読む。

## hash
- 257a41f253650893268074af5397ea060c176065ed9213bf148225354a7a795f
