# `doc`

## Summary
- cmoc のアプリケーション仕様を扱う oracle doc ディレクトリ。CLI 自動補完、Codex CLI 呼び出し、ログ、doctor preprocess、プロンプト、run・session lifecycle、サブコマンド、INDEX 更新など、個別仕様文書を探す入口を提供する。
- branch・commit・worktree の用語や関係を確認する場合は branch_model.md、採用しなかった realization refactor 方式の理由を確認する場合は considered_alternative、Python 実装・CLI 配置・開発環境・テスト規則を確認する場合は dev_rule へ進む。

## Read this when
- cmoc のアプリケーション仕様を確認・変更・レビューするとき
- CLI 起動、Codex agent call、ログ、プロンプト、run・session、サブコマンド、INDEX 更新の仕様上の入口を探すとき
- 複数の個別仕様にまたがる共通ルールや、参照すべき正本仕様文書を切り分けるとき

## Do not read this when
- 具体的な realization implementation や realization test の実装詳細だけを確認するとき
- アプリケーション仕様と無関係な開発環境・設計・テスト実行規則を確認するとき
- 特定の仕様文書の内容が明らかで、対象文書へ直接進めるとき

## hash
- 89c115638adcbce95e2bcb0fe535ceba09f17decc5fd93872a46cc7cd9e7e088

# `src`

## Summary
- `oracle` 配下の実装・設定を機能別に整理する下位領域。ACP agent call 設定、共通設定・パス・構造化文書処理、prompt builder 部品などの oracle source へ進む入口。

## Read this when
- ACP agent call の共通設定、prompt、Structured Output schema の oracle source を調査・変更するとき。
- cmoc 固有設定、パス解決、規範構造、StructDoc の生成や Markdown レンダリングに関わる oracle source を調査するとき。
- oracle／realization 規則、ファイルアクセス制約、INDEX.md ルーティング規則などの prompt builder 部品を調査・変更するとき。

## Do not read this when
- CLI コマンドの通常処理、TUI の画面表示、Python 実行環境やテスト実行方法を直接確認したいとき。
- 個別の oracle 文書、realization 実装・テスト、または特定機能の詳細だけを確認したいときは、対応する下位ディレクトリやファイルを直接読む。

## hash
- 0b1f6a71dfdc061b873c325879744f2d16af026c4f5818fb58e357af9c6ed2a6
