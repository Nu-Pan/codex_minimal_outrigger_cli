# `_support.py`

## Summary
- CLI 系 realization test で共有する最小限の helper と import を置く補助モジュール。`CliRunner`、一時 Git repository 作成、fake Codex home 作成、apply worktree 解決など、複数の責務別 test module が同じ前提で使う処理を集約する。
- テスト対象の仕様を直接検証するファイルではなく、責務別に分割された test module 間で重複しやすい setup 処理を一箇所に保つための共有部品である。

## Read this when
- CLI 系テストで使う `make_repo`、`run_git`、`setup_codex_home`、`apply_worktree_from_state` の挙動を確認・変更する。
- 複数の test module に同じ setup helper や共有 import を追加しそうになり、共通化できるか判断したい。

## Do not read this when
- 5449952c03b396f445c5e13a3c9e170508719554f100931745e0395be2c1fe3c
- プロンプト部品や実行パラメータ schema の期待値だけを確認したい場合は `test_prompt_parts.py` を読む。

## hash
- 5449952c03b396f445c5e13a3c9e170508719554f100931745e0395be2c1fe3c

# `test_basic_runtime.py`

## Summary
- path token 変換、duration 表示、repo root/work root 判定、設定 default、構造化エラー描画、CLI preflight、`.cmoc` ignore、file access mode 変換など、cmoc の基礎挙動を検証する realization test。

## Read this when
- `basic` model、`cmoc_runtime` の基本 helper、CLI 共通 preflight、構造化エラー表示、sandbox mode 変換を変更する。

## Do not read this when
- init/TUI、session、review、apply、indexing、Codex subprocess 呼び出しなど、個別サブコマンドの状態遷移や外部プロセス境界を確認したい。

## hash
- 4c7770885a8b5d5d472b8d3a5b5f44ec52624b62e9dac8a8964c5e746d956e39

# `test_cli_init_tui.py`

## Summary
- `cmoc init` の `.cmoc` ignore、tracked file cleanup、既存 staged change 保持、config default 同期と、`cmoc tui` の editor 実行、prompt 保存、Markdown prompt parsing を検証する realization test。

## Read this when
- init の git/index/config 副作用、linked worktree 対応、TUI の editor 起動・Codex 起動・prompt parsing を変更する。

## Do not read this when
- session/apply/review/indexing の状態遷移や Codex runtime wrapper 自体を確認したい。

## hash
- 13b0f315d8584042955d84aef7e3b5475079c95819b0158c528ec0ba68e05416

# `test_session_cli.py`

## Summary
- session fork/abandon/join の branch、worktree、state、conflict resolution、cleanup warning を検証する realization test。

## Read this when
- `cmoc session` 系サブコマンドの branch/worktree/state 遷移、abandon rollback、join conflict 解決、session branch cleanup を変更する。

## Do not read this when
- apply 専用の fork/join/abandon 状態、review oracle、indexing、Codex runtime wrapper を確認したい。

## hash
- f86cba5c60f882fd9f9bc960c1f50d62cb8da8a3cfd4d034d3261efa05b14bc8

# `test_review_oracle_cli.py`

## Summary
- review oracle の report 生成、scope 別対象選定、gitignored oracle file 除外、session scope 集計、review INDEX 変更 merge を検証する realization test。

## Read this when
- `cmoc review oracle` の対象 file 列挙、report schema、scope option、gitignore 扱い、review 結果の merge 処理を変更する。

## Do not read this when
- apply finding application loop、indexing entry 生成、prompt 部品の文言自体を確認したい。

## hash
- b6c694f89cdd628e4aa4a07e15aca5e63d55b6f76fbdf20d950c9c3293c384e7

# `test_apply_fork_cli.py`

## Summary
- apply fork の Codex loop、状態更新、report 生成、dirty recheck、禁止 diff 検出、rolling apply の previous join commit 利用を検証する realization test。

## Read this when
- `cmoc apply fork` の AI application loop、report/change summary、state 更新、dirty file convergence、`.agents` 差分拒否、rolling apply 基準 commit を変更する。

## Do not read this when
- apply abandon/join の cleanup や merge 後処理だけを確認したい場合は、それぞれの専用 test module を読む。

## hash
- 6086875a241c0da01ba489e43de75dbd0bcaf2c8ec7efd5aaa8b4b043661863b

# `test_apply_abandon_cli.py`

## Summary
- apply abandon の apply worktree/branch cleanup、missing cleanup warning、running process 停止、running state の process id 必須条件、apply worktree からの実行を検証する realization test。

## Read this when
- `cmoc apply abandon` の cleanup、state 遷移、process 終了、warning 表示、実行 worktree 解決を変更する。

## Do not read this when
- apply fork の Codex loop や apply join の merge/reset 処理を確認したい。

## hash
- 4e240fe87573ccaac1c39ef4601bf1ee76505f1870d0f9869434b509d41a7ce9

# `test_apply_join_cli.py`

## Summary
- apply join の apply worktree/branch cleanup、apply worktree からの実行、clean worktree 要求、unexpected diff 報告と force revert、`.gitignore` 差分扱いを検証する realization test。

