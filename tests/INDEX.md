# `conftest.py`

## Summary

- pytest 実行時に `<cmoc-root>/src` を Python の import path 先頭へ追加するテスト共通設定ファイルです。
- `tests` 配下のテストから cmoc 本体の `src` 配下モジュールを直接 import できるようにします。
- `Path(__file__).resolve().parents[1] / "src"` で `<cmoc-root>/src` を解決し、`sys.path.insert(0, ...)` で優先的に参照されるよう設定します。

## Read this when

- pytest で `src` 配下の cmoc 実装モジュールを import できる理由を確認したいとき。
- テスト実行時の Python import path 設定や `sys.path` の変更箇所を探しているとき。
- `tests` 配下の共通 pytest 設定が何をしているか把握したいとき。

## Do not read this when

- 個別テストケースの内容や期待値を調べたいとき。
- cmoc の CLI 挙動、サブコマンド仕様、ユーザー向け出力仕様を確認したいとき。
- pytest fixture、mock、Fake Codex CLI などの具体的なテスト補助機能を探しているとき。
- 本番コードの実装ロジックやアプリケーション設定の詳細を調べたいとき。

## hash

- 70811f2ee49ed59eeb60c3c17354146e78b9c21d8ab9bfbcb46007f9d6c8eb57

# `test_codex.py`

## Summary

- `tests/test_codex.py` は `commons.codex.run_codex_exec()` とその周辺補助処理を検証するテスト群の入口です。
- Structured Output の schema ファイル生成、JSON / text の再試行、schema 検証失敗や意味的検証失敗、`reasoning_effort` 制約を扱います。
- Codex CLI 呼び出しログ、`subcommand_log` 通知、`INDEX.md` 事前メンテナンス、`skip_index_maintenance`、workspace-write 時の `oracles` 保護を確認します。
- quota 枯渇時の待機と `resume` 再実行、`session_id` 抽出、`_resume_command`、`_prepare_codex_exec_paths` も扱います。
- 末尾には、テスト用 git repo 初期化の補助関数と、git 実行補助の関数があります。

## Read this when

- `commons.codex.run_codex_exec()` の引数組み立て、`read_only` / `workspace-write`、`--json`、`--output-schema`、`reasoning_effort` の扱いを確認したいとき。
- Structured Output の parse 失敗、JSON Schema 不一致、意味的検証失敗に対するリトライやエラー表示を追いたいとき。
- Codex CLI 呼び出しログ、`subcommand_log` 通知、出力プレビュー、quota 枯渇時の待機と `resume` 再実行の流れを確認したいとき。
- `INDEX.md` の事前メンテナンス、`skip_index_maintenance`、workspace-write 時の `oracles` 保護、`session_id` 抽出や `_resume_command` を追いたいとき。
- `_prepare_codex_exec_paths` のログ予約、Structured Output 用 schema ファイル生成、テスト用 git リポジトリ初期化の `_init_git_repo` / `_git` の役割を確認したいとき。

## Do not read this when

- `src/commons/codex.py` の実装ロジックそのものを追いたいとき。
- `tests/test_indexing.py` や `tests/test_repo.py` など、別のテスト群だけを確認したいとき。
- `INDEX.md` 全体の生成ルールや `oracles` 正本仕様だけを確認したいとき。
- `README.md`、`AGENTS.md`、`memo` の運用や編集可否だけを確認したいとき。

## hash

- 49b038d72dd1d494971024dd1afd589ab8fccb69e445f72c41bbf68200d59477

# `test_file_naming.py`

## Summary

- `tests/test_file_naming.py` はリポジトリ構成のファイル名が命名規則に従うことを検証するテストです。
- 旧ルーティングファイルである `routing.md` と `ROUTING.md` が残存していないことを確認します。
- ルート直下の案内ファイルを増やさず、現行のルーティング入口を `INDEX.md` 群へ統合していることを検証します。

## Read this when

- リポジトリ直下に旧ルーティングファイルが残っていないことを確認したいとき。
- `routing.md` と `ROUTING.md` の不存在をテスト観点から確認したいとき。
- ルーティング入口を `INDEX.md` 群へ一本化する方針の回帰テストを探すとき。

## Do not read this when

- cmoc のサブコマンド仕様や Codex CLI 連携の挙動を確認したいとき。
- Python 実装規約、INDEX.md メンテナンス、git 共通処理など別機能のテストを探しているとき。
- README、AGENTS、oracles、memo などの編集可否やファイルアクセス規則だけを確認したいとき。

## hash

- 8cffbbd037cfef7eddae93b596fc8e14a5e496a69ec1a9cc344e42ba99a22f43

# `test_indexing.py`

## Summary

- `commons.indexing.maintain_indexes` の回帰テスト群です。
- `INDEX.md` の対象判定、再生成、既存目次の再利用、自動コミットまでを検証します。
- ロック直列化や、gitignore・symlink・非 UTF-8・バイナリ・空ディレクトリの扱いも含みます。

## Read this when

- `INDEX.md` の生成対象や除外条件を見直したいとき。
- `maintain_indexes` の再生成条件、hash 更新、既存 entry の再利用条件を確認したいとき。
- 自動コミットや `_locked_index_maintenance` の並列実行制御を追いたいとき。
- 特殊ファイル名や非 UTF-8 path、Markdown 境界を含む入力の扱いを確認したいとき。

