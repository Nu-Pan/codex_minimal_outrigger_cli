# `_support.py`

## Summary
- cmoc の realization test から共有されるテスト支援モジュール。最小 Git リポジトリ、Codex home、Codex 実行パラメータ、fake Codex profile、fake Ollama/systemctl 環境、doctor/init 実行、apply worktree 解決など、CLI・runtime 系テストの共通 fixture/helper をまとめている。

## Read this when
- テスト内で Git リポジトリや tracked oracle file を作る既存 helper を使いたいとき。
- Codex CLI 実行、profile 生成、Codex home、AgentCallParameter に関するテスト支援処理を確認・変更するとき。
- doctor/init や managed Ollama/systemctl を伴うテストの fake 外部コマンド環境を確認・変更するとき。
- session state から apply worktree を解決するテスト helper を探すとき。

## Do not read this when
- 個別コマンドの期待挙動や assertion を確認したいだけなら、該当するテストファイルを直接読む。
- 本番実装の Git 操作、Codex 実行、Ollama 管理、apply worktree 解決を変更したい場合は、src 側の該当モジュールを読む。
- oracle file の正本仕様や開発ルールを確認したい場合は、oracle 配下の該当文書を読む。

## hash
- 5e196edd21cf742a57e6103709833292de810b3e53516c437704cae8d6f0ebc5

# `test_acp_builder_parameters.py`

## Summary
- ACP builder が生成する agent call parameter、prompt に埋め込む root 表記、structured output schema 参照、公開 export 境界を検証する realization test。
- apply fork、TUI parameter resolve、index entry、review oracle、session join conflict resolution など、複数 builder の互換性と正本 schema 追従を横断的に確認する。

## Read this when
- ACP builder の model class、reasoning effort、file access mode、preflight 実行有無、schema path の期待値を変更する。
- builder prompt に含める `<repo-root>`、`<work-root>`、`<oracle-root>` などの placeholder 表記や、動的入力文字列の保持挙動を変更する。
- oracle 側 structured output schema と realization builder が参照する schema の一致を確認したい。
- builder module の `__all__` や互換 module が外部へ公開する名前を変更する。
- apply fork、TUI resolve parameter、indexing index entry、review oracle finding、session conflict resolution の既存外部挙動に影響する変更を行う。

## Do not read this when
- 個別 builder の実装詳細だけを調べる場合は、対応する implementation へ直接進めばよい。
- oracle schema の内容そのものを編集・確認する場合は、oracle 側の schema 定義を読む。
- ACP の基礎型や enum の定義だけを確認したい場合は、基礎型を定義する implementation を読む。
- INDEX.md エントリー生成の出力文面だけを調整する場合は、indexing 用 builder またはその schema を優先して読む。

## hash
- cf91f4a5e1b2deb5113e2f191407d273f16c7acb9c633c5305dac69b150efa93

# `test_apply_abandon_cli.py`

## Summary
- apply abandon が active apply run を破棄する外部挙動を CLI 経由で検証するテスト。apply worktree、apply branch、session state、process id file の cleanup と warning 表示、running apply process / child process group の停止処理、linked session worktree や apply worktree から実行した場合の境界条件を扱う。
- ファイル自体が 16,000 文字を超える理由として、apply abandon の成功・警告・失敗条件が同じ state fixture と境界条件を共有するため、分割せず一箇所で読む設計意図も本文冒頭で説明している。

## Read this when
- apply abandon の CLI 挙動、出力、終了コード、state 遷移、worktree/branch 削除を変更または検証するとき。
- running apply run の abandon 時に、親 apply process、Codex child process group、pid file、PID reuse、終了済み process、tracking lock をどう扱うか確認するとき。
- apply abandon を apply worktree 内、linked session worktree、linked apply worktree、stale apply branch から実行した場合の境界条件を確認するとき。
- apply abandon の失敗時に cleanup 対象を残すべき条件、または cleanup 対象が欠落している場合に warning として成功扱いにする条件を確認するとき。

