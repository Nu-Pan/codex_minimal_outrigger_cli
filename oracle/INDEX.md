# `doc`

## Summary
- cmoc の正本文書群を、アプリケーション仕様、branch・commit・worktree モデル、不採用案、Python 開発規約に分類して案内するディレクトリ。各下位文書へ進むための意味上の入口を提供する。

## Read this when
- cmoc の正本仕様・設計資料・開発規約の所在を確認し、適切な下位文書を選ぶとき
- アプリケーション仕様、branch/worktree、検討済み代替案、Python 実装・テスト規約のいずれかを調査するとき

## Do not read this when
- 特定の仕様・設計・環境・テスト手順を直接確認できる下位文書が明確なとき
- 実装ファイル、テストファイル、prompt literal、Structured Output schema の内容だけを確認したいとき
- INDEX.md の構成や、アプリケーション仕様と無関係な一般作業だけを扱うとき

## hash
- 1a9e9a74886147bd387127492bacbdc06ce25bf9f218c5dabde00626d95c02d7

# `src`

## Summary
- oracle/src は、oracle・realization を扱う agent call の共通モデル、prompt 構築、設定・パス・構造化文書処理、および各種サブコマンド向け起動パラメータをまとめる実装領域です。
- agent call の論理モデル、モデル種別、推論強度、ファイルアクセスモードを確認するときは `acp_builder` へ進みます。
- 完全 prompt、入力用 editor 文面、oracle・realization の規定、feedback・routing・conflict resolution などの prompt 部品を確認するときは `prompt_builder` へ進みます。
- パス解決、cmoc 設定、構造化ドキュメントの表現と Markdown レンダリングを確認するときは `other` へ進みます。
- feedback issue の報告データ形式を確認するときは `feedback` へ進みます。

## Read this when
- oracle または realization に関する agent call の共通処理や、prompt・起動パラメータの実装入口を探すとき。
- oracle、realization、feedback、indexing、session、TUI などの下位機能がどの領域に配置されているか判断するとき。
- agent call の設定、パス境界、構造化文書、prompt policy の関係を横断して確認するとき。

## Do not read this when
- 特定の oracle、realization、feedback、indexing、session、TUI 機能の詳細だけを調べる場合は、`acp_builder` 配下の対応する下位領域へ直接進むとき。
- prompt の個別 policy や部品だけを確認する場合は、`prompt_builder` 配下の対応する下位領域へ直接進むとき。
- パス・設定・構造化文書の個別処理だけを確認する場合は、`other` の対象へ直接進むとき。
- Codex CLI の実行処理や、oracle doc・realization 実装など `oracle/src` 外の正本・実装を確認するとき。

## hash
- 5dcd9aaf1cdb69a5046db391e19c6f789ec4904c7337bce1fa952edac4b7c8e6
