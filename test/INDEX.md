# `_support.py`

## Summary
- CLI 制御系の realization test で使う共通テスト補助を集めたファイル。最小 Git リポジトリの作成、git 状態確認、Codex home の準備、Codex profile 生成のスタブ化、外部コマンド用 Python 実行ファイルの生成、session state から apply worktree path を解決する helper を提供する。

## Read this when
- cmoc CLI のテストで、一時 Git リポジトリや初期 commit 済み fixture を作る必要があるとき。
- テスト中に現在 branch、tracked だが ignore される oracle file、Codex home、Codex profile stub、fake external command を準備する helper を探すとき。
- runtime apply の state から apply worktree path を確認するテスト補助が必要なとき。

## Do not read this when
- 個別の CLI コマンド挙動そのものを検証するテストケースを探しているとき。
- 本番実装側の git 操作、Codex 実行、apply worktree 管理の処理を変更したいとき。
- oracle file の仕様やテスト方針の正本記述を確認したいとき。

## hash
- 0cca941e1150a51ddaccd880353c25aaaa2b13e64623de563fee334ecbd61346

# `test_acp_builder_parameters.py`

## Summary
- ACP builder が生成する AgentCallParameter のモデル種別、推論量、ファイルアクセスモード、prompt 内容、structured output schema 参照を検証する realization test。
- apply fork、TUI parameter 解決、INDEX エントリー生成、oracle review、session join conflict resolution など複数 builder の公開挙動と互換 module の export 境界をまとめて確認する。

## Read this when
- ACP builder の parameter 生成結果や prompt 断片、schema path、schema 内容の期待値を変更する。
- apply fork、TUI resolve parameter、indexing index entry、review oracle、session join conflict resolution の builder 実装を変更した後、既存の外部挙動テストを確認する。
- builder module の `__all__` や不要な内部名の公開有無に関する互換性テストを確認する。
- oracle src 側の ACP builder schema と realization 側 builder が参照する schema の一致を検証するテストを探している。

## Do not read this when
- 個別 builder の実装詳細を変更したいだけで、まず実装側の責務や prompt 構築ロジックを確認する必要がある場合。
- ACP builder 以外の CLI 挙動、永続状態、path model、Git 操作のテストを探している場合。
- INDEX.md エントリー生成の仕様そのものを確認したい場合は、oracle または builder 実装の該当箇所を直接読む。

## hash
- 0ba7fd0ee9d440a619c73605256ee5364379f781d3de108a8c0cde1d5b750dd9

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
- apply fork の CLI 経由の統合的な挙動を検証するテスト。所見列挙、適用、commit、変更要約、report 生成、session state 更新までの制御を一つの文脈として扱う。
- apply fork 用 ACP builder の import 可能性、prompt/schema 参照、変更ファイル再検査、未収束・収束・error report、禁止領域変更からの recovery、rolling apply fork の対象選定を検証する。

## Read this when
- apply fork の report 内容、終了コード、収束判定、未収束判定、error 時の変更要約を確認・変更したいとき。
- apply fork が所見適用後に変更ファイルや新規ディレクトリ配下を再検査する制御を確認・変更したいとき。
- apply fork の commit message、apply branch、session state 更新、rolling apply fork の基準 commit を確認・変更したいとき。
- apply fork 用の change summary、file finding enumeration、finding application の ACP builder、prompt、schema path、packaged layout import を確認・変更したいとき。
- apply fork 中に oracle など禁止領域が変更された場合の recovery と、許可差分だけを commit する挙動を確認・変更したいとき。

## Do not read this when
- apply fork 以外のサブコマンド、または CLI を介さない低レベル helper 単体の挙動だけを確認したいとき。
- report schema や prompt builder の正本仕様そのものを確認したいときは、対応する oracle file を読む。
- session fork や apply join の基本動作だけを確認したいときは、それぞれの専用テストを読む。
- 変更要約 helper の内部実装だけを変更したいときは、まず実装側の該当モジュールを読む。

## hash
- dd0c7c5f5b265d7071b5a91321c9ca416fc6ac144a256bc1c1e29f49d1b2abbd

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
- cmoc の共通 runtime 契約を横断して固定する基本回帰テスト。root placeholder 解決、linked worktree と work root 判定、設定 dict 検証、CmocError の Markdown 表示、CLI parse/preflight error の stdout report、subcommand log、状態 branch 名、`.cmoc` ignore、FileAccessMode から Codex sandbox/profile への変換、binary 判定など、個別サブコマンドより下位の実行前提を扱う。
- 複数領域にまたがるが、共通 fixture と root 状態を共有して一緒に崩れやすい runtime 境界のテストを集約する入口として位置づける。

## Read this when
- runtime の root 解決、worktree 作成・削除、安全な対象 path 判定、または `<run-root>` / `<work-root>` / `<cmoc-root>` の挙動を変更する。
- 設定読み込み、既定値、型検証、CmocError、CLI error report、Click parse error の表示形式や出力先を変更する。
- subcommand log の生成条件、timestamp 衝突時の扱い、preflight 失敗時の副作用、shell completion probe の副作用抑制を確認する。
- FileAccessMode、Codex profile、sandbox writable roots、extra writable/read path、oracle conflict write、repo log read 許可、binary 判定の runtime 契約を変更または検証する。
- cmoc の基礎 runtime 変更後に、個別サブコマンドのテストより先に共通前提の回帰範囲を把握したい。

