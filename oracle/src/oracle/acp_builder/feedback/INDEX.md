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
- 構造化された feedback observation と、事前に絞り込まれた既存 issue candidate を比較し、同一 issue か新規 issue かを判定するための agent call parameter を構築する。feedback issue の同一性判断に必要な prompt、読み取り専用の call context、Structured Output schema の指定を担う。

## Read this when
- feedback observation を既存 issue candidate と照合し、同一 issue の再報告か新規 issue かを判定する処理を変更・調査するとき
- 同一性判断用 prompt の入力範囲、参照禁止条件、または agent call の読み取り専用設定を確認するとき

## Do not read this when
- issue の summary、impact、原因、重要度、現在性、actionability、human action、verification verdict、relation を生成・確定する処理を調べるとき
- 候補 issue の絞り込みや feedback state の保存・更新処理を直接調べるとき

## hash
- 036ff1f061244c0860726b49546fb80933306c407207e135ecd6003c6b2eff48

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
- feedback issue candidate を、report cut 時点で固定された参照だけから検証する prompt と agent call 起動パラメータの構築定義。
- 人間の対応が必要な未解決 issue の判定に加え、resolved・not_actionable・inconclusive の判定条件と Structured Output の事後条件を prompt に組み込む。
- 読み取り専用の agent call として、指定モデル・推論設定・検証用 schema・agent call context を返す。

## Read this when
- feedback issue candidate の検証 prompt または検証用 agent call の起動パラメータを変更・調査するとき
- report cut reference 以外の live state や feedback state を読まない検証境界を確認するとき

## Do not read this when
- feedback issue の報告・保存・候補生成を変更・調査するとき
- 一般的な agent call パラメータや検証結果 schema を直接確認すれば足りるとき

## hash
- 06e683b45d98d5e107abd1ec4bfe81ac61b67e21180475bfc787bfd4b603373b
