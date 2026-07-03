# `_support.py`

## Summary
- CLI テストで共有される補助関数群。最小 Git リポジトリの作成、Git 状態確認、Codex home と fake profile の準備、fake 外部コマンド作成、session state から apply worktree を解決する処理をまとめる。

## Read this when
- CLI テストで使う一時 Git リポジトリ、初期コミット、branch 状態、tracked かつ ignored な oracle file の fixture を確認・変更したいとき。
- Codex 実行や TUI 実行をテスト内で fake profile に差し替える方法、`CODEX_HOME` の最小セットアップ、fake 実行ファイルの作り方を確認したいとき。
- apply 系テストで session state に記録された apply branch から worktree path を求める補助処理を探しているとき。

## Do not read this when
- 個別 CLI コマンドの期待挙動や assertion 内容を確認したいだけなら、該当するテスト本文を読む。
- プロダクト実装の Git 操作、Codex profile 生成、apply worktree 管理の仕様や実装を確認したいなら、対応する実装モジュールを読む。
- pytest fixture の網羅的な定義やテスト設定全体を確認したいだけなら、テスト設定用の別ファイルを読む。

## hash
- 5dbdaa085d2071735998882ad1e46e3d4b4bc9980f15dabcb148a45de893a484

# `test_acp_builder_parameters.py`

## Summary
- ACP builder が生成する agent call parameter、prompt の埋め込み内容、file access mode、reasoning effort、structured output schema 参照が、正本仕様断片や既存互換の期待に合っているかを検証するテスト群。
- apply fork、TUI parameter 解決、index entry 生成、oracle review、session join conflict resolution など、複数の builder の公開挙動を横断的に確認する。

## Read this when
- ACP builder の返す model class、reasoning effort、file access mode、structured output schema path、prompt 文面を変更する。
- 正本 schema と realization builder の schema 参照が一致しているかを確認したい。
- TUI parameter 解決、index entry 生成、oracle review finding 系、apply fork 系、session join conflict resolution 系の builder 変更に伴う回帰テストを探している。
- builder module の公開 export を絞る互換性要件を確認したい。

## Do not read this when
- 個別 builder の実装責務や prompt 組み立て処理を読みたい場合は、対象 builder の実装へ直接進む。
- 正本 schema 自体の内容を確認・変更したい場合は、oracle 側の schema 定義を読む。
- INDEX.md エントリー生成ロジックそのものを変更したい場合は、indexing builder や関連実装を読む。

## hash
- 57c4ec7a2e17dfe4510e65e26483bb9661348b995d0783d9766548dcd9488029

# `test_apply_abandon_cli.py`

## Summary
- apply abandon が active apply run を破棄する CLI 外部挙動を検証するテスト群。worktree、branch、session state の cleanup、実行位置の補正、linked session worktree の扱い、running apply process と記録済み child process group の停止を同じ操作の境界条件として扱う。
- 16,000 文字を超えるが、対象責務は apply abandon の成功、警告、拒否条件に閉じており、同じ state fixture と境界条件を共有するため一箇所にまとまっている。

## Read this when
- apply abandon の CLI 出力、終了コード、state 遷移、worktree/branch 削除、cleanup 警告の期待値を確認または変更するとき。
- running 状態の apply abandon が process identity を読み、child process group と親 process を停止してから cleanup する挙動を確認または変更するとき。
- apply worktree、linked session worktree、linked apply worktree、stale apply branch など、abandon 実行位置ごとの許可・拒否条件を確認するとき。
- apply process id file の読み取り、advisory lock 待機、PID reuse、終了済み process、zombie leader の扱いに関するテストを探すとき。

## Do not read this when
- apply fork 自体の Codex 実行、findings 生成、active run 作成の仕様を確認したいだけなら、apply fork 側の実装またはテストを読む。
- session fork、init、git worktree 作成 helper など、abandon の前提を作る補助処理そのものを調べたい場合は、それぞれの責務を持つ実装やサポートコードを読む。
- apply abandon 以外の apply サブコマンドの外部挙動や CLI 仕様を確認したい場合は、そのサブコマンドに対応するテストを読む。

