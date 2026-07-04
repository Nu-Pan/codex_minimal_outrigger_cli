# `_support.py`

## Summary
- CLI テストで共有する pytest 補助関数群。最小 Git リポジトリの作成、Codex ホームとプロファイルの差し替え、外部コマンドの偽装、doctor 実行、apply 用 worktree 解決など、テスト本体が前提環境の準備や Git 状態確認を簡潔に行うための入口になる。

## Read this when
- CLI テストで使う一時 Git リポジトリ、初期コミット、ユーザー設定、署名や hook の無効化を確認または変更したいとき。
- テスト内で Codex ホーム、認証ファイル、プロファイル生成の monkeypatch、偽の外部実行ファイルを準備する方法を確認したいとき。
- doctor コマンドのテストで偽の Ollama 実行ファイルやローカル HTTP 応答をどう用意しているか確認したいとき。
- セッション状態から apply 用 worktree のパスを解決するテスト補助を確認したいとき。

## Do not read this when
- 個別 CLI コマンドの期待出力や失敗条件そのものを確認したい場合は、該当するテスト本体を読む方がよい。
- プロダクト実装の Git 操作、Codex 実行、TUI、doctor、apply の本体仕様を確認したい場合は、対応する実装ファイルを読む方がよい。
- oracle の正本仕様やテストルールの根拠を確認したい場合は、oracle 配下の該当文書を読む方がよい。

## hash
- 99ff1a5d76b407ca101533888481a28d6e5d80b208115596b1b446c146f6d1fe

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
- apply fork CLI の統合的な挙動を検証する realization test。Codex 実行ループ後の state/worktree 更新、linked worktree 起点の branch/HEAD 利用、.gitignore の保持・編集、設定読み込み失敗時の非開始、apply 対象 path の正規化を扱う。

## Read this when
- apply fork コマンドの外部挙動、session state、apply branch、apply worktree、process pid の生成・削除条件を確認・変更したいとき。
- linked worktree から apply fork を開始した場合の oracle snapshot commit や apply branch の起点 commit を確認したいとき。
- .gitignore や .git/info/exclude と apply fork の相互作用を確認・変更したいとき。
- apply fork の scope 対象候補から root 直下 memo、管理 path、AGENTS.md、INDEX.md、ignored file、binary file をどう扱うか確認したいとき。
- Codex 実行を fake に差し替えた apply fork の制御フローや所見列挙・適用ループのテストを変更したいとき。

## Do not read this when
- apply fork の実装詳細だけを追う場合。まず apply fork 実装側を読む。
- session fork や doctor の単体挙動を確認したい場合。各コマンドの専用テストを読む。
- Codex CLI 自体の出力品質や LLM 応答内容を検証したい場合。このテストは Codex 実行結果を fake 化して制御ロジックを検証する。

## hash
- b16cce374d0bf32ea9a1d52981f55bd4e301accf569786cef20b1c0733861bd0

# `test_apply_fork_report_cli.py`

## Summary
- apply fork の CLI 経由の制御を検証する大規模な realization test。所見列挙、所見適用、commit、変更要約、report 出力、session state 更新、再検査、rolling apply fork の対象選定までを一連の apply fork report 文脈として扱う。
- apply fork 用 ACP builder の import 可能性、prompt 内容、oracle schema 参照、変更差分要約 helper の挙動も同じ apply fork report・再検査制御の入口として検証する。

## Read this when
- `apply fork` の CLI 実行結果、終了コード、作業レポート内容、所見数推移、変更内容要約、commit message、session state 更新を確認・変更する。
- apply fork が所見適用後に変更ファイルや新規ディレクトリ配下を再調査する条件、収束・未収束・error の判定、上限到達時の扱いを確認・変更する。
- apply fork report 用の変更要約が未 commit 差分、未追跡 file、削除済み tracked file をどう扱うかを確認・変更する。
- apply fork 用の change summary、file finding enumeration、finding application の ACP builder import、prompt、structured output schema path を確認・変更する。
- rolling apply fork が前回 apply join 後の oracle 変更だけを対象にする制御や、session state の join 済み apply snapshot 記録を確認・変更する。
- 所見適用が oracle など禁止領域を書いた場合に apply fork が事後修復を呼ばない挙動を確認・変更する。

