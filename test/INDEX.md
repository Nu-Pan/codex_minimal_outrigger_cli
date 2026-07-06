# `_support.py`

## Summary
- CLI・runtime 周辺のテストで共有する最小 Git リポジトリ、Codex home、fake Codex profile、fake managed Ollama/systemctl、Typer runner 実行、apply worktree 解決の補助をまとめるテスト支援モジュール。
- 外部コマンドやローカルサービスを実際の利用環境から切り離し、テストごとに一時領域内で再現可能な git 状態・認証状態・Ollama 管理状態を作る入口になる。

## Read this when
- CLI テストで使う一時 Git リポジトリ、初期 commit、tracked ignored oracle file、現在 branch の確認を用意したいとき。
- Codex 実行 wrapper や TUI 実行 wrapper のテストで、認証済み home、既定の agent call parameter、profile 生成の差し替えが必要なとき。
- doctor や profile 作成経路のテストで、実 systemctl や実 Ollama に依存しない fake managed Ollama 環境を使いたいとき。
- テスト用の Python 実行ファイルを生成したいとき、または session state から apply worktree path を解決する補助が必要なとき。

## Do not read this when
- 個別サブコマンドの期待出力や業務ロジックそのものを確認したいだけなら、該当するテスト本文または実装を直接読む。
- oracle file、realization file、path keyword などの仕様上の定義を確認したいだけなら、正本仕様側の該当文書を読む。
- fake 外部コマンドではなく本番の Codex profile 生成、Ollama 管理、runtime apply 実装の詳細を変更する作業では、対応する実装モジュールを直接読む。

## hash
- 7125b09c0a993a5f31e0499ba8bcf7a36ed3648abbadef5fb12b442bc62a088d

# `test_acp_builder_parameters.py`

## Summary
- ACP builder が生成する AgentCallParameter のモデル種別、reasoning effort、file access mode、preflight 設定、prompt 埋め込み、structured output schema 参照、互換 module の公開名を検証する realization test。
- apply fork、TUI resolve parameter、indexing index entry、review oracle、session join conflict resolution の builder 群について、oracle src の schema や builder と realization 側の出力が一致するかを確認する。

## Read this when
- ACP builder の parameter 生成ロジック、prompt 内容、schema path、schema 内容、公開 API を変更する。
- apply fork、TUI resolve parameter、indexing index entry、review oracle、session join conflict resolution の builder 実装や compatibility module を変更した後、既存挙動の期待値を確認する。
- oracle src の structured output schema を realization 側 builder が正しく参照しているかを調べる。
- builder が使う `<repo-root>`、`<work-root>`、`<oracle-root>` の prompt 表記や動的文字列の保持を検証したい。

## Do not read this when
- ACP builder 以外の CLI 実行、永続状態、path model、index 生成本文などを調べたい場合。
- structured output schema の正本内容そのものを確認したい場合は、対応する oracle src の schema を直接読む。
- 個別 builder の実装方針を調べたい場合は、対象 builder の realization implementation を直接読む。

## hash
- 9af27731ac237fd99af478859368c13a57b4401a0f1e8e7000593bb7ab644450

# `test_apply_abandon_cli.py`

## Summary
- apply abandon が active apply run を破棄する CLI 外部挙動を検証するテスト。worktree・branch・session state の cleanup、missing target の warning、running process と child process group の停止、pid reuse・race・lock 待ち、実行位置や linked worktree 境界での拒否条件を扱う。

## Read this when
- apply abandon の成功時に apply worktree、apply branch、session state、process id file がどう cleanup されるかを確認・変更する。
- running apply process の停止順序、child process group の扱い、pidfd・start time・PID reuse・終了 race・tracking lock 待ちに関する挙動を確認・変更する。
- apply abandon を session worktree、apply worktree、linked session worktree、linked apply worktree、stale apply branch から実行したときの受理・拒否条件を確認・変更する。
- 破損した apply_branch、別 session の apply branch、running state で process identity が無い場合など、cleanup 前に拒否すべき条件を確認・変更する。

## Do not read this when
- apply abandon 以外の apply subcommand の通常処理や Codex 実行内容を確認したいだけの場合。
- session fork、doctor、git helper、state schema などの共通基盤そのものを確認・変更する場合。
- process 停止処理の CLI 経由の abandon 境界ではなく、低レベル runtime helper の単体仕様だけを確認したい場合。

## hash
- 7114d6da5666657a42c2c9868ff913eabf66c3840903a71e638ceeb6c14e865a

