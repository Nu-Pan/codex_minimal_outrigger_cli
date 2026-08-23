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
- 構造化された feedback observation と絞り込み済みの既存 issue candidate を比較し、同一 issue か新規 issue かだけを判定する agent call の prompt と起動パラメータを構築する。入力外の情報や候補外 issue を参照せず、判定結果の issue ID 整合性も指定する feedback 同一性判断の実装入口。

## Read this when
- feedback observation と既存 issue candidate の重複・同一性判定用 agent call を追加、変更、レビューするとき
- 同一性判定 prompt の入力範囲、出力後条件、model・reasoning・file access・preflight 設定を確認するとき

## Do not read this when
- feedback issue の summary、impact、原因、現在性、actionability、human action、verification verdict、relation を生成・評価する処理を調べるとき
- candidate の絞り込み、feedback state の読み取り、raw log や過去 session の参照を調べるときは、該当する入力生成・候補管理の対象を直接読む

## hash
- 6cd458da7a9bfd26658bdb9210b7cee1828a84c50e7e7130d66ed19550d4e89b

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
- feedback issue candidate 1件の検証用 AgentCallParameter を構築する定義。report cut 時点で固定された参照だけを入力として prompt、読み取り専用実行条件、最高品質のモデル設定、Structured Output schema、preflight 無効化をまとめる。
- issue candidate と report cut references を動的 prompt に埋め込み、verdict の意味、参照制約、変更禁止、Structured Output の事後条件を静的 prompt として指定する。feedback 検証の prompt 文面や起動パラメータを変更するときの入口。

## Read this when
- feedback issue candidate の unresolved / resolved / not_actionable / inconclusive 判定 prompt を変更するとき
- report cut reference の受け渡し、読み取り範囲、変更禁止、verdict の事後条件を確認するとき
- feedback 検証 agent のモデル、推論強度、実行ディレクトリ、preflight、structured output schema の起動設定を変更するとき

## Do not read this when
- feedback issue の検証結果 schema の項目や型だけを確認したいときは、対応する JSON schema を直接読む
- feedback issue の報告・保存・report cut 処理や候補生成の挙動を変更するときは、それぞれの実装定義を直接読む
- 一般的な prompt 構築規則や AgentCallParameter の共通仕様だけを確認するときは、共通の prompt builder / ACP 定義を直接読む

## hash
- 2ee4f76b63e38f555cb47acd58fdc1391aba31a87cb827bf9a569e00488018f3