## Do not read this when
- apply fork 以外のサブコマンド、または apply join・session fork 単体の通常動作だけを調べたい。
- Codex 実行 wrapper、git helper、runner fixture などの共通テスト基盤そのものを調べたい。
- apply fork の report・再検査・変更要約に関係しない ACP builder や structured output schema を調べたい。
- 実装内部の小さな helper 分割や純粋な unit-level 挙動だけを確認したく、CLI report や session state まで観測する必要がない。

## hash
- 3b79f259afd2bf81c3eeefb11c0a959cb330b8a2cfd51e70343a4dfb7101bd66

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
- cmoc の基礎 runtime 契約を横断して検証する realization test。root placeholder 解決、linked worktree と main worktree の扱い、run worktree の安全境界、config 読み込み、CmocError の Markdown 表示、CLI error の stdout report、subcommand log、FileAccessMode と Codex profile、binary 判定、session/apply branch state 解析をまとめて扱う。
- 個別サブコマンドの詳細仕様ではなく、複数機能の実行前提になる共通 runtime 挙動の回帰確認入口として位置づけられている。

## Read this when
- root/work/run/repo root の解決、root placeholder 変換、linked worktree 実行時の root 境界を確認または変更する。
- CmocError、CLI 引数解析 error、stdout/stderr の report 出力、call stack 表示、preflight 失敗時の副作用抑制を確認または変更する。
- subcommand log の作成条件、timestamp 衝突時の log file 分離、log 作成前 check の失敗挙動を確認または変更する。
- CmocConfig の既定値、config_from_dict の型検証、Codex model/reasoning effort 名の扱いを確認または変更する。
- FileAccessMode、Codex sandbox profile、追加書き込み許可 path、oracle/memo/.git/.agents/.codex などの許可境界を確認または変更する。
- session/apply branch 名から session id を得る処理や、破損 branch 名に対する state 読み込み拒否を確認または変更する。
- binary 判定、duration 表示、`.cmoc/local` ignore 追加、起動 wrapper の missing venv report など、共通 runtime の小さな契約を変更する。

## Do not read this when
- 個別サブコマンド固有の business logic、出力内容、workflow の詳細だけを確認したい場合は、そのサブコマンドの専用テストを読む。
- oracle file の正本仕様そのもの、仕様文書の編集方針、INDEX.md 生成規則を確認したい場合は oracle 側の該当文書を読む。
- 単一 helper の内部実装だけを局所的に変更し、root 境界や CLI 表示や Codex profile などの共通 runtime 契約に影響しないことが明らかな場合は、該当実装とより狭いテストを優先する。

## hash
- f0d9dd0734e7108fdd31790a870dec2ca53b23fc0a9391a6d452aeecec363b3f

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
- Codex CLI/TUI 起動まわりの realization test。Codex subprocess のプロセスグループ分離、profile 生成、sandbox writable roots、cwd、schema 出力先、local SLM provider 設定、呼び出しログ、エラー報告を、スタブした codex 実行ファイルで検証する。
- agent call 後の差分を post validation で差し戻さない方針を広く検証する。oracle、.git、.agents、.codex、memo、README、gitignore、ignored artifact、cache、venv、cmoc log、linked worktree など、各 file access mode と runtime 生成物の扱いを確認する。
- extra read path の事前許可チェック、pure oracle read の実行位置、linked worktree からの repo-local read、missing Codex CLI や非ゼロ終了時の CmocError と console report も扱う。

## Read this when
- Codex CLI の exec/tui 呼び出し引数、profile TOML、CODEX_HOME、sandbox 設定、cwd、prompt stdin、output schema の保存場所に関する挙動を変更・確認したいとき。
- FileAccessMode と Codex 呼び出し後の差分検査の関係、特に forbidden path や runtime/cache/log/ignored file の差分を許容する挙動を変更・確認したいとき。
- run_codex_subprocess、run_tracked_codex_subprocess、run_codex_exec、run_codex_tui の失敗時挙動、process tracking、schema retry、linked worktree 対応を調べるとき。

## Do not read this when
- agent call parameter の enum や値オブジェクト自体の定義だけを確認したいときは、basic 側の実装またはそのテストを直接読む。
- Codex 以外の runtime、repository 作成 helper、git helper、test support utility の詳細を調べたいだけなら、それぞれの support 実装・テストを読む。
- oracle/realization の概念定義や file access mode の正本仕様を確認したい場合は、oracle doc/src の該当箇所を読む。

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

# `test_doctor_cli.py`

