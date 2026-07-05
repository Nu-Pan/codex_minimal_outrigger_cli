# `_support.py`

## Summary
- cmoc CLI のテストで共有される補助関数群。最小 Git リポジトリの作成、Codex home/profile のスタブ化、fake Ollama/systemctl 実行環境、Typer CLI runner、apply 用 worktree path 解決など、複数テストから使う外部状態の準備を担う。

## Read this when
- CLI テスト用の Git リポジトリ、tracked かつ ignored な oracle file、Codex home、fake Codex profile を準備する既存 helper を確認・再利用したいとき。
- doctor や profile 生成を伴うテストで、fake Ollama や fake systemctl の挙動、環境変数、サービス PID の扱いを調整したいとき。
- session state から apply worktree path を解決するテスト補助処理を確認したいとき。
- テスト内で外部コマンド相当の Python 実行ファイルを生成する処理を共通化したいとき。

## Do not read this when
- 個別サブコマンドの期待出力やシナリオそのものを確認したいだけで、共有 fixture や fake 外部コマンド環境を変更しないとき。
- 本番実装の Codex 実行、TUI、apply、doctor の制御ロジックを調べたいとき。
- oracle file や realization file の定義・分類そのものを確認したいとき。

## hash
- c85bdfcd41ee21c513b6b6cbdf6dd42298568e369c47e1549b18a99afbcc53af

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
- apply abandon が active apply run を破棄する外部挙動を CLI 経由で検証する realization test。worktree・branch・state の cleanup、missing cleanup target の warning、running process と Codex child process group の停止順序、PID reuse・race・lock 待ち、apply worktree や linked session worktree からの実行位置判定、破損 state や stale apply branch の拒否条件を扱う。
- 16,000 文字を超えるが、active apply run の abandon に関する成功・警告・失敗条件と共有 fixture を一箇所で読むための凝集したテストとして位置づけられている。

## Read this when
- apply abandon の CLI 挙動、cleanup 結果、出力内容、state 更新、branch/worktree 削除条件を確認・変更したいとき。
- running apply process の停止、Codex child process group の停止順序、PID file 読み取り、tracking lock、PID reuse や終了 race の扱いを確認・変更したいとき。
- apply abandon を repo root、apply worktree、linked session worktree、linked apply worktree、stale apply branch から実行した場合の判定を確認・変更したいとき。
- apply abandon が破損 state、process identity 欠落、未コミット差分、active run ではない apply branch を拒否する条件を確認・変更したいとき。

## Do not read this when
- apply fork や session fork の生成処理そのものを確認したいだけで、abandon の前提 fixture としての利用に関心がないとき。
- apply abandon 以外の subcommand の CLI 仕様や一般的な session state 管理を確認したいとき。
- Codex 実行結果の品質、findings の内容、LLM 出力そのものを検証したいとき。
- INDEX.md 生成規則や oracle/realization の一般標準を確認したいとき。

## hash
- 0aa147edb6623ca11edd2f7145f55bbc19068f1ee03e1e848fec0eb29401ef96

# `test_apply_fork_cli.py`

## Summary
- apply fork コマンドの CLI 経路と内部本体を、実際の git repository・session state・worktree・report 生成・Codex 実行呼び出しの境界で検証する realization test。
- apply fork が session branch から apply branch/worktree を作成し、state を completed に更新し、旧状態 field や pid file を残さないことを確認する。
- 対象正規化が realization file 定義に沿って root 直下の管理領域・規範文書・ignore 状態を扱い、編集対象として残すべき tracked ignored file や binary file を保持することを検証する。

## Read this when
- apply fork の CLI 挙動、state 遷移、apply branch/worktree 作成、report 生成前後の完了状態を変更または調査するとき。
- apply fork 実行前の doctor preprocess、cmoc ignore 修復、config 読み込み失敗時の副作用抑止、missing config 修復を確認するとき。
- apply fork の対象列挙・対象正規化で、memo、oracle、.cmoc、.codex、.agents、INDEX/AGENTS、git ignore、binary file の扱いを変更するとき。
- Codex 実行ループの呼び出し目的、所見列挙、所見適用、変更 summary 生成のテスト境界を確認するとき。

## Do not read this when
- apply fork 以外の session fork、doctor、設定読み込み、git helper の単体仕様だけを調べたいときは、それぞれの実装または専用テストを直接読む。
- INDEX.md エントリー生成規則や oracle/realization file の定義そのものを確認したいときは、正本仕様側を読む。
- 実際の Codex CLI 出力品質や LLM 応答内容を評価したいとき。この対象は Codex 呼び出しを fake に置き換え、制御ロジックと副作用だけを検証する。

## hash
- 4c5f30dd623e51a0f2c44274de6142ccfa584e5603f42e67387da5047675bc8d

