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
- 構築済みの cmoc 開発環境で、Python interpreter と repository root の決定、preflight、focused test・品質検査の選択、pytest/Ruff/mypy の実行、実経路統合テストを含む fresh な完了ゲート、完了判定、結果報告を定める手順。関連するテスト要件・コーディング要件・環境構築要件との責務境界も示す。

## Read this when
- 変更に対して、どの test・品質検査を選び、どの interpreter と command で実行し、何をもって完了と判定するかを確認するとき。
- focused test、full test、実経路統合テスト、Ruff、mypy、ResourceWarning 検査の実行条件や結果報告項目を確認するとき。
- 検査を開始できない環境不足や、失敗・skip・外部要因をどのように分類して報告するかを判断するとき。

## Do not read this when
- realization test が満たす意味上の要件を確認したいときは、test_rule.md を直接読む。
- 型注釈や docstring の品質要件を確認したいときは、coding_rule.md を直接読む。
- Python 環境の新規構築、依存関係追加、pip 操作の規則を確認したいときは、development_environment.md を直接読む。
- 個別テストの実装や対象機能の仕様を調べたいときは、対応する test code または仕様文書を直接読む。

## hash
- 0a22e5471b7fa296113c99fc5490cdc5fb01a49dd278cf4a16d2fd76f7389ff5

# `test_rule.md`

## Summary
- realization test が満たす意味要件を定める正本規約。pytest、tmp_path による隔離、決定論的制御ロジックと Codex CLI 結合動作の検証範囲を扱う。
- 実経路統合テストの用語、pytest marker、公開末端サブコマンドとの対応、実在する Codex CLI と実推論の使用、model provider・Model・Reasoning Effort・quota の扱いを定める。
- 実経路統合テスト以外では、Real Codex CLI が不要な決定論的制御ロジックの検証に限り Fake Codex CLI を使用できる。

## Read this when
- realization test の目的、責務境界、対象とすべき cmoc の制御ロジックを決めるとき。
- 実経路統合テストを追加・変更し、用語、marker、公開サブコマンドとの対応、外部から観測可能な結果、実際の Codex CLI 呼び出し要件を確認するとき。
- テスト用 CmocConfig や agent call の model provider、Model、Reasoning Effort、quota の扱いを設計するとき。
- Fake Codex CLI を使ったテストが許容される範囲を判断するとき。

## Do not read this when
- 構築済み環境での test・品質検査の実行手順、完了判定、報告方法を確認したいときは test_execution.md を読む。
- 開発環境の新規構築、依存関係の追加、pip 操作を確認したいときは development_environment.md を読む。
- model provider に対する cmoc の責務境界を確認したいときは codex_model_provider.md を読む。
- quota 枯渇時を含む通常の Codex CLI 呼び出し規則を確認したいときは codex_exec_rule.md を読む。
- テスト対象の具体的な実装コードや個別テストケースの内容を確認したいときは、対応する realization test のソースを直接読む。

## hash
- 9037578e7664d3488c6282dd2a7d2a1a75307be476ba4ac6978d0454edd6cb74
