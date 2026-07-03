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
- ACP builder が生成する AgentCallParameter のモデル種別、reasoning effort、ファイルアクセスモード、prompt 内容、structured output schema 参照を検証するテスト群。
- apply fork、TUI resolve、index entry、review oracle、session join conflict resolution など複数 builder の外部契約と、oracle source の schema との一致を確認する。
- 互換 module の公開名が必要な builder のみに絞られていることも検証し、ACP builder 周辺の公開面整理を確認する入口になる。

## Read this when
- ACP builder の parameter 生成結果、prompt に埋め込まれる path・標準文書断片・動的文字列、または structured output schema path の挙動を変更する。
- apply fork、TUI resolve、indexing index entry、review oracle、session join conflict resolution の builder 実装や互換 module の `__all__` を変更する。
- oracle source の JSON schema を realization 側 builder が正しく参照しているか、または schema validation 用の代表入力を確認したい。
- ファイルアクセス規則違反リカバリー担当や review oracle validate/merge/enumerate の prompt 中の `<oracle-root>` 表記、既知所見文字列の保持、公開名制限を調べる。

## Do not read this when
- ACP builder 以外の CLI コマンド、永続状態、git 操作、path model の実装挙動を調べたいだけで、このテストが扱う parameter 生成契約に触れない。
- 個別 schema の正本内容そのものを確認したい場合は、対応する oracle source の JSON schema を直接読む。
- INDEX.md エントリー生成規則や routing 文書の仕様を確認したい場合は、仕様文書側を読む。

## hash
- 922b293ac9298ad5387e636da3dc70107b818510fcb2ec89d2c8b25034582973

# `test_apply_abandon_cli.py`

## Summary
- active apply run を abandon する CLI 外部挙動を検証するテスト。apply worktree と branch の cleanup、state の ready への復帰、cleanup 対象欠落時の warning、running process と記録済み child process の停止、PID 再利用・終了競合・lock 待機の扱いを同じ abandon 境界として確認する。
- 通常 worktree、linked session worktree、apply worktree 内からの実行位置差を含め、abandon が repo 側 state を正として処理することや、dirty な linked session、破損 state、stale apply branch を拒否することを検証する。

## Read this when
- apply abandon の成功時 cleanup、warning 出力、state 更新、worktree/branch 削除の期待挙動を確認または変更するとき。
- running apply を abandon する際の process identity 読み取り、child process group 停止、PID 再利用防止、pidfd signal、終了済み process の扱いを確認または変更するとき。
- apply abandon をどの worktree から実行できるか、linked session や stale apply branch の拒否条件を確認または変更するとき。
- apply fork が作る active apply run の state 形状が abandon のテスト fixture に影響する変更を行うとき。

## Do not read this when
- apply abandon 以外の apply サブコマンドの通常フローだけを確認したいとき。
- Codex 実行結果の品質や findings 内容そのものを検証したいとき。
- session fork、init、git helper の一般仕様を確認したいだけで、active apply run の破棄挙動に触れないとき。

## hash
- 3dbe52f9e2bd55b89592854c3796a71cd636b99783fe8d8098a8d70e1e3aff3d

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
- apply run を session へ join する CLI 外部挙動を検証する realization test。成功時の worktree/branch cleanup、state 更新、report 生成と、dirty worktree、stale apply branch、想定外差分、merge conflict、force resolve の拒否・復旧条件を扱う。
- apply join の可否判断に関わる git 状態、session/apply worktree、管理対象 path 分類の境界条件を一箇所で確認するための入口。

## Read this when
- apply join の CLI 挙動、終了コード、標準出力、report、state 更新、worktree/branch 後片付けを変更または確認したいとき。
- apply join が apply worktree 内・session worktree 内・linked session worktree 内から実行された場合の挙動を確認したいとき。
- apply join の dirty worktree、stale apply branch、想定外差分、merge conflict、force resolve の扱いを変更または調査したいとき。
- apply join で realization file、oracle、AGENTS、INDEX、memo、tracked ignored file などの path 分類が join 可否にどう影響するかを確認したいとき。

## Do not read this when
- apply fork の Codex 実行、prompt 構築、apply worktree 作成だけを確認したいとき。
- session fork や init の基本挙動だけを確認したいとき。
- apply join の内部 helper 実装を直接変更したいだけで、CLI 経由の外部挙動テストを先に読む必要がないとき。

