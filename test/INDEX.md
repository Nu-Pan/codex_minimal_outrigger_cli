# `_support.py`

## Summary
- CLI と runtime 周辺の realization test で共有する pytest 用 helper 群。最小の git リポジトリ作成、Codex home/profile の stub、fake Ollama/systemctl、doctor 実行、apply worktree 解決など、外部状態や subprocess を伴うテスト準備を集約する。

## Read this when
- CLI テストや runtime wrapper テストで、使い捨て git repository、Codex home、AgentCallParameter、fake 外部コマンドを用意したいとき。
- doctor 実行、managed Ollama 起動確認、systemctl 連携を実プロセスに依存せず検証するテストの前提を確認・変更するとき。
- session state から apply worktree path を解決するテスト helper の挙動を確認するとき。

## Do not read this when
- 個別コマンドの期待出力や CLI 挙動そのものを確認したいだけで、共有 fixture や fake 外部サービスの前提を変更しないとき。
- 本番実装の git 操作、Codex 実行、Ollama 管理、apply 処理を調べたいとき。
- oracle 側のテスト規則や正本仕様断片を確認したいとき。

## hash
- 8d2fdb8243af194d29d9c805c66dfe02fed058bcaa0bc7506667cc1741dd0904

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
- apply abandon が active apply run を破棄する外部挙動を CLI 経由で検証する realization test。apply worktree と branch の cleanup、state の ready 化、警告出力、running process 停止、pid reuse や終了競合への扱い、linked session/worktree からの実行境界をまとめて扱う。

## Read this when
- apply abandon の成功時 cleanup、警告扱い、失敗条件、出力内容を変更・確認するとき。
- running apply process の PID 読み取り、child process group 停止、pidfd signal、PID reuse 防止、停止順序に関する挙動を変更・確認するとき。
- apply worktree 内、linked session worktree、linked apply worktree、stale apply branch など実行位置ごとの abandon 境界条件を調べるとき。

## Do not read this when
- apply abandon 以外の apply サブコマンドの通常処理や Codex 実行結果の生成を調べたいとき。
- session fork、doctor、git helper、state 保存形式そのものの実装を調べたいとき。
- process 停止の単体的な仕様ではなく、他コマンドの process 管理や一般的な runtime helper を調べたいとき。

## hash
- 4acf89c60ce02aade6c08bf5801e01a9c3325bd6deffe0f3458863e1411e2a86

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
- CLI 経由の apply fork 制御を、所見列挙、所見適用、commit、変更要約、report 生成、session state 更新まで一連の挙動として検証するテスト。
- apply fork 用 ACP builder の import 可能性、prompt/schema の接続、変更ファイル再調査、収束・未収束・error report、未追跡/削除済み file の変更要約、rolling apply fork の対象選定を扱う。
- apply fork report の期待値と loop 制御の観測文脈を一箇所に集めることで、report schema と再検査制御の関係を追える入口になる。

## Read this when
- apply fork の CLI 実行結果、終了コード、report 内容、session state 更新、apply branch の commit 結果を変更または調査する。
- apply fork が所見適用後に変更 file や新規ディレクトリ配下を再調査する条件、収束・未収束の判定、上限到達時の扱いを確認する。
- apply fork の error report や変更要約が、commit 前差分、未追跡 file、削除済み tracked file をどう扱うかを確認する。
- apply fork 用 ACP builder の prompt、Structured Output schema path、packaged layout での import、禁止領域書き込み時の挙動を確認する。
- rolling apply fork が前回 apply join 後の oracle 変更だけを対象にするかを調査する。

## Do not read this when
- apply fork の内部 helper 単体の実装だけを確認したい場合は、実装側の該当モジュールを直接読む。
- apply join、session fork、doctor など apply fork report 以外の CLI 挙動だけを調査する場合は、それぞれの専用テストまたは実装を読む。
- ACP builder 全般の共通構造や oracle schema 自体を確認したい場合は、builder 実装または oracle 側の定義を読む。
- report 内容を伴わない単純な git 操作 helper、テスト fixture、実行支援関数の詳細だけを確認したい場合は、共通 test support を読む。

