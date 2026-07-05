# `_support.py`

## Summary
- CLI テストで共有するリポジトリ作成、Git 状態確認、Codex home/profile のスタブ化、fake Ollama/systemctl 環境、doctor/init 実行、apply worktree 解決の補助関数をまとめたテスト支援モジュール。
- 外部コマンドや管理対象 Ollama を実際に使わず、Typer CLI と subprocess 制御を検証するための最小 fixture・fake executable 生成の入口になる。

## Read this when
- CLI テストで使う一時 Git リポジトリ、初期コミット、追跡済み ignored oracle file、現在ブランチを用意または検証したいとき。
- Codex CLI 実行テスト向けに CODEX_HOME、profile 生成、ローカル SLM、fake 外部コマンドをどう差し替えているか確認したいとき。
- doctor/init をテスト内で起動する共通手順や、fake managed Ollama/systemctl の環境変数・スクリプト生成を変更したいとき。
- session state から apply worktree path を解決するテスト補助を使う、またはその前提を確認したいとき。

## Do not read this when
- 個別コマンドの仕様や本体実装を確認したいだけなら、実装側の CLI・runtime モジュールへ直接進めばよい。
- oracle file の定義やテスト規則そのものを確認したい場合は、対応する oracle 文書を読む方がよい。
- 単一テストケースの期待値や外部挙動を確認したいだけなら、そのテスト本文を先に読めばよい。

## hash
- 6e65299890a06f72550c82713bf8533a62636006d84fce14771d3ada4fc3ca93

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
- active apply run を破棄する `apply abandon` の CLI 外部挙動を検証するテスト。apply worktree・branch・session state の cleanup、警告出力、実行位置の扱い、running apply process と記録済み child process の停止を同じ abandon 操作の境界条件として扱う。
- running state の process identity 欠落、破損した apply branch、linked session worktree の dirty 状態、stale apply branch など、cleanup 前に拒否すべき失敗条件も検証する。

## Read this when
- `apply abandon` の成功時に削除される worktree・branch・state 更新内容、または警告として許容する cleanup 対象欠落を確認したいとき。
- running apply run の停止順序、pid file 読み取り、child process group 停止、PID reuse・終了競合・zombie leader の扱いを変更または調査するとき。
- apply worktree 内、linked session worktree、linked apply worktree、stale apply branch から `apply abandon` を実行した場合の判定を確認したいとき。
- active apply run を破棄できない破損 state や dirty worktree の拒否条件を確認したいとき。

## Do not read this when
- apply run の作成、findings の解釈、または `apply fork` 自体の通常動作だけを確認したいとき。
- session fork や linked session の生成仕様そのものを調べたいとき。
- process 停止ではなく、apply 結果の取り込み・merge・commit など abandon 以外の apply 操作を調べたいとき。

## hash
- 361497a57d52cb6b226af2519632aac1d473777ec5f21e9956b34a27da4f2009

# `test_apply_fork_cli.py`

## Summary
- apply fork サブコマンドの CLI 挙動を検証する realization test。Codex 実行ループ、apply run の state 更新、apply worktree 配置、linked worktree 起点の branch/HEAD 利用、doctor preprocess、cmoc ignore 修復、設定読み込み失敗時の中断、`.gitignore` 編集、target normalization、report 生成前の completed 書き込みを扱う。

## Read this when
- `apply fork` の開始から完了までの外部挙動、state file、apply branch、apply worktree、report 生成順序を確認・変更したいとき。
- `apply fork` が Codex 呼び出しをどの目的で実行するか、所見列挙や所見適用の制御をテストしたいとき。
- linked worktree 上で `session fork` した後の `apply fork` が、linked worktree の現在 HEAD から apply run を始める挙動を確認したいとき。
- `apply fork` 実行前の doctor preprocess、`.cmoc/local/` ignore 補修、clean worktree 維持に関する回帰を調べるとき。
- `apply fork` の設定ファイル欠落・不正 JSON など、apply run を開始してはいけない失敗条件を確認したいとき。
- `normalize_apply_targets` の除外・保持ルールを、root 直下の memo、管理ディレクトリ、oracle 配下、binary file、tracked ignored file の観点で確認したいとき。

## Do not read this when
- `apply fork` の実装内部だけを変更し、外部挙動や state・worktree・target normalization の期待値を確認する必要がないとき。
- `apply fork` 以外の apply 系サブコマンド、session 操作、doctor 処理の単体仕様を探しているとき。
- Codex CLI や LLM 出力品質そのもののテスト方針を確認したいとき。
- INDEX 生成やルーティング文書の仕様を確認したいとき。

