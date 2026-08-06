# `enumerate_finding.json`

## Summary
- 対象スキーマと関連する oracle review 仕様を確認しました。明白な論理矛盾や実装不能な制約は見つかりませんでした。

## Read this when
- oracle review の所見列挙出力を扱うとき。

## Do not read this when
- 所見列挙以外の oracle review 処理を確認するとき。

## hash
- 3c851fade3f048b47c7dec3c065395d99fbadaea6bda723c7ae63ba3b9020225

# `enumerate_finding.py`

## Summary
- `cmoc oracle review` で新規所見を列挙するための agent call パラメータを構築する実装。レビュー対象 oracle file、関連する既知の所見、oracle-only の読み取り制約、動的プロンプト、構造化出力スキーマ、作業ディレクトリなどを設定し、完成した呼び出し定義を返す。

## Read this when
- `cmoc oracle review` の新規所見列挙フローを変更・調査するとき
- レビュー用 prompt の構築条件、oracle file の参照範囲、agent call の実行設定を確認するとき
- 新規所見列挙用の Structured Output schema との対応を確認するとき

## Do not read this when
- oracle review の所見判定基準そのものを確認したいときは、レビュー標準や対象 oracle file を直接読む
- 新規所見列挙以外の `cmoc oracle review` サブコマンドを変更・調査するとき
- 一般的な prompt 構築や agent call 基盤の仕様だけを確認したいときは、対応する共通実装を直接読む

## hash
- f809fae0a0130114150d1cfc82c53d129ebdf149451cb68571c797c8f0babadd

# `judge_finding.json`

## Summary
- 対象は `verdict` と `reason` を必須とする判定結果用 JSON Schema です。

## Read this when
- 対象の判定結果形式を確認するとき。

## Do not read this when
- 判定対象の所見そのものを確認するとき。

## hash
- a024022fc7378f92b7df63be281522661d57e9b773f1d51db649dbcb5b673512

# `judge_finding.py`

## Summary
- `cmoc oracle review`で、単一のレビュー所見と賛成・反対理由を材料に、所見を人間へ提示すべきか判定するエージェント呼び出しパラメータを構築する。プロンプト、読み取り範囲、モデル設定、構造化出力スキーマ、作業ディレクトリをまとめて定義する。

## Read this when
- `cmoc oracle review`の所見採否判定処理を変更・調査するとき。
- 所見、賛成理由、反対理由を入力とするエージェント呼び出しのプロンプト生成や実行設定を確認するとき。
- この判定処理の構造化出力スキーマやoracle読み取り権限、パスコンテキストの設定を確認するとき。

## Do not read this when
- レビュー所見の内容そのものや、oracle仕様レビュー全体のルールを確認する場合。
- 判定結果の構造化データ形式だけを確認する場合は、対応する出力スキーマを直接読む。
- `cmoc oracle review`以外のサブコマンドのエージェント呼び出しを調査する場合。

## hash
- ac18a5d34f4aa9a070d79a04c7c147f49ba9d8117bee0ed0e6465347fce51f63

# `merge_finding.json`

## Summary
- レビュー所見リストの重複・矛盾を解消する編集操作を定義するスキーマ。所見の削除、単一所見の置換、複数所見の統合を表現し、各操作に対象所見と統合後の所見内容を指定する。

## Read this when
- レビュー結果として複数の所見を整理・統合・置換・削除する処理を実装または確認するとき
- 所見編集操作の入力・出力契約を確認するとき

## Do not read this when
- 個別のレビュー所見そのものの内容や根拠を確認するとき
- レビュー判定ルールや所見生成処理を確認するときは、対応するレビュー仕様・実装を直接読む

## hash
- 53f10a41fd1c8b619ef8948aba0d176282093ba61e8ead9f412f99725d632ed3

# `merge_finding.py`

## Summary
- `cmoc oracle review` における所見リストマージ用の agent call パラメータを構築する実装。oracle file の所見一覧を動的プロンプトへ埋め込み、重複・矛盾の解消と編集操作の列挙を要求する呼び出し条件、モデル設定、アクセス範囲、Structured Output schema の参照先を定義する。oracle review の所見マージ処理へ進む入口となる。

