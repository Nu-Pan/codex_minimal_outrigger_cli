# `normalize_issue.json`

## Summary
- observation を既存 issue に統合するか新規 issue とするかを表す正規化結果の JSON Schema。統合先 ID、新規 issue 判定、要約、人間の対応候補、影響、原因評価、存在可能性、関連 issue ID を定義する。

## Read this when
- feedback observation の issue 正規化処理、統合判断、またはその入出力契約を確認・変更するとき
- 正規化結果の必須項目、列挙値、文字数制約、関連 issue ID の扱いを確認するとき

## Do not read this when
- feedback observation の収集・送信だけを扱い、issue 正規化結果を扱わないとき
- 正規化処理の具体的な実装やテスト内容を確認する場合

## hash
- 8e1462f8e78706cfa4ce334f96491af6630563d003815a43d4df01903460f2d8

# `normalize_issue.py`

## Summary
- 構造化された feedback observation と絞り込み済みの既存 issue 候補を入力として、曖昧な issue の既存 issue への統合または新規作成を判断する agent call parameter を構築する oracle src。
- 参照範囲を現在の指定参照対象に限定し、raw log・過去 session・feedback 保存 file の追加調査を禁止する prompt、モデル設定、READONLY 権限、構造化出力 schema の指定を担う。

## Read this when
- `cmoc feedback report` の observation を既存 issue または新規 issue に正規化する prompt の挙動を確認・変更するとき
- feedback 正規化 agent call の参照範囲、入力形式、モデル・推論設定、Structured Output 制約を確認するとき

## Do not read this when
- feedback issue の保存形式や human disposition の運用を確認したいとき
- 正規化結果の JSON schema 自体を確認したいときは、対応する schema を直接読む
- 一般的な prompt 構築や別の agent call parameter の実装を確認したいとき

## hash
- 8f2e7aa4c6b2f0f6fd3deec26e2c17e269485c058aeaa9f354330ae1b74fc50b
