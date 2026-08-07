# `doc`

## Summary
- cmoc の正本ドキュメントを集約するディレクトリ。アプリケーション横断仕様、branch・commit・worktree のモデル、開発規則、および採用しなかった設計案の検討記録を扱う。各サブディレクトリ・文書へ進むための仕様文書の入口となる。

## Read this when
- cmoc の正本仕様や開発規則の所在を横断的に確認したいとき
- アプリケーション仕様、branch model、Python 開発規則など複数領域にまたがる文書を探すとき
- 採用済み仕様と不採用案の検討記録を区別して参照したいとき

## Do not read this when
- 単一機能の正本仕様が明確で、該当する下位文書を直接確認できるとき
- 具体的な実装ファイルの配置やテスト実行など、ドキュメント一覧ではなく個別の開発規則を確認したいとき
- 既存仕様を変更せず、単に realization の実装・テスト内容だけを調査するとき

## hash
- 90385a00c562c9bf2be036aa22f0bb695707f20793c25895ddeb198611ebd994

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