## hash
- f7fc8307f5c3e4f0bf58dbf73a36a4b57ee9c714f53b982f093d6494601e8fef

# `test_apply_join_cli.py`

## Summary
- apply run を session へ join する CLI 外部挙動を検証するテスト。apply worktree と branch の cleanup、session state 更新、report 生成、linked session worktree への merge、dirty worktree 拒否、想定外差分検出、force resolve、merge conflict 処理を同じ join 操作の境界条件として扱う。
- apply join が realization file と session 側変更をどう分類し、oracle、memo、AGENTS、INDEX、.codex、gitignore、tracked ignored file、rename/delete path をどう扱うかを確認する入口。

## Read this when
- apply join の成功時 cleanup、state 更新、report 出力、または apply worktree から実行した場合の残存挙動を変更・確認したいとき。
- apply join が dirty apply worktree、stale apply branch、想定外差分、merge conflict を拒否または報告する条件を確認したいとき。
- apply join の --force-resolve が oracle、AGENTS、.codex などの想定外差分を戻す挙動を変更・確認したいとき。
- apply join の変更パス分類、managed branch 上の rename/delete 扱い、root memo や tracked ignored file の期待変更判定を確認したいとき。
- linked session worktree から fork された apply を、root ではなく現在の session worktree へ join する挙動を扱うとき。

## Do not read this when
- apply fork の Codex 実行、prompt 構築、または apply branch/worktree 作成だけを確認したいとき。
- session fork、doctor、git helper、test fixture の一般的な挙動を確認したいだけで、apply join の外部挙動に関心がないとき。
- INDEX.md エントリー生成や oracle/realization の概念定義そのものを確認したいとき。
- apply join の内部実装だけを局所的に調べたい場合で、CLI 経由の統合挙動や git 状態を伴うテスト確認が不要なとき。

## hash
- 4ccd1a3f2a8925b1f2beb303e380699abc4ed905cfe5a2eab7c7be7ba900625e

# `test_basic_runtime.py`

## Summary
- cmoc の基礎 runtime 契約を横断的に検証する realization test。root placeholder と worktree 判定、config 変換・検証、CmocError の表示、CLI wrapper の preflight と error report、subcommand log、session state、FileAccessMode から Codex profile への変換、binary 判定など、個別サブコマンドより下位の共通前提をまとめて扱う。
- 共通 fixture と root 状態を共有しながら崩れやすい runtime 境界を回帰確認する入口であり、CLI 全体の実行前提や sandbox/profile 生成の変更時に読む対象。

## Read this when
- root、repo root、work root、run root、linked worktree、placeholder path 解決の挙動を変更または確認する。
- CmocError、CLI 引数解析 error、stdout/stderr の error report、doctor preprocess、subcommand log の共通 runtime 挙動を変更または確認する。
- cmoc config の既定値、dict/JSON 変換、入力検証、model spec、reasoning effort の扱いを変更または確認する。
- session/apply branch 名から session id や state を読む処理、session state file の validation を変更または確認する。
- FileAccessMode、Codex profile、sandbox writable/read permission、追加書き込み許可 path、oracle conflict write の許可境界を変更または確認する。
- binary 判定、duration formatting、`.cmoc/local` ignore、起動 wrapper の missing venv report など、複数サブコマンドにまたがる基礎 runtime 回帰を確認する。

## Do not read this when
- 特定サブコマンド固有の business logic、個別 prompt、個別 report 内容だけを確認したい場合は、そのサブコマンドや対象機能の test を読む。
- oracle doc や oracle src の正本仕様そのものを確認したい場合は、対応する oracle file を読む。
- runtime helper の実装詳細だけを局所的に変更する場合は、まず対応する src 側の module を読み、外部挙動の回帰確認が必要になったときに読む。
- INDEX.md の生成規則やルーティング文書の内容だけを扱う場合は、indexing 関連の対象を読む。

