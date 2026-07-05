# `_support.py`

## Summary
- CLI と runtime 周辺のテストで共有する pytest 用 helper 群。最小 Git リポジトリ、Codex home、fake Codex profile、fake Ollama/systemctl、Typer runner 実行、apply worktree 解決など、外部コマンドや環境状態を伴うテスト準備をまとめる。

## Read this when
- CLI コマンドのテストで、一時 Git リポジトリや初期 commit 済み作業ツリーを用意する必要があるとき。
- Codex CLI 実行・profile 生成・CODEX_HOME・AgentCallParameter をテスト内で差し替える準備を確認または変更するとき。
- doctor/init や managed Ollama 起動確認を、実サービスではなく fake ollama/systemctl で検証するテストを扱うとき。
- session state から apply 用 worktree path を解決するテスト補助を使う、またはその挙動を変更するとき。

## Do not read this when
- 個別コマンドの期待出力や分岐条件そのものを確認したいだけで、テスト側の環境構築 helper が関係しないとき。
- 本体実装の Git 操作、Codex profile 生成、Ollama 管理、apply worktree 解決のロジックを調べるとき。
- oracle file の正本仕様やテスト方針を確認する必要があるとき。
- 単純な unit test の assertion 追加だけで、共有 fixture・fake 外部コマンド・一時リポジトリ作成を変更しないとき。

## hash
- 044b35ca5c83b73269dccfa6ace64a9a46dc6fd7c0206ba29863420ed577ee03

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
- apply fork CLI の統合的な外部挙動を検証する realization test。Codex 実行を fake 化し、apply run の開始・完了、state 更新、apply branch/worktree の作成、report 前の completed 書き込み、doctor preprocess、設定読み込み失敗時の中断、`.gitignore` 編集、target 正規化を扱う。
- session fork 済み状態から apply fork を実行したときの state schema、branch 命名、worktree 配置、不要な旧 state field や pid file の不在を確認する入口になる。
- target 正規化について、root 直下 memo、管理領域、規範 path、`.cmoc/local`、tracked ignored file、binary file、oracle 配下 symlink の扱いを確認する入口になる。

## Read this when
- apply fork の CLI 挙動、state 遷移、apply branch/worktree 作成、Codex loop 呼び出し順を変更または調査するとき。
- apply fork 実行前の doctor preprocess、`.cmoc/local` ignore 修復、clean worktree 維持、`.gitignore` を所見対象として編集できる挙動を確認するとき。
- 設定ファイルの欠落・JSON 不正など、apply run を開始する前に失敗すべき条件と、そのとき branch/state/pid を作らない保証を確認するとき。
- apply fork の対象列挙・正規化で、realization file 定義から外れる path、root 直下 memo、tracked ignored file、binary、symlink、`.cmoc` 配下の扱いを確認するとき。
- linked worktree 上で session branch と HEAD を基準に apply run を開始する挙動を調査するとき。

## Do not read this when
- apply fork 以外のサブコマンドや、session fork 単体の詳細だけを調査するときは、該当コマンドの実装・テストへ進む。
- Codex 実行 wrapper の一般仕様や実際の LLM 出力品質を調査するときは、この fake 前提の CLI テストではなく Codex 呼び出し層を読む。
- target 正規化の実装詳細だけを局所的に変更するときは、まず apply fork 実装側の正規化関数を読み、必要に応じてこのテストで外部挙動を確認する。
- report 本文の形式や表示内容を調査するときは、report 生成処理の実装・テストへ進む。

## hash
- 1c15028df8aab20679cc428e8652a4cd9d678da3b95b291df94acdc19d8750a2

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
- cmoc の基礎 runtime 契約を横断的に固定する回帰テスト。root placeholder 解決、linked worktree と run/work root、config 読み書きと validation、CmocError の Markdown 表示、CLI error の stdout 化、subcommand log、session/apply branch state、`.cmoc` ignore、FileAccessMode から Codex sandbox/profile への変換、binary 判定など、個別サブコマンドより下位の共通実行前提を扱う。
- 共通 fixture と root 状態を共有して検証する性質が強く、個別機能の単体テストではなく runtime 境界の崩れをまとめて検出する入口として位置づけられる。