## hash
- f9a4d466f8c0587c817e3794b259953e6897ec1a8567ce6750298cd7400128a4

# `test_basic_runtime.py`

## Summary
- cmoc の基礎 runtime 契約を横断的に検証する realization test。root placeholder と worktree root 解決、config validation、CmocError の Markdown 表示、CLI error の stdout 変換、subcommand log、FileAccessMode ごとの Codex sandbox profile、binary 判定、session/apply branch state 解析を一つの回帰テスト群として扱う。
- 個別サブコマンドの機能仕様ではなく、複数の実行経路の前提になる runtime 境界をまとめて固定する入口。共通 fixture と root 状態を共有するため、runtime の基礎契約を変更する際に関連する挙動を同時に確認できる。

## Read this when
- root placeholder、repo root、run root、work root、linked worktree、main worktree の解決規則を変更または調査する。
- CmocError、CLI 引数解析 error、stdout/stderr の error report、Call stack 表示、duration 表示など、利用者向け error/rendering 契約を変更または調査する。
- cmoc config の既定値、型 validation、論理 model class、reasoning effort の扱いを変更または調査する。
- subcommand log の生成タイミング、timestamp 衝突時の log file 扱い、preflight 失敗時の副作用抑制を変更または調査する。
- FileAccessMode、Codex sandbox profile、追加 writable/read path、oracle・memo・runtime 管理領域のアクセス制限を変更または調査する。
- session branch や apply branch から session id/state を読む制御、壊れた branch 名の拒否を変更または調査する。
- `.cmoc` ignore pattern、起動 wrapper の missing venv report、binary 判定の読み取り範囲など、runtime の基礎的な補助挙動を変更または調査する。

## Do not read this when
- 個別サブコマンド固有の業務ロジック、入出力 schema、差分生成、review/apply の詳細挙動だけを確認したい場合は、そのサブコマンドや機能に対応するテストへ直接進む。
- oracle doc や oracle src の正本仕様そのものを確認したい場合は、realization test ではなく oracle 側の対象本文を読む。
- テスト共通 fixture、runner、git helper の実装だけを変更したい場合は、support 用のテスト補助コードを読む。
- runtime の外部挙動ではなく、内部 helper の局所的な実装整理だけが目的で、ここに固定された契約へ影響しない場合は、対象 implementation とより小さい単位のテストを優先する。

## hash
- f63b5c14aaf2a8933343ac939915bd3de09c8e53d267fa2ac6fb39f5e58013f1

# `test_cli_init_tui.py`

## Summary
- init と TUI 起動直前の CLI 境界における外部挙動を検証するテスト群。cmoc 初期化、.cmoc ignore、既存 git 差分の保護、設定既定値の同期、linked worktree での状態配置、Markdown prompt 整形、Codex TUI 起動 parameter 構築を同じ利用開始フローとして扱う。

## Read this when
- init 実行時の gitignore 更新、.cmoc 追跡解除、.agents/.gitkeep commit、既存 staged/unstaged 変更の保護に関する回帰を確認・変更するとき。
- linked worktree 上での init/TUI 実行時に、repository root と worktree 側の .cmoc、log、config、schema、gitignore がどこに作られるかを確認するとき。
- TUI 起動前の editor 実行、Markdown comment 除去、完成 prompt 保存、resolve_parameter の解釈、AgentCallParameter への file access mode・model・reasoning effort・schema・extra_read_paths 反映を変更するとき。
- init が既存 config の人間設定を保持しつつ不足した既定値を補完する挙動を確認するとき。

## Do not read this when
- init や TUI 前処理ではなく、個別 subcommand の業務ロジックや Codex 実行結果そのものを確認したいとき。
- CLI 境界の外部挙動ではなく、低レベル helper の内部実装だけを変更するとき。ただしその helper が init/TUI の observable な状態配置や parameter に影響する場合は読む。
- oracle 文書や routing entry の内容を確認したいとき。
- テスト支援関数、repo fixture、fake executable 作成処理そのものを変更したいときは、支援コード側を直接読む。