## hash
- fbb6e6bbb1e9b3c5a90815bc0b450fc1d61922df31ee64752d55218af5357016

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
- Codex CLI 実行ラッパーのテスト群で、profile 生成、sandbox 設定、作業ディレクトリ、schema 保存先、管理 Ollama provider 設定、実 Codex CLI 呼び出し時の記録内容を検証する。
- fake executable と実 Codex CLI の両方を使い、agent call parameter から Codex exec の引数・標準入力・出力・ログ・設定ファイルへ反映される境界を確認する。

## Read this when
- Codex exec 起動処理、profile TOML 生成、sandbox writable roots、CODEX_HOME 配下の profile 配置、prompt/output/schema ログの扱いを変更する時。
- 管理 Ollama provider、local SLM model、Codex CLI の provider 指定、または Codex CLI へ渡す引数を変更する時。
- linked worktree での cwd、repo local 配下の状態保存先、extra read path、schema path の扱いを確認する時。
- Codex 実行ラッパーの外部挙動をテストで固定したい時、または既存テストに同じ観点のケースを追加できるか判断する時。

## Do not read this when
- Codex CLI 実行に関係しない設定読み込み、path model、または agent call parameter の純粋なデータ定義だけを確認したい時。
- LLM の応答品質、生成文面の妥当性、または Codex CLI 自体の内部実装を検証したい時。
- oracle 側の正本仕様断片や開発規則そのものを確認したい時。

## hash
- 7603b7d57d09490689d56e65b4bb0a2205a24e1bda435bf05940f1d9c79a410f

# `test_codex_runtime_exec_post_validation_forbidden.py`

## Summary
- Codex CLI 実行後の差分検証が、許可されない oracle 側変更を検出して CmocError にすることを検証する realization test。
- schema retry、既存の禁止差分、引用符や空白を含む oracle path、session join resolution の許可対象外差分など、post validation の境界条件を扱う。
- 非ゼロ終了時や .git 配下変更時には post validation の禁止差分判定を優先しないこと、許可された realization 側変更は通すことも確認する。

## Read this when
- Codex CLI 実行後に禁止差分を検出する処理、特に oracle への書き込み検出や preexisting diff との差分比較を変更する時。
- FileAccessMode、extra_writable_paths、allow_oracle_conflict_writes、schema retry が post validation とどう相互作用するかを確認したい時。
- Codex CLI の終了コード、turn.completed、output-last-message 周辺の失敗処理と差分検証の優先順位を変更・調査する時。

## Do not read this when
- Codex CLI の引数構築、モデル選択、capacity wait など、差分検証後の禁止ファイル判定に関係しない実行制御だけを扱う時。
- oracle/realization のファイル分類ルールそのものや path model の正本仕様を確認したい時。
- 通常の realization ファイル編集許可や README 更新許可だけを確認したい場合で、post validation の失敗条件に踏み込まない時。

## hash
- 67adc5ced4af290ed713f19b63f51d7f73477533ba01abe6572425d6a5ba6c54

# `test_codex_runtime_exec_post_validation_runtime.py`

## Summary
- Codex 実行後のファイルアクセス検証について、実行時に発生し得る差分の許可・拒否境界を確認するテスト群。無視された生成物、一時キャッシュ、仮想環境、cmoc ログ、ブロック対象ディレクトリ配下の扱いを、アクセスモード別の外部挙動として検証する。

## Read this when
- Codex 実行後の禁止差分検出や許容差分の判定を変更する。
- readonly、realization write、repo write の各アクセスモードで、実行後に残るファイル差分の扱いを確認する。
- git ignore された生成物、一時キャッシュ、仮想環境、cmoc ログ、ブロック対象ディレクトリ配下の差分が許可される条件を調べる。
- Codex 用 sandbox profile の writable roots に、書き込み禁止領域が含まれないことを検証したい。

## Do not read this when
- Codex プロセスの起動引数、標準出力イベント、最終メッセージの通常処理だけを確認したい。
- ファイルアクセス分類そのものやパス種別の定義を調べたい。
- Codex 実行後の差分検証に関係しない CLI コマンド、設定読み込み、リポジトリ作成補助のテストを探している。

