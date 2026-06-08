# `__init__.py`

## Summary

- `tests/test_subcommands/__init__.py` は `tests/test_subcommands` をテストパッケージとして成立させるための初期化ファイルです。
- このファイル自体にはテストロジックはなく、サブコマンド関連テスト群のパッケージ境界を示します。

## Read this when

- `tests.test_subcommands` をパッケージとして import する前提を確認したいとき。
- 相対 import や共有テスト補助の前提として、このテストパッケージの入口を確認したいとき。
- サブコマンド系テスト群が同一パッケージとしてまとめられているかを把握したいとき。

## Do not read this when

- 個々のテストケース本文やアサーションを確認したいとき。
- `tests/test_subcommands` 配下の他のテストモジュールや `helpers.py` を直接たどりたいとき。
- パッケージ初期化ではなく、サブコマンド本体の仕様や実装を確認したいとき。

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

- `tests/test_subcommands/test_apply_abandon.py` は、`cmoc apply abandon` の回帰テスト群です。
- 未 join の apply run を安全に破棄できること、`apply.state` を `ready` に戻すこと、apply branch と worktree を削除することを検証します。
- session / apply の state 境界、実行中 process の停止、legacy PID file の安全性、dirty な作業ツリーや別 session 混入時の拒否も確認します。

## Read this when

- `cmoc apply abandon` の破棄条件、state 遷移、cleanup の流れを確認したいとき。
- apply branch / apply worktree の削除、session branch への復帰、実行中 process の停止条件を確認したいとき。
- 別 session の apply branch を誤って消さない条件、dirty worktree の検出、`ready` / `error` / `running` / 未知 state の扱いを確認したいとき。

## Do not read this when

- `cmoc apply fork` / `cmoc apply join` の処理順やレポート生成だけを確認したいとき。
- `cmoc session fork/join/abandon` など、session 側の開始・統合・破棄ロジックだけを確認したいとき。
- `tests/test_subcommands.py` の横断的な入口や、他のサブコマンド回帰テストを確認したいとき。

## hash

- fd783bed47bada01e6e4b1b52a28b7abe373f24879451a96ea89003e0d19405b

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

- `cmoc apply join` や `cmoc apply abandon` など、別の `apply` サブコマンドのテストを確認したいとき。
- `cmoc session fork/join/abandon` や `cmoc review oracles` など、`apply fork` 以外の挙動を追いたいとき。
- `src/sub_commands/apply/fork.py` の実装本体や、`oracles/docs/app_specs/sub_commands/apply_fork.md` の仕様断片だけを読みたいとき。
- `tests/test_subcommands` の共通ヘルパーや CLI 横断テストではなく、このファイル固有の確認だけで足りるとき。

## hash

- 4d77497ad074cb70ef600b15e682d899192f30e677ea6dd662d74c3c9c0ab0b1

# `test_apply_join.py`

## Summary

- `tests/test_subcommands/test_apply_join.py` は `cmoc apply join` の回帰テスト群です。
- session/apply state の検証、想定外差分の判定、`--force-resolve`、`INDEX.md` conflict の自動解決と cleanup をまとめて確認します。
- apply branch と session branch のどちらで実行してもよい経路や、worktree / report / branch 削除の境界条件も扱います。

## Read this when

- `cmoc apply join` の正常系・失敗系・cleanup 条件を確認したいとき。
- 想定外差分の判定基準、`--force-resolve` の挙動、`INDEX.md` conflict の自動解決を追いたいとき。
- apply branch / session branch / linked worktree / report / result の分岐や、rename/copy・NUL 安全な path・制御文字を含む差分表示の回帰を確認したいとき。
- このファイルが何を守っているかを先に整理してから、個別テストケースへ進みたいとき。

## Do not read this when

- `cmoc apply join` の実装ロジックそのものを追いたいとき。
- `cmoc apply join` の利用手順や仕様断片だけを確認したいとき。
- `cmoc session` や `cmoc apply fork/abandon` など、別サブコマンドのテストを探しているとき。
- `tests/test_subcommands` 全体の横断入口や、上位の `INDEX.md` だけを確認したいとき。

## hash

- d8023325e1a46b9ecc8cf8d44cc1c1d5e171c6dae1f06ca7d377c9015f5f405b

# `test_cli.py`

## Summary

- `tests/test_subcommands/test_cli.py` は、`main.py` と `bin/cmoc` を中心にした CLI 横断の回帰テストをまとめるファイルです。
- サブコマンド登録、hidden alias、補完、終了コード、エラーレポート整形など、ユーザーが最初に触れる CLI 入口の挙動をまとめて検証します。
- 個別サブコマンドの詳細実装へ進む前に、CLI 全体の接続点と共通の表示仕様を確認するための目次として機能します。

