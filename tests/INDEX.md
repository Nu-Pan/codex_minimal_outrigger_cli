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
- Structured Output の再試行、JSON / テキスト検証、`output_schema` の生成とキャッシュ、`resume` と quota 復旧の分岐を重点的に確認します。
- 呼び出しログ、コンソール通知、UTF-8 処理、workspace-write 時の oracle 変更検出も含みます。

## Read this when

- `run_codex_exec` の再試行条件や `json_validator` / `text_validator` の扱いを確認したいとき。
- `output_schema` の検証、ファイル化、キャッシュ再利用、schema 不一致時の挙動を追いたいとき。
- `resume`、quota 枯渇時の poll、capacity retry、last message 読み取り失敗の診断を追いたいとき。
- call log、subcommand log、コンソール進捗表示、prompt preview の整形を確認したいとき。
- workspace-write 実行時の oracle 変更ガードや `skip_index_maintenance` の境界を調べたいとき。

## Do not read this when

- `commons.indexing` や `commons.repo` の実装だけを追いたいとき。
- `tests/test_indexing.py`、`tests/test_repo.py`、`tests/test_subcommands.py` など、別領域の回帰を確認したいとき。
- `INDEX.md` 全体の生成ルールや `oracles` 側の正本仕様だけを知りたいとき。
- `run_codex_exec` 以外の CLI サブコマンドやファイル命名ルールを調べたいとき。
- codex 呼び出しログや quota / resume ではなく、純粋な git 共通処理や session state だけを確認したいとき。

## hash

- f9c8bc2903de2b63db6bf59fcfc3998666576214efe3b7d6758971904f6658a6

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

- `INDEX.md` メンテナンス処理の回帰テスト集です。
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

- 90fac4fafbe963a89ecec462a3c90e70c2465a73482e36e86671c172a9432205

# `test_repo.py`

## Summary

- `src/commons/repo.py` の git 共通処理を検証する回帰テスト群です。
- repo root 検出、`.cmoc` の ignore 保証、実装/正本ファイルの列挙と変更検出を扱います。
- session state、apply process id、`cmoc` ブランチ判定、active session 判定の境界条件も押さえます。

## Read this when

- repo root 検出や `.cmoc` の ignore 保証の挙動を確認したいとき。
- `list_implementation_files` / `list_oracle_files` や変更検出系の境界条件を調べたいとき。
- `commit_if_changed` のコミット可否や、失敗時に index と HEAD を壊さない挙動を確認したいとき。
- session state の読み書き、`active_session_ids_for_home_branch`、`is_cmoc_branch` の判定条件を確認したいとき。
- .gitignore`、`.git/info/exclude`、`INDEX.md`、`memo` の除外・対象判定の回帰を修正するとき。

## Do not read this when

- `src/commons/repo.py` の実装ロジックを直接追いたいとき。
- 個別の git ユーティリティや単体関数の使い方だけを確認したいとき。
- `INDEX.md` の生成ルールや `oracles` 全体のルーティング方針だけを知りたいとき。
- `session` や `apply` など、repo 共通処理以外のサブコマンド仕様を調べたいとき。

## hash

- 9f0a63e4c10b81e0dcbeeee2667216b95f2bb12f0c5092fd096773bd8baf4982

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

- `tests/test_subcommands.py` は cmoc の横断回帰テストの入口で、`run_command`、`main`、`bin/cmoc`、`format_error_report` など共通制御をまとめて検証します。
- `init`、`session`、`apply`、`review oracles` の状態遷移、ブランチ操作、エラー表示、終了コード、レポート出力を一括で押さえます。
- 補完プローブ、`.cmoc` ignore 修復、作業ツリー復旧、サブコマンドログ、error report の境界条件まで含みます。

## Read this when

- サブコマンド横断の制御フローや終了コードの仕様を確認したいとき。
- `cmoc init`、`session fork`、`session join`、`session abandon`、`apply fork`、`apply join`、`apply abandon`、`review oracles` の回帰観点を整理したいとき。
- `main` の補完登録、`bin/cmoc` の起動前提、`format_error_report` の出力整形を確認したいとき。
- `run_command` がコンソール出力と JSONL サブコマンドログをどう残すか確認したいとき。
- `tests/test_subcommands.py` がどの範囲の振る舞いを守るか把握したいとき。

## Do not read this when

- 個別サブコマンドの内部実装だけを追いたいときは、`src/sub_commands/*` を直接読むべきです。
- `commons.command_runner` や `commons.errors` など単一の共通ヘルパーだけを確認したいとき。
- `tests/test_timestamps.py` や `tests/test_report_files.py` のような別のテスト入口を見たいとき。
- pytest の共通設定やテスト命名規則だけを確認したいとき。
- `INDEX.md` の生成ルール全体や `oracles` 側の正本仕様だけを確認したいとき。

## hash

- a06b5aef920742eb5287fe0019ee77b8b826f00589b1e053d7e1eaafd5afed4f

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
