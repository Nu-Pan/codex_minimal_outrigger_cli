# `acp_builder`

## Summary
- oracle 用 ACP builder の実装と Structured Output schema を扱うディレクトリ。`cmoc oracle edit` と `cmoc oracle review` の agent call 設定、完全プロンプト、ログ保存、所見の検証・統合、入出力契約を確認する入口。

## Read this when
- `cmoc oracle edit` の TUI 起動条件、完全プロンプト、ログ保存、モデル・推論強度・ファイルアクセス設定を確認または変更するとき。
- `cmoc oracle review` の所見列挙、擁護・反証、採否判定、重複・矛盾の統合を確認または変更するとき。
- oracle review 用 agent call の prompt と Structured Output schema の対応を追跡するとき。

## Do not read this when
- 共有 ACP パラメータ型、モデル設定、ファイルアクセスモード、パス解決の一般仕様だけを確認するとき。
- 完全プロンプトの共通構成や oracle review の一般基準だけを確認するとき。
- 個別の処理実装または schema が特定できており、このディレクトリ全体の構成を確認する必要がないとき。

## hash
- 1af78704400be823d007d8cfabfd2651babfe205b98721d0ba934ac4276ed3ea

# `other`

## Summary
- cmoc の設定モデル、パス解決、規範文書モデル、構造化文書の Markdown 変換を担う oracle src 群。設定・パス・標準文書・Markdown レンダリングの仕様確認における入口。

## Read this when
- cmoc 固有設定や Codex CLI の実行上限を確認するとき
- ルートパスのプレースホルダ解決・相互変換を確認するとき
- 規範文書のデータ構造や構造化文書の Markdown 出力を確認するとき

## Do not read this when
- 設定 JSON の永続化や doctor による同期処理だけを調べるとき
- CLI サブコマンドの個別入出力や業務ロジックを調べるとき
- 個別の標準文書の内容や Markdown 以外の文書形式を直接調べるとき

## hash
- 70e9314013e0b3c2656bb4e1aaf3f6bddbe79b9d04362a3eb2c83cc5c56b0b4e

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
