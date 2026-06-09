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

- `tests/test_codex.py` は `commons.codex` の `run_codex_exec` と関連ヘルパーを対象にした回帰テスト群です。
- Structured Output の再試行、schema 検証、出力ログ、UTF-8 処理、quota/resume 復旧、workspace-write 時の oracle 保護をまとめて検証します。
- `_extract_session_id`、`_resume_command`、`_prepare_codex_exec_paths`、`_write_output_schema`、通知出力や index maintenance の境界も確認します。

## Read this when

- `commons.codex` の `run_codex_exec` と関連ヘルパーの回帰テスト範囲を把握したいとき。
- Structured Output の再試行、schema 検証、`output_schema` の生成・キャッシュ・修復を変更したいとき。
- 呼び出しログ、UTF-8 処理、通知出力、launch failure の正規化を確認したいとき。
- workspace-write 時の oracle 保護、`skip_index_maintenance` の適用範囲、active conflict の許可条件を確認したいとき。
- quota 検出と resume 復旧、`_extract_session_id`、`_resume_command`、`_prepare_codex_exec_paths` の仕様を確認したいとき。

## Do not read this when

- `tests/test_repo.py`、`tests/test_indexing.py`、`tests/test_subcommands` など、`commons.codex` 以外の回帰テストを確認したいとき。
- `src/commons/codex.py` の実装ロジックそのものだけを追いたいとき。
- CLI 全体のサブコマンド登録や `cmoc` の利用手順だけを確認したいとき。
- `output_schema` や workspace-write 保護の詳細ではなく、別の共通ヘルパーや別機能のテストを探したいとき。

## hash

- 206d248e8d9825570bd4c18a3f3e1d4a23a66eb5595598b9730afec1bddc009d

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

- `tests/test_indexing.py` は `src/commons/indexing.py` の `INDEX.md` メンテナンスと不整合検査の回帰テスト群です。
- `maintain_indexes` と `find_index_inconsistencies` を中心に、再生成・再利用・整合性確認の境界を押さえます。
- `.gitignore`、symlink、binary、非 UTF-8 path、並列化、自動 commit などの例外条件も網羅します。

## Read this when

- `maintain_indexes` の生成・再生成・再利用条件を確認したいとき。
- `is_maintained_index_path` / `is_maintained_index_path_at_commit` の判定規則を確認したいとき。
- `find_index_inconsistencies` の検査内容や、古い path の正規化を追いたいとき。
- gitignore、symlink、binary、空 directory、非 UTF-8 path の扱いを確認したいとき。
- 自動 commit、排他 lock、並列生成、Structured Output 検証の回帰を見たいとき。

## Do not read this when

- `src/commons/indexing.py` の実装ロジックそのものを追いたいとき。
- `cmoc indexing` の CLI 引数や本体入口だけを確認したいとき。
- `oracles/docs/app_specs/indexing.md` の正本仕様だけを確認したいとき。
- `tests/test_repo.py` や `tests/test_codex.py` など、別の回帰テストを確認したいとき。

## hash

- 05b7c7c0bfa9d174d850a41098c4dd99f48f11662f750ac4e2805696ea35229a

# `test_repo.py`

## Summary

- `tests/test_repo.py` は `src/commons/repo.py` の git 共通処理を検証する回帰テスト群の入口です。
- .cmoc の ignore 保証、repo root 検出、実装ファイルと正本ファイルの列挙・変更検出を中心に扱います。
- session state、apply process id、cmoc ブランチ判定、active session 判定の境界条件も確認します。

## Read this when

- repo root 検出や `.cmoc` の ignore 保証の挙動を確認したいとき。
- `list_oracle_files` / `list_implementation_files`、`changed_oracle_files`、`changed_implementation_files` の判定条件を調べたいとき。
- `commit_if_changed` のコミット可否や、失敗時に index と HEAD を壊さない挙動を確認したいとき。
- session state の読み書き、`active_session_ids_for_home_branch`、`is_cmoc_branch` / `is_cmoc_reserved_branch` の境界条件を確認したいとき。

## Do not read this when

- `src/commons/repo.py` の実装ロジックそのものを追いたいとき。
- 個別の git ユーティリティやヘルパー関数の使い方だけを確認したいとき。
- `tests/test_codex.py` や `tests/test_indexing.py` など、別の回帰テスト群を確認したいとき。

## hash

- 424e1cdace0552bac58b0ca8412be6a45313be1e637cad159d71ba650ccb34da

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

# `test_subcommands`

## Summary

- `tests/test_subcommands` 配下のサブコマンド横断テスト群への入口です。
- `helpers.py` と `test_core.py` が共通基盤を担い、`test_cli.py` が CLI 入口を検証します。
- `test_apply_*.py`、`test_session_*.py`、`test_review_oracles.py` が各サブコマンドの回帰テストを分担します。

## Read this when

- `tests/test_subcommands` 配下の回帰テストをどのファイルで扱っているか整理したいとき。
- CLI 入口、共通実行基盤、`apply` 系、`session` 系、`review oracles` 系のテストの入口を探したいとき。
- 共通ヘルパーの使い方や、各サブコマンドのテストがどの責務に分かれているかを確認したいとき。

## Do not read this when

- `tests/test_subcommands` 全体ではなく、`test_apply_fork.py` や `test_session_join.py` など個別ファイルだけを確認したいとき。
- `src/sub_commands/` 側の実装や `oracles/docs/app_specs/sub_commands/` 側の正本仕様だけを読みたいとき。
- CLI の利用手順や設計方針ではなく、テスト用ヘルパーや共通基盤の詳細だけを追いたいとき。

## hash

- a7f9f44c64f327ba3091902c2aa7d326511a5c31e672f1c54cca033e3782bb20

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
