# `coding_rule.md`

## Summary
- Python 実装の基本方針、PEP 8、最小限の変更、識別子命名、型ヒント、import、docstring、コメント、非公開識別子のコーディング規則を定める。

## Read this when
- Python の実装・リファクタリングで命名、型注釈、import、docstring、コメント、公開範囲、変更規模の規則を確認するとき。
- cwd 識別子の命名や、ログメッセージ・コメントの言語方針を確認するとき。

## Do not read this when
- テスト固有の実装規則や検証方法だけを確認したいとき。
- 仕様上の挙動、設計上の責務分担、実行環境や依存関係の規則を確認したいとき。

## hash
- 20c080c18d8f4462559e6dbc5afcf2d8250ee835db5465563626b37079a191cd

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
- 構築済みのcmoc開発環境で、testと品質検査の対象・実行方法・完了条件・結果報告を定める手順書。
- worktreeとPython interpreterの選択、preflight、focused test、Ruff・mypy・pytest、実経路統合テスト、freshな完了ゲートの入口。

## Read this when
- testや品質検査を実行する前に、対象範囲・使用環境・コマンド・warning扱いを決めるとき
- 変更後にRuff、mypy、pytest、実経路統合テストを含むfreshな完了判定を行うとき
- 検査結果を、skip理由・実行環境・外部要因・full testの完了状況とともに報告するとき

## Do not read this when
- realization testが満たす意味上の要件を確認するときはtest_rule.mdを読む
- 型注釈やdocstringの品質要件を確認するときはcoding_rule.mdを読む
- Python環境の新規構築、依存関係追加、またはpip操作を行うときはdevelopment_environment.mdを読む
- 個別の実装やtestの内容を理解するときは、対応するrealizationまたはtest本文を直接読む

## hash
- 70cae4dfa732b790cb0d189ca2d09d1b43ea6fe444a7a85949986ee5a9914d8d

# `test_rule.md`

## Summary
- realization test が満たすべき意味上の要件と、決定論的な制御ロジックおよび Codex CLI 呼び出し経路の検証範囲を定める文書。
- pytest、tmp_path による隔離、実経路統合テストの用語・選択・検証要件、モデル設定、quota、Fake Codex CLI の扱いを確認するための入口。

## Read this when
- realization test の追加・変更・レビューで、検証対象、テスト環境、実経路統合テストの定義や要件を判断するとき。
- 公開末端サブコマンドとのテスト対応、実在 Codex CLI・実推論の使用、終了 code と外部結果の検証、テスト用 CmocConfig の設定を確認するとき。
- pytest marker、test 用 tmp_path 隔離、Fake Codex CLI の適用範囲を決めるとき。

## Do not read this when
- 構築済み環境での test・品質検査の選択、実行、完了判定、報告手順だけを確認したいときは、test_execution.md を直接読む。
- 開発環境の新規構築、依存関係の追加、または pip 操作を行うときは、development_environment.md を直接読む。
- Codex の model provider に関する責務境界や通常の quota 待機・再開規則だけを確認したいときは、指定された codex_model_provider.md または codex_exec_rule.md を直接読む。

## hash
- 4c8ae7117b0833069e0b6a410745b8d1b274d609c0bb2bf971d36abcc30b6d8d
