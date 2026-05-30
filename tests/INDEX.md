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

- `commons.codex` の `run_codex_exec` と周辺ヘルパーの回帰テストをまとめたファイルです。
- Structured Output の schema 準備、JSON / text 検証、semantic validation による retry、quota 復旧後の `resume` を検証します。
- `output_schema` のキャッシュ、呼び出しログ、コンソール出力、`INDEX.md` 保守、oracle 変更検知、HEAD / reflog / commit range の境界条件を押さえます。

## Read this when

- `run_codex_exec` の呼び出し条件、戻り値、例外、再試行、`resume` の挙動を確認したいとき。
- Structured Output の schema 準備、JSON / text 検証、semantic validation、`output_schema` キャッシュを確認したいとき。
- Codex CLI の呼び出しログ、コンソール通知、`last_message`、`subcommand_log` の整合性を確認したいとき。
- workspace-write 時の `INDEX.md` 保守、oracle 変更検知、HEAD / reflog / commit range の境界条件を確認したいとき。
- `_extract_session_id`、`_resume_command`、`_active_allowed_oracle_conflict_paths` など周辺ヘルパーの仕様を確認したいとき。

## Do not read this when

- `commons.codex` の実装本体を直接追いたいとき。
- `tests/test_repo.py` や `tests/test_indexing.py` など、`test_codex.py` 以外の回帰テストだけを見たいとき。
- `INDEX.md` の生成ルールや `oracles` 全体の正本仕様だけを確認したいとき。
- `session` や `apply` など、Codex 呼び出し以外のサブコマンド仕様を探しているとき。

## hash

- 50b52d84a2a8135e58f9c7ac0a99a94a4d57d55de52a36ec2030e017d9d2fd10
<!-- cmoc-index-kind: file -->

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

- `tests/test_indexing.py` は `INDEX.md` メンテナンス処理の回帰テスト集です。
- 目次エントリの生成・再利用・再生成条件と、ハッシュ更新や Structured Output の検証を扱います。
- gitignore、symlink、binary、非 UTF-8 path、並列処理、排他 lock、自動 commit まで広く押さえます。

## Read this when

- `maintain_indexes` と `is_maintained_index_path` の期待動作を確認したいとき。
- `INDEX.md` の生成・再利用・再生成条件や、特殊な path の扱いを調べたいとき。
- 並列実行、排他 lock、自動 commit、gitignore、symlink、binary、非 UTF-8 path の回帰を修正・追加したいとき。

## Do not read this when

- `commons.indexing` の実装本体だけを確認したいとき。
- `INDEX.md` の生成ルール全体や `oracles` 側の正本仕様だけを確認したいとき。
- `session` や `apply` など、INDEX 以外のサブコマンド仕様を探しているとき。

## hash

- 4d936a8e2e426e8baa0f54da57d3acbbfb03995e9165a79fb124bd8086fb2c5d
<!-- cmoc-index-kind: file -->

# `test_repo.py`

## Summary

- `src/commons/repo.py` の git 共通処理を検証する回帰テスト群です。
- repo root 検出、`.cmoc` の ignore 保証、oracle/実装ファイルの列挙・変更・削除判定、`commit_if_changed` を扱います。
- session state、apply process id、`cmoc` ブランチ判定、active session 判定の境界条件も押さえます。

## Read this when

- repo root 検出や `.cmoc` の ignore 保証、変更ファイル列挙の仕様を確認したいとき。
- `.gitignore`、`oracles`、`memo`、`INDEX.md` の除外・対象判定を確認したいとき。
- `changed_oracle_files`、`changed_implementation_files`、削除検出、`commit_if_changed` の境界条件を見たいとき。
- session state、apply process id、`cmoc` ブランチ判定、active session 判定の期待動作を確認したいとき。

## Do not read this when

- `src/commons/repo.py` の実装ロジックそのものを確認したいとき。
- 個別関数だけを探していて、git 共通処理全体の回帰範囲は不要なとき。
- `oracles` や session state の正本仕様だけを読みたいとき。

## hash

- 2980ec95cd73033f16d553d806e5f66e531b37088e31119832b9ec26af8d2d65
<!-- cmoc-index-kind: file -->

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

- `tests/test_subcommands.py` は、cmoc のサブコマンド群に関する決定論的な制御ロジックの回帰テストをまとめた入口です。
- init、session、apply、review oracles、main、CLI エントリポイント、ヘルプ登録、エラー整形、共通 runner を広く検証します。
- 状態遷移、レポート保存、prompt / validation ヘルパー、`bin/cmoc` を含む周辺制御まで押さえるため、サブコマンド全体の挙動を俯瞰するときの目次です。

## Read this when

- `tests/test_subcommands.py` がどのサブコマンド群と CLI 入口を守っているか確認したいとき。
- `run_command`、`cmoc_init_impl`、`cmoc_session_*`、`cmoc_apply_*`、`cmoc_eval_oracles_impl` の回帰観点を整理したいとき。
- CLI のヘルプ登録、エラー整形、レポート生成、状態遷移、`bin/cmoc` の挙動をテスト観点から追いたいとき。
- prompt 生成や validation ヘルパー、Fake Codex CLI を使う評価系テストの意図を確認したいとき。

## Do not read this when

- `src/sub_commands` 配下の実装ロジックそのものを追いたいとき。
- `oracles` 配下の正本仕様だけを確認したいとき。
- 個別サブコマンドの引数や利用手順だけを確認したくて、テスト観点が不要なとき。
- `INDEX.md` の生成ルールや内容ハッシュの扱いだけを確認したいとき。

## hash

- 613e129440735aaaa4e700fb212d7184e24d9bc48632100779a338d803f3b8a8
<!-- cmoc-index-kind: file -->

# `test_timestamps.py`

## Summary

- `tests/test_timestamps.py` は `commons.timestamps.make_timestamp` と `commons.timing.format_duration` の仕様を確認するテスト群の入口です。
- タイムスタンプはローカルタイムゾーン基準で `YYYY-MM-DD_HH-MM_SS_mmm` 形式に整形されることを検証します。
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

- 11dd52f0ae222154a626c7567449aff80b4ca53d28ed40f54116c98cd70908ed
