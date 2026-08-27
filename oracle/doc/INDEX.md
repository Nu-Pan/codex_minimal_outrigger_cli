# `app_spec`

## Summary
- cmoc のアプリケーション仕様を機能領域ごとに参照するための入口。CLI 自動補完、Codex 実行、ログ、doctor 前処理、feedback、session／run、各サブコマンド、通知などの正本仕様を扱う。
- 共通仕様と個別仕様の責務境界、および実装・テスト・外部契約へ進むための参照先を示す。

## Read this when
- cmoc のアプリケーション挙動仕様を横断して、読むべき正本仕様の入口を探すとき。
- CLI 実行、ログ、feedback、session／run、サブコマンド、通知、INDEX.md 生成の仕様を確認するとき。

## Do not read this when
- 確認対象の機能に対応する個別仕様ファイルが明確な場合は、概観ではなくそのファイルを直接読むとき。
- 実装コード、テスト、開発環境、または仕様から委譲された外部契約の具体的内容を確認するとき。

## hash
- 804e9ed2e9eddb9b7b97982a55c50528bb3a4707b6ae9108af36c86a344cb051

# `branch_model.md`

## Summary
- cmoc が session と run を git branch・commit・worktree で隔離するモデルを定義する正本文書。各管理対象の命名、分岐元・統合先、run の差分検査に用いる commit、run 用 worktree の関係を確認する入口。

## Read this when
- session fork や run の branch 分岐・統合、run worktree の作成、または関連する commit 名・役割を実装・変更・調査するとき。
- cmoc 管理 branch と通常の local branch・remote-tracking branch の境界を確認するとき。

## Do not read this when
- branch model の具体的な CLI 入出力契約だけを確認する場合は、該当する CLI 仕様を直接読む。
- git 操作を伴わない workload の実行内容や report の詳細仕様だけを確認する場合は、各機能の仕様・実装文書を直接読む。

## hash
- c40f58b39046604d613c84f9bd18f7a9688be81e5c3b97293298f685511debdd

# `considered_alternative`

## Summary
- cmoc の設計・リファクタで採用しなかった作業方式や仕様案を記録する検討資料群。事前計画、並列所見管理、事後アクセス違反検査、`.gitignore` 連携、AI-generated memory などの不採用理由を確認するための入口であり、採用済みの現行仕様や具体的な実装手順の正本ではない。

## Read this when
- cmoc realization の作業フローや調査単位について、採用しなかった代替案とその理由を比較するとき
- AI による作業計画・memory の自動継承や、アクセス制御の事後検査、`.gitignore` 連携案の採否背景を調査するとき
- 現行設計が特定の代替方式を採用しなかった根拠を確認したいとき

## Do not read this when
- 現行のアクセス制御、refactor state、oracle、realization の仕様を確認・変更するとき
- 具体的な realization file の実装方法、CLI の挙動、テスト手順を調べるとき
- 採用済み workflow の操作方法や現在の実行結果だけを確認したいとき

## hash
- 2306639b6cb9d46169d1e0614cafd6a1ff50856b67ccfe5f40849ae09d0cd405

# `dev_rule`

## Summary
- Python 開発におけるコーディング規則、CLI の設計・配置方針、テスト要件、テスト実行手順を扱う開発ルール文書群。実装方法、責務境界、テスト設計、品質検査の実行手順へ進むための入口となる。

## Read this when
- Python コードの命名、型ヒント、import、docstring、コメント、ログなどの記述規則を確認するときは coding_rule.md を読む
- CLI のエントリーポイント、サブコマンド、共有処理の配置や責務分担を判断するときは design_rule.md を読む
- pytest による realization test の要件、隔離、Fake Codex CLI、実経路統合テストの成立条件を確認するときは test_rule.md を読む
- 構築済み環境での test・Ruff・mypy の選択、実行、結果判定、報告手順を確認するときは test_execution.md を読む
- Python 環境の構築、依存関係追加、pip 操作、実行環境の前提を確認するときは development_environment.md を読む

## Do not read this when
- CLI の具体的な挙動や出力内容そのものを確認するときは app_spec 配下の正本を直接読む
- テストの意味上の要件を確認するときに、単なる実行手順だけが必要なら test_execution.md ではなく test_rule.md を読む
- Python の環境構築や依存関係管理だけを確認するときは、他の開発ルール文書ではなく development_environment.md を直接読む
- 実装やテストの責務・配置を判断するときに、実行手順だけを定める test_execution.md を入口にしない

## hash
- b43db23d4f61803173a85c3cf48da31f2f9bb24f3503e0eb8295928bdd2436b0
