# `coding_rule.md`

## Summary
- Python 実装の基本的なコーディング方針と、識別子・型ヒント・import・docstring・コメント・ログ・非公開識別子に関する規則を定める文書。実装時に、同階層の個別仕様ではなく、コードの書き方や命名・記述上の制約を確認する入口となる。

## Read this when
- Python コードの新規作成、変更、レビューで、PEP 8、最小限の実装、命名、責務、入出力の方針を確認するとき
- cwd を表す内部識別子の命名を決めるとき
- 型ヒント、Any の使用、from __future__ import annotations の禁止、相対 import、循環参照回避の規則を確認するとき
- docstring、コメント、ログメッセージ、非公開識別子の記述規則を確認するとき

## Do not read this when
- Python 環境の構築、依存関係、pip 操作の規則を確認するとき
- テストの追加・変更・実行に関する規則を確認するとき
- 特定機能の仕様や設計上の責務を確認するとき

## hash
- 9bb6dd90d176d700d0a9ffc4bf1035577cd851337142043de5a097ed48adaf99

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
- Python 開発環境の構築条件、依存関係追加、pip 操作の手順を定める正本文書。Python・仮想環境・エンコード・命名規則に関する前提を扱い、開発環境操作の入口となる。

## Read this when
- Python 仮想環境を新規作成するとき
- 依存関係を追加・インストールするとき
- pip を操作するとき
- Python 実行環境、ファイルエンコード、命名規則の前提を確認するとき

## Do not read this when
- 構築済み環境で既存 test や品質検査を実行・判定・報告するだけのときは、test_execution.md を直接読む

## hash
- a13ec95d864a050b35a175111679065fa638c2688f4ff161232e4e1b5c4eab0d

# `test_execution.md`

## Summary
- 構築済みの cmoc 開発環境を対象に、Python interpreter の選定と preflight、focused／full pytest、real_path_integration の分離実行、Ruff・mypy の検査、完了判定、結果報告までを定める実行手順。test と品質検査を実際に選択・実行・報告する必要がある場合の入口となる。
- realization test の意味上の要件、Python 環境構築や依存関係管理とは責務を分離し、それぞれの正本文書へ案内する。

## Read this when
- 構築済み環境で test や品質検査を実行する前に、対象 worktree と Python interpreter、必要な preflight を確認するとき。
- 変更に対する focused test、Ruff、mypy、full pytest、real_path_integration の選択基準を確認するとき。
- 検査結果、skip、外部実行条件、未完了理由を含む完了判定と報告方法を確認するとき。

## Do not read this when
- realization test が満たす意味上の要件や実経路統合テストの成立条件そのものを確認したいときは、oracle/doc/dev_rule/test_rule.md を直接読む。
- Python 環境の新規構築、依存関係の追加、pip 操作の手順を確認したいときは、oracle/doc/dev_rule/development_environment.md を直接読む。
- agent call の file access mode、作業範囲、sandbox の書き込み先を判断するときは、この手順を根拠にせず、動的生成プロンプトの指定を確認する。

## hash
- 70421a592225a6ac1179441ed8f388d4a1cff30ffd24fa0e7ffee8e18a292521

# `test_rule.md`

## Summary
- pytest を用いた realization test の意味上の要件を定め、決定論的な cmoc の制御ロジックと Codex CLI 呼び出しを伴う結合動作の検証範囲を示す。pytest の tmp_path に被テスト環境を隔離して構築する基本方針と、Fake Codex CLI の利用境界を扱う。実経路統合テストの正本用語、対象範囲、終了 code・外部結果の検証、公開末端サブコマンドとの機械的対応、Real Codex CLI・実推論・専用モデル設定の要件を定める。テスト実行手順や開発環境・依存関係の管理は、同階層の別文書ではなく指定された正本へ進むための入口となる。

## Read this when
- realization test を追加・変更・レビューし、pytest、tmp_path による隔離、検証対象の goal/non-goal、または Fake Codex CLI の利用可否を判断するとき
- 実経路統合テストの用語、pytest marker、公開末端サブコマンドとの対応、終了 code と外部から観測可能な結果の検証要件を確認するとき
- Codex CLI 呼び出しを伴うテストで、Real Codex CLI、実推論、ModelClass.MINIMUM、ReasoningEffort.LOW、model provider の扱いを確認するとき
- 公開末端サブコマンドを追加または rename し、対応する実経路統合テストケースの追加要否を確認するとき

## Do not read this when
- 構築済み環境での test・品質検査の選択、実行、完了判定、報告手順だけを確認するときは oracle/doc/dev_rule/test_execution.md を直接読む
- 開発環境の新規構築、依存関係の追加、pip 操作だけを確認するときは oracle/doc/dev_rule/development_environment.md を直接読む
- model provider に対する cmoc の責務境界や通常の Codex CLI 呼び出し規則を確認するときは、それぞれ指定された app_spec の正本を直接読む
- LLM の回答品質、Codex CLI 自体、または model provider の正しさ・安定性を自動テストの目的として評価するとき

## hash
- ab3b21471ee33a0847b80cb9e5b2c2ff71b67034de4ee5a9b0b4b70c97e478e2