## hash
- 16e781a6547b00a686ffe2380f5cc164fd6a417db6dd4073fb16f5107361f30d

# `test_apply_fork_report_cli.py`

## Summary
- apply fork の CLI 経由の挙動を検証するテスト。所見列挙から適用、commit、変更要約、report 出力、session state 更新までの一連の制御を扱う。
- apply fork 用 ACP builder の import 可能性、prompt/schema の組み立て、変更ファイル再検査、未収束・収束・error report、rolling apply fork の差分基準を確認する。

## Read this when
- `apply fork` の report 内容、終了コード、収束判定、未収束判定、error 時の変更要約を変更または確認したいとき。
- apply fork が所見適用後に変更ファイルや新規ディレクトリ配下を再調査する制御を変更または確認したいとき。
- apply fork 用 ACP builder の import 経路、prompt に含める標準文書、structured output schema 参照を変更または確認したいとき。
- apply fork の commit 作成、apply branch、session state、rolling fork が参照する前回 apply join 情報を変更または確認したいとき。
- report 用変更要約が未追跡 file を含めるか、削除済み tracked file を除外するかを確認したいとき。

## Do not read this when
- apply fork 以外のサブコマンドの CLI 挙動だけを確認したいとき。
- apply fork の内部 helper 単体の細部だけを確認したく、CLI report や再検査 loop の外部挙動に関心がないとき。
- Codex 実行そのものや LLM 出力品質を検証したいとき。

## hash
- bbd8ca82801415dd0ba171b8547cf825479dc7f88677ded2af086e8f2ae67788

# `test_apply_join_cli.py`

## Summary
- apply join の CLI 外部挙動を検証するテスト。apply worktree から session への join 成功時の cleanup、state 更新、report 生成と、dirty worktree、stale apply branch、想定外差分、merge conflict、管理対象外 path 判定などの拒否・復旧条件を扱う。

## Read this when
- apply join の成功条件、後片付け、state 遷移、report 出力を変更または確認したいとき。
- apply join が apply worktree 内から実行された場合や、linked session worktree へ merge される挙動を確認したいとき。
- apply join の dirty worktree、stale apply branch、想定外差分、merge conflict、force resolve の扱いを変更または確認したいとき。
- apply join における realization path、oracle、memo、AGENTS.md、.codex、tracked ignored file、deleted path、rename path の分類を確認したいとき。

## Do not read this when
- apply fork の Codex 実行内容や fork 作成そのものを確認したい場合は、apply fork 側のテストまたは実装を読む。
- session fork の branch/worktree 作成挙動だけを確認したい場合は、session fork 側のテストまたは実装を読む。
- apply join の内部 helper の実装詳細だけを調べたい場合は、対応する apply join 実装を直接読む。
- oracle file や realization file の一般定義を確認したい場合は、oracle 配下の仕様断片を読む。

## hash
- 9e784f57d7f6b5c401012741e163966a9c7c9b553abe01b18419b4d5333433bc

# `test_basic_runtime.py`

## Summary
- cmoc の基礎 runtime 契約を横断検証する realization test。root placeholder と worktree 判定、config 読み込み・検証、CmocError の表示、CLI preflight と parse error、subcommand log、gitignore 更新、FileAccessMode から Codex sandbox/profile への変換、binary 判定、session state branch 解析をまとめて扱う。
- 個別サブコマンド単体ではなく、実行前提として同時に崩れやすい runtime 境界の回帰確認を担う。

## Read this when
- root/repo/work/run root の解決、linked worktree、run worktree 作成・削除の安全条件を変更・調査する時。
- cmoc config の既定値、辞書からの構築、型検証、missing config error を変更・調査する時。
- CmocError の Markdown report、CLI error の stdout/stderr、Click parse error、work root preflight、completion probe、subcommand log 生成条件を変更・調査する時。
- FileAccessMode、Codex profile、sandbox writable roots、extra writable/read paths、oracle conflict write、local SLM provider の挙動を変更・調査する時。
- session/apply branch 名から session id や state を読む制御、binary 判定、duration 表示、起動 wrapper の call stack 表示を変更・調査する時。

## Do not read this when
- apply、review、session など個別サブコマンド固有の業務ロジックだけを確認したい時。
- oracle doc や oracle src の正本仕様そのものを確認したい時。
- 単一 helper の内部実装だけを追えば足り、runtime 境界をまたぐ外部挙動や CLI 表示に影響しない時。

