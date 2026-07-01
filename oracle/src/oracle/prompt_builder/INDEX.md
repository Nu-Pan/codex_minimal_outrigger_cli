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
- agent call に渡す完全なプロンプトを、固定パーツと呼び出しごとの動的パーツに分けて構築する実装。
- oracle / realization / review / INDEX エントリーなどの標準プロンプト注入フラグを受け取り、必要な依存標準も自動的に有効化する。
- 追加の静的・動的プロンプト、プレースホルダ定義、ファイルアクセス規則、ルーティング規則を統合し、StructDoc の列として返す。

## Read this when
- agent call 用の完全なプロンプト構築順序、静的プロンプトと動的プロンプトの配置、またはキャッシュヒット率を意識したプロンプト構成を確認・変更するとき。
- oracle standard、realization standard、review standard、apply review standard、index entry standard の注入フラグ間の依存関係を確認・変更するとき。
- role、summary、goal、補助プロンプト、プレースホルダ定義、ファイルアクセス規則、ルーティング規則が最終プロンプトへどう組み込まれるかを確認するとき。

## Do not read this when
- 個別の標準プロンプト本文そのものを確認・変更したいときは、対応する parts 側の builder を読む。
- StructDoc や PlaceholderMap、FileAccessMode の型や基本表現を確認したいだけなら、それぞれの定義元を読む。
- 生成済みプロンプトを受け取った後の agent call 実行処理や結果処理を調べたいときは、この構築関数ではなく呼び出し側の実装を読む。

## hash
- 9924680390e1456414e8adffcf76792622f817e7d2687eca42ef1605d801601f

# `parts`

## Summary
- oracle file・realization file・ルーティング・ファイルアクセス・レビュー判定に関するプロンプト本文を、標準文書や規則文書として組み立てる部品群を収めるディレクトリ。
- 人間が責任を持つ正本仕様断片と AI が具体化する realization の境界、oracle 適用レビューや oracle 自体のレビューで所見にする条件、INDEX.md エントリーの規範、作業時の読み進め方、ファイル読み書き規則を確認する入口になる。
- プロンプト全体の結合処理ではなく、各規範セクションの本文内容と、その本文が定める判断基準を調べるための対象である。

## Read this when
- oracle file と realization file の定義、所有責任、配置分類、生成方向の基本概念を確認したいとき。
- oracle file に書くべき内容、未定義部分の扱い、実装から仕様への逆流禁止、用語・命名・goal/non-goal の規範を確認したいとき。
- realization file の品質、重複削除、分割統合、コメント、抽象化、公開面、依存、テスト肥大化抑制の規範を確認したいとき。
- oracle file の内容を realization file に適用するレビューで、どの不整合や問題を所見として扱うべきか判断したいとき。
- oracle file 自体のレビューで、fatal 所見、minor 所見、所見にしない事項の境界を確認したいとき。
- INDEX.md エントリーに書くべき意味情報、読む条件の境界、本文根拠、機械的情報を混ぜない規範を確認したいとき。
- 作業開始時に INDEX.md をどう使って読む先を選ぶか、本文とルーティング情報が食い違う場合に何を根拠にするか確認したいとき。
- ファイルアクセスモードごとにプロンプトへ入る読み書き禁止範囲、memo の扱い、git 追跡対象外判定による例外を確認したいとき。

## Do not read this when
- プロンプト文書全体の結合順序、placeholder 展開、StructDoc などの汎用データ構造や変換処理の実装詳細を調べたいとき。
- 特定の CLI 機能、入出力 schema、状態ファイル形式、パスモデル、個別コマンド仕様を確認したいとき。
- 実際の realization implementation や realization test の現在構造を調べて修正したいだけのとき。
- oracle doc、oracle src、oracle test の個別内容を確認したいとき。
- 個別ディレクトリや個別ファイルの既存 INDEX.md エントリー内容を確認したいだけのとき。

## hash
- e0e4ac81704808cc39d5cc9a03548aad846f659ce52e8cbf22db49ea581a3e2c

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