## Read this when
- root path placeholder、repo root、work root、run root、linked worktree の扱いを変更または調査する。
- CmocConfig の既定値、dict 変換、config validation、missing config error を変更または調査する。
- CmocError、CLI parse error、CLI preflight error、error report の stdout/stderr 境界や Markdown 表示を変更または調査する。
- subcommand log の生成条件、timestamp 衝突時の log path、pre-log check 失敗時の副作用を変更または調査する。
- session/apply branch 名から session id や state を扱う処理を変更または調査する。
- `.cmoc` の gitignore 追加、run worktree 作成・削除の安全境界を変更または調査する。
- FileAccessMode、Codex sandbox mode、Codex profile の writable/readable path 制約、local SLM provider 設定を変更または調査する。
- binary 判定の読み取り量や runtime content 判定を変更または調査する。

## Do not read this when
- 特定サブコマンド固有の正常系・業務ロジックだけを確認したい場合は、そのサブコマンドのテストを先に読む。
- oracle 文書の正本仕様や prompts の内容を確認したい場合は、対応する oracle file を直接読む。
- 個別 helper の内部実装だけを局所的に変更し、root/config/error/profile など共通 runtime 契約に影響しないことが明らかな場合は、該当実装とより小さいテストを先に読む。

## hash
- a21e84da85716a6c94671abc7b170415e0ad9e49f927f2b265896bb4f6c574cb

# `test_cli_tui.py`

## Summary
- TUI 起動直前の CLI 前処理について、エディタで作成された依頼文の整形、パラメータ解決、Codex TUI 起動用パラメータ、ログ保存先、gitignore 更新、linked worktree 上での root/cwd/schema/log の扱いを外部挙動として検証するテスト。

## Read this when
- TUI サブコマンドの起動前処理、依頼文保存、補完済みプロンプト生成、Codex 実行パラメータ解決、または Codex TUI 呼び出し条件を変更する。
- TUI サブコマンドが生成するローカルログ、schema 配置、`.cmoc/local` の gitignore 対象化、または linked worktree での保存先解決を確認する。
- エディタ入力から削除されるテンプレート文言、補完済みプロンプトに含める標準文書、file access mode の既定値を検証する。

## Do not read this when
- TUI 起動前処理ではなく、Codex 本体の対話 UI や LLM 応答品質そのものを確認したい。
- TUI 以外のサブコマンド固有の CLI 挙動だけを変更する。
- oracle 側の仕様断片やルーティング文書の内容を確認したい。

## hash
- 108810a6a73d65b528b8eedfa8b0132a62f06394c906c075e5572579e029b5bf

# `test_codex_runtime_errors.py`

## Summary
- Codex CLI 実行ラッパーが外部コマンド未導入時に利用者向けの CmocError を返すことを検証するテスト。exec 経路と TUI 経路の両方で、subprocess から FileNotFoundError が出た場合のエラー変換を扱う。

## Read this when
- Codex CLI が存在しない環境でのエラー処理、例外メッセージ、または CmocError への変換を変更・確認したいとき。
- Codex 実行の exec 経路と TUI 経路に共通する外部コマンド起動失敗時の挙動を確認したいとき。
- Codex 実行テストで subprocess.run の差し替え、リポジトリ fixture、Codex home/profile stub の使い方を確認したいとき。

## Do not read this when
- Codex CLI が正常に存在する場合の標準入出力、成功時戻り値、または実行結果の解析を確認したいとき。
- Codex の設定値、プロファイル生成、または runtime 全般の正常系を調べたいだけのとき。
- 外部コマンド未導入以外の Codex 実行エラーや終了コード処理を確認したいとき。

## hash
- 2454f19fb74101e9efac6c84c115ffd723173aba2ff033a65a1ab5185c82ade7

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 実行ラッパーの外部挙動を、偽の codex 実行ファイルと一時 Git リポジトリで検証するテスト群。
- プロファイル生成、作業ディレクトリ、標準入力、出力取得、sandbox の writable_roots、ローカル SLM 用 provider 設定、schema 保存場所、linked worktree での実行引数を扱う。
- 実際の Codex CLI 品質ではなく、run_codex_exec が codex exec に渡す引数・環境・生成設定と、結果オブジェクトへ反映する値の契約を確認する入口。

