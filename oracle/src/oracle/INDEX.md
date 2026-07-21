# `acp_builder`

## Summary
- 参照可能な正本ソースが存在するかを確認するための入口です。実装仕様や具体的な処理内容は扱いません。

## Read this when
- このディレクトリ内の内容や、参照可能な正本ソースの有無を確認するとき。

## Do not read this when
- 実装仕様や具体的な処理内容を確認したいとき。

## hash
- 8222010c681083a028be75dd5758c6b070ce6cb2abaaa642caebe374cdb3dfc5

# `other`

## Summary
- oracle の設定・パスモデル・規範構造・Markdown 構造化文書を扱う実装群。cmoc 設定値やルートパス解決、Standard/Requirement の構造化、StructDoc による Markdown レンダリングを確認するための入口。

## Read this when
- cmoc の設定項目、Codex 実行設定、oracle review 上限を調べるとき
- プレースホルダを含むルートパスの探索・解決や検証規則を調べるとき
- Standard/Requirement のデータ構造や StructDoc への変換を調べるとき
- 階層文書の Markdown レンダリング、見出し・コードブロック・空行・インデント処理を変更・確認するとき

## Do not read this when
- CLI コマンドの実行フローや設定ファイルの生成・同期処理だけを調べるとき
- ModelClass、ReasoningEffort、StructDoc の個別定義元だけを直接調べるとき
- 個別の規範本文や、Markdown レンダリングを経由しない別機能の仕様を確認するとき

## hash
- 96d9af87bdc3ebc13337ecdac9dff551adb5b72ad9adf6622d22910a3dea2e84

# `prompt_builder`

## Summary
- cmoc のエージェントプロンプトを構成するビルダーと部品群を収めるディレクトリ。プレースホルダ表現の型定義、完全なプロンプトの組み立て、oracle・realization 標準やファイルアクセス・ルーティング規則などのプロンプト部品を扱う。

## Read this when
- エージェントプロンプト全体の構成や部品の有効化条件を確認・変更するとき。
- プレースホルダ展開の型や、文字列・Path を統一して扱う方法を確認するとき。
- oracle・realization の標準、ファイルアクセス制限、INDEX.md ルーティング規則の生成内容を調査するとき。

## Do not read this when
- 個別のプロンプト部品の文面や責務だけを確認したいときは、対応する parts 配下を直接読む。
- プロンプト組み立てと無関係な個別 oracle file・realization file の仕様や実装を調査するとき。
- Codex CLI の実行環境や sandbox 設定そのものを確認するとき。

## hash
- a133bb8e9afc0c123acd7cac6633ca31d9208aac1c83506961e8d3870fc4036c
