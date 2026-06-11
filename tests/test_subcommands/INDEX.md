# `__init__.py`

## Summary

- `<cmoc-root>/tests/test_subcommands/__init__.py` は `tests.test_subcommands` を Python パッケージとして成立させるための最小モジュールです。
- 公開 API、定数、実行ロジック、再エクスポートは持ちません。

## Read this when

- `tests.test_subcommands` が Python パッケージとして import できる理由を確認したいとき。
- `<cmoc-root>/tests/test_subcommands` の入口だけを把握してから個別テストへ進みたいとき。

## Do not read this when

- `<work-root>/tests/test_subcommands` 配下の個別の `test_*.py` や `helpers.py` の内容を確認したいとき。
- `cmoc apply`、`cmoc session`、`cmoc review` など、サブコマンド実装や CLI 挙動を追いたいとき。
- このファイルに公開 API、定数、実行ロジック、再エクスポートがある前提で探したいとき。

## hash

- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `helpers.py`

## Summary

- `<work-root>/tests/test_subcommands` 配下の回帰テストで共通利用する import、fixture 補助、テスト用リポジトリ構築関数をまとめたヘルパーモジュールです。
- session/apply の状態作成、衝突再現、oracle snapshot 作成、補完実行プローブ、git 実行補助などの再利用ロジックが入っています。
- 個別テストを簡潔に保つための共通土台であり、サブコマンド横断テストの前処理と検証補助を担います。

## Read this when

- `<work-root>/tests/test_subcommands` 配下で共通利用する import とヘルパー関数を確認したいとき。
- テスト用 git リポジトリ、session/apply state、conflict 状態の作り方を把握したいとき。
- subcommand log、`StepTimer`、エラーレポート、補完プローブ、git 実行補助などの共通基盤を変更・レビューしたいとき。

## Do not read this when

- 個別の `test_*.py` の期待値や分岐だけを確認したいとき。
- `cmoc apply` / `cmoc session` / `cmoc review oracles` の本体仕様や実装だけを追いたいとき。
- `INDEX.md` の生成ルールやメタデータ管理方法そのものを確認したいとき。

## hash

- 4e108249a532c9f12bdf12736720f4571e33c052bf478e04490392cc77611b95

# `test_apply_abandon.py`

## Summary

- `<cmoc-root>/tests/test_subcommands/test_apply_abandon.py` は、`cmoc apply abandon` の回帰テスト群をまとめたファイルです。
- 未 join の apply run を安全に破棄し、`apply.state` を `ready` に戻して、apply branch と worktree を削除する挙動を検証します。
- 実行中 process の停止、legacy PID file の安全性、dirty な作業ツリーや別 session 混入時の拒否も確認します。

## Read this when

- `cmoc apply abandon` の破棄条件、state 遷移、cleanup の流れを確認したいとき。
- apply branch と worktree の削除、session branch への復帰、実行中 process の停止条件を確認したいとき。
- 別 session の apply branch を誤って消さない条件、dirty worktree の検出、`ready` / `error` / `running` / 未知 state の扱いを確認したいとき。

## Do not read this when

- `cmoc apply fork` や `cmoc apply join` の処理順、調査・取り込み・レポート生成だけを確認したいとき。
- `cmoc session fork`、`cmoc session join`、`cmoc session abandon` など、session 側の開始・統合・破棄ロジックを確認したいとき。
- `<work-root>/tests/test_subcommands` 全体の入口や、他のサブコマンド回帰テストを探したいとき。

## hash

- 3c34ff885a8c08fa3d0b563cbac11cfca79f046dfa63432f4140eb2f8d1b55b8

# `test_apply_fork.py`

## Summary

- `<cmoc-root>/tests/test_subcommands/test_apply_fork.py` は `cmoc apply fork` の回帰テストを集約したファイルです。
- 調査対象の選定、並列な不整合調査、改善ループ、レポート生成、状態更新、エラー時の扱いを検証します。
- Structured Output の要修正点スキーマ、scope 切り替え、change summary、path 制約、index maintenance との境界も含みます。

## Read this when

- `cmoc apply fork` の正常系・異常系・回帰観点を整理したいとき。
- 不整合調査の対象ファイル列挙、並列実行、要修正点改善ループ、レポート出力の流れを確認したいとき。
- `rolling` / `session` / `full` の scope 切り替え、`INDEX.md` や禁止パスの扱い、Structured Output schema の検証条件を追いたいとき。
- `apply.state` の遷移、commit の境界、`run` の隔離実行や worktree の取り扱いを把握したいとき。

## Do not read this when

- `cmoc apply join` や `cmoc apply abandon` など、別の `apply` サブコマンドの仕様やテストを確認したいとき。
- `cmoc session fork/join/abandon` や `cmoc review oracles` など、`apply fork` 以外のサブコマンドを確認したいとき。
- `<work-root>/src/sub_commands/apply/fork.py` の実装本体や `<work-root>/oracles/docs/app_specs/sub_commands/apply_fork.md` の仕様断片だけを直接読みたいとき。
- `<work-root>/tests/test_subcommands/helpers.py` や `<work-root>/tests/test_subcommands/INDEX.md` など、共通基盤や上位目次だけを確認したいとき。

