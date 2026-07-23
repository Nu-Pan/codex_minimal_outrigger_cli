# `doc`

## Summary
- cmoc の正本仕様ドキュメント群を収録するディレクトリ。アプリケーション仕様、branch・commit・worktree のモデル、不採用案、開発ルールなど、個別の仕様・開発判断を確認するための入口。

## Read this when
- cmoc の仕様を横断的に調査するとき
- 対象機能に対応する oracle doc を特定するとき
- Python 実装、CLI 配置、開発環境、realization test の規則を確認するとき
- branch・session・run・worktree の関係や、不採用となった設計案の背景を調べるとき

## Do not read this when
- 確認対象の仕様文書が既に特定できており、その本文を直接読めるとき
- 実装コードやテストコードの詳細だけを調査するとき
- INDEX.md の読み方や一般的なルーティング規則を確認したいとき

## hash
- b7baf783ec2598bf68caa8b9623828d3e07294aee16a2d2ba4181c21f9cfd107

# `src`

## Summary
- oracle の実行時正本ソース群。設定・パス・構造化文書などの共通定義、AgentCallParameter と各サブコマンド向け prompt/Structured Output schema の構築、prompt 部品と完全 prompt の組み立てを扱う。`other`、`acp_builder`、`prompt_builder` が主な下位領域。

## Read this when
- cmoc の設定、ルートパス、Standard、StructDoc などの共通定義を調べるとき。
- AgentCall のモデル・推論負荷・ファイルアクセス設定や、indexing、tui、oracle、realization、session join 向けの呼び出しパラメータ構築を調べるとき。
- 完全 prompt の生成、prompt 部品、プレースホルダ、oracle/realization 標準、ファイルアクセス規則を調べるとき。

## Do not read this when
- サブコマンドの実行経路、ファイル探索、実際のモデル呼び出しを調べるとき。
- 特定の prompt 部品、Structured Output schema、共通定義、個別サブコマンドの AgentCall 構築だけを確認したいときは、対応する下位領域へ直接進む。

## hash
- fa8aeff5b44224b2ed27eb099784d579af225a149c4349aa7cb3b13b02c95307
