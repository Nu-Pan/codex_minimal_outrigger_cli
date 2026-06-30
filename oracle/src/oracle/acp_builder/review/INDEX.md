# `oracle`

## Summary
- `cmoc review oracle` の各段階で使う oracle file レビュー用 agent call parameter と Structured Output schema をまとめるディレクトリ。
- 新規所見の列挙、所見の擁護・反証、採否判定、重複・矛盾の整理について、AI 呼び出しへ渡す prompt 断片、読み取り制約、モデル設定、出力契約を確認する入口になる。
- レビュー所見の生成から検証・整理までの出力境界や prompt 接続を段階別にたどるための下位ファイルを収める。

## Read this when
- `cmoc review oracle` の oracle file レビュー処理で、所見列挙、所見検証、採否判定、所見マージのいずれかの agent call parameter や出力 schema を確認・変更したいとき。
- レビュー対象 oracle file、既知所見、既知の擁護理由・反証理由、所見リストが、各レビュー段階の prompt や Structured Output にどう渡るか調べたいとき。
- oracle file を根拠にした新規所見、新規理由、採否理由、重複・矛盾整理の応答契約を段階別に確認したいとき。
- `PURE_ORACLE_READ`、review oracle standard、対応 JSON schema、reasoning effort、モデル設定など、oracle review 用 agent call の正本 prompt 断片を探すとき。

## Do not read this when
- `cmoc review oracle` サブコマンド全体の CLI 引数、実行制御、結果集約、表示処理など realization implementation 側の挙動を確認したいとき。
- oracle file 全般の品質基準、oracle standard、review oracle standard の本文そのものを読みたいとき。
- oracle review 以外の agent call parameter、または oracle file 以外を読むレビュー処理を調べたいとき。
- INDEX.md エントリーやルーティング文書の生成規則を確認したいとき。

## hash
- 0ca42e71c8d96d420ccfc746ebb73086636777932770c73e0dac3ef85aefe3d9
