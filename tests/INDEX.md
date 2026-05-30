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

- `tests/test_codex.py` は、Codex CLI 呼び出しラッパー `run_codex_exec` の挙動を、正常系から異常系まで広く検証するテスト群です。
- Structured Output のスキーマ検証、JSON / テキストの意味的 validation、quota や capacity の再試行、`resume` を含む復旧フロー、ログ出力を重点的に確認します。
- あわせて、workspace-write 時の oracle 変更ガード、`subcommand_log` 連携、session id 抽出、`skip_index_maintenance` の使用範囲も検証します。

## Read this when

- `run_codex_exec` の起動前チェック、失敗時診断、再試行、再開処理を変更するとき。
- Structured Output の `output_schema`、JSON/テキストの意味的検証、validator の扱いを変えるとき。
- quota や capacity の検知、待機、`resume` への切り替え条件を調整するとき。
- workspace-write 時の oracle 保護、未コミット差分の検出、`skip_index_maintenance` の前提を変えるとき。
- call log、subcommand log、コンソール通知の出力形式や内容を変えるとき。
- `_extract_session_id` や `_resume_command` の resume まわりのロジックを変えるとき。

## Do not read this when

- `commons.codex` の実装仕様そのものだけを確認したいとき。
- `subcommand_log` や `commons.indexing` の単体仕様だけを確認したいとき。
- `oracles` 配下の個別仕様やファイル生成ルールだけを確認したいとき。
- このテスト群ではなく、特定の実装ファイルや別のテストだけを見れば足りるとき。

## hash

- 5c177f32272e25df3ac2f00e175cf157ed70d19402d5416527dcc012f399168e
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

- 7abe9ede601af68a8a246e895f9952a426868048a3a0c12aacf939b4ab8e8c50

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

# `test_repo.py`

## Summary

- `src/commons/repo.py` の git 共通処理を検証する回帰テスト群です。
- repo root 検出、`.cmoc` の ignore 保証、実装/正本ファイルの列挙と変更検出を扱います。
- session state、apply process id、`cmoc` ブランチ判定、active session 判定の境界条件も押さえます。

## Read this when

- repo root 検出、`.cmoc` の ignore 保証、`list_implementation_files` / `list_oracle_files` の対象判定を確認したいとき。
- `changed_paths`、`changed_oracle_files`、`changed_implementation_files`、削除検出の境界条件を調べたいとき。
- `commit_if_changed` のコミット可否や、失敗時に index と HEAD を壊さない挙動を確認したいとき。
- session state の読み書き、`active_session_ids_for_home_branch`、`is_cmoc_branch` の判定条件を確認したいとき。
- .gitignore、`.git/info/exclude`、`INDEX.md`、`memo` の除外・対象判定の回帰を修正するとき。

## Do not read this when

- `src/commons/repo.py` の実装そのものを追いたいとき。
- 個別の git ユーティリティや関数単体の使い方だけを確認したいとき。
- `INDEX.md` の生成ルールや `oracles` 全体のルーティング方針だけを知りたいとき。
- `session` や `apply` など、repo 共通処理以外のサブコマンド仕様を調べたいとき。

## hash

- 80385bba58bf311ef6c963184cfd1b01b1d81f1b9871704381ed6c9040b63a19

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

- `tests/test_subcommands.py` は、`init`、`session`、`apply`、`review oracles`、`main`、`bin/cmoc` の公開入口と周辺ヘルパーを横断して検証する回帰テスト群です。
- `run_command` の出力・ログ・終了コード、エラー整形、補完プローブ、Fake Codex CLI、git worktree、conflict marker の扱いを含む決定論的な制御を守ります。
- 各サブコマンドの業務ロジックそのものより、CLI と共通制御の境界条件と安定した統合動作を確認することを目的にしています。

## Read this when

- 公開 CLI の登録、ヘルプ、補完プローブ、`main` / `bin/cmoc` の入口仕様を確認したいとき。
- `init`、`session`、`apply`、`review oracles` の状態遷移や失敗時の挙動、`run_command` のログ出力を確認したいとき。
- report 生成、エラー整形、prompt / validation helper、Fake Codex CLI、git worktree、conflict marker の境界条件を確認したいとき。
- `format_error_report` や各種 prompt / validation helper の回帰意図を把握したいとき。

## Do not read this when

- `src/sub_commands` や `src/commons` の実装ロジックそのものを追いたいとき。
- 個別サブコマンドの詳細仕様や `oracles` の正本仕様だけを確認したいとき。
- `INDEX.md` の生成ルールや内容ハッシュの管理だけを調べたいとき。
- `tests/test_repo.py` や `tests/test_indexing.py` など、別の共通処理の回帰だけを見たいとき。

## hash

- 5471eaa166dee99a1128cf8674ca065efa0e0ce6c437d1a30e67ea0a1f18591a
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
