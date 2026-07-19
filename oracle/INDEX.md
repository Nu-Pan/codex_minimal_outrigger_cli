# `doc`

## Summary
- cmoc のアプリケーション仕様を収録するディレクトリ。CLI 補完、ログ、エラー処理、プロンプト、managed ollama、session/run、branch・commit・worktree、サブコマンドなど、利用者向け挙動と主要 workflow の正本仕様への入口。
- 現行仕様そのものに加え、branch model や realization refactor に関する不採用案、開発規則への導線も含む。

## Read this when
- cmoc の利用者向け挙動、CLI 実行条件、出力・ログ、状態管理、プロンプト、サービス管理、session/run、branch・worktree、サブコマンドの正本仕様の所在を確認するとき。
- 複数のアプリケーション仕様にまたがる workflow や、読むべき個別仕様・開発規則の入口を判断するとき。
- realization refactor の作業方式や検査方式について、採用・不採用の理由を確認するとき。

## Do not read this when
- 具体的な機能の詳細仕様が特定できる場合は、このディレクトリ全体ではなく対応する個別仕様ファイルを直接読む。
- 開発環境、設計・テスト規則、oracle/realization の共通定義、または具体的な実装詳細だけを確認するときは、対応する専用文書や実装本文を直接読む。
- 現在の realization refactor state や agent 呼び出し経路など、現行の refactor 運用仕様だけを確認するときは、不採用案の記録ではなく現行仕様の直接の参照先を読む。

## hash
- 5534e702758742152e7d16a0938e43b1a4a3907273b4cd7105d4ad7c69b0acd1

# `src`

## Summary
- `oracle/src` は、cmoc の正本ソースを集約する入口です。
- `oracle/acp_builder` は、各種 agent call・TUI・レビュー・fork 用パラメータと Structured Output schema を扱います。
- `oracle/other` は、設定、パス解決、規範データ構造、構造化 Markdown の基盤を扱います。
- `oracle/prompt_builder` は、完全なプロンプト構築と、アクセス規則・標準規則・ルーティング規則などの注入部品を扱います。

## Read this when
- cmoc の正本実装や Structured Output schema の定義箇所を特定するとき。
- agent call、TUI、oracle review、realization の fork 処理に対応する正本ソースを調査するとき。
- 設定値、パスモデル、構造化文書、完全なプロンプト生成や注入規則を調査するとき。

## Do not read this when
- CLI の具体的な実行経路や入出力処理だけを調査するとき。
- oracle/doc の自然言語仕様、oracle/test のテスト、または realization 側の実装を直接調査するとき。
- 個別のプロンプト本文や標準規則の内容だけを確認する場合は、該当する下位ディレクトリを直接読むとき。

## hash
- bb980daff461288cf45247499c8374d1f8e35bce6358b4d3364fef7c2ff48e52