## Do not read this when
- apply abandon 以外の apply subcommand、session fork、init などの通常挙動だけを確認したいとき。
- CLI 経由ではなく、process utility や runtime helper の単体仕様だけを広く確認したいとき。ただし apply abandon の running cleanup と関係する process 停止条件はこのファイルが入口になる。
- oracle 側の realization file サイズ基準やコメント基準そのものを確認したいとき。本文冒頭の根拠 path ではなく、対応する oracle file を直接読む。

## hash
- 361497a57d52cb6b226af2519632aac1d473777ec5f21e9956b34a27da4f2009

# `test_apply_fork_cli.py`

## Summary
- apply fork CLI の外部挙動を、共有 fixture を使って回帰確認するテスト群。Codex loop 実行、apply run の state/worktree 更新、linked worktree 起点、doctor preflight、設定読み込み失敗時の停止、gitignore 編集、target normalization、report 前の completed 書き込みを同じ CLI 境界から検証する。
- 16,000 文字超のまま維持する根拠を持つテスト文脈であり、target normalization、doctor preflight、config failure、state updates、gitignore handling を分割せず同じ apply fork 境界と repository fixture で観測する。

## Read this when
- apply fork の CLI 実行が Codex 呼び出し後に state、apply branch、worktree、process pid 周辺をどう更新するか確認・変更する。
- apply fork が linked worktree の session branch と HEAD を起点に apply run を開始する挙動を確認・変更する。
- apply fork 本体前の doctor preprocess、特に .cmoc/local ignore 修復と clean worktree 維持を確認・変更する。
- cmoc config の破損または欠落時に apply run の branch/state を開始しない失敗挙動を確認・変更する。
- apply fork の対象列挙や target normalization で、root 直下 memo、管理領域、INDEX/AGENTS、.cmoc/local、binary、tracked ignored file、oracle 配下 symlink をどう扱うか確認・変更する。
- apply fork が .gitignore を所見対象として扱い、apply branch 側で編集できることを確認・変更する。
- apply loop 正常完了後、report 生成前に state file へ completed を書く順序を確認・変更する。

## Do not read this when
- apply fork 以外の apply サブコマンドや session 操作だけを調べたい。
- Codex CLI や LLM 出力品質そのものの検証を調べたい。
- 単体 helper の内部実装だけを確認したく、CLI 境界・repository fixture・state/worktree 副作用を伴う外部挙動が関係しない。
- oracle 文書や oracle src の正本仕様内容そのものを確認したい。

## hash
- 15368877c84664bd5f05d87ce401b558c7e606399675c6eed7a0b083526b2746

# `test_apply_fork_report_cli.py`

## Summary
- apply fork の CLI 経由の挙動を、所見列挙、所見適用、commit、変更要約、report 生成、session state 更新まで一体で検証するテスト。
- apply fork report の収束、未収束、error、変更ファイル再調査、rolling fork、change summary builder import、schema 参照、禁止領域を書いた場合の扱いを同じ制御ループと report schema の観測結果として扱う。
- 16,000 文字を超えるが、apply fork report の期待値と再検査制御の文脈を一箇所に保つため、責務境界は apply fork report CLI 検証に閉じている。

## Read this when
- `apply fork` の report 出力、終了コード、収束・未収束・error の判定、所見数推移、変更内容要約の期待値を確認または変更するとき。
- apply fork が所見適用後に変更ファイルを再調査する制御、新規ディレクトリ配下の展開、差分なし適用時の未収束扱いを確認または変更するとき。
- apply fork の change summary が未追跡 file、削除済み tracked file、未 commit 差分、Codex 空要約時の fallback をどう扱うか確認または変更するとき。
- apply fork builder の import 可能性、prompt に含める standard 文書、structured output schema path を検証するテストを探すとき。
- rolling apply fork が前回 apply join 後の oracle 変更だけを対象にする session state 連携を確認または変更するとき。

