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

- `tests/test_codex.py` は `commons.codex.run_codex_exec()` の振る舞いを Fake Codex CLI で検証するテスト群の入口です。
- Structured Output の schema ファイル生成、JSON とテキストの再試行、意味的検証失敗時の詳細エラー、`enum` や文字列長制約の検査を扱います。
- 呼び出しログ、`subcommand_log` への通知、`INDEX.md` 事前メンテナンスと `skip_index_maintenance`、quota 枯渇時の待機・疎通確認・`--resume` 再実行も確認します。
- ファイル末尾には、テスト用 git リポジトリを初期化して `git` を実行する補助関数 `_init_git_repo` と `_git`、および `_FailingTextIO` / `_RecordingTextIO` があります。

## Read this when

- `commons.codex.run_codex_exec()` の引数、`--output-schema`、`--output-last-message`、`--resume`、`skip_index_maintenance`、`reasoning_effort` の扱いを確認したいとき。
- Structured Output の parse 失敗、意味的検証失敗、JSON Schema の `enum` や文字列長制約に対するリトライとエラー表示を確認したいとき。
- Codex CLI 呼び出しログ、`subcommand_log` への通知、出力プレビュー、quota 枯渇時の待機と疎通確認、再実行の流れを確認したいとき。
- Codex 呼び出し前後の `INDEX.md` メンテナンスの有無や、`skip_index_maintenance` による明示スキップを確認したいとき。
- テスト用 git リポジトリを初期化して `git` を実行する補助関数 `_init_git_repo` と `_git`、ならびに `_TeeTextIO` の補助テストを確認したいとき。

## Do not read this when

- `cmoc` の個別サブコマンド正本仕様だけを確認したいときは、`oracles/app_specs/sub_commands/INDEX.md` 側を読むべきです。
- `INDEX.md` の生成・更新ルールそのものだけを確認したいときは、`oracles/app_specs/indexing.md` を読むべきです。
- `commons.codex.run_codex_exec()` 以外の実装や、`tests` 配下の別テスト群だけを追いたいときは、このファイルでは範囲が広すぎます。
- `README.md`、`AGENTS.md`、`memo` の運用や編集可否だけを確認したいときは、このテスト目次ではなく別の案内を参照すべきです。

## hash

- e4860b4c71a56d69dab03afe3d94b071487da810591b3e401c816decd518ae98

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

- `commons.indexing.maintain_indexes` による `INDEX.md` メンテナンス処理を検証する pytest テスト群です。
- gitignore 除外、空ディレクトリへの空 `INDEX.md` 作成、`build` / `tmp` の目次掲載、バイナリ除外、UTF-8 文字境界、`memo` ディレクトリの扱いを確認します。
- 既存 `INDEX.md` の不備による再生成、Structured Output のリトライ、最新 `INDEX.md` の再利用、自動コミット範囲、`.cmoc` ignore の責務境界を確認します。
- テスト用 git リポジトリを作る `_init_repo` と、git コマンドを実行する `_git` の補助関数を含みます。

## Read this when

- `maintain_indexes` がどのファイル・ディレクトリを `INDEX.md` の目次対象にするか確認したいとき。
- `INDEX.md` 生成時の gitignore 除外、空ディレクトリ処理、`build` / `tmp` の掲載と配置除外の関係を確認したいとき。
- 非 UTF-8 バイナリ、UTF-8 文字境界、`memo` ディレクトリ、既存エントリの再生成や再利用、Structured Output のリトライ挙動を確認したいとき。
- `INDEX.md` メンテナンス後の自動コミット範囲や、`.cmoc` の ignore 保証をこのテスト観点から確認したいとき。
- テスト用 git リポジトリの作り方や、補助関数 `_init_repo` / `_git` の使い方を確認したいとき。

## Do not read this when

- `commons.indexing.maintain_indexes` の実装ロジックだけを追いたいときは、このテスト目次ではなく実装本体を読むべきです。
- `INDEX.md` の正本仕様や生成・更新ルールを確認したいときは、`oracles/app_specs/indexing.md` を読むべきです。
- `cmoc init`、`cmoc session`、`cmoc apply`、`cmoc eval-oracles` など、他のサブコマンドの仕様だけを調べたいときは目的外です。
- Codex CLI の呼び出し仕様、ログ保存、エラーハンドリングなど、`INDEX.md` メンテナンス以外の共通仕様を知りたいときはこのファイルではありません。

## hash

- 955e1fffe864416494be630b7db90d00b6d2f25f3c613c1638acdc02e6e7d48a

# `test_repo.py`

## Summary

- `tests/test_repo.py` は `commons.repo` の git リポジトリ共通処理を検証するテスト群の入口です。
- .cmoc の ignore 保証、tracked な `.cmoc` の index 解除、cmoc ブランチ判定、ファイル列挙と変更・削除検出を扱います。
- `oracles` / 実装ファイルの抽出、`INDEX.md`・`.gitignore`・`.git/info/exclude`・`memo` の除外条件、session state の読み書きと active session 探索を確認します。
- ファイル末尾には、テスト用 git リポジトリを初期化する `_init_repo` と、git コマンド実行用の `_git` 補助関数があります。

