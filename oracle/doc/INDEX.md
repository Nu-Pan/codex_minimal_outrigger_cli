# `app_spec`

## Summary
- cmoc のアプリケーション仕様を集約するディレクトリ。CLI 自動補完、Codex 呼び出し、ログ・エラー処理、feedback、状態管理、run/session、通知、サブコマンドなどの正本仕様への入口を提供する。各機能の実装・変更・レビュー時に、該当する下位仕様へ進むために読む。

## Read this when
- cmoc のアプリケーションレベルの挙動仕様、共通契約、サブコマンド仕様、状態管理、agent call、feedback、通知、INDEX.md 運用の参照先を選ぶとき
- 複数のアプリケーション仕様にまたがる責務境界や、目的に応じた個別仕様への導線を確認するとき

## Do not read this when
- 特定の機能やサブコマンドが明確で、その個別仕様を直接確認できるとき
- 実装コード、テスト、prompt builder、JSON schema、外部契約など、下位の指定対象が直接の確認先となるとき
- INDEX.md の既存内容や、アプリケーション仕様と無関係な機能を扱うとき

## hash
- af2ef4e8ea6bf859481597da3638a05cd41188791afa17cec08c2ec6de39351c

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
- cmoc の開発規則をまとめたディレクトリ。Python のコーディング方針、CLI の実装配置、開発環境・依存関係、テスト要件、テスト実行と品質検査の入口を提供する。各文書は責務ごとに分かれており、該当する作業の正本文書へ進むために読む。

## Read this when
- cmoc の Python 実装方針、CLI の責務分担、開発環境、テスト要件、またはテスト・品質検査の実行手順を確認するとき
- 新規実装、実装配置の判断、環境構築、テストの追加・変更・レビュー、既存テストや静的検査の実行に着手するとき

## Do not read this when
- 特定機能の CLI 挙動や出力内容そのものを確認するときは、app_spec 配下の正本仕様を直接読む
- 構築済み環境でのテスト実行手順だけを確認するときは test_execution.md を直接読む
- realization test の意味上の要件だけを確認するときは test_rule.md を直接読む
- Python 環境の新規構築や依存関係・pip 操作だけを確認するときは development_environment.md を直接読む
- Python の文法、型ヒント、docstring、コメントの書き方だけを確認するときは coding_rule.md を直接読む

## hash
- c67db3ef9416fabd5ce8a2540116b72505309c043d99984b2e8d2e20f4e087eb