## Do not read this when
- apply fork の CLI 実装本体や report 生成ロジックを変更したいだけで、テスト期待値ではなく実装の入口を探しているとき。
- apply fork 以外の apply/join/session コマンドや一般的な repository 初期化 helper の挙動を確認したいとき。
- Codex CLI や agent call の低レベル実行処理そのものを確認したいとき。
- INDEX.md 生成規則、oracle/realization の一般標準、path placeholder の定義だけを確認したいとき。

## hash
- 6e0a2ce4c0258715d4b8d46c5e8f37f76511ea51437015c353ecf43d1132f87f

# `test_apply_join_cli.py`

## Summary
- apply run を session に join する CLI 外部挙動を検証する realization test。結合成功時の worktree/branch cleanup、state 更新、report 生成と、dirty worktree、stale branch、想定外差分、merge conflict などの拒否・復旧条件を同じ join 操作の境界条件として扱う。

## Read this when
- apply join の成功時に apply worktree や apply branch が削除される条件、または現在の作業場所によって cleanup が残る条件を確認したいとき。
- apply join 後の session state、last joined oracle snapshot commit、report 出力の期待挙動を確認したいとき。
- apply join が dirty worktree、stale apply branch、想定外差分、merge conflict をどう検出し、通常実行と force resolve でどう振る舞うかを確認したいとき。
- realization file として許容される apply 側変更、session 側変更、ignored tracked path、delete、rename target、root memo、oracle symlink などの分類ロジックをテスト観点から確認したいとき。
- apply join のテストを追加・整理する際に、同じ fixture と git 状態を共有する既存ケースへ統合できるか判断したいとき。

## Do not read this when
- apply fork や session fork の単独挙動を調べたいだけで、join 後の結合・cleanup・異常検出に関心がないとき。
- apply join の実装詳細を先に変更したいとき。この対象は外部挙動のテストであり、実装責務の入口ではない。
- oracle file の編集方針や正本仕様そのものを確認したいとき。この対象は realization test であり、正本仕様ではない。

## hash
- 9e784f57d7f6b5c401012741e163966a9c7c9b553abe01b18419b4d5333433bc

# `test_basic_runtime.py`

## Summary
- cmoc の基礎 runtime 契約を横断的に検証するテスト群。root placeholder と worktree 解決、config の既定値・復元・不正値拒否、CmocError の Markdown 表示、CLI error の stdout 出力、subcommand log、FileAccessMode から Codex sandbox/profile への変換、binary 判定など、個別サブコマンドより下位の共通実行前提を扱う。
- 共通 fixture と root 状態を同じ文脈で読む必要がある runtime 回帰テストとしてまとまっており、複数のサブコマンドや runtime helper が共有する境界条件の変更時の入口になる。

## Read this when
- root 解決、repo root と linked worktree、run/work root placeholder、worktree 作成・削除の安全条件を変更または確認するとき。
- cmoc config の既定値、JSON 変換順、不正値検証、欠落時の CmocError を変更または確認するとき。
- CmocError の report 形式、CLI parse error、想定済み CLI error、preflight 失敗、doctor preprocess、completion probe、subcommand log の挙動を変更または確認するとき。
- FileAccessMode、Codex profile、sandbox writable roots、extra writable/read path、oracle conflict write、local SLM provider 設定の境界を変更または確認するとき。
- binary 判定、duration 表示、gitignore 更新、テスト用 repo 作成 helper の runtime 前提を変更または確認するとき。

## Do not read this when
- 個別サブコマンドの業務ロジックだけを確認したい場合は、そのサブコマンドを直接検証するテストや実装へ進む。
- oracle file の正本仕様そのものを確認したい場合は、対応する oracle doc または oracle src を読む。
- UI 表示、LLM 出力品質、生成内容の意味評価など、基礎 runtime 契約ではない領域を調べる場合は対象外。
- 単一 helper の内部実装だけを局所的に変更し、root 状態・CLI wrapper・profile・config などの共通 runtime 境界に影響しないことが明らかな場合は、より近い実装ファイルと狭いテストを優先する。

