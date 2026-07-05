# `_support.py`

## Summary
- CLI テストで共有する pytest/CliRunner 用の補助関数群。最小 Git リポジトリ作成、Codex home/profile の差し替え、fake 外部コマンド生成、doctor 実行環境、apply worktree 解決など、複数テストから使う共通セットアップを担う。

## Read this when
- cmoc CLI のテストで使う一時 Git リポジトリ、tracked かつ ignored な oracle file、Codex home、Codex profile のスタブを用意する共通 fixture 相当の処理を確認・変更したいとき。
- doctor や profile 作成を伴うテストで、fake Ollama、fake systemctl、管理対象 Ollama 環境の挙動を調べたいとき。
- テスト内で fake Python executable を生成する方法、現在 branch の確認、apply session state から worktree path を解決する方法を再利用または修正したいとき。

## Do not read this when
- 個別 CLI コマンドの期待出力や終了コードなど、テストケース本体を確認したいだけのときは、該当する test file を直接読む。
- 本番実装の Git 操作、Codex 実行、Ollama 管理、apply worktree 計算の仕様を確認したいときは、対応する src 側の実装または oracle file を読む。
- INDEX.md の生成規則や oracle/realization の責務境界を確認したいときは、このテスト補助ではなく該当する正本仕様を読む。

## hash
- 65e8db6f52f5e82aa6a34618ff8299eebdbb18546a8bb15d2e6087d5054f7f1e

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
- apply run を session へ join する CLI 外部挙動を検証するテスト。成功時の worktree/branch cleanup、state 更新、report 生成と、dirty worktree、stale branch、想定外差分、merge conflict などの拒否条件を扱う。
- apply join が扱う realization/session/oracle/.codex/memo/INDEX.md などの path 分類や、force resolve 時の差分破棄・復元挙動も検証対象に含む。

## Read this when
- apply join の成功・失敗条件、後片付け、状態更新、report 出力に関するテストを確認または変更するとき。
- apply worktree から実行した join、linked session worktree からの join、stale apply branch の拒否など、実行場所や branch 状態に依存する挙動を確認するとき。
- apply join の想定外差分検出、force resolve、merge conflict 処理、INDEX.md conflict の扱いを確認するとき。
- apply join が許可または拒否する path 分類を変更し、realization file、oracle file、memo、AGENTS.md、.codex、tracked ignored file への影響をテストで追うとき。

## Do not read this when
- apply fork の Codex 実行や apply worktree 作成だけを確認したいとき。
- session fork、doctor、git helper、state schema など、join 以外の基盤実装を調べる必要があるとき。
- apply join の内部実装を直接変更するために、テストではなく command 本体の制御フローから読み始めるべきとき。
- 単に INDEX.md 用エントリーの形式やルーティング規則を確認したいだけのとき。

## hash
- 9e8523c640a4431026483f339cf443e7795633856526b5cf145eee2b4de11df6

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
- TUI 起動直前の CLI 前処理を外部挙動として検証するテスト。エディタで作成された依頼文の補完、パラメータ解決用 Codex exec 呼び出し、TUI 用 Codex 起動パラメータ、ログ保存先、`.cmoc/local` の無視設定を扱う。
- 通常 worktree と linked worktree の両方で、TUI プロンプト生成物や schema、sub_command ログが repository root 側の `.cmoc/local` に置かれ、linked worktree 側へ追跡対象の成果物を残さないことを確認する。

## Read this when
- `tui` サブコマンドの起動前処理、エディタ起動、依頼文の補完、パラメータ解決、Codex TUI 起動引数を変更する時。
- TUI 実行時の file access mode、structured output schema、追加 read path、prompt 文面の組み立てを確認したい時。
- `.cmoc/local/log/tui`、`.cmoc/local/log/sub_command`、`.cmoc/local/schema`、`.gitignore` への TUI 実行時副作用を変更または検証する時。
- linked worktree 上で `tui` を実行した場合の root/cwd の扱い、ログ保存先、worktree 側 `.cmoc` の ignore 挙動を確認する時。

## Do not read this when
- TUI の対話 UI 本体や表示レイアウトだけを調べる時。
- Codex 実行ラッパー全般の低レベルな実装だけを調べる時。
- `doctor`、git worktree 作成、テスト用 repository fixture の汎用挙動だけを確認したい時。
- oracle file や INDEX.md 生成規則そのものを確認したい時。

## hash
- f41e9bffe37fa782ecc1d2e1e273d4f4f7a8f1823c750e5789e707d1321808bb

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
- doctor/init がリポジトリ初期化状態、`.cmoc` の ignore/untrack、`.agents` の追跡、managed ollama の準備、既定設定の同期、Codex profile 準備時の doctor 起動を正しく行うことを検証する realization test。
- git 状態修復、設定ファイル生成・同期、managed ollama provider model の取得、既存 staged 変更の保持といった、doctor 系 CLI/前処理の外部挙動を確認する入口になる。

