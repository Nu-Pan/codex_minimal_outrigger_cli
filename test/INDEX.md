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
- ACP builder が生成する AgentCallParameter の model/reasoning/file access 設定、prompt に埋め込む標準文書・root 表記、structured output schema 参照、および互換 module の公開名を検証する realization test。apply fork、TUI parameter 解決、index entry、review oracle、session join conflict resolution の builder 群を横断して扱う。

## Read this when
- ACP builder の parameter 生成結果、prompt 内容、structured output schema path、または schema 内容の期待値を変更する。
- apply fork、TUI resolve parameter、indexing index entry、review oracle finding、session join conflict resolution の builder 実装や互換 module の export を変更する。
- oracle 側の ACP builder schema と realization 側 builder が同じ schema を参照しているかを確認したい。

## Do not read this when
- 個別 builder の実装詳細だけを調べたい場合は、対応する実装 module を直接読む。
- ACP builder 以外の CLI 挙動、path model、永続状態、または一般的なテスト基盤を調べたいだけである。
- oracle file の正本仕様そのものを確認したい場合は、対応する oracle doc または oracle src を読む。

## hash
- cf91f4a5e1b2deb5113e2f191407d273f16c7acb9c633c5305dac69b150efa93

# `test_apply_abandon_cli.py`

## Summary
- apply abandon が active apply run を破棄する外部挙動を CLI 経由で検証するテスト。apply worktree・apply branch・session state の cleanup、実行場所が通常 session / apply worktree / linked worktree の場合の戻り先、running apply process と Codex child process の停止順序、PID reuse や終了競合時の扱いを扱う。
- apply process id file の読み取り、advisory lock による中間状態回避、child process group 停止、欠損・破損 state・stale apply branch・dirty linked session worktree の拒否条件をまとめて確認する。

## Read this when
- apply abandon の成功時出力、cleanup 対象、state 遷移、warning 表示を変更する。
- running apply を abandon する際の process identity 読み取り、親 process と Codex child process の停止、pidfd・process group・PID reuse 対策を変更する。
- apply abandon をどの worktree から実行できるか、cleanup 後にどの作業ディレクトリへ戻すか、linked session worktree の dirty 判定を変更する。
- apply state の apply_branch から apply worktree を導く処理、破損 state や stale apply branch のエラー条件を変更する。

## Do not read this when
- apply fork の Codex 実行内容や findings 判定だけを確認したい場合。
- session fork、init、git worktree 作成の基本挙動だけを確認したい場合。
- apply abandon 以外のサブコマンドの CLI 表示や state 遷移を確認したい場合。
- INDEX.md 生成規則や oracle / realization の一般標準だけを確認したい場合。

## hash
- df6c8e10c380255816e9a8fd5148399301db97c3cc6bd3d2f929b73f66cfeef7

# `test_apply_fork_cli.py`

## Summary
- apply fork の CLI 挙動と対象正規化を検証する realization test。Codex loop 実行後の session/apply state 更新、apply worktree 配置、linked worktree 起点、.gitignore の扱い、設定読み込み失敗時の中断、所見対象編集、realization/oracle/memo/管理 path の対象選別を扱う。

## Read this when
- apply fork コマンドの状態遷移、branch/worktree 作成、apply run 完了処理を変更・調査するとき。
- apply fork が linked worktree 上の session branch と HEAD をどう扱うべきか確認するとき。
- .cmoc/local/ ignore の保証、session 側 .gitignore の非破壊性、apply branch 側での .gitignore 編集可否を確認するとき。
- apply fork の設定読み込みエラー時に、apply branch/state/pid を開始しない挙動を確認するとき。
- apply fork の対象 path 正規化で、root 直下 memo、oracle、管理ディレクトリ、INDEX.md、AGENTS.md、binary file、tracked ignored file の扱いを確認するとき。

## Do not read this when
- apply fork 以外の apply サブコマンドや session fork 自体の仕様を調べたいだけのとき。
- Codex 実行結果の品質や LLM 出力内容そのものを検証したいとき。
- 実装側の helper 分割や内部アルゴリズムだけを確認したい場合で、外部挙動テストの期待値が不要なとき。

## hash
- 81f7135aede24894b922ed9b0c5a23468e290084fbcb1126d1f9572a065ed9e9

# `test_apply_fork_report_cli.py`

## Summary
- apply fork の CLI 経由の統合的な挙動を検証するテスト。所見列挙、適用、commit、変更要約、report 生成、session state 更新までの制御を一つの文脈として扱う。
- apply fork 用 ACP builder の import 可能性、prompt/schema 参照、変更ファイル再検査、未収束・収束・error report、禁止領域変更時の停止、rolling apply fork の対象選定を検証する。