## hash
- 62e892f5a46177a48411cfe9f3209361c87d83e512f7a46bd4438f0510400a2d

# `test_cli_tui.py`

## Summary
- TUI サブコマンド起動直前の CLI 前処理を検証する realization test。エディタで作成した依頼文の整形、パラメータ解決用 Codex exec 呼び出し、TUI 用 Codex 呼び出し、生成プロンプト保存、`.cmoc/local` ログ配置、gitignore 反映、リンク worktree 上での root/cwd/schema/log の扱いを外部挙動として確認する。

## Read this when
- TUI サブコマンドの起動前処理、依頼文テンプレート編集、完了プロンプト生成、`launch_tui.json` や `resolve_parameter.json` の選択、file access mode 解決に関するテストを確認・変更したいとき。
- リンク worktree で `tui` を実行した場合に、ログや schema をどの worktree 配下へ置くか、Codex 呼び出しへ渡す `root`・`cwd`・`extra_read_paths` がどう検証されているかを確認したいとき。
- `.cmoc/local` の無視設定、TUI ログ、sub_command ログの生成場所が CLI 実行後に git 追跡対象外として扱われることを確認したいとき。

## Do not read this when
- TUI 内部の画面操作や対話 UI そのものを調べたいとき。この対象は TUI 起動前の CLI 側処理と Codex 呼び出し境界を検証している。
- TUI 以外のサブコマンド、共通ランタイム、または git worktree 操作の一般仕様だけを確認したいとき。より直接の実装または対応するテストを読む方がよい。
- oracle file の正本仕様を確認したいとき。この対象は realization test であり、正本仕様断片ではない。

## hash
- 108810a6a73d65b528b8eedfa8b0132a62f06394c906c075e5572579e029b5bf

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
- Codex CLI 実行ラッパーの実テスト群。プロファイル生成、作業ディレクトリ指定、sandbox writable roots、schema 保存先、linked worktree からの実行、cmoc 管理 Ollama provider 設定、実 Codex CLI 呼び出し時の記録内容を検証する。
- 外部 Codex 実行を fake executable で記録するケースと、実 Codex CLI が存在する場合だけ実 provider 設定を通すケースを含み、runtime 実行処理の引数・環境・生成ファイル・戻り値の境界を確認する。

## Read this when
- Codex CLI を起動する runtime 実装、特に実行引数、stdin、output-last-message、profile、sandbox、working directory の組み立てを変更する時。
- FileAccessMode ごとの writable roots や PURE_ORACLE_READ の扱い、repo write 時に許可される書き込み先を検証したい時。
- cmoc 管理 Ollama provider、local SLM model、Codex profile TOML の model_provider や model_providers 設定を変更する時。
- linked worktree からの実行で、schema state や extra read path がどの root に基づいて扱われるべきかを確認する時。
- Codex 実行ログ、profile path、schema path、prompt log path など、run_codex_exec の結果オブジェクトと副作用の整合を確認する時。

## Do not read this when
- AgentCallParameter や ModelClass などの基本データ構造そのものの仕様を確認したいだけの時。
- Codex 以外の runtime backend、または一般的な設定読み込み処理だけを変更する時。
- LLM の応答品質や生成内容の妥当性を検証したい時。このテストは provider と実行制御を対象にしており、モデル出力品質は対象外。
- oracle 文書や oracle src の正本仕様を調べたい時。ここは realization test であり、正本仕様の入口ではない。

## hash
- 88bab42685d28059de30433904ff3c977ebbe9aa03354c82a27b2b1d7e4c2bbd

# `test_codex_runtime_exec_post_validation_forbidden.py`

## Summary
- Codex CLI 実行後に、実行中の forbidden file access 差分を事後検証で拒否しないことを検証するテスト群。oracle 配下、.git 配下、引用符や空白を含む oracle path、README.md、既存の forbidden 差分、session join conflict 対象を扱い、schema retry や非ゼロ終了時の挙動も確認する。