# `test_apply_fork_report_cli.py`

## Summary
- apply fork の CLI 挙動を、所見列挙、所見適用、commit、変更要約、report 生成、session state 更新まで一連の制御として検証するテスト。
- apply fork report の収束、未収束、error、変更ファイル再調査、rolling fork、変更要約 builder の import・schema・prompt 構成を同じ観測文脈で扱う。

## Read this when
- apply fork の report 内容、終了コード、収束判定、未収束時の表示、error report の変更要約を確認・変更したいとき。
- apply fork が変更後ファイルや新規ディレクトリ配下を再調査する制御、上限回での収束・未収束判定、差分なし適用時の扱いを確認したいとき。
- apply fork の変更要約が未追跡ファイルを含み、削除済み tracked file を除外する挙動を確認したいとき。
- apply fork 関連の ACP builder が src 直下の PYTHONPATH や packaged layout で import できること、完全な標準 prompt と oracle schema を使うことを検証したいとき。
- rolling apply fork が前回 apply join 後の oracle 変更だけを対象にする session state 更新を確認したいとき。

## Do not read this when
- apply fork の内部 helper 分割や実装詳細だけを調べたい場合は、対象の実装ファイルを先に読む。
- apply fork 以外の subcommand、session fork/join 一般、doctor、config 初期化の挙動を調べたい場合は、それぞれの専用テストや実装へ進む。
- Codex 実行基盤そのもの、汎用 ACP builder、path model、oracle 標準の正本仕様を確認したい場合は、この CLI 結合テストではなく対応する oracle file または実装を読む。

## hash
- 43e9f6808546ef7b56964b3228cf2ab001f9a3f8827e088f8658d4da094a5edd

# `test_apply_join_cli.py`

## Summary
- apply run を session へ join する CLI 外部挙動を検証するテスト。
- apply join の成功時 cleanup、state 更新、report 生成、linked session worktree への merge、apply worktree からの実行可否を扱う。
- dirty worktree、stale apply branch、想定外差分、tracked ignored file、削除・rename path、merge conflict、INDEX conflict 解決など、join の受理・拒否境界をまとめて検証する。

## Read this when
- apply join の CLI 挙動、終了コード、標準出力、report、state 遷移、worktree/branch cleanup を変更・調査するとき。
- apply branch と session branch の差分分類、realization/oracle/.codex/memo/AGENTS.md/INDEX.md の扱いを確認するとき。
- apply join の merge conflict、想定外差分、force-resolve の挙動、linked worktree 上の session への反映を確認するとき。

## Do not read this when
- apply fork の Codex 実行内容や apply worktree 作成だけを確認したいとき。
- session fork の branch/state 初期化だけを確認したいとき。
- apply join の内部 helper 実装を先に読みたいときは、対応する実装ファイルを直接読む。

## hash
- 0c76601fa64ea8b6bfa5e1d6b96e7814977b107a7316ad6e93dcb3e53b40c3fd

# `test_basic_runtime.py`

## Summary
- cmoc の基礎 runtime 契約を横断的に検証する realization test。root 解決、config 読み込み、CmocError 表示、CLI error 出力、subcommand log、FileAccessMode と Codex sandbox profile、binary 判定、session state branch 解析、worktree 作成・削除の安全条件を、個別サブコマンドより下位の共通前提としてまとめて扱う。
- 複数領域にまたがる回帰を 1 箇所に置くことで、共通 fixture と root 状態の読み取り文脈を分散させず、basic runtime の崩れを検出する入口になる。

## Read this when
- cmoc の実行前提、root/worktree/repo root の解決、placeholder path、linked worktree の扱いを変更・確認する。
- config の既定値、dict からの config 変換、型不正時の CmocError、論理 model class や reasoning effort の扱いを変更・確認する。
- CLI の preflight、Click 解析 error、想定済み error の stdout report、CmocError の Markdown 表示、起動 wrapper の call stack 表示を変更・確認する。
- subcommand log の生成条件、timestamp 衝突時の log path、pre-log check failure 時の副作用抑制を変更・確認する。
- FileAccessMode、Codex profile、sandbox writable roots、追加書き込み許可 path、linked worktree からの repo local read、session join conflict target の許可境界を変更・確認する。
- session/apply branch 名から session id を読む処理、破損 branch 名の拒否、session state 読み込み条件を変更・確認する。
- `.cmoc` ignore pattern の追加、managed worktree path の安全確認、worktree 作成・削除時に管理外 path を破壊しない条件を変更・確認する。
- binary 判定や duration 表示など、個別機能よりも runtime 共通契約として扱われる小さな基礎挙動を変更・確認する。

