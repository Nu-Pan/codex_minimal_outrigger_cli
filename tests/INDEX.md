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
- 目次エントリの生成・再利用・再生成条件、hash 更新、Structured Output の検証を扱います。
- gitignore、symlink、binary、非 UTF-8 path、並列処理、排他 lock、自動 commit まで広く押さえます。

## Read this when

- `maintain_indexes` と `is_maintained_index_path` の期待動作を確認したいとき。
- gitignore、symlink、binary、非 UTF-8 path、空ディレクトリ、特殊文字を含む path の扱いを修正・追加したいとき。
- 並列生成、排他 lock、Codex 呼び出しの再試行、既存 INDEX の再利用・再生成、自動 commit の境界条件を確認したいとき。

## Do not read this when

- `commons.indexing` の実装ロジックをそのまま追いたいだけのとき。
- `oracles` 側の正本仕様や、`INDEX.md` 全体の生成ルールだけを確認したいとき。
- `session` や `apply` など、INDEX 保守以外のサブコマンド仕様を調べたいとき。

## hash

- ca92d4f8ae0ab1ad5af06b24e2cd6de771974db09db746d149e01205831dcabe
<!-- cmoc-index-kind: file -->

# `test_repo.py`

## Summary

- `src/commons/repo.py` の git 共通処理を検証する回帰テスト群です。
- .cmoc の ignore 保証、実装/正本ファイルの列挙、変更・削除判定、`commit_if_changed` を扱います。
- session state、apply process id、`cmoc` ブランチ判定、active session 判定の境界条件も押さえます。

## Read this when

- repo root 検出、`.cmoc` の ignore 保証、`list_implementation_files` / `list_oracle_files` の対象判定を確認したいとき。
- `changed_paths`、`changed_oracle_files`、`changed_implementation_files`、削除検出の境界条件を調べたいとき。
- `commit_if_changed` のコミット可否や、失敗時に index と HEAD を壊さない挙動を確認したいとき。
- session state の読み書き、`active_session_ids_for_home_branch`、`is_cmoc_branch` の判定条件を確認したいとき。
- `.gitignore`、`.git/info/exclude`、`INDEX.md`、`memo` の除外・対象判定の回帰を修正するとき。

## Do not read this when

- `src/commons/repo.py` の実装そのものを追いたいとき。
- 個別の git ユーティリティや関数単体の使い方だけを確認したいとき。
- `INDEX.md` の生成ルールや `oracles` 全体のルーティング方針だけを知りたいとき。
- `session` や `apply` など、repo 共通処理以外のサブコマンド仕様を調べたいとき。

## hash

- ee93caa9fc7de7dcf4d27b077ca5e70b29e9dc4bfb7ae2233dd83bb417be535d

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

- サブコマンド本体と CLI 入口の決定論的な回帰テストを集めたファイルです。
- `init`、`session`、`apply`、`review oracles`、`main`、`bin/cmoc`、エラー整形と共通 runner の挙動を横断して検証します。
- 状態遷移、レポート生成、prompt/validation ヘルパー、Fake Codex CLI を使う評価系テストまで含みます。

## Read this when

- 公開 CLI の登録内容やヘルプ、サブコマンドの接続関係を確認したいとき。
- `run_command`、`cmoc_init_impl`、`cmoc_session_*`、`cmoc_apply_*`、`cmoc_eval_oracles_impl` の回帰観点を追いたいとき。
- エラー整形、`bin/cmoc` の起動条件、補完プローブ、レポート出力、状態遷移のテスト意図を把握したいとき。
- prompt 生成や validation ヘルパー、Fake Codex CLI を使う評価系テストの役割を確認したいとき。

## Do not read this when

- `src/sub_commands` や `src/commons` の実装ロジックそのものを追いたいとき。
- `oracles` 配下の正本仕様だけを確認したいとき。
- 個別サブコマンドの利用手順や引数仕様だけが必要で、テスト観点が不要なとき。
- `INDEX.md` の生成ルールや内容ハッシュの扱いだけを確認したいとき。

## hash

- 6e56547ce991c020e8cdcbb19d80e93d034699541721eca84d2de8a16ead5927
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