## Read this when
- Codex CLI 呼び出し後の file access post validation の有無や対象範囲を変更する時。
- run_codex_exec が forbidden path への書き込みを見つけた時に再試行・失敗・巻き戻しを行うべきかを確認する時。
- schema validation retry、非ゼロ終了、allow_oracle_conflict_writes、extra_writable_paths と forbidden diff の関係を調べる時。

## Do not read this when
- Codex CLI に渡す引数、環境変数、sandbox 設定の組み立てだけを調べる時。
- file access rule の定義や path 分類そのものを調べる時。
- Codex CLI の stdout event parsing や output-last-message 読み取りだけを変更する時。

## hash
- 16d397a8bbb52f49de8c29f5076e936a4e0c0988c7ed16192e028fc7ab817581

# `test_codex_runtime_exec_post_validation_runtime.py`

## Summary
- Codex 実行後のファイル差分検証で、無視対象・一時キャッシュ・仮想環境・cmoc ログ・制限ディレクトリ内の許容差分が再試行や失敗扱いにならないことを確認するテスト群。
- 擬似 codex 実行ファイルで実行後差分を作り、FileAccessMode ごとの post validation と sandbox profile の writable_roots 境界を検証する。

## Read this when
- run_codex_exec の実行後ファイルアクセス検証、差分許容条件、または FileAccessMode ごとの扱いを変更する時。
- git ignore された成果物、一時キャッシュ、.venv、.cmoc/local ログ、memo・.agents・.codex・.git 配下の実行時生成物を許容する条件を確認したい時。
- Codex 用 sandbox profile が .agents を writable_roots に含めないことを検証するテストを探す時。

## Do not read this when
- Codex 実行プロセスの起動引数、出力 JSON、イベント処理そのものの正常系・異常系を確認したいだけの時。
- ファイルアクセスモードの定義やパス分類ロジックの実装を確認したい時。
- oracle file と realization file の概念仕様やルーティング文書生成規則を確認したい時。

## hash
- 115e61bbe3bbe1d58835956060b0cc8d9f36b126b18d47c2627f5e5f196ac905

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
- Codex exec が quota exceeded で失敗した後の待機、probe、resume、再実行の外部挙動を検証する realization test。
- probe の共有、resume token 抽出、call log/subcommand log、CODEX_HOME と cwd、失敗時の post validation 抑制を、同じ quota retry 状態機械の観測点として扱う。

## Read this when
- Codex exec の quota retry、quota availability probe、resume token、quota 回復後の再実行に関する挙動を確認または変更するとき。
- quota 待機中の call log、subcommand log、stdout/prompt/output jsonl、profile、CODEX_HOME、cwd の扱いを検証するとき。
- 複数の Codex exec が同時に quota exceeded になった場合の代表 probe 共有、待機呼び出しの復帰、probe 失敗時の全体失敗を確認するとき。
- quota exceeded 後に file access violation の post validation を走らせない制御を確認するとき。

## Do not read this when
- 通常成功する Codex exec の基本 argv 組み立てや出力 JSON 読み取りだけを確認したいとき。
- quota retry と関係しない runtime error、設定読み込み、リポジトリ作成用 test support を調べたいとき。
- oracle 側の quota probe parameter builder の正本仕様そのものを確認したいとき。

## hash
- 40cac26d5ac7cb13510265cf9857c3a023f8c002d291ad7d97de20341a8ae81c

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 実行ラッパーの再試行制御を検証する realization test。構造化出力の schema 不一致、出力ファイル欠落・空・JSON 破損、モデル capacity、quota/capacity 文言の検出範囲、再試行時の call log と subcommand log の外部挙動を扱う。

## Read this when
- Codex CLI 呼び出しの retry 条件、成功判定、失敗詳細、call log 記録、subcommand log イベントを変更または調査する時。
- 構造化出力の parse/schema validation 失敗後に再試行する挙動、または capacity retry 中の file access post validation の扱いを確認する時。
- stdout JSONL の error event と、stderr や通常 stdout に出た同一文言を区別する挙動を確認する時。

