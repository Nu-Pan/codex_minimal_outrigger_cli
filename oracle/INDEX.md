# `doc`

## Summary
- cmoc のアプリケーション仕様、branch・commit・worktree のモデル、不採用案、Python 開発規則を分野別に収める正本文書群。アプリケーション挙動や開発・テスト方針を確認する際の入口となる。

## Read this when
- cmoc のアプリケーション仕様を調査し、対象となる個別仕様文書を選ぶとき
- branch・session・run・worktree の関係やライフサイクルを確認するとき
- Python の実装、CLI 設計、開発環境、テスト規則・実行手順を確認するとき
- 採用されなかった refactor の作業方式や検査方式の設計理由を調べるとき

## Do not read this when
- 対象の個別仕様文書がすでに特定でき、その本文を直接読むべきとき
- 実装配置、テスト実行手順、開発環境など、対象文書が明確なアプリケーション仕様以外の事項を直接確認するとき
- 現行実装の詳細や具体的なテスト内容だけを確認したいとき

## hash
- 8363ba78bb8990c78d226077232e8a198b51602418f0eeb1f455085169542272

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
