# `coding_rule.md`

## Summary
- cmoc の Python 実装におけるコーディング規則を定める文書。命名・責務・型ヒント・import・docstring・コメント・非公開識別子など、実装時に守るべき基準への入口となる。

## Read this when
- cmoc の src または oracle/src の実装を新規作成・変更・レビューするとき。
- 識別子の命名、型注釈、import 構成、docstring、コメントやログの言語などの判断基準を確認したいとき。

## Do not read this when
- 実装規則ではなく、cmoc の機能仕様や利用手順を確認したいとき。
- テスト固有の規則だけを確認する場合。本文では test を型注釈・docstring の必須検査範囲から除外しているため、テストの詳細はテスト関連の対象を直接読む。

## hash
- 7b69cc4f94c3fe9dfc733e35b3cc4adb199db63accbbc6132a7204d246d2a200

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
- Python 仮想環境の新規作成、依存関係の追加、pip 操作に必要な開発環境の前提と手順を定める文書。

## Read this when
- Python 実行環境や仮想環境を新規構築するとき
- pyproject.toml に依存関係を追加し、開発用パッケージをインストールするとき
- 使用する Python インタプリタや pip の場所、環境上の命名・エンコード規則を確認するとき

## Do not read this when
- 構築済み環境で通常の test や品質検査を実行するだけのときは、検査手順の正本を直接読む
- Python 環境の構築や依存関係の変更を伴わない通常の開発作業を行うとき

## hash
- 5a954b891dfe79f56dde7f96c48d7171a032e728a180f42c152ff57cc29c1091

# `test_execution.md`

## Summary
- 構築済みの cmoc 開発環境で、pytest・Ruff・mypy による focused 検査、full 完了ゲート、実経路統合テストの選択・実行・完了判定・結果報告を定める手順書。

## Read this when
- cmoc の変更に対して、使用する worktree と Python interpreter、preflight、検査範囲、pytest の warning 設定、Ruff・mypy・full test の実行条件を判断するとき。
- focused test や実経路統合テストを実行し、skip・失敗・環境不足を含む完了可否と報告項目を確認するとき。

## Do not read this when
- realization test の意味上の要件、型注釈・docstring の品質要件、Python 環境構築や依存関係管理の正本を確認する場合は、それぞれの oracle 規約を直接読むとき。
- 検査手順ではなく、実装や test 自体の変更方針・仕様適合性を確認するとき。

## hash
- a4d0f1d56f4832dfe3af8055baed1962b4dba0f7c09db08edb25ed2f834962da

# `test_rule.md`

## Summary
- realization test が検証すべき意味上の要件を定め、pytest・隔離された tmp_path 環境・決定論的制御ロジックのテスト方針を示す文書。
- 実経路統合テストの正本用語、選択 marker、対象範囲、実在する Codex CLI と実推論を用いた検証要件、および公開末端サブコマンドとの対応要件を定める。
- 実経路統合テストにおける agent call の設定取得、quota の扱い、model provider・Model・Reasoning Effort の境界と、Fake Codex CLI を使用できる条件を示す。

## Read this when
- realization test の目的、責務境界、配置、隔離環境、検証対象を確認するとき。
- 実経路統合テストを追加・変更・選択するとき、特に公開末端サブコマンドとの対応や実在の Codex CLI を使う要件を確認するとき。
- 実経路統合テストの agent call 設定、quota、model provider、または Fake Codex CLI の扱いを判断するとき。

## Do not read this when
- 構築済み環境での test・品質検査の選択、実行、完了判定、報告手順を確認したいとき。
- 開発環境の新規構築、依存関係の追加、または pip 操作の手順を確認したいとき。
- LLM や Codex CLI 自体の回答品質・安定性、または model provider の正しさを評価するとき。

## hash
- 4df53f32146e8aa5b6649442dd2e4a581ce74a5e79bd2d1ea1b6a55edf35f234
