# `coding_rule.md`

## Summary
- Python 実装における基本的なコーディング規則を定める文書。PEP 8、命名・責務・入出力、最小限の変更、型ヒント、import、docstring、コメント、非公開識別子の扱いを確認するための入口。

## Read this when
- Python の実装・レビュー・リファクタリングで、命名や責務分割、型ヒント、import、docstring、コメント、識別子の公開範囲を確認するとき。
- cwd 識別子の命名規則や、日本語コメント・英語ログの方針を確認するとき。

## Do not read this when
- Python の実行環境や依存関係の手順を確認したいとき。
- 機能固有の設計・入出力仕様・テスト方法を確認したいとき。

## hash
- 47218a5c7bc19834ad43ff601a1fb8094ee2e2f16cb533ba64a536996089b771

# `design_rule.md`

## Summary
- cmoc の CLI 構成と共通モジュール配置の方針を定める。エントリーポイント、サブコマンド本体、`src/commons` に置く共有処理の境界を確認したいときに読む。

## Read this when
- `src/main.py` と各サブコマンド実装の責務分担を決めたいとき
- サブコマンド間で共有する処理をどこに置くか判断したいとき
- CLI の実装配置方針を確認したいとき

## Do not read this when
- Python の文法、型ヒント、docstring、コメントの書き方を確認したいときは `dev_rule/coding_rule.md` を読む
- テストの目的や配置方針を確認したいときは `dev_rule/test_rule.md` を読む
- CLI の挙動や出力内容そのものの正本仕様を確認したいときは `app_spec` 配下を読む

## hash
- e08b233e78e0aa9ec5de1cc287b99c15f953e430fe3626ef2f73f2f533df6c72

# `development_environment.md`

## Summary
- Python 環境の新規構築、依存関係の追加、pip 操作に必要な開発環境の正本仕様。WSL2・Python バージョン・venv・pip 実行方法、命名規則、エンコード、パッケージ追加手順を扱う。

## Read this when
- Python 仮想環境を新規作成するとき
- Python パッケージや依存関係を追加するとき
- pip を実行する方法や開発環境の前提を確認するとき

## Do not read this when
- 構築済み環境で既存テストや品質検査を選択・実行・報告するときは、repository local の run-cmoc-tests skill を直接読む
- 通常のテスト実行だけを行うとき

## hash
- 2dd1253da053a65bff5ebdc4ad5c019acb18aa34b0b10ada5b40a4f5a74db35f

# `test_rule.md`

## Summary
- cmoc の realization test における基本方針、検証対象、実経路統合テスト、test-local Ollama、GPU 実行、キャッシュ、クラウド backend、Fake Codex CLI の認可境界を定める正本仕様。テスト実装・実行方法を判断する際の入口。

## Read this when
- cmoc の realization test を追加・変更・レビューするとき
- 実経路統合テストの対象、Real Codex CLI、test-local Ollama、GPU marker、timeout、cache、sandbox escalation の要件を確認するとき
- full test や品質検査の対象範囲と未完了条件を確認するとき

## Do not read this when
- 実装配置や CLI の責務境界だけを判断する場合は design_rule.md を読む
- Python 環境や依存関係の構築だけを行う場合は development_environment.md を読む
- 具体的な pytest・Ruff・mypy の選択、実行、報告手順だけを確認する場合は repository local の run-cmoc-tests skill を読む

## hash
- 58f6d502e8b8d7c6c33cfad68839fd8482b6a066a4fe0ec7a3b9cb6456c4acd4
