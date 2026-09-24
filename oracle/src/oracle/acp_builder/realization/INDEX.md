# `apply`

## Summary
- oracle file の指定 commit 範囲に含まれる変更を realization 全体へ反映する fork 用 agent 呼び出しの prompt と起動パラメータを組み立てる実装への入口。

## Read this when
- commit 差分を起点とする realization apply の追従対象、作業範囲、起動条件を確認・変更するとき。
- oracle file の変更を realization に反映する処理で、指定 commit 範囲の受け渡しや agent 呼び出し内容を調べるとき。

## Do not read this when
- commit 差分の人間向け要約や、差分に依存しないファイル単位のレビュー・修正用呼び出しが目的なら、refactor 側の対象から確認するとき。
- agent 呼び出し全般の共通処理を調べる場合は、該当する共通実装から確認するとき。

## hash
- 1a7c545c1945749c633abcf0a8ffde4076221a1515e0aff35c99808776c51a1a

# `refactor`

## Summary
- refactor fork 用の agent call 構築定義をまとめる入口。commit 差分の要約と、対象ファイルのレビュー・修正という二つの呼び出しを調整するときに参照する。

## Read this when
- refactor fork の変更要約呼び出しが、どの commit 範囲を対象にするか確認するとき。
- 指定ファイルから所見を調査し、対応する realization file を修正する呼び出しの指示や制約を確認するとき。

## Do not read this when
- 実際の差分やレビュー結果を確認する場合は、その実行結果や対象 commit 範囲を直接調べる。
- 共通の prompt 合成、path 解決、file access mode、preflight の挙動を確認する場合は、それらを定義する共通部品を読む。
- 実装適用など別フェーズの呼び出しを調べる場合は、そのフェーズの定義を読む。

## hash
- c3978677de16c4e9c9913210e654257d656947613274247636402c7420633a46