## hash
- 2b0bbc11e7e1f8f93ffd626e7d0a887566000327ecb4a3e190c9c33e9fceea8f

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
- Codex exec が quota exceeded になった後の待機、probe、resume token 利用、resume 不可時の再実行、call log と subcommand log、CODEX_HOME と cwd の扱いを検証する realization test。
- 並列実行時に quota availability probe を代表 1 回へ共有し、成功時は待機中の呼び出しが resume し、probe 失敗時は待機中の呼び出しも失敗することを確認する。
- quota retry 回帰の観測点を同じ fake Codex 呼び出し列で追うため、ファイルサイズは大きいが単一の retry 状態機械の外部挙動テストとして一箇所にまとまっている。

## Read this when
- Codex exec の quota exceeded 検出後の retry、probe、resume、再実行の挙動を変更または調査する時。
- quota availability probe の生成条件、最小モデル・低 reasoning・readonly・preflight 無効化・cwd 継承を確認する時。
- Codex call log、output jsonl log、prompt log、stdout/stderr log、subcommand log の quota retry 関連イベントを変更する時。
- CODEX_HOME が相対パスの場合の subprocess cwd、Codex の --cd、profile 分離の扱いを確認する時。
- 複数の Codex 呼び出しが同時に quota exceeded になった場合の代表 probe 共有と待機側の成否伝播を変更する時。
- quota poll limit 到達時または probe 失敗時に file access post validation を行わない挙動を確認する時。

## Do not read this when
- quota retry と無関係な通常成功時の Codex exec 起動引数や基本的な subprocess 実行だけを確認したい時。
- agent call parameter の一般的な構造、モデル種別、file access mode の定義だけを確認したい時。
- INDEX 生成、path model、oracle/realization の一般ルールなど、Codex runtime の quota retry 以外の仕様を調べる時。
- quota availability probe のプロンプト本文そのものの仕様だけを確認したい時は、probe builder 側を直接読む。

## hash
- cb134ed051e775572c74b9e5cf6a3f58d141acfdea2f63a238fa29a3ea3b40f1

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 実行ラッパーのリトライ挙動を検証する realization test。構造化出力の schema 不一致・JSON 解析失敗・capacity エラー時の再試行、call log と subcommand log の記録、capacity retry 後の file access violation 検出、stdout JSONL 外のエラーマーカーをリトライ条件にしないことを扱う。

## Read this when
- `run_codex_exec` のリトライ条件、構造化出力検証、capacity/quota エラー判定、call log 記録、または `codex_call` イベントの status を変更・確認する。
- Codex CLI 呼び出し失敗時に、出力ファイル、stdout/stderr、JSONL イベント、または file access violation をどう扱うかを調べる。
- `commons.runtime_codex` の外部挙動に関する回帰テストを追加・整理する。

## Do not read this when
- Codex CLI 呼び出しの通常成功経路だけを確認したい場合は、より直接その基本実行を検証するテストを読む。
- agent call parameter、config、logger、テスト用 repo 作成 helper の定義だけを調べたい場合は、それぞれの実装または support 側を読む。
- oracle file や INDEX.md の仕様・ルーティング規則自体を確認したい場合は対象外。

## hash
- 36bbd2e896572cbf17dce5a12fd44ebddfe4b4f24f7d4b1a6f15f738f1274513

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
- Codex TUI 呼び出し実行処理のテスト群。起動前の追加 read path 検証、complete prompt の許可範囲、linked worktree からの呼び出し時の作業ディレクトリ・権限 profile、Codex CLI/TUI 非ゼロ終了時のエラー表示と call log 記録を検証する。

