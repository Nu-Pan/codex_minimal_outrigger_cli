# `oracle`

## Summary
- oracle file レビュー向けの agent call parameter 正本と Structured Output schema をまとめる領域。新規所見の列挙、所見の擁護・反証理由の追加調査、採否判定、所見リストの整理に関する prompt 構成と出力契約を扱う。

## Read this when
- `cmoc review oracle` で AI エージェントへ渡す role、goal、補助 prompt、file access mode、model class、reasoning effort、placeholder、標準文脈、出力 schema の対応を確認または変更したいとき。
- oracle file レビュー所見の生成、擁護理由調査、反証理由調査、採否判定、重複・矛盾整理のいずれかの入出力契約や prompt 構成を確認したいとき。
- 既知所見や既知理由との重複排除、新規所見・新規理由がない場合の表現、所見に必要な重大度・見出し・根拠 oracle file・理由の制約を確認したいとき。

## Do not read this when
- oracle file 本体の仕様内容や、レビュー基準本文そのものを確認したいとき。
- `cmoc review oracle` 以外の review サブコマンドや、oracle review 以外の agent call parameter を調べたいとき。
- agent call parameter の共通データ構造、path placeholder 解決、完全 prompt 構築処理、構造化 markdown rendering などの汎用実装詳細を調べたいとき。
- INDEX.md 用エントリーの生成形式やルーティング方針を確認したいだけのとき。

## hash
- b4068ee6c36f1c68a4680220ee58baf96b626e723112eacfaa546772bc47ec57
