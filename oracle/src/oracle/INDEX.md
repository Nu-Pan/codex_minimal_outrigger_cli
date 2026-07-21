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
- cmoc のエージェントプロンプトを構成する実装群。プレースホルダ型、完全なプロンプトの組み立て、oracle／realization や各種標準・ファイルアクセス・INDEX.md ルーティング規則などのプロンプト部品を扱う。配下の個別モジュールや標準規範を調査するための入口。

## Read this when
- cmoc のプロンプト生成基盤全体の責務や構成を確認したいとき。
- 配下のプレースホルダ定義、完全なプロンプトビルダー、プロンプト部品群のどれを読むべきか判断したいとき。

## Do not read this when
- 個別のプロンプト部品の文面や責務だけを調べたいときは、配下の parts など対応する実装を直接読む。
- cmoc の CLI 処理、実際の oracle／realization file の仕様、または INDEX.md の実際の内容を調査するとき。

## hash
- 14e39f520a308e63ffb008162205f5db8df9bcbe5bbcc827dcaf6488d97bc99e
