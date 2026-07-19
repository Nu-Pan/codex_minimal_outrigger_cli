# `acp_builder`

## Summary
- 参照可能な正本ソース本文を含まない空の入口ディレクトリです。正本ソースの有無を確認するために使用します。

## Read this when
- このディレクトリに参照可能な正本ソースが存在するか確認するとき。

## Do not read this when
- 実装仕様や処理内容を確認したいとき。

## hash
- af14647647bde4a7fcfb3715b7c95ff89038f5004f0e89357b460a53dd25ba64

# `other`

## Summary
- cmoc の設定、ルートパスモデル、規範データ構造、構造化文書の Markdown 変換を担う基盤モジュール群。設定・パス解決・標準文書モデル・文書レンダリングの各実装を調べる入口。

## Read this when
- cmoc の設定 dataclass、ルートパスプレースホルダ、規範文書モデル、StructDoc の Markdown 出力を変更または調査するとき。
- 設定永続化対象やルート探索規則、標準文書の構造、見出し・コードブロック・cmoc_ref の扱いを確認するとき。

## Do not read this when
- 設定ファイルの生成・同期手順や doctor の処理を調べるとき。
- ModelClass、ReasoningEffort、StructDoc の利用側、CLI 実行経路、oracle file の配置・命名方針、個別の標準文書内容を確認するときは、それぞれの定義元・呼び出し元・標準文書を直接読む。

## hash
- 0b174c0c78c774c9a947eba32eee441d0cacd7ae4f8e3393c8f850b1695a6f88

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