## Do not read this when
- Codex CLI の通常起動引数、sandbox 設定、prompt 組み立てだけを確認したい時。
- agent call parameter や設定値のデータ構造そのものを調べたい時。
- retry を伴わない単純なログ出力やリポジトリ fixture の作成方法だけを確認したい時。

## hash
- 118abe8694a4f2e5aa72946ec6b81d5fe4b3dd16e53c0fc49afa13326f3907f5

# `test_codex_runtime_subprocess.py`

## Summary
- Codex subprocess 起動時の apply process tracking の扱いを検証する realization test。専用 process group の記録、既存 tracking file の保持、継承された tracking 環境変数を通常の Codex 実行から除外する挙動を扱う。

## Read this when
- Codex subprocess 実行 helper の process group 分離や apply process tracking の挙動を変更・確認するとき。
- `run_tracked_codex_subprocess` または `run_codex_subprocess` が tracking file や tracking 環境変数をどう扱うべきかをテストから確認したいとき。
- Codex 実行時に外部から継承された apply tracking 設定で不要な状態ファイルが作られないことを確認したいとき。

## Do not read this when
- Codex subprocess 以外の CLI コマンド挙動や出力形式を調べたいとき。
- apply process tracking と無関係な runtime profile の設定・探索・環境構築を確認したいとき。
- 実装側の helper 責務や内部処理を確認したいだけなら、対応する runtime profile 実装を直接読む。

## hash
- ad80da3fef78c45fa133633666d9a2d60df6a2244d07c1a849846adadb2e363b

# `test_codex_runtime_tui.py`

## Summary
- Codex TUI 起動処理のテスト群。追加 read path の許可判定、complete prompt の扱い、linked worktree での作業ディレクトリと writable roots、Codex CLI 異常終了時のエラー表示と呼び出しログを検証する。
- 実際の Codex CLI は一時実行ファイルで差し替え、起動引数、cwd、profile、ログ内容など外部挙動を確認する。

## Read this when
- Codex TUI 呼び出し処理、特に `run_codex_tui` の引数構築、cwd、profile、sandbox writable roots、呼び出しログを変更する時。
- TUI 実行前の追加 read path 検証や、`memo` 配下を許可領域外として拒否する挙動を確認する時。
- pure oracle read や repo write の file access mode ごとに、complete prompt を extra read path として扱う条件を確認する時。
- Codex CLI が非 0 終了した場合の `CmocError`、コンソール出力、tui call log の期待挙動を確認する時。

## Do not read this when
- Codex TUI ではなく非対話的な Codex 実行、agent call、または別 CLI サブコマンドの挙動だけを確認したい時。
- file access mode の定義そのもの、path model、設定値の正本仕様を確認したい時。
- Git worktree の一般操作やリポジトリ生成 helper の実装を調べたい時。
- TUI 呼び出しの外部挙動ではなく、Codex CLI や LLM の出力品質そのものを検証したい時。

## hash
- 21420e8f441b2b53bdfaa328d0e7bd3f8045bf0c9c77f24b55794b12cdb78a4d

# `test_doctor_cli.py`

## Summary
- doctor/init 系 CLI の外部挙動を検証する realization test。git 修復、`.cmoc/local` の ignore/untrack、`.agents` 追跡、設定生成・同期、managed Ollama の導入・検証、local SLM 用 Codex profile 準備時の doctor 起動を扱う。
- 既存の staged/unstaged 変更や rename を壊さずに修復コミットを作ること、設定ファイルだけを追跡対象にし local cache を追跡しないことなど、git 状態を伴う doctor 前処理の回帰確認への入口になる。

## Read this when
- doctor または init の CLI 挙動、別名コマンド、標準出力、設定生成・既存設定との同期を変更する。
- doctor 前処理が `.gitignore`、`.agents`、`.cmoc/config.json`、`.cmoc/local`、linked worktree、既存の staged/unstaged 変更に与える影響を確認する。
- managed Ollama の install/service/model pull/port listener 検証や、cmoc provider model の重複排除 pull を変更する。
- local SLM 用 Codex profile 生成時に doctor が起動される条件や、managed Ollama profile 内容を変更する。