# `test_apply_fork_cli.py`

## Summary
- apply fork CLI の回帰テスト。Codex ループ実行、apply state と worktree 更新、linked worktree 起点の branch/HEAD、doctor preprocess、設定読み込み失敗時の未開始保証、`.gitignore` 編集、target normalization、report 前の completed state 書き込みを、共有 fixture 上の外部挙動として検証する。
- target normalization では root 直下の管理領域や `memo`、未追跡 ignored file の除外、tracked ignored file や binary file、repository path 基準の symlink 分類など、apply fork の対象選別境界を確認する。

## Read this when
- apply fork CLI の外部挙動、apply run の状態遷移、apply branch/worktree 作成規則、Codex 呼び出しループ、report 生成前後の state 更新を変更・確認する場合。
- apply fork 実行前の doctor preprocess、`.cmoc/local` の ignore 確保、`.gitignore` を対象 file として扱う挙動を変更・確認する場合。
- apply fork の scope 対象列挙、realization/oracle/memo/管理 path/git ignored file/symlink/binary file の target normalization を変更・確認する場合。
- 設定ファイルの missing/invalid 時に apply run を開始しない失敗挙動を変更・確認する場合。

## Do not read this when
- apply fork 以外の subcommand の基本 CLI 挙動だけを確認する場合。
- Codex 実行 wrapper、doctor、session fork、report writer などの単体実装を調べたいだけで、apply fork 境界から観測される統合挙動が不要な場合。
- target normalization の仕様ではなく、個別ファイルの分類語や path model の正本仕様を確認したい場合は oracle 側の該当文書を先に読む。

## hash
- 155dca26d71fdfc0a053ba3d151d36ee77792904a577cec6ef9c1f6566e9ec44

# `test_apply_fork_report_cli.py`

## Summary
- apply fork を CLI から実行したときの所見列挙、適用、commit、変更要約、report 生成、session state 更新までの制御を検証する realization test。
- 変更ファイルの再調査、収束・未収束・error report、未追跡 file や削除済み file の変更要約、rolling apply fork の対象選択を同じ report schema と loop 制御の観測として扱う。
- apply fork 用 ACP builder が packaged layout や src のみの PYTHONPATH で import でき、標準 prompt と oracle schema を参照できることも検証する。

## Read this when
- apply fork の CLI 実行結果、終了 code、report 内容、変更要約、commit message、session state 更新を変更または調査するとき。
- apply fork が適用後の変更 file や新規 directory 配下を再調査する loop、回数上限での収束判定、未差分適用時の未収束扱いを確認するとき。
- apply fork の error report が未 commit 差分を要約する挙動、未追跡 file を差分に含める挙動、削除済み tracked file を要約対象から外す挙動を扱うとき。
- rolling apply fork が前回 apply join 後の oracle 変更だけを対象にする制御を変更または確認するとき。
- apply fork の所見列挙・所見適用・変更要約 builder の import、prompt、structured output schema path を調査するとき。

## Do not read this when
- apply fork 以外の CLI command、session fork/join 単体、doctor、設定 load などを調査しており、apply fork の report や再検査制御に触れないとき。
- report rendering の細部だけを局所的に確認したい場合で、対象 module の単体実装またはより小さい report helper test を直接読む方が十分なとき。
- ACP builder 全般の共通仕様や oracle prompt 断片そのものを調査しており、apply fork 専用 builder の CLI 経由検証が不要なとき。

## hash
- 1619b1eb112c0ee77a38e6d8bad7239186617d0e432ec91971d10f7096d23f0f

# `test_apply_join_cli.py`

## Summary
- apply run を session へ join する CLI 外部挙動を検証する realization test。join 成功時の worktree/branch cleanup、state 更新、report 生成と、dirty worktree、想定外差分、merge conflict、force resolve、linked session worktree などの拒否・回復条件を一箇所で扱う。
- 責務は apply join の可否判断と後片付けの統合的な挙動確認に閉じており、fixture と git 状態の読み取り文脈を共有する境界条件群への入口になる。

## Read this when
- apply join の CLI 挙動、終了コード、標準出力、report 生成、state 更新、apply worktree/branch cleanup を変更または確認したいとき。
- apply join が apply worktree 内、session worktree 内、linked session worktree 内のどこから実行された場合に何へ merge するかを確認したいとき。
- dirty apply worktree、stale apply branch、想定外差分、tracked ignored path、rename/delete、root memo、oracle/AGENTS、.codex、INDEX conflict、未解決 merge conflict の扱いを確認したいとき。
- apply join の force resolve が session/apply 側の想定外変更をどう戻すか、また cleanup 可能性に応じて worktree と branch を残すか削除するかを確認したいとき。

