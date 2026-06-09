# `__init__.py`

## Summary

- `tests/test_subcommands/__init__.py` は `tests.test_subcommands` を Python パッケージとして成立させるための空の初期化ファイルです。
- テストケースや共通ヘルパー、公開 API は持たず、パッケージの入口だけを提供します。

## Read this when

- `tests.test_subcommands` を import できる理由を確認したいとき。
- 個別の `test_*.py` や `helpers.py` を読む前に、この入口だけ把握したいとき。
- このファイルが空であることを前提に、ルーティングの目次を作りたいとき。

## Do not read this when

- 個別テストや共通ヘルパーの内容を確認したいとき。
- サブコマンド実装や CLI 挙動の詳細を追いたいとき。
- このファイルに公開 API や実装ロジックがある前提で探したいとき。

## hash

- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `helpers.py`

## Summary

- `tests/test_subcommands` 配下の回帰テストで共通利用する import、fixture 補助、テスト用リポジトリ構築関数をまとめたヘルパーモジュールです。
- session/apply の状態作成、衝突再現、oracle snapshot 作成、補完実行プローブ、git 実行補助などの再利用ロジックが入っています。
- 個別テストを簡潔に保つための共通土台であり、サブコマンド横断テストの前処理と検証補助を担います。

## Read this when

- `tests/test_subcommands` 配下のテストで共通利用している import とヘルパー関数を確認したいとき。
- テスト用 git リポジトリ、session/apply 状態、conflict 状態の作り方を把握したいとき。
- subcommand log、`StepTimer`、エラーレポート、補完プローブなどの共通テスト基盤を変更・レビューしたいとき。

## Do not read this when

- 個別のサブコマンド仕様や本番実装の挙動だけを確認したいとき。
- `tests/test_subcommands` の個別テストケースの期待値や分岐だけを追いたいとき。
- `INDEX.md` の生成ルールやメタデータ管理方法そのものを確認したいとき。

## hash

- 4e108249a532c9f12bdf12736720f4571e33c052bf478e04490392cc77611b95

# `test_apply_abandon.py`

## Summary

- `tests/test_subcommands/test_apply_abandon.py` は、`cmoc apply abandon` の回帰テスト群をまとめたファイルです。
- 未 join の apply run を安全に破棄し、`apply.state` を `ready` に戻して、apply branch と worktree を削除する挙動を検証します。
- 実行中 process の停止、legacy PID file の安全性、dirty な作業ツリーや別 session 混入時の拒否も確認します。

## Read this when

- `cmoc apply abandon` の破棄条件、state 遷移、cleanup の流れを確認したいとき。
- apply branch と apply worktree の削除、session branch への復帰、実行中 process の停止条件を確認したいとき。
- 別 session の apply branch を誤って消さない条件、dirty worktree の検出、`ready` / `error` / `running` / 未知 state の扱いを確認したいとき。

## Do not read this when

- `cmoc apply fork` や `cmoc apply join` の処理順、調査・取り込み・レポート生成だけを確認したいとき。
- `cmoc session fork`、`cmoc session join`、`cmoc session abandon` など、session 側の開始・統合・破棄ロジックを確認したいとき。
- `tests/test_subcommands` 全体の入口や、他のサブコマンド回帰テストを探したいとき。

## hash

- 3c34ff885a8c08fa3d0b563cbac11cfca79f046dfa63432f4140eb2f8d1b55b8

# `test_apply_fork.py`

## Summary

- `<cmoc-root>/tests/test_subcommands/test_apply_fork.py` は `cmoc apply fork` の回帰テストを意味カテゴリ別にまとめたファイルです。
- 開始前提の判定、調査対象 scope の決定、要修正点の改善ループ、report 出力、state 更新を扱います。
- 不整合調査の JSON schema、並列実行、変更要約、path 制約、エラー報告の境界条件も確認します。

## Read this when

- `cmoc apply fork` の正常系・異常系・回帰観点をまとめて把握したいとき。
- 不整合調査の流れ、要修正点の抽出と再調査、report 生成、state 更新の検証ポイントを確認したいとき。
- 絶対パス、禁止パス、並列調査、Structured Output schema、change summary の生成条件を追いたいとき。
- `<cmoc-root>/tests/test_subcommands/test_apply_fork.py` が何を守っているかを先に整理したいとき。

## Do not read this when

- `cmoc apply join` や `cmoc apply abandon` など、別の apply サブコマンドの挙動を確認したいとき。
- `cmoc session fork/join/abandon` や `cmoc review oracles` など、apply fork 以外のサブコマンドを確認したいとき。
- `src/sub_commands/apply/fork.py` の実装本体や、`oracles/docs/app_specs/sub_commands/apply_fork.md` の仕様断片だけを読みたいとき。
- `tests/test_subcommands` の共通ヘルパーや CLI 横断テストではなく、このファイル固有の確認だけで足りるとき。

## hash

- 67342edc991d9a34e817dd35ee7b8f7f21742ed4bb6eff66a3646bbcd52f916c