## Do not read this when
- agent call parameter や model enum の純粋なデータ構造だけを確認したい場合は、該当する実装または単体テストへ進む。
- doctor/init 以外のサブコマンド、通常の agent 実行、apply fork、出力 schema の挙動を調べる場合は、より直接その領域のテストへ進む。
- Ollama service の実プロセス制御全体を読む必要があり、このテストで monkeypatch されている境界だけでは足りない場合は、runtime 側の実装へ進む。

## hash
- ba18c8937621798507df273e723a6fa469c1c258e63a28a0cc2638233a8c41af

# `test_indexing_cli.py`

## Summary
- INDEX.md 生成・更新の CLI 回帰テストを扱う。Codex によるエントリー生成、fresh hash による再生成スキップ、不正エントリー再生成、空ディレクトリ、兄弟順序、並列生成、memo 除外、symlink cycle 除外を検証する。
- indexing 実行時の git 境界を扱う。clean/dirty worktree、linked worktree、apply worktree preflight、INDEX.md だけを commit する条件、INDEX.md conflict 解決の外部挙動を確認する。

## Read this when
- indexing サブコマンド、indexing preflight、または INDEX.md 更新ワークフローの CLI から見える挙動を変更・確認する時。
- INDEX.md の対象列挙、hash 再利用、エントリー schema 検証、render 順、並列更新、memo や symlink の扱いを調べる時。
- indexing による commit 対象、dirty worktree 拒否、linked worktree での実行、merge conflict 解決の回帰を確認する時。

## Do not read this when
- INDEX.md エントリー文面の生成指示そのものや Structured Output schema の定義だけを確認したい時。
- routing document 更新とは関係しない CLI サブコマンド、apply join の通常処理、または runtime 設定の一般的な読み書きを調べる時。
- 個別 helper の内部実装だけを変更し、indexing CLI から観測される git 状態・生成結果・commit 条件に影響しない時。

## hash
- b84e14c35db19fa57f4f3932aff74fd4e0bb8525dcf28ec71a3929a4447ffadd

# `test_indexing_preflight.py`

## Summary
- Codex 実行前に INDEX.md 更新 preflight が走ることを検証する realization test。exec/TUI 呼び出し、cwd が別 worktree を指す場合の更新対象、repository lock 待機、parameter による preflight 無効化、file access violation 後に recovery 用の追加 indexing が走らないことを扱う。

## Read this when
- Codex 呼び出し前の indexing preflight の実行順、対象 root/worktree、commit 後の作業ツリー状態を変更・確認したいとき。
- indexing preflight の lock 待機、無効化フラグ、file access violation 時の再実行抑制に関するテストを確認したいとき。
- runtime Codex wrapper と indexing_module.update_indexes の連携を mock した制御ロジックのテストを探しているとき。

## Do not read this when
- INDEX.md エントリー生成ロジック自体や対象ファイル走査ルールを確認したいだけなら、indexing 実装や専用テストへ進む。
- Codex 実行バイナリの引数組み立て、モデル設定、ACP 値そのものを確認したいだけなら、runtime Codex 実装や basic/config 側へ進む。
- 通常のリポジトリ作成 helper、git helper、Codex home setup helper の詳細を確認したいだけなら、テスト支援モジュールへ進む。

## hash
- 3acf23fa47098ab15a3be7f2e5aee79bf66f091be6fd7808f39b0c1e0f9f0f73

# `test_packaged_import.py`

## Summary
- packaged layout だけを PYTHONPATH に置いた subprocess 上で、realization implementation と oracle src の import 境界が成立することを検証する realization test。pyproject の oracle package 設定、review oracle enumerate builder、basic builder の canonical reexport、config reexport の公開範囲を確認する。

