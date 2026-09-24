# `coding_rule.md`

## Summary
- cmoc の Python コードに適用する実装規約を定め、命名、型付け、import、docstring、コメント、非公開識別子の判断先となる。
- 型注釈や docstring の適用範囲を、実装コードとテストコードで区別する規則も扱う。

## Read this when
- cmoc の実装を追加・変更するとき、Python の書き方や識別子の命名方針を確認したい。
- 型注釈、import、docstring、コメント、または型エラーへの対処方法を判断したい。

## Do not read this when
- CLI や共通機能の配置・責務を決める場合は、コード設計の規則へ進む。
- テストの意味上の要件や検証対象を決める場合は、テスト実装規約へ進む。
- 既存環境での検査の選択・実行・完了判定は検査実行手順へ、環境構築・依存追加・pip 操作は開発環境の規則へ進む。

## hash
- 63c5f274802e9cf39e0da98fc168f9282d6181d4635cf6989b3566615a687b26

# `design_rule.md`

## Summary
- CLI の入口とサブコマンド本処理の分担、および複数コマンドで使う共通機能の配置を定める設計規則。

## Read this when
- CLI の引数受付とサブコマンド実装の分担や、共通処理の配置を決める・見直すとき。

## Do not read this when
- 命名、型注釈、import、docstring など個別の書き方だけを確認するときは、コーディング規則を読む。
- 特定コマンドの利用者向け挙動や入出力の仕様を確認するときは、該当するアプリ仕様を読む。
- テストの意味上の要件や実行手順を確認するときは、テスト規則またはテスト実行手順を読む。

## hash
- 5140757764500307eeae7ac0ea55ba98c6fb640c5f775d67e6a04e8b7a813867

# `development_environment.md`

## Summary
- cmoc 開発環境の前提、文字コード・命名規則、Python 仮想環境と pip の扱いを定める。
- Python 環境の構築や依存関係の変更に関する判断の入口となる。

## Read this when
- Python 環境を新規構築する、開発依存関係を追加する、または pip を操作するとき。
- Python のバージョン・仮想環境の使い方や、ファイルの文字コード・命名規則を確認するとき。

## Do not read this when
- 構築済み環境での test や品質検査の選択・実行・完了判定だけを行うときは、実行手順を定める文書を直接読む。

## hash
- 5d2103792f6eb36a50a8cccddb6f6f101ec5cfa830aec08dd17885163ae9cad0

# `test_execution.md`

## Summary
- 構築済みの cmoc 開発環境で test と品質検査を選択・実行し、完了判定と結果報告を行う手順を定める。
- 変更内容に応じて検査範囲を選び、fresh な完了ゲートが必要か判断するときの入口となる。

## Read this when
- 既存の Python 環境で test や品質検査を実行する対象・手順を決めるとき。
- 変更後の完了条件や、検査結果の報告に必要な項目を確認するとき。

## Do not read this when
- realization test の意味上の要件や実経路統合テストの成立条件を確認するときは、テスト実装規約を読む。
- Python 環境の新規構築、依存関係の追加、pip 操作を行うときは、開発環境の規約を読む。
- 型ヒントや docstring 自体の品質要件を確認するときは、コーディング規約を読む。

## hash
- 0a22e5471b7fa296113c99fc5490cdc5fb01a49dd278cf4a16d2fd76f7389ff5

# `test_rule.md`

## Summary
- realization test が検証する意味上の要件と対象範囲を定め、決定論的な制御ロジックと Codex CLI を伴う結合動作を扱う。
- 利用者向け CLI の実経路統合テストの成立条件と、Fake Codex CLI を使える範囲を示す。

## Read this when
- テストの期待動作や対象範囲を決める、または realization test の方針を見直すとき。
- 公開 CLI サブコマンドに対応する実経路統合テストを追加・変更するときや、テストの分類・実推論の扱いを確認するとき。
- Fake Codex CLI を使える条件を確認するとき。

## Do not read this when
- 構築済み環境での test・品質検査の選択、実行、完了判定、報告だけが必要な場合は、その実行手順の正本を読む。
- Python 環境の新規構築、依存関係の追加、pip 操作の条件だけが必要な場合は、開発環境の正本を読む。

## hash
- 9037578e7664d3488c6282dd2a7d2a1a75307be476ba4ac6978d0454edd6cb74
