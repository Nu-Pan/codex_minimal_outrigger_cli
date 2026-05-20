# `commons`

## Summary

- `src/commons` は、cmoc のサブコマンドや実行時処理から横断的に使われる共通処理をまとめる Python パッケージです。
- Codex CLI 呼び出し、Structured Output 検証、ログ保存、リトライ、共通エラーレポート、Typer サブコマンド実行ラッパーを扱います。
- git リポジトリルート探索、`.cmoc` の git 追跡対象外保証、未コミット差分検査、一時 index を使った限定 commit、oracle ファイル列挙、branch base commit 記録などのリポジトリ操作を提供します。
- `INDEX.md` 自動メンテナンスの対象ディレクトリ列挙、除外規則、内容ハッシュによる更新判定、Codex CLI への目次生成依頼、既存目次ブロック再利用を実装しています。
- タイムスタンプ生成とサブコマンドのステップ別・総経過時間計測の補助処理を含みます。

## Read this when

- cmoc の複数サブコマンドから共有される処理の入口や責務分担を把握したいとき。
- Codex CLI 呼び出し、Structured Output、JSON 検証、ログ保存、リトライ、INDEX 保守との連携を調べたいとき。
- サブコマンドの共通実行制御、repo root 解決、例外からエラーレポートと終了コードへの変換を確認したいとき。
- git 操作、`.cmoc` ignore 保証、未コミット差分検査、oracle ファイル列挙、限定 commit、branch base commit ファイルの扱いを実装・修正したいとき。
- `INDEX.md` の自動生成・更新、除外対象、hash 判定、既存ブロック再利用、目次生成 prompt の流れを確認したいとき。
- cmoc 仕様の `<time-stamp>` 形式やステップ時間計測・経過時間表示の共通実装を確認したいとき。

## Do not read this when

- 個別サブコマンドの CLI オプション、具体的な業務ロジック、ユーザー向けワークフローだけを調べたいとき。
- 正本仕様断片としての oracle 本文や、仕様ルーティングそのものを確認したいとき。
- テストコード、pytest 設定、Fake Codex CLI など、テスト実装だけを調べたいとき。
- README、AGENTS、oracles、memo の編集可否など、リポジトリ運用ルールだけを確認したいとき。
- 特定の共通処理ファイルを読むべきことが既に明確で、このパッケージ全体の目次情報が不要なとき。

## hash

- cb340e7f1fe19f45d5f3cf6acc67d9b094de92c84cea3ca9d0b7f13df7b9b599

# `main.py`

## Summary

- `src/main.py` は cmoc CLI のエントリーポイントで、Typer アプリケーション `cmoc` を定義する。
- `init`、`branch`、`eval-oracles`、`apply`、`merge` の各サブコマンドを登録し、実処理は `sub_commands` 配下の実装関数へ委譲する。
- `eval-oracles` では `--full` / `-f` オプション、`apply` では `--repeat` / `-r` オプション、`merge` では任意の `cmoc_branch` 引数を受け取る。
- `eval-oracles` の実装は `load_eval_oracles_module()` で遅延ロードしたモジュールから取得する。
- `main()` は `app(prog_name="cmoc", standalone_mode=False)` で Typer を起動し、Click/Typer の終了やパースエラー、その他例外を cmoc 共通のエラーレポート形式へ変換して終了コードを制御する。
- `python src/main.py` として直接実行された場合も `main()` を呼び出して CLI を起動する。

## Read this when

