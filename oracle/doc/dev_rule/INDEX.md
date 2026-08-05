# `coding_rule.md`

## Summary
- cmoc の Python 実装におけるコーディング規則を定める正本仕様。PEP 8、命名・責務・入出力の明確化、最小限の変更、型ヒント、相対 import、Google style docstring、コメント・ログの言語、非公開識別子の命名を扱う。

## Read this when
- Python の実装、修正、レビューを行うとき
- 命名、型ヒント、import、docstring、コメント、ログ、cwd 識別子の規則を確認するとき

## Do not read this when
- テスト固有の作成・変更規則だけを確認するとき
- 開発環境の構築や依存関係管理だけを確認するとき
- 仕様そのものや CLI の挙動を確認するとき

## hash
- 10ce107790563037a796187d2a3959120787f2c61e70a5c832cc6c59154f5a56

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
- 構築済みの cmoc 開発環境を前提に、現在の worktree と Python interpreter を決定し、preflight、focused test、品質検査、full test、GPU test、完了判定、結果報告までの実行手順を定める文書。pytest は repository local runner を使用し、Python development mode と ResourceWarning 検査を適用する。

## Read this when
- cmoc の test、pytest、Ruff、mypy、GPU integration test、品質検査を選択・実行・報告するとき。
- Python 環境や依存関係の不足、test の skip・失敗、GPU test の sandbox escalation、full test の完了可否を判断するとき。
- 変更後に fresh な完了ゲートを実行し、使用した worktree・interpreter・command・結果・skip reason を報告するとき。

## Do not read this when
- realization test が満たすべき意味上の要件を確認する場合は、test_rule.md を直接読む。
- Python 環境の新規構築、依存関係の追加、pip 操作を行う場合は、development_environment.md を直接読む。
- test 実行以外の実装、仕様設計、または agent call の file access・作業範囲・sandbox 権限を判断する場合。

## hash
- 53cf7109630279120a8f0d6905abe4d6ae04605afa8f447043fa4aef1e417ff8

# `test_rule.md`

## Summary
- realization test の意味上の要件を定める正本文書。pytest、隔離された test-root、決定論的制御ロジック、Codex CLI を含む実経路統合テスト、test-local Ollama、GPU 実行、キャッシュ、クラウド backend 禁止、Fake Codex CLI の適用範囲を扱う。テスト実行手順や環境構築・依存操作の詳細は別の正本文書への入口として位置づけられる。

## Read this when
- realization test の追加・変更・レビューで、検証対象、実経路統合テスト、Codex CLI と Ollama の扱い、GPU marker、timeout、cache、backend 制約を判断するとき。
- テストが仕様上の goal / non-goal や外部から観測可能な結果を満たしているか確認するとき。

## Do not read this when
- 構築済み環境でのテスト選択・実行・完了判定・報告手順だけを確認したいときは、test_execution.md を直接読む。
- Python 環境の新規構築、依存関係の追加、pip 操作を行うときは、development_environment.md を直接読む。
- LLM の回答品質、Codex CLI 自体や model provider の正しさ、有料クラウド backend、GPU 性能・推論速度そのものを評価するとき。

## hash
- f1837a73e1fc07ba376aeb4a6cb5583c0b6e5eaf10a366a0bbb50508c1880ff3
