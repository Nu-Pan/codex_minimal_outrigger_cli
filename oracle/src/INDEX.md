# `oracle`

## Summary
- AI コーディングエージェント呼び出しの prompt、起動パラメータ、入力契約、設定、パス解決、構造化文書レンダリングを扱う下位領域への入口。
- agent call の構築、共通 prompt 生成、feedback 入力契約、エディタ入力、設定・パス基盤を目的別に案内する。

## Read this when
- agent call や prompt の構成、起動条件、入力契約、設定・パス解決、構造化文書の扱いについて、適切な下位領域を特定するとき。
- feedback、oracle review、realization、editor input handoff などの処理段階や契約の確認先を探すとき。

## Do not read this when
- 特定の下位要素の詳細仕様、実装、schema、保存・集約処理、または個別のレビュー結果だけを確認したいとき。
- Codex CLI の実行処理、サブコマンドの業務ロジック、prompt の具体的な共通生成規則を直接調べたいとき。

## hash
- 38e66436c16f06ac0986d58948d26d13515f6bc69f97b4587936c7664ca2cc91
