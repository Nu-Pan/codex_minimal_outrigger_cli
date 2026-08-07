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
- `cmoc feedback report` における曖昧な issue の正規化用 AgentCallParameter を構築する正本実装。構造化 observation と絞り込み済み既存 issue 候補を入力し、指定参照範囲だけを許可する読み取り専用 prompt、モデル設定、Structured Output schema を組み立てる。

## Read this when
- feedback observation から既存 issue への統合または新規 issue 作成を判断する prompt の仕様・参照範囲・出力制約を確認するとき
- feedback 正規化処理の AgentCallParameter、モデル、推論強度、読み取り専用設定、Structured Output schema の対応を確認するとき

## Do not read this when
- feedback issue の保存処理や human disposition の決定を調べるとき
- raw Codex call log、feedback observation 保存 file、または別の prompt builder の実装を直接調べるべきとき

## hash
- 126a46c0dada76cf04e9fcf8ffc0dd77e06601e5dd44f4ac9519f5a06c43f0e3