## Do not read this when
- apply fork の Codex 実行、prompt 生成、apply worktree 作成そのものを確認したいだけのとき。
- session fork や doctor の基本動作を確認したいだけで、apply join への接続条件を扱わないとき。
- 内部 helper の単体的な path 判定だけを調べたい場合で、CLI 経由の join 全体挙動や git 状態の fixture が不要なとき。
- oracle file や realization file の一般定義、INDEX エントリー規約、ファイルアクセス規則を確認したいとき。

## hash
- ad667629064f5a56d12c809d6c0c4a998829eadf38332d7dfbeff6f07b271f0b

# `test_basic_runtime.py`

## Summary
- cmoc の基礎 runtime 契約を横断的に検証する realization test。root placeholder 解決、repo/run/work root の扱い、config 変換・検証、CmocError の表示、CLI wrapper の preflight と error report、subcommand log、session state、FileAccessMode から Codex profile への変換、binary 判定、managed worktree 操作の安全性を、共通 fixture と root 状態を共有する回帰テストとして扱う。
- 個別サブコマンドの仕様確認より下層にある、実行前提・sandbox/profile・root 解決・状態読み書きの共通 runtime 挙動を変更するときの入口になる。

## Read this when
- root placeholder、repo root、run root、work root、linked worktree の解決挙動を変更・調査する。
- CmocConfig の既定値、JSON 変換順、config 読み込み失敗、config_from_dict の型検証を変更・調査する。
- CmocError、render_error、CLI parse error、stdout/stderr の error report、doctor preprocess、pre-log check、subcommand log の挙動を変更・調査する。
- session/apply branch 名から session id を読む処理、SessionState の dict 変換・検証、branch に対応する state 読み込みを変更・調査する。
- FileAccessMode、Codex sandbox mode、Codex cwd、build_codex_profile の読み書き許可 root、extra writable/read root、ignored gap write、oracle conflict write の制御を変更・調査する。
- `.cmoc/local` の gitignore 追加、run worktree 作成・削除の安全性、起動 wrapper の missing venv call stack 表示、binary 判定の runtime 補助挙動を変更・調査する。

## Do not read this when
- apply、review、doctor、indexing など個別サブコマンド固有の業務仕様や出力仕様だけを確認したい場合。
- oracle doc や oracle src の正本仕様断片そのものを確認したい場合。
- 単一 helper の内部実装だけを読む方が直接的で、共通 runtime 契約の回帰観点を確認する必要がない場合。
- LLM 出力品質、prompt 文面、生成される自然言語の妥当性そのものを検証したい場合。

## hash
- 596ed13adbfb8a0ed592f47e47ea23ba62f5eccffa503cf07c293bc5add29d6b

# `test_cli_tui.py`

## Summary
- TUI サブコマンド起動直前の CLI 前処理を検証する realization test。エディタで作成した依頼文の整形、Codex パラメータ解決、TUI 起動用パラメータ、ログ保存先、`.cmoc/local` の ignore、linked worktree での root/cwd/schema/log の扱いを外部挙動として確認する。

## Read this when
- TUI サブコマンドの起動前処理、依頼文編集、完了プロンプト生成、Codex exec/TUI 呼び出しパラメータを変更する時。
- TUI の file access mode 解決、空値時の既定値、structured output schema の選択を確認する時。
- linked worktree 上で TUI を実行した場合のログ保存先、schema 生成先、root/cwd 引き渡し、`.cmoc/local` の git ignore 挙動を変更または調査する時。

## Do not read this when
- TUI 内部画面の操作や表示だけを確認したい時。
- Codex 実行共通処理、doctor、git helper、設定読み込みなど、TUI 起動前処理以外の単体挙動を直接確認したい時。
- oracle file の正本仕様断片そのものを確認したい時。

## hash
- 672610acbfc3598b14ed3f8a5dc6cd622a6f7e51ef01a8bff7d37719c56fd3e3

# `test_codex_runtime_errors.py`

## Summary
- Codex CLI 実行経路で外部 `codex` コマンドが見つからない場合のエラー変換を検証する realization test。exec 実行と TUI 実行の両方で、低レベルの `FileNotFoundError` ではなく利用者向けの `CmocError` が報告されることを確認する。