## Do not read this when
- 個別サブコマンド固有の正常系や業務ロジックだけを確認したい場合は、そのサブコマンドの実装・テストへ進む。
- oracle file の正本仕様そのものを確認・編集したい場合は、対応する oracle doc/src/test を読む。
- INDEX.md エントリー生成やルーティング文書の構成だけを扱う場合は、対象本文の責務把握に必要な範囲を超えてこのテストの詳細 assertion を読む必要はない。
- UI 表示、LLM 出力品質、外部サービス連携など、basic runtime 境界に含まれない挙動を調べる場合は、より直接の対象を探す。

## hash
- 5f73704a7fd614798d14052b4d1a85678f7533748c0d9f934c94866646c4bc4c

# `test_cli_tui.py`

## Summary
- TUI サブコマンド起動前の CLI 前処理を、外部コマンド呼び出し・生成プロンプト・ログ保存先・linked worktree での root/cwd 扱いから検証するテスト。エディタで編集された依頼文を resolve parameter に渡し、解決結果から TUI 起動用パラメータと schema path、extra_read_paths、.cmoc/local 配下のログと .gitignore が整うことを確認する。

## Read this when
- TUI サブコマンドの起動前処理、エディタ起動後の依頼文整形、resolve parameter の結果反映、run_codex_tui への引数を変更する。
- TUI の complete prompt、orig prompt、sub_command ログ、launch_tui.json や resolve_parameter.json の配置・参照方法を変更する。
- linked worktree 上で tui を実行したときの保存先、root/cwd、.cmoc/local の ignore 状態、schema 生成場所を確認する。
- file_access_mode の解決値が空の場合のデフォルト挙動を確認する。

## Do not read this when
- TUI 内部画面の描画や対話操作そのものを確認したい場合。
- Codex 実行ラッパー全般の低レベルな挙動だけを確認したい場合。
- doctor、git helper、テスト用 repo 作成 helper の詳細だけを確認したい場合。

## hash
- f4c67d69d00fa03a5f56318ca591b648cb24ddeb07dd59606c0af73aaf26cd2d

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 実行/TUI 呼び出しのテスト群。プロファイル生成、作業ディレクトリ、sandbox 設定、schema 出力、プロセスグループ追跡、Codex CLI 欠落・非ゼロ終了時のエラー、実行後 diff を追加検証しない方針を検証する。
- oracle・memo・blocked runtime 領域・git 管理外キャッシュ・linked worktree・追加 read/write path など、Codex 呼び出し時のファイルアクセス境界とログ/状態配置に関する外部挙動を扱う。

## Read this when
- Codex CLI を exec または TUI として起動する runtime 実装の挙動を変更する時。
- Codex 用 profile、sandbox writable_roots、local provider、managed ollama、schema state、call log、prompt log の生成や配置を確認する時。
- FileAccessMode ごとの許可領域、extra_read_paths、extra_writable_paths、linked worktree の cwd/--cd、実行後 diff の扱いを変更・調査する時。
- Codex subprocess のプロセスグループ追跡、継承された apply tracking 環境変数の無視、Codex CLI 欠落や非ゼロ終了のエラー表示を確認する時。

## Do not read this when
- Codex 呼び出し runtime ではなく、通常の cmoc サブコマンドや oracle 文書生成ロジックだけを扱う時。
- ファイルアクセス分類そのものの定義や path model の正本仕様を確認したい時。まず対応する oracle 側の仕様断片を読む。
- テスト支援 fixture や一時リポジトリ作成 helper の詳細だけを変更する時。支援コード側を直接読む。

## hash
- 1d8c0822bb39e9ac2f37e98d3edaf3b837cd14265d1e9712bc2d8796939a3864

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

# `test_doctor_cli.py`

## Summary
- doctor/preprocess と managed Ollama 連携の外部挙動を検証するテスト群。git 修復、`.cmoc` の追跡除外、`.agents` 初期化、修復 commit の範囲、既存 staging の保持、設定同期、cmoc provider model の pull、ローカル SLM profile 作成時の doctor 実行を扱う。

## Read this when
- doctor/preprocess が git 状態や管理対象外ファイルをどう修復するかを確認・変更する時。
- managed Ollama のインストール配置、systemd user service、model pull、profile 生成との連携を変更する時。
- デフォルト設定同期で既存の人間設定を上書きしないこと、または `.cmoc` を git 追跡対象にしないことを検証する時。
- doctor の修復 commit が既存の staged change を巻き込まないことを確認する時。

## Do not read this when
- doctor/preprocess 以外の CLI コマンド挙動を確認したいだけの場合。
- Ollama や Codex profile とは無関係な設定 schema の静的定義だけを確認する場合。
- テスト支援関数や一時 git repository 作成方法そのものを調べたい場合は、共有 fixture・support 側を直接読む。

## hash
- ea45c539449cb08d7407ab84e8b60eaa67ef57c27578a48a9f6d63143115fd55

# `test_indexing_cli.py`

