# `__init__.py`

## Summary

- Declares the src.commons package with a short module docstring.
- Contains no imports, exports, runtime logic, constants, or public API definitions.

## Read this when

- You need to confirm that src.commons is a Python package.
- You are documenting or routing the commons package at a package-level overview.

## Do not read this when

- You need implementation details for shared utilities; inspect the concrete modules under src/commons instead.
- You are looking for command behavior, workflow logic, configuration handling, or tests.

## hash

- ff1b23adb7b4c5a75686ac97283d2065d5cacc8861143f25677b559abeb6e2d0

# `codex.py`

## Summary

- Codex CLI の共通実行処理をまとめたモジュールで、`codex exec` のコマンド組み立て、`--output-last-message` の付与、実行ログ保存、`resume` 再開を扱う。
- Structured Output 用の `--output-schema` ファイル生成と再利用、JSON の解析、JSON Schema 検証、呼び出し結果の意味検査を含む。
- quota 枯渇時のポーリング待機、capacity 一時失敗の指数バックオフ再試行、workspace-write 時の `oracles` 変更検査、`INDEX.md` 事前メンテナンスも実装されている。

## Read this when

- Codex CLI 呼び出しの共通処理や、`read_only` / `workspace-write` の切り替えを確認したいとき。
- Structured Output の schema ファイル生成、JSON 解析、JSON Schema 検証、出力の意味検査を見直したいとき。
- quota 待機と `resume` 再開、capacity 一時失敗の指数バックオフ再試行、失敗時の診断情報を追いたいとき。
- workspace-write 実行時の `oracles` 保護、実行前の `INDEX.md` メンテナンス、呼び出しログの保存方法を確認したいとき。

## Do not read this when

- `codex exec` の基本的な使い方や個別オプションの詳細だけを確認したいとき。
- `INDEX.md` の生成・維持ルールそのものを確認したいとき。
- `repo.py`、`errors.py`、`indexing.py` など別の共通モジュールだけを追いたいとき。
- 個別サブコマンドの業務ロジックや CLI 引数定義だけを確認したいとき。

## hash

- 1cfa78a615b23e96da3d8f81828013a41d2347c31f2dbc6053602ba123e0a219

# `command_runner.py`

## Summary

- Typer から呼ばれるサブコマンド共通の実行ラッパーで、`<repo-root>` の解決、`subcommand_log` の開始、例外の変換、終了コード決定をまとめています。
- 通常のサブコマンド本体は `Path` を受け取り、`subcommand_log` と `timing` と連携して実行結果を集約します。
- `typer.Exit` と通常例外を分けて扱い、必要に応じて `CmocError` と `format_error_report()` で利用者向けのエラー表示を行います。
- 終了時には `log_event()`、`report_current_timer()`、`format_duration()`、`clear_current_timer()` を使って完了レポートを出します。

## Read this when

- サブコマンドの入口をどこに集約し、共通の実行制御をどう掛けているか確認したいとき。
- 各サブコマンドが `<repo-root>` の `Path` をどう受け取るか確認したいとき。
- 例外時のエラー表示、終了コード、`typer.Exit` への変換規則を見直したいとき。
- 実行ログ、経過時間、待機時間、戻り値の集計出力の流れを追いたいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや CLI 引数定義だけを確認したいとき。
- `<repo-root>` 探索や `.cmoc` の扱いの詳細を追いたいときは、`repo.py` を読むべきです。
- エラーメッセージ本文の整形や共通例外の定義そのものを確認したいときは、`errors.py` を読むべきです。
- サブコマンドログやタイミング計測の実装だけを調べたいときは、`subcommand_log.py` と `timing.py` を直接読むべきです。
- Codex CLI 呼び出し、Structured Output、`INDEX.md` 生成など別機能を調べたいとき。

## hash

- 5464d0e62e6d10ccdc888415490d0ead1a958e3da4dddf0c0cb337fb61b09a09

# `errors.py`

## Summary

- `src/commons/errors.py` は、cmoc 全体で使う共通例外 `CmocError` と、stdout 向けのエラーレポート整形関数 `format_error_report` をまとめるモジュールです。
- `CmocError` は利用者向けメッセージ、複数の次アクション、詳細、終了コードを保持し、次アクションは最低 2 件を必須にします。
- `format_error_report` は `ERROR` / `Summary` / `Next actions` / `Detail` / `Call stack` 形式で例外を整形し、`CmocError` と通常例外を分けて扱います。

## Read this when