## Read this when
- Codex CLI 不在時の失敗挙動、例外メッセージ、または `CmocError` への変換を変更・確認したいとき。
- `run_codex_exec` または `run_codex_tui` の外部コマンド起動エラー処理を変更した後に、対応するテスト観点を確認したいとき。
- テスト用リポジトリ、Codex home、Codex profile の stub を使った Codex runtime 系テストの最小例を確認したいとき。

## Do not read this when
- Codex CLI が存在する通常実行時の標準出力、セッション状態、または成功時の挙動を確認したいとき。
- Codex runtime 以外の CLI サブコマンド、設定読み込み、または path model の仕様を調べたいとき。
- 外部コマンド不在ではなく、Codex CLI の終了コード、stderr、タイムアウトなど別種の実行失敗を調べたいとき。

## hash
- 2454f19fb74101e9efac6c84c115ffd723173aba2ff033a65a1ab5185c82ade7

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 実行ラッパーとプロファイル生成の統合挙動を検証するテスト群。実 Codex CLI と cmoc managed ollama を使う任意実行系、偽 Codex 実行による argv・cwd・stdin・出力・call log・schema 配置・sandbox/profile 設定の確認を扱う。
- file access mode ごとの Codex profile 差分、linked worktree 実行時の作業ディレクトリと repo-local 状態保存、`.agents` を writable roots に含めない制約など、Codex 起動境界の外部挙動を確認する入口となる。

## Read this when
- Codex CLI を起動する処理、`run_codex_exec` の引数構築、stdin/prompt/output/call log/schema path の扱いを変更する。
- `prepare_codex_profile` や Codex profile TOML の生成内容、sandbox mode、writable roots、cmoc permissions、model provider 設定を変更する。
- cmoc managed ollama provider、doctor preprocess による managed service 起動、ローカル SLM 用 profile の扱いを確認・変更する。
- linked worktree 上での Codex 実行、`root` と `cwd` の使い分け、repo-local な `.cmoc/local` 配下への状態保存を変更する。
- Codex 実行時に `.agents`、`oracle`、`src`、`test`、`.gitignore` などへ許可する読み書き範囲を見直す。

## Do not read this when
- Codex 実行ラッパーではなく、一般的な設定 dataclass や oracle 上の model 定義そのものだけを確認したい。
- Codex CLI を起動しない純粋な path helper、git helper、テスト用 fixture 作成 helper の詳細だけを変更する。
- LLM の回答品質や prompt 内容の良し悪しを検証したい。ここでは cmoc が管理する実行成果物と起動条件だけを検証している。
- systemd や ollama service の単体仕様だけを確認したい。managed ollama の実サービス連携は扱うが、主対象は Codex runtime 統合である。

## hash
- d34683f2f7ead282de279202d4a6ecf13964de43505f930cac0d893c60acc92a

# `test_codex_runtime_home.py`

## Summary
- Codex CLI 実行時の Codex home 解決と事前検証を扱うテスト。`CODEX_HOME` 未設定時の既定 home、相対 `CODEX_HOME` の扱い、profile 配置、call log への記録、存在しない home・ファイルの home・認証情報欠落時の `CmocError` を検証する。

## Read this when
- `run_codex_exec` が Codex CLI に渡す `CODEX_HOME`、profile、作業ディレクトリ、call log の挙動を変更・確認したいとき。
- Codex home の存在確認、ディレクトリ確認、`auth.json` 確認、またはそれらのエラー文言を変更・確認したいとき。
- 相対パスの `CODEX_HOME` をどの基準ディレクトリで解決するかを確認したいとき。

## Do not read this when
- Codex CLI 実行の入出力イベント処理、capacity 待機、プロンプト内容など、Codex home 以外の実行制御を確認したいとき。
- リポジトリ作成や fake executable 作成など、テスト用 helper 自体の実装を確認したいとき。
- 設定値全般の schema や `CmocConfig` の定義を確認したいとき。

## hash
- a989ab21405d6144d79e829669f55418ae4b97c687add6f570fa9d2d518956f9

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex quota exceeded 後の retry 状態機械を、外部の fake Codex 呼び出しを通じて検証するテスト。quota probe、resume token、再実行、call log、subcommand log、CODEX_HOME と cwd の扱い、並列時の代表 probe 共有を一箇所で扱う。