## hash
- dfb4db2e9b41c4b652b91c0b52a49bef4332ff6c432f132f747de3365c84d9fa

# `test_apply_fork_cli.py`

## Summary
- apply fork コマンドの CLI 経由の実行、Codex 呼び出し、session state 更新、apply branch/worktree 作成、設定読み込み失敗時の中断、.gitignore の扱い、対象 path 正規化を検証する realization test。
- apply fork が session branch と現在の HEAD を基準に apply run を開始し、完了時に一時的な pid や旧 apply worktree 表現を残さないことを確認する。
- realization file 判定に関わる memo、oracle、管理ディレクトリ、INDEX/AGENTS、binary file、tracked ignored file の対象選別を確認する入口になる。

## Read this when
- apply fork の外部挙動、state 遷移、apply branch 名、apply worktree 配置、Codex loop 呼び出し順を変更する。
- linked worktree 上で apply fork を実行する挙動や、oracle snapshot commit と apply branch の起点を確認する。
- apply fork 実行時の .cmoc ignore 保証、session 側 .gitignore の非破壊性、apply branch 側での .gitignore 編集可否を変更または検証する。
- apply fork の設定ファイル読み込みエラー時に apply run を開始しない挙動、標準出力へのエラー表示、pid/state/branch の未生成を確認する。
- apply fork の対象正規化で、root 直下 memo、管理 path、INDEX/AGENTS、oracle path、binary file、tracked ignored file の扱いを確認する。

## Do not read this when
- apply fork 以外のサブコマンドの CLI 挙動だけを確認したい。
- Codex 実行器そのものの統合挙動や LLM 出力品質を確認したい場合で、apply fork 側の呼び出し・状態更新は関係しない。
- path model や realization/oracle file の定義そのものを確認したい場合は、正本仕様側を先に読む。

## hash
- 8132fa30a1ec010f5fecea77ff23e4bf3b34c02c05eaad6deab39af8f9353f9b

# `test_apply_fork_report_cli.py`

## Summary
- apply fork の CLI 経由の統合テスト。所見列挙、所見適用、commit、変更要約、report 出力、session state 更新までの一連の制御を検証する。
- apply fork 用 ACP builder の import 可能性、prompt 内容、schema 参照、packaged layout での動作もこのファイルで確認する。
- 変更ファイル再調査、未収束、収束、error report、file access rule violation recovery、rolling apply fork など、apply fork report と再検査 loop に関する期待値の入口になる。

## Read this when
- apply fork の report 内容、終了コード、収束・未収束・error の扱いを変更または確認したいとき。
- apply fork が変更後ファイルや新規ディレクトリ配下を再調査する制御を変更または確認したいとき。
- apply fork の変更要約が未 commit 差分、未追跡 file、削除済み tracked file をどう扱うか確認したいとき。
- apply fork の所見適用後 commit、session state、rolling fork の基準 commit 更新を変更または確認したいとき。
- apply fork 関連 ACP builder の prompt、schema path、import 経路、packaged layout 対応を変更または確認したいとき。
- file access rule violation recovery が許可差分だけを commit する挙動を確認したいとき。

## Do not read this when
- apply fork 以外のサブコマンドや session fork/join 単体の挙動だけを確認したいとき。
- apply fork の内部 helper の純粋な単体ロジックだけを確認でき、CLI report や loop 制御を見なくてよいとき。
- Codex 実行基盤全般や ACP builder 全般の仕様を確認したいだけで、apply fork 固有の prompt・schema・report 期待値に関係しないとき。
- oracle file や INDEX.md の正本仕様そのものを確認したいとき。

## hash
- f8dfe753b40a2eace94c5b42d13807d14e5d30c741119b8ecde6d319a502251b

# `test_apply_join_cli.py`

## Summary
- apply run を session へ join する CLI 外部挙動を検証するテスト群。正常 join、apply worktree からの実行、linked session worktree への反映、後片付け、state 更新、report 生成を扱う。
- join 可否を分ける境界条件として、stale apply branch、dirty apply worktree、想定外差分、force resolve、削除差分、rename target、memo 判定、gitignore 変更、merge conflict、INDEX.md conflict の扱いを同じ文脈で確認する。
- ファイル自体は大きいが、同じ fixture と git 状態を使う apply join の成功条件・拒否条件を一箇所で読むための凝集したテストとして位置づけられている。

