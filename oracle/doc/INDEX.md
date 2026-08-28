# `app_spec`

## Summary
- cmoc のアプリケーション仕様を集約する正本文書群。CLI サブコマンド、agent call、feedback、session/run、ログ、通知、自動補完、インデクシングなど、利用者向け挙動と横断的な実行契約の確認先を提供する。
- 個別機能の仕様へ進むための上位入口であり、共通規約とサブコマンド固有仕様の担当範囲を整理している。

## Read this when
- cmoc の利用者向け挙動、CLI サブコマンド、workflow、agent call、feedback、session/run の正本仕様を探すとき
- 複数のアプリケーション仕様にまたがる実行境界、状態遷移、ログ、通知、自動補完、インデクシングの仕様入口を確認するとき

## Do not read this when
- 対象となる単一仕様の内容が明確な場合は、一覧から該当する個別仕様を直接読む
- 実装ファイル、テスト、または oracle file と realization file の分類規則だけを確認するときは、それぞれの対象ファイルや共通規約を直接読む

## hash
- bc02ae37e8ac2a42826d0f4fb76a62096f3c0459c6aeb3d24ed4f2338b087982

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
