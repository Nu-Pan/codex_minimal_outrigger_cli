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
- oracle file・realization file・INDEX.md・file access・routing・review など、エージェントへ注入する基本規範の prompt 部品群を収めるディレクトリ。
- 各部品は StructDoc と placeholder 値を組み立て、ファイル分類、正本仕様断片、実装側品質、ルーティング文書、アクセス制約、レビュー所見判定のような横断的な作業規則を生成する。
- 個別の規範文面を変更・確認する際に、目的に合う部品へ進むための入口になる。

## Read this when
- エージェント用 prompt に含まれる横断的な規範部品の所在を選びたいとき。
- oracle file と realization file の基本定義、oracle 側規範、realization 側規範、INDEX.md エントリー規範、ルーティング規則、ファイルアクセス規則のどれを読むべきか切り分けたいとき。
- oracle review や oracle 適用 review で、所見として扱う条件を定める prompt 部品を探しているとき。
- prompt builder が生成する規範文書の内容や、個別部品ごとの責務境界を確認したいとき。

## Do not read this when
- 特定の CLI コマンド、状態ファイル、パス解決、テスト方針など、プロダクト個別仕様の正本仕様断片を探しているとき。
- StructDoc、PlaceholderMap、Standard、Requirement などの共通データ構造や、prompt 部品を結合する上位処理そのものを調べたいとき。
- 実装ファイルやテストファイルの現在構造を確認して、具体的なコード変更箇所を探したいだけのとき。
- ファイルアクセスモードやパス語彙の列挙値・解決仕様など、このディレクトリの部品が参照する基礎定義そのものを確認したいとき。

## hash
- e2d817e9760badd5b8f6c4260dad85a5d92260f4b4c2928fa80e4da0ad943fab

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