## Read this when
- Codex exec が quota exceeded になった後の probe、resume、rerun の挙動を変更・確認する場合。
- quota availability probe の AgentCallParameter、prompt、profile、ログ出力、失敗時エラー処理を変更・確認する場合。
- quota 待機中の複数 run_codex_exec 呼び出しで代表 probe を共有する並列制御を変更・確認する場合。
- Codex 呼び出しログ、subcommand log、stdout/output jsonl、prompt log、resume token 抽出の連携を確認する場合。
- 相対 CODEX_HOME や Codex 実行 cwd が quota retry 中にどう引き継がれるかを確認する場合。

## Do not read this when
- quota exceeded 後の retry 制御に関係しない通常の Codex exec 成功・失敗だけを確認する場合。
- quota probe のプロンプト生成だけを確認したい場合は、probe builder の実装やより小さい単体テストを先に読む。
- runtime quota retry とは無関係な CLI サブコマンド、設定読み込み、ファイルアクセス制御のテストを探している場合。

## hash
- a1b99690a95c5ed756951036f32ab4b31331b309e6ebc045b1c113a2954a1262

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 呼び出しの再試行制御を検証する realization test。構造化出力の schema 不一致、出力 JSON の欠落・空・不正、capacity エラー時の再試行、再試行時の call log と subcommand log、stdout JSONL 外のエラーマーカーを再試行条件にしない境界を扱う。

## Read this when
- Codex CLI 呼び出しの再試行条件、再試行回数、成功時に返す構造化出力の扱いを変更する。
- Codex CLI 呼び出しの call log、prompt log、stdout log、subcommand log の記録内容や生成タイミングを変更する。
- capacity エラー、quota エラー、構造化出力 parse/schema validation failure の判定境界を変更する。
- 再試行前後で agent が作成した差分や作業ツリー上の副作用をどう扱うかを確認する。

## Do not read this when
- Codex CLI の通常成功時の引数組み立てやモデル選択だけを確認したい。
- repository fixture、Codex home fixture、fake executable 作成 helper の実装だけを確認したい。
- oracle file や realization file の定義、パスモデル、INDEX.md 生成規則を確認したい。

## hash
- 33d854def2987dfa425870a934c76ea911013b1b950f23d004a780489932439c

# `test_codex_runtime_subprocess.py`

## Summary
- Codex subprocess 起動 helper のテスト。追跡付き起動が子プロセスを専用 process group で実行し、一時的な apply process tracking 情報を親の tracking file に残さないことを検証する。通常起動が継承された apply tracking 環境変数を無視し、外部 tracking file を作らないことも確認する。

## Read this when
- Codex subprocess 起動 helper の process group 分離や apply process tracking の扱いを変更する時。
- run_codex_subprocess と run_tracked_codex_subprocess の外部挙動、環境変数の継承抑制、一時 tracking file 更新の期待値を確認したい時。
- Codex 実行用 subprocess wrapper のテスト失敗を調査する時。

## Do not read this when
- Codex subprocess wrapper の実装ではなく、CLI コマンド引数や出力 schema の仕様を確認したい時。
- 一般的なテスト補助関数や Python executable fixture の使い方だけを調べたい時。
- apply process tracking と無関係な runtime 設定、path model、oracle/realization 境界を確認したい時。

## hash
- d9f96358767fbb5d265ebd4e8c302ad0f070f1e1765812f32ce388205dabba8d

# `test_codex_runtime_tui.py`

## Summary
- Codex TUI 実行ラッパーの realization test。起動前の追加読み取りパス検査、pure oracle read 時の complete prompt 取り扱い、linked worktree からの prompt 読み取り、呼び出しログとサブコマンドログ、Codex CLI/TUI の非ゼロ終了時エラーを外部挙動として検証する。

## Read this when
- Codex TUI 呼び出し時のアクセス許可、追加読み取りパス、complete prompt、linked worktree の cwd と profile 権限に関する挙動を確認・変更する時。
- Codex CLI/TUI 呼び出しの成功・失敗ログ、標準出力への呼び出し結果表示、call log と subcommand logger の記録内容を確認・変更する時。
- Codex TUI 実行ラッパーの回帰テストを追加・整理し、外部 codex 実行を stub して argv、cwd、profile、ログを検証したい時。

## Do not read this when
- Codex TUI ではなく Codex API 実行、agent call、または他サブコマンドの runtime 挙動だけを扱う時。
- 実装本体の制御フローや profile 生成ロジックを確認したい時は、対応する runtime 実装や設定生成側を読む。
- oracle file の正本仕様断片を確認したい時は、oracle 配下の該当文書・実装を読む。

