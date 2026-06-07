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

- `tests/test_codex.py` は `commons.codex` の `run_codex_exec` と関連ヘルパーの回帰テスト群です。
- Structured Output の再試行、schema 検証、出力ログ、UTF-8 処理、quota/resume 復旧、workspace-write 時の oracle 保護を扱います。
- `output_schema` の生成・キャッシュ・検証や、`_extract_session_id`、`_resume_command`、`_prepare_codex_exec_paths`、通知出力も確認します。

## Read this when

- `run_codex_exec` の正常系・失敗系・再試行条件を確認したいとき。
- Structured Output の schema 検証、JSON/text validator、`output_schema` ファイルの生成・再利用を変更したいとき。
- Codex CLI 呼び出しログ、コンソール通知、`subcommand_log` への記録内容を確認したいとき。
- quota 枯渇時の poll/resume、`_extract_session_id`、`_resume_command`、workspace-write 時の oracle 保護や `skip_index_maintenance` の適用範囲を追いたいとき。

## Do not read this when

- `tests/test_indexing.py` や `tests/test_repo.py` など、別の回帰テストの内容を確認したいとき。
- `commons.indexing` や `commons.repo` の個別実装だけを追いたいとき。
- `tests/test_subcommands.py` のサブコマンド横断ロジックだけを確認したいとき。
- `commons.timestamps`、`commons.report_files`、`commons.subcommand_log` など、他の共通ヘルパーだけを確認したいとき。

## hash

- e90aca968b428cb0367e8ff89dfeb115f13e45c967bfe1a748b1c135bbb27d5e

# `test_file_naming.py`

## Summary

- `tests/test_file_naming.py` はリポジトリ構成のファイル名が命名規則に従うことを検証するテストです。
- 旧ルーティングファイルである `routing.md` と `ROUTING.md` が残存していないこと、`INDEX.md` に旧内部種別コメントが残っていないことを確認します。
- `cmoc apply/session/review` のサブコマンド本体が階層化された import 可能モジュールに置かれ、旧 flat module が残っていないことを検証します。

## Read this when

- 旧ルーティングファイルや旧 INDEX 内部コメントが残っていないことを確認したいとき。
- `src/sub_commands/apply/`、`src/sub_commands/session/`、`src/sub_commands/review/` 配下の階層化 layout を検証するテストを探したいとき。
- `apply.py`、`apply_join.py`、`session_fork.py`、`eval_oracles.py` などの旧 flat module を禁止する回帰テストを把握したいとき。
- ファイル命名規則に関する検証範囲を確認したいとき。

## Do not read this when

- cmoc のサブコマンド実装や実行フローを確認したいとき。
- `INDEX.md` 自体の生成・再利用・再生成ルールを追いたいとき。
- `tests/test_indexing.py` や `tests/test_repo.py` など、別の回帰テストの内容を確認したいとき。
- ファイルアクセス規則やリポジトリ運用ルールだけを確認したいとき。

## hash

- 19d26b700e712e55500144a00541ab4733ecc1b35d24a3d6824cf2f556aa0b33

# `test_indexing.py`

## Summary

- `tests/test_indexing.py` は `src/commons/indexing.py` の `INDEX.md` メンテナンス処理に関する回帰テスト群です。
- 生成・再利用・再生成、hash 更新、Structured Output 検証に加えて、`find_index_inconsistencies()` の検査や自動コミットまでを扱います。
- `gitignore`、symlink、binary、非 UTF-8 path、空ディレクトリ、並列処理、排他 lock の境界条件も押さえます。

## Read this when

- `maintain_indexes()` や `is_maintained_index_path()` / `is_maintained_index_path_at_commit()` の判定条件を見直したいとき。
- `INDEX.md` の生成・再利用・再生成、hash 更新、Structured Output の妥当性確認を追いたいとき。
- `gitignore`、symlink、binary、非 UTF-8 path、空ディレクトリ、並列実行、排他 lock、自動 commit の挙動を確認したいとき。
- `find_index_inconsistencies()` が不整合をどう報告するか確認したいとき。

## Do not read this when

- `src/commons/indexing.py` の実装ロジックそのものを追いたいとき。
- `INDEX.md` の正本仕様や配置ルールだけを確認したいとき。
- `tests/test_repo.py` や `tests/test_codex.py` など、別の回帰テストを確認したいとき。

## hash

- e8e359c211d7f66d45b00c9aae1817575838153a465c5c45b8e931682f50b3a8

# `test_repo.py`

## Summary

- `tests/test_repo.py` は `src/commons/repo.py` の Git 共通処理を検証する回帰テスト群の入口です。
- .cmoc の ignore 保証、repo root 検出、oracle / implementation の列挙と差分検出、コミット可否を扱います。
- session state の永続化、apply process id、cmoc 予約ブランチ判定、active session 判定の境界条件も押さえます。

## Read this when

