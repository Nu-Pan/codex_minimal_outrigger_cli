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

- `tests/test_codex.py` は `commons.codex.run_codex_exec()` の挙動を Fake Codex CLI で検証する pytest 群の目次です。
- Structured Output の schema ファイル生成、JSON とテキストのリトライ、意味的検証失敗、呼び出しログ、出力通知、quota 枯渇時の再開を扱います。
- Codex CLI 呼び出し前の `INDEX.md` 事前メンテナンスと、そのスキップ可否も確認します。
- ファイル末尾にはテスト用に git リポジトリを初期化して実行する `_git` 補助関数があります。

## Read this when

- `run_codex_exec()` の引数や `--output-schema`、`--output-last-message`、`--resume` の扱いを確認したいとき。
- Structured Output の構文検証と意味的検証が 3 回までリトライされる条件を確認したいとき。
- 呼び出しログ、出力スキーマファイル、last message ファイル、標準出力通知の記録規則を確認したいとき。
- quota 枯渇時の待機・疎通確認・再開、および Codex 呼び出し前の `INDEX.md` 事前メンテナンスの有無を確認したいとき。
- テスト用 git リポジトリを作る `_git` 補助関数の使い方を確認したいとき。

## Do not read this when

- `cmoc` のユーザー向けサブコマンド仕様や oracle 正本仕様だけを知りたいとき。
- pytest の共通 fixture や `tests` 全体の配置ルールを探したいとき。
- `run_codex_exec()` 以外の `commons` 実装や git 共通処理の仕様を調べたいとき。
- `README.md`、`AGENTS.md`、`memo` の運用ルールだけを確認したいとき。

## hash

- 32372c764d82f5d3ea6686a2998b7ba5de71fedad212d77698dd1121a2bb2dfe

# `test_indexing.py`

## Summary

- `commons.indexing.maintain_indexes` による `INDEX.md` メンテナンス処理を検証する pytest テストの目次です。
- gitignore 除外、空ディレクトリへの空 `INDEX.md` 作成、`build` / `tmp` の扱い、非 UTF-8 バイナリ除外、UTF-8 文字境界、`memo` ディレクトリの扱いを確認します。
- 既存 `INDEX.md` の必須セクション欠落による再生成、Structured Output 不正時のリトライ、最新 `INDEX.md` では Codex CLI を呼ばない挙動、自動コミットの対象範囲を確認します。
- テスト用 git リポジトリを作成する `_init_repo` と、git コマンドを実行する `_git` の補助関数を含みます。

## Read this when

- `maintain_indexes` がどのファイル・ディレクトリを `INDEX.md` の目次対象にするか確認したいとき。
- `INDEX.md` 生成時の gitignore 除外、空ディレクトリ処理、`build` / `tmp` の掲載と配置除外の関係を確認したいとき。
- 非 UTF-8 バイナリ、UTF-8 文字境界、`memo` ディレクトリの扱いがどうなるかをテスト観点から確認したいとき。
- 既存 `INDEX.md` が壊れている場合の再生成、Structured Output のリトライ、最新判定による Codex CLI 呼び出し有無を確認したいとき。
- `INDEX.md` メンテナンス後に自動コミットがどの差分だけを含むかを確認したいとき。
- テスト用 git リポジトリの作り方や、`_init_repo` / `_git` の使い方を確認したいとき。

## Do not read this when

- `commons.indexing` の実装本体だけを追いたいとき。
- `INDEX.md` の正本仕様そのものを知りたいとき。仕様断片は `oracles/app_specs/indexing.md` を読むべきです。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` など個別サブコマンドの仕様を調べたいとき。
- Codex CLI 呼び出し共通仕様、ログ保存、エラーハンドリングなど `INDEX.md` メンテナンス以外の実行仕様を調べたいとき。
- `README.md`、`AGENTS.md`、`oracles`、`memo` の運用ルールや編集可否だけを確認したいとき。

## hash

- 6383cc6754a4b18b2ce48438321bf510c759435e76b43b86e3c3d6132e4fa117

# `test_repo.py`

## Summary

- `tests/test_repo.py` は `commons.repo` にある git リポジトリ共通処理の自動テストをまとめた目次です。
- `.cmoc` の ignore 保証、既存 tracked ファイルの index 除外、cmoc ブランチ判定、branch base commit 記録先を扱います。
- oracle ファイル列挙では `INDEX.md` の除外、root `.gitignore` のみを使う判定、`/` 付き pattern、`**` pattern、tracked な ignored file の扱いを検証します。
- 実装ファイル列挙では `oracles`、`.git`、`INDEX.md`、gitignore 対象を除外して、実装対象だけを返すことを検証します。
- 変更・削除検出では、base commit からの oracle / 実装の差分抽出、rename、未追跡ディレクトリ、履歴上の戻し、削除判定と `assert_no_uncommitted_changes` を確認します。

## Read this when

- `commons.repo` の git リポジトリ探索や `.cmoc` ignore 保証のテスト観点を確認したいとき。
- `.cmoc` 配下に既に tracked なファイルがある場合に、index から外す挙動を確認したいとき。
- oracle ファイル列挙で `INDEX.md`、root `.gitignore`、`/` 付き pattern、`**` pattern をどう扱うか確認したいとき。
- 実装ファイル列挙で `oracles` や `INDEX.md` を除外し、実装対象だけを返す条件を確認したいとき。
- `changed_oracle_files` が base commit と working tree / staged / committed 変更をどう拾うか確認したいとき。
- rename 後の oracle を削除ではなく変更として扱うか、削除検出とどう分かれるか確認したいとき。
- `has_deleted_oracle_files` と `has_deleted_implementation_files` の削除判定条件を確認したいとき。
- `cmoc apply` の前提条件として、未コミット差分を拒否する `assert_no_uncommitted_changes` の挙動を確認したいとき。
- cmoc ブランチ名の判定規則や、branch base commit の保存パスを確認したいとき。
- テスト用 git リポジトリを作る `_init_repo` と、そこで git コマンドを実行する `_git` の補助実装を見たいとき。

## Do not read this when

- `cmoc` のユーザー向け CLI 仕様やサブコマンドの入出力だけを知りたいとき。
- `commons.repo` 以外の本体実装や別モジュールのテストを探しているとき。
- oracle 正本仕様そのものを知りたいとき。仕様断片は `oracles/app_specs` 側を読むべきです。
- `INDEX.md` の自動生成やメンテナンス仕様だけを知りたいとき。
- `README.md`、`AGENTS.md`、`memo` の運用ルールだけを確認したいとき。
- `tests/test_codex.py` や `tests/test_indexing.py` のような別テスト群の仕様を調べたいとき。
- gitignore pattern の一般論だけを調べており、cmoc における oracle / 実装ファイル列挙の期待挙動が不要なとき。

## hash

- d2819022054e7ef9e7ed6cf5c2c2ddb1f4f42c3091dd8f2d6284d508083915f3

# `test_subcommands.py`

## Summary

- `tests/test_subcommands.py` は、cmoc の主要サブコマンドと CLI 入口の決定論的な制御ロジックを検証する pytest 群の目次です。
- `run_command` の stdout への tee、ファイルログ保存、共通エラーレポート、終了コード処理を横断して確認します。
- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc apply`、`cmoc merge` の実行フロー、prompt、Structured Output、補助関数をまとめて扱います。
- `main.py` のコマンド登録、`--help` 表示、互換 alias、`bin/cmoc` の起動条件も検証します。

