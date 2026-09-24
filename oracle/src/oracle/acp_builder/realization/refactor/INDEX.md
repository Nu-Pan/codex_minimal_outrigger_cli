# `fork`

## Summary
- 対象ファイルを起点に oracle と realization を調査し、realization を修正するファイル単位レビュー・修正 agent call の prompt と起動パラメータを定義する。
- 指定 commit 間の差分全体を読み取り、人間向けに要約する agent call の prompt と起動パラメータを定義する。

## Read this when
- refactor fork のファイル単位レビュー・修正 agent call の指示、アクセス権、起動条件、または所見と修正結果の扱いを変更するとき。
- 指定 commit 範囲の変更要約 agent call の指示や、差分取得の前提を変更するとき。

## Do not read this when
- 特定の oracle または realization file の内容をレビュー・修正するときは、その file と対応する要求を直接読む。
- 特定の commit 間の実際の変更内容を調べたり要約したりするときは、対象の Git 差分を直接確認する。

## hash
- b4b632ac0e3cd5ed0f95a54283fd8941a98e12ede141996d50ede89ef2ad4da3
