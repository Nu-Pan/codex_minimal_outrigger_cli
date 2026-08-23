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
- 構造化済み observation と絞り込み済みの既存 issue candidate を比較し、feedback issue が既存か新規かだけを判定する起動パラメータを構築する。入力以外の状態を参照しない限定的な同一性判断用 prompt、読み取り専用コンテキスト、Structured Output schema、主力モデル等の実行条件を定義する。

## Read this when
- feedback issue の同一性判定用 agent call の prompt や起動パラメータを変更・確認するとき
- 構造化 observation と既存 issue candidate の比較範囲、入力閉鎖、決定論的な issue ID 条件を確認するとき

## Do not read this when
- feedback issue の summary、impact、原因、重要度、現在性、actionability、human action、verification verdict、relation を生成・評価する処理を確認するとき
- 候補 issue の絞り込み、feedback observation の構造化、または Structured Output schema 自体を直接確認するとき

## hash
- 02b45d682e9fa69c20f23fdb3745911e022552b7852102dedfd79691776d47ae

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
- feedback issue candidate 1件を、report cut 時点で固定された参照だけから検証する prompt と AgentCallParameter を構築する。verdict の定義、参照・変更禁止、Structured Output の決定論的事後条件、モデル・推論・アクセスモード・preflight 設定を検証 agent の起動定義としてまとめる。

## Read this when
- feedback issue candidate の現在性と人間対応の要否を検証する prompt を確認するとき
- report cut reference 以外を読ませない検証境界、verdict 条件、current evidence と human action の後続条件を変更・調査するとき
- feedback 検証 agent のモデル品質、readonly 設定、routing policy、indexing preflight の扱いを確認するとき

## Do not read this when
- feedback issue candidate の生成、report cut による参照固定、または feedback state の管理を確認したいときは、それらを直接担う対象を読む
- 検証結果の Structured Output schema の項目名・型・形式だけを確認したいときは、隣接する schema を直接読む
- 検証対象の具体的な candidate や report cut reference の内容を確認したいときは、この起動定義ではなく入力データの生成元を読む

## hash
- 8ee8b0295ac4e850b8049f7fe062f276095ef01cfddd32d95ca3db56b0c2957f
