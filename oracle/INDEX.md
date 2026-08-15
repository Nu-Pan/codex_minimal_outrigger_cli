# `doc`

## Summary
- app_spec は cmoc の CLI・workflow・agent call・feedback・出力・状態管理に関する正本仕様の入口で、複数仕様にまたがる責務境界や下位仕様の選択を確認する。branch_model.md は session fork、run 隔離、branch・commit・worktree の関係やライフサイクルを確認する正本仕様である。considered_alternative は realization refactor で不採用となった作業・検査・状態管理方式の理由を確認する記録であり、現行仕様や実装の直接の参照先ではない。dev_rule は Python 実装、CLI 配置、開発環境、テスト要件、テスト実行・品質検査の正本文書群への入口である。

## Read this when
- cmoc の CLI、workflow、agent call、feedback、ログ・report、エラー・中断、通知、run/session state の正本仕様や、複数仕様間の責務境界を確認するときは app_spec を読む。
- session fork、run の隔離、branch・commit・worktree の用語・命名・ライフサイクル、run report や apply の基準 commit を確認するときは branch_model.md を読む。
- realization refactor で採用しなかった作業フロー、調査・検査方式、状態管理、gitignore 連携、AI-generated memory の背景を確認するときは considered_alternative を読む。
- Python 実装、CLI の責務配置、Python 環境や依存関係、realization test の要件、既存テスト・品質検査の実行手順を確認するときは dev_rule を読む。

## Do not read this when
- 特定のアプリケーション仕様の本文が明確な場合は app_spec ではなく、その個別仕様を直接読む。
- branch や worktree の用語・ライフサイクルが関係しない特定 CLI 実装の調査では branch_model.md を読まない。
- 現行の realization refactor state、具体的な実装・テスト内容、INDEX、oracle、ログ、実行成果物の形式を確認する場合は considered_alternative を読まない。
- テストの意味要件だけ、テスト実行手順だけ、または CLI の挙動・出力そのものだけを確認する場合は dev_rule ではなく、それぞれの直接の正本文書を読む。

## hash
- ed3ca68f46d0fe38b3f312c5637cdc7eaf29ea7fc20e05eeec47ba06d32dbb52

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
