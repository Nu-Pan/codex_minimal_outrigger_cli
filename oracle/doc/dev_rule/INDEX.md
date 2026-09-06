# `coding_rule.md`

## Summary
- Python 実装の基本的なコーディング規則、cwd 識別子、型ヒント、import、docstring、コメント・ログの言語、非公開識別子の命名を定める開発ルール。

## Read this when
- cmoc の Python コードを新規作成・変更・レビューするときに、命名、責務、型注釈、import、docstring、コメント、非公開識別子の規則を確認したい場合。
- src または oracle/src の公開対象に対する型注釈・Google style docstring の適用範囲や、cwd を表す識別子の命名方針を確認する場合。

## Do not read this when
- 実行環境の構築や依存関係の扱いを確認する場合は、開発環境の規則を直接読む。
- テストの追加・変更・実行方法だけを確認する場合は、テスト規則やテスト実行手順を直接読む。
- 機械検査を通過した後の一般的な品質所見だけを求めており、コーディング規則自体を確認する必要がない場合。

## hash
- 4b3c191e6cf9e80e55f02ae55a91975ef315b242edd937f0c713ee5a6bd3f288

# `design_rule.md`

## Summary
- CLI の実装責務を定め、Typer によるエントリーポイントとサブコマンド本命処理の分離方針を示す設計規則。
- 複数サブコマンドで共通利用する機能を commons 配下へ配置する境界を定義する。

## Read this when
- CLI のエントリーポイント、引数解釈、サブコマンド実装の配置や責務分担を変更・確認するとき。
- サブコマンド間で共有するユーティリティ、定数、エラー処理などの配置を判断するとき。

## Do not read this when
- CLI や共通系の実装責務・配置を扱わず、個別サブコマンドの本命処理だけを直接確認するとき。
- テスト実行方法や開発環境の構築手順を確認するとき。

## hash
- 6050a02f8b64d7a55ae83b1504dc36e6a782b2da777aedd8ed114ebd87e8fc23

# `development_environment.md`

## Summary
- Python 環境の新規構築、依存関係の追加、pip 操作に必要な開発環境の前提・命名・エンコード・仮想環境運用を定める入口。
- 構築済み環境での通常の test 実行や品質検査の手順は扱わず、専用の test_execution.md へ案内する。

## Read this when
- Python 仮想環境の新規作成、パッケージのインストールや追加、pip 操作の条件を確認するとき。
- Python 実行環境、ファイル命名・エンコード、WSL2・VS Code・Codex CLI の開発前提を確認するとき。

## Do not read this when
- 構築済み環境で既存 test や品質検査を選択・実行・完了判定・報告するときは、test_execution.md を直接読む。
- 通常の test 実行だけを行うとき。

## hash
- 2a120c3c6f2224e4a7cb2a48344b62e80b763a5fe92a94abf2163a2134b55efc

# `test_execution.md`

## Summary
- 構築済みの cmoc 開発環境で、Python interpreter の選択と preflight、focused test・品質検査の選定、pytest・Ruff・mypy の実行、実経路統合テスト、fresh な完了ゲート、結果報告までを定める手順書。

## Read this when
- cmoc の test や品質検査を選択・実行するとき。
- 変更内容に応じた focused test、Ruff、mypy、通常の pytest、実経路統合テストの範囲を判断するとき。
- 検査完了の条件、skip の扱い、実行結果として報告すべき項目を確認するとき。

## Do not read this when
- realization test が満たすべき意味上の要件を確認するときは、正本である test_rule.md を直接読む。
- 型注釈や docstring の意味上の品質要件を確認するときは、coding_rule.md の該当箇所を読む。
- Python 環境の新規構築、依存関係の追加、または pip 操作を行うときは、development_environment.md を読む。

## hash
- e7cb58f143adea1d01654cc07d75f27550a4707839532c2a4babee00fb915d5b

# `test_rule.md`

## Summary
- pytest による realization test の意味上の要件、隔離された tmp_path 環境、決定論的制御ロジック、および Codex CLI 連携の検証範囲を定める正本。
- 実経路統合テストの用語、公開末端サブコマンドとの対応、実在の Codex CLI と実推論の使用、テスト用設定および quota の扱いを確認する入口。
- Fake Codex CLI を使用できる条件と、テスト実行手順・環境構築手順を別の正本へ委譲する境界を示す。

## Read this when
- realization test の新規作成・変更・レビューで、pytest、隔離環境、検証対象、Fake Codex CLI の使用可否を判断するとき。
- 利用者向け CLI の公開末端サブコマンドに対する実経路統合テストケースの要件や、Codex CLI 呼び出しの実推論・設定・観測結果の検証条件を確認するとき。
- テスト用 CmocConfig、model provider・Model・Reasoning Effort、quota の扱いを仕様に照らして確認するとき。

## Do not read this when
- 構築済み環境でのテスト・品質検査の選択、実行、完了判定、報告手順だけを確認したいときは test_execution.md を読む。
- Python 環境の新規構築、依存関係の追加、または pip 操作を行うときは development_environment.md を読む。
- LLM の回答品質、Codex CLI 自体、または model provider 自体の正しさを評価するテスト方針を求めているとき。

## hash
- 7afec483e6ff7e971fb1950621b011ee79cfbbfbcea066dcb0511892c5ccb922
