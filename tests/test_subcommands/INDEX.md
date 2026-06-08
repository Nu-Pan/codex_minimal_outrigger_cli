# `__init__.py`

## Summary

- `tests/test_subcommands/__init__.py` は `tests/test_subcommands` パッケージの空のマーカーです。
- サブコマンド横断テスト群の入口を示すだけで、公開 API や実行ロジックは持ちません。

## Read this when

- `tests/test_subcommands` パッケージ全体の入口としての役割を確認したいとき。
- このディレクトリが Python パッケージとして成立していることを把握したいとき。
- 個別テストへ進む前に、この階層の案内役だけを確認したいとき。

## Do not read this when

- 個別のサブコマンド回帰テストの本文やアサーションを確認したいとき。
- `helpers.py` や各 `test_*.py` の詳細な役割を直接追いたいとき。
- `src/sub_commands/` 側の実装や `oracles` 側の仕様断片を確認したいとき。

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
- subcommand log、StepTimer、エラーレポート、補完プローブなどの共通テスト基盤を変更・レビューしたいとき。

## Do not read this when

- 個別のサブコマンド仕様や本番実装の挙動だけを確認したいとき。
- `tests/test_subcommands` の個別テストケースの期待値や分岐だけを追いたいとき。
- `INDEX.md` の生成ルールやメタデータ管理方法そのものを確認したいとき。

## hash

- d311673e0302d66a652af18b19d57f8607eeec7594ae1055f0ea039e1aebb254

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

- `tests/test_subcommands/test_apply_fork.py` は、`cmoc apply fork` の回帰テスト群を意味カテゴリ別にまとめた入口です。
- apply 開始時の前提条件、調査対象の scope 判定、要修正点の抽出・改善・適用ループ、report 出力と session/apply state の更新を検証します。
- 不整合調査の JSON schema、絶対パス制約、並列実行、`INDEX.md` メンテナンス、終了時の session HEAD 記録や再調査対象の選定もこのファイルの守備範囲です。

## Read this when

- `cmoc apply fork` の開始条件、scope 選択、反復回数、report 生成、状態遷移を確認したいとき。
- 不整合調査の Structured Output schema、要修正点リスト、evidence path、対象ファイルの選定ロジックを確認したいとき。
- apply 実行中の `INDEX.md` メンテナンス、修正適用後の再調査、要修正点改善ループ、session HEAD 記録の挙動を追いたいとき。
- apply fork の並列調査、ログ記録、rollback 条件、完了・未収束の分岐をテスト観点で把握したいとき。

## Do not read this when

- `cmoc apply fork` 以外の `apply join` / `apply abandon` の挙動を確認したいとき。
- `cmoc session fork/join/abandon` や他サブコマンドの状態遷移を調べたいとき。
- CLI 登録、`main.py`、`bin/cmoc`、`test.sh` などの横断的な起点だけを追いたいとき。
- `src/sub_commands/apply/fork.py` の実装本体や、`src/commons/indexing.py` の一般的なメンテナンス処理だけを直接確認したいとき。

## hash

- 7169bd0764d93d4d2e961b5c2c4955f90030400173cea903a93a56f2bafec526

# `test_apply_join.py`

## Summary

- `tests/test_subcommands/test_apply_join.py` は `cmoc apply join` の回帰テスト群です。
- session/apply state の検証、想定外差分の判定、`--force-resolve`、`INDEX.md` conflict の自動解消と cleanup をまとめて確認します。
- apply branch と session branch のどちらで実行してもよい経路や、worktree / report / branch 削除の境界条件も扱います。

## Read this when

- `cmoc apply join` の正常系・失敗系・cleanup 条件を確認したいとき。
- 想定外差分の判定基準、`--force-resolve` の挙動、`INDEX.md` conflict の自動解消を追いたいとき。
- apply branch / session branch / linked worktree / missing report / missing result の分岐を確認したいとき。
- rename/copy、NUL 安全な unmerged path、制御文字を含む差分表示など、境界条件の回帰を確認したいとき。

## Do not read this when

- `cmoc apply join` の実装ロジックそのものを追いたいときは、`src/sub_commands/apply/join.py` を読むべきです。
- `cmoc apply join` の利用手順や仕様断片だけを確認したいときは、`oracles/docs/app_specs/sub_commands/apply_join.md` を読むべきです。
- `cmoc session fork/join/abandon` や `cmoc apply fork/abandon` など、別サブコマンドのテストを探しているとき。
- `tests/test_subcommands.py` 全体の横断入口や、`tests/INDEX.md` の上位目次だけを確認したいとき。

## hash

- c573a747525e7202fb3b31b20ffff2d4cccb190ae34a61d694325e12f707e300

# `test_cli.py`

## Summary

- `tests/test_subcommands/test_cli.py` は、`main.py` と `bin/cmoc` を中心にした CLI 横断の回帰テストをまとめるファイルです。
- サブコマンド登録、hidden alias、補完、終了コード、エラーレポート整形など、ユーザーが最初に触れる CLI 入口の挙動をまとめて検証します。
- 個別サブコマンドの詳細実装へ進む前に、CLI 全体の接続点と共通の表示仕様を確認するための目次として機能します。

## Read this when