## Read this when
- apply fork の report 内容、終了コード、収束判定、未収束判定、error 時の変更要約を確認・変更したいとき。
- apply fork が所見適用後に変更ファイルや新規ディレクトリ配下を再検査する制御を確認・変更したいとき。
- apply fork の commit message、apply branch、session state 更新、rolling apply fork の基準 commit を確認・変更したいとき。
- apply fork 用の change summary、file finding enumeration、finding application の ACP builder、prompt、schema path、packaged layout import を確認・変更したいとき。
- apply fork 中に oracle など禁止領域が変更された場合に、許可差分だけを commit せず未収束として止める挙動を確認・変更したいとき。

## Do not read this when
- apply fork 以外のサブコマンド、または CLI を介さない低レベル helper 単体の挙動だけを確認したいとき。
- report schema や prompt builder の正本仕様そのものを確認したいときは、対応する oracle file を読む。
- session fork や apply join の基本動作だけを確認したいときは、それぞれの専用テストを読む。
- 変更要約 helper の内部実装だけを変更したいときは、まず実装側の該当モジュールを読む。

## hash
- 12b684155421257f7f555b6a66ecf09bb64b89e8d65defb0ae5a4b000cf08eec

# `test_apply_join_cli.py`

## Summary
- apply run を session に join する CLI 外部挙動を検証するテスト群。apply worktree/branch の cleanup、session state 更新、join report 生成、linked session worktree への merge、dirty worktree 拒否、想定外差分検出、force resolve、merge conflict 処理を扱う。
- apply join の対象 path 判定 helper について、削除 path の除外、rename target の採用、memo を session change として扱う境界、AGENTS.md や .codex 配下の apply change 拒否、tracked ignored path の許可も確認する。

## Read this when
- apply join CLI の成功時 cleanup、state 更新、report 出力、apply worktree からの実行時挙動を変更・確認したいとき。
- apply join が dirty apply worktree、stale apply branch、想定外差分、未解決 merge conflict をどう拒否するかを確認したいとき。
- apply join の --force-resolve が oracle、AGENTS.md、.codex などの非 realization 差分を戻す挙動を変更・確認したいとき。
- apply join の path 分類、managed branch の変更 path 抽出、tracked ignored file や削除・rename の扱いを確認したいとき。
- linked session worktree 上の apply join が root ではなく現在の session worktree に merge されることを検証したいとき。

## Do not read this when
- apply fork の Codex 実行 parameter や apply worktree 作成処理そのものを確認したいだけのとき。
- session fork、init、汎用 state schema、git helper の単体挙動を確認したいとき。
- apply join 以外の subcommand の CLI 出力や cleanup を調べたいとき。
- oracle file や realization file の定義・標準そのものを確認したいとき。

## hash
- 7cbaeedea59561fb18367273fcec911629a9ee0a6f4aaaa08ee23087bc8228b3

# `test_basic_runtime.py`

## Summary
- cmoc の基礎 runtime 契約を横断的に固定する realization test。root placeholder 解決、run/work/repo root の扱い、config 検証、CmocError 表示、CLI error の stdout report 化、subcommand log、worktree 安全性、FileAccessMode と Codex sandbox/profile 生成、binary 判定、session state branch 解析など、個別サブコマンドより下位の共通実行前提をまとめて検証する。
- 共通 fixture と root 状態を同時に使う回帰テスト群であり、runtime 境界の変更が複数機能へ波及しないかを確認する入口になる。

## Read this when
- root placeholder、repo root、run root、work root、linked worktree の解決規則を変更または調査するとき。
- CmocError、render_error、CLI 引数解析 error、stdout/stderr の error report 表示を変更または調査するとき。
- cmoc config の既定値、型検証、codex model/reasoning effort map の扱いを変更または調査するとき。
- subcommand log の生成条件、timestamp 衝突時の log file 分離、preflight 失敗時の log 抑制を変更または調査するとき。
- create/remove run worktree の管理領域判定や、branch 名から session id を読む制御を変更または調査するとき。
- FileAccessMode、Codex sandbox mode、Codex profile の writable/readable root、extra writable path、local SLM provider 設定を変更または調査するとき。
- `.cmoc/local` の ignore 追加、binary 判定、起動 wrapper の missing venv error 表示など、基礎 runtime の外部挙動を変更または調査するとき。