## hash
- ec99e0e08d126e5c5c21de8446890ee66b607d2db8bdd22d7588d73a0a431ddb

# `test_cli_tui.py`

## Summary
- TUI サブコマンド起動前の CLI 前処理を、外部挙動として検証するテスト。エディタで作成された依頼文の整形、parameter resolve 用の Codex exec 呼び出し、TUI 用 Codex parameter 構築、prompt 保存先、`.cmoc/local` の ignore とログ配置を扱う。
- 通常 worktree と linked worktree の両方で、TUI 起動時に root と cwd が分離され、schema・prompt・ログが repo root 側の `.cmoc/local` に置かれることを確認する。

## Read this when
- TUI サブコマンドの起動直前処理、prompt 作成、resolve_parameter の呼び出し条件、launch_tui schema の指定、または `run_codex_tui` へ渡す `AgentCallParameter` を変更する時。
- linked worktree 上で `tui` を実行した場合の `.cmoc/local` の保存先、root/cwd の扱い、`.gitignore` 更新、sub_command/tui ログ配置を確認したい時。
- 空文字の resolved file access mode を readonly へ戻す既定挙動を変更または確認する時。

## Do not read this when
- TUI 画面そのものの対話挙動や表示を調べたいだけで、起動前の CLI 前処理・prompt 保存・Codex 呼び出し parameter に関心がない時。
- TUI 以外のサブコマンドのログ形式や `.cmoc/local` 管理を調べる場合で、より直接そのサブコマンドのテストがある時。
- oracle file や INDEX.md の仕様記述そのものを調べたい時。

## hash
- e7782f01dad7fd46bef6892713197c923251aa615bf9a4f7bad29e1376e24d8f

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 実行・TUI 起動まわりの runtime 挙動を検証するテスト群。プロファイル生成、作業ディレクトリ、sandbox writable_roots、schema 出力先、管理 Ollama profile、subprocess の apply tracking、Codex CLI 不在や非 0 終了時のエラー報告を扱う。
- Codex 呼び出し後の file access 差分を事後検証しない方針を、oracle、.git、README、ignored 生成物、一時 cache、blocked runtime dir、.cmoc log、linked worktree などのケースで確認する。

## Read this when
- run_codex_exec、run_codex_tui、run_codex_subprocess、run_tracked_codex_subprocess の引数、環境変数、profile 生成、ログ・schema 保存先、cwd の挙動を変更する時。
- Codex 呼び出し後に forbidden/blocked/ignored/temporary な差分をどう扱うか、または post-call file access validation を追加・削除・変更する時。
- PURE_ORACLE_READ、READONLY、REALIZATION_WRITE、REPO_WRITE の各 file access mode が Codex runtime profile と writable_roots にどう反映されるかを確認する時。
- linked worktree からの Codex 実行、repo root 配下の .cmoc local schema/log、extra_read_paths、extra_writable_paths、allow_oracle_conflict_writes に関わる runtime 変更を行う時。
- Codex CLI が見つからない場合や TUI/exec の非 0 終了時に、CmocError と console/report 出力が期待通りか確認する時。

## Do not read this when
- Codex runtime の実装ではなく、agent call parameter や model/config 型そのものの単体仕様だけを調べたい時。
- Codex 以外の外部コマンド実行、git 操作 helper、repository fixture の一般挙動だけを調べたい時。
- oracle file や realization file の定義・分類そのものを確認したい時。
- INDEX.md ルーティングや文書生成規則のテストを探している時。

## hash
- 2d06e820e15b2353769c6bbe21eb5c821f00a57d828832eeab8d4c573ed68720

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
- Codex exec が quota exceeded になった後の待機、probe、resume、再実行の制御を検証する realization test。
- quota retry 状態機械の観測点として、probe 共有、resume token 抽出、call log、subcommand log、CODEX_HOME、cwd、並列呼び出し時の代表 probe をまとめて扱う。

## Read this when
- Codex exec の quota exceeded 検出後に、availability probe を実行して復帰後に resume または再実行する挙動を確認・変更したいとき。
- quota availability probe の AgentCallParameter、最小モデル、low reasoning、readonly、cwd 継承、実際の probe prompt を検証したいとき。
- quota retry 中の call log、stdout/output jsonl log、prompt log、subcommand log、console 表示の記録内容を確認したいとき。
- resume token を JSONL log から抽出する挙動、token がない場合の再実行挙動、relative CODEX_HOME と cwd の扱いを確認したいとき。
- 並列に quota 待機した Codex exec が単一の代表 probe を共有し、probe 成功時は各呼び出しが復帰し、probe 失敗時は待機中の呼び出しも失敗する制御を確認したいとき。
- quota 待機上限到達時や probe 失敗時に、quota で失敗した呼び出し・probe 呼び出しへ file access post validation をかけない挙動を確認したいとき。

