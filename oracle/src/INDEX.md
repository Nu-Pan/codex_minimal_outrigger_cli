# `oracle`

## Summary
- AI コーディングエージェント呼び出しに必要な共通パラメータ、用途別 builder、prompt 構築、入力スキーマ、設定・パス・Markdown レンダリングの実装入口をまとめる領域。

## Read this when
- agent call の共通設定や用途別 builder の責務を確認するとき。
- prompt の構築規則、policy の組み込み、editor handoff、feedback 入力契約を調べるとき。
- cmoc の設定・パス解決・構造化文書の Markdown 化に関する実装入口を探すとき。

## Do not read this when
- 特定機能の prompt、出力契約、スキーマ、保存処理などの詳細を確認する場合は、対応する下位対象を直接読むとき。
- Codex CLI の実行処理そのもの、oracle・realization の具体的な仕様、または INDEX.md の構造規則だけを調べるとき。

## hash
- ce77b41f4fdcc585628084d858cbdfacd67cf99e44a47ac4513cc27a257ad5a0