## Read this when
- doctor preprocess、init、`.cmoc` の git ignore/untrack、`.agents` の初期追跡、managed ollama のインストール・service・model pull に関する挙動を変更する時。
- 既定 config の追加・変更時に、人間が書いた値を上書きせず不足項目だけ同期されるかを確認したい時。
- Codex profile 準備処理が local SLM 用 provider を使う条件や、ollama service が未準備の時に doctor を走らせる制御を変更する時。
- doctor の repair commit が既存の staged 変更を巻き込まないこと、または修復後に作業ツリーを汚さないことを確認する時。

## Do not read this when
- agent call の一般的な引数モデル、file access mode、reasoning effort の仕様だけを確認したい時。
- ollama の実インストール手順や systemd service の詳細実装だけを追う時は、実装側の runtime doctor/profile preparation を直接読む方がよい。
- 設定 schema や default 値の正本定義そのものを確認したい時は、oracle 側または config 実装の定義を直接読む方がよい。

## hash
- cafc3e40ef4e2a1d33ca4ca9d4c3a5c04b6970dc0dfaae1af4745b7eb278d536

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
- review oracle コマンドの外部挙動を CLI 経由で検証するテスト。report の構成と集計、対象 oracle file の列挙、session/full scope、linked worktree、INDEX.md 差分の merge、処理失敗時 report、review worktree が許されない差分を作った場合の拒否を扱う。
- 所見 loop の制御を検証するテストを含む。enumerate が対象ごとに関連所見だけを受け取ること、challenger/advocate/judge/merge の呼び出し、merge operation の契約違反や target 再利用の拒否を確認する。

## Read this when
- review oracle の CLI 実行結果、report 文面・セクション順・集計値・終了コードを変更する。
- review oracle の対象 oracle file 列挙条件、scope の意味、tracked ignored file、AGENTS.md/INDEX.md 除外、linked worktree 上の review 対象を変更する。
- review oracle の所見 enumerate/validate/judge/merge loop、finding の採否、merge operation の検証規則を変更する。
- review oracle 実行中に生成された INDEX.md 差分の取り込み、preflight indexing 差分の扱い、index conflict 解決、非 INDEX.md 差分の拒否を変更する。
- review oracle の処理失敗時に error report を残す挙動や stdout/stderr へのエラー表示を変更する。

## Do not read this when
- review oracle 以外の review サブコマンドや通常の session 操作だけを変更する。
- oracle file の定義そのものや正本仕様文書を確認したいだけで、CLI 実装の外部挙動テストを確認する必要がない。
- INDEX.md エントリー生成や一般的な indexing の挙動だけを扱い、review oracle 実行時の差分取り込みや衝突解決に触れない。

## hash
- 539805ba7347128ae468217f6c61199958527dc5a481c5c567cd4a1429d1aee0

# `test_session_cli.py`

## Summary
- session fork/join/abandon の CLI 回帰テスト。session branch と session state のライフサイクルを中心に、linked worktree、state cleanup、dirty worktree 拒否、join 時の conflict 解消、branch 削除失敗時の外部挙動をまとめて検証する。
- session 状態ファイルの生成・更新・破損検出、home/session branch の切替、preprocess による .cmoc/.agents/.gitignore 整理、stdout/stderr へのエラー出力先など、session CLI の観測可能な挙動を扱う。

## Read this when
- session fork、session join、session abandon の外部挙動や回帰テストを確認・変更する。
- session branch と session state file のライフサイクル、既存 state との衝突、active/joined/abandoned 状態遷移を扱う。
- linked worktree 上での session 操作、home branch の検出、root worktree との branch 状態の分離を確認する。
- session join の merge conflict 解消、oracle conflict 解消用 agent 呼び出し、conflict marker 検出、delete conflict の stage 処理を変更する。
- session completion 時の cleanup、branch 削除失敗時の警告、cleanup failure 時の rollback、未コミット差分拒否、エラー出力先を検証する。

## Do not read this when
- session CLI 以外のサブコマンド挙動を調べる場合。
- session の内部 helper 単体の細部だけを確認したい場合で、対象 helper の実装ファイルまたはより小さい単体テストへ直接進める場合。
- doctor、config、runtime profile、agent call parameter の一般仕様を確認したいだけで、session join/fork/abandon の外部挙動に関係しない場合。
- oracle file の正本仕様そのものを読む必要がある場合。

## hash
- 2943eb85367151a80f9c8136874af2c73d52ff9ebc2e8e1576c8db6c2277c43c

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