## Do not read this when
- 特定サブコマンド固有の正常系・業務ロジックだけを確認したい場合は、そのサブコマンドのテストへ進む。
- oracle 文書や prompt builder の正本仕様そのものを確認したい場合は、oracle 側の該当本文を読む。
- UI 文言や個別出力内容のうち、runtime error/report/profile と関係しない仕様を調べるだけなら対象外。
- INDEX.md ルーティングの生成・検証だけが目的で、runtime の外部挙動を読む必要がない場合は本文まで読まなくてよい。

## hash
- 532736633e7ef52228a71848d2b565f26d7271bd7602281592bc1e160eeedfe3

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
- Codex CLI 実行/TUI 起動のランタイム挙動を検証する realization test。Codex subprocess の起動引数、profile 生成、cwd、schema 出力先、apply process tracking、ログ、missing CLI/nonzero exit のエラー報告を扱う。
- agent call 後のファイルアクセス規則チェックと復旧処理を、oracle・.git・.agents・.codex・memo・cmoc log・一時キャッシュ・ignored file・linked worktree などの差分ケースで検証する。

## Read this when
- Codex CLI を起動する実装、profile 生成、sandbox/writable_roots、run_codex_exec、run_codex_tui、run_codex_subprocess、run_tracked_codex_subprocess の挙動を変更する時。
- agent call 後の禁止領域差分検出、既存の禁止差分の扱い、復旧プロンプト生成、schema retry/nonzero error 前後の復旧順序を確認・変更する時。
- PURE_ORACLE_READ、READONLY、REALIZATION_WRITE、REPO_WRITE の各 file access mode が Codex 実行時の cwd・許可領域・差分許容に与える影響を確認する時。
- linked worktree での Codex 実行、schema state の配置、repo log read、TUI complete prompt の許可範囲を確認する時。

## Do not read this when
- Codex ランタイム以外の CLI サブコマンド、設定読み込み、path model、oracle 文書生成などを調べる時。
- Codex subprocess を実際に起動する実装本文だけを読みたい時は、先に対応する runtime 実装や profile 実装を読む方が直接的。
- 一般的な Git helper、テスト用 repo 作成 helper、stub executable helper の詳細だけを調べる時は、support 側のテスト補助コードを読む方が直接的。

## hash
- f701b7ba39e41089c935c1c08113a7f6878c6bfcf922d556f91737314d39cb05

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
- Codex exec が quota exceeded になった後の待機・probe・resume・再実行の外部挙動を検証する realization test。
- quota retry 状態機械の観測点として、probe 共有、resume token、call log、subcommand log、CODEX_HOME と cwd の扱い、file access violation 回復をまとめて扱う。

## Read this when
- quota exceeded 後に Codex exec が probe を実行し、復帰後に resume または再実行する挙動を変更・確認する場合。
- quota availability probe の入力、実行 profile、ログ記録、失敗時の扱い、並列呼び出しでの probe 共有を確認する場合。
- quota retry 中の CODEX_HOME、cwd、file access violation 回復、call log や subcommand log の観測結果を確認する場合。

## Do not read this when
- 通常の Codex exec 成功時だけの引数組み立てや出力 JSON 読み取りを確認したい場合。
- quota availability probe の prompt 生成そのものだけを確認したい場合。
- realization standard やファイル分割方針の正本仕様を確認したい場合。

## hash
- 75fe18b650824444abf3ba72899f3964f455528e0e8a4a65742c8486ea2b7c6d

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
- review oracle コマンドの CLI 経由の外部挙動と、所見の列挙・検証・judge・merge を含む評価 loop の制御を検証するテスト群。
- report 生成時の章構成、件数、accepted/rejected 所見の表示、エラー report、対象 oracle file の列挙条件、session/full scope、linked worktree、review 中に生成された INDEX 変更の merge、非 INDEX 差分の拒否を扱う。
- oracle review の fake Codex 応答と report 文脈を共有する統合的なテストとしてまとまっており、review run 全体の状態遷移と出力確認の入口になる。

## Read this when
- review oracle コマンドの report 出力、終了コード、表示されるメタ情報、章順、所見件数、エラー時 report の挙動を確認または変更したいとき。
- oracle review の対象ファイル選択、full scope と session scope、git ignored だが追跡済みの oracle file、AGENTS.md や INDEX.md の除外条件を確認したいとき。
- review oracle の所見 loop で、列挙結果の再投入範囲、challenger/advocate/judge/merge の呼び出し順や入力、merge operation の検証規則を変更するとき。
- linked worktree 上の session branch、review 用 worktree、review_join_commit、review 中に生じた INDEX.md 変更の取り込み、INDEX conflict 解決を扱うとき。
- review oracle 実行中に INDEX.md 以外の差分が発生した場合の拒否と、元 worktree を汚さない制御を確認したいとき。

## Do not read this when
- review oracle 以外の review コマンドや通常の session/init CLI の挙動だけを確認したいとき。
- oracle file の正本仕様本文や prompt 文面そのものを確認したいとき。
- INDEX.md 生成一般、runtime Codex preflight 一般、git worktree 操作一般の実装詳細を単体で確認したいとき。
- report rendering や merge operation helper の局所的な実装だけを先に読みたい場合で、対応する実装ファイルを直接読む方が目的に近いとき。

## hash
- decd06f7ed777ec7afb7f4be6549973f71431105626811ce534533a617c2784e

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
