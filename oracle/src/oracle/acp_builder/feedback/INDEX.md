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
- feedback issue の同一性判断に使う agent call parameter を構築する定義。構造化 observation と絞り込み済み候補だけを入力として、既存 issue との同一性または新規 issue を判断する prompt、読み取り専用の call context、モデル設定、Structured Output schema の参照をまとめる。

## Read this when
- feedback issue の重複・同一性判定用 agent call parameter を変更または確認するとき
- observation と既存 issue candidate を用いた prompt 構築規則を確認するとき
- normalize issue のモデル、推論、ファイルアクセス、indexing preflight などの起動設定を確認するとき

## Do not read this when
- feedback issue の summary、impact、原因、現在性、actionability、human action、verification verdict、relation の生成規則を確認したいとき
- feedback state の保存や候補 issue の絞り込み処理を変更または確認するとき
- 同一性判定の Structured Output schema 自体を変更または検証するとき

## hash
- 9094802205a6c2b8b6cf14e3608447414595558e0e8ee955a5a45584b3b02bbd

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
- feedback issue の検証担当向け AgentCallParameter を構築する定義。report cut 時点の固定済み参照、candidate、agent call context から、読み取り専用の検証 prompt と Structured Output 設定を生成する。
- issue candidate の判定基準、参照・変更禁止事項、Structured Output の事後条件を prompt に組み込み、検証結果を所定の schema へ接続する。

## Read this when
- feedback issue の検証 prompt や起動パラメータを変更するとき
- candidate、report cut reference、verification verdict の制約を確認するとき
- AgentCallParameter の読み取り専用設定や Structured Output schema の接続を確認するとき

## Do not read this when
- feedback issue の報告・保存処理そのものを変更するとき
- 一般的な prompt builder や共通の agent call 型の仕様だけを確認するとき
- 検証対象の issue candidate や report cut reference の内容を直接確認するとき

## hash
- 8ab1f0a937e4acf0cd9d890f3484a045d2207200e533cc8ab6cc0f9987121ec0