# `test_apply_join.py`

## Summary

- この `tests/test_subcommands/test_apply_join.py` は、`cmoc apply join` の回帰テスト群をまとめたファイルです。
- `session/apply` の state 遷移、想定外差分の検出、`--force-resolve` による復旧、`INDEX.md` の自動解決を扱います。
- rename/copy の差分判定、NUL 安全な path 処理、linked worktree からの join、join 後の branch / worktree cleanup も確認します。

## Read this when

- `cmoc apply join` の正常系・失敗系・強制復旧・cleanup の回帰を確認したいとき。
- session/apply の state 遷移や、完了済み apply branch を session branch に取り込む前提条件を確認したいとき。
- 想定外差分の判定基準や、`--force-resolve` でどの差分だけを復元・維持するかを追いたいとき。
- `INDEX.md` conflict の自動解決、rename/copy の扱い、NUL を含む path の安全性を確認したいとき。
- linked worktree から join した場合の cleanup 先や、branch / worktree 削除条件を確認したいとき。

## Do not read this when

- `cmoc apply fork` や `cmoc apply abandon` など、別の apply サブコマンドの挙動を確認したいとき。
- `cmoc session fork`、`cmoc session join`、`cmoc session abandon` など、session 側のテストを確認したいとき。
- `src/sub_commands/apply/join.py` の実装本体や、`oracles/docs/app_specs/sub_commands/apply_join.md` の仕様断片だけを読みたいとき。
- `tests/test_subcommands` 全体の入口や共通ヘルパーだけを先に確認したいとき。

## hash

- 61668fba567c6adee3cb9291dc66c07db3e7babe51d994fddfa687d08ec797be

# `test_cli.py`

## Summary

- `tests/test_subcommands/test_cli.py` は cmoc の CLI 入口と周辺ランチャーの横断回帰テストをまとめたファイルです。
- root help、completion probe、公開サブコマンドの登録、エラー報告の Markdown 整形、`bin/cmoc` と `test.sh` の振る舞いを扱います。
- `session`、`apply`、`review`、`indexing` の公開面と、`review oracles` や `eval-oracles` の互換性も確認します。

## Read this when

- `main` の root CLI 入口、`Typer` への委譲、サブコマンド登録の境界を確認したいとき。
- `cmoc --help`、completion probe、`review oracles` の alias、`indexing` の公開有無を確認したいとき。
- `apply fork` や `review oracles` の help 表示、正式オプション名、エラー報告の整形を変更したいとき。
- `bin/cmoc` ランチャーや `test.sh` の PATH 優先順位、仮想環境未検出時の挙動を確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや引数検証の詳細だけを追いたいとき。
- `commons.codex`、`commons.indexing`、`commons.repo` など別モジュールの実装を確認したいとき。
- `tests/test_codex.py` や `tests/test_repo.py` など、CLI 以外の回帰テストを探したいとき。

## hash

- e1296a5251d512fb48a393ee22b16ba9bb0c71b142217eaaba1acd85bc9d7762

# `test_core.py`

## Summary

- `tests/test_subcommands/test_core.py` は、サブコマンド横断の共通実行基盤、エラーレポート、`StepTimer` の回帰テストをまとめたファイルです。
- `cmoc init` の `.cmoc` ignore 修復・commit・tracked ファイル解除と、`cmoc indexing` の maintenance / check / dirty repo 判定も扱います。

## Read this when

- `run_command()`、`StepTimer`、`start_step()` の終了処理やログ・計測表示を変更したいとき。
- `cmoc init` の `.cmoc` ignore 修復、commit、tracked `.cmoc` の追跡解除の挙動を確認したいとき。
- `cmoc indexing` の通常実行、`--check`、dirty リポジトリ判定、INDEX 保守への委譲条件を確認したいとき。
- サブコマンド横断の共通動作と、初期化・インデックス保守の境界を把握したいとき。

## Do not read this when

- CLI のサブコマンド登録、補完、`help` 表示だけを確認したいとき。
- `apply` や `session` の個別サブコマンドの状態遷移や処理順だけを追いたいとき。
- `src/commons/command_runner.py`、`src/sub_commands/init.py`、`src/sub_commands/indexing.py` の実装本体を直接確認したいとき。

## hash

- 5770493150a54bcb583b59ce64c1f1dbafe9668054487a2af578b2c0eb9afe75

# `test_review_oracles.py`

## Summary

- `tests/test_subcommands/test_review_oracles.py` は、`cmoc review oracles` と旧別名 `cmoc eval-oracles` の回帰テスト群です。
- review worktree の隔離、oracles の固定 snapshot、所見の列挙・統合・検証・判定までの pipeline をまとめて検証します。
- Structured Output schema、レポート出力、エラー処理、prompt 文言、検証ヘルパー、ループ回数の境界条件も扱います。

## Read this when

