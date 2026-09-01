# `cmoc oracle review` を採用しない理由

## `cmoc oracle review` とは

`cmoc oracle review` は、通常の workload とは独立して oracle file のスナップショットを網羅的に検査し、潜在的な問題を人間向けの Markdown レポートへまとめる専用サブコマンドだった。oracle file 自体は変更しない。

`cmoc oracle review` をやらないとは、この独立した網羅検査とレポート作成の仕組みを提供しないことを指す。通常の workload で必要な oracle file の調査や、そこで解消できない問題を feedback observation として報告することは禁止しない。

## 判断

`cmoc oracle review` は提供しない。oracle file だけを網羅的に検査すると、意図的な未定義部分と問題の境界が曖昧になる。根拠の薄い所見に基づく修正の反復は、oracle file の過剰な詳細化と肥大化を招く。

## 代替

通常の workload で解消できず、人間の対応が必要だと判明した問題を feedback observation として報告し、`cmoc feedback report` で確認する。

報告基準は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の「agent による報告」を正本とする。report 処理は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の `cmoc feedback report` を正本とする。

通常の workload で発見されない潜在的な問題は残り得る。この不確実性を許容し、oracle file を疎に保ちながら実装可能な安定状態へ到達することを優先する。
