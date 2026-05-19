# `commons`

## Summary

- `src/commons` は cmoc のサブコマンド群から共有される共通処理をまとめる Python パッケージです。
- Codex CLI 呼び出し、Structured Output 検証、ログ保存、`INDEX.md` 自動メンテナンス、共通エラーレポート、Typer サブコマンド実行ラッパーを扱います。
- git リポジトリ root 探索、cwd 固定、ブランチ・HEAD 情報取得、`.cmoc` の git 追跡対象外保証、未コミット差分検査、oracle ファイル列挙などのリポジトリ操作を提供します。
- cmoc 仕様のタイムスタンプ生成と、サブコマンドのステップ別・合計経過時間表示のための軽量ユーティリティを含みます。
- 個別サブコマンド固有の業務ロジックではなく、`src/sub_commands` や `src/main.py` から再利用される横断的な実装の入口です。

## Read this when

- cmoc の複数サブコマンドで共有される実行制御、エラー処理、Codex CLI 連携、git 操作、時間計測の実装場所を探したいとき。
- `run_codex_exec`、`parse_json_object`、Structured Output schema 検証、Codex 実行ログ、JSON リトライ、サンドボックス指定の共通挙動を確認したいとき。
- `maintain_indexes` による `INDEX.md` 配置対象、除外規則、目次生成プロンプト、内容ハッシュ判定、既存目次ブロック再利用、自動コミット条件を調べたいとき。
- `run_command` による `<repo-root>` 解決、サブコマンド本体への `Path` 引き渡し、例外から `typer.Exit` への変換を確認したいとき。
- `CmocError` と `format_error_report` による共通エラーレポート形式、復旧アクション、詳細、終了コードの扱いを実装または修正したいとき。
- repo root 探索、`.cmoc` ignore 保証、未コミット差分検査、oracle ファイル列挙、cmoc ブランチ base commit 記録、git コマンド実行ラッパーを確認したいとき。
- cmoc の `<time-stamp>` 形式、ログ名やブランチ名に使う時刻文字列、ステップ別経過時間と合計経過時間の stdout 表示を調べたいとき。
- 個別サブコマンドの実装を読む前に、共通 helper の責務分担と参照先を把握したいとき。

## Do not read this when

- Typer の CLI エントリーポイントやサブコマンド登録だけを調べたいときは、`src/main.py` や `src/sub_commands` 側を読むべきです。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の個別業務フローやユーザー向け挙動だけを確認したいとき。
- cmoc の正本仕様断片を確認したいときは、実装ではなく `oracles` 配下の該当 `INDEX.md` から辿るべきです。
- pytest、Fake Codex CLI、テスト fixture、期待出力など、テスト側の構成だけを調べたいとき。
- README、AGENTS、oracles、memo の編集可否やリポジトリ運用ルールだけを確認したいとき。
- Codex CLI や git の一般的な使い方を調べており、cmoc 固有の共通実装が不要なとき。
- 特定モジュールの詳細な内部処理が既に明確な場合は、このディレクトリ概要ではなく `codex.py`、`indexing.py`、`repo.py` など該当ファイルを直接読むべきです。

## hash

- 7c2cca1e60e1edc1163b945778a8dbf440072b69c60ed2f80042d809aa8951b0

# `main.py`

## Summary

- cmoc の Typer ベースの CLI エントリーポイントを定義するファイル。
- `init`、`branch`、`eval-oracles`、`apply`、`merge` の各サブコマンドを登録し、それぞれ対応する `sub_commands` 配下の実装関数へ委譲する。
- `eval-oracles` では `--full` / `-f` オプション、`apply` では `--repeat` / `-r` オプション、`merge` では任意の `cmoc_branch` 引数を受け取る。
- `main()` は Typer/Click の例外や想定外例外を `commons.errors.format_error_report` による共通エラーレポート形式へ変換し、適切な終了コードで終了する。
- スクリプトとして直接実行された場合は `src` ディレクトリを `sys.path` に追加してから `main()` を起動する。

## Read this when

- cmoc CLI のトップレベルコマンド一覧やサブコマンド名を確認したいとき。
- 各 CLI コマンドがどの `sub_commands` 実装関数へ委譲されるか調べたいとき。
- `eval-oracles`、`apply`、`merge` の CLI 引数やオプション定義を確認したいとき。
- Typer/Click の parse error や実行時例外が、cmoc の共通エラーレポートへどう変換されるか確認したいとき。
- `bin/cmoc` などから直接起動される際のエントリーポイント処理を調べたいとき。

