# `fork`

## Summary
- refactor fork における変更要約とファイル単位レビュー・修正の AgentCallParameter、およびそれらの Structured Output schema を定義するファイル群。変更要約・レビュー結果の形式確認と、各 prompt 構築処理の変更時に参照する入口。

## Read this when
- refactor fork の変更要約出力形式、根拠ファイル一覧、要約結果の検証項目を確認するとき
- ファイル単位レビュー・修正の所見フォーマットや、根拠・oracle 要求・対応・検証結果の構造を確認するとき
- 変更要約またはファイル単位レビュー・修正の prompt 構成、対象 path、実行条件、モデル設定、Structured Output schema の参照先を確認・変更するとき
- レビュー時の oracle・realization 参照規則や修正・検証条件を確認するとき

## Do not read this when
- レビュー対象ファイルの具体的な実装内容や個別の所見を調査するとき
- 変更差分そのものや要約結果の具体的内容を確認するとき
- 共通 prompt builder や path model の内部仕様を直接確認するとき
- 通常の実装・テスト仕様や、このディレクトリ以外の出力スキーマを扱うとき

## hash
- 12913bfeda81826d1ac4f3960be1353550c3ad0b4e4c95e1afc3ad82d88b6754
