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

- `tests/test_codex.py` は `commons.codex` の `run_codex_exec` と周辺ヘルパーの回帰テスト群です。
- Structured Output の再試行、schema 検証、出力ログ、コンソール通知、UTF-8 処理、quota / resume 復旧、workspace-write 時の oracle 保護を扱います。
- `output_schema` の生成・キャッシュ・検証や、セッション ID 抽出、resume コマンド生成、主要な境界条件も確認します。

## Read this when

- `run_codex_exec` の正常系・失敗系・再試行条件を確認したいとき。
- `expect_json`、`text_validator`、`json_validator`、Structured Output schema の受け渡しや検証を変更したいとき。
- `codex exec` 呼び出しログ、コンソール進捗表示、subcommand log の記録内容を確認したいとき。
- quota 枯渇時の poll / resume、capacity retry、`_extract_session_id`、`_resume_command` の挙動を追いたいとき。
- workspace-write 実行時の oracle 保護、`skip_index_maintenance`、active conflict path の判定を確認したいとき。
- `_write_output_schema` や `_prepare_codex_exec_paths` のファイル生成・再利用・排他制御を確認したいとき。

## Do not read this when

- `commons.indexing` や `tests/test_indexing.py` の INDEX 保守仕様だけを確認したいとき。
- `commons.repo` の git 共通処理、ブランチ / セッション管理、`.cmoc` の差分検査だけを追いたいとき。
- `tests/test_subcommands.py` のようなサブコマンド横断の制御フローだけを確認したいとき。
- `commons.timestamps`、`commons.report_files`、`tests/test_timestamps.py` など別の共通ヘルパーの仕様だけを確認したいとき。

## hash

- c7624c7afd39217f0d49db0361e089d497509e303e38b6a6431b2e46655f4056

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

- 9212a0b14153b59d46d1634605fe82aa95084212fd00545d88aefefcac59c1c3

# `test_indexing.py`

## Summary

- `tests/test_indexing.py` は `src/commons/indexing.py` の `INDEX.md` メンテナンス処理に関する回帰テスト群です。
- `INDEX.md` の生成・再利用・再生成条件・hash 更新・Structured Output 検証を中心に、gitignore、symlink、binary、非 UTF-8 path、並列処理、排他 lock、自動 commit の境界条件も確認します。
- `maintain_indexes` と `is_maintained_index_path` の期待動作や、I/O 失敗時の `CmocError` 化も押さえます。

## Read this when

- `maintain_indexes` と `is_maintained_index_path` の期待動作を確認したいとき。
- gitignore、symlink、binary、非 UTF-8 path、空ディレクトリ、特殊文字を含む path の扱いを修正・追加したいとき。
- 並列生成、排他 lock、Codex 呼び出しの再試行、既存 INDEX の再利用・再生成、自動 commit の境界条件を確認したいとき。

## Do not read this when

- src/commons/indexing.py の実装ロジックを直接追いたいとき。
- oracles 側の正本仕様や `INDEX.md` 全体の生成ルールだけを確認したいとき。
- session や apply など、INDEX 保守以外のサブコマンド仕様を調べたいとき。

## hash

- 9e596de407b3d4186c8509c6d5d6a306aafc3b02666024631461b1610054c110

# `test_repo.py`

## Summary

- `tests/test_repo.py` は `src/commons/repo.py` の Git 共通処理を検証する回帰テスト群です。
- .cmoc の ignore 保証、repo root 検出、実装 / 正本ファイルの列挙と変更検出を扱います。
- session state、apply process id、`cmoc` ブランチ判定、active session 判定の境界条件も押さえます。

## Read this when

- repo root 検出や `.cmoc` の ignore 保証の挙動を確認したいとき。
- `list_oracle_files` / `list_implementation_files` や変更検出系の境界条件を調べたいとき。
- `commit_if_changed` のコミット可否や、失敗時に index と HEAD を壊さない挙動を確認したいとき。
- session state の読み書き、`active_session_ids_for_home_branch`、`is_cmoc_branch` の判定条件を確認したいとき。

## Do not read this when

- `src/commons/repo.py` の実装そのものを直接追いたいとき。
- 個別の Git ユーティリティの使い方だけを確認したいとき。
- `INDEX.md` の生成ルールや `oracles` 全体のルーティング方針だけを確認したいとき。
- `session` や `apply` など、repo 共通処理以外のサブコマンド仕様を調べたいとき。

## hash

- 24637378f1f2d603615c9e1678629408a9e5f2fc77819fd347cd14fbab0d19bb

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

- `tests/test_subcommands.py` は、cmoc のサブコマンド群をまたぐ決定論的な制御ロジックを検証する pytest テストの集約です。
- `run_command` を中心に、共通エラーレポート、終了コード、経過時間集計、CLI の委譲や補完応答までをまとめて確認します。
- `init`、`session`、`apply`、`review oracles` の遷移と副作用の回帰を、個別実装ではなくサブコマンド全体の入口として押さえます。

## Read this when

- `cmoc` のサブコマンド群に対する横断的な制御ロジックのテスト範囲を把握したいとき。
- `run_command` の stdout への進捗表示、エラー報告、終了コード処理、repo ルート解決失敗時の挙動を確認したいとき。
- `init`、`session`、`apply`、`review oracles` の状態遷移、branch/worktree/STATE の整合性、Structured Output の受け渡しと検証を追いたいとき。

## Do not read this when

- `src/sub_commands/` 側の各実装や内部ヘルパーの詳細を直接追いたいとき。
- `tests/test_repo.py`、`tests/test_indexing.py`、`tests/test_timestamps.py` など、別機能の回帰テストだけを確認したいとき。
- 個別の `cmoc init`、`cmoc session`、`cmoc apply`、`cmoc review oracles` の操作手順や引数仕様だけを知りたいとき。

## hash

- ca2fff0e925bbdc40ac27631698875e5b8eefcaa58658f93c58d8d9db2231fac

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