## hash

- 0ba2d3db2a03e3d2a4560167ac6fcde021bc81d3345c42bc3aa24ec8109862c7

# `test_apply_join.py`

## Summary

- `<cmoc-root>/tests/test_subcommands/test_apply_join.py` は、`cmoc apply join` の回帰テスト群をまとめたファイルです。
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
- `<work-root>/src/sub_commands/apply/join.py` の実装本体や、`<work-root>/oracles/docs/app_specs/sub_commands/apply_join.md` の仕様断片だけを読みたいとき。
- `<work-root>/tests/test_subcommands` 全体の入口や共通ヘルパーだけを先に確認したいとき。

## hash

- ed1c75b6587bf77f9d2ab1f1c5e3bf240ffcb850294b4cede0259d9866ffb9f8

# `test_cli.py`

## Summary

- `<work-root>/tests/test_subcommands/test_cli.py` は cmoc の CLI 入口と周辺ランチャーの横断回帰テストをまとめたファイルです。
- `main` の Typer 委譲、root help、`review oracles` / `eval-oracles` の登録互換、`indexing` の公開有無を検証します。
- `apply fork` の help と正式オプション、`session` / `apply` 各コマンドの公開登録、`<work-root>/bin/cmoc` と `test.sh` の起動経路も確認します。

## Read this when

- `main` の root CLI 入口や Typer への委譲境界を確認したいとき。
- `cmoc --help`、completion probe、`review oracles` の alias、`indexing` の公開登録を確認したいとき。
- `apply fork` や `review oracles` の help 表示、正式オプション名、エラー報告の整形を変更したいとき。
- `<work-root>/bin/cmoc` ランチャーや `test.sh` の PATH 優先順位、仮想環境未検出時の挙動を確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや引数検証の詳細だけを追いたいとき。
- `commons.codex`、`commons.indexing`、`commons.repo` など別モジュールの実装を確認したいとき。
- `<work-root>/tests/test_codex.py` や `<work-root>/tests/test_repo.py` など、CLI 以外の回帰テストを探したいとき。

## hash

- 0db581815c6774df55ec0542f7aead6cfcad554f18e1809febb3e0952130a50f

# `test_core.py`

## Summary

- `<work-root>/tests/test_subcommands/test_core.py` は、サブコマンド横断の共通実行基盤、エラーレポート、`StepTimer` の回帰テストをまとめたファイルです。
- `cmoc init` の `.cmoc` ignore 修復・commit・tracked ファイル解除と、`cmoc indexing` の maintenance / check / dirty repo 判定も扱います。

## Read this when

- `run_command()`、`StepTimer`、`start_step()` の終了処理やログ・計測表示を変更したいとき。
- `cmoc init` の `.cmoc` ignore 修復、commit、tracked `.cmoc` の追跡解除の挙動を確認したいとき。
- `cmoc indexing` の通常実行、`--check`、dirty リポジトリ判定、INDEX 保守への委譲条件を確認したいとき。
- サブコマンド横断の共通動作と、初期化・インデックス保守の境界を把握したいとき。

## Do not read this when

- CLI のサブコマンド登録、補完、`help` 表示だけを確認したいとき。
- `apply` や `session` の個別サブコマンドの状態遷移や処理順だけを追いたいとき。
- `<work-root>/src/commons/command_runner.py`、`<work-root>/src/sub_commands/init.py`、`<work-root>/src/sub_commands/indexing.py` の実装本体を直接確認したいとき。

## hash

- 5770493150a54bcb583b59ce64c1f1dbafe9668054487a2af578b2c0eb9afe75

# `test_review_oracles.py`

## Summary

- `<cmoc-root>/tests/test_subcommands/test_review_oracles.py` は `cmoc review oracles` と旧別名 `cmoc eval-oracles` の回帰テストをまとめた入口です。
- review worktree の分離、oracles スナップショット固定、所見パイプライン（列挙・統合・検証・判定）を扱うテスト群への入口です。
- レポート生成、エラー報告、prompt と Structured Output schema、ループ回数や finding ID まわりの補助ロジックも案内します。

## Read this when

- `cmoc review oracles` / `cmoc eval-oracles` の挙動と回帰範囲を確認したいとき。
- review worktree、oracles snapshot、`INDEX.md` メンテナンス、レポート出力の流れを把握したいとき。
- 所見の列挙・マージ・検証・判定、Structured Output schema、prompt 文言、loop 変数の境界を追いたいとき。
- finding ID 管理、payload validation、改善後 issue の再配置などの補助処理を確認したいとき。

## Do not read this when

- `cmoc apply` / `cmoc session` / `cmoc init` / `cmoc indexing` のテストを探したいとき。
- `<work-root>/src/sub_commands/review/oracles.py` の実装本体だけを追いたいとき。
- `<work-root>/tests/test_subcommands` 全体の共通ヘルパーや他ファイルの回帰範囲だけを確認したいとき。
- `review oracles` の利用手順だけで足り、テストの詳細が不要なとき。

