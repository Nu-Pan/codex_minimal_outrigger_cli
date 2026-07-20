# `acp_builder`

## Summary
- 参照可能な正本ソース本文は含まれず、ACP 呼び出し設定に関する正本ソースの有無を確認する入口。配下には基礎パラメータ、indexing、oracle、realization、session、tui の各領域がある。

## Read this when
- ACP builder 配下に参照可能な正本ソースが存在するか確認するとき。
- ACP 呼び出し条件に関係する正本ソースの配置先を探索するとき。

## Do not read this when
- 具体的な実装仕様、処理内容、呼び出しパラメータの詳細を確認したいときは、該当する配下ファイルを直接読む。

## hash
- 5fbad40cd6edff0c3061cdd487f2176f4df9ebcd969842441092f815ab441721

# `other`

## Summary
- oracle の設定・パスモデル・規範データ構造・構造化文書レンダリングを担う実装群をまとめたディレクトリ。cmoc の設定値、ルートパス解決、標準文書の構造化、Markdown 変換の実装へ進む入口となる。

## Read this when
- cmoc のリポジトリ固有設定や既定値、Codex・Ollama・oracle review の制御を調査するとき。
- プレースホルダを含むパス解決や cmoc・repo・run・work ルートの探索を調査するとき。
- 規範文書のデータ構造、構造化文書の Markdown レンダリング、cmoc_ref 検証を調査するとき。

## Do not read this when
- CLI 機能の具体的な実装や入出力処理だけを調査するとき。
- Codex CLI、Ollama、Markdown の一般的な利用方法を調査するとき。
- oracle review の所見生成・統合・検証ロジックなど、このディレクトリの定義を利用する個別機能だけを調査するとき。

## hash
- bf71c04445202355b44b4cd52767830fb91c56fccfda3589dd7767e5513bcc81

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
