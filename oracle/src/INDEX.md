# `oracle`

## Summary
- 参照可能な正本ソース本文が存在しないディレクトリであり、正本ソースの有無を確認するための入口。
- oracle の設定・パスモデル・規範構造・Markdown 構造化文書を扱う実装群。cmoc 設定値やルートパス解決、Standard/Requirement の構造化、StructDoc による Markdown レンダリングを確認するための入口。
- cmoc のエージェントプロンプトを構成する実装群。プレースホルダ型、完全なプロンプトの組み立て、入力エディタの初期文面、oracle・realization やルーティング規則などのプロンプト部品を扱う。

## Read this when
- このディレクトリの内容や、参照可能な正本ソースの有無を確認するとき。
- cmoc の設定項目、Codex 実行設定、oracle review 上限を調べるとき。
- プレースホルダを含むルートパスの探索・解決や検証規則を調べるとき。
- Standard/Requirement のデータ構造や StructDoc への変換を調べるとき。
- 階層文書の Markdown レンダリング、見出し・コードブロック・空行・インデント処理を変更・確認するとき。
- エージェントプロンプト全体の構成や部品の有効化条件を確認・変更するとき。
- プロンプト部品、プレースホルダ、入力エディタの初期文面を確認・変更するとき。
- oracle・realization の定義、各種標準、ファイルアクセス規則、INDEX.md ルーティング規則の生成処理を確認するとき。

## Do not read this when
- 実装仕様や処理内容を確認したいとき。
- CLI コマンドの実行フローや設定ファイルの生成・同期処理だけを調べるとき。
- ModelClass、ReasoningEffort、StructDoc の個別定義元だけを直接調べるとき。
- 個別の規範本文や、Markdown レンダリングを経由しない別機能の仕様を確認するとき。
- 個別のプロンプト部品の文面や責務だけを確認したいとき。
- 個別の oracle file や realization file の仕様・実装を調査するとき。
- Codex CLI の実行環境や sandbox 設定そのものを確認するとき。

## hash
- 8e245a0ca078ff30a4cbeff757b70040de1227b4b10747a6c0c626214f44af48