## Read this when
- Codex TUI 実行ラッパーの挙動を変更し、subprocess 起動条件、cwd、--cd 引数、profile 生成、call log、エラー処理への影響を確認したいとき。
- 追加 read path の許可判定、memo 配下の拒否、complete prompt の扱い、PURE_ORACLE_READ と REPO_WRITE の差をテストで確認したいとき。
- linked worktree から Codex TUI を起動する場合の、prompt 参照、local 配下の read 権限、worktree 側の write 権限が期待通りか確認したいとき。
- Codex CLI/TUI が非ゼロ終了した時に、CmocError、コンソール出力、tui call log がどの外部挙動として固定されているか確認したいとき。

## Do not read this when
- Codex TUI ではない通常の Codex 実行、agent 呼び出し、または他サブコマンドのテストを探しているとき。
- 権限モデルや path 分類の仕様そのものを確認したいとき。この対象はそれらを使った TUI 実行時の外部挙動だけを検証する。
- Codex subprocess の細かい実装手順や profile TOML の生成ロジックを直接変更したいとき。まず実装側の該当処理を読む方がよい。

## hash
- 8aab459acdf1746faed23c188b30f0ccb5f8fd1a8adcc0e98c3f783312817abe

# `test_doctor_cli.py`

## Summary
- doctor CLI と doctor preprocess の外部挙動を検証する realization test。git 修復、`.cmoc/local` の ignore/untrack、`.agents` 管理、config 生成・同期、managed Ollama の導入・検証、linked worktree での対象 root 判定、`dector` alias、local SLM profile 作成時の doctor 起動を扱う。
- doctor 実行が既存の staged/unstaged 変更や rename を壊さないこと、repair commit と config commit の対象が分離されることを確認する入口になる。

## Read this when
- doctor コマンド、`dector` alias、または doctor preprocess の挙動を変更する。
- `.cmoc/config.json` の生成・default 同期・git tracking、または linked worktree で repo config を使う処理を変更する。
- `.cmoc/local` の ignore/untrack、`.agents/.gitkeep`、repair commit、既存 staged/unstaged 変更の保全に関わる git 操作を変更する。
- managed Ollama の install/service/model pull/listener verification、または cmoc provider model の pull 対象選定を変更する。
- local SLM 用 Codex profile 作成時に doctor を起動する条件や副作用を変更する。

## Do not read this when
- doctor 以外の CLI サブコマンドだけを変更する。
- config schema の定義そのものや serialization の単体挙動だけを確認したい場合は、config 側の実装・テストを先に読む。
- Ollama service helper の内部単体挙動だけを確認したい場合は、runtime Ollama 側のより直接的なテストや実装を先に読む。
- agent call parameter、model class、reasoning effort、file access mode の定義だけを調べる場合は、basic 側の対象を読む。

## hash
- a18521dbb2a3e559ad9094ac62e525f399f09d42776f2bc05ef760f5d9021d65

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
- Codex 実行前に INDEX 更新の preflight が走ること、更新が commit され worktree が clean に戻ること、実際の Codex 呼び出し順序が保たれることを検証する pytest。
- preflight 対象 root の選択、repository lock 待機、AgentCallParameter による preflight 無効化、file access violation 時に recovery 側の追加 indexing が走らないことを扱う。
- 実 git repository、fake Codex executable、monkeypatch した indexing 更新処理を使い、commons.runtime_codex_preflight と commons.indexing の連携挙動を外部挙動として確認する。

## Read this when
- Codex call または TUI call の前に indexing preflight が実行される条件や順序を変更する。
- cwd が別 worktree 内にある場合の indexing 対象 repository の選択ロジックを変更する。
- indexing lock、preflight の有効化・無効化、AgentCallParameter の indexing preflight フラグに関わる制御を変更する。
- Codex 実行失敗や file access violation 後の recovery 処理と indexing preflight の関係を確認する。

## Do not read this when
- INDEX.md 生成内容そのもの、各 entry の文面、indexing 対象ファイル探索の詳細だけを確認したい場合。
- Codex CLI の引数組み立てや subprocess 実行一般を確認したいが、indexing preflight との連携を扱わない場合。
- oracle/realization のファイルアクセス規則そのものを確認したい場合。