- repo root 検出や `.cmoc` の ignore 保証、tracked `.cmoc` の untrack 挙動を確認したいとき。
- `list_oracle_files`、`list_implementation_files`、`changed_*`、`has_deleted_*` の対象判定や rename / gitignore 境界を追いたいとき。
- `commit_if_changed` や `assert_no_uncommitted_changes` のコミット・拒否条件を確認したいとき。
- session state の read / write、`active_session_ids_for_home_branch`、`is_cmoc_branch`、`is_cmoc_reserved_branch` の判定条件を確認したいとき。

## Do not read this when

- `src/commons/repo.py` の実装そのものや Git ユーティリティの内部処理だけを追いたいとき。
- cmoc の CLI サブコマンド仕様や実行フローを確認したいとき。
- INDEX.md の生成ルールや `oracles` 全体のルーティング方針だけを確認したいとき。
- `tests/test_indexing.py` など、repo 共通処理以外のテストを探しているとき。

## hash

- c7ac61b25fc3b13dfe671581444cffca27b0ec9d956e150e1a06a50fea99ec67

# `test_report_files.py`

## Summary

- `src/commons/report_files.py` の `write_timestamped_report` が、同名ファイルを上書きせず別名で保存することを検証するテストです。
- タイムスタンプ衝突時の再試行と、既存レポートの内容が保持されることを確認します。
- `make_timestamp` を差し替えて衝突条件を再現し、保存処理の境界を押さえます。

## Read this when

- `write_timestamped_report` の排他的作成や再試行の仕様を変更するとき。
- レポート保存時の上書き防止や、タイムスタンプ衝突時の回帰を確認したいとき。
- `tests/test_report_files.py` が何を守っているかを把握したいとき。

## Do not read this when

- レポート本文の構成や評価結果の意味づけを確認したいとき。
- タイムスタンプ生成そのものの仕様を確認したいとき。
- `INDEX.md` の生成ルールや、他の共通ヘルパーの仕様だけを確認したいとき。

## hash

- 5d46cca82b67cc3fea042c2120193bf0b83020a0f788966ea5aad42d0aa9d587

# `test_subcommands.py`

## Summary

- `tests/test_subcommands.py` は、cmoc のサブコマンド本体に対する横断的な回帰テスト群の入口です。
- 共通実行制御、エラーハンドリング、終了コード、タイマとログ出力をまとめて検証します。
- `init` / `session` / `apply` / `review oracles` の主要フローと、CLI 登録・補完・レポート生成の整合性も確認します。

## Read this when

- `run_command()` を中心にしたサブコマンド横断の共通制御、エラーレポート、終了コードの扱いを確認したいとき。
- `init` / `session` / `apply` / `review oracles` の主要な状態遷移、復旧、cleanup を横断的に追いたいとき。
- CLI 登録、補完委譲、起動経路、ログ出力、経過時間サマリー、Structured Output 検証の意図を把握したいとき。
- サブコマンド共通のテスト補助や、エラー文面・レポート形式の回帰をまとめて確認したいとき。

## Do not read this when

- 個別の `src/sub_commands/...` 実装の詳細や、各サブコマンドの状態遷移だけを追いたいとき。
- `cmoc init` / `session` / `apply` / `review oracles` の利用手順や引数仕様だけを確認したいとき。
- `tests/test_repo.py` や `tests/test_indexing.py` など、別の回帰テスト群を確認したいとき。

## hash

- 058d22b77c95de24602a3a7db27bc976e9c5335e0afc2d944d746dd0439f393c

# `test_timestamps.py`

## Summary

- `tests/test_timestamps.py` は `commons.timestamps.make_timestamp` と `commons.timing.format_duration` の仕様を確認するテスト群の入口です。
- タイムスタンプはローカルタイムゾーン基準で `YYYY-MM-DD_HH-MM_SS_mmmmmmmmm` 形式に整形され、ミリ秒が 9 桁ゼロ埋めになることを検証します。
- `format_duration` の固定幅表示、0.1 秒単位の切り捨て、そして同一ファイル内の補助関数が caller first, callee last で並ぶことを確認します。

## Read this when

- `commons.timestamps.make_timestamp` の出力形式や、aware / naive `datetime` の扱いを確認したいとき。
- `commons.timing.format_duration` の固定幅表示や 0.1 秒単位の切り捨てを確認したいとき。
- タイムスタンプ生成や経過時間表示の変更がこのテスト群に影響するか判断したいとき。
- 同一ファイル内の補助関数の並び順を `inspect.getsourcelines()` で検証している意図を確認したいとき。

## Do not read this when

- `commons.timestamps.make_timestamp` や `commons.timing.format_duration` 以外の CLI サブコマンド仕様を確認したいとき。
- 日時のパース、UTC 固定、その他の日時ユーティリティを探しているとき。
- `INDEX.md` の自動生成や内容ハッシュの管理方法だけを調べたいとき。
- コンソール出力、Codex CLI 呼び出し、エラー処理など別の共通実行制御を確認したいとき。

## hash

- 9a286390e49c3179f26f5f51aa6b3f21faa27a63bce0745a15a0908b98e65372
