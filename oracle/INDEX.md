# `doc`

## Summary
- cmoc の正本文書を、アプリケーション仕様と開発ルールの領域に分けて案内する文書群。CLI、Codex 呼び出し、prompt、logging、feedback、session/run、branch/worktree などの挙動仕様と、Python 実装・環境・テスト・品質検査の開発規則への入口を提供する。採用しなかった設計案の検討記録も含む。

## Read this when
- cmoc の正本仕様や開発ルールの入口を探すとき
- CLI、Codex 呼び出し、prompt、Structured Output、logging、feedback、session/run、branch/worktree の挙動を確認・変更・レビューするとき
- Python 実装、開発環境、テスト要件、テスト実行手順の根拠を確認するとき
- 現行仕様ではなく、採用されなかった設計案の理由や検討背景を調べるとき

## Do not read this when
- 対象となる個別の仕様書、実装、テスト、または開発手順が既に特定できているとき
- 具体的な実装コードや realization test の挙動だけを調査するとき
- INDEX.md の生成規則や、対象文書に直接記載された詳細手順だけを確認するとき

## hash
- 592a46e3d8a72af33be72a583c2e9e6a4ec3bc1a6f2e9b2306e16533b34af4a8

# `src`

## Summary
- cmoc の oracle 実装における共通モデル、設定・パス解決、agent 向け標準定義、構造化 Markdown 文書生成を扱う下位要素への入口。oracle 側の共通定義や文書表現を調査・変更する際に、該当する下位要素へ進むために読む。

## Read this when
- oracle 共通モデル、設定、パスコンテキスト、標準定義、または構造化文書生成の実装を調査・変更するとき
- 複数の oracle 関連モジュールにまたがる責務の入口を確認し、該当する下位要素へ進むとき

## Do not read this when
- agent call の prompt、Structured Output、起動条件、実行権限の定義を調査するとき
- 特定の CLI サブコマンド、feedback、realization、session、TUI の業務ロジックを調査するとき
- 生成済み prompt の構成や prompt 部品の組み合わせを調査するとき

## hash
- c6e16de93db2b1703cdc0f6464adab7ddf2f3b7ac57489f1756a4b4c885e94d9
