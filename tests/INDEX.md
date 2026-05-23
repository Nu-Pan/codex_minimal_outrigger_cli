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

- `tests/test_codex.py` は `commons.codex.run_codex_exec()` の挙動を Fake Codex CLI で検証する pytest 群の入口です。
- Structured Output の schema ファイル生成、JSON/テキストのリトライ、意味的検証失敗、ログ出力、quota 枯渇時の再開、INDEX.md 事前メンテナンスを扱います。
- `cmoc` の Codex 呼び出しラッパーに関する制御ロジックを確認するためのテストです。

## Read this when

- `run_codex_exec()` の引数や `--output-schema` / `--output-last-message` / `--resume` の扱いを確認したいとき。
- JSON / テキスト出力の構文・意味的検証が 3 回までリトライされる条件を確認したいとき。
- 呼び出しログ、出力スキーマファイル、last message ファイル、標準出力通知の記録規則を確認したいとき。
- quota 枯渇時の待機・疎通確認・再開、および INDEX.md 事前メンテナンスの有無を確認したいとき。

## Do not read this when

- `cmoc` のユーザー向けサブコマンド仕様や oracle 正本仕様だけを知りたいとき。
- pytest の共通 fixture や `tests` 全体の配置ルールを探したいとき。
- `run_codex_exec()` 以外の `commons` 実装や git 共通処理の仕様を調べたいとき。
- `README.md`、`AGENTS.md`、`memo` の運用ルールだけを確認したいとき。

## hash

- 725b71c5caab41a2c32523c179a637406a180d4f613de1c1c730ed0eec505da9

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

- c0f44d7d640d0d3849d8e75450417b77b1e3808170911631ee5292682eba42a8

# `test_repo.py`

## Summary

- `tests/test_repo.py` は、`commons.repo` にある git リポジトリ共通処理の自動テストです。
- `find_repo_root`、`.cmoc` の ignore 保証、`.cmoc` 配下 tracked ファイルの index 除外、cmoc ブランチ名判定、branch base commit 記録パスを検証します。
- oracle ファイル列挙について、`INDEX.md` の除外、root `.gitignore` のみを使う除外判定、slash 付き pattern、`**` pattern、tracked かつ gitignore 対象の扱いを検証します。
- 実装ファイル列挙について、`oracles`、`.git`、`INDEX.md`、gitignore 対象を除外し、実装対象だけを返すことを検証します。
- cmoc ブランチの base commit からの変更検出について、committed 変更、未コミット変更、未追跡ディレクトリ内の新規 oracle、履歴上で戻された変更、rename 後 path、gitignore 対象除外を検証します。
- oracle 削除検出について、committed 削除、途中 commit での削除後再追加、working tree 削除、staged 削除を全体評価切替条件として扱うことを検証します。
- oracle 削除検出の除外条件として、rename、`INDEX.md` の削除、root `.gitignore` 対象ファイルの削除を削除扱いしないことを検証します。
- 実装ファイル変更・削除検出について、oracle や `INDEX.md` を除いた実装対象の変更抽出と、実装ファイル削除の検出を検証します。
- `assert_only_oracles_uncommitted` が `cmoc apply` の事前条件として oracles 外の未コミット差分を拒否することを検証します。
- テスト用 git リポジトリを作成する `_init_repo` と、指定リポジトリで git コマンドを実行する `_git` の補助関数を含みます。

## Read this when

- `commons.repo` の git リポジトリ探索、cmoc 用 `.gitignore` 更新、`.cmoc` 配下ファイルの追跡解除に関するテストを確認したいとき。
- oracle ファイル列挙や変更検出で、`INDEX.md`、root `.gitignore`、slash pattern、double-star pattern、tracked ignored file をどう扱うべきか確認したいとき。
- `changed_oracle_files`、`has_deleted_oracle_files`、`changed_implementation_files`、`has_deleted_implementation_files` の期待挙動をテストから把握したいとき。
- cmoc ブランチの base commit を基準に、committed 変更、未コミット変更、未追跡ファイル、rename、削除、再追加履歴をどう検出するか確認したいとき。
- `cmoc apply` 実行前に oracles 外の未コミット差分を拒否する条件を確認したいとき。
- cmoc ブランチ名の正規表現的な判定条件や、branch base commit 記録ファイルの配置を確認したいとき。
- git を使う pytest の fixture 的な補助関数や、一時リポジトリ作成パターンを参考にしたいとき。