## Do not read this when
- quota retry 以外の Codex exec 正常実行、引数構築、構造化出力処理だけを確認したいとき。
- quota availability probe の実装本文や prompt builder の責務を確認したいだけで、retry 時の外部挙動テストを読む必要がないとき。
- SubcommandLogger や call log 形式そのものの汎用仕様を確認したいだけで、quota retry 時の記録内容に関心がないとき。

## hash
- 9608587e76e52a1c7407c7978c17b649f56cb3fdb3532325b3f790841089e8ad

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

# `test_doctor_cli.py`

## Summary
- doctor と init の CLI 周辺挙動を検証する pytest 群。cmoc 管理 Ollama の導入・systemd user service 生成・service 検証・モデル pull、.cmoc/config.json の生成または非同期、.gitignore と git 追跡状態の修復、既存 staged 変更を repair commit に混ぜないこと、ローカル SLM profile 準備時の doctor 実行を扱う。

## Read this when
- doctor preprocess、init、cmoc 管理 Ollama、runtime_doctor、runtime_codex_profile、または .cmoc/config.json の生成・無視・追跡解除に関する外部挙動を変更する時。
- repair commit が .gitignore や .agents/.gitkeep をどう扱い、既存 staged 変更をどう保護するかを確認したい時。
- Ollama service の main PID、listener process、model pull 対象の重複排除、またはローカル SLM profile 作成時の service 自動準備を変更・調査する時。

## Do not read this when
- doctor や init の CLI 外部挙動に関係しない設定モデル、path model、agent call 実行制御だけを調べる時。
- Ollama service の実装詳細だけを確認したい場合で、期待されるテスト挙動ではなく実装本文を直接読む方が適切な時。
- oracle file の正本仕様そのものを確認したい時。

## hash
- b54fbb56e81126f4346efe55719d4e554fca461b66ad80f546702e27b37a1848

# `test_indexing_cli.py`

## Summary
- INDEX.md の生成・更新、hash 再利用、Codex entry 生成、commit 対象、dirty worktree 拒否、linked worktree 対象化、apply preflight、INDEX.md conflict 解決を CLI 境界から検証する indexing 回帰テスト。
- routing document 更新ワークフローの外部挙動を、git 状態、fixture、commit 履歴、preflight の設定参照、並列・直列生成制御、memo 除外、symlink cycle 除外まで含めて一箇所で扱う。

## Read this when
- indexing subcommand または indexing preflight の CLI 挙動、commit 条件、dirty worktree 判定、linked worktree 上の更新対象、Codex entry builder 呼び出し条件を確認・変更する。
- INDEX.md の malformed entry 再生成、fresh hash による生成スキップ、空ディレクトリの INDEX.md 作成、兄弟 entry の生成順、非祖先 directory の並列生成、memo directory や directory symlink の扱いを確認する。
- apply workflow で INDEX.md conflict を解決する処理が、INDEX.md を削除して unmerged 状態を解消し merge commit を成立させることを検証する。

## Do not read this when
- routing entry の本文表現や Structured Output schema だけを確認したい場合は、実装または oracle 側の prompt/schema 定義を読む方が直接的。
- indexing 以外の subcommand、agent call 全般、設定ファイル形式そのもの、または git helper の低レベル実装だけを調べる場合。
- 単体の内部 helper のアルゴリズム詳細を読む目的で、CLI 境界の回帰シナリオや git 状態を確認する必要がない場合。

## hash
- 40cda8c97ac4a60ea4e43e9c6275698dd62f61582aeebc49678f278af9da0b93

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
- パッケージ化された配置で、realization 側の import 経路が oracle src の正本定義を直接コピーせず参照できることを検証するテスト。
- 一時的な site 配置へ必要なパッケージをコピーし、`PYTHONPATH` をその配置に限定した subprocess 上で、review oracle builder、basic builder、cmoc config の公開 import 境界を確認する。
- oracle src 由来の定義を realization 側が再エクスポートする構造や、packaging 設定と実行時 import の整合性を扱うテストへの入口となる。

