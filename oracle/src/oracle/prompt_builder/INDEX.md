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
- oracle/realization の基本概念、oracle file と realization file の標準、レビュー判定、ファイルアクセス規則、INDEX.md ルーティング規則など、AI エージェントへ注入するプロンプト断片を構築する oracle src 群。
- 各部品は StructDoc 形式の規範文書または規則文書を生成し、正本仕様断片の扱い、実装側品質、レビュー所見の境界、読み書き制約、読む先の選び方を個別の責務として分担する。
- プロンプト全体の具体的な結合処理ではなく、注入される規範・規則そのものの内容と境界を確認する入口になる。

## Read this when
- AI エージェントに渡す oracle/realization 関連の規範文書やルーティング規則の生成内容を確認・変更したいとき。
- oracle file、realization file、レビュー所見、ファイルアクセス、INDEX.md エントリー、ルーティングの各標準がどのプロンプト部品で定義されているかを探したいとき。
- oracle file の保守方針、realization file の品質基準、レビューで所見にする条件など、複数の標準部品のどれを読むべきか判断したいとき。
- ファイルアクセスモード別の禁止事項や、oracle file と realization file の読み書き可否を生成する部品を探したいとき。
- プロンプト部品が出力する規範の責務境界を確認し、特定の標準部品へ進む前に同階層の候補を比較したいとき。

## Do not read this when
- 特定の CLI コマンド、状態ファイル、パスモデル、出力 schema など、個別機能の正本仕様断片を確認したいとき。
- StructDoc、Standard、Requirement、PlaceholderMap などの汎用データ構造や、プロンプト全体の結合フローを調べたいとき。
- oracle/realization の規範ではなく、実際の realization implementation や realization test の現在構造を修正するために読みたいとき。
- 個別ファイルの責務がすでに分かっており、そのファイル本文へ直接進む方が早いとき。
- INDEX.md エントリーの生成対象本文そのものではなく、既存のルーティング文書や生成済みエントリーを確認したいとき。

## hash
- 2bf112d3713b00ceb458dce06165a3ef9a944f21982756ceaf66b923919068fd

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
