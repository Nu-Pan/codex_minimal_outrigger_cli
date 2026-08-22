# `coding_rule.md`

## Summary
- Python 実装時のコーディング規約を定める文書。PEP 8、命名・責務・入出力、最小限の変更、コメント・docstring、型ヒント、import、cwd 識別子、非公開識別子、ログ言語などの判断基準を扱う。コードの書き方や識別子・コメント・型注釈の規則を確認する入口。

## Read this when
- Python コードを新規作成・変更・レビューするとき
- cwd を表す識別子、型ヒント、import、docstring、コメント、ログ、非公開識別子の規則を確認するとき
- 要求を満たす最小限の実装方針やオーバーエンジニアリング回避の基準を確認するとき

## Do not read this when
- 実装の責務配置や CLI の設計境界を確認したいとき
- テストの追加・変更規則やテスト実行手順を確認したいとき
- 正本仕様そのものの挙動・インターフェース契約を確認したいとき

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
- 構築済みの cmoc 開発環境を対象に、test と品質検査の選択、preflight、実行、完了判定、結果報告を定める手順書。
- 現在の worktree と適切な Python interpreter の決定、focused/full pytest、実経路統合テスト、Ruff、mypy、Python development mode、ResourceWarning 検査を扱う。
- test の意味要件や環境構築、依存関係追加、権限拡張は責務外として、対応する正本仕様へ委譲する。

## Read this when
- cmoc の変更に対して実行すべき focused test、full test、Ruff、mypy を選ぶとき
- 現在の worktree で preflight と品質検査を実行し、完了可否を判定するとき
- pytest の skip、実経路統合テスト、Codex CLI、model provider、quota、timeout などの実行結果を報告するとき

## Do not read this when
- realization test が満たす意味上の要件を確認するときは test_rule.md を直接読む
- Python 環境の新規構築、依存関係の追加、pip 操作を行うときは development_environment.md を直接読む
- Codex CLI の呼び出し規則や実経路統合テスト固有の仕様を確認するときは、それぞれの正本仕様を直接読む

## hash
- 333f7ed9b3d623e8ced8ba572a79e4972bc03baf5107021c6033ef3c4699fbae

# `test_rule.md`

## Summary
- 対象は cmoc の realization test が満たすべき意味上の要件を定める正本文書です。pytest、tmp_path による隔離、決定論的制御ロジック、Codex CLI を含む実経路統合テスト、Fake Codex CLI の適用範囲を扱います。
- テストの実行手順や品質検査の選択は別の test_execution 文書、環境構築や依存関係・pip 操作は development_environment 文書へ分岐するため、それらの入口ではありません。

## Read this when
- realization test の新規作成・変更・レビューで、検証対象やテストの責務境界を確認するとき
- 実経路統合テストの定義、対象サブコマンドとの対応、実在 Codex CLI・実推論の使用要件を確認するとき
- テスト隔離、モデル設定、quota、Fake Codex CLI の適用条件を判断するとき

## Do not read this when
- 構築済み環境でのテスト選択・実行・完了判定・報告手順を確認したいときは test_execution 文書を読む
- Python 環境の新規構築、依存関係の追加、pip 操作を行うときは development_environment 文書を読む
- テスト対象ではなく実装の設計責務や CLI 実装配置を判断するときは design_rule 文書など実装側の正本を読む

## hash
- d0ae77dbeb53077ad82230fb8c0c2d81d56841ad396bdaad7e670dfbce68c506