## Read this when
- パッケージング後の `oracle` package 配置、`package-dir`、または package discovery の設定変更が import に与える影響を確認したいとき。
- `acp.builder.review.oracle.enumerate_finding`、`acp.builder.basic`、`config.cmoc_config` の import 境界や再エクスポート挙動を変更するとき。
- oracle src の定義を realization src にコピーせず利用する方針が、隔離された import 環境でも維持されるかを検証したいとき。
- subprocess と一時コピー配置を使った packaged layout 系テストの既存パターンを確認したいとき。

## Do not read this when
- 通常の CLI 実行フロー、コマンド引数、標準出力、終了コードの挙動を調べたいだけのとき。
- prompt 本文の生成規則や review oracle standard の内容そのものを確認したいとき。
- 設定 dataclass のフィールド意味や validation 仕様を調べたいとき。
- ローカルの editable install や開発環境全体のセットアップ手順を知りたいだけのとき。

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
- review oracle の CLI 経由の外部挙動を検証するテスト。report 生成、対象 oracle file の選択、所見の列挙・検証・judge・merge、scope 指定、error report、review 用 worktree と join commit、INDEX.md 変更の取り込み、非 INDEX 差分の拒否を扱う。
- 所見評価 loop の制御を直接検証するテストも含み、enumerate 時の既存所見の渡し方、challenger/advocate の理由伝播、merge operation の契約と semantic retry を確認する。

## Read this when
- `review oracle` CLI の report 内容、section 順、count、accepted/rejected finding の表示、error report の挙動を変更または調査するとき。
- review oracle の対象ファイル列挙、full/session scope、tracked ignored oracle file、`AGENTS.md` と `INDEX.md` の除外、oracle root alias の扱いを確認するとき。
- review oracle 実行時の一時 worktree、linked worktree、review join commit、INDEX.md 変更の merge、INDEX.md conflict 解決、非 INDEX 差分の拒否を扱うとき。
- review oracle の finding loop、validate challenger/advocate、judge、merge operation、semantic retry、finding id 採番の制御を変更するとき。

## Do not read this when
- oracle review ではないサブコマンド、または CLI 経由の review oracle 外部挙動に関係しない内部 helper だけを扱うとき。
- realization file 全般の file classification や path model の正本仕様を確認したいときは、oracle 配下の該当仕様を読む。
- INDEX.md エントリー生成そのものやルーティング文書の形式だけを扱うときは、このテストではなく対象のルーティング規則を読む。

## hash
- 526c05c8b3b39046eb1b55cbcb4c50bb3c1e7c75c8a39ef5375d73f23d6277b2

# `test_session_cli.py`

## Summary
- session fork、join、abandon の CLI 回帰を、session branch と session state のライフサイクルを軸に検証する realization test。
- linked worktree、state cleanup、dirty worktree 拒否、session-id 衝突、壊れた state、join conflict 解消、branch 削除失敗時の出力など、session CLI の外部挙動と状態遷移をまとめて扱う。
- 16,000 文字を超えるが、同じ branch/state fixture を追う session CLI 回帰として凝集しているため一箇所に保つ意図が本文冒頭に記録されている。

## Read this when
- session fork が session branch と state file を作る挙動、session-id 衝突時の retry・失敗、壊れた session state の拒否を確認したいとき。
- session abandon が home branch へ戻る挙動、state を abandoned にする挙動、home branch 不在や cleanup 失敗時の rollback・エラー出力を確認したいとき。
- session join が session branch の変更を home branch へ反映する挙動、joined state、session branch 削除可否、delete conflict 解消を確認したいとき。
- linked worktree 上で session fork、join、abandon を実行した場合の branch 選択、state 保存場所、preprocess の挙動を確認したいとき。
- oracle conflict 解消 agent の file access mode、書き込み許可範囲、conflict 解消以外の差分拒否、conflict marker 検出を確認したいとき。
- session join、abandon の成功・失敗時に stdout と stderr のどちらへ完了報告やエラーが出るかを調べたいとき。

## Do not read this when
- session CLI の実装構造や内部 helper の責務を変更したいだけで、外部挙動の回帰条件を確認する必要がないときは、対応する実装側を先に読む。
- session 以外の sub command、設定読み込み、共通 runtime、doctor の個別仕様を調べたいときは、それぞれの対象へ直接進む。
- 単体の git wrapper、path helper、ログ出力 helper の細部だけを確認したいときは、session CLI 全体の回帰を扱うこの対象から始めなくてよい。
- oracle file の正本仕様そのものを確認したいときは、realization test ではなく oracle 側の該当箇所を読む。

## hash
- 889f628ebbcd43943748868134d19693e97a29e71663a845e5034a26fe6e9d32

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
