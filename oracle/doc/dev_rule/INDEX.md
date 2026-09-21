# `coding_rule.md`

## Summary
- cmoc の Python 実装に適用する基本的なコーディング規則を定める正本。PEP 8、責務と入出力、過剰実装の回避に加え、cwd 識別子、型ヒント、import、docstring、コメント、非公開識別子の扱いを確認する入口。

## Read this when
- cmoc または oracle/src の実装で命名・型注釈・import・docstring・コメント・公開範囲を決めるとき
- Ruff や mypy などの機械検査だけでは判断できないコード品質上の規約を確認するとき
- cwd を表す識別子や agent call 関連の変数名を追加・変更するとき

## Do not read this when
- 機能の振る舞い、入出力仕様、CLI 操作、データ形式の正本仕様を確認したいとき
- テスト固有の設計や fixture の規約だけを確認したいとき
- 個別の実装箇所を直接調査するだけで、コーディング方針の判断が不要なとき

## hash
- 63c5f274802e9cf39e0da98fc168f9282d6181d4635cf6989b3566615a687b26

# `design_rule.md`

## Summary
- cmoc の CLI 実装配置と共通機能の配置ルールを定める設計規約です。
- CLI の引数解釈は src/main.py、各サブコマンドの本命処理は src/sub_commands 配下、複数サブコマンドで共有する機能は src/commons 配下に置く構成を示します。

## Read this when
- CLI のエントリーポイント、サブコマンド処理、または共通ユーティリティの実装場所や分割方針を決めるとき。
- src/main.py と src/sub_commands 配下の責務分担、または複数サブコマンドで使う機能の配置を確認するとき。

## Do not read this when
- 個別サブコマンドの仕様や処理内容を確認したいときは、そのサブコマンドの oracle doc または実装を直接読みます。
- Typer や共通機能の具体的な API、エラー仕様、テスト方針を確認したいときは、対応する詳細仕様やコードを直接読みます。

## hash
- 5140757764500307eeae7ac0ea55ba98c6fb640c5f775d67e6a04e8b7a813867

# `development_environment.md`

## Summary
- cmoc 開発環境の正本ルール。前提となる開発環境、文字コードと命名規則、Python 仮想環境の使用方法、依存関係追加時の手順を定める。

## Read this when
- Python 環境を新規構築するとき。
- 依存関係やパッケージを追加・インストールするとき。
- Python インタプリタ、pip、ファイルエンコード、命名規則など開発環境上の条件を確認するとき。

## Do not read this when
- 構築済み環境で既存テストや品質検査を実行・判定・報告するだけのときは、test_execution.md を直接読む。
- 個別の機能仕様や実装内容を確認・変更するときは、対象の oracle doc や src/test を直接読む。

## hash
- 5d2103792f6eb36a50a8cccddb6f6f101ec5cfa830aec08dd17885163ae9cad0

# `test_execution.md`

## Summary
- 構築済みの cmoc 開発環境で、Python interpreter と preflight 条件を確認し、focused test・品質検査・実経路統合テスト・fresh な完了ゲートの選択、実行、完了判定、結果報告を定める手順書。関連するテスト仕様、コーディング規約、開発環境の正本への入口でもある。

## Read this when
- cmoc のテストや Ruff・mypy の実行対象、実行コマンド、warning の扱い、実経路統合テストの分離方法を決めるとき。
- 変更後に fresh な完了ゲートを実行し、未完了条件や skip・failure の理由を報告するとき。

## Do not read this when
- テストそのものが満たす意味上の要件を確認したいときは、テスト実装規約を直接読む。
- 型注釈・docstring の品質要件を確認したいときは、コーディング規約を直接読む。
- Python 環境の構築や依存関係、pip 操作の手順を確認したいときは、開発環境の正本を直接読む。
- 個別の実装やテストコードの仕様・挙動を確認したいとき。

## hash
- 3715cf45eaba6acb3862f6f56e7b24cdbdbd67d27a08b072fcb25aa4ea5ec167

# `test_rule.md`

## Summary
- realization test が満たす意味上の要件を定め、pytest・隔離された tmp_path 環境・テストの目的と非目的を示す。
- 実経路統合テストについて、対象範囲、独立 process 実行、実在の Codex CLI と実推論、サブコマンド対応、設定と quota の扱いを定める。
- 実経路統合テスト以外で決定論的な制御ロジックを検証する場合の Fake Codex CLI の利用境界を示す。

## Read this when
- realization test の設計・実装方針、テスト対象と非対象の境界を確認したいとき。
- 実経路統合テストケースの追加・変更、公開末端サブコマンドとの対応、Codex CLI 呼び出しを伴う検証方法を判断するとき。
- Fake Codex CLI を使える条件や、テスト用 CmocConfig の model provider・Model・Reasoning Effort 設定を確認するとき。

## Do not read this when
- 構築済み環境での test・品質検査の実行手順や完了判定を確認したいときは、test_execution.md を直接読む。
- 開発環境の構築、依存関係の追加、pip 操作を確認したいときは、development_environment.md を直接読む。
- Codex CLI の model provider に関する責務境界や通常の呼び出し規則を確認したいときは、指定された app_spec 文書を直接読む。
- 個別の実装コードやテストケースの詳細を確認したいときは、該当する realization test・実装ファイルを直接読む。

## hash
- 4de13a36023c782020e6db812050bab16c4767d51ec2aecfba87dba18a69ea45
