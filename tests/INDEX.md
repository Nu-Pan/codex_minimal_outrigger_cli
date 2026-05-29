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

- `commons.indexing` の `INDEX.md` 生成・更新処理を検証する pytest 集です。
- gitignore、除外ディレクトリ、symlink、バイナリ、非 UTF-8 path、特殊文字、空ディレクトリ、既存 INDEX の再利用と再生成を網羅します。
- 目次生成の Structured Output 検証、並列化、ロック、自動コミット、既存差分の扱いも確認します。

## Read this when

- `commons.indexing` の対象選別ルールや `INDEX.md` 更新ロジックを変更するとき。
- `INDEX.md` の自動コミット、差分ステージング、ロック制御、並列実行を修正するとき。
- gitignore、symlink、非 UTF-8 path、バイナリ判定、特殊ファイルの扱いを確認したいとき。
- Structured Output の schema 検証や再生成条件を変えるとき。

## Do not read this when

- `cmoc` のサブコマンド仕様や利用手順だけを確認したいとき。
- `INDEX.md` の記述内容そのものを人手で書き換えるだけで、メンテナンス処理を触らないとき。
- `commons.indexing` 以外の CLI 実装や別機能のテストを探しているとき。

## hash

- acb4220d9c04b79edbb31ac5f8d3d8b9a284a87bfd63c5f58300ad166be9f7f3

# `test_repo.py`

## Summary

- git リポジトリ共通処理に対する pytest テスト群です。
- repo root の探索、`.cmoc` ignore の補修と検証、oracle/implementation ファイルの列挙、変更・削除の検出、session/apply state の永続化と読込検証を扱います。
- 特殊なパス文字列や gitignore の細かな解釈、schema 不一致や UTF-8 decode failure などの境界条件も含みます。

## Read this when

- `commons.repo` の git リポジトリ共通処理を変更するとき
- repo root 検出、`.cmoc` ignore、oracle/implementation ファイル列挙、変更検出、削除検出の挙動を確認したいとき
- session state や apply process id の読み書き、形式検証、エラーハンドリングの期待値を確認したいとき

## Do not read this when

- cmoc の個別サブコマンドの仕様や CLI 全体の使い方だけを確認したいとき
- `commons.repo` とは無関係な機能や、git 状態判定以外の実装を調べたいとき
- `oracles` の正本仕様や `INDEX.md` 生成ルールそのものを確認したいとき

## hash

- 67dd838f700a5a315b07af2b272d4efd7c23a40d48885bd692757b263627ba56

# `test_subcommands.py`

## Summary

- `tests/test_subcommands.py` は、cmoc の主要サブコマンドと CLI 入口の決定論的な制御ロジックを検証するテスト群の目次です。
- `run_command` のログ出力、終了コード、例外時レポート、`repo_root` 解決失敗時の扱いを確認します。
- `init`、`session`、`apply`、`review oracles`、`eval_oracles` の各コマンド登録とヘルプ表示を回帰確認します。
- conflict marker の判定、補助関数の配置順、`bin/cmoc` ランチャーの挙動も含みます。

## Read this when

- cmoc の主要サブコマンド入口と `main.py` から各実装への委譲関係を確認したいとき。
- `run_command`、`StepTimer`、`start_step`、`format_error_report` のログ出力や終了集計を追いたいとき。
- `init`、`session`、`apply`、`review oracles`、`eval_oracles` の登録・ヘルプ表示・例外処理を広く回帰確認したいとき。
- conflict marker 判定や `bin/cmoc` ランチャーの挙動を確認したいとき。
- テスト内の補助関数の並び順や、共通のテスト前提を確認したいとき。

## Do not read this when

- `src/sub_commands/apply/*`、`src/sub_commands/session/*`、`src/sub_commands/init.py` など、個別サブコマンド実装の詳細だけを確認したいとき。
- `commons.repo` や `commons.indexing` など、サブコマンド共通処理の別領域を確認したいとき。
- `tests/test_codex.py`、`tests/test_indexing.py`、`tests/test_repo.py` など、別のテスト群だけを追いたいとき。
- `oracles` 配下の正本仕様や `INDEX.md` の生成ルールそのものを確認したいとき。

## hash

- 467aaba954a0e7c1c5a5a22ba7bb08b61df23f89fd540f142d504ad6e9802c13

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
