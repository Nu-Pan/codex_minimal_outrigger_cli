# `app_spec`

## Summary
- cmoc のアプリケーション仕様を、CLI 自動補完、Codex 実行、ログ、doctor 前処理、feedback、session／run、各種サブコマンドなどの個別仕様へ案内する正本文書群。機能の挙動・責務境界・状態遷移を確認する際の入口となる。

## Read this when
- cmoc のアプリケーション挙動に関する正本仕様を探すとき
- CLI、feedback、session／run、TUI、ログ、通知、agent call など特定機能の仕様を実装・変更・レビューするとき
- 個別仕様間の責務分担や、より詳細な正本文書への入口を確認するとき

## Do not read this when
- 実装コードやテストの具体的な挙動だけを確認したいときは、対象の realization file を直接読む
- INDEX.md の生成・更新規則だけを確認したいときは、indexing の仕様を直接読む
- 個別仕様の詳細が特定できている場合は、この仕様群の概要ではなく該当する正本文書を直接読む

## hash
- e1cbd03a987eadb63244b0b2c15e8267edaeef1e5369d4be3f702984c6ebcf3c

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
- cmoc の開発ルール文書群への入口。Python の書き方、CLI の責務配置、開発環境、テスト要件、テスト実行手順を、それぞれの正本文書へ振り分けて確認できる。
- 実装・環境構築・テストに関する判断で、コーディング規則、CLI 構成、依存関係、テストの意味要件、または検査実行手順のどれを確認すべきかを選ぶための案内を担う。

## Read this when
- Python 実装の命名、型ヒント、import、docstring、コメント、ログなどの記述規則を確認するとき
- CLI のエントリーポイント、サブコマンド、共有処理の配置と責務境界を判断するとき
- Python 仮想環境、依存関係、pip 操作、実行環境の前提を確認するとき
- テストの検証要件、隔離、Fake Codex CLI、実経路統合テストの条件を確認するとき
- 構築済み環境で focused test、品質検査、通常の pytest、実経路統合テストを選択・実行・判定するとき

## Do not read this when
- 特定機能の挙動や出力など、アプリケーション仕様そのものを確認したいとき
- 実装やテストの責務・配置を個別に判断するときは、対応する正本文書を直接確認するとき
- テストの意味上の要件を確認するときは test_rule.md を直接読むとき
- Python 環境の新規構築、依存関係の追加、pip 操作を確認するときは development_environment.md を直接読むとき
- 単に実装上の問題や期待値の意味を調査し、文書の実行手順を必要としないとき

## hash
- a9eb031831fbfcc2aae337585c7e2af5d64d5a4aa2137ecc1f49137f43e2175d
