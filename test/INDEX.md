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
- apply fork の CLI 挙動と対象正規化を検証する pytest 群。Codex 実行を fake 化し、session fork 後の apply run 完了、state 更新、worktree/branch 作成、doctor preprocess、設定読み込み失敗、.gitignore 編集、対象 path の除外・保持条件を確認する。

## Read this when
- apply fork の外部挙動、状態遷移、作業ブランチ・worktree の作成規則を変更または確認したいとき。
- apply fork が Codex loop、所見列挙、所見適用、report 生成とどう接続されるべきかをテスト側から確認したいとき。
- apply fork 実行前の doctor preprocess、.cmoc/local ignore 追加、clean worktree 維持、設定ファイル読み込み失敗時の中断挙動を扱うとき。
- apply 対象の正規化で、root 直下 memo、oracle、.gitignore、.cmoc/local、AGENTS.md、INDEX.md、tracked ignored file、binary file、symlink をどう扱うか確認したいとき。

## Do not read this when
- apply fork の内部実装手順そのものを読みたいだけなら、実装側の apply fork 本体へ進む。
- apply 以外の session fork、doctor、config、report の単体仕様や実装だけを調べたいときは、それぞれの直接の実装またはテストへ進む。
- Codex 実行品質や LLM 出力内容そのものを検証したいとき。この対象は Codex 実行を fake 化し、cmoc 側の制御と副作用を検証する。

## hash
- 497cbb0513213e9ef27deccaef4af3a1ab3de15385ed917f69937a8c90c7f2d2

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
- cmoc の共通 runtime 契約を横断して検証する realization test。root placeholder と worktree 判定、config 読み書き、CmocError 表示、CLI preflight と parse error、subcommand log、FileAccessMode から Codex sandbox profile への変換、binary 判定など、個別サブコマンドより下の実行前提をまとめて扱う。
- 複数領域にまたがるが、共通 fixture と root 状態を共有する basic runtime 回帰として凝集させており、分割しない根拠も本文冒頭で説明している。

## Read this when
- root 解決、repo root と linked worktree、run/work root placeholder の挙動を変更・調査する時。
- CmocError、CLI error report、Click parse error、doctor preprocess、pre-log check、subcommand log の外部挙動を変更・調査する時。
- cmoc config の既定値、JSON 化順序、読み込み失敗、型検証、Codex model spec や reasoning effort の扱いを変更・調査する時。
- FileAccessMode、Codex sandbox profile、追加書き込み許可 path、oracle・realization・repo write 境界、linked worktree からの repo local read 許可を変更・調査する時。
- `.cmoc/local` ignore 追加、managed worktree 作成・削除保護、branch session id 解析、binary 判定、起動 wrapper の missing venv report を変更・調査する時。

## Do not read this when
- 個別サブコマンド固有の業務ロジック、出力内容、状態遷移だけを確認したい時は、そのサブコマンドの test または実装へ進む。
- oracle 文書や oracle src の正本仕様そのものを確認したい時は、対応する oracle file を読む。
- routing 文書や INDEX.md エントリー生成規則だけを確認したい時は、routing・indexing 系の文書または test を読む。
- LLM 出力品質、prompt 文面そのもの、agent call の高水準 orchestration だけを確認したい時は、runtime 境界より直接の対象へ進む。

## hash
- da13c497f268e5fdc7eb45fc05c7dcde49c0f5e230863b883277c12a7a7306b3

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
- Codex CLI 実行ラッパーのテスト群。プロファイル生成、作業ディレクトリ、sandbox writable roots、schema 保存場所、managed Ollama provider 設定、実 Codex CLI 呼び出し時の記録内容を検証する。
- fake executable と一時 git repo を使い、外部コマンド起動時の argv、stdin、cwd、出力、生成ファイル、設定ファイル内容が期待どおりになることを確認する。

## Read this when
- Codex CLI を起動する実装、実行プロファイル生成、sandbox 設定、writable roots、output schema の保存先、linked worktree での cwd と root の扱いを変更するとき。
- managed Ollama provider や local SLM 用の model_provider 設定、Codex CLI へ渡す引数、builtin Ollama flags を使わない挙動を確認するとき。
- agent call 実行結果のログ、prompt 入力、last message 出力、実 Codex CLI 連携のテスト方針を確認するとき。

## Do not read this when
- Codex CLI 起動やプロファイル生成に関係しない設定読み込み、path model、通常の CLI サブコマンド挙動だけを調べるとき。
- oracle 文書、INDEX 生成、リポジトリ構造定義など、agent 実行ラッパーの外部挙動に触れない仕様や実装を扱うとき。
- テスト支援関数そのものの実装や fixture 作成方法を変更する場合で、まず共通テストサポートを直接読む方が適切なとき。

## hash
- 31f3f37fbbe16f44a4d5fdee0590a60438e9c15aea87efe2b56ba422a86fbe85

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
- Codex exec が quota exceeded で失敗した後の quota availability probe、resume token 抽出、resume または再実行、call log と subcommand log、CODEX_HOME と cwd の扱いをまとめて検証する regression test。
- 並列実行時に quota probe が代表 1 回だけ共有され、probe 成功時は待機中の呼び出しが復帰し、probe 失敗時は待機中の呼び出しも失敗することを検証する。
- ファイルサイズは大きいが、quota 待機から復帰する Codex exec の同一 retry 状態機械を複数の観測点から確認するため、一箇所に集約されている。