## Read this when
- run_codex_exec の引数構築、profile TOML 生成、CODEX_HOME 配下の設定ファイル、または --cd と実プロセス cwd の関係を変更する時。
- FileAccessMode.REPO_WRITE、PURE_ORACLE_READ、READONLY が sandbox 設定や writable_roots にどう反映されるべきかを確認したい時。
- managed Ollama や ModelClass.MINIMUM 向けの model_provider 設定、builtin Ollama 用フラグを使わない挙動を変更・検証する時。
- structured output schema のコピー先を、linked worktree ではなく元の repo root 配下に置く挙動を変更する時。
- linked worktree からの実行で、cwd、--cd、extra_read_paths 周辺の Codex 起動挙動を確認する時。

## Do not read this when
- Codex 実行ラッパーの実装そのものを変更したいだけで、まず実装箇所の責務や内部構造を確認すべき段階。
- oracle file の分類、path placeholder の定義、または cmoc 全体の仕様方針を確認したい時。
- Codex CLI や LLM の実出力品質、推論内容、対話内容そのものを検証したい時。
- Git worktree 作成 helper、テスト用 executable 生成 helper、または test support fixture の実装詳細だけを調べたい時。

## hash
- d5db898b5b7af9e3c94d01dc651c54f9f90bb1f4593ff59b22092b7e9bf2e161

# `test_codex_runtime_exec_post_validation_forbidden.py`

## Summary
- Codex CLI 実行後に、禁止領域への差分を後段検証で拒否しない挙動を検証するテスト群。oracle や .git への書き込み、既存の禁止差分、schema retry、session join の競合対象など、実行結果や retry 制御を優先する境界を扱う。

## Read this when
- Codex CLI 呼び出し後の file access 違反検出を変更する時。
- 禁止領域への差分がある状態で、retry・失敗終了・schema 検証・session join がどう振る舞うべきかを確認する時。
- oracle や .git など通常は書き込み禁止の場所に差分が発生した場合でも、後段検証で実行を止めない条件を確認する時。

## Do not read this when
- Codex CLI に渡す引数、環境変数、sandbox 設定そのものの組み立てだけを確認したい時。
- file access 違反の事前防止や権限プロファイル生成の仕様を確認したい時。
- 通常の Structured Output 成功・失敗処理だけを確認したく、禁止領域差分との相互作用を扱わない時。

## hash
- 16d397a8bbb52f49de8c29f5076e936a4e0c0988c7ed16192e028fc7ab817581

# `test_codex_runtime_exec_post_validation_runtime.py`

## Summary
- Codex 実行後の差分検査が、git ignore 対象、実行時キャッシュ、仮想環境、ブロック対象ディレクトリ、cmoc ログなどの副作用を許容する境界を検証するテスト群。
- FileAccessMode ごとに、post-call file access check の対象外として扱うべき runtime diff と、run_codex_exec が呼び出しを不要に再試行しないことを確認する。

## Read this when
- run_codex_exec の実行後ファイルアクセス検査で、許容する差分・無視する差分・ブロック対象配下の扱いを変更する。
- READONLY、REALIZATION_WRITE、REPO_WRITE の各モードで、エージェント実行後に残るキャッシュ、ログ、ignored untracked file、memo/.agents/.codex/.git 配下の差分を扱う挙動を確認する。
- Codex 呼び出し後の副作用が原因で再試行や失敗が起きるかどうかをテストしたい。

## Do not read this when
- Codex CLI に渡す引数、標準出力イベント、last message の基本的な成功・失敗処理だけを確認したい。
- 事前の file access sandbox 設定や、Codex 実行前の権限モデルそのものを調べたい。
- oracle file と realization file の定義やパス分類の正本仕様を確認したい。

## hash
- e16b72b4e3f4693dc8788ef855d071eb27431de5db16ece11f1c542fcc6e14fc

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
- Codex quota exceeded 後の retry 状態機械を外部挙動から検証する realization test。quota 検出後の probe 共有、resume token 抽出、resume または再実行、call log・subcommand log、CODEX_HOME と cwd の扱い、失敗時の post validation 抑制を同じ fake Codex 呼び出し列の観測点として扱う。

