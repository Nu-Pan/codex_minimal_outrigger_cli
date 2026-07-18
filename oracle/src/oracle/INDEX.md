# `acp_builder`

## Summary
- ACP 呼び出しに関する基礎パラメータ、indexing・oracle・realization・session・tui 向けの agent call 構築定義を含む oracle src ディレクトリ。各サブ領域の呼び出し条件、プロンプト、権限設定、Structured Output 契約を確認する入口。

## Read this when
- ACP builder 配下の agent call パラメータ、プロンプト、モデル・推論強度、ファイルアクセス権、Structured Output schema を調査・変更するとき。
- indexing、oracle、realization、session、tui の各 agent call 構築定義の担当領域や参照先を特定するとき。

## Do not read this when
- 実際の agent 呼び出し実行、サブコマンド本体、TUI 画面処理、共通 prompt builder の実装だけを調査するとき。
- oracle file の編集内容やレビュー基準など、agent call パラメータ以外の正本仕様を確認するとき。

## hash
- ff4aa39bc258ff493eedba7c281f26f348e196a5ba5e85ef52b26b7b0c5b9050

# `other`

## Summary
- cmoc の設定・パス解決・規範データ構造・構造化 Markdown 文書化を担う oracle 実装群。設定定義、プレースホルダ付きパスの解決、Standard/Requirement の構造化、StructDoc の Markdown 変換を確認するための入口。

## Read this when
- cmoc の設定 dataclass や既定値、パス表記と各ルート解決、規範データ構造、構造化文書の Markdown 出力を変更・調査するとき。
- 複数の oracle 実装にまたがる設定・パス・規範文書・レンダリングの連携を確認するとき。

## Do not read this when
- 個別の CLI 実行経路、設定ファイルの生成・同期手順、Codex CLI 呼び出し、oracle review の実行ロジックを調べるとき。
- ModelClass、ReasoningEffort、StructDoc の利用側、個別の標準文書、Markdown 以外の文書形式だけを調べるときは、各定義元・利用側・個別文書を直接読む。

## hash
- e4a26d1052ac747c36b4b112e2b6587e774ce5e6d5668a64ad67b48982fe9195

# `prompt_builder`

## Summary
- プレースホルダ名と実パス・文字列の対応を表す型定義を提供する。置換対象の表現を確認する入口。
- 固定・動的パーツ、プレースホルダ、標準ルール設定からエージェント呼び出し用の完全なプロンプトを構築する。全体構造や組み立てを調査するときの入口。
- oracle・realization、INDEX.md、ファイルアクセス規則、レビュー基準など、プロンプト生成に注入する標準ルールの部品をまとめる。各規範の本文や構成を変更・確認するときの入口。

## Read this when
- プレースホルダ展開用の型や、文字列とPathを含む置換対象の表現を確認するとき。
- 完全なプロンプトの構造、標準ルールの依存関係、動的プロンプトやプレースホルダの組み立てを調査・変更するとき。
- oracle・realization、INDEX.md、ファイルアクセス規則、レビュー基準、prompt builder部品の生成内容を調査・変更するとき。

## Do not read this when
- プロンプト本文の生成手順や置換ロジックの詳細だけを調べるとき。
- 特定の注入パーツや個別標準ルールの本文だけを調べるとき。
- 個別のoracle file・realization file、CLIコマンド、実際のファイル操作、prompt builderの生成処理やファイル探索処理だけを調べるとき。

## hash
- 824e06f5f482694f3ac1d41a92029bb7cfb1ed304a449f4e07ed8111d0f96b98