## Read this when
- `cmoc oracle review` の所見リストマージ処理を変更・調査するとき
- 所見マージ用 agent call のプロンプト、モデル、推論強度、ファイルアクセスモード、実行ディレクトリを確認するとき
- 所見リストの動的入力や Structured Output の事後条件がどのように呼び出しへ反映されるか確認するとき

## Do not read this when
- 所見の個別内容や oracle file の仕様本文を確認することが目的のときは、対象となる oracle file を直接読む
- 所見マージ結果の Structured Output の形式だけを確認するときは、参照される schema ファイルを直接読む
- `cmoc oracle review` のマージ以外のサブコマンドや、一般的な prompt builder の共通仕様だけを調査するとき

## hash
- 2b4b13abc8b3a9e9cf744bf542d7ca477afdebbdfdfb250b6c3d4e155e456c55

# `validate_finding_advocate.json`

## Summary
- 対象 JSON は、レビュー所見の妥当性を支持する新規理由を `reasons` 配列で返すための Structured Output schema を定義する。追加プロパティは禁止され、`reasons` は必須である。

## Read this when
- レビュー所見の妥当性を支持する理由を構造化出力として生成・検証するとき。

## Do not read this when
- レビュー所見の内容や妥当性判定ロジックを確認するとき。出力形式ではなく、関連するプロンプトまたは検証処理を直接読む。

## hash
- e375c55fcdef28f2b23f82065da03126e8885307b7b63ab505cb428574c5c73f

# `validate_finding_advocate.py`

## Summary
- `cmoc oracle review` において、レビュー所見が妥当である理由を調査するための AI エージェント呼び出しパラメータを構築する oracle prompt 定義。対象所見、既知の賛成理由・反対理由をプロンプトへ渡し、既存理由と重複しない新規理由の列挙を要求する。
- oracle の読み取り専用アクセス、最大推論 effort、効率重視モデル、構造化出力スキーマ、リポジトリルートを作業ディレクトリとする実行条件を設定する。

## Read this when
- `cmoc oracle review` の所見擁護フロー、またはその agent call prompt の内容・実行条件を調査するとき。
- 所見が妥当である理由の重複排除、理由がない場合の空配列、構造化出力の設定を確認するとき。
- この prompt builder が生成する agent call parameter のモデル、推論強度、ファイルアクセス範囲、作業ディレクトリを確認するとき。

## Do not read this when
- レビュー所見が妥当でない理由の列挙や、擁護以外の oracle review prompt を調査するときは、該当する別の prompt 定義を読む。
- レビュー処理そのもの、構造化出力のスキーマ内容、または prompt の共通生成ロジックを直接調査する場合は、それぞれの実装・スキーマ・共通 builder を読む。

## hash
- 226dc4d18a232051757e1c6b30f594422e32598d19f72f7b29d000c6bae3dce1

# `validate_finding_challenger.json`

## Summary
- 対象所見が妥当ではない新規理由は確認できません。

## Read this when
- 対象所見に対する妥当性検証結果の理由を扱う出力形式を確認するとき。

## Do not read this when
- 対象所見の内容そのものや、既知理由の定義を確認するとき。

## hash
- d784259c47bd99b2599523de5d28145bb4bfffd252b7f4d2042a1ed553270c85

# `validate_finding_challenger.py`

## Summary
- `cmoc oracle review` において、レビュー所見が妥当ではない理由を列挙するための agent call パラメータを構築する。所見、既知の賛成理由、既知の反証理由をプロンプトへ渡し、重複しない新規の反証理由だけを返すレビュー処理への入口となる。

## Read this when
- `cmoc oracle review` の所見反証処理、またはその agent call パラメータ生成を変更・調査するとき。
- 所見、既知の理由、Structured Output、oracle 専用読み取り設定の受け渡しを確認するとき。

## Do not read this when
- レビュー所見の妥当性そのものを評価する実装を直接調べるとき。
- 反証理由の出力スキーマだけを確認したいときは、対応する JSON スキーマを直接読む。
- `cmoc oracle review` 以外のサブコマンドや、一般的な agent call 構築処理だけを調べるとき。

## hash
- b929fd36b37c905037e353b41582b6bc88efc0b34419089457af236859bd945a