- `cmoc review oracles` と旧別名 `cmoc eval-oracles` の挙動をテスト観点で追いたいとき。
- review worktree の作成・merge、oracles snapshot の固定、`INDEX.md` メンテナンスの扱いを確認したいとき。
- finding pipeline の列挙・統合・検証・判定、report / error report 生成、prompt 仕様、loop option を確認したいとき。
- `_evaluation_prompt`、`_improvement_prompt`、検証ヘルパー、output schema 定数、issue ID 付与などの補助ロジックを確認したいとき。

## Do not read this when

- `cmoc apply`、`cmoc session`、`cmoc init`、`cmoc indexing` の回帰テストを確認したいとき。
- `src/sub_commands/review/oracles.py` の実装本体や CLI 登録だけを追いたいとき。
- `tests/test_subcommands` の共通ヘルパーや、他の個別テストファイルを確認したいとき。
- `cmoc review oracles` の利用手順だけで足り、回帰テストの詳細が不要なとき。

## hash

- d82b790c9613586349cc1a297fa62abb8a25a3c43cce7a5992d100bd80ad6986

# `test_session_abandon.py`

## Summary

- `tests/test_subcommands/test_session_abandon.py` は `cmoc session abandon` の回帰テスト群です。
- session branch を merge せず破棄して home branch に戻す正常系と、`session.state` / `apply.state` の前提条件、`.cmoc` の ignore 補修を扱います。
- cleanup 失敗時の rollback、branch 削除失敗、state 保存失敗、再実行案内まで含む境界条件を確認します。

## Read this when

- `cmoc session abandon` の挙動を変更したとき。
- `session.state`、`apply.state`、未コミット差分、home branch の存在確認などの事前条件を確認したいとき。
- cleanup 失敗時の rollback やエラーメッセージ、`.cmoc` 補修の回帰を確認したいとき。

## Do not read this when

- `cmoc session fork` や `cmoc session join` の仕様やテストだけを確認したいとき。
- `cmoc apply` 系サブコマンドや `cmoc review` / `cmoc init` のテストを確認したいとき。
- `src/sub_commands/session/abandon.py` の実装や `oracles/docs/app_specs/sub_commands/session_abandon.md` の仕様断片だけを確認したいとき。

## hash

- 479667e765c2fa673d66c44b5224e001c29c4b897b0f2b3e12cd0660d900fe2c

# `test_session_fork.py`

## Summary

- `tests/test_subcommands/test_session_fork.py` は `cmoc session fork` の回帰テスト群の入口です。
- session branch の作成、state 保存、`.cmoc` の ignore 補修、前提条件チェック、競合検出、rollback をまとめて確認します。
- このファイルから、`cmoc session fork` の正常系と失敗系を横断的にたどれます。

## Read this when

- `cmoc session fork` の回帰テストが何を守っているかを把握したいとき。
- session branch 作成、session state 記録、`.cmoc` ignore 補修の流れを確認したいとき。
- local branch 限定、detached HEAD、cmoc 管理 branch、未コミット差分、既存 active session などの拒否条件を確認したいとき。
- linked worktree から実行したときの state 保存先や、main repo-root 側の active session 判定を確認したいとき。
- state 保存失敗時の rollback、branch 削除失敗時の後始末、壊れた session state や orphan branch の扱いを確認したいとき。

## Do not read this when

- `cmoc session fork` の実装本体や git 操作の詳細を追いたいときは、`src/sub_commands/session/fork.py` を直接読むとき。
- `cmoc session join` / `cmoc session abandon` など、session の別サブコマンドを確認したいとき。
- `tests/test_subcommands` 全体の入口や、他の回帰テスト群の見取り図だけを確認したいとき。
- `oracles/docs/app_specs/sub_commands/session_fork.md` の仕様断片だけを読みたいとき。

## hash

- 1db6d3d5ce45d3308f36bfbf197ca6771aeefaab600f91605bef5dbe5ef2be05

# `test_session_join.py`

## Summary

- `tests/test_subcommands/test_session_join.py` は `cmoc session join` の回帰テスト群です。
- session_home_branch の検証、非 session branch の拒否、`.cmoc` の ignore 補修、merge 後の `joined` 更新と branch 削除を確認します。
- merge conflict 時の自動解消、root document や forbidden path の扱い、Codex の不正変更や merge state 改ざんの検出も扱います。

## Read this when

- `cmoc session join` の正常系と異常系をまとめて把握したいとき。
- session branch を記録済み home branch に merge し、状態更新と branch 削除まで含めた流れを確認したいとき。
- merge conflict 時の Codex 依頼、禁止領域、未解決 marker、merge state の不正検出までのテスト観点を確認したいとき。

## Do not read this when

- `cmoc session fork` や `cmoc session abandon` の挙動だけを確認したいとき。
- `cmoc apply` 系の開始・統合・破棄の回帰テストを確認したいとき。
- `src/sub_commands/session/join.py` の実装そのものを追いたいときは、このテストではなく本体実装を読むべきです。

## hash

- ffd80ab9f5211d7ee7f91fe4e1a7885bdcc5cc6cb11d4f784c7832de14ca93cf
