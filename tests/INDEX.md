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

- `commons.codex.run_codex_exec` の Codex CLI 呼び出しラッパーを検証する pytest テストファイルです。
- Structured Output の JSON schema 渡し、`--json`、`--output-last-message`、`--output-schema`、model、reasoning effort、schema ファイル生成、ログ記録の挙動を確認します。
- JSON parse 失敗、JSON schema 不一致、JSON semantic validator 失敗、非 JSON text validator 失敗について、3 回リトライする挙動と失敗時の `CmocError` 詳細出力を検証します。
- stdout の進捗表示では、prompt と output を元文字列の先頭 80 文字で切ってから改行を可視化する仕様を確認します。
- Structured Output 利用時の `output_schema` 必須条件と、oracle で禁止される high/xhigh reasoning effort の起動前拒否を検証します。
- quota 枯渇時のセッション再開、`--resume` 付き再実行、resume 後の想定外エラー報告、`commons.indexing.maintain_indexes` の事前実行とスキップ指定を確認します。
- テストでは一時ディレクトリに fake `codex` 実行ファイルを作成し、`PATH` 差し替え、`monkeypatch`、`capsys`、一時 git repo を使って外部 Codex CLI の挙動を模擬します。

## Read this when

- `run_codex_exec` のリトライ回数、ログ保存、進捗表示、エラー詳細の期待仕様をテストから確認したいとき。
- Structured Output の `output_schema` ファイル化、Codex CLI 引数、JSON schema 検証、semantic validator の扱いを調べたいとき。
- 非 JSON テキスト出力に対する validator、リトライ、失敗時 `CmocError` の詳細内容を確認したいとき。
- quota 枯渇検出、疎通確認 prompt、`--resume` 再実行、resume 後エラー処理のテストケースを探しているとき。
- Codex CLI 呼び出し前の `INDEX.md` メンテナンス実行と、生成処理や conflict 解消時のメンテナンススキップ指定を確認したいとき。
- fake `codex` バイナリ、`tmp_path`、`monkeypatch`、`capsys` を使った Codex CLI ラッパーの単体テスト実装例を参照したいとき。

## Do not read this when

- `run_codex_exec` の実装本体や内部 helper の具体的な処理を直接確認したいとき。
- cmoc のサブコマンド全体、CLI エントリーポイント、設定ファイル、oracle 評価、branch/apply/merge などの仕様を調べたいとき。
- `INDEX.md` 自動生成ロジックそのもの、対象ディレクトリの列挙、ハッシュ管理、ルーティング文書生成の詳細実装を調べたいとき。
- Codex CLI や OpenAI API の一般的な使い方、外部仕様、最新のモデル情報を調べたいとき。
- pytest 全体の設定、テスト共通 fixture、テスト環境構築、依存関係管理だけを確認したいとき。

## hash

- 9500b79b0454eaad4460bde1cb95644ffebd726197018fb30b11442881ef93fa

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

- `tests/test_subcommands.py` は、cmoc の主要サブコマンドと CLI エントリーポイント周辺の決定論的な制御ロジックを検証する pytest ファイルです。
- `cmoc init` について、`.cmoc` の ignore 追加、tracked `.cmoc` ファイルの追跡解除、unborn HEAD での初期 commit、既存 `.gitignore` 差分や事前 stage 済み差分を初期化 commit に混ぜないことを確認します。
- `cmoc branch` について、`cmoc_` で始まる作業ブランチ作成、base commit 記録、進捗表示を確認します。
- `cmoc eval-oracles` について、Fake Codex CLI を使った評価レポート保存、PEP 8 準拠の `eval_oracles.py` 配置、評価 prompt が oracle 仕様だけを参照させること、prompt の行順を確認します。
- `cmoc apply` について、不整合なし・不整合残存時の終了コードとレポート、repeat 上限、Codex JSON schema 指定、必須項目不足レポートの拒否、cmoc ブランチ外実行の拒否、`.cmoc` ignore 保証 commit と oracle commit の分離、禁止領域差分の再検査を確認します。
- apply の不整合調査 JSON について、必須フィールド不足や近い名前の誤ったキーを `_validate_discrepancy_payload` が拒否することを確認します。
- `cmoc merge` について、明示された cmoc ブランチの merge と削除、自動解決失敗時の案内抑制、conflict 解消 prompt で oracles 編集を常に禁止すること、conflict marker 検査が git 管理対象全体を見ることを確認します。
- `main` と `bin/cmoc` について、Typer コマンド関数が impl へ直接委譲すること、`cmoc --help` の Usage 表示、サブコマンドエラーの非ゼロ終了、ランチャーが仮想環境 Python を必須にし、欠落時に stdout の共通エラーレポートを出すことを確認します。
- テスト補助として、一時 git リポジトリを初期化する `_init_repo`、固定名の cmoc ブランチへ切り替える `_checkout_cmoc_branch`、git コマンドを実行する `_git` を定義しています。

## Read this when

- cmoc のサブコマンド実装を変更し、既存テストがどのユーザー向け挙動や git 操作を固定しているか確認したいとき。
- `cmoc init` の `.cmoc` ignore、追跡解除、初期 commit、既存差分や stage 済み差分の扱いを調べたいとき。
- `cmoc branch` のブランチ名、base commit 記録、stdout 進捗表示に関するテストを探しているとき。
- `cmoc eval-oracles` のレポート保存、Codex 呼び出しの fake 化、評価 prompt の禁止事項や文面順序を確認したいとき。
- `cmoc apply` の repeat ループ、不整合 JSON schema、レポート必須項目、終了コード、`.cmoc` 保証 commit、oracle 差分 commit、禁止パス検査を確認したいとき。
- `cmoc merge` の merge 後ブランチ削除、自動解決失敗時の出力、conflict 解消 prompt、conflict marker 検査範囲を確認したいとき。
- Typer の `main` 実装、`cmoc --help` 表示、サブコマンドエラー時のプロセス終了コード、`bin/cmoc` ランチャーの仮想環境チェックを変更するとき。
- サブコマンドのテストで一時 git リポジトリをどう作り、cmoc ブランチ状態をどう再現しているか知りたいとき。

## Do not read this when

- cmoc の正本仕様そのものを確認したいとき。このファイルはテストであり、仕様断片は `oracles` 配下を読むべきです。
- 個別サブコマンドの実装詳細を直接修正したいだけで、既存テストの期待値確認が不要なとき。
- INDEX.md 生成、ファイル列挙、Structured Output など、目次メンテナンス専用のテストを探しているとき。
- Codex CLI 呼び出し共通処理、設定ファイル、repo 探索、ログ保存などの単体テストだけを探しているとき。
- pytest の一般的な書き方や git の一般的な操作方法だけを知りたいとき。
- README、AGENTS、oracles、memo の編集可否など、リポジトリ運用ルールだけを確認したいとき。

## hash

- 79cfe2ec927568ece2fe0c595f38bc18dd684a56673073817cb310ca625bf7e2

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