## Read this when
- apply join の CLI 挙動、終了コード、標準出力、report 内容、state 更新、worktree/branch cleanup を変更または確認したいとき。
- apply join が session worktree と apply worktree のどちらから実行されたかで cleanup や merge 先がどう変わるかを確認したいとき。
- apply join で許可される差分と拒否される差分の境界、または --force-resolve による revert 挙動を確認したいとき。
- apply join の merge conflict 検出、INDEX.md conflict の自動解決、想定外差分 report の内容を変更または検証したいとき。
- apply join 周辺の helper が、変更パスの抽出、memo 判定、expected apply/session change 判定をどう扱うべきか確認したいとき。

## Do not read this when
- apply fork の Codex 実行や apply worktree 作成そのものを確認したいだけのとき。
- session fork、init、repository fixture など join 前提を作る別 CLI の単独挙動を確認したいとき。
- apply join の内部実装だけを局所的に読みたい場合で、外部挙動テストの期待値を確認する必要がないとき。
- oracle 正本仕様や realization standard の本文を確認したいとき。
- INDEX.md ルーティング文書の生成規則や他ファイルへの入口を確認したいとき。

## hash
- 46beb0d4dff71ffe132541609d84cd7a44f9f350ad4618a383b8daf3c40c943f

# `test_basic_runtime.py`

## Summary
- cmoc の基礎 runtime 契約を横断的に検証する regression test。path placeholder 解決、run/work/repo root、worktree 作成・削除防御、config validation、CmocError 表示、CLI error 出力、subcommand log、FileAccessMode と Codex profile、binary 判定、session/apply branch state 解決を同じ runtime 前提として扱う。
- 個別機能単位ではなく、CLI 実行前提や sandbox/profile 境界が一緒に崩れやすい共通 runtime 層の挙動をまとめて固定する入口。

## Read this when
- root placeholder、repo root、work root、run root、linked worktree の解決挙動を確認・変更する。
- CmocError、CLI parse error、stdout/stderr の error report、call stack 表示、subcommand log の生成条件を確認・変更する。
- cmoc config の既定値や不正値拒否、FileAccessMode、Codex sandbox profile、追加 writable/read path の許可境界を確認・変更する。
- session/apply branch 名からの session id 抽出や state 読み込み、managed worktree の作成・削除防御、`.cmoc` ignore、binary 判定の runtime 回帰を確認する。

## Do not read this when
- 個別サブコマンド固有の業務ロジックや出力仕様だけを調べたい場合。
- oracle file の正本仕様そのものを確認したい場合。
- 単一 helper の内部実装だけを読みたい場合で、runtime 境界全体の外部挙動を確認する必要がない場合。

## hash
- cd044770d2804b9741505b9cfb542ca3b3a8d4472628bd035c73d2233c3b94d0

# `test_cli_init_tui.py`

## Summary
- init と TUI 起動直前の CLI 境界における外部挙動を検証するテスト。cmoc 初期化、.cmoc ignore、既存 staged/unstaged 変更の保護、設定既定値同期、linked worktree での root/worktree 扱い、TUI prompt 保存、parameter 解決、Codex 起動引数の組み立てを同じ利用開始直後の回帰領域として扱う。
- 16,000 文字を超えるが、初期化済み repository/runtime 状態を共有する init/TUI 前処理の凝集した回帰テストとして一箇所に保つ意図を持つ。

## Read this when
- init の外部挙動、生成・更新される設定、.cmoc の ignore 化、初期化コミット、既存の staged/unstaged 変更を壊さない制御を変更または確認する時。
- linked worktree 上での init/TUI 実行時に、root 側と worktree 側の .cmoc、.gitignore、log、schema、config の配置や git 状態を確認する時。
- TUI 起動前の editor 実行、Markdown prompt 解析、parameter 解決、complete prompt 保存、Codex TUI へ渡す AgentCallParameter や extra read path を変更する時。
- subcommand log の command_invoked や step_started など、init/TUI 開始前後の記録形式や保存場所を変更する時。