## hash
- 0176c3bc7925652d3299ab136525799032a454b93a9cb2841d06780bed1ee5a8

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
- Codex exec が quota exceeded になった後の待機、probe、resume token 利用、resume 不能時の再実行、ログ記録、ファイルアクセス違反回復、並行呼び出し時の代表 probe 共有を検証する realization test。
- quota 待機から復帰する retry 状態機械の外部挙動を、fake Codex 呼び出し列、call log、subcommand log、CODEX_HOME/cwd の観測を通じてまとめて確認する。

## Read this when
- Codex exec の quota exceeded 検出後の retry、probe、resume、再実行に関する挙動を変更または調査するとき。
- quota availability probe の生成、実行、失敗時処理、ログ出力、subcommand event の status/purpose/returncode を確認するとき。
- CODEX_HOME が相対パスの場合の cwd、PURE_ORACLE_READ 時の --cd、quota 待機中のファイルアクセス違反回復を検証するとき。
- 複数の run_codex_exec が同時に quota exceeded になった場合に、probe が代表 1 回だけ実行され、待機側が成功または失敗を共有する制御を確認するとき。

## Do not read this when
- 通常の Codex exec 成功経路、引数構築、出力 JSON 読み取りだけを確認したいときは、より直接その挙動を扱う runtime Codex exec の実装または別テストを読む。
- quota availability probe の prompt 内容そのものや AgentCallParameter の構築仕様だけを確認したいときは、probe builder 側を読む。
- INDEX.md 生成、oracle/realization の分類、ファイルアクセス規則そのものの仕様を確認したいときは、対応する oracle 文書を読む。

## hash
- 57767c7bb7841e9f8290194c77b6113b29e7fbe433c7f0dcd9ecdea8d13ff7d0

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
- packaged layout でコピーした最小の site 環境から、主要な realization module が oracle package を正しく import・再 export できることを検証するテスト。
- pyproject の oracle package 設定、review oracle enumerate finding builder、acp.builder.basic、config.cmoc_config の import 境界と公開名を確認する。

## Read this when
- packaging 設定、PYTHONPATH 上の配置、または oracle/src/oracle を package として扱う import 経路を変更する。
- acp.builder.review.oracle.enumerate_finding、acp.builder.basic、config.cmoc_config の import 元や re-export の境界を変更する。
- oracle src の定義を realization 側へコピーせず参照する方針が、インストール相当のレイアウトで壊れていないか確認したい。

## Do not read this when
- 通常の CLI 実行フロー、コマンド引数、永続状態、ログ出力の挙動を調べたい。
- prompt の本文内容や schema の詳細仕様そのものを確認したい場合は、対応する oracle file や builder 実装を直接読む方がよい。
- 単体関数の内部ロジックや helper 分割を調べたいだけで、packaged layout 上の import 境界に関係しない。

## hash
- 484451aa5216148342d78d9c4c971994fc8e33e9de194a997d6b2fc605432142

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
- review oracle の CLI 実行を、report 生成、対象 oracle file の選択、所見列挙から検証・judge・merge までの loop、review 用 worktree で発生した INDEX.md 差分の join、失敗時 report まで含めて検証する realization test。
- 16,000 文字を超えるが、同じ review run の fake Codex 応答、report 文脈、対象選択、所見評価 loop の状態を共有する外部挙動テストとして凝集している。

## Read this when
- review oracle コマンドの外部挙動、出力 report の構成・集計・所見表示を変更または確認する。
- review oracle の対象 oracle file 列挙、full/session scope、tracked ignored file、AGENTS.md・INDEX.md 除外、symlink や memo 配下の扱いを確認する。
- review oracle の所見列挙 loop、対象ごとの既存所見 prompt、challenger/advocate/judge、merge operation の契約や invalid operation の扱いを変更する。
- review oracle が linked worktree や review worktree をどう使い、生成・preflight された INDEX.md 差分をどう join するかを確認する。
- review oracle の処理失敗時 report、非 INDEX.md 差分の拒否、index conflict 解決など、review 実行中の失敗・差分管理を変更する。

## Do not read this when
- oracle review 以外の review サブコマンドや、一般的な CLI 起動処理だけを確認したい。
- report rendering や所見 loop の実装だけを局所的に読みたい場合で、まず対応する実装 module を読む方が直接的である。
- INDEX.md エントリー生成、path model、session fork などの個別仕様・実装を確認したいだけで、review oracle CLI の統合挙動に関心がない。

## hash
- 5bd15606b49b7cbdc4c905c452efe8489f1da98c2d70676e062cd086187b5470

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
