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
- cmoc の基礎 runtime 契約を横断的に検証する realization test。root placeholder 解決、linked worktree と work root 判定、config 読み書き、CmocError の Markdown 表示、CLI 解析 error の stdout report、subcommand log、session state、FileAccessMode から Codex profile/sandbox への変換、binary 判定など、個別サブコマンドより下の共通実行前提をまとめて扱う。
- 共通 fixture と root 状態を共有する runtime 回帰テスト群であり、runtime の基礎契約を変更したときに、CLI 実行前処理・権限 profile・状態読み書き・error 表示が一緒に崩れていないか確認する入口になる。

## Read this when
- root placeholder、repo root、work root、run root、linked worktree の解決や拒否条件を変更する。
- cmoc config の default、JSON 変換、読み込み失敗、型検証、削除済み設定の扱いを変更する。
- CmocError、render_error、CLI parse error、stdout/stderr の error report、doctor preprocess、subcommand log の生成・記録内容を変更する。
- session branch/apply branch からの session id 抽出、session state file の読み書きや不正値検証を変更する。
- FileAccessMode、Codex sandbox mode、Codex cwd、Codex profile の read/write 許可 root、extra writable/read root、oracle conflict write、local SLM provider 設定を変更する。
- `.cmoc/local` の gitignore 追加、起動 wrapper の missing venv report、binary 判定の読み取り範囲など、runtime の共通補助挙動を変更する。

## Do not read this when
- 特定サブコマンド固有の業務ロジック、出力内容、状態遷移だけを確認したい場合は、そのサブコマンドの test を直接読む。
- oracle file の正本仕様本文や oracle src の定義自体を確認したい場合は、oracle 側の該当本文を読む。
- INDEX.md エントリー生成やルーティング文書の規則だけを確認したい場合は、routing/index standard 側を読む。
- 個別 helper の実装詳細だけを調べる場合は、対応する runtime 実装 module を直接読む。

## hash
- cce8b1beaaadaafaef5afd80874f4e7502795e4ba9beb56465583e3d394ca0c8

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
- Codex CLI 実行ラッパーの統合テスト群。プロファイル生成、sandbox/permissions、作業ディレクトリ、schema 保存先、call log、cmoc managed ollama provider 連携、real Codex CLI を使う任意統合経路を検証する。
- fake Codex 実行ファイルを使い、実際に渡される argv、stdin、環境、生成された TOML profile、出力ファイル、許可された writable/readable root が期待どおりかを外部挙動として確認する。

## Read this when
- Codex CLI を起動する実行経路、profile 生成、`--cd`、`--output-schema`、`--output-last-message`、call log、prompt log の挙動を変更する場合。
- file access mode ごとの sandbox 設定、読み取り権限、書き込み可能 root、`.agents` を開かない制約を確認・変更する場合。
- cmoc managed ollama provider、local SLM profile、real Codex CLI 統合、systemd user service を使う任意統合テストの期待挙動を確認する場合。
- linked worktree から実行する際の cwd、repo local state の保存先、追加 read path の扱いを変更する場合。

## Do not read this when
- agent call parameter のデータ構造や enum 定義だけを確認したい場合は、それらの定義元を読む。
- cmoc 設定値や model provider の正本定義だけを確認したい場合は、設定・oracle 側の定義を読む。
- Codex 実行ラッパー以外の CLI サブコマンド、ルーティング文書生成、通常の git 操作の挙動を調べる場合。
- 単体 helper の内部実装だけを変更し、このテストが検証する公開的な実行引数・profile・保存先・権限に影響しない場合。

## hash
- 26e81e283fcb12ded3ef4e78fd6cb20cdbdd42f1ef127e8a06164c3e5c39c1bd

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
- doctor CLI と doctor 前処理の realization test。リポジトリ修復、設定生成・同期、cmoc 管理 Ollama の準備・検証、リンク済み worktree での対象 root 判定、既存 staged/unstaged 変更の保護を外部挙動として検証する。
- Ollama service の起動確認、listener PID 検証、model pull/load の制御、ローカル SLM profile 準備時の doctor 実行も扱う。

## Read this when
- doctor コマンド、dector alias、doctor 前処理、設定ファイル生成・同期、.cmoc/local ignore/untrack、.agents/.gitignore 修復 commit の挙動を変更または調査するとき。
- cmoc 管理 Ollama の install/service/model 準備、service 検証失敗、listener process 判定、cmoc provider model の重複排除 pull を変更または調査するとき。
- リンク済み worktree で doctor がどの root の config を使い、どの worktree を修復対象にするかを確認するとき。
- doctor が既存の staged 変更、unstaged hunk、staged rename、preexisting staged .gitignore を壊さないことを確認するとき。
- ローカル SLM 用 Codex profile 作成時に Ollama port が無い場合の doctor 連携を変更または調査するとき。

## Do not read this when
- doctor 以外の CLI サブコマンドや agent call の挙動だけを調べるとき。
- 設定 schema や default 値そのものの正本仕様を確認したいとき。
- Ollama binary の取得方法や systemd unit の生成ロジックを実装レベルで読む必要があり、テスト期待値ではなく本体実装へ直接進むべきとき。
- テスト支援 fixture、fake environment、repo 作成 helper の定義だけを確認したいとき。

## hash
- 60fc3a0ae86a2c96125d2d2f81c5d7e3227d3cc200f3618d2d7942bbd6dd986d

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
- review oracle の CLI 外部挙動と所見評価 loop を検証するテスト。対象 oracle の列挙、scope 別の選択、report 生成、accepted/rejected 所見の分類表示、merge/validate/judge の制御、上限到達時の失敗、review worktree と join commit、INDEX.md 変更の取り込み、処理失敗時 report、想定外差分の拒否を扱う。
- eval-oracle が review oracle 実装へ委譲する互換経路、oracle_path プレースホルダ解決、oracle symlink や tracked ignored oracle file の扱いもこのテストで確認する。
- このファイルは大きいが、同じ review run の fake Codex 応答、report 文脈、所見状態を共有する統合的なテスト群としてまとまっている。

## Read this when
- review oracle CLI の挙動、report の出力内容、scope full/session の対象選択、所見の列挙・検証・judge・merge loop を変更する。
- oracle file の列挙条件、tracked ignored file、symlink、AGENTS.md/INDEX.md 除外、<oracle-root>/<work-root> の oracle_path 解決を確認したい。
- review 実行用 worktree、linked worktree 上の session branch、review_join_commit、INDEX.md 変更の merge や conflict 解決に関わる処理を変更する。
- review oracle 実行中のエラー report、未コミット差分の拒否、review が INDEX.md 以外の差分を作った場合の拒否や復元を確認したい。
- eval-oracle コマンドと review oracle コマンドの接続を変更する。

## Do not read this when
- oracle review 以外の CLI サブコマンドや session 操作だけを調べる場合。
- report の文字列整形ではなく、Codex 実行基盤、設定読み込み、runtime preflight の一般処理だけを調べる場合。
- INDEX.md エントリー生成の仕様や oracle/realization 標準そのものを確認したい場合。
- 単体 helper の詳細実装だけを確認でき、review oracle の CLI 経由の外部挙動や loop 制御に関心がない場合。

## hash
- 7c7dfdfed515a03c4c2db9f4195bb17fa89d5a732c1afb6fe4e0bb65d9d2cdfc

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