## hash
- 2cb7a8f0578f3726c1d5dfd18207da0e71ef2640c4c819187dac2993b3d0dcb8

# `test_doctor_cli.py`

## Summary
- doctor 系 CLI の pytest 群。doctor 前処理が git 状態を修復し、管理対象 ollama を準備し、既定設定を生成・同期し、linked worktree では対象 worktree と repo 側 config を正しく扱うことを外部挙動で検証する。
- gitignore、.agents、.cmoc/local の追跡解除、config commit、既存 staged/unstaged 変更や rename の保持など、doctor が利用者の git index を壊さないことを確認する入口。
- cmoc provider model の重複排除 pull、doctor の別名コマンド、設定値の非上書き同期を含む、doctor CLI と preprocess の回帰テストをまとめて扱う。

## Read this when
- doctor コマンド、doctor preprocess、または dector alias の挙動を変更・調査するとき。
- doctor が生成・同期する config、管理対象 ollama の準備、cmoc provider model の pull 対象選定を確認するとき。
- doctor 実行時の git 修復 commit、.cmoc/local の ignore/untrack、.agents の tracking、既存 staged/unstaged 変更の保持を検証するとき。
- linked worktree 上で doctor がどの root に修復・config 生成を行うべきかを確認するとき。

## Do not read this when
- doctor 以外のサブコマンドや agent orchestration の仕様・実装だけを調べるとき。
- config schema や model spec の定義そのものを確認したいときは、対応する設定定義や oracle src を直接読む。
- ollama の install、service、model pull の内部実装だけを調べたいときは、runtime 側の実装を直接読む。
- テスト支援 fixture、repo 作成 helper、CLI runner helper の詳細だけを確認したいときは、支援コードを直接読む。

## hash
- 7f6486133c85c23dba3e28afac19f5ce0f7b338685ca85bbbb5209f84b57bf8e

# `test_indexing_cli.py`

## Summary
- indexing の preflight と subcommand が routing document を更新する CLI 境界を検証する回帰テスト。
- 対象列挙、hash 再利用、Codex によるエントリー生成、commit 対象、linked worktree、dirty worktree 拒否、conflict 解決、空ディレクトリ、memo 除外、symlink cycle 回避など、INDEX.md 更新ワークフローの外部挙動をまとめて扱う。

## Read this when
- indexing 実行時の INDEX.md 生成・更新・commit 条件を変更または調査するとき。
- indexing preflight と通常の indexing subcommand の dirty worktree 判定、repo config 参照、linked worktree での動作差を確認するとき。
- INDEX.md エントリーの schema 検証、fresh hash による Codex 呼び出し省略、malformed entry の再生成、render 順序や並列生成の挙動を変更するとき。
- apply 側の INDEX.md conflict 解決が index を削除して merge commit を完了する挙動を調査するとき。

## Do not read this when
- routing document 更新ではなく、通常の agent call 実行、prompt 構築、設定ファイルの型定義だけを調べたいとき。
- 個別の helper 実装の内部構造だけを確認したい場合で、外部 CLI 挙動や git 状態の回帰を確認する必要がないとき。
- INDEX.md エントリー本文の望ましい自然言語表現だけを確認したいとき。

## hash
- fcd714cf26d0fea5a9b0291ed05130022e89fc81caee999060eaa8665a1418b4

# `test_indexing_preflight.py`

## Summary
- Codex 実行前に行う index 更新 preflight の realization test。exec/TUI 呼び出しで index 更新が先に実行され commit されること、cwd が別 worktree 内の場合はその worktree を対象にすること、repository lock 待機、parameter による preflight 無効化、file access violation 後に recovery 用の追加 index 更新を走らせないことを検証する。

## Read this when
- Codex 呼び出し前の indexing preflight の実行条件・順序・commit 挙動を変更または確認したいとき。
- root と cwd が異なる worktree を指す場合に、どの worktree の INDEX 更新を行うべきかを確認したいとき。
- indexing lock の待機挙動や、preflight 無効化フラグの効き方を変更または確認したいとき。
- file access violation や recovery 処理と indexing preflight の相互作用を確認したいとき。

