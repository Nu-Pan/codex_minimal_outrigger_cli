# `oracle`

## Summary
- cmoc の agent call 構築を支える正本モデルと入力契約をまとめた領域。agent call の共通設定・用途別 builder、prompt 構築、パス・設定・構造化文書、エディタ入力上書き、feedback 報告の入口を案内する。

## Read this when
- agent call の構築責務や共通入力契約の所在を確認するとき。
- prompt、パス、設定、構造化文書、エディタ入力 handoff、feedback 報告のどの領域から読み始めるべきか判断するとき。
- quota probe、indexing、oracle・realization、session、TUI など用途別の builder を探すとき。

## Do not read this when
- 特定用途の agent call における prompt や Structured Output schema の詳細だけを確認したいとき。
- agent call の実行処理や Codex CLI の実際の挙動を調査したいとき。
- 設定保存、feedback 受付、oracle・realization の編集など、個別処理の実装や具体的な文書内容だけを確認したいとき。

## hash
- 7dd58b5536ac78fa779bdfa19789e1f95a6b7d64447b04ef07d412e12e3ab4c3
