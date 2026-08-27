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
- `test_execution.md` は、構築済みの cmoc 開発環境で test と品質検査を選択・実行し、結果から完了可否を判定して報告する手順を定める。
- 現在の worktree と使用可能な `.venv` を確定し、preflight、focused test、Ruff、mypy、通常の full pytest、実経路統合テストを実行する際の条件と境界を扱う。
- test の意味上の要件は `oracle/doc/dev_rule/test_rule.md`、環境構築や依存関係・pip 操作は `oracle/doc/dev_rule/development_environment.md` に委ねるため、それらを確認する際の実行手順上の入口となる。
- 実行結果では interpreter、command、test 数、skip reason、失敗原因、実在の Codex CLI や実推論の実行状況、fresh な full test 完了可否を区別して報告する。

## Read this when
- cmoc の Python code、test、または first-party path の変更後に、実行すべき focused test と品質検査を決めるとき
- 現在の worktree、利用する `.venv`、Python version、pytest・Ruff・mypy の preflight を確認するとき
- 通常の pytest と `real_path_integration` を分けて実行し、fresh な完了ゲートを判定するとき
- test や品質検査の終了状態、skip、環境不足、model provider、quota、timeout などを分類して報告するとき

## Do not read this when
- test が満たすべき意味上の要件や実経路統合テストの成立条件を確認するときは、`oracle/doc/dev_rule/test_rule.md` を直接読む
- Python 環境の新規構築、依存関係の追加、または pip 操作を行うときは、`oracle/doc/dev_rule/development_environment.md` を直接読む
- 実装や test の責務・配置を判断するときは、この実行手順ではなく対応する設計・test の正本を直接読む
- 対象文書の内容を変更せず、単に実装上の問題や期待値の意味を調査するときは、この手順書を入口にする必要はない

## hash
- d60907479d0a19ec18d3a86b096906eb9149e24975c77601b98cb495bacb0cd2

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