## hash

- d82b790c9613586349cc1a297fa62abb8a25a3c43cce7a5992d100bd80ad6986

# `test_session_abandon.py`

## Summary

- `<cmoc-root>/tests/test_subcommands/test_session_abandon.py` は `cmoc session abandon` の回帰テスト群をまとめたファイルです。
- session branch を merge せず破棄して home branch に戻す正常系と、`session.state` / `apply.state` の前提条件、`.cmoc` ignore 補修を扱います。
- cleanup 失敗時の rollback、branch 削除失敗、state 保存失敗、再実行案内まで含む境界条件を確認します。

## Read this when

- `cmoc session abandon` の挙動や cleanup の流れを変更・確認したいとき。
- `session.state`、`apply.state`、未コミット差分、home branch の存在確認などの前提条件を把握したいとき。
- cleanup 失敗時の rollback、エラーメッセージ、`.cmoc` 補修の回帰を確認したいとき。

## Do not read this when

- `cmoc session fork` や `cmoc session join` の仕様やテストだけを確認したいとき。
- `cmoc apply` 系サブコマンドや `cmoc review` / `cmoc init` のテストを確認したいとき。
- `<work-root>/src/sub_commands/session/abandon.py` の実装や `<work-root>/oracles/docs/app_specs/sub_commands/session_abandon.md` の仕様断片だけを確認したいとき。

## hash

- 479667e765c2fa673d66c44b5224e001c29c4b897b0f2b3e12cd0660d900fe2c

# `test_session_fork.py`

## Summary

- `<work-root>/tests/test_subcommands/test_session_fork.py` は `cmoc session fork` の回帰テスト群の入口です。
- session branch の作成、state 保存、`.cmoc` の ignore 補修、前提条件チェック、競合検出、rollback を横断的に確認します。
- このファイルから、`cmoc session fork` の正常系と失敗系をまとめてたどれます。

## Read this when

- `cmoc session fork` の回帰テストが何を守っているかを把握したいとき。
- session branch 作成、state 記録、`.cmoc` の ignore 補修の流れを確認したいとき。
- local branch 限定、detached HEAD、cmoc 管理 branch、未コミット差分、既存 active session などの拒否条件を確認したいとき。
- linked worktree から実行したときの state 保存先や、main repo-root 側の active session 判定を確認したいとき。
- state 保存失敗時の rollback、branch 削除失敗時の後始末、壊れた session state や orphan branch の扱いを確認したいとき。

## Do not read this when

- `cmoc session join` や `cmoc session abandon` など、session の別サブコマンドの回帰テストを確認したいとき。
- `<work-root>/src/sub_commands/session/fork.py` の実装本体や git 操作の詳細だけを追いたいとき。
- `<work-root>/tests/test_subcommands` 全体の入口や共通ヘルパーだけを先に把握したいとき。
- `<work-root>/oracles/docs/app_specs/sub_commands/session_fork.md` の仕様断片だけを読みたいとき。

## hash

- 1db6d3d5ce45d3308f36bfbf197ca6771aeefaab600f91605bef5dbe5ef2be05

# `test_session_join.py`

## Summary

- `<work-root>/tests/test_subcommands/test_session_join.py` は、`cmoc session join` の回帰テスト入口で、session 完了の通常系と異常系をまとめたファイルです。
- session state / apply state の前提条件、`.cmoc` の追跡解除、ブランチ移動と merge 後始末の挙動を検証します。
- merge conflict 時の Codex 依頼、禁止領域の編集検出、conflict marker 残存チェック、プロンプト生成の境界も押さえます。

## Read this when

- `cmoc session join` の実装・修正・レビューで、このテストが守る振る舞いを整理したいとき。
- session branch の merge 完了、home branch への復帰、`session.state` の `joined` 更新や branch 削除条件を確認したいとき。
- `session.state` / `apply.state` の前提条件、非 session branch、dirty worktree、null home branch などの拒否条件を確認したいとき。
- merge conflict の自動解消、Codex CLI への依頼内容、README/AGENTS/oracles などの禁止領域ルールを確認したいとき。
- conflict marker 残存検査、禁止領域への書き込み検出、プロンプト生成や補助関数の境界を確認したいとき。

## Do not read this when

- `cmoc session fork`、`cmoc session abandon`、`cmoc apply` 系など、別サブコマンドの挙動だけを確認したいとき。
- 実装本体の `<work-root>/src/sub_commands/session/join.py` や、仕様断片の `<cmoc-root>/oracles/docs/app_specs/sub_commands/session_join.md` だけを読みたいとき。
- `<work-root>/tests/test_subcommands/helpers.py` や、他のテスト入口・共通基盤だけを確認したいとき。
- `<work-root>/tests/test_subcommands` 全体の横断テスト構成ではなく、このファイル固有の回帰観点だけを追いたいとき。

## hash

- ffd80ab9f5211d7ee7f91fe4e1a7885bdcc5cc6cb11d4f784c7832de14ca93cf