## hash
- 08f486a6d0b17bc60b01a7f81985a2be47ad9ce3233d4c0c2e65be6a55281410

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
- review oracle の CLI 外部挙動を検証する realization test。eval-oracle から review oracle 実装への委譲、review oracle report の生成内容、finding の列挙・検証・judge・merge loop、対象 oracle file の選択、review 用 worktree と join commit、INDEX.md 差分の扱い、処理失敗時 report、review 中の不正な非 INDEX 差分拒否を扱う。
- 対象選択、report 出力、finding 評価 loop、merge 操作、worktree 統合の各挙動が同じ review run の状態と fake Codex 応答を共有するため、review oracle の CLI 振る舞いを広く確認する入口になる。

## Read this when
- review oracle コマンド、eval-oracle コマンド、または review oracle の report 出力形式を変更する。
- review oracle の finding 列挙、検証、judge、merge、semantic retry、上限到達時の挙動を変更する。
- review oracle の対象 oracle file 判定、full scope と session scope、tracked ignored file、symlink、AGENTS.md や INDEX.md の除外条件を確認する。
- review oracle が linked worktree や session branch 上でどの oracle と commit を対象にするかを変更する。
- review oracle 実行中に生成された INDEX.md 差分の取り込み、preflight indexing 差分、merge conflict 解決、非 INDEX 差分拒否を変更する。
- review oracle の処理失敗時に error report を残す挙動や CLI へのエラー表示を変更する。

## Do not read this when
- review oracle 以外の review 種別、または oracle review と共有されない CLI コマンドだけを扱う。
- Codex 実行基盤、設定読み込み、git helper、session 管理などの内部実装だけを調べたい場合で、review oracle の外部挙動を確認する必要がない。
- report 本文の実装方法だけを局所的に調べたい場合は、まず review oracle 実装側を読む。
- oracle file の定義や realization standard そのものを確認したい場合は、正本仕様側を読む。

## hash
- e73f418d72a45d89af2bd56f7d5640651e45bbf92fef2ce10481799dab026c24

# `test_session_cli.py`

## Summary
- session の fork、join、abandon に関する CLI 回帰テストをまとめる。session branch と session state のライフサイクルを軸に、状態ファイル生成・更新、home branch への復帰、branch 削除、linked worktree、preprocess、dirty worktree 拒否、cleanup 失敗時の rollback、join conflict 解消 agent の制約、stdout/stderr のエラー出力境界を検証する。
- 同じ branch/state fixture を共有する session 状態遷移の外部挙動を一箇所で追うためのテスト群であり、session CLI の完了系・失敗系・競合解消系を横断して確認する入口になる。

## Read this when
- session fork、session join、session abandon の CLI 外部挙動を変更または調査するとき。
- session state file の active、joined、abandoned への遷移、session_home_branch、session_start_commit、joined_at、apply state の扱いを確認するとき。
- session branch の作成、削除、削除失敗時の警告、session-id 衝突時の retry や既存 state 保護を確認するとき。
- linked worktree 上での session 操作、root worktree と linked worktree の branch 状態、preprocess 実行順を確認するとき。
- session join の conflict 解消 agent 呼び出し、oracle conflict write profile、conflict marker 検出、conflict 解消以外の差分拒否を確認するとき。
- session CLI の失敗時にエラーレポートが stdout と stderr のどちらへ出るかを確認するとき。
- dirty worktree、壊れた session state、home branch 不在、cleanup 失敗などの session 操作の拒否・rollback 挙動を確認するとき。

## Do not read this when
- session 以外のサブコマンドや一般的な CLI runner の挙動だけを調べたいとき。
- session の内部 helper 単体の小さなロジックだけを確認したい場合で、より直接その実装ファイルまたは単体テストを読めば足りるとき。
- apply、doctor、config、prompt、runtime profile などの session 状態遷移に直接関係しない仕様や実装を調べたいとき。
- git 操作 wrapper や test support fixture の一般挙動だけを確認したいとき。

## hash
- dca4c6c64bcae0959b99b46315d69513236de3961353043461887a5b767498d6

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