## Do not read this when
- init や TUI 前処理を経由しない個別サブコマンドの挙動だけを確認する時。
- Codex CLI や editor の実体の品質、LLM 出力内容そのもの、または外部ツール自体の動作を検証したい時。
- 設定値や AgentCallParameter の型定義そのものを確認する時は、実装または定義側を先に読む。
- oracle の正本仕様断片を確認する時は、対応する oracle file を読む。

## hash
- 22f2bb4c955b256be15fa821fc5dc65609144b9431a938ae8b2c69e8e9fca25d

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 呼び出しの実行・TUI 起動まわりを、サブプロセス起動条件、生成 profile、cwd、標準入力、schema 出力、ログ記録、終了時エラーとして検証する realization test。
- agent call 後の file access rule 検査を、oracle・runtime 管理領域・memo・git directory・readonly realization diff・一時 cache・ignore 対象・preexisting diff・recovery retry などの境界で確認する。
- linked worktree や pure oracle read における cwd、writable roots、repo log 読み取り許可、schema state 配置など、実行 root と作業 root がずれるケースの回帰検査を担う。

## Read this when
- Codex CLI/TUI を起動する runtime wrapper の引数、profile 生成、cwd、stdin、output schema、call log の挙動を変更する。
- agent call 後の file access rule 違反検出、違反 recovery、許可される一時生成物や ignored diff の扱いを変更する。
- readonly、repo write、realization write、pure oracle read の各 access mode による sandbox・許可 path・post-call diff 検査の違いを確認する。
- linked worktree 上での Codex 実行、schema state 保存先、repo log の読み取り許可、complete prompt の扱いを変更する。
- Codex CLI の missing binary、nonzero exit、TUI failure reporting などのエラー報告挙動を確認する。

## Do not read this when
- Codex runtime ではなく、通常の CLI command parsing や agent call parameter の型定義だけを確認したい。
- file access rule の正本仕様そのものを調べたい場合は、oracle doc または rule 実装へ直接進む。
- INDEX entry 生成、path model、oracle/realization 分類など、Codex サブプロセス実行と無関係な routing 仕様を調べたい。
- 個別の test support fixture や fake repository 作成 helper の実装詳細だけを確認したい場合は、support 側の対象へ直接進む。

## hash
- e18d7ed81e6294b067ee93134119e3e7da205aa15cf17dface6601a01911e004

# `test_codex_runtime_home.py`

## Summary
- Codex CLI 実行時の Codex home 解決と事前検証を扱う realization test。環境変数未設定時の既定値、相対値の解決基準、プロファイル配置、呼び出しログへの記録、Codex CLI 起動前に失敗すべき認証環境不備を検証する。

## Read this when
- Codex CLI 呼び出しに渡す CODEX_HOME、プロファイル、作業ディレクトリ、呼び出しログの挙動を変更または確認したいとき。
- Codex home が存在しない、ディレクトリではない、認証情報がない場合のエラー文言や失敗タイミングを変更または確認したいとき。
- file access mode によって Codex CLI の実行 cwd が変わるケースで、相対 CODEX_HOME の解決挙動を確認したいとき。

## Do not read this when
- Codex CLI の標準出力イベント処理、capacity wait、一般的な agent call 結果処理だけを確認したいとき。
- Codex home ではなく、repository path、oracle path、run root、work root の一般的なパスモデルを確認したいとき。
- CLI 利用者向けコマンド定義や設定ファイル全体の schema を確認したいとき。

## hash
- b92995fbdd0a93c847ae8a31d4ea6534df7c8b4185810379c129ee1b456241d7

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex exec が quota exceeded で失敗した後の待機、probe、resume または再実行、ログ記録、ファイルアクセス違反回復をまとめて検証する realization test。
- 単一呼び出しと並列呼び出しの両方について、quota retry 状態機械の外部挙動を fake Codex 呼び出し列、call log、subcommand log、CODEX_HOME、cwd から観測する。