## Read this when
- Codex exec が quota exceeded を返した後の待機、probe、resume、再実行の制御を変更・確認したいとき。
- quota availability probe の parameter 生成、oracle builder への委譲、probe 用 profile・model・reasoning effort・file access mode の分離を確認したいとき。
- quota retry 中に出力される call log、stdout・stderr・prompt・output log、subcommand log、console 表示の期待挙動を確認したいとき。
- 複数の Codex exec が同時に quota 待機した場合に、代表 probe を 1 回だけ実行し、待機中の呼び出しが復帰または失敗を共有する挙動を確認したいとき。
- quota poll limit 到達時や probe 失敗時に、失敗した Codex 呼び出しの file access post validation を実行しないことを確認したいとき。

## Do not read this when
- 通常の Codex exec 成功経路、CLI 引数組み立て、profile 生成だけを確認したいときは、より直接その責務を持つ実装またはテストを読む。
- quota retry と関係しない file access validation、repository setup、subcommand logging の一般挙動だけを確認したいとき。
- oracle builder 側の probe prompt 内容や正本仕様そのものを確認したいときは、対応する oracle 側の定義を読む。

## hash
- 356488debb1c23494fb42612361330802da8c88f1eecc7971ee336453250c77d

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

# `test_codex_runtime_subprocess.py`

## Summary
- Codex subprocess 実行 helper が apply process tracking 用の環境変数を扱う境界を検証するテスト。追跡付き実行では子プロセスが専用 process group で起動され、既存の追跡ファイル内容を保持したまま子プロセス情報を記録することを確認する。通常実行では親から継承した apply tracking 環境変数を無視し、外部の追跡ファイルを作らないことを確認する。

## Read this when
- Codex subprocess 起動処理、process group 分離、apply process tracking の記録挙動を変更する。
- 通常の Codex subprocess 実行で、親環境の tracking 変数を除去または無視する挙動を確認したい。
- runtime の Codex 実行 helper が子プロセスへ渡す環境変数や実行結果の扱いを変更した後、対応する外部挙動のテストを確認したい。

## Do not read this when
- Codex subprocess ではなく、一般的な path 処理、設定読み込み、CLI 引数解析のテストを探している。
- apply process tracking や process group 分離に関係しない runtime helper の挙動だけを確認したい。
- テスト補助関数そのものの実装や、一時 Python 実行ファイル生成 helper の詳細を調べたい。

## hash
- ad80da3fef78c45fa133633666d9a2d60df6a2244d07c1a849846adadb2e363b

# `test_codex_runtime_tui.py`

## Summary
- Codex TUI 実行ラッパーのテスト。追加読み取りパスの事前検査、完了プロンプトの許可、linked worktree での cwd/profile 設定、Codex CLI 非ゼロ終了時のエラー表示と呼び出しログを検証する。

## Read this when
- Codex TUI 起動時の sandbox/profile/cwd/追加読み取りパス制御を変更する場合。
- `run_codex_tui` のエラー処理、呼び出しログ、非ゼロ終了時の利用者向け出力を確認する場合。
- `.cmoc/local/log/tui` の完了プロンプトや linked worktree からの TUI 実行許可を扱う場合。

## Do not read this when
- Codex API 実行や TUI 以外の runtime 呼び出しを確認したい場合。
- 設定ファイルの読み込み仕様や repository 作成 helper 自体を調べたい場合。
- oracle file のアクセス分類や path model の正本仕様を確認したい場合。

## hash
- 3c68f30c7fc5f422a0c2b28779e4b6eb456b6e89eba6bc979dc31d89e1105d9f

# `test_doctor_cli.py`

## Summary
- doctor/init CLI がリポジトリの git 状態、無視設定、管理下 Ollama、設定ファイルをどう修復・生成するかを外部挙動として検証するテスト群。
- doctor preprocess が linked worktree を対象にすること、既存の staged 変更や人間の設定値を巻き込まないこと、cmoc 管理ファイルを追跡対象から外すことを確認する。
- Codex profile 準備時に管理下 Ollama の port が未準備なら doctor 相当の準備が走る連携挙動も扱う。

