# `acp_builder`

## Summary
- AIエージェント呼び出し用パラメータを構築する正本ソースを扱うディレクトリ。共通の論理モデル、INDEX.md生成、oracle操作、realization適用、session競合解消、TUI起動に関する下位領域への入口を提供する。

## Read this when
- agent call のモデル、推論強度、権限、Structured Output、作業ディレクトリなど共通パラメータの定義を確認するとき
- INDEX.md エントリー生成、oracle 操作、realization 適用、session join の競合解消、TUI 起動に関する agent call 構築を調査・変更するとき

## Do not read this when
- oracle file や realization file の具体的な仕様・実装内容を確認するとき
- 一般的な prompt 構築、path 解決、構造化文書レンダリングなど、別の共通実装を調査するとき
- 対象ディレクトリに参照可能な正本ソースが存在するかどうかだけを確認したいとき

## hash
- ef4983f1a55a0ce984ef42acbc2a5af845c923a9b4d9adef137525352c7dead8

# `other`

## Summary
- oracle/other 配下の設定・パスモデル・規範構造・Markdown 構造化文書を扱う Python モジュール群。設定値や root 解決、Standard/Requirement の変換、StructDoc のレンダリング実装へ進む入口。

## Read this when
- CmocConfig などのリポジトリ固有設定、agent call のパスモデル、oracle standard の構造化、または StructDoc の Markdown レンダリングを調査・変更するとき
- これらの責務をまたぐデータ構造や変換処理の入口を探すとき

## Do not read this when
- CLI の実行フロー、設定ファイルの生成・同期、個別の規範本文、または ModelClass・ReasoningEffort 自体の定義だけを調査するとき
- 対象が path model、Standard/Requirement、StructDoc のいずれにも関係しない realization 実装や文書のとき

## hash
- 3f5e687e9358b4be7c379094f67af7a85e77c5dabc9832409073fbae1b51cc5d

# `prompt_builder`

## Summary
- プロンプトビルダーの中核実装をまとめたディレクトリ。placeholder 型、完全な agent call プロンプトの構築、エディタ初期文面の生成、oracle／realization／INDEX などの規範部品を扱う。プロンプト生成やその規範注入の実装を調査・変更する際の入口。

## Read this when
- agent call に渡す完全なプロンプトの構成や注入順序を確認するとき
- プロンプト入力エディタの初期文面や自動注入指示を変更するとき
- oracle／realization、レビュー、INDEX.md ルーティングなどの規範を prompt builder に組み込む処理を調査するとき
- placeholder の型や、文字列・Path を含む置換対象の表現を確認するとき

## Do not read this when
- 個別のプロンプトパーツ本文だけを確認・変更するとき
- プロンプト生成と無関係な CLI、パスモデル、構造化文書機構、プロダクト機能を調査するとき
- Codex CLI の実行環境やテスト手順の正本仕様を確認するとき

## hash
- b99f333e91b7f4bdcff91d80714190551f6784e6928c9781dd074507a912aee1
