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
- フィードバック報告の observation と絞り込み済み issue candidate を比較し、既存 issue と新規 issue の同一性だけを判断する agent call パラメータを構築する。
- 入力外の状態を参照しない読み取り専用 prompt、モデル・推論設定、同一性判断専用の出力スキーマ、および実行コンテキストをまとめて返す。

## Read this when
- feedback issue の同一性判断用 prompt、agent call 設定、入力制約、または実行コンテキストを変更・確認するとき
- 構造化 observation と候補 issue の比較処理の入口を確認するとき

## Do not read this when
- issue の summary、impact、原因、重要度、現在性、actionability、human action、verification verdict、relation を生成・評価するとき
- 候補 issue の絞り込み、feedback state、raw log、過去の Codex session など入力外の情報を調べるとき
- feedback の報告や保存処理そのものを変更・確認するとき

## hash
- 4d14145ebaacd4d01bd49d862c8890a58585af9ce4934843ae8bb58b8a7c1998

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
- `cmoc feedback report` における issue candidate 検証用の AgentCallParameter を構築する。report cut で固定された candidate と参照だけを入力し、未解決・解決済み・報告対象外・判定不能の verdict を返す読み取り専用 verification prompt、実行コンテキスト、Structured Output schema を定義する。feedback report の issue verification 処理に進むための入口である。

## Read this when
- `cmoc feedback report` の issue candidate 検証 prompt、verdict 条件、report cut reference の扱い、または verification 用 AgentCallParameter を変更・確認するとき
- issue verification の読み取り専用制約、動的 prompt の入力、Structured Output schema との接続を確認するとき

## Do not read this when
- feedback observation の記録・送信処理だけを変更するとき
- issue candidate の生成、report cut の作成、または verification 後の feedback 保存処理を直接確認するとき
- 一般的な ACP builder の共通設定や、検証結果の schema 定義だけを確認するときは、それぞれの直接の実装・定義へ進む

## hash
- 7208567346b271507910b7bf3d6a9d37b25815f9503779a9a871475910e7bc23