## Read this when

- `cmoc --help`、`cmoc review oracles --help`、`cmoc indexing --help` など、CLI 登録とヘルプ表示の挙動を確認したいとき。
- `session`、`apply`、`review` の各コマンド群に対する補完プローブや、Typer への委譲方針を確認したいとき。
- 引数なし起動やサブコマンドエラー時に、stdout へ Markdown 形式のエラーレポートが出るかを確認したいとき。
- `main.py`、`bin/cmoc`、`format_error_report`、`eval-oracles` / `eval-oracle` の互換 alias を含む CLI 横断の回帰を把握したいとき。

## Do not read this when

- `cmoc apply`、`cmoc session`、`cmoc review oracles`、`cmoc indexing` など、個別サブコマンドの実装や状態遷移そのものを追いたいとき。
- `tests/test_subcommands/test_apply_fork.py` や `tests/test_subcommands/test_session_join.py` など、サブコマンド固有の回帰テストを確認したいとき。
- `format_error_report` や補完プローブの共通ヘルパーだけを直接確認したいとき。
- `bin/cmoc` の起動スクリプトや `main.py` の CLI 登録ではなく、個別仕様ファイルだけを確認したいとき。

## hash

- 6f76212a4a678302e172a0e73b84352370f2f4c8764a6bf833feb33d402021a6

# `test_core.py`

## Summary

- サブコマンド共通の実行基盤、エラーレポート、ステップ計測の回帰テストをまとめたファイルです。
- `run_command()` の終了コード、ログ出力、総経過時間、例外時の報告、`apply` の非エラー終了を確認します。
- `cmoc init` の `.cmoc` ignore 修復・commit・tracked ファイル解除と、`cmoc indexing` の maintenance / check / dirty repo 判定も扱います。

## Read this when

- `run_command()`、`StepTimer`、`start_step()` の終了処理やログ・計測表示を変更するとき。
- `cmoc init` の `.cmoc` ignore 追加、既存 `.gitignore` の扱い、tracked `.cmoc` の解除を確認したいとき。
- `cmoc indexing` の通常実行、`--check`、dirty リポジトリ判定、INDEX 保守の委譲条件を確認したいとき。
- サブコマンド横断の共通動作や、初期化とインデックス保守の境界を把握したいとき。

## Do not read this when

- CLI 引数登録、補完、ヘルプ表示だけを確認したいとき。
- `apply` や `session` の個別サブコマンドの状態遷移や処理順だけを追いたいとき。
- `src/commons/command_runner.py`、`src/sub_commands/init.py`、`src/sub_commands/indexing.py` の実装本体を直接読みたいとき。

## hash

- a40341ead2f19209eb543aa97396134abbb4f587575ed0eac49d3a8a1adf6d96

# `test_review_oracles.py`

## Summary

- `tests/test_subcommands/test_review_oracles.py` は、`cmoc review oracles` と旧別名 `cmoc eval-oracles` の回帰テスト群です。
- review 専用ワークツリーでの実行、`oracles` の固定 snapshot、所見の列挙・マージ・検証・判定、レポート生成とエラー処理をまとめて検証します。
- このファイルは、`review oracles` 固有の前提条件と出力仕様を確認するための入口です。

## Read this when

- `cmoc review oracles` と旧別名 `cmoc eval-oracles` の回帰テスト内容を把握したいとき。
- review ワークツリーの隔離、`oracles` スナップショット固定、所見パイプライン、レポート生成、エラー報告の挙動を確認したいとき。
- Structured Output schema、所見の列挙・マージ・検証・判定、プロンプト文言、`INDEX.md` 参照ルールの変更影響を確認したいとき。
- session branch 前提、`INDEX.md` メンテナンス、部分評価・全件評価・改善ループの分岐をテスト観点で追いたいとき。

## Do not read this when

- `cmoc apply`、`cmoc session`、`cmoc init`、`cmoc indexing` など、別サブコマンドのテストだけを確認したいとき。
- `src/sub_commands/review/oracles.py` の実装本体だけを直接追いたいとき。
- `tests/test_subcommands` の共通ヘルパーや他の個別テストファイルを先に確認したいとき。

## hash

- 37578fa16cbe4fc89080a54657695425e4f29cfdf24fc34851cfa8326329e852

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

- 361451016d2c4d8f1341ea6cc4cf59a9f6cc7de37dae4605956458335633d0d1

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
