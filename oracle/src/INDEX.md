# `oracle`

## Summary
- AI agent call の prompt・起動パラメータ・Structured Output schema を構築する oracle 定義をまとめたディレクトリです。agent call の共通契約は `acp_builder`、feedback 処理は `feedback`、設定・パス・構造化文書は `other`、prompt の組み立てと目的別 policy は `prompt_builder` へ進みます。

## Read this when
- agent call の論理モデル、Reasoning effort、ファイルアクセスモード、作業ディレクトリ、indexing preflight の定義を確認するとき
- feedback issue の入力・同一性判断・検証に関する oracle 定義を調査するとき
- oracle・realization・INDEX.md 生成・conflict 解消などの prompt policy と構築経路を確認するとき
- cmoc 固有設定、agent call のパス解決、構造化文書の Markdown 化を確認するとき

## Do not read this when
- 特定の agent call の具体的な prompt、起動処理、Structured Output schema だけを確認する場合は、対応する `acp_builder` 配下の実装や schema を直接読むとき
- prompt の構成部品や目的別 policy だけを確認する場合は、`prompt_builder` 配下を直接読むとき
- 設定・パスモデル・構造化文書ヘルパーの個別実装だけを確認する場合は、`other` 配下を直接読むとき
- oracle や realization の正本仕様、実装本体、テストの挙動を確認する場合は、この oracle 定義ディレクトリではなく対応する正本仕様・realization・test を読むとき

## hash
- 5e532eb0d9068768715455b0f409089b5c73e0fcb04353352035a03710d4fc6b