## Read this when

- サブコマンドの CLI 入口がどの実装関数へ委譲されるか確認したいとき。
- `run_command` の stdout とファイルへの tee、ログ保存、例外時の終了コードやエラーレポートを確認したいとき。
- `cmoc init` の `.cmoc` ignore 追加、tracked ファイルの追跡解除、初期 commit を確認したいとき。
- `cmoc branch` のブランチ作成、base commit 記録、進捗表示を確認したいとき。
- `cmoc eval-oracles` の部分・全体評価切り替え、レポート保存、severity 集約、prompt 制約を確認したいとき。
- `cmoc apply` の不整合調査、要修正点の改善、修正 commit、レポート検証、Structured Output schema を確認したいとき。
- `cmoc merge` の branch 自動解決、コンフリクト解消 prompt、conflict marker 検査、ブランチ削除条件を確認したいとき。
- `main.py` の `--help`、`eval-oracle` と `eval-oracles` の両立、`cmoc apply --help` のオプション表示を確認したいとき。
- `bin/cmoc` の仮想環境 Python 必須条件や、launcher のエラーレポート出力を確認したいとき。
- テスト内の補助関数 `_init_repo`、_checkout_cmoc_branch`、`_git`、`_discrepancy_json`、`_eval_oracle_issue` の役割を確認したいとき。

## Do not read this when

- `src/sub_commands` の個別実装本体だけを追いたいとき。
- `src/commons` の共通基盤仕様だけを知りたいとき。
- `oracles` 側の正本仕様だけを確認したいとき。
- 他のテストファイル、たとえば `tests/test_repo.py` や `tests/test_indexing.py` を探しているとき。
- `README.md`、`AGENTS.md`、`memo` の運用ルールだけを確認したいとき。
- 開発者向けのコーディング規約、設計規約、テスト規約だけを調べたいとき。

## hash

- b26609a50991c4ad08d6090142edad6abde55461b15922dd21855ff5d03fcfdb

# `test_timestamps.py`

## Summary

- `tests/test_timestamps.py` は、`commons.timestamps.make_timestamp` と `commons.timing.format_duration` の出力仕様を確認するテストの目次です。
- cmoc の `<time-stamp>` が `YYYY-MM-DD_HH-MM_SS_mmm` 形式でゼロ埋めされることと、経過時間表示が固定幅の ` h  m  s` 形式で出ることを検証します。
- 同一ファイル内の補助関数の並び順が、呼び出し側を先・呼び出し先を後ろに置く方針になっていることも確認します。

## Read this when

- タイムスタンプ文字列の生成形式や、`make_timestamp` のゼロ埋め・ミリ秒表現を確認したいとき。
- サブコマンドの経過時間表示に使う `format_duration` の表示形式や、小数 1 桁の切り捨て規則を確認したいとき。
- `commons.timestamps` や `commons.timing` の仕様変更が、このテスト群にどう影響するか把握したいとき。
- テスト内の補助関数の配置順や、`inspect.getsourcelines()` を使った順序検証の意図を確認したいとき。

## Do not read this when

- タイムスタンプや経過時間表示と関係のない CLI サブコマンド仕様だけを調べたいとき。
- 日時のパース、タイムゾーン変換、UTC 固定など、タイムスタンプ生成以外の日時処理を探しているとき。
- Codex CLI 呼び出し、ログ保存、oracle 評価、INDEX.md 自動生成など、別の共通仕様を調べたいとき。
- `tests/test_repo.py` や `tests/test_indexing.py` のような別テスト群を探しているとき。

## hash

- e94f2022b96d86d1d943862a01d1866f5bd2872b6fd31f7e4dd3df4f64c6ca30
