# `doc`

## Summary
- cmoc の正本仕様を自然言語で定義する文書群。CLI 挙動、branch・session・run のモデル、Python 開発規則、不採用案の背景を扱い、実装・検証時の仕様上の入口となる。

## Read this when
- cmoc の挙動や状態モデル、開発・テスト規則などの正本仕様を確認するとき
- 実装やテストの変更前に、対象領域の意図と制約を確認するとき

## Do not read this when
- 具体的な実装やテストの詳細だけを確認したいとき
- 対象領域が特定できている場合に、配下の該当文書へ直接進めるとき
- INDEX の生成規則やリポジトリ固有の作業手順を確認したいとき

## hash
- 0c09d5249f809b8e2e6ff02813e68c0c885de6e89f875664679c0ac64f6f3c73

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
