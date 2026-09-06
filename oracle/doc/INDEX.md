# `app_spec`

## Summary
- cmoc の実行・設定・状態管理・ログ・feedback・通知・編集 run など、アプリケーション共通の正本仕様を横断して案内する仕様群の入口。
- サブコマンドやワークロード固有の契約から、Codex 呼び出し、前処理、エラー処理、indexing、session、oracle/realization 管理などの個別仕様へ進むための上位ルーティングを提供する。

## Read this when
- cmoc のアプリケーション全体に関わる正本仕様の所在を確認するとき
- サブコマンド、編集 run、feedback、Codex agent call、ログ、通知、状態管理など複数領域にまたがる仕様の参照先を選ぶとき
- 共通仕様と個別サブコマンド仕様の責務境界を確認するとき

## Do not read this when
- 単一ファイルの具体的な実装、prompt、schema、provider 設定、feedback 観測、または個別サブコマンドの詳細だけを確認したいとき
- 対象の仕様ファイルが既に特定できており、その本文を直接読む方が適切なとき
- oracle/realization ファイルの列挙や実装コードの内部構造だけを調べるとき

## hash
- 813c5fd1a5c266ad7e1644f37baccc8a76b65b67570baa2fdd6bac27f933b1dc

# `branch_model.md`

## Summary
- cmoc における session・run の branch、commit、worktree の役割と関係を定義する正本文書。
- branch の作成元・命名・統合先、commit の fork/join、run worktree の分離条件を確認する入口。

## Read this when
- session fork、run の開始・分離・join、apply の追従対象、run report の commit 基準を扱うとき。
- cmoc 管理 branch と通常の git branch、session home branch の意味を区別する必要があるとき。
- branch・commit・linked worktree の用語や対応関係を確認するとき。

## Do not read this when
- run state や report の状態遷移そのものを確認したいとき。
- oracle の変更手順や設計責務、test の実行規則を直接確認したいとき。
- 個別の git 操作手順だけを知りたいときで、branch model の用語上の判断を必要としない場合。

## hash
- 955dd077586a6c946e3573d1b1bbde073736e4f7325fbd93ed6c09a3862fc858

# `considered_alternative`

## Summary
- realization refactor、file access policy、AI-generated memory、oracle review、作業計画レビューなど、採用しなかった設計案とその理由を記録した検討資料群への入口。現行仕様ではなく、設計判断の背景や代替案の評価を確認するための対象。

## Read this when
- realization refactorの作業フロー、file access policyの事後検査、.gitignore連携、AI-generated kaizenの自動注入、oracle review、作業計画レビューなどの不採用理由や設計背景を調べるとき。

## Do not read this when
- 現行の正本仕様、具体的な実装、状態管理、アクセス制限、feedback処理、oracleやrealizationの個別内容を確認するとき。

## hash
- 06605a888f8a7f27a0c29a55cfa6d58e8128f3a61b16c54d5ba991b81213eb2c

# `dev_rule`

## Summary
- cmoc の Python 開発環境、コーディング、CLI 設計、テスト要件・実行手順を定める開発ルール群への入口。
- Python 実装規約、CLI の責務分担、環境構築、テスト設計、テスト・品質検査の実行方法を、目的別の下位文書へ案内する。

## Read this when
- cmoc の Python 実装・CLI 設計・開発環境・テストについて、どの正本規則を確認すべきか判断するとき。
- 複数の開発ルール領域にまたがる変更や調査で、適切な下位規則への入口を探すとき。

## Do not read this when
- 特定の Python コーディング規則、CLI 設計規則、開発環境、テスト要件、またはテスト実行手順が明確な場合は、該当する下位文書を直接読む。
- 実装対象の個別コードや、LLM・Codex CLI・model provider 自体の一般的な正しさだけを確認するとき。

## hash
- 0bfd3e30d446406ae5c3a3c2e06c9c65505d36888b4747ddaa79dde16d2cd762