## Read this when

- `tests/test_repo.py` が `commons.repo` のどの機能を検証しているか確認したいとき。
- .cmoc の ignore 保証、tracked な `.cmoc` の untrack、cmoc ブランチ判定を見直したいとき。
- `oracles` / 実装ファイルの列挙、変更検出、削除検出、`INDEX.md` や `.gitignore`、`.git/info/exclude`、`memo` の扱いを確認したいとき。
- session state の読み書き、active session の探索、`commit_if_changed` や `assert_no_uncommitted_changes` の前提条件を把握したいとき。
- テスト用 git リポジトリの初期化や、`_init_repo` / `_git` 補助関数の役割を確認したいとき。

## Do not read this when

- cmoc の CLI 操作手順や各サブコマンドのユーザー向け仕様だけを確認したいとき。
- `commons.repo` 以外の実装や、別モジュールのテスト群だけを追いたいとき。
- `INDEX.md` の生成・更新ルールそのものや、`README.md`・`AGENTS.md`・`memo` の運用規則だけを確認したいとき。
- git の一般論ではなく、このテスト群が何を検証しているかを知りたいとき。

## hash

- 615aa798360925b26210c46a85657ff1e25ccca48f14f0163d9c429e60379216

# `test_subcommands.py`

## Summary

- `tests/test_subcommands.py` は、cmoc の各サブコマンドと共通エラー処理の決定論的な制御ロジックを検証するテスト群の入口です。
- `init`、`session`、`apply`、`eval-oracles`、`main`、共通 runner、エラーレポート、CLI 登録、help 表示を横断して確認します。
- prompt 文言、Structured Output schema、対象選択、状態遷移、後始末、`bin/cmoc` の起動条件、補助関数の並び順まで固定します。

## Read this when

- `tests/test_subcommands.py` を修正・追加するとき。
- `cmoc init`、`cmoc session fork/join/abandon`、`cmoc apply fork/join/abandon`、`cmoc eval-oracles` の決定論的な制御フロー、state 更新、branch/worktree の後始末を確認したいとき。
- `main` のコマンド登録、help 表示、終了コード、共通エラーレポート、`bin/cmoc` の起動条件を確認したいとき。
- prompt 文言、Structured Output schema、対象ファイル選択ルール、validation helper の順序、CLI から impl への delegate 方針を見直したいとき。

## Do not read this when

- 個別サブコマンドのユーザー向け仕様だけを確認したいときは、対応する `oracles/app_specs/sub_commands/*.md` を直接読むべきです。
- 実装コードの配置や設計方針だけを確認したいときは、このテスト目次ではなく `oracles/app_specs` や `oracles/dev_rules` を読むべきです。
- `INDEX.md` の生成・更新ルールそのものだけを確認したいときは、`oracles/app_specs/indexing.md` を読むべきです。
- `tests/test_codex.py` や `tests/test_indexing.py` など、別のテスト群の観点だけを追いたいときはこのファイルでは範囲が広すぎます。
- README、AGENTS、memo の運用や編集可否だけを確認したいときは、このテスト目次ではなく別の案内を参照すべきです。

## hash

- 1a26bab981be0d0ab3fd2e6442982af4b27c8b1215d7f27afc18353d712713d8

# `test_timestamps.py`

## Summary

- `tests/test_timestamps.py` は `commons.timestamps.make_timestamp` と `commons.timing.format_duration` の仕様を確認するテスト群の目次です。
- タイムスタンプはローカルタイムゾーン基準で `YYYY-MM-DD_HH-MM_SS_mmm` 形式にゼロ埋めされることを検証します。
- `format_duration` の固定幅表示、小数 1 桁の切り捨て、そして同一ファイル内の補助関数が caller first, callee last で並ぶことを確認します。

## Read this when

- タイムスタンプ生成の書式、ミリ秒表現、aware datetime のローカルタイムゾーン変換を確認したいとき。
- サブコマンドなどで使う経過時間表示の書式や丸め方を確認したいとき。
- `commons.timestamps` や `commons.timing` の変更がこのテスト群に影響するか判断したいとき。
- テスト内の関数配置順や `inspect.getsourcelines()` を使った順序検証の意図を確認したいとき。

## Do not read this when

- タイムスタンプや経過時間表示と関係のない CLI サブコマンド仕様だけを調べたいとき。
- 日時のパースや UTC 固定など、`make_timestamp` 以外の日時処理を探しているとき。
- Codex CLI 呼び出し、ログ保存、`INDEX.md` 自動生成など別の共通仕様を調べたいとき。
- 別のテスト群や `tests` 全体の配置規則を確認したいとき。

## hash

- 86539d333fc59e712b7d1da968c1e89542375bc49ee7fef7e0ce81b4dc030a01