## Read this when
- quota exceeded 後に Codex exec が probe を実行し、復旧後に resume token で再開する挙動を確認・変更する時。
- resume token が無い場合の再実行、probe 失敗時の即時失敗、quota poll 上限到達時の扱いを確認する時。
- quota retry 中の call log、subcommand log、prompt/stdout/stderr/output の記録内容や console 表示を変更する時。
- CODEX_HOME が相対パスの場合の cwd、PURE_ORACLE_READ 時の実行位置、ファイルアクセス違反からの回復処理を確認する時。
- 複数の Codex exec が同時に quota 待機した場合に、代表 probe を 1 回だけ実行し、待機中の呼び出しが同じ結果に従う制御を確認する時。

## Do not read this when
- quota retry と関係しない通常成功時の Codex exec 起動引数や出力 JSON 処理だけを確認したい時。
- quota availability probe の prompt を組み立てる仕様そのものを確認したい時。
- CLI サブコマンド全体の構成、設定読み込み、repository fixture の基本動作を調べたい時。
- ログファイルの汎用フォーマットや SubcommandLogger の通常動作だけを確認したい時。

## hash
- ff3997f87bd1f67490dd75b6c23f3bb4e7e6b88a431ae10a3d0a134011fcd49f

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 実行ラッパーの retry 挙動を検証する realization test。Structured Output の schema 不一致・出力欠落・空出力・JSON parse failure、capacity error、file access violation 復旧、stdout JSONL 以外の error marker の扱いを、fake Codex 実行ファイルとログ検査で確認する。
- agent call の出力 JSON、call log、prompt log、stdout log、subcommand log event が retry ごとに期待通り記録されるかを確認する入口になる。

## Read this when
- Codex CLI 呼び出しの retry 条件、retry 回数、成功時 result、失敗時 CmocError の外部挙動を変更または確認したいとき。
- Structured Output の schema validation、出力ファイルの欠落・空・不正 JSON に対する再試行とログ内容を確認したいとき。
- capacity error の検出、sleep を伴う再試行、capacity retry log event の扱いを変更または確認したいとき。
- realization write 実行中に oracle 側へ書き込みが発生した場合の復旧順序や、capacity retry より前に file access violation を処理する挙動を確認したいとき。
- stdout JSONL の structured event ではない stderr や通常 stdout 上の文字列を、capacity/quota retry marker として扱わないことを確認したいとき。

## Do not read this when
- Codex CLI 起動コマンドの組み立て、実際の subprocess 実装、ログファイル生成処理そのものを変更したいだけなら、対応する implementation を直接読む。
- agent call parameter の型、model class、reasoning effort、file access mode の定義を確認したいだけなら、基本型定義側を読む。
- repository fixture、Codex home stub、fake executable 作成 helper の詳細を変更したいだけなら、test support 側を読む。
- INDEX.md 生成規則や oracle/realization の概念定義を確認したいだけなら、この retry テストではなく正本仕様断片を読む。

## hash
- 8313d00d0611f65598134671436e71a2d2672817c7c23087ee8913235ceba802

# `test_indexing_cli.py`

## Summary
- INDEX.md 生成・更新、indexing preflight、indexing subcommand、INDEX.md conflict 解決の外部挙動を検証する回帰テスト群。
- 対象列挙、hash 再利用、Codex 生成、commit 対象、dirty worktree 拒否、linked worktree、空ディレクトリ、並列生成、memo 除外、symlink cycle 回避を routing document 更新ワークフローとしてまとめて扱う。

## Read this when
- indexing CLI が INDEX.md を生成・更新・commit する条件を確認したいとき。
- indexing preflight と通常の indexing subcommand で dirty worktree、linked worktree、repo config、commit 対象の扱いがどう違うかを確認したいとき。
- 既存 INDEX.md entry の hash 再利用、malformed entry の再生成、Structured Output schema 不一致の拒否を変更・検証するとき。
- INDEX.md conflict 解決、空ディレクトリへの INDEX.md 配置、並列生成、root 直下 memo 除外、入れ子 memo 対象化、directory symlink cycle 回避に関わる実装を変更するとき。

## Do not read this when
- INDEX.md entry の自然言語内容そのものを設計・更新したいだけで、CLI 境界や git 状態の回帰確認が不要なとき。
- routing document 生成に関係しない subcommand、設定、agent call、apply join の挙動を調べたいとき。
- 単体 helper の内部実装だけを確認したく、外部 CLI 挙動、commit、worktree、git conflict の観測が不要なとき。

