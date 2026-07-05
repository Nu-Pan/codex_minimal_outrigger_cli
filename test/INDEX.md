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
- apply abandon が active apply run を破棄する外部挙動を CLI 経由で検証する realization test。worktree・branch・session state の cleanup、running apply process と Codex child process の停止、pid file 読み取り、linked session/apply worktree からの実行位置判定、破損 state や stale apply branch の拒否条件を扱う。
- 16,000 文字を超えるが、同じ abandon 操作の成功・警告・失敗条件と state fixture を共有するため、active apply run 破棄の検証文脈を一箇所に保つテストとして位置づけられている。

## Read this when
- apply abandon の CLI 出力、終了コード、session state 更新、apply worktree 削除、apply branch 削除の挙動を確認・変更する。
- running apply abandon が親 process と記録済み Codex child process をどう停止し、pid file や lock をどう扱うかを確認・変更する。
- apply worktree 内、linked session worktree、linked apply worktree、stale apply branch など、実行位置による abandon の境界条件を確認・変更する。
- cleanup 対象が既に消えている場合の warning 成功扱いや、process identity 欠落・worktree 導出不能・dirty linked session などの拒否条件を確認する。

## Do not read this when
- apply fork の Codex 実行結果生成や findings 処理そのものを確認したい場合。
- apply abandon 以外の session fork、doctor、repo 作成 helper の基本挙動を確認したい場合。
- CLI を介さない汎用的な git worktree 操作や branch 操作の実装詳細だけを確認したい場合。
- oracle file の正本仕様そのもの、または INDEX.md エントリー生成規則を確認したい場合。

## hash
- 4acf89c60ce02aade6c08bf5801e01a9c3325bd6deffe0f3458863e1411e2a86

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
- apply run を session へ join する CLI 外部挙動を検証するテスト。apply worktree/branch の後片付け、session state 更新、join 結果 report、linked session worktree への merge、現在 cwd が apply worktree の場合の扱いを確認する。
- apply join の拒否条件と異常検出も同じ責務として扱い、stale apply branch、dirty apply worktree、想定外差分、managed branch の変更パス分類、merge conflict、INDEX.md conflict 解決後の継続を検証する。
- realization/oracle/memo/.git/.agents/.codex/INDEX/AGENTS などのパス分類に基づき、apply 側変更と session 側変更の期待可否を判定する helper の挙動も、この join 操作の境界条件として含める。

## Read this when
- apply join の CLI 挙動、成功時の cleanup、state 更新、report 出力を変更または確認したいとき。
- apply join が apply worktree 内、session worktree 内、linked session worktree 内のどこから実行されたかによって cleanup や merge 先が変わる挙動を確認したいとき。
- apply join の拒否条件、dirty worktree、stale apply branch、想定外差分、force-resolve、merge conflict の扱いを変更または確認したいとき。
- apply join で realization file と oracle/memo/.git/.agents/.codex/INDEX/AGENTS などをどう分類するか、変更パス検出 helper の期待値を確認したいとき。

## Do not read this when
- apply fork の Codex 実行や apply worktree 作成そのものを確認したいだけなら、apply fork 側のテストを読む。
- session fork の基本挙動、session branch 作成、session state 初期化を確認したいだけなら、session fork 側のテストを読む。
- join 操作を伴わない path model や oracle/realization 定義の正本仕様を確認したい場合は、oracle 側の該当文書または実装を読む。
- CLI を経由しない小さな helper 単体の実装詳細だけを追う場合は、対象 helper が定義されている apply join 実装を直接読む。

## hash
- 4ccd1a3f2a8925b1f2beb303e380699abc4ed905cfe5a2eab7c7be7ba900625e

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
- doctor/init CLI と runtime doctor 周辺の統合テスト。`.cmoc` 設定生成・ignore/untrack、`.agents` 修復コミット、managed ollama の配置・systemd user service、cmoc provider model pull、既存 staged 変更を巻き込まない修復、local SLM profile 準備時の doctor 起動を検証する。