## Read this when
- Codex exec の quota exceeded 検出後に、probe、resume、再実行のどれが行われるかを変更または確認するとき。
- quota availability probe の AgentCallParameter、profile、prompt、file access mode、cwd、CODEX_HOME の扱いを変更または確認するとき。
- quota retry 中の call log、stdout/jsonl/output/prompt log、subcommand log、console 表示、失敗時 status を変更または確認するとき。
- quota poll 上限、probe の非 quota 失敗、file access post validation を行わない失敗経路を変更または確認するとき。
- 複数の Codex exec が同時に quota 待機した場合の代表 probe 共有と待機呼び出しへの結果伝播を変更または確認するとき。

## Do not read this when
- 通常成功する Codex exec の引数生成、profile 生成、出力解析だけを確認したいときは、runtime 実装またはより直接の通常系テストを読む。
- quota retry と関係しない file access mode の一般的な検証や post validation の仕様を確認したいときは、その責務を持つ実装またはテストを読む。
- Codex 以外の subcommand 実行、ログ基盤そのもの、repo fixture 作成 helper の挙動だけを確認したいときは、それぞれの対象を読む。

## hash
- fbcbb71e690cd89f6efbb9b004b94953062eb0b58b59087b8b39458112b7c641

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
- Codex TUI 起動処理のテスト。追加読み取りパスの許可判定、complete prompt の扱い、linked worktree 起動時の作業ディレクトリと writable roots、Codex CLI/TUI の非ゼロ終了時のエラー表示と呼び出しログを検証する。

## Read this when
- Codex TUI 実行時の `extra_read_paths` の許可・拒否条件を確認または変更する時。
- PURE_ORACLE_READ で complete prompt を渡す場合の `--output-schema` 抑制や起動引数を確認する時。
- linked worktree から TUI を起動する時の `cwd`、`--cd`、sandbox writable roots の挙動を確認する時。
- Codex CLI/TUI が非ゼロ終了した時の `CmocError`、コンソール出力、codex 呼び出しログを確認する時。

## Do not read this when
- Codex TUI ではなく Codex API 呼び出しや通常の非対話実行の挙動を確認したい時。
- ACP のファイルアクセスモードそのものの定義や一般的な許可領域モデルを確認したい時。
- TUI 実行の実装詳細を先に確認したい時は、対応する runtime 実装を直接読む。

## hash
- 2ce3e1be542f251fe08993bd60fc3ab97ab68e28680f466bf3763e5a0411fb47

# `test_doctor_cli.py`

## Summary
- CLI の初期化・doctor 前処理・管理 Ollama 連携を外部挙動として検証するテスト群。設定ファイル生成と既存値保持、gitignore と追跡状態の修復、preexisting staged/unstaged 変更の保全、worktree 対象選択、doctor 別名、Codex profile 準備時の doctor 起動を扱う。
- Ollama サービスについては、systemd user service の生成内容、管理バイナリと models ディレクトリの配置、サービス PID と listener process の照合、cmoc provider model の重複排除 pull を検証する。

## Read this when
- doctor または init コマンドの利用者向け挙動、生成される設定、git 追跡・ignore 修復、修復 commit の対象範囲を変更・確認したいとき。
- 管理 Ollama のインストール、systemd service 生成、サービス検証、listener 照合、cmoc provider model pull の制御ロジックを変更・確認したいとき。
- Codex profile 準備時に local SLM 用の managed Ollama が不足している場合の自動 doctor 実行を変更・確認したいとき。
- 既存の staged 変更、unstaged hunk、rename、過去に追跡された local cache を doctor 前処理がどう保全・整理するかを検証したいとき。

## Do not read this when
- doctor/init の外部挙動ではなく、設定 schema やデフォルト値の正本定義そのものを確認したいだけのとき。
- Ollama service の内部 helper 実装だけを局所的に読めば足り、CLI 経由の統合挙動や git 状態への副作用を確認しないとき。
- agent call、apply fork、path model など doctor/init と直接関係しない領域のテストを探しているとき。

## hash
- eac9f79b06ec0e5bdecd7d97218e71b6976de00f65617f1e848276832574f357

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
- session fork/join/abandon の CLI 回帰テストをまとめる。session branch と session state のライフサイクルを軸に、状態ファイル生成、session-id 衝突、linked worktree、join conflict 解消、branch 削除、cleanup、dirty worktree 拒否、エラー出力先を検証する。
- session 系サブコマンドの外部挙動を変更する時に、session 状態遷移と git branch/worktree 操作が壊れていないか確認する入口となる。

## Read this when
- session fork が session branch と state file を作る挙動、session-id 衝突時の retry/失敗、既存 state を上書きしないことを確認したい時。
- session abandon が home branch へ戻り、session branch を削除し、state を abandoned に更新する挙動を確認したい時。
- session join が session branch の変更を home branch へ取り込み、state を joined に更新し、session branch 削除可否を報告する挙動を確認したい時。
- linked worktree 上で session fork/join/abandon を実行する挙動や、root worktree と linked worktree の branch が混線しないことを確認したい時。
- session join の conflict 解消 agent 呼び出し、oracle conflict 書き込み権限、conflict marker 検出、delete conflict 解消後の staging を確認したい時。
- session state file の破損、必須 field 欠落、home branch 欠落、cleanup 失敗、dirty worktree などの失敗時挙動と stdout/stderr の出力先を確認したい時。
- session CLI の回帰テストが大きい理由や、session branch/state fixture を一箇所で扱う意図を確認したい時。

## Do not read this when
- session 以外のサブコマンドの CLI 挙動だけを確認したい時。
- session 実装の内部 helper 単体の責務やアルゴリズムだけを確認したい時は、対応する実装ファイルを直接読む。
- doctor、apply、prompt builder など、session branch/state のライフサイクルと関係しない挙動だけを確認したい時。
- テスト支援関数や一時 git repository fixture の基本的な作りだけを確認したい時は、共通 support 側を直接読む。

## hash
- b30840a5a51aae27c33a6790eeae119d0d8e917be4ee989eebc6820e28807ffa

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