## Do not read this when
- INDEX 更新内容そのもの、エントリー生成ロジック、対象ファイル探索の詳細を確認したいときは、indexing 実装やその専用テストを読む。
- Codex subprocess/TUI 実行自体の引数組み立てや出力解析を確認したいだけで、preflight との順序や抑止条件に関心がないとき。
- agent call parameter の enum や config の定義だけを確認したいときは、それぞれの定義元を読む。

## hash
- 53add1f54659fea880475e18a941754e100865991782abe1acb7cc4bc800827d

# `test_packaged_import.py`

## Summary
- インストール後に近い配置へ必要なパッケージだけを複写し、通常の作業ディレクトリ外から import できることを検証するテスト。
- 設定上の package 配置、review oracle 用 builder の prompt/schema 参照、basic builder の canonical 定義への再公開、設定定義の再公開境界を確認する。

## Read this when
- packaged layout からの import 失敗、package-dir や package discovery 設定、oracle src を含む配布配置の問題を調査するとき。
- review oracle enumerate builder が配布相当の import 環境で prompt や structured output schema を参照できるか確認するとき。
- basic builder や設定定義の再公開境界を変更し、canonical な oracle src 定義との関係や公開名の範囲を検証するとき。

## Do not read this when
- 通常の開発ツリー上での単体 import や関数内部ロジックだけを確認したいとき。
- CLI の実行フロー、永続状態、agent call orchestration の挙動を調べたいとき。
- prompt 本文、schema 本体、設定 dataclass の詳細仕様そのものを読む必要があるとき。

## hash
- ed59fc9ad74514656ac722e4f60386946e3868ea9284ecd7656a4bc61d4d6131

# `test_prompt_parts.py`

## Summary
- 標準 prompt parts と complete prompt の Markdown 組み立て結果を検証する realization test。各標準文書 builder が期待する核となる語句・タイトルを描画すること、complete prompt が指定された標準群・file access rule・root placeholder 情報を含めるまたは省くことを外部挙動として確認する。
- prompt builder の標準文書出力、file access mode ごとの read/write rule、review/apply review/index entry/realization/routing standard の注入制御、root token と `<work-root>` placeholder の保持に関する変更時の入口になる。

## Read this when
- 標準 prompt part の文面、タイトル、または render 結果に含まれるべき主要語句を変更する。
- complete prompt が標準文書を含める条件、既定で省く条件、または routing rule を常に含める挙動を変更する。
- file access mode ごとの禁止・許可ルール文面や mode とタイトルの対応を変更する。
- `<repo-root>`、`<work-root>`、`<cmoc-root>`、`<run-root>` などの root token を prompt 内で保持・記録する挙動を変更する。
- index entry standard や review oracle standard など、動的に注入される標準 prompt の回帰をテストで確認したい。

## Do not read this when
- prompt builder の実装責務や標準文書の正本内容そのものを確認したい場合は、対応する実装または oracle 側の標準定義を直接読む。
- CLI コマンド、永続状態、ファイル探索、agent 実行制御など prompt 組み立て以外の挙動を調べている。
- StructDoc や Markdown renderer の汎用仕様を確認したいだけで、complete prompt や標準 prompt parts の期待出力に関心がない。

## hash
- a61448d13fe6b11acc398a8f268160b43e11b800fb149526e056ef20a992fdad

# `test_review_oracle_cli.py`

## Summary
- review oracle の CLI 外部挙動を検証する realization test。report 生成、対象 oracle file の列挙、所見の列挙・検証・judge・merge、accepted/rejected findings の表示、エラー report、review worktree と join commit の扱いをまとめて扱う。
- eval-oracle から review oracle 実装への委譲、oracle path placeholder 解決、tracked ignored oracle file や symlink の対象判定、session/full scope の差分対象、INDEX.md 変更の取り込みと非 INDEX 差分の拒否も検証する。

## Read this when
- `review oracle` CLI の report 出力、終了結果、出力セクション、件数集計、accepted/rejected findings の扱いを変更・調査するとき。
- oracle review の対象列挙で、full/session scope、tracked ignored file、symlink、AGENTS.md/INDEX.md 除外、review fork commit 基準の差分を確認するとき。
- 所見評価 loop の enumerate、validate challenger/advocate、judge、merge operation、semantic retry、関連 findings の prompt 引き継ぎを変更するとき。
- review 実行用 worktree、linked worktree、INDEX.md の preflight/update/merge、join commit、review が作った差分の許容範囲を扱うとき。
- `eval-oracle` コマンド、`finding_oracle_path`、`apply_finding_merge_operations`、`resolve_review_index_conflicts` の外部挙動を確認するとき。