## Do not read this when

- CLI サブコマンドのユーザー向け仕様や stdout 表示、Codex CLI 呼び出し、Structured Output、ログ保存などの実行時仕様を調べたいとき。
- `commons.repo` 以外の実装モジュール、サブコマンド本体、設定ファイル処理、エラーレポート処理のテストを探しているとき。
- oracle 正本仕様そのものの記述内容や、仕様ファイル間のルーティングを調べたいとき。
- `README.md`、`AGENTS.md`、`oracles`、`memo` の編集可否など、リポジトリ運用ルールだけを確認したいとき。
- cmoc を使って別リポジトリを開発する `<repo-root>` 側の作業手順を知りたいとき。
- gitignore pattern の一般仕様だけを調べており、cmoc の oracle・実装ファイル列挙における期待挙動が不要なとき。

## hash

- cfb776e4fd4975b4cf44e30dbf3f26ce83f82cd6aa53526305112fd45422cd03

# `test_subcommands.py`

## Summary

- `tests/test_subcommands.py` は、`cmoc` の主要サブコマンドと CLI エントリポイント周辺の決定論的な制御ロジックを検証するテスト群の目次です。
- `run_command` の stdout への tee、ログ保存、例外時のエラーレポート、終了コード処理を横断的に扱います。
- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc apply`、`cmoc merge` の制御フローに加え、`main` と `bin/cmoc` の委譲構造や補助ヘルパー群の確認先になります。

## Read this when

- `cmoc` 各サブコマンドの制御フロー、終了コード、ログ出力をテスト観点から確認したいとき。
- `main` / `bin/cmoc` の起動経路、`cmoc --help`、エラー表示、仮想環境 Python 必須条件を確認したいとき。
- `apply` の不整合 JSON schema、`eval_oracles` の prompt 仕様、`merge` の conflict 解消プロンプトをテストで追いたいとき。
- テスト用 git リポジトリの作り方や、`_checkout_cmoc_branch` などの補助関数を把握したいとき。

## Do not read this when

- `cmoc` の正本仕様そのものを知りたいとき。
- サブコマンドの実装本体や共通処理のコードだけを追いたいとき。
- `INDEX.md` 自動生成や `<repo-root>` 側のディレクトリ列挙仕様だけを知りたいとき。
- `README.md`、`AGENTS.md`、`oracles`、`memo` の運用ルールだけを確認したいとき。

## hash

- 3b20d8c30f290681a7b279bc940f93d00cd9e1ef82d40687595f06d735de7949

# `test_timestamps.py`

## Summary

- `commons.timestamps.make_timestamp` と `commons.timing.format_duration` の出力形式を検証するテストファイルです。
- cmoc timestamp が `YYYY-MM-DD_HH-MM_SS_mmm` 形式で、日時要素とミリ秒がゼロ埋めされることを確認します。
- 経過時間表示が stdout 用の固定幅 ` h  m  s` 形式になり、秒の小数第 1 位が切り捨てで表示されることを確認します。

## Read this when

- タイムスタンプ文字列の仕様や `make_timestamp` の期待フォーマットを確認したいとき。
- サブコマンド完了時などに表示する経過時間文字列のフォーマットを確認したいとき。
- `commons.timestamps` または `commons.timing` の出力仕様を変更し、その既存テスト影響を把握したいとき。

## Do not read this when

- タイムスタンプや経過時間表示と関係のない CLI サブコマンド仕様を調べているとき。
- 日時生成処理そのものの実装詳細だけを読みたいとき。
- Codex CLI 呼び出し、ログ保存、oracle 評価などの高レベルな実行仕様を確認したいとき。

## hash

- 05d4e42195653c5b491aa1c7a212a92f0c106b6988f231389a2ab14348ca30dc
