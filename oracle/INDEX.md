# `doc`

## Summary
- cmoc の正本ドキュメントを機能領域ごとに整理したディレクトリ。アプリケーション仕様、branch・commit・worktree モデル、不採用案の検討記録、開発ルールへの入口を提供する。

## Read this when
- cmoc の正本仕様や開発ルールから、対象機能に対応する文書を探すとき
- CLI、session・run、branch・worktree、ログ、prompt、サブコマンド、INDEX.md 生成などの仕様を確認するとき
- realization refactor の設計判断や不採用案の背景を確認するとき
- Python 実装配置、開発環境、テスト方針などの開発ルールを確認するとき

## Do not read this when
- 構築済み環境での具体的なテスト、Ruff、mypy の実行手順だけを確認するときは repository local の run-cmoc-tests skill を読む
- 特定機能の実装詳細やテスト詳細だけを確認するときは対応する realization code または realization test を直接読む
- 正本仕様と無関係な一般的な CLI 入出力や実装上の細部だけを調査するとき

## hash
- 19aff3ccea76461b3677632278fa506f97282bf8eda6991cd8bcf20466093b0e

# `src`

## Summary
- AIエージェント呼び出し用パラメータの正本ソースを扱うディレクトリ。ACP設定、パスモデル、設定モデル、構造化Markdown、完全プロンプト、各種規範プロンプト、INDEX生成、oracle review、realization操作、session join、TUI起動の実装入口を含む。

## Read this when
- agent callのモデル・推論・ファイルアクセス設定やパラメータ構築を調査・変更するとき
- agent callのcwd、worktree、repo root、placeholderなどのパス解決を調査・変更するとき
- 完全プロンプト、エディタ初期文面、規範注入、StructDocのMarkdown化を調査・変更するとき
- INDEX生成、oracle review、realization適用・refactor、session join、TUI起動のprompt構築を調査・変更するとき

## Do not read this when
- realization側のCLI実装や実行フローだけを調査・変更するとき
- oracleドキュメント本文や個別規範の内容だけを確認するとき
- ACPのモデル・推論値そのものの利用箇所や、設定ファイルの生成・同期処理だけを調査するとき

## hash
- 15a2b0a78fabdb3e363407ec80b26fdbd569f82f65e894a4a1562dce8f875c23