## Do not read this when

- 個別サブコマンドの詳細な処理内容や仕様を調べたいとき。
- `init`、`branch`、`eval-oracles`、`apply`、`merge` の内部実装ロジックを修正したいとき。
- 共通エラーレポートの具体的な整形ルールや例外クラス定義を調べたいとき。
- Codex CLI 呼び出し、ログ保存、oracle 評価、ブランチ操作、マージ処理などの実装詳細を確認したいとき。
- テストコード、開発環境、コーディング規約など cmoc 開発ルール全般を調べたいとき。

## hash

- 94aa9dcc576677bc140d61d6c7aaa19ae18ff8b875a40faa38c4d3517611adca

# `sub_commands`

## Summary

- `src/sub_commands` は、cmoc の各 CLI サブコマンド本体を実装する Python パッケージです。
- `init.py`、`branch.py`、`apply.py`、`eval_oracles.py`、`merge.py` に、`cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の実行フローが分かれて配置されています。
- 各サブコマンドは、stdout 進捗表示、`StepTimer` による経過時間表示、共通ヘルパー呼び出し、git 操作、Codex CLI 呼び出し、レポート保存などを必要に応じて接続します。
- `init.py` は `.cmoc` を git 追跡対象外にする初期化処理と、初期化差分の commit を扱います。
- `branch.py` は cmoc 作業ブランチ作成、ブランチ名生成、`.cmoc` ignore 保証、作成元 commit の記録を扱います。
- `apply.py` は oracle と実装の不整合調査、Structured Output schema、Codex CLI による実装修正依頼、禁止領域検査、変更 commit、apply レポート生成を扱います。
- `eval_oracles.py` は oracle 評価対象の選択、部分評価と全体評価の切り替え、Codex CLI による読み取り専用評価、評価レポート生成を扱います。
- `merge.py` は cmoc ブランチの解決、`git merge --no-ff`、conflict 発生時の Codex CLI 依頼、marker 検査、merge commit、作業ブランチ削除を扱います。
- `__init__.py` はサブコマンド実装パッケージであることを示すだけで、実行ロジックは含みません。

## Read this when

- cmoc の個別サブコマンド本体がどのファイルに実装されているか判断したいとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の処理順序、stdout 進捗表示、終了コード、レポート出力、git 操作を確認したいとき。
- サブコマンド実装から `commons.command_runner`、`commons.repo`、`commons.codex`、`commons.indexing`、`commons.timing`、`commons.timestamps` などの共通処理がどう呼ばれているか追いたいとき。
- `.cmoc` の git 追跡対象外保証、初期化 commit、cmoc 作業ブランチ作成、base commit 記録など、cmoc ワークフロー開始時の処理を確認したいとき。
- oracle 不整合調査、Structured Output schema、Codex CLI への prompt、実装修正依頼、禁止パス検査、commit message 生成など `cmoc apply` 固有の制御を調べたいとき。
- oracle 評価の部分評価条件、全体評価へのフォールバック、評価 prompt、`.cmoc/reports/eval-oracles` へのレポート保存形式を確認したいとき。
- cmoc ブランチ作成、base commit 記録、未マージ cmoc ブランチ解決、merge conflict 解消依頼、conflict marker 検査、ブランチ削除の実装を確認したいとき。
- サブコマンドの挙動を変更するために、実装入口となるモジュールを選びたいとき。

## Do not read this when

- Typer へのサブコマンド登録、CLI エントリーポイント、トップレベルのコマンド分岐だけを調べたいとき。
- git 実行、repo 探索、`.cmoc` パス生成、Codex CLI 呼び出し、INDEX メンテナンス、timestamp 生成などの共通ヘルパー内部だけを詳しく調べたいとき。
- cmoc の正本仕様断片やユーザー向け仕様だけを確認したいとき。
- pytest、Fake Codex CLI、テストデータ、テスト実装規約など tests 側の構成だけを調べたいとき。
- README、AGENTS、oracles、memo の編集可否やリポジトリ運用ルールだけを確認したいとき。
- `<repo-root>` 側で cmoc を使う開発作業の対象ファイルや、利用者リポジトリ固有の実装内容を調査したいとき。
- 個別サブコマンドではなく、cmoc 全体の設計方針、開発環境、コーディング規約だけを確認したいとき。

## hash

- 5940a7bc9dc62312c4d532eebbf7eb0a5987cfceb97ae5c88fb30d7677068e0d