## Do not read this when
- 個別サブコマンド固有の業務ロジック、prompt 内容、review/apply/session の詳細挙動だけを確認したいとき。
- oracle file の正本仕様本文、path placeholder の概念説明、realization standard の記述そのものを確認したいとき。
- runtime の公開挙動ではなく、単一 helper の内部実装だけを局所的に変更し、その外部契約に影響しないと分かっているとき。

## hash
- c8ee866cc50c3db1d6a72cf2acd69004da196d5a1f54be80b1634ca4b5de978b

# `test_cli_init_tui.py`

## Summary
- init と TUI 起動直前の CLI 前処理について、利用開始直後の外部挙動をまとめて検証するテストファイル。cmoc 初期化、.cmoc local ignore、既存 staged/unstaged 差分の保護、.agents/.gitignore/config の同期、linked worktree 上での初期化と TUI ログ保存、Markdown prompt 解析、Codex TUI 起動 parameter 構築を扱う。

## Read this when
- init サブコマンドの git 操作、.cmoc/.agents/.gitignore/config.json 生成・同期・commit 対象を変更する時。
- 既存の staged/unstaged 変更を init が壊さないこと、または .cmoc 配下の追跡解除・ignore 設定の挙動を確認する時。
- linked worktree 上で init または tui を実行した時の repository root、worktree cwd、ログ・schema・config の配置を変更する時。
- tui サブコマンドの editor 起動後 prompt 整形、HTML comment 除去、resolve_parameter の結果解釈、AgentCallParameter 構築、Codex TUI 起動引数を変更する時。
- CLI サブコマンド実行ログの event、command、argv、step 名、保存先を変更する時。

## Do not read this when
- init や TUI 起動前処理に関係しないサブコマンドの挙動だけを調べる時。
- oracle file の正本仕様そのものを確認したい時。対応する oracle doc または oracle src を直接読む方が適切。
- 内部 helper の単体実装だけを確認したい時。ただしその変更が init/TUI の外部挙動に影響する場合は読む。
- Codex CLI や editor 実体の品質・出力内容を検証したい時。このテストは外部ツールを stub して cmoc 側の制御を検証する。

## hash
- 5b2acb50537e4152e2115ab963a7bb04e98591a7755919bc9b7e2f7950d3e5e1

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 実行・TUI 起動のランタイム挙動を、スタブ化した codex 実行ファイルと一時 Git リポジトリで検証するテスト群。
- プロファイル生成、作業ディレクトリ、sandbox writable_roots、schema 出力先、ローカル SLM 用 provider 設定、apply process tracking、呼び出しログ、Codex CLI 不在・非ゼロ終了時のエラー報告を扱う。
- 呼び出し後のファイル差分について、oracle、memo、.git、.agents、.codex、ignored/cache、README、linked worktree などを post validate しない／許容する現在挙動の境界を確認する。

## Read this when
- run_codex_exec または run_codex_tui の引数組み立て、profile TOML、CODEX_HOME、--cd、--output-last-message、--output-schema の挙動を変更・確認するとき。
- FileAccessMode ごとの Codex 呼び出し時 sandbox 設定、extra_read_paths、extra_writable_paths、linked worktree の cwd/root の扱いを変更・確認するとき。
- Codex 呼び出し後の forbidden diff、ignored artifact、cache、.cmoc log、blocked runtime directory への変更を検査するかどうかの挙動を変更・確認するとき。
- run_codex_subprocess や run_tracked_codex_subprocess の process group、APPLY_PROCESS_TRACKING_ENV、subprocess 起動環境の扱いを変更・確認するとき。
- Codex CLI が見つからない場合、TUI が非ゼロ終了した場合、exec が schema retry や非ゼロ終了を扱う場合のエラー挙動を変更・確認するとき。

## Do not read this when
- Codex runtime ではなく、agent call parameter の型定義や enum 自体の仕様だけを確認したいとき。
- Git リポジトリ作成、stub codex、pytest fixture などテスト支援関数の実装詳細を確認したいとき。
- Codex 以外の外部コマンド実行、通常の CLI サブコマンド、または oracle/realization 文書生成の挙動を調べたいとき。
- INDEX.md エントリー生成やルーティング文書の規則そのものを確認したいとき。

## hash
- e43360607d9c6d637d97ab082632721d0dad162c214aca99e2c4f837ede13835

# `test_codex_runtime_home.py`

## Summary
- Codex CLI 実行時の Codex home 解決と事前検証を対象にしたテスト。環境変数未設定時の既定位置、相対パス指定時の扱い、profile 生成先、call log への記録、認証情報やディレクトリ種別の失敗時エラーを検証する。

