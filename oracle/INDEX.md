# `doc`

## Summary
- cmoc の正本ドキュメントを分野別に整理するディレクトリ。アプリケーション仕様、branch・commit・worktree モデル、不採用案の検討記録、Python 開発規約への入口を提供する。各下位ディレクトリの仕様群へ進むためのルート。

## Read this when
- cmoc の正本仕様・設計規約を探しており、対象分野が app_spec、branch model、considered alternative、または dev_rule のいずれかに該当するとき
- 複数分野にまたがる仕様の入口や、目的に応じた下位ドキュメントの選択先を確認するとき

## Do not read this when
- 特定の仕様本文が明確な場合は、該当する下位ディレクトリまたは文書へ直接進むとき
- 実装コード、テストコード、実装詳細、または実行成果物を確認するとき

## hash
- ff0923cf8f6ef617fb53fa66fcb593794c9808033eb0f0670f899cbd746735ec

# `src`

## Summary
- oracle/src is the source-code portion of the repository’s authoritative oracle tree. It contains executable/configuration definitions that drive cmoc Agent-call behavior, including shared call parameters, purpose-specific prompts or launch settings, and Structured Output schemas; use it as the implementation-level entry point before descending into a narrower subdirectory.

## Read this when
- 調査・変更対象が cmoc Agent call の共通設定、用途別 prompt／起動設定、モデル・推論設定、権限・作業ディレクトリ、実行前設定、または Structured Output schema の実装定義であるとき。
- oracle/src 配下の特定の用途や設定領域への入口を探すとき。

## Do not read this when
- 通常の realization 実装・テスト、または CLI／TUI の実行フローそのものを調査するとき。
- 正本仕様ドキュメント、sandbox・permission profile、共通 prompt 構築の詳細だけを調査するときは、それぞれの oracle/doc 配下の直接の対象を読むとき。
- 特定用途の prompt や schema の詳細だけを確認したいときは、oracle/src 全体ではなく該当する下位ディレクトリやファイルを直接読むとき。

## hash
- acbe7573c2a82b1699975f51a13fe95ea80c972aed3694e02172ca992b55c20d