- cmoc の共通エラーハンドリングや、例外から stdout 向けレポートへ変換する処理を実装・修正したいとき。
- 復旧手順を複数提示する `CmocError` をサブコマンドや共通処理から投げたいとき。
- `message`、`actions`、`detail`、`exit_code` の意味や制約を確認したいとき。
- 通常の Python 例外が cmoc の共通エラーレポートでどう表示されるか確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジック、引数解析、git 操作、`codex exec` 呼び出しを確認したいときは、このモジュールではなく該当するサブコマンドや共通処理を読むべきです。
- ログ保存、リトライ、Structured Output、サンドボックス指定など、`format_error_report` とは別の共通機能だけを確認したいときは、このファイルの範囲外です。
- タイムスタンプ生成、経過時間表示、サブコマンドログなど、他の共通ユーティリティを調べたいときは `src/commons/errors.py` ではありません。
- テスト実装の詳細や Fake Codex CLI の使い方だけを確認したいときは、このモジュールを読む必要はありません。

## hash

- a72dbd1205ce53b398ceacaaf86e966b9aba8f03be9634806f0d94a73e4717ea

# `indexing.py`

## Summary

- `INDEX.md` の生成・維持処理を担うモジュールです。
- リポジトリ配下を走査して、`.gitignore`、`.git/info/exclude`、`memo`、`build` / `tmp`、dotfile、symlink、バイナリ、既存 `INDEX.md` などを除外しながら目次対象を決めます。
- 既存の `INDEX.md` ブロックを解析し、ハッシュと形式が一致する場合は再利用し、崩れている場合は再生成します。
- Structured Output の schema 検証、生成プロンプトの組み立て、Markdown 変換、gitignore 判定補助、自動コミットの流れを含みます。

## Read this when

- `INDEX.md` の自動生成・更新ロジックを実装または修正したいとき。
- 直下項目の列挙条件、除外条件、再利用条件、ハッシュ更新判定を確認したいとき。
- Structured Output の schema 検証、Codex 生成プロンプト、Markdown 変換、gitignore やバイナリ判定の補助処理を追いたいとき。
- `INDEX.md` 差分だけを自動コミットする流れや、更新対象範囲の決め方を見直したいとき。

## Do not read this when

- `codex exec` の起動方法や `--output-schema` の一般的な使い方だけを確認したいとき。
- 共通エラーハンドリングやサブコマンド実行制御だけを確認したいとき。
- `INDEX.md` の正本仕様そのものを確認したいときは、このモジュールではなく対応する `oracles` 側を読むべきです。
- `repo.py` や `errors.py` など別の共通モジュールだけを追いたいとき。

## hash

- 7b01aac47ce43ef06d2df987fedea589cf3fdb65eceb033c028d892fdb56f87f

# `repo.py`

## Summary

- `git` リポジトリと cmoc 作業ディレクトリの共通処理をまとめたモジュールです。
- repo root 探索、branch 判定、session id 抽出、apply worktree パス復元、session state の保存・読込・検証を扱います。
- `.cmoc` の ignore 保証、未コミット差分の検査、pathspec commit、`oracles` / 実装ファイルの列挙と変更・削除検出、root `.gitignore` の評価補助も含みます。

## Read this when

- git リポジトリルート探索、現在ブランチ、HEAD、`cmoc/session/...` と `cmoc/apply/...` の branch 判定を確認したいとき。
- session state JSON の保存・読込・固定スキーマ検証、active session の列挙を確認したいとき。
- `.cmoc` を追跡対象外に保つ保証、未コミット差分の検査、`cmoc init` 向けの差分分離と commit ロジックを追いたいとき。
- `oracles` と実装ファイルの列挙、変更検出、削除検出、root `.gitignore` の評価方法を確認したいとき。

## Do not read this when

- `cmoc` の個別サブコマンドの引数や実行手順だけを確認したいとき。
- `src/commons/errors.py` や `src/commons/indexing.py` など、別の共通モジュールだけを確認したいとき。
- `.cmoc` の追跡対象外保証や git 操作の細部ではなく、CLI 仕様やワークフロー仕様だけを追いたいとき。

## hash

- dce7e13310d8af71646d9631b03abf3a394a80a8a57760634dd6b8a91db7516f

# `subcommand_log.py`

## Summary

- サブコマンド呼び出し単位の JSON Lines ログを管理する共通処理への入口です。
- ログ状態の保持、イベント追記、quota 待ち時間の加算、現在のログコンテキスト取得をまとめます。
- ログファイルの作成先を `repo root` 側に寄せつつ、worktree 配下に出力しないための判定と `git info/exclude` 更新も扱います。

