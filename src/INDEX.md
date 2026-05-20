# `commons`

## Summary

- `src/commons` は cmoc のサブコマンド横断で使う共通処理を集約する Python パッケージです。
- Codex CLI 呼び出し、Structured Output 検証、ログ保存、INDEX.md 自動メンテナンス、共通エラー報告、Typer 実行ラッパー、git リポジトリ操作、タイムスタンプ生成、ステップ時間計測を扱います。
- `codex.py` は `codex exec` の実行、read-only / workspace-write サンドボックス指定、最大 3 回の JSON リトライ、schema 検査、`.cmoc/logs/codex_exec` へのログ保存を担当します。
- `indexing.py` は `INDEX.md` の配置対象列挙、除外規則、内容 hash による更新判定、Codex CLI への目次生成依頼、既存目次ブロック再利用、自動コミット連携を実装します。
- `repo.py` は repo root 探索、cwd 固定、git コマンド実行、`.cmoc` の ignore 保証、作業ツリー検査、oracle ファイル列挙、cmoc ブランチ基点 commit 管理などを提供します。
- `errors.py`、`command_runner.py`、`timestamps.py`、`timing.py` はそれぞれ共通エラー整形、サブコマンド実行制御、cmoc タイムスタンプ生成、ステップ別経過時間表示を担います。

## Read this when

- cmoc の複数サブコマンドから再利用される共通実装の入口を探しているとき。
- Codex CLI 呼び出し、Structured Output、ログ保存、リトライ、JSON object 解析の共通挙動を確認したいとき。
- `INDEX.md` の自動作成・更新、目次生成プロンプト、除外規則、hash による再生成判定を調べたいとき。
- repo root 探索、git コマンド実行、未コミット差分チェック、`.cmoc` の git 追跡対象外保証を実装または修正したいとき。
- oracle ファイル列挙、変更済み oracle の抽出、oracle 削除検出、cmoc branch の base commit 記録を確認したいとき。
- サブコマンドの Typer 関数から本体 handler を呼び出す共通ラッパーや、例外を stdout エラーレポートと終了コードへ変換する流れを調べたいとき。
- ログ名やブランチ名に使う `<time-stamp>` 形式、またはサブコマンド完了時のステップ別タイミング表示を確認したいとき。

## Do not read this when

- 個別サブコマンドの CLI オプション、ユーザー向けワークフロー、業務ロジックそのものを調べたいとき。
- cmoc の正本仕様断片を読みたいだけで、実装コードの共通ユーティリティには関心がないとき。
- テストコード、pytest fixture、Fake Codex CLI など tests 配下の実装だけを確認したいとき。
- README、AGENTS.md、oracles、memo などのリポジトリ運用ルールや編集可否だけを確認したいとき。
- Python パッケージの存在確認だけが目的で、各共通処理の責務や実装詳細が不要なとき。
- git や Codex CLI の一般的な使い方を調べており、cmoc 固有の共通ラッパーの挙動が不要なとき。

## hash

- e3027f77566ac1122671df82ed3ef10b0a8d18c8d040321bea46379e23a6a0d0

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
- `init.py` は `cmoc init` の本体で、`.cmoc` を git 追跡対象外にする保証、初期化差分の commit、2 段階の進捗表示と時間計測を扱います。
- `branch.py` は `cmoc branch` の本体で、`cmoc_<timestamp>` 形式の作業用ブランチ作成、衝突時リトライ、`.cmoc` ignore 保証、作成元 commit の `.cmoc/branch` 記録を扱います。
- `apply.py` は `cmoc apply` の本体で、cmoc ブランチ制約、oracle 外未コミット差分の拒否、`INDEX.md` メンテナンス、oracle と実装の不整合調査、Codex CLI による実装修正依頼、禁止パス検査、commit、apply レポート生成を扱います。
- `eval-oracles.py` は `cmoc eval-oracles` の本体で、`.cmoc` ignore 保証、`INDEX.md` メンテナンス、部分評価と全体評価の対象選択、Codex CLI による oracle 評価、`.cmoc/reports/eval-oracles` への Markdown レポート保存を扱います。
- `eval_oracles.py` は、ハイフン付きファイル名の `eval-oracles.py` を通常の Python import から扱うための互換モジュールで、`cmoc_eval_oracles_impl` と `_evaluation_prompt` を再公開します。
- `merge.py` は `cmoc merge` の本体で、未コミット変更確認、merge 元 cmoc ブランチ解決、`git merge --no-ff`、conflict 発生時の Codex CLI 解消依頼、marker 残存検査、merge commit、安全な source branch 削除を扱います。
- `__init__.py` は `sub_commands` がサブコマンド実装パッケージであることを示すだけの初期化ファイルです。

## Read this when

- cmoc のサブコマンド実装がどのファイルに分かれているか把握したいとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の本体処理を調べたいとき。
- サブコマンドごとの進捗表示、`StepTimer` による時間計測、共通 runner への委譲、repo root 引数の扱いを確認したいとき。
- `.cmoc` を git 追跡対象外にする処理が各サブコマンドでどのタイミングで呼ばれるか確認したいとき。
- 作業用 cmoc ブランチの作成、base commit 記録、merge 元ブランチ解決、merge 後の branch 削除など、ブランチ操作に関係するサブコマンド実装を追いたいとき。
- oracle ファイル、`INDEX.md` メンテナンス、Codex CLI 呼び出し、Structured Output、レポート保存に関係するサブコマンド実装を確認したいとき。
- `eval-oracles.py` と `eval_oracles.py` の関係や、テスト・他モジュールが eval-oracles 実装を import するための互換レイヤーを確認したいとき。
- サブコマンドから `commons.codex`、`commons.indexing`、`commons.repo`、`commons.command_runner`、`commons.timing`、`commons.timestamps` などの共通処理がどう使われるか入口を探したいとき。

## Do not read this when

- CLI エントリーポイントでサブコマンドが argparse にどう登録されるかだけを調べたいとき。
- git コマンド実行、repo root 探索、共通エラー整形、Codex CLI ラッパー、JSON パース、ログ保存、リトライ、タイムスタンプ生成、時間計測などの共通ユーティリティ実装そのものを調べたいとき。
- cmoc の正本仕様断片を調べたいとき。その場合は `oracles/INDEX.md` から必要な仕様ファイルへルーティングしてください。
- cmoc 自体の Python コーディング規約、設計規約、テスト規約、開発環境ルールを調べたいとき。
- 自動テストの具体的な実装、Fake Codex CLI、pytest fixture、期待値の詳細を調べたいとき。
- README、AGENTS、oracles、memo などの編集可否やリポジトリ運用ルールだけを確認したいとき。
- cmoc を使って開発する別リポジトリ側の `<repo-root>` oracle 内容や、ユーザー向けワークフロー説明だけを確認したいとき。
- `__pycache__` 配下の生成済み bytecode や実行時キャッシュの内容を調べたいとき。

## hash

- d709246660b6338864492c0a1249d4b1134092c14c7ac41edf65fa94cd2bf952