## Read this when
- Codex CLI 呼び出し時に CODEX_HOME をどう環境へ渡すか、または内部的にどの絶対パスとして扱うかを変更する時。
- Codex home の存在確認、ディレクトリ確認、認証情報確認に関する失敗時メッセージや CmocError の内容を変更する時。
- Codex profile の配置先、profile 名の CLI 引数への反映、call log に残す Codex home 情報を確認する時。
- Codex CLI の実行 cwd と相対 CODEX_HOME の解決基準の関係を確認する時。

## Do not read this when
- Codex home 以外の Codex CLI 引数、標準出力イベント、容量待機、モデル指定、ファイルアクセスモード全般を調べたい時。
- 実際の Codex CLI 認証処理や外部サービスとの連携そのものを確認したい時。
- repository fixture、fake executable 作成、profile stub などのテスト支援部品の実装を調べたい時。

## hash
- a989ab21405d6144d79e829669f55418ae4b97c687add6f570fa9d2d518956f9

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex exec が quota exceeded で失敗した後の待機、probe、resume、再実行の外部挙動を検証する realization test。
- resume token 抽出、quota availability probe の生成・共有・失敗時挙動、call log・subcommand log・標準出力・prompt log・CODEX_HOME・cwd の扱いを、同じ retry 状態機械の観測点としてまとめて扱う。
- quota retry 回帰は fake Codex 呼び出し列を追う必要があるため、関連する並列実行、probe 代表選出、resume 可否、post validation 抑制の確認を一箇所に集約している。

## Read this when
- Codex exec の quota exceeded 後に、probe を挟んで resume または通常再実行する制御を変更・調査する時。
- quota availability probe のパラメータ、profile、prompt、CODEX_HOME、cwd、ログ記録、失敗時の扱いを確認する時。
- 複数の Codex exec が同時に quota 待機へ入った場合の代表 probe 共有、成功時の復帰、失敗時の全待機呼び出し失敗を調べる時。
- quota 待機上限到達時や probe 失敗時に、失敗した呼び出しの file access post validation を行わない挙動を確認する時。

## Do not read this when
- 通常成功する Codex exec の基本的な argv 組み立てや出力 JSON 読み取りだけを確認したい時。
- quota retry と関係しない file access mode、repository setup、Codex profile の一般仕様を調べたい時。
- quota availability probe prompt の自然言語内容や builder の正本仕様を確認したい時。
- subcommand log や call log の一般的な schema 全体を確認したい時。

## hash
- a8b9fedbc0ed4f2274433fc985acda31d011e2173715b35d4656187e8eebc2e6

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
- 118abe8694a4f2e5aa72946ec6b81d5fe4b3dd16e53c0fc49afa13326f3907f5

# `test_indexing_cli.py`

## Summary
- INDEX.md 生成・更新、indexing preflight、indexing subcommand、INDEX.md conflict 解決の外部挙動を検証する回帰テスト群。
- 対象列挙、hash 再利用、Codex 生成、commit 対象、dirty worktree 拒否、linked worktree、空ディレクトリ、直列生成、memo 除外、symlink cycle 回避を routing document 更新ワークフローとしてまとめて扱う。

## Read this when
- indexing CLI が INDEX.md を生成・更新・commit する条件を確認したいとき。
- indexing preflight と通常の indexing subcommand で dirty worktree、linked worktree、repo config、commit 対象の扱いがどう違うかを確認したいとき。
- 既存 INDEX.md entry の hash 再利用、malformed entry の再生成、Structured Output schema 不一致の拒否を変更・検証するとき。
- INDEX.md conflict 解決、空ディレクトリへの INDEX.md 配置、直列生成、root 直下 memo 除外、入れ子 memo 対象化、directory symlink cycle 回避に関わる実装を変更するとき。

## Do not read this when
- INDEX.md entry の自然言語内容そのものを設計・更新したいだけで、CLI 境界や git 状態の回帰確認が不要なとき。
- routing document 生成に関係しない subcommand、設定、agent call、apply join の挙動を調べたいとき。
- 単体 helper の内部実装だけを確認したく、外部 CLI 挙動、commit、worktree、git conflict の観測が不要なとき。

## hash
- e40e4a7a7de570e5a5e343b138b87c9256c9a1c5eeabc5ad72d0427a8a40cea1

# `test_indexing_preflight.py`

## Summary
- Codex 実行前に INDEX 更新の preflight が走ること、その更新が git commit され作業ツリーを汚さないことを検証する realization test。
- 実行対象 worktree の選択、repository lock 待機、特定 purpose での preflight skip を扱う。