## hash
- ba84ba2a5f8fac06dd16494e65b04728e1b72568d45ca51a5e25aa2604e2bf43

# `test_indexing_preflight.py`

## Summary
- Codex 実行前に INDEX 更新の preflight が走ること、その更新が git commit され作業ツリーを汚さないことを検証する realization test。
- 実行対象 worktree の選択、repository lock 待機、特定 purpose での preflight skip、file access recovery 後の再実行時 preflight までを扱う。

## Read this when
- Codex 呼び出し前の indexing preflight の起動条件、skip 条件、実行順序を変更する。
- root と cwd が別 worktree を指す場合に、どの worktree の INDEX 更新を行うかを確認する。
- indexing lock の待機挙動や、preflight 更新後の git commit・clean status の期待を確認する。
- file access recovery による Codex 再試行時にも indexing preflight が再実行されるかを確認する。

## Do not read this when
- INDEX 生成内容そのもの、エントリー本文の品質、ルーティング文書の記述規則だけを確認したい。
- Codex 実行ラッパーではなく、通常の indexing 更新処理の差分検出や文書生成ロジックを確認したい。
- CLI 引数 parsing や設定読み込みなど、preflight 起動後の Codex 実行順序と関係しない領域を調べたい。

## hash
- a693f2e5f73bf64bdf25ba7f48910e3be0fffbd38f9fafe0a5b3954d37d8fe11

# `test_packaged_import.py`

## Summary
- packaged layout から読み込まれる import 境界を検証する realization test。配布時の package 設定、oracle package の配置、acp builder が oracle 側の正本実装を参照できることを subprocess 上の隔離 PYTHONPATH で確認する。

## Read this when
- packaged layout、pyproject の package-dir/packages 設定、または oracle/src と src 配下 package の import 境界を変更する。
- acp.builder.review.oracle.enumerate_finding または acp.builder.basic の配布環境での import 失敗を調査する。
- oracle.acp_builder.basic の canonical 定義と acp.builder.basic の再 export 関係を検証したい。

## Do not read this when
- 通常の prompt 内容、review oracle standard の本文、または structured output schema の詳細仕様だけを確認したい。
- 開発環境上の直接 import だけを調査しており、packaged layout や隔離 PYTHONPATH での挙動が関係しない。
- packaging ではなく個別 builder の内部ロジックや finding 列挙仕様そのものを変更する。

## hash
- c8a690ba867f441064f70e79f446514d95e4f7f52d690a0fd4d91457ce91970a

# `test_prompt_parts.py`

## Summary
- 標準 prompt parts と complete prompt の組み立て結果を検証する realization test。各 standard builder が期待する見出し・本文断片を返すこと、complete prompt が指定された standard 群・routing rule・file access rule・root placeholder を適切に含めるまたは省くことを確認する。

## Read this when
- prompt parts の出力内容、見出し、含まれるべき語句のテストを確認・変更する。
- complete prompt が routing rule、file access rule、各種 standard、補助 prompt、root placeholder をどう組み込むかの期待挙動を確認・変更する。
- file access mode ごとの prompt 文言や、standard の既定での省略・明示指定時の追加に関するテストを探している。

## Do not read this when
- prompt parts や complete prompt の実装を変更したいだけで、テスト期待値を確認する必要がない場合は、対応する実装側を直接読む。
- StructDoc や markdown rendering の汎用仕様を確認したい場合は、その構造化文書処理の実装やテストを読む。
- oracle file の正本文言そのものを確認したい場合は、対応する oracle 側の文書または生成元を読む。

## hash
- b9fef4ddaeb2f0e1b881f9a3685913297160ea4124bfa48ab10ce916c6c54096

# `test_review_oracle_cli.py`

## Summary
- review oracle コマンドの外部挙動を CLI 経由で検証するテスト。対象 oracle file の列挙、scope 別の評価対象、report の構成と集計、accepted/rejected 所見の出力、エラー時 report、review 用 worktree と join commit、INDEX.md 変更の取り込み、想定外差分の拒否を扱う。
- 所見評価 loop の制御を検証するテスト。enumerate が同一対象の既存所見だけを受け取ること、challenger/advocate/judge/merge の入出力、merge operation の契約違反や target 再利用の拒否を確認する。

