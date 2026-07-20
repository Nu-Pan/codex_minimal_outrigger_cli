# `acp_builder`

## Summary
- 参照可能な正本ソース本文は含まれず、ACP 呼び出し設定に関する正本ソースの有無を確認する入口。配下には基礎パラメータ、indexing、oracle、realization、session、tui の各領域がある。

## Read this when
- ACP builder 配下に参照可能な正本ソースが存在するか確認するとき。
- ACP 呼び出し条件に関係する正本ソースの配置先を探索するとき。

## Do not read this when
- 具体的な実装仕様、処理内容、呼び出しパラメータの詳細を確認したいときは、該当する配下ファイルを直接読む。

## hash
- d843d19b5a1c530a25ce4e35a21d08ca3d1c09e1950652f806e61dbbcb0d9ae1

# `other`

## Summary
- cmoc の oracle 実装で使う設定・パスモデル・規範データ構造・構造化 Markdown 文書化を定義するファイル群。設定値やルート探索、規範文書の構造化、Markdown 変換を確認する入口。

## Read this when
- cmoc の設定項目、既定値、Codex CLI 設定、provider 設定、oracle review の上限を確認・変更するとき
- cmoc・repo・run・work のルート探索、パスプレースホルダ変換、git worktree 対応を確認するとき
- 規範文書のデータ構造、Requirement の制約、Standard の構造化文書変換を確認するとき
- StructDoc の Markdown レンダリング、見出し・入れ子・コードブロック・空行やインデントの処理を確認するとき

## Do not read this when
- CLI の設定読み書き、doctor による生成・同期、または設定利用側の個別機能を確認したいとき
- モデル分類や推論 effort の Enum 定義だけを確認したいとき
- 個別の標準文書の内容や、oracle file の配置・命名規則を確認したいとき
- CLI の実行経路やプロンプト生成全体、Markdown 以外の文書レンダリングを確認したいとき

## hash
- 4baf81dea861dbe6930a286191d9c7ebe2230b45fd29d2f63515f19e804ec50b

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