- cmoc CLI のトップレベルコマンド登録箇所を確認したいとき。
- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc apply`、`cmoc merge` がどの実装関数へ委譲されるか調べたいとき。
- 各サブコマンドの Typer 側のオプションや引数定義を確認したいとき。
- Typer や Click の例外、CLI パースエラー、想定外例外がどのように共通エラーレポートへ整形されるか確認したいとき。
- cmoc のプロセス終了コードがエラー種別ごとにどう決まるか調べたいとき。
- `python src/main.py` で直接実行する経路を確認したいとき。

## Do not read this when

- 各サブコマンドの具体的な処理内容や git 操作、ファイル生成、Codex CLI 呼び出しの詳細を知りたいとき。
- cmoc の共通エラーレポート本文の生成ロジックそのものを調べたいとき。
- oracle 仕様、INDEX.md 生成仕様、ログ保存仕様などのアプリケーション仕様を確認したいとき。
- テストコード、Fake Codex CLI、pytest 設定などのテスト実装を調べたいとき。
- README、AGENTS、oracles、memo などのリポジトリ運用ルールや編集可否だけを確認したいとき。

## hash

- 5409068ac50eafc1be02f00a6e8fcb4a568bea891f19d8c57c736a33f2eb7946

# `sub_commands`

## Summary

- `src/sub_commands` は、cmoc の各サブコマンド本体を実装する Python パッケージです。
- `init.py` は `cmoc init` の本体で、repo root 解決を共通 runner に委譲し、`.cmoc` の git ignore 保証、初期化差分の commit、2 段階の進捗表示と時間レポートを扱います。
- `branch.py` は `cmoc branch` の本体で、`cmoc_<timestamp>` 形式の作業ブランチ作成、衝突時の最大 10 回リトライ、`.cmoc` ignore 保証、作成元 commit の `.cmoc/branch` 記録を扱います。
- `apply.py` は `cmoc apply` の本体で、cmoc ブランチ制約、未コミット差分検査、INDEX.md メンテナンス、不整合調査、Codex CLI による実装修正、禁止パス検査、commit、apply レポート生成、収束時と未収束時の終了コードを扱います。
- `eval-oracles.py` は `cmoc eval-oracles` の本体で、`.cmoc` ignore 保証、INDEX.md メンテナンス、部分評価または全体評価の対象 oracle 選択、Codex CLI による oracle 評価、`.cmoc/reports/eval-oracles` への Markdown レポート保存を扱います。
- `eval_oracles.py` は、ハイフン付きファイル名の本命実装 `eval-oracles.py` を通常の Python import から扱うための互換モジュールです。
- `merge.py` は `cmoc merge` の本体で、作業ツリー検査、merge 元 cmoc ブランチ解決、`git merge --no-ff`、conflict 時の Codex CLI 解消依頼、marker 検査、merge commit、source branch の安全削除を扱います。
- `__init__.py` はサブコマンド実装パッケージであることを示すだけの初期化ファイルで、実行ロジックは含みません。

## Read this when

- cmoc の個別サブコマンド実装がどのファイルにあるか判断したいとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の本体処理、進捗表示、時間計測、エラー条件、レポート保存、git 操作の呼び出し順序を調べたいとき。
- サブコマンドから `commons.command_runner`、`commons.repo`、`commons.codex`、`commons.indexing`、`commons.timing` などの共通処理がどう使われているか確認したいとき。
- Codex CLI に渡す prompt、read-only と workspace-write の使い分け、Structured Output schema、レポート生成 prompt、conflict 解消 prompt を確認したいとき。
- cmoc ブランチ上での oracle 差分処理、INDEX.md メンテナンス、不整合追従、禁止パス検査、commit 作成、merge conflict 解消など、複数のサブコマンドにまたがる実行フローを実装コードから追いたいとき。
- テストから直接呼ばれる `cmoc_*_impl` 関数や、`eval_oracles.py` 経由の互換 import の理由を確認したいとき。

## Do not read this when

- CLI エントリーポイントで Typer コマンドがどう登録されるかだけを調べたいとき。
- repo root 探索、git コマンド実行、`.cmoc` パス生成、oracle ファイル列挙、タイムスタンプ生成、時間計測、Codex CLI 実行、JSON パース、INDEX.md 生成の共通実装そのものを調べたいとき。
- cmoc の正本仕様断片やユーザー向け仕様だけを確認したいとき。その場合は `oracles/INDEX.md` から必要な仕様へルーティングしてください。
- cmoc 自体の開発ルール、Python コーディング規約、テスト規約、開発環境ルールだけを確認したいとき。
- 自動テストの具体的なケース、Fake Codex CLI、pytest fixture、テストデータ構成だけを調べたいとき。
- `__pycache__` 配下の生成済みバイトコードを調べたいとき。通常の実装確認では読む必要がありません。

## hash

- 8a69133f03609f59877673d231aec0340c16dab75b501a18b78c9398c5c97bba
