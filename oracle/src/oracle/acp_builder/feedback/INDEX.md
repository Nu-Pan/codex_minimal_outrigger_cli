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
- feedback issue の同一性判断用 agent call parameter を構築する定義。構造化 observation と絞り込み済み既存 issue candidate だけを入力として、既存 issue と同一か新規 issue かの判断を依頼する prompt、読み取り専用の call context、モデル設定、Structured Output schema の参照を組み立てる。feedback normalize issue の agent 起動設定を確認する入口。

## Read this when
- 構造化 observation と既存 issue candidate の同一性判定フローを変更・レビューするとき
- feedback normalize issue 用 prompt の入力制限、判定後条件、モデル・権限・実行設定を確認するとき
- この agent call が返す Structured Output schema の指定元を確認するとき

## Do not read this when
- issue の summary、impact、原因、現在性、actionability、human action、verification verdict、relation の生成仕様を確認したいとき
- agent call の共通 prompt 生成処理そのものを調べるときは、直接 build_complete_prompt の定義を読む方が適切
- 同一性判断結果の項目・型・形式だけを確認したいときは、指定された Structured Output schema を直接読む方が適切

## hash
- d85b268c2b97fcc51fc2edf86777b9b63677a212dd3667c323b8b8a2d14161be

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
- feedback issue candidate 1件を、report cut時点で固定された参照だけから検証する prompt と AgentCallParameter を構築する。
- 検証結果は unresolved / resolved / not_actionable / inconclusive のいずれかを返す前提で、candidate ID、current evidence、human action などの事後条件を prompt に組み込む。
- READONLY の flagship・最大推論設定で実行し、live repository state、raw log、別 candidate、feedback state などを参照しない verification 専用の呼び出し設定を返す。

## Read this when
- feedback issue candidate の検証 prompt や起動パラメータの構築方法を確認・変更するとき。
- report cut reference の利用範囲、検証結果の判定基準、Structured Output の事後条件を確認するとき。
- feedback verification call の読み取り専用設定、モデル・推論設定、prompt schema path、indexing preflight 無効化の責務を確認するとき。

## Do not read this when
- feedback issue の生成・報告・状態管理そのものを確認する場合。
- 検証結果の Structured Output schema の項目や型を直接確認する場合は、対応する schema ファイルを読むべきである。
- 一般的な AgentCallParameter や prompt rendering の共通仕様を確認する場合は、各共通実装を直接読むべきである。

## hash
- 0f06a72659b2a72bc8e9d6b17dcd6b59df5690318ff4bffe480a5ed4d831e493
