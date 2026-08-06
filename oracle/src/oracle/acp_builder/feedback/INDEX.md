# `normalize_issue.json`

## Summary
- 対象ファイルは、複数の観測結果を既存 issue に統合するか新規 issue として正規化するための Structured Output schema を定義する。判断、issue 要約、人間の対応候補、影響、原因・存在可能性の評価、関連 issue ID を扱う。
- 入力候補の issue ID を既存 issue に統合する場合と、新しい issue として扱う場合の排他的な出力契約を提供する下位仕様への入口である。

## Read this when
- 観測結果から issue の統合・新規作成判断を行う処理、またはその出力項目と必須条件を確認するとき。
- 原因の確度、report 時点での存在可能性、対応候補、影響の記述ルールを確認するとき。

## Do not read this when
- 単に issue の実装箇所や実行フローを調べるだけで、正規化結果の出力契約を変更・検証する必要がないとき。
- issue の保存・取得や別の Structured Output schema を直接確認する必要があるときは、それらの対象を読む。

## hash
- 947eda2a227a3d2ab1e05ebeeb2dc445c6feb50d948fa0c9d09f6428f79998f9

# `normalize_issue.py`

## Summary
- `cmoc feedback report` における曖昧な issue の正規化用 agent call パラメータを構築する正本実装。構造化 observation と候補 issue、指定された現在参照対象だけを入力範囲として、既存 issue への統合または新規 issue 作成を判断する prompt を生成する。feedback issue 正規化の prompt 構成、参照範囲、決定論的事後条件、モデル・読み取り専用設定を確認する入口となる。

## Read this when
- feedback report の issue 正規化 prompt を変更・レビューするとき
- observation と既存 issue 候補の比較、参照対象の制約、既存 issue ID の扱いを確認するとき
- 正規化 agent call のモデル設定、推論強度、Structured Output schema 連携を確認するとき

## Do not read this when
- feedback observation の生成や raw log の解析処理を変更するとき
- 正規化結果の Structured Output schema 自体を変更するとき
- issue の永続化、表示、human disposition の決定処理を確認するとき

## hash
- 2794fc4b35000003fe7ae675a062ab6f5f75c07c921b2b25210ce2f4e90bf7c9
