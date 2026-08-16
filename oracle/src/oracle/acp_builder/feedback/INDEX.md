# `normalize_issue.json`

## Summary
- 観測が既存 issue candidate と同一か新規かを判定する Structured Output Schema。既存 issue を選ぶ場合と新規 issue とする場合の結果構造、および issue ID の形式を定義する。

## Read this when
- issue 同一性判定の出力契約や、既存・新規の判定結果を扱う処理を確認するとき

## Do not read this when
- issue 同一性判定以外のフィードバック処理を扱うとき
- 一般的な JSON Schema の仕様や、個別 issue の内容を確認するとき

## hash
- 8e42e7c00ff52afa94b5ccecd29af1a50f3add5b951ad93cfa8466e02fa58c57

# `normalize_issue.py`

## Summary
- 構造化された observation と、絞り込み済みの既存 issue candidate を比較し、feedback issue が既存 issue と同一か新規かを判断するための prompt と agent call parameter を構築する定義。feedback issue の同一性判断処理へ進む際の入口であり、issue の内容生成や原因・重要度の確定を担うものではない。

## Read this when
- 構造化 observation と既存 issue candidate の同一性だけを判定する prompt や agent call parameter を変更・確認するとき
- feedback issue の正規化処理で、入力制約、読み取り専用設定、または Structured Output の事後条件を確認するとき

## Do not read this when
- issue の summary、impact、原因、現在性、actionability、human action、verification verdict、relation を生成・判定する処理を確認するとき
- 候補 issue の絞り込みや feedback state、raw log、過去 session の参照処理を確認するとき

## hash
- 9ee306782ace8a783c5bcf93fc842645449ffd761ce345a8e5cd213eecee4313

# `verify_issue.json`

## Summary
- report cut 時点の issue candidate を、現在の evidence に基づいて unresolved、resolved、not_actionable、inconclusive のいずれかへ検証する JSON Schema です。
- 各 verdict に応じて candidate ID、current evidence、reason を定義し、unresolved の場合だけ作業外の人間が取る具体的な対応を求めます。

## Read this when
- issue candidate の現在状態を report cut の参照情報から判定する出力契約を確認するとき
- verdict ごとの必須フィールド、evidence の形式、human_action の許容有無を確認するとき
- feedback verification 処理がこの構造化出力に適合しているかを調べるとき

## Do not read this when
- report cut reference や issue candidate の具体的な内容だけを確認したいとき
- 実際の verification 実装やテストの挙動を確認したいとき
- 一般的な JSON Schema の作成・検証方法だけを調べるとき

## hash
- 49d2a67344bebe92475f921fc7d25286d371c7f93878a143c876cee9c26245e5

# `verify_issue.py`

## Summary
- feedback issue candidate を、report cut 時点で固定された参照だけから検証するための prompt と agent call parameter を構築する。候補、参照、検証基準を prompt に組み込み、読み取り専用・最高推論 effort・専用 Structured Output schema の call 設定を返す。feedback issue の検証フローや、その起動パラメータと prompt 構成を確認する際の入口となる。

## Read this when
- report cut reference に限定した feedback issue candidate の検証 prompt を変更・確認するとき
- 検証 call の読み取り専用設定、モデル・推論設定、Structured Output schema の割り当てを確認するとき
- unresolved / resolved / not_actionable / inconclusive の判定条件や、current evidence・human action の prompt 事後条件を確認するとき

## Do not read this when
- feedback issue の発見・保存・送信処理を調べるとき
- 検証結果の Structured Output schema 自体や、候補・参照データの生成処理を直接確認するとき
- 一般的な agent call parameter や prompt builder の共通仕様だけを調べるとき

## hash
- faf23a30bab1768cd24bbb260e439c35fb2a012fd87ed36884487580cf2d53ce
