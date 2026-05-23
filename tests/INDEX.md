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

- `tests/test_codex.py` は、`commons.codex.run_codex_exec` の Codex CLI 呼び出しラッパーを検証するテストの目次です。
- Structured Output の `--json`、`--output-last-message`、`--output-schema`、schema ファイル生成、`model`、`reasoning_effort` の受け渡しを扱います。
- JSON 解析失敗、schema 不一致、semantic validator 失敗、非 JSON テキストの validator 失敗に対する最大 3 回のリトライと、失敗時の `CmocError` 詳細を扱います。
- stdout の進捗表示の切り詰めと改行可視化、quota 枯渇時の疎通確認と `--resume` 再実行、`INDEX.md` 事前メンテナンスの実行・スキップも検証対象です。

## Read this when

- `run_codex_exec` の引数構成、Structured Output の渡し方、リトライ挙動を確認したいとき。
- Codex CLI 呼び出し前後のログ保存、stdout 進捗表示、戻り値の扱いを調べたいとき。
- JSON schema 検証、semantic validator、非 JSON テキスト validator の失敗時挙動を確認したいとき。
- quota 枯渇時の疎通確認プロンプトと `--resume` 再実行の流れを確認したいとき。
- `INDEX.md` の事前メンテナンスが通常呼び出しで走る条件と、明示スキップできる条件を確認したいとき。

## Do not read this when

- `commons.codex.run_codex_exec` の実装本体や内部 helper の処理だけを確認したいとき。
- `cmoc` のサブコマンド全体、CLI エントリーポイント、`branch` / `apply` / `merge` など他機能の仕様を調べたいとき。
- `INDEX.md` 自動生成ロジックそのものや、対象ディレクトリ列挙の詳細を知りたいとき。
- Codex CLI や OpenAI API の一般的な使い方、外部仕様を調べたいとき。
- pytest 全体の共通設定や、テスト用 git リポジトリ作成の一般論だけを確認したいとき。

## hash

- c38030f1b7be20b969877e663701fb89f92a1116805c3ccab03f13d6d41f625f

# `test_indexing.py`

## Summary

- `commons.indexing.maintain_indexes` による `INDEX.md` メンテナンス処理の pytest テストです。
- gitignore 対象の除外、空ディレクトリへの空 `INDEX.md` 作成、`build`/`tmp` の親目次掲載と配置除外、非 UTF-8 バイナリ除外、UTF-8 文字境界の取り扱い、`memo` ディレクトリの扱いを検証します。
- 既存 `INDEX.md` の必須セクション欠落時の再生成、Structured Output 不正時のリトライ、最新 `INDEX.md` では Codex CLI を呼ばないこと、自動コミット対象がメンテナンス差分に限られることを検証します。
- テスト用 git リポジトリ作成と git コマンド実行の補助関数 `_init_repo` と `_git` を含みます。

## Read this when

- `maintain_indexes` の対象ファイル・対象ディレクトリ判定、除外規則、ハッシュによる再生成判定を確認したいとき。
- `INDEX.md` 生成で Codex CLI に渡す Structured Output schema、model、reasoning effort の期待値を確認したいとき。
- `build`、`tmp`、`memo`、`.gitignore`、非 UTF-8 バイナリ、空ディレクトリ、UTF-8 文字境界が `INDEX.md` メンテナンスでどう扱われるかを調べたいとき。
- 既存 `INDEX.md` が最新か壊れているかで Codex CLI 呼び出し、再生成、リトライがどう変わるかを確認したいとき。
- `INDEX.md` メンテナンス後の自動コミットがユーザー作業ファイルを巻き込まないことを確認したいとき。

## Do not read this when

- cmoc の `INDEX.md` 目次仕様そのものを正本仕様として確認したいとき。
- `maintain_indexes` の実装詳細を直接修正したいだけで、テスト期待値を確認する必要がないとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` など個別サブコマンドの挙動を調べたいとき。
- Codex CLI 実行共通処理や Structured Output リトライ処理の実装本体だけを読みたいとき。
- git リポジトリ操作一般、pytest 一般、またはテスト用 fixture の書き方だけを調べたいとき。

## hash

- 80901c433ef95e2268b5afeafbaf564a0371c640b34fdb568aebd38a5ec655f6

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

- `tests/test_subcommands.py` は、cmoc の主要サブコマンドと CLI エントリポイント周辺の決定論的な制御ロジックを固定するテスト群の目次です。
- `run_command` の stdout とログへの tee、例外時のエラーレポート、`cmoc init` / `cmoc branch` / `cmoc eval-oracles` / `cmoc apply` / `cmoc merge` の振る舞いを横断的に扱います。
- `main` と `bin/cmoc` の委譲構造、`cmoc --help` の表示、終了コード、仮想環境 Python 必須条件、共通エラー表示の文言も検証対象です。
- `apply` の不整合 schema 検証、`merge` の conflict prompt、`_init_repo` や `_checkout_cmoc_branch` のテスト補助も含みます。

## Read this when

- cmoc の各サブコマンドがどのように git 操作、レポート保存、終了コード処理を行うかをテスト観点から確認したいとき。
- サブコマンド実行時の stdout とログファイルの出力規則、進捗表示、例外時のまとめ出力を確認したいとき。
- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc apply`、`cmoc merge` の主要な制御フローを pytest の期待値から追いたいとき。
- `main` / `bin/cmoc` の起動経路、ヘルプ表示、エラー終了、仮想環境 Python 必須条件を確認したいとき。
- 不整合調査 JSON の schema、merge の conflict marker 検査、テスト用 git リポジトリの作り方を把握したいとき。

## Do not read this when

- cmoc の正本仕様そのものを知りたいとき。仕様断片は `oracles` 配下を読むべきです。
- 各サブコマンドの実装コードだけを追いたいとき。実装本体は `src/sub_commands` 配下にあります。
- `INDEX.md` 自動生成や更新の共通ロジックだけを調べたいとき。
- `commons.repo` や `commons.codex` など、サブコマンド以外の共通処理の単体テストを探しているとき。
- `README.md`、`AGENTS.md`、`oracles`、`memo` の運用ルールや編集可否だけを確認したいとき。

## hash

- a3ee2f52051d19370f268afce2685a86cb7eefca4913075ebedb18abfb2e8769

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
