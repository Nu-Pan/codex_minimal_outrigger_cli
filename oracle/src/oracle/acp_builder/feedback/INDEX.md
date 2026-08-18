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
- 構造化済み observation と絞り込み済み既存 issue candidate を比較し、feedback issue が既存 issue と同一か新規かを判断する prompt と AgentCallParameter を構築する。入力以外の状態を参照しない読み取り専用の agent call を定義し、判断専用の Structured Output schema、モデル設定、実行コンテキストを指定する。

## Read this when
- feedback observation と既存 issue candidate の同一性判定用 agent call の prompt、入力範囲、読み取り制約、または起動パラメータを確認・変更するとき。

## Do not read this when
- feedback issue の summary、impact、原因、現在性、actionability、human action、verification verdict、relation などの内容生成を扱うとき。
- 候補の絞り込み、feedback state や raw log の参照、または Structured Output schema 本体の詳細を直接確認する必要があるとき。

## hash
- 014740162e9310fae6f6048522b33af9cddda4254cdd32015cbaf65e531b02ba

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
- feedback issue candidate を、report cut 時点で固定された参照だけから検証する prompt と AgentCallParameter を構築する。検証用の読み取り専用 call context、verdict の判定規則、Structured Output の事後条件、動的な candidate/reference 入力をまとめ、対応する検証処理の入口となる。

## Read this when
- feedback issue candidate の unresolved / resolved / not_actionable / inconclusive 判定条件を確認するとき
- report cut reference に限定した検証 prompt の構築規則や、読み取り専用の agent call パラメータを変更・調査するとき
- feedback 検証用 Structured Output schema と prompt の結び付きを確認するとき

## Do not read this when
- feedback issue の記録・送信や observation の状態管理を確認したいとき
- 検証結果の Structured Output 項目や JSON schema 自体を直接確認できるとき
- 一般的な prompt 構築、agent call の共通型、パスコンテキストの仕様を確認する場合は、それぞれの共通実装・定義を直接読むとき

## hash
- 33ba6f7c41847aea9b18809b3bf0c797e2798800fdcdde681256c608dcb44489