## Do not read this when
- oracle review の prompt 文面や Structured Output schema そのものを確認したいだけなら、該当する prompt/schema 側を読む。
- review oracle 以外の review サブコマンド、または oracle file 定義に関係しない一般的な CLI 挙動を調べるとき。
- 個別 helper の内部実装だけを変更し、CLI report・対象列挙・所見 loop・worktree 差分制御に影響しないことが明確なとき。

## hash
- a88ec99ac1df6a28f45b570c88f3c7f44a6a178c65d45e0a973fd8b7fd119678

# `test_runtime_ollama.py`

## Summary
- Ollama ランタイムのサービス検証とモデル準備処理に対する realization test。systemd 上のサービス PID、待受プロセス、HTTP 応答、モデル store 準備後の show/pull/load の制御を、外部プロセスや実 Ollama に依存せず monkeypatch で検証する。

## Read this when
- Ollama サービス起動後の検証条件、特に main PID 欠落、非 2xx HTTP 応答、待受プロセスの照合失敗時のエラー挙動を変更する。
- Ollama の待受プロセスが期待するサービスプロセスまたはその子孫であることを確認する制御を変更する。
- Ollama モデルの存在確認、pull、load の呼び出し順や、モデル store 準備後に load する挙動を変更する。

## Do not read this when
- Ollama ランタイム以外のサービス検証、モデル管理、CLI 表示、設定処理だけを確認する。
- 実 Ollama バイナリやネットワークを使った結合テスト、インストール処理、永続状態のファイル内容を確認したい。
- テスト対象の実装詳細ではなく、oracle file 上の正本仕様断片を確認したい。

## hash
- 90d5c7b3501be284473425dc316ee0a0afc1386fcfadb857cb621fbda4a1bb7b

# `test_session_cli.py`

## Summary
- session branch と session state のライフサイクルを、CLI の外部挙動としてまとめて検証する realization test。
- fork、join、abandon、linked worktree、state cleanup、dirty worktree 拒否、conflict 解消 agent の制約、エラー出力先を同じ session 状態遷移の観測点として扱う。
- 大きいテストファイルだが、同じ branch/state fixture を追う必要があるため session CLI 回帰テストとして一箇所に保たれている。

## Read this when
- session fork/join/abandon の CLI 挙動、出力、終了コード、branch/state 更新を変更または確認する。
- session state file の生成、破損検出、collision retry、active/joined/abandoned 遷移を検証するテストを探している。
- linked worktree 上の session 操作、preprocess invariants、dirty worktree 拒否、home branch 欠落時の挙動を確認する。
- session join の conflict 解消 agent 呼び出し、writable profile、conflict path、非 conflict 差分拒否、conflict marker 検出、delete conflict staging を確認する。
- session abandon/join の cleanup 失敗、session branch 削除失敗、エラーレポートの stdout/stderr 振り分けを変更する。

## Do not read this when
- session CLI 以外のサブコマンドや、session 状態遷移に関係しない一般的な CLI テストを探している。
- session の内部 helper 単体の詳細だけを確認したい場合で、外部挙動や git/state 副作用を追う必要がない。
- agent call の出力品質そのもの、または Codex CLI/LLM の生成内容を検証したい。
- oracle file の正本仕様本文を確認したい場合。

## hash
- 4d36820c80933ac20f61dfe958673b7b8233b38020039b054a72c5e77ca6dee9

# `test_struct_doc_rendering.py`

## Summary
- StructDoc の Markdown renderer が通常テキストとコードブロック内の連続空行をどのように畳むかを検証する単体テスト。renderer の整形互換性、特に不要な空行の圧縮とコードフェンス内の空行保持境界を確認する入口になる。

## Read this when
- StructDoc から Markdown へ変換する処理の空行整形を変更・確認したいとき。
- render_as_markdown の出力に含まれる通常テキストの連続空行、またはコードブロック内の連続空行の期待値を確認したいとき。
- Markdown renderer の分割根拠に対応する realization test を探しているとき。

## Do not read this when
- StructDoc のデータ構造や renderer 実装そのものを確認したいだけのときは、実装側を直接読む。
- Markdown renderer 以外の prompt builder、oracle、CLI 挙動のテストを探しているとき。
- INDEX.md エントリー生成規則やルーティング文書の書き方を確認したいとき。

## hash
- 51580019f3a5f35c894b459980668eec4b098eecee22f1645f571c7c2084f811