## Read this when
- `review oracle` の CLI 挙動、report 出力、scope の意味、review 用 worktree、join commit、INDEX.md 変更の扱いを変更・調査する時。
- oracle review の対象列挙で、tracked ignored file、symlink、binary、`AGENTS.md`、`INDEX.md`、memo 配下との境界を確認したい時。
- review oracle の finding loop、validation、judge、merge operation、accepted/rejected 所見の集計や表示を変更する時。
- review oracle 実行中の失敗時 report、標準出力へのエラー表示、または review が INDEX.md 以外の差分を作った場合の拒否挙動を確認する時。

## Do not read this when
- review oracle 以外の review サブコマンドや一般的な CLI 初期化・session 操作だけを調べる時。
- oracle review の prompt 文面や structured output schema の詳細だけを確認したい時は、対応する実装または schema を直接読む方がよい。
- 単体の path model、設定読み込み、git helper の内部実装だけを変更する時。ただし review oracle の外部挙動に影響する場合は読む。

## hash
- 720fd16a240c7eae5a58619834e3a9cd4d328668ed56875e59ea09fe9ee7f726

# `test_session_cli.py`

## Summary
- session の分岐作成・統合・破棄に関する CLI 外部挙動を、Git branch と session state のライフサイクルとしてまとめて検証する realization test。
- linked worktree 上での branch/state 操作、session-id 衝突、状態ファイル破損、dirty worktree 拒否、cleanup 失敗時の rollback、conflict 解消 agent の権限と差分制限、branch 削除可否、stdout/stderr へのエラー出力先を扱う。
- 同じ session branch/state fixture を共有する回帰観点を一箇所に集約し、分割よりも session CLI の状態遷移を通しで追うことを優先している。

## Read this when
- session の fork・join・abandon の CLI 挙動、出力、終了コード、Git branch 操作、session state 更新を変更または確認するとき。
- session 操作が linked worktree でどの branch を基準に動くか、root worktree への影響を受けるかを確認するとき。
- session state file の生成・破損検出・abandoned/joined/active 遷移・cleanup 失敗時の復旧挙動を確認するとき。
- join 時の merge conflict 解消 agent、oracle conflict write 権限、conflict marker 検出、delete conflict staging、余計な差分の拒否を変更するとき。
- session 完了処理でのエラー報告先、サブコマンドログ付き完了表示、branch 削除失敗時の警告表示を確認するとき。

## Do not read this when
- session 以外の CLI サブコマンド、設定読み込み、agent call の一般処理だけを確認したいとき。
- session の内部 helper 単体の細部だけを調べたい場合で、対象 helper の実装やより小さい単体テストを直接読めるとき。
- oracle file の正本仕様そのものを確認したいとき。この対象は realization test であり、正本仕様ではない。

## hash
- 05c54f4da38117724999b77fb2ed1e5490a1f0f1bac67603844556163a9c18f8

# `test_struct_doc_rendering.py`

## Summary
- StructDoc の Markdown renderer が本文中の連続空行を正規化する挙動を検証する単体テスト。通常テキストとコードブロックを対象に、過剰な空行が折りたたまれ、期待される Markdown 文字列になることを確認する。

## Read this when
- StructDoc の Markdown 出力で空行の扱いを変更・確認したいとき。
- 通常テキストまたはコードブロック内の連続空行がどのように描画されるべきかをテストから確認したいとき。
- render_as_markdown の整形挙動に関するテストを追加・修正したいとき。

## Do not read this when
- StructDoc のデータ構造そのものや renderer 全体の実装を確認したいときは、実装側を読む。
- Markdown renderer 以外の prompt builder 分割根拠や正本仕様を確認したいときは、対応する oracle 側の文書を読む。
- CLI 挙動、ファイル操作、永続状態など StructDoc の Markdown 整形と無関係な挙動を調べたいとき。

## hash
- 51580019f3a5f35c894b459980668eec4b098eecee22f1645f571c7c2084f811
