# `acp_builder`

## Summary
- cmoc の各サブコマンド向け ACP エージェント呼び出しパラメータを構築する oracle src のディレクトリ。apply fork、oracle、session、tui、indexing などの prompt、Structured Output schema、モデル・推論・アクセス設定を扱う下位領域への入口。

## Read this when
- cmoc のサブコマンドがエージェントへ渡す AgentCallParameter、prompt、Structured Output schema、モデル・推論強度、ファイルアクセス設定を調査・変更するとき。
- 特定サブコマンドの agent call 構成を確認し、対応する下位ディレクトリを選ぶとき。

## Do not read this when
- ACP パラメータの共通型や既定値だけを確認するときは、basic.py を直接読む。
- agent call の実行本体、TUI 画面処理、差分適用や conflict 解消などの後段処理を調査するとき。
- 特定サブコマンドの実装や schema だけを確認でき、ディレクトリ全体の構成を知る必要がないとき。

## hash
- 2eac1a91a98e1c1fcf11063eb4d67262cc8f8e33b8bfb3cd64b2e33c4ed29650

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
