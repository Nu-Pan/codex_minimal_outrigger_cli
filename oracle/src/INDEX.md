# `oracle`

## Summary
- cmoc の oracle・realization 関連機能と、それらを動かす agent call の prompt・起動パラメータをまとめる中核領域です。共通の agent call データモデル、prompt 構築、設定・パス・構造化文書の補助機能を提供し、feedback、indexing、oracle、realization、session、TUI の各下位領域へ進む入口になります。
- agent call の共通パラメータや論理モデル・推論強度・ファイルアクセスモードを確認する場合は `acp_builder`、完全 prompt の構成や policy 部品を確認する場合は `prompt_builder`、設定・パス解決・Markdown 構造化を確認する場合は `other` へ進みます。

## Read this when
- oracle または realization に関する agent call の構築箇所や、prompt・Structured Output・起動設定の入口を探すとき。
- feedback、indexing、oracle review、realization 実行、session、quota probe、TUI の下位機能の配置を判断するとき。
- agent call の共通データモデル、設定、パス境界、構造化文書の扱いを確認するとき。

## Do not read this when
- 特定の feedback、indexing、oracle、realization、session、TUI 機能の詳細だけを調べるときは、対応する下位ディレクトリへ直接進む。
- Codex CLI の実際の実行処理や backend のモデル名変換規則を調べるとき。
- 個別の正本仕様、realization 実装、feedback state、既存の INDEX.md の内容そのものを確認するとき。

## hash
- 8f219b0f481d2d36f48d431b979cbc61f6e794432621e861cb50c59b6786c24d
