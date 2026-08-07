# `doc`

## Summary
- cmoc の正本ドキュメントをまとめたディレクトリ。アプリケーション仕様、branch・commit・worktree のモデル、採用しなかった設計案、Python 開発規則など、仕様・設計判断・開発手順の各領域へ進むための入口となる。

## Read this when
- cmoc の正本ドキュメントから、対象領域に対応する仕様・設計・開発規則を探すとき
- アプリケーション仕様、branch model、検討済み代替案、Python 開発規則など複数領域の構成を把握するとき
- 対象となる個別文書がまだ特定できず、正本ドキュメント全体の入口を確認したいとき

## Do not read this when
- 対象となる個別仕様・設計文書が既に分かっており、その本文を直接確認できるとき
- 具体的な実装配置や個別テストの実行手順など、より直接対応する文書だけを確認すればよいとき
- 採用しなかった設計案の背景ではなく、現行仕様や実装の具体的内容だけを調査するとき

## hash
- d8b31fa3af1ab18cf354b561cb56b5f1f3c79055fbca3e544b0f705e4f3e1aec

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