## Read this when
- doctor preprocess、init、`.cmoc/config.json`、`.gitignore`、`.agents/.gitkeep`、managed ollama、cmoc model provider、local SLM profile 準備の外部挙動を変更する時。
- doctor が Git の tracked/ignored/staged 状態をどう修復・保持するべきかを確認したい時。
- 既定設定の同期で、人間が書いた設定値を上書きしないことを検証したい時。

## Do not read this when
- 個別の低レベル helper の単体挙動だけを確認したい時。
- doctor/init 以外の CLI コマンドや agent call 実行フローを調べる時。
- oracle 側の正本仕様や config schema の定義そのものを確認したい時。

## hash
- 0828ac0649ca7513aac6df5a6fe0a13edc3f947cd601c7821726e9aa04a3b4a7

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
- review oracle の CLI 実行と report 生成の外部挙動を検証するテスト群。対象 oracle の列挙、scope 指定、report の構成・集計、accepted/rejected 所見の表示、エラー時 report、review 用 worktree と join commit の扱いを扱う。
- 所見 loop の制御を検証するテスト群。列挙結果の次 round への渡し方、challenger/advocate/judge/merge の呼び出し、merge operation の契約、semantic merge 失敗時の retry と失敗終了を扱う。
- tracked ignored oracle file、AGENTS.md/INDEX.md 除外、memo 配下や symlink の扱いなど、oracle file 定義に基づく review 対象選択の境界を検証する。
- review 中に生成された INDEX.md 差分だけを取り込み、それ以外の作業ツリー差分を拒否する挙動を検証する。

## Read this when
- review oracle コマンドの CLI 挙動、scope オプション、report 出力、終了コードを変更または確認したいとき。
- review oracle の所見列挙・検証・judge・merge loop、所見 ID、merge operation の validation や retry 制御を変更するとき。
- oracle file の列挙条件、tracked ignored file、AGENTS.md/INDEX.md 除外、memo や symlink 境界を変更するとき。
- review 用 worktree、linked worktree、join commit、review 中の INDEX.md 更新取り込み、非 INDEX 差分拒否の挙動を変更するとき。

## Do not read this when
- review oracle 以外の review コマンドや通常の session 操作だけを確認したい場合は、対象機能に対応するテストへ進む。
- report の文字列整形ではなく INDEX.md 生成そのものの仕様や実装を確認したい場合は、indexing 側の実装・テストを読む。
- Codex 実行 wrapper や runtime preflight の一般挙動だけを確認したい場合は、その責務を持つ実装・テストを直接読む。
- oracle file の正本仕様本文を確認したい場合は、テストではなく oracle 配下の該当文書を読む。

## hash
- 6c008cf76073a00fadf64e2a936c1628f3b61f3c5f0dcd4a70e9c3eb8bcbc693

# `test_session_cli.py`

## Summary
- session fork/join/abandon の CLI 回帰テスト。session branch と session state のライフサイクルを軸に、状態ファイル作成・衝突、linked worktree、join 時の conflict 解消、branch 削除、cleanup、dirty worktree 拒否、stdout/stderr のエラー出力を検証する。

## Read this when
- session fork/join/abandon の外部挙動、終了後の branch/state 遷移、または出力内容を変更・確認する。
- session 操作で linked worktree を扱う挙動、home branch への復帰、session branch 削除可否、state cleanup の回帰を確認する。
- session join の conflict 解消 agent 呼び出し、oracle conflict 書き込み許可、conflict marker 検出、非 conflict 差分拒否を確認する。
- session 操作前後の preprocess、.cmoc/.agents の追跡状態、dirty worktree や不正 state file の拒否を確認する。

## Do not read this when
- session 以外の CLI サブコマンドや doctor 単体の挙動だけを確認する。
- session の内部 helper 実装だけを変更し、fork/join/abandon の外部挙動や branch/state ライフサイクルに影響しない。
- apply 系の状態遷移や agent call 全般を確認したいだけで、session join の conflict 解消経路を扱わない。

## hash
- fc3e96ceebf51d7fff64d10e7b20b02d59840d6b03a23aae70b2f245aa3f8591

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