## Do not read this when

- `src/commons/indexing.py` の実装ロジックだけを追いたいとき。
- `tests/test_codex.py` や `tests/test_repo.py` など別のテスト群だけを見たいとき。
- `INDEX.md` の正本仕様そのものや、`oracles` 配下のルーティングを確認したいとき。

## hash

- 7ae0a4d7ff147f6589f8c8c7b157a5081a065ae08d8fa4a219d87284fc1b375c

# `test_repo.py`

## Summary

- `tests/test_repo.py` は `commons.repo` の git リポジトリ共通処理を検証するテスト群の入口です。
- .cmoc の ignore 保証、ファイル列挙、差分検出、削除検出、session state の読み書きと検証を扱います。
- 末尾に、テスト用 git リポジトリを初期化する `_init_repo` と、git コマンド実行補助の `_git` があります。

## Read this when

- `tests/test_repo.py` が `commons.repo` のどの機能を検証しているか確認したいとき。
- `.cmoc` の ignore 保証、tracked な `.cmoc` の untrack、`find_repo_root`、`is_cmoc_branch` を見直したいとき。
- `list_oracle_files` / `list_implementation_files`、`changed_*`、`has_deleted_*` の除外条件や変更検出条件を確認したいとき。
- session state の読み書き、`active_session_ids_for_home_branch`、`read_session_start_commit`、`session_state_root` の前提条件を把握したいとき。
- テスト用 git リポジトリの初期化や `_init_repo` / `_git` の役割を確認したいとき。

## Do not read this when

- `src/commons/repo.py` の実装ロジックそのものを追いたいとき。
- `tests/test_codex.py`、`tests/test_indexing.py`、`tests/test_subcommands.py` など、別のテスト群だけを確認したいとき。
- `INDEX.md` 全体の生成ルールや `oracles` 正本仕様だけを確認したいとき。

## hash

- 8d1f22a8a3c87544abffb708919bf39fd2c185c9b25dfe76b1da52110c40fcaa

# `test_subcommands.py`

## Summary

- `tests/test_subcommands.py` は cmoc のサブコマンド全体にまたがる決定論的な制御ロジックを検証するテスト群の入口です。
- 共通 runner のログ・終了コード・エラー報告、`init` / `session` / `apply` / `review oracles` の実行と保護条件、CLI 登録とヘルプ表示を扱います。
- 各サブコマンドの prompt、payload 検証、worktree・session state・branch 取り扱い、`bin/cmoc` の起動条件まで含めて回帰確認するための目次です。

## Read this when

- cmoc の主要サブコマンド入口、`run_command`、`StepTimer`、`start_step`、`format_error_report` の制御と出力を確認したいとき。
- `init`、`session`、`apply`、`review oracles` の状態遷移、例外処理、CLI 登録、ヘルプ表示を広く回帰確認したいとき。
- `bin/cmoc` ランチャー、共通エラーレポート、prompt 文、Structured Output の検証、`eval-oracles` / `apply` の主要な検証ロジックをまとめてたどりたいとき。

## Do not read this when

- `src/sub_commands/*` の個別実装だけを追いたいとき。
- `commons.repo` や `commons.indexing` など、サブコマンド以外の共通処理だけを確認したいとき。
- `tests/test_codex.py`、`tests/test_indexing.py`、`tests/test_repo.py` など別のテスト群だけを見たいとき。

## hash

- 1b9cca145a4bafef381a2218d55fd75ad52f6f72510f89d90b66d44a68e0f080

# `test_timestamps.py`

## Summary

- `tests/test_timestamps.py` は `commons.timestamps.make_timestamp` と `commons.timing.format_duration` の仕様を確認するテスト群の入口です。
- タイムスタンプはローカルタイムゾーン基準で `YYYY-MM-DD_HH-MM_SS_mmmmmmmmm` 形式に整形されることを検証します。
- `format_duration` の固定幅表示、0.1 秒単位の切り捨て、そして同一ファイル内の補助関数が caller first, callee last で並ぶことを確認します。

## Read this when

- `commons.timestamps.make_timestamp` の出力形式や、aware / naive `datetime` の扱いを確認したいとき。
- `commons.timing.format_duration` の固定幅表示や 0.1 秒単位の切り捨てを確認したいとき。
- タイムスタンプ生成や経過時間表示の変更がこのテスト群に影響するか判断したいとき。
- 同一ファイル内の補助関数の並び順を `inspect.getsourcelines()` で検証している意図を確認したいとき。

## Do not read this when

- タイムスタンプや経過時間表示とは関係のない CLI サブコマンドの仕様を確認したいとき。
- 日時のパース、UTC 固定、その他の日時ユーティリティを探しているとき。
- Codex CLI 呼び出し、ログ保存、`INDEX.md` 自動生成など別の共通仕様を調べたいとき。
- このテスト群以外の `tests` 配置や別ファイルの順序検証だけを確認したいとき。

## hash

- 90f4f5d595174be36883a3057c9ce8cccea795151a6ab18194478795325fdd5c