## Read this when

- サブコマンド呼び出し単位の JSON Lines ログをどこにどう作るか確認したいとき。
- 現在実行中のサブコマンドログ状態を `ContextVar` で保持し、イベントを追記する実装を確認したいとき。
- `.cmoc/logs/sub_commands/<time-stamp>.jsonl` の作成、排他生成、即時 flush、ログ追記の流れを実装・修正・レビューしたいとき。
- `.cmoc/logs/` を git の未コミット差分にしないための `info/exclude` 更新や、worktree での保存先切り替えを確認したいとき。

## Do not read this when

- 個別サブコマンドの引数や状態遷移だけを確認したいときは、この共通ログ処理ではなく該当サブコマンドの仕様を読むべきです。
- `cmoc` のコンソール表示フォーマットだけを確認したいときは、`console_and_file_log.md` を先に読むべきです。
- `codex exec` の呼び出し方や quota 待ちの共通規約だけを確認したいときは、`codex_call.md` を読むべきです。
- `.cmoc` の配置や `INDEX.md` の生成ルールそのものを確認したいときは、このファイルではなく `misc_specs.md` や `indexing.md` を読むべきです。

## hash

- c5363a43ba379d9f913aed453f9a6588296f5b5a2f6d9aa207ef4687eb837977

# `timestamps.py`

## Summary

- `cmoc` 仕様で使う `<time-stamp>` 文字列を生成する共通モジュールです。
- `make_timestamp(now: datetime | None = None) -> str` は、指定された `datetime` または現在のローカル時刻からタイムスタンプを作ります。
- aware な `datetime` はローカルタイムゾーンへ変換し、naive な `datetime` はローカル時刻として扱います。
- 出力形式は `YYYY-MM-DD_HH-MM_SS_mmm` で、年月日時分秒はゼロ埋めし、ミリ秒は `microsecond // 1000` を 3 桁で表現します。

## Read this when

- `<time-stamp>` の文字列生成ルールを確認したいとき。
- ローカル時刻と aware / naive `datetime` の扱いを確認したいとき。
- ログ名やファイル名に使う時刻文字列の生成実装や、そのテストを書きたいとき。

## Do not read this when

- cmoc のサブコマンドごとのタイムスタンプ利用箇所や保存先仕様を調べたいとき。
- 日時のパース、UTC 固定、その他の日時ユーティリティを探しているとき。
- `INDEX.md` の自動生成や内容ハッシュの管理方法だけを調べたいとき。
- コンソール出力、Codex CLI 呼び出し、エラー処理など別の共通実行制御を確認したいとき。

## hash

- bf17be3874ec3ab0c88d7652c9869ca7c9b7b5554037dbc60f26117a2287a391

# `timing.py`

## Summary

- サブコマンド実行中のステップ単位の経過時間を管理し、最後に stdout へ集計表示する共通モジュールです。
- `StepTimer` は開始時刻、現在ステップ、確定済みの各ステップ時間を保持し、`start()` と `finish_current()` で計測区間を区切ります。
- `start_step()` は flat / hierarchical なステップ番号を整形して `step_start` ログと stdout の開始通知を出します。
- `current_timer()`、`report_current_timer()`、`clear_current_timer()` は `ContextVar` 上の現在の計測器を取得・出力・解除します。
- `format_duration()` は秒数を 0.1 秒単位で切り捨て、負値を 0 として固定幅の経過時間文字列に整形します。

## Read this when

- サブコマンドのステップ別の経過時間表示や、完了時の総経過時間表示を実装・修正したいとき。
- `StepTimer` の状態遷移や、`start()`、`finish_current()`、`report()` の関係を確認したいとき。
- 階層化されたステップ番号を含む開始通知の表示形式を確認したいとき。
- 現在の計測器を `ContextVar` 経由で参照・出力・解除したいとき。
- 経過時間の表示フォーマットや、0.1 秒単位への切り捨て、負値の扱いを確認したいとき。

## Do not read this when

- 各サブコマンドの業務ロジックや引数解析だけを確認したいとき。
- ログ保存、`subcommand_log`、`repo` 探索など、経過時間計測以外の共通処理を調べたいとき。
- `INDEX.md` の自動生成や内容ハッシュの規則だけを確認したいとき。
- Python の一般的な時間計測 API や `perf_counter` の詳細だけを知りたいとき。

## hash

- 2dc577ed39e2040ba837ec032afb14e81fd0313520c6969249125b3f858884ea