## Read this when
- doctor または init コマンドの git 修復、.cmoc 無視、.agents 管理、設定生成・同期の挙動を変更する。
- 管理下 Ollama の install/service/model pull/検証ロジック、または service process と listener の照合条件を変更する。
- linked worktree 上での doctor 実行対象、既存 staged 変更の退避・復元、修復 commit に含める path の境界を確認したい。
- local SLM 用 Codex profile 作成時に doctor preprocess が起動する条件を変更・確認する。

## Do not read this when
- doctor/init の CLI 外部挙動ではなく、個別の設定 schema 定義や model enum の意味だけを確認したい場合は、その定義元を直接読む。
- agent call の一般的な parameter 構造や Codex profile の通常生成だけを調べたい場合は、profile 実装とその専用テストを直接読む。
- Ollama や systemd の低レベル helper 単体の実装詳細だけを調べる場合は、runtime doctor 実装を直接読む。

## hash
- b3f9940592b6bfff68fc4e939dead57f1af0aef503cc2bda1b7b44c8833e5291

# `test_indexing_cli.py`

## Summary
- routing document の生成・更新を行う indexing 系 CLI と preflight の外部挙動を検証する回帰テスト。
- 生成対象の列挙、既存 hash による再利用、Codex entry builder 呼び出し、commit 対象の限定、linked worktree、未初期化または dirty な状態、conflict 解決を同じ routing 更新ワークフローとして扱う。

## Read this when
- indexing subcommand や indexing preflight の CLI 境界、git 状態、commit 条件、linked worktree 上の挙動を変更する。
- routing document の生成対象、空ディレクトリ、root 直下 memo の除外、ネストした memo の扱い、symlink cycle 回避、兄弟 entry の描画順や並列生成を変更する。
- entry schema の検証、既存 hash が新鮮な場合の再生成スキップ、malformed entry の再生成、Codex への structured output schema 指定を確認する。
- apply 側の INDEX conflict 解決で、対象 document の削除、未解決 conflict の解消、merge commit の成立を確認する。

## Do not read this when
- 個別の routing document 本文を作るだけで、indexing CLI や更新ワークフローの挙動を確認しない。
- Codex 実行や git 操作を伴わない純粋な entry 文面の品質だけを扱う。
- indexing 以外の subcommand、apply join の一般処理、設定ファイル形式そのものを変更する場合で、routing document 更新や conflict 解決に触れない。

## hash
- e5f0405a6aa471fc4f60ad61941d770a887aac67f98eb8b6d88a5376ec637921

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
- review oracle の CLI 実行、report 生成、対象 oracle file の列挙、所見の列挙・検証・judge・merge loop、review 用 worktree の join 結果を外部挙動として検証するテスト群。
- accepted/rejected finding の report 表示、fatal/minor 件数、no_targets/error の report、tracked ignored oracle file や symlink の扱い、INDEX.md 差分の merge と非 INDEX.md 差分の拒否までを同じ review run 文脈で扱う。

## Read this when
- review oracle コマンドの CLI 出力、report の構成・メタ情報・件数・section 順序を変更または確認したいとき。
- oracle file の review 対象列挙、full/session scope、tracked ignored file、AGENTS.md・INDEX.md 除外、symlink の分類条件を確認したいとき。
- finding の enumerate loop、同一対象への既存 finding の渡し方、challenger/advocate/judge/merge の制御、merge operation の契約や retry 挙動を変更するとき。
- review 実行中に生成された INDEX.md 差分の取り込み、preflight indexing の反映、join commit の report 表示、merge conflict 解消、非 INDEX.md 差分の拒否を確認したいとき。
- review oracle が途中失敗した場合の error report と CLI 表示を変更または検証したいとき。

## Do not read this when
- oracle review 以外の review サブコマンドや、report 生成を伴わない汎用 CLI 挙動だけを確認したいとき。
- oracle file の正本仕様本文そのものや、仕様文書の編集方針を確認したいとき。
- INDEX.md エントリー生成の一般規則や routing 文書の構成だけを確認したいとき。
- Codex 実行基盤や preflight の単体的な実装詳細だけを確認したいとき。
- session fork や git worktree 操作そのものの基本挙動だけを確認したいとき。

## hash
- 8f9544479db593c17e5a54d9ba47e1f89000aad759b50632b038bf3bcd60d112

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