- `cmoc --help`、`cmoc indexing --help`、`cmoc review oracles --help` など、CLI 登録とヘルプ表示の挙動を確認したいとき。
- `session`、`apply`、`review` の各コマンド群に対する補完プローブや、Typer への委譲方針を確認したいとき。
- 引数なし起動やサブコマンドエラー時に、stdout へ Markdown 形式のエラーレポートが出るかを確認したいとき。
- `main.py`、`bin/cmoc`、`format_error_report`、`eval-oracles` / `eval-oracle` の互換 alias を含む CLI 横断の回帰を把握したいとき。

## Do not read this when

- 個別の `cmoc apply`、`cmoc session`、`cmoc review oracles`、`cmoc indexing` の実装や状態遷移そのものを追いたいとき。
- `tests/test_subcommands/test_apply_fork.py` や `tests/test_subcommands/test_session_join.py` など、サブコマンド固有の回帰テストを確認したいとき。
- `format_error_report` や補完プローブの共通ヘルパーだけを直接確認したいとき。
- `bin/cmoc` の起動スクリプトや `main.py` の CLI 登録ではなく、個別仕様ファイルだけを確認したいとき。

## hash

- 3a184fde576965fa8404286b990cb8f139888422e1a644a6ffa8a756f3394b1f

# `test_core.py`

## Summary

- `tests/test_subcommands/test_core.py` は、サブコマンド共通の実行基盤と `cmoc init` / `cmoc indexing` の主要な回帰テストをまとめたファイルです。
- `run_command()` のエラー報告、終了コード、ログ記録、総経過時間、repo root 解決失敗、`apply` の非エラー終了を検証します。
- あわせて `cmoc init` の ignore 修復・commit・tracked `.cmoc` の解除や、`cmoc indexing` の maintenance / check / dirty repo 判定も扱います。

## Read this when

- `run_command()`、`StepTimer`、`start_step()` を中心に、サブコマンド共通の終了処理・ログ出力・経過時間表示を確認したいとき。
- `cmoc init` の `.cmoc` ignore 追加、tracked `.cmoc` の解除、既存 `.gitignore` や staged 差分の保持・復旧条件を確認したいとき。
- `cmoc indexing` の通常実行、`--check`、不整合検出、dirty repo での停止条件を確認したいとき。
- `tests/test_subcommands/test_core.py` が、サブコマンド横断の共通動作と初期化・インデックス保守の境界をどう守っているかを把握したいとき。

## Do not read this when

- `tests/test_subcommands/test_cli.py` など、CLI 引数や補完の挙動だけを確認したいとき。
- `tests/test_subcommands/test_apply_*.py` や `tests/test_subcommands/test_session_*.py` など、個別サブコマンドの詳細な回帰テストを追いたいとき。
- `src/commons/command_runner.py`、`src/sub_commands/init.py`、`src/sub_commands/indexing.py` など、実装そのものを直接確認したいとき。
- `oracles/docs/app_specs/sub_commands/INDEX.md` 以下の個別仕様を読みたいとき。

## hash

- e6245bbad872991c845d61ec8ce4de95f5cd06d9d2ea9bc96a19c9dd70939489

# `test_review_oracles.py`

## Summary

- `tests/test_subcommands/test_review_oracles.py` は、`cmoc review oracles` と旧別名 `cmoc eval-oracles` の回帰テスト群です。
- review 用ワークツリーの隔離実行、`oracles` スナップショットの固定、所見パイプライン、レポート生成、エラー時の報告を検証します。
- このサブディレクトリでは、`review oracles` に固有の挙動を追う入口になります。

## Read this when

- `cmoc review oracles` の実行条件、出力、終了時の挙動を確認したいとき。
- review ブランチ・review ワークツリー・`oracles` スナップショット・`INDEX.md` メンテナンスの関係を追いたいとき。
- 所見の列挙、マージ、検証、判定、Structured Output schema、プロンプト文言の変更がテストに与える影響を見たいとき。

## Do not read this when

- `cmoc apply`、`cmoc session`、`cmoc init`、`cmoc indexing` など、別サブコマンドのテストだけを探しているとき。
- `sub_commands.review.oracles` の実装本体や共通基盤の処理だけを確認したいとき。
- `tests/test_subcommands` の共通 helpers や、`review oracles` 以外の個別テストを追いたいとき。

## hash

- 677644cd2f6b4a354069420e7ac54b599acb0325ecd7031c5ec69aab8b3ea935

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

- `tests/test_subcommands/test_session_fork.py` は `cmoc session fork` の回帰テスト群で、session branch の作成、session state の記録、`.cmoc` の ignore 補修、active session 競合、detached HEAD や managed branch からの開始拒否、linked worktree での state 保存先、失敗時 rollback を検証します。

## Read this when

- `cmoc session fork` の実装・修正・レビュー・テストを行うとき。
- session branch の作成条件、session state の記録、rollback、linked worktree での挙動、エラー文言を確認したいとき。
- `src/sub_commands/session/fork.py` と `oracles/docs/app_specs/sub_commands/session_fork.md` に進む前に、この回帰テストの観点を把握したいとき。

## Do not read this when

- `cmoc session join` / `cmoc session abandon` / `cmoc apply` 系の挙動だけを確認したいとき。
- 実装ロジックそのものや `src/sub_commands/session/INDEX.md` の入口構造だけを確認したいとき。
- `tests/test_subcommands/helpers.py` や他のサブコマンド回帰テストを探しているとき。

## hash

- 4287f8ae9d6031511b6942a7eb553f7f57094dcf2883c246779034e376041fd0

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
