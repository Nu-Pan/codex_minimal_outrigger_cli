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
- feedback issue の同一性判断に使う agent call parameter と prompt を構築する。構造化 observation と絞り込み済み既存 issue candidate を入力として、既存 issue か新規 issue かだけを判定する処理の入口。

## Read this when
- feedback observation と既存 issue candidate の同一性判定用 agent call の起動条件、モデル設定、読み取り専用の prompt 構成を確認するとき。
- 構造化出力 schema の配置や agent call のパスコンテキスト・preflight 設定を確認するとき。

## Do not read this when
- issue の summary、impact、原因、現在性、actionability、human action、verification verdict、relation を生成・評価するときは、この定義ではなく、それらを扱う対象へ進む。
- 候補 issue の絞り込みや feedback state、raw log、過去 session の参照が必要なときは、この対象を直接の入口にしない。

## hash
- 8e47b40b3a9bd5e10317283384d3395d0a27b89ae34aa0f6015d6c06cf1a70dc

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
- feedback issue candidate 1件を、report cut時点で固定された参照情報だけから検証するための prompt と AgentCallParameter を構築する。検証結果の判定基準、参照・変更禁止事項、Structured Output の事後条件を prompt に組み込み、指定モデル・最大推論・読み取り専用・構造化出力スキーマ・起動ディレクトリを設定する。
- feedback issue の検証用 agent call の prompt、起動パラメータ、参照制約、または構造化出力の検証条件を変更・確認するときの入口となる。issue candidate の生成や feedback の送信、検証結果スキーマ自体の定義を直接確認する場合は、それぞれの担当対象へ進む。

## Read this when
- report cut reference に限定した issue candidate 検証の prompt 文面や判定条件を確認するとき
- feedback 検証 agent call のモデル、推論強度、読み取り専用設定、起動時パラメータを確認するとき
- current evidence、human action、candidate ID の一致など、構造化出力に対する prompt 内の事後条件を確認するとき

## Do not read this when
- issue candidate の作成・収集ロジックを確認するとき
- feedback observation の送信や feedback state の更新処理を確認するとき
- 検証結果の Structured Output schema の項目・型・形式だけを確認するとき

## hash
- 44c557bc915630d3a9ac2f5b324c8e6dc5a665510d792fe1f275c9658d6f3b87
