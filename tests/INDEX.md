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

- `tests/test_codex.py` は `commons.codex.run_codex_exec()` の挙動を Fake Codex CLI で検証するテスト群の目次です。
- Structured Output の schema ファイル生成、JSON / テキスト出力の再試行、意味的検証失敗時のエラー表示、`enum` や文字列長制約を含む schema 検証を扱います。
- 呼び出しログ、`subcommand_log` への通知、出力プレビュー、`--resume` 再実行、quota 枯渇時の待機と疎通確認、`INDEX.md` 事前メンテナンスと `skip_index_maintenance` の扱いも確認します。
- ファイル末尾には、テスト用 git リポジトリを初期化して `git` を実行する補助関数 `_git` があります。

## Read this when

- `run_codex_exec()` の引数、`--output-schema`、`--output-last-message`、`--resume`、`skip_index_maintenance`、`reasoning_effort` の扱いを確認したいとき。
- Structured Output の構文検証・意味的検証のリトライ条件や、JSON Schema の `enum` や文字列長制約の検査を確認したいとき。
- `logs/codex_exec` の呼び出しログ、`logs/sub_commands` への通知、標準出力の進捗表示、80 文字の出力プレビュー規則を確認したいとき。
- quota 枯渇時の待機・疎通確認・`--resume` 再開の流れや、Codex 呼び出し前後で `INDEX.md` を保守するかどうかを確認したいとき。
- テストファイル末尾の `_git` 補助関数を使って、テスト用 git リポジトリを初期化する方法を確認したいとき。

## Do not read this when

- `cmoc` のユーザー向けサブコマンド仕様や `oracles` 側の正本仕様だけを確認したいときは、このテスト目次ではなく該当する仕様文書を読むべきです。
- `tests` 全体の共通 fixture や他のテストファイルの観点だけを追いたいときは、このファイルを読む必要はありません。
- `commons.codex` 以外の共通モジュールや `src/sub_commands` の実装ロジックだけを調べたいときは、このテスト群は目的外です。
- `INDEX.md` の生成・更新ルールそのものや、`README.md` / `AGENTS.md` / `memo` の運用ルールだけを確認したいときは、このファイルではなく別の案内を読むべきです。

## hash

- b218fda9e9398154cebcae82c5763379b1e34e6c4c7c94ed9c9c0ddc2075d774

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

- da6fb4e9bc601ae30956b75bfcaf9e3aff37eb1cad5ed6bf58094e64ec5cf412

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

- 094d29ba140eed5ad41fa5246ae11a99c8dcaff0c547362954b9431135c684a0

# `test_repo.py`

## Summary

- `tests/test_repo.py` は `commons.repo` の git リポジトリ共通処理を検証するテスト群の目次です。
- .cmoc の ignore 保証、既存 tracked ファイルの index 解除、cmoc ブランチ判定、session state の保存・読込を扱います。
- oracle ファイル列挙と実装ファイル列挙での `INDEX.md`・`.gitignore`・`.git/info/exclude`・`memo` の扱い、さらに base commit からの変更検出と削除検出を確認します。

## Read this when

- `commons.repo` の git リポジトリ共通処理がどのようにテストされているか確認したいとき。
- .cmoc の ignore 保証、tracked な `.cmoc` ファイルの index 解除、cmoc ブランチ判定を見直したいとき。
- oracle / 実装ファイルの列挙、変更検出、削除検出、session state の読み書きと検証条件を確認したいとき。

## Do not read this when

- `cmoc` の CLI 仕様や各サブコマンドの入出力だけを確認したいとき。
- `commons.repo` 以外の実装や、別モジュールのテストだけを追いたいとき。
- `INDEX.md` の自動生成ルールそのものや、`README.md`・`AGENTS.md`・`memo` の運用を確認したいとき。

## hash

- 4df1c877026403d80616b2d0f80b3e33ce2a82595a1da3ab53a5bd0569c28b37

# `test_subcommands.py`

## Summary

- `tests/test_subcommands.py` は `cmoc` のサブコマンド実装に対する回帰テストの目次です。
- `init`、`session`、`apply`、`eval-oracles` の制御フロー、状態遷移、ブランチ操作、レポート生成、ログ出力をまとめて扱います。
- `run_command`、`format_error_report`、各種 prompt 生成、Structured Output schema、`main` の Typer ルーティング委譲の整合性も検証します。

## Read this when

- `src/main.py` と `src/sub_commands/*` のルーティングや各 impl の入出力を変更・レビューしたいとき。
- `session` / `apply` の state 遷移、branch / worktree 管理、`join` / `abandon` の前提条件を見直したいとき。
- `run_command` のログ tee、`format_error_report`、`eval-oracles` / `apply` の prompt や Structured Output schema を修正したいとき。
- `main` の Typer 委譲、hidden alias、引数伝搬、`from __future__ import annotations` の禁止を確認したいとき。

## Do not read this when

- `src/commons/*` の実装詳細だけを追いたいとき。
- `oracles/app_specs/*` の正本仕様だけを読みたいとき。
- `INDEX.md` の生成・更新ルールそのものを確認したいとき。
- `README.md`、`AGENTS.md`、`memo` の運用や編集可否だけを確認したいとき。

## hash

- e23add9e64f13d7fbdc5f8dee3c695e20ac64485c554e58c55273a3e18424946

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
