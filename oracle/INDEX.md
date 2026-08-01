# `doc`

## Summary
- cmoc のアプリケーション仕様を扱う正本文書群。branch・commit・worktree、採用しなかった設計案、Python 開発規則など、複数の個別仕様・開発ルールへの入口を提供する。

## Read this when
- cmoc の利用者向け挙動、状態管理、CLI、agent call、run/session lifecycle などの正本仕様を探すとき
- branch model や realization refactor の設計背景を確認するとき
- Python 実装、CLI 配置、開発環境、realization test の規則を確認するとき
- 複数の仕様領域にまたがる変更で、参照すべき個別文書を切り分けるとき

## Do not read this when
- 特定の個別仕様や realization 実装・テストの内容が明確で、その本文を直接読めば足りるとき
- oracle と realization の一般定義や共通原則だけを確認したいとき
- INDEX.md のルーティング方針自体を確認したいとき

## hash
- e533ac35305334fcef66883cec0e5c1630887e2985b37dada2afc6153ead3001

# `src`

## Summary
- cmoc の正本ソース実装を集約するディレクトリ。設定モデル、ルートパス解決、Standard/Requirement と StructDoc の変換・Markdown レンダリング、エージェントプロンプトの構成部品、ACP 用パラメータ生成、oracle review・realization・INDEX 生成に関する処理を扱う。各機能の実装やパラメータ定義へ進む入口。

## Read this when
- cmoc の設定値、モデル指定、ファイルアクセスモード、oracle review 設定を確認するとき
- cmoc・リポジトリ・実行・作業ルートの解決やプレースホルダ変換を確認するとき
- Standard/Requirement の構造や StructDoc の Markdown レンダリングを確認するとき
- 完全なエージェントプロンプト、プロンプト部品、初期入力文面の構成を確認するとき
- ACP セッション結合、TUI、oracle review、realization refactor/apply、INDEX エントリー生成のパラメータを確認するとき

## Do not read this when
- CLI の実行フローや設定ファイルの生成・同期処理だけを調べるとき
- 特定のプロンプト部品、review 処理、パラメータ生成処理の詳細だけを確認したいとき
- Codex CLI の実行環境や sandbox 設定そのものを調べるとき
- 個別の oracle file・realization file の仕様や実装だけを調査するとき

## hash
- 3cfc371675e494e9d74a32d23858c9c7c930ce1a1c07f05ea76dca3a1292df50
