# `fork`

## Summary
- refactor fork における変更差分の要約生成と、ファイル単位のレビュー・修正処理に必要な AgentCallParameter 構築を扱うディレクトリ。変更要約およびレビュー結果の構造化出力スキーマと、それぞれの prompt・実行条件を定義する実装が入口となる。

## Read this when
- refactor fork の変更差分を人間向けに要約する処理を確認・変更するとき
- ファイル単位の実装レビュー、修正、検証を行う AgentCallParameter の構成を確認するとき
- 変更要約またはレビュー・修正結果の Structured Output 契約を確認するとき

## Do not read this when
- 実際のレビュー対象実装や個別仕様の内容を調査するとき
- 通常の realization 実装・テストの挙動を確認するとき
- このディレクトリの処理を呼び出す上位の fork 運用や、対象外の prompt builder を調査するとき

## hash
- 7d6f18f66b1ef7d6f17f045706a02537e05f1ae64673e707ec12639bcc9c359e