## Read this when
- `cmoc apply join` の merge/cleanup/state reset、dirty apply worktree 拒否、予期しない差分検出、force revert を変更する。

## Do not read this when
- apply fork の AI loop や apply abandon の process cleanup を確認したい。

## hash
- c00ce9596a605e60be91edf70c7d2663290bbc0470d09921cf17c734340d933f

# `test_indexing_cli.py`

## Summary
- INDEX.md conflict 解決、index entry builder 呼び出し、linked worktree 対象化、fresh hash skip、malformed hash 再生成、sibling 並列更新、memo directory indexing、Codex call 前の indexing preflight を検証する realization test。

## Read this when
- indexing 実行、INDEX.md conflict resolution、hash freshness 判定、並列 entry 更新、memo ディレクトリ扱い、Codex call 前後の indexing preflight を変更する。

## Do not read this when
- review oracle の finding merge や Codex subprocess wrapper の stdin/log/schema 保存だけを確認したい。

## hash
- 4c524dccfcacbd63a6adf942844ce8f10a33bcb1ec0c0ad9bea2968a45c5bc67

# `test_codex_runtime_exec.py`

## Summary
- Codex exec/TUI runtime wrapper の stdin 渡し、profile/schema/log 保存、cwd work root への schema 保存、TUI prompt argument、repo config 読み込みを検証する realization test。

## Read this when
- `run_codex_exec` または `run_codex_tui` の subprocess 引数、stdin、log、schema 保存先、config 読み込みを変更する。

## Do not read this when
- CODEX_HOME/auth validation や quota retry/resume の境界条件だけを確認したい。

## hash
- 29137aaebebdc51db383ac92823d6e28dc19ec74cf93e418e890ae12d9141e20

# `test_codex_runtime_home.py`

## Summary
- Codex runtime wrapper の CODEX_HOME default、既存 CODEX_HOME 維持、missing home、file home、missing auth.json の事前失敗を検証する realization test。

## Read this when
- Codex CLI 呼び出し前の CODEX_HOME 解決、環境変数引き継ぎ、auth.json validation、事前エラー文面を変更する。

## Do not read this when
- subprocess stdin/log/schema 保存や quota retry/resume の挙動を確認したい。

## hash
- edede0989727c4367d407b9fa2be3dfac723e7f2300fb9f5fda3bd51396503f4

# `test_codex_runtime_retry.py`

## Summary
- Codex exec runtime wrapper の semantic output retry、quota polling/resume、resume token 不在時の失敗、representative quota probe を検証する realization test。

## Read this when
- Structured Output validation retry、quota エラー時の resume loop、quota probe 選定、quota 失敗時のエラーを変更する。

## Do not read this when
- CODEX_HOME/auth validation や通常の subprocess/log/schema 保存だけを確認したい。

## hash
- c35c3e2f390d2676ec57591e68b9a72fa69a58961a94d06df91197afea0a31e7

# `test_prompt_parts.py`

## Summary
- プロンプト部品と実行パラメータ生成が、期待する文書タイトル・必須文言・既定の含有/省略条件・Structured Output schema の論理構造を満たすことを検証する realization test。
- レビュー基準、ルーティング規則、ファイルアクセス規則、実現基準、索引エントリー基準、review oracle 基準など、利用者へ渡すプロンプト断片のレンダリング内容を外部挙動として固定する入口になる。
- TUI のパラメータ解決、indexing 用パラメータ、review oracle merge finding 用パラメータについて、モデル種別・reasoning effort・アクセスモード・schema 内容が意図どおり選ばれることも確認する。

## Read this when
- プロンプト断片を生成する builder の戻り値、タイトル、Markdown レンダリング結果、または必須文言を変更する。
- complete prompt が標準類を既定で含むか、フラグ指定時だけ含むかという合成条件を変更する。
- ファイルアクセスモードごとの禁止事項文言や、READONLY / PURE_ORACLE_READ / REALIZATION_WRITE / ORACLE_WRITE / REPO_WRITE の扱いを変更する。
- TUI パラメータ解決、indexing、review oracle merge finding の model class、reasoning effort、file access mode、または schema の required / enum / boolean flag 構造を変更する。
- 索引エントリー生成基準で、何を書くべきか、何を出力に混ぜないか、対象内容を根拠にするかというルールを調整する。

## Do not read this when
- CLI コマンド実行、Git 操作、worktree 操作、ファイルシステム操作など、プロンプト部品の文書レンダリングや実行パラメータ生成と無関係な挙動だけを調べる。
- 61760f748d4b30088b5a4fe9fbd6bd65b8e7a2f926559d577ef17c7b7b2375c8
- StructDoc や Markdown renderer の汎用的な実装詳細だけを変更し、このテストで固定している具体的なプロンプト文言やパラメータ選定には触れない。
- アプリケーション本体の業務ロジックや UI 表示を調べており、プロンプト合成・標準文書 builder・パラメータ schema の期待値に関係しない。

## hash
- 61760f748d4b30088b5a4fe9fbd6bd65b8e7a2f926559d577ef17c7b7b2375c8