## Summary
- doctor/preprocess 系のテスト。git 管理状態の修復、`.gitignore`・`.agents`・既定設定の同期、repo-local Ollama の起動、既存 staged 変更を修復 commit に混ぜないこと、local SLM 用 Codex profile 作成時の doctor 自動実行を外部挙動として検証する。

## Read this when
- doctor コマンドまたは preprocess が repo 初期化・修復時に作るファイル、commit 対象、git index の扱いを変更する。
- `.cmoc/config.json` の既定値同期で、人間が設定済みの値を保持しつつ不足キーを補う挙動を確認・変更する。
- repo-local Ollama の port ファイル生成、起動確認、local SLM profile 生成との連携を変更する。
- doctor 実行時に既存の staged 変更を保持し、修復 commit に含めない制御を確認する。

## Do not read this when
- 個別コマンドの CLI 引数解析だけを確認したい場合。doctor 実行後のリポジトリ副作用に関係しないなら、より直接の CLI テストまたは実装を読む。
- Codex profile の一般的な TOML 生成だけを確認したい場合。doctor 自動実行や local Ollama port の補修に関係しないなら、profile 生成側のテストを読む。
- 設定 schema や既定値そのものの一覧を確認したい場合。この対象は設定値定義ではなく、doctor による同期結果を検証する。

## hash
- 273857ad2dd5617707946057ab037f37005bb2f2968d4c137d2ec8298d64d990

# `test_indexing_cli.py`

## Summary
- INDEX.md 生成・更新、indexing preflight、indexing サブコマンド、INDEX.md conflict 解決の外部挙動を検証する回帰テスト。対象列挙、hash 再利用、Codex 生成、commit 対象、dirty worktree 拒否、linked worktree、空ディレクトリ、memo 除外、symlink cycle 除外を同じ routing 更新ワークフローとして扱う。

## Read this when
- indexing CLI または indexing preflight の成功・失敗条件、commit 条件、git worktree 上での対象 root 判定を変更する時。
- INDEX.md エントリーの schema 検証、fresh hash による Codex 呼び出し省略、malformed entry の再生成、空ディレクトリ用 INDEX.md 生成を確認する時。
- routing document 更新対象の列挙順、並列生成境界、root 直下 memo 除外、入れ子の memo 扱い、directory symlink cycle 除外を変更する時。
- apply join 側の INDEX.md merge conflict 解決が、INDEX.md を削除して未解決 conflict を消し commit する挙動を確認する時。

## Do not read this when
- INDEX.md 生成の実装詳細や helper の責務を調べたいだけなら、対応する実装モジュールを読む。
- doctor 初期化、runtime config、AgentCallParameter の一般仕様を調べたいだけなら、それぞれの直接の実装またはテストを読む。
- 個別の routing 文書本文や INDEX.md エントリー文言の品質を確認したいだけなら、対象の oracle doc または生成対象ファイルを読む。

## hash
- 5b7f371d8e42cbb5a70e45d110a8ff125ef5f24ed6bc5f034bef8f91e31903cd

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
- session fork、join、abandon の CLI 外部挙動を、session branch と session state のライフサイクルとしてまとめて検証するテスト。
- linked worktree 上での session 操作、state cleanup、dirty worktree 拒否、join 時の conflict 解消、branch 削除失敗時の警告、エラー出力先を扱う。
- ファイルサイズは大きいが、同じ session 状態遷移と branch/state fixture を共有する回帰テストとして一箇所に集約されている。

## Read this when
- session fork、join、abandon の CLI 挙動や出力、終了コード、branch/state 更新を変更する。
- session state file の生成、破損検出、cleanup rollback、abandoned/joined 状態への遷移を確認する。
- linked worktree 上の session branch 切替、home branch 復帰、session branch 削除可否に関わる挙動を確認する。
- session join の conflict 解消 agent 呼び出し、oracle conflict 書き込み許可、conflict marker 検出、解消後差分の検証を変更する。
- session join/abandon のエラーや完了レポートを stdout/stderr のどちらへ出すかを確認する。

## Do not read this when
- session 以外のサブコマンドや、CLI 共通 runner だけを確認したい。
- session の内部 helper 単体の詳細だけを確認したく、外部 CLI 挙動や branch/state ライフサイクルを見ない。
- oracle file や realization standard の正本仕様そのものを確認したい。
- git repository 作成 fixture、doctor 実行 fixture、共通テスト補助関数の実装だけを確認したい。

## hash
- df0edf9c3c229987726368914b584a046dd01461b7c4e5bd40c3ce6e9ce0f6e7

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