## Summary
- INDEX.md 生成・更新と conflict 解決に関する CLI 回帰テストをまとめたファイル。indexing 実行時の Codex 呼び出し、hash 再利用、commit 対象、dirty worktree 拒否、linked worktree、preflight、 malformed entry 再生成、空ディレクトリ・memo・symlink cycle・並列生成の外部挙動を検証する。

## Read this when
- indexing サブコマンドまたは indexing preflight の外部挙動、commit 条件、対象列挙、INDEX.md conflict 解決を変更する時。
- INDEX.md entry の schema 検証、fresh hash 判定、malformed entry 再生成、空ディレクトリや symlink cycle の扱いを確認する時。
- linked worktree や apply worktree での indexing 対象 root、設定参照、dirty worktree 拒否条件を確認する時。

## Do not read this when
- INDEX.md entry のレンダリングや対象列挙の実装詳細だけを局所的に確認したい場合は、先に indexing 実装や共通処理を読む。
- apply join 全般や merge 処理全般を調べる場合で、INDEX.md conflict 解決に関係しない時は対象外。
- Codex 実行基盤、config schema、doctor 初期化処理そのものを調べる場合は、それぞれの実装・テストを直接読む。

## hash
- 4d598793c24667f9dbaeb8e46867f8ad5b8ee3e5306ac81ae54cba361e7e1588

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
- review oracle の CLI 実行を通じて、report 生成、対象 oracle file の列挙、所見の列挙・検証・judge・merge、review 用 worktree で生じた INDEX.md 差分の取り込み、異常時 report を検証する realization test。
- review run の状態と出力を共有する外部挙動テストを一箇所に集約し、full scope と session scope、tracked ignored oracle file、linked worktree、merge operation の契約、非 INDEX.md 差分拒否を扱う。

## Read this when
- review oracle コマンドの report 出力、集計値、section 順序、accepted/rejected finding の表示を変更または確認したいとき。
- review oracle の対象 oracle file 列挙条件、full/session scope、tracked ignored file、AGENTS.md/INDEX.md 除外、linked worktree 上の対象選択を確認したいとき。
- 所見 loop の enumerate、validate challenger/advocate、judge、merge operation、同一 round の理由伝播、対象別 prompt 文脈を変更または確認したいとき。
- review 実行中に生成された INDEX.md 差分の join、preflight indexing 差分の取り込み、INDEX.md merge conflict 解消、非 INDEX.md 差分拒否の挙動を変更または確認したいとき。
- review oracle の途中失敗時に error report を残す挙動や、CLI 出力先を確認したいとき。

## Do not read this when
- review oracle 以外の review サブコマンドや、oracle を対象にしない CLI 挙動だけを扱うとき。
- report の最終表示ではなく、prompt 文面そのものや Structured Output schema の定義だけを確認したいとき。
- session fork、doctor、git worktree 操作などの基盤機能を単体で確認したいとき。
- INDEX.md エントリー生成そのものや indexing 全般の仕様を確認したいとき。

## hash
- 79909773d6fe2fab5ae58a4d4878cd384837bbf704c610226668f7e26b70b200

# `test_session_cli.py`

## Summary
- session fork/join/abandon の CLI 外部挙動を、branch と session state のライフサイクルを中心に検証する回帰テスト。
- session branch の作成・削除、state file の作成・更新・rollback、linked worktree 上の挙動、dirty worktree 拒否、join 時の conflict 解消 agent 呼び出し、エラー出力先をまとめて扱う。
- 16,000 文字超のファイルだが、同じ branch/state fixture を共有する session CLI 状態遷移の観測点として凝集している。

## Read this when
- cmoc session fork/join/abandon の CLI 外部挙動を変更・確認する。
- session state file の active/joined/abandoned 遷移、必須 field 欠落、破損 state、session-id collision の扱いを確認する。
- session branch と home branch の切替、削除可否、linked worktree での branch/head/state の扱いを確認する。
- session join の merge conflict 解消、oracle conflict 書き込み profile、conflict marker 検出、delete conflict 解消、conflict agent が残した余計な差分の拒否を確認する。
- session abandon/join の失敗時 rollback、cleanup 失敗、stdout/stderr へのエラーレポート出力を検証する。

## Do not read this when
- session CLI 以外のサブコマンド挙動や一般的な CLI 起動だけを確認したい。
- session 状態遷移ではなく、個別 helper の純粋な単体ロジックだけを確認したい。
- oracle conflict 解消や branch/state cleanup を伴わない通常の git 操作 wrapper を確認したい。
- テスト支援 fixture や repo 作成 helper の定義を調べたい場合は、支援モジュールを直接読む。

## hash
- ffa4b4bdfc025ffdf8e77ac70cd8b16c2b737bd17c8866d0d9010f9719039149

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