## Read this when
- packaged layout、PYTHONPATH、setuptools package-dir/packages 設定に関わる変更を行うとき。
- oracle src を realization implementation から import・reexport する境界を変更するとき。
- review oracle enumerate builder、acp.builder.basic、config.cmoc_config の import 互換性や公開名を変更するとき。

## Do not read this when
- 通常の CLI 実行フローやコマンド引数の挙動だけを確認したいとき。
- oracle doc の自然言語仕様や prompt 文面そのものを確認したいとき。
- パッケージ配置や import 境界に関係しない単体ロジックのテストを探しているとき。

## hash
- 484451aa5216148342d78d9c4c971994fc8e33e9de194a997d6b2fc605432142

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
- review oracle の CLI 外部挙動を検証する realization test。eval-oracle から review oracle への委譲、review report の構成・件数・所見表示、scope ごとの oracle file 選択、fake Codex 応答を使った enumerate/validate/judge/merge loop、review 用 worktree と join commit、INDEX.md 差分の取り込みや競合解決、処理失敗時 report、INDEX.md 以外の差分拒否を扱う。
- oracle review run の状態、report 文脈、fake Codex 応答を共有するテスト群であり、対象 oracle の列挙から所見評価 loop と report 生成までの統合的な挙動確認の入口になる。

## Read this when
- review oracle コマンド、eval-oracle コマンド、または review oracle の report 出力形式を変更する。
- oracle file のレビュー対象列挙、full/session scope、tracked ignored file、symlink、AGENTS.md/INDEX.md 除外の挙動を確認・変更する。
- review oracle の enumerate、validate challenger/advocate、judge、merge の loop 制御、semantic merge retry、finding id 付与、accepted/rejected findings の扱いを変更する。
- review oracle 実行時の worktree、session branch、review fork/join commit、INDEX.md 差分の merge、preflight indexing、index conflict 解決、非 INDEX.md 差分拒否を調べる。
- review oracle が途中失敗した場合の error report、stdout/stderr、未判定 finding の表示抑制を確認する。

## Do not read this when
- oracle review のプロンプト文面や Structured Output schema 自体だけを変更したい場合。
- review oracle 以外の review サブコマンド、一般的な session 操作、または Codex 実行ラッパー単体の挙動だけを調べる場合。
- INDEX.md エントリー生成ロジックや汎用 indexing 実装だけを確認したい場合。
- 個別 helper の純粋な単体挙動だけを確認でき、CLI 実行、report 生成、review loop、worktree 状態を読む必要がない場合。

## hash
- 4f3dff08d747dae176842029472ee2665c769b54f148915ad124958afa572b49

# `test_session_cli.py`

## Summary
- session の fork、join、abandon をまたぐ CLI 回帰テストをまとめる。session branch と session state のライフサイクルを軸に、linked worktree、state cleanup、dirty worktree 拒否、join 時の conflict 解消と失敗報告の外部挙動を検証する。
- session 状態遷移に関わる branch 操作、状態ファイル更新、出力先、cleanup 失敗時の rollback、preprocess の副作用を同じ fixture 文脈で確認するためのテスト群である。

## Read this when
- session fork、join、abandon の CLI 外部挙動を変更する。
- session branch の作成・削除、home branch への復帰、session state file の state や field 更新を確認する。
- linked worktree 上での session 操作、preprocess、dirty worktree 拒否、cleanup 失敗時の rollback を扱う。
- join の conflict 解消 agent 呼び出し、oracle conflict 書き込み権限、conflict marker 検出、非 conflict 差分拒否、エラー出力先を変更する。

## Do not read this when
- session CLI 以外のサブコマンドや、session 状態遷移と無関係な共通処理だけを確認する。
- 個別 helper の単体仕様だけを確認したい場合で、より直接の実装または小さな単体テストがある。
- oracle や realization の文書ルールを確認したいだけで、session fork/join/abandon の実行時挙動を扱わない。

## hash
- 61e95962407c18a30d25cbd2feb06270648c53bcf239671c73bbe7416de48d25

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