## Read this when
- Codex 呼び出し前の indexing preflight の起動条件、skip 条件、実行順序を変更する。
- root と cwd が別 worktree を指す場合に、どの worktree の INDEX 更新を行うかを確認する。
- indexing lock の待機挙動や、preflight 更新後の git commit・clean status の期待を確認する。

## Do not read this when
- INDEX 生成内容そのもの、エントリー本文の品質、ルーティング文書の記述規則だけを確認したい。
- Codex 実行ラッパーではなく、通常の indexing 更新処理の差分検出や文書生成ロジックを確認したい。
- CLI 引数 parsing や設定読み込みなど、preflight 起動後の Codex 実行順序と関係しない領域を調べたい。

## hash
- 3acf23fa47098ab15a3be7f2e5aee79bf66f091be6fd7808f39b0c1e0f9f0f73

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
- a61448d13fe6b11acc398a8f268160b43e11b800fb149526e056ef20a992fdad

# `test_review_oracle_cli.py`

## Summary
- review oracle コマンドの外部挙動を CLI 経由で検証する realization test。report の生成内容、対象 oracle file の列挙、session/full scope、linked worktree、INDEX.md 変更の取り込み、異常時 report、review 実行中の不正差分拒否を扱う。
- 所見評価 loop の制御を検証する。enumerate が対象 oracle ごとの既存所見だけを受け取ること、challenger/advocate/judge/merge の呼び出しと結果反映、accepted/rejected/fatal/minor の集計、merge operation の契約違反検出を確認する。

## Read this when
- review oracle の report 出力内容、section 順、件数集計、accepted/rejected 所見の表示、error report の挙動を確認または変更したいとき。
- review oracle の対象 oracle file 列挙条件を確認または変更したいとき。特に AGENTS.md/INDEX.md 除外、git ignored だが tracked な oracle file、symlink、binary、memo 形状の path の扱いを確認する場合。
- review oracle の session scope と full scope、短縮 option、対象なしの場合の挙動を確認または変更したいとき。
- review oracle が linked worktree 上の session branch と oracle をどう扱うか、review worktree をどこに作るか、join commit を report にどう出すかを確認したいとき。
- review oracle 実行中に生成された INDEX.md 変更の merge、preflight indexing の commit 取り込み、INDEX.md conflict 解決、不正な非 INDEX.md 差分の拒否を扱うとき。
- 所見 loop の enumerate/validate/judge/merge の制御、prompt に渡す既存所見や challenger reason、merge operation の validation を確認または変更したいとき。

## Do not read this when
- review oracle 以外の review サブコマンドや通常の session 操作だけを扱うとき。
- CLI 経由の外部挙動ではなく、prompt 文面や Structured Output schema の正本仕様そのものを確認したいとき。
- oracle file や realization file の概念定義、path placeholder の定義など、正本仕様断片を確認したいとき。
- INDEX.md エントリー生成や一般的な routing 文書の規則だけを確認したいとき。
- review oracle の内部 helper の細部だけを局所的に確認でき、report・対象列挙・所見 loop・review worktree の統合挙動を読む必要がないとき。

## hash
- 155113381cb71b08bb9269a534e0298f473e63724d496fce0799fa59c598e1e9

# `test_session_cli.py`

## Summary
- session fork、join、abandon の CLI 回帰テストをまとめたファイル。session branch と session state のライフサイクルを中心に、linked worktree、state cleanup、dirty worktree 拒否、join 時の conflict 解消と branch 削除失敗時の外部挙動を検証する。

## Read this when
- session fork、join、abandon の CLI 外部挙動を変更・調査する。
- session state file の生成、破損検出、active/joined/abandoned への遷移、cleanup 失敗時の rollback を確認する。
- linked worktree 上での session 操作、session branch の作成・切替・削除、home branch への復帰を確認する。
- session join の conflict 解消 agent 呼び出し、oracle conflict write profile、conflict marker 検出、delete conflict staging、非 conflict 差分拒否を確認する。
- session join/abandon のエラー出力先、完了レポート、dirty worktree 拒否、branch 削除不能時の warning を確認する。

## Do not read this when
- session 以外の CLI サブコマンドの挙動を調べる場合。
- session fork/join/abandon の実装詳細だけを変更し、外部挙動や状態遷移の回帰確認が不要な場合。
- 単体 helper の純粋な入力出力だけを確認したい場合。ただし conflict marker block 検出の現行期待値を確認する場合は読む。

## hash
- 5d724e7a4e8f3299cc328546d84800bee93a6430bcc61025baac462c2a950dc4

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
