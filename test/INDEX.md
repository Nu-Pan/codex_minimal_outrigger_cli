# `_support.py`

## Summary
- cmoc の realization test で共有される pytest 補助関数群を定義する。最小 Git リポジトリ、Codex home、fake Codex profile、fake Ollama/systemctl 環境、CLI doctor/init 実行、apply worktree 解決など、複数テストから使う外部状態と subprocess 周辺の準備を担う。

## Read this when
- CLI 実行テストで使う一時 Git リポジトリ、Codex home、AgentCallParameter、fake 外部コマンドの作り方を確認したいとき。
- doctor/init や Codex subprocess 制御のテストが参照する fake Ollama/systemctl 環境、固定テスト用 SLM model、fake service 停止処理を変更するとき。
- apply branch の state snapshot から worktree path を解決するテスト補助を確認するとき。

## Do not read this when
- 個別サブコマンドの期待挙動や assertion 本体を確認したいだけなら、そのテストファイルを直接読む。
- production 実装の Git 操作、Codex 実行、Ollama 管理、apply worktree ロジックを変更したい場合は、src 配下の対応実装を読む。
- oracle file の定義やテストルールの正本仕様を確認したい場合は、oracle 配下の該当文書を読む。

## hash
- 044b35ca5c83b73269dccfa6ace64a9a46dc6fd7c0206ba29863420ed577ee03

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
- apply fork の CLI 実行を通じて、所見列挙、所見適用、変更要約、report 出力、session state 更新、rolling fork の対象選定をまとめて検証する realization test。
- apply fork report の収束・未収束・error・変更ファイル再調査・未追跡 file・削除済み file 除外・禁止領域汚染時の非修復など、同じ制御 loop と report schema から観測される挙動を扱う。
- apply fork 用 ACP builder が src のみの PYTHONPATH や packaged layout から import でき、oracle 由来の schema と標準 prompt を参照することも検証する。

## Read this when
- apply fork の report 内容、exit code、変更要約、commit message、session state 更新の期待挙動を確認・変更する。
- apply fork が所見適用後に変更 file や新規 directory 配下を再調査し、収束または未収束を判定する制御を確認・変更する。
- apply fork の error 時 report、未 commit 差分、未追跡 file、削除済み tracked file の扱いを確認・変更する。
- apply fork 用 ACP builder の prompt、structured output schema、packaged layout での import 互換性を確認・変更する。
- rolling apply fork が前回 apply join 後の oracle 変更だけを調査対象にする挙動を確認・変更する。

## Do not read this when
- apply fork の内部実装だけを局所的に確認したい場合は、先に該当する実装側の subcommand や report helper を読む。
- apply join、session fork、config 初期化など、apply fork report の観測結果に直接関係しない CLI 挙動だけを調べる。
- Codex 実行 wrapper や runtime logging の一般挙動を調べる場合で、apply fork 固有の report・再検査制御が関係しない。
- oracle file の正本仕様を確認したい場合は、対応する oracle doc または oracle src を読む。

## hash
- da2a01e92ef01e865a3998344fd4b70902cc056ec329c50aed4968f47aba0f8e

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
- cmoc の基礎 runtime 契約を横断的に固定する realization test。root placeholder 解決、repo root と linked worktree の扱い、config 読み書き、CmocError 表示、CLI error 出力、subcommand log、FileAccessMode と Codex sandbox profile、binary 判定、worktree 作成・削除の安全条件をまとめて検証する。
- 個別サブコマンドの振る舞いではなく、複数機能の実行前提になる共通 runtime 境界の回帰を扱う入口。

## Read this when
- root 解決、work root / run root / repo root、linked worktree、または path placeholder の挙動を変更・調査するとき。
- CmocConfig、config JSON 変換、model / reasoning effort の検証、load_config の error、または既定 config を変更・調査するとき。
- CmocError、render_error、CLI parse error、stdout / stderr の error report、doctor preprocess、pre-log check、subcommand log の失敗時記録を変更・調査するとき。
- FileAccessMode、Codex profile、sandbox writable roots、extra writable / readable path、oracle conflict write、local SLM provider 設定を変更・調査するとき。
- create_run_worktree / remove_worktree の管理外 path 拒否、branch session id / apply branch session id、runtime state 読み込み条件を変更・調査するとき。
- `.cmoc/local` ignore 設定、起動 wrapper の missing venv report、binary 判定の読み取り範囲など、cmoc の基礎 runtime 前提に関わる回帰を確認するとき。

## Do not read this when
- 個別サブコマンド固有の業務ロジックや出力だけを調べる場合は、そのサブコマンドの test や実装を直接読む。
- oracle doc や oracle src の正本仕様そのものを確認したい場合は、対応する oracle file を読む。
- runtime と無関係な UI、文書、生成物、または isolated helper の単体挙動だけを扱う場合は、より直接の対象を読む。

## hash
- 717e6f5bfaf1ceca21dfd55d385c5425ccb1fc237880c37a697901142b64b19b

# `test_cli_tui.py`

## Summary
- TUI サブコマンドが起動直前に行う CLI 前処理の外部挙動を検証するテスト。エディタで入力された依頼文の整形、パラメータ解決用 Codex 呼び出し、本番 TUI 呼び出し、生成されるプロンプトログ、gitignore 更新、linked worktree での保存先と実行位置の扱いを確認する。

## Read this when
- TUI 起動前のプロンプト作成、エディタ入力、HTML コメント除去、パラメータ解決、または TUI 用 Codex 呼び出しの挙動を変更・確認する場合。
- TUI の file access mode 解決で空値を既定値に戻す挙動を確認する場合。
- linked worktree から TUI を起動したときに、ログ・schema・追加 read path が worktree 側ではなくルート側の local 領域を使うことを確認する場合。
- TUI 実行時に .cmoc/local 配下が git 追跡対象にならないことや、古い logs/sub_commands ではなく local/log/sub_command を使うことを確認する場合。

## Do not read this when
- TUI の画面内操作や対話 UI そのものの表示・キー操作を確認したい場合。
- TUI 以外のサブコマンドの実行ログ、初期化処理、git worktree 操作を単独で確認したい場合。
- Codex 実行ラッパーの内部実装や AgentCallParameter の汎用的な構築規則だけを確認したい場合。

## hash
- aa7bdcd098756577daa3aea7e9adb2f86d9f32fc7485beae852486fe6697583d

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
- Codex CLI 実行ラッパーが、モデル設定、sandbox profile、作業ディレクトリ、標準入力、出力、生成ファイル、schema 配置、linked worktree 上の読み取り許可を正しく扱うかを検証する realization test。
- 実物の Codex CLI と cmoc 管理 Ollama provider を組み合わせた統合寄りの確認と、偽の codex 実行ファイルによる引数・profile・副作用の確認を含む。

## Read this when
- Codex CLI を起動する処理、profile 生成、model provider 設定、sandbox の writable roots、Codex 実行時の cwd や標準入力の扱いを変更するとき。
- FileAccessMode と Codex profile の対応、特に repo write と pure oracle read の書き込み可能範囲を確認したいとき。
- 構造化出力 schema の保存場所、linked worktree から実行した場合の repo local 配下の扱い、Codex 実行ログの内容を確認したいとき。
- cmoc 管理 Ollama provider 用の Codex profile から、Codex CLI 組み込みの Ollama 向け flag を使わないことを検証したいとき。

## Do not read this when
- Codex 実行ラッパーではなく、agent call parameter や config のデータ構造そのものだけを確認したいとき。
- 通常の git 操作、repository 作成 helper、テスト支援用 fake executable の実装詳細だけを調べたいとき。
- Codex CLI や LLM の応答品質を評価したいとき。この対象は provider と実行制御を確認するもので、出力品質を検証しない。

## hash
- 929a3eeb0018059d8a77da251a968763e3bd4964137b3d2cd41c6164085f66eb

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
- Codex 実行後の post validation が、git ignore 対象・一時キャッシュ・仮想環境・実行時管理領域・cmoc ログなどの差分を許容することを検証するテスト群。
- 偽の codex 実行ファイルを使い、各 file access mode で run_codex_exec 後に残る許容差分の扱いを外部挙動として確認する。

## Read this when
- run_codex_exec の実行後ファイルアクセス検査で、どの差分を許容するかを変更・確認したいとき。
- FileAccessMode.READONLY、REALIZATION_WRITE、REPO_WRITE における post call の差分許容挙動をテストしたいとき。
- git ignore 対象の build、pytest cache、__pycache__、.venv、.agents、.codex、.git、memo、.cmoc/local/log/codex の扱いに関する回帰テストを探すとき。

## Do not read this when
- run_codex_exec のプロセス起動、引数構築、Codex 出力解析そのものを確認したいだけのとき。
- ファイルアクセス規則の定義や FileAccessMode の仕様を確認したいとき。
- post validation 以外の runtime_codex 全般のテストを探しているとき。

## hash
- e16b72b4e3f4693dc8788ef855d071eb27431de5db16ece11f1c542fcc6e14fc

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
- Codex exec が quota exceeded になった後の待機、probe、resume token 利用、再実行、ログ記録、cwd/CODEX_HOME の扱いを検証する realization test。
- 並列実行時に quota availability probe を代表 1 回に共有し、復帰時は各待機 call が resume し、probe 失敗時は待機 call も失敗する制御を外部挙動として確認する。
- quota retry 回帰を fake Codex 呼び出し列、call log、subcommand log、出力 JSONL とあわせて一箇所で追うためのテスト群。

## Read this when
- Codex exec の quota exceeded 後の retry、polling、probe、resume、または resume token 抽出の挙動を変更・調査する時。
- quota availability probe の AgentCallParameter、profile、prompt、ログ、file access post validation の扱いを確認する時。
- 複数の Codex exec が同時に quota 待機する場合の代表 probe 共有や失敗伝播を変更・検証する時。
- CODEX_HOME が相対パスの場合や Codex subprocess の cwd/--cd の扱いが quota retry 中に正しいか確認する時。

## Do not read this when
- 通常成功する Codex exec の基本引数生成や出力 parsing だけを確認したい時。
- quota exceeded と関係しない runtime error、設定読み込み、リポジトリ作成 fixture の挙動を調べる時。
- oracle 側の正本仕様や quota probe prompt の文面そのものを編集・確認したい時。

## hash
- 724d29f586cca5c255a72ca151e59c7a2c8dfc6305238166836393c3b109a560

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
- Codex TUI 起動経路の realization test。追加読み取りパスの事前アクセス検査、complete prompt の許可、linked worktree 起動時の作業ディレクトリと writable_roots、Codex CLI/TUI 非ゼロ終了時のエラー表示と呼び出しログを検証する。

## Read this when
- Codex TUI 実行時の extra_read_paths が、起動前に許可領域外として拒否されるかを確認・変更したいとき。
- PURE_ORACLE_READ または REPO_WRITE で、完了済み prompt ファイルを追加読み取り対象として渡す挙動を確認・変更したいとき。
- linked worktree から Codex TUI を起動する際の cwd、--cd、sandbox writable_roots、呼び出しログの挙動を確認・変更したいとき。
- Codex CLI/TUI が非ゼロ終了した場合の CmocError、コンソール表示、codex call log の内容を確認・変更したいとき。

## Do not read this when
- Codex TUI ではなく Codex exec や他の実行モードの挙動を調べるとき。
- ACP のファイルアクセスモード定義そのもの、CmocConfig の設定項目そのもの、または repository/worktree fixture の作成方法を調べるとき。
- oracle file や realization file の定義、INDEX.md 生成規則、パスモデル仕様を調べるとき。

## hash
- 3c68f30c7fc5f422a0c2b28779e4b6eb456b6e89eba6bc979dc31d89e1105d9f

# `test_doctor_cli.py`

## Summary
- doctor/init CLI の実行前処理と設定生成を検証する realization test。git 状態の修復、`.cmoc/local` の ignore/untrack、`.agents` の追跡、config の生成・同期、managed ollama の準備・検証、linked worktree 対象化、ローカル SLM profile 作成時の doctor 実行を扱う。

## Read this when
- doctor または init コマンドの外部挙動、git への副作用、config 生成・同期、managed ollama 準備に関するテストを確認・変更する場合。
- `.cmoc/local` を追跡対象外に保つ処理、既存 staged/unstaged 変更を壊さない repair commit、既存 tracked local file の untrack 挙動を検証したい場合。
- linked worktree 上で doctor が現在の作業ツリーだけを対象にすること、またはローカル SLM 用 Codex profile 作成時の doctor 連携を確認する場合。

## Do not read this when
- doctor/init 以外の CLI コマンドや、git 副作用を伴わない純粋な設定モデルの単体検証を探している場合。
- runtime doctor の内部 helper 実装そのものを変更する場合は、まず対応する実装側を読む。
- INDEX.md や oracle file のルーティング・正本仕様を編集するための根拠を探している場合。

## hash
- 94f148ad6ae03e6186caba88532a7dae0d5be432cd85265092d8cbd7fc6df2fd

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
- review oracle の CLI 実行、レポート描画、対象 oracle file 列挙、所見列挙・検証・judge・merge の制御、review 用 worktree と join commit、INDEX.md 変更の取り込み、異常時レポート、想定外差分の拒否をまとめて検証するテスト群。
- fake Codex 応答と一時 Git repository を使い、外部挙動としての report 内容、scope 別の対象選択、tracked ignored file や symlink の扱い、merge operation の契約違反検出を確認する。
- 大きなテストファイルだが、oracle review run の状態、出力、fake 応答文脈を共有する一連の外部挙動検証として凝集している。

## Read this when
- review oracle サブコマンドの CLI 挙動、report の見出し・集計・所見表示・error 表示を変更または調査する。
- oracle review の対象ファイル列挙、full scope と session scope、tracked ignored oracle file、AGENTS.md・INDEX.md 除外、symlink の分類を変更または調査する。
- review oracle の所見 loop、enumerate に渡す既存所見、challenger と advocate の検証理由、judge 結果、semantic merge の retry と失敗条件を変更または調査する。
- review oracle 用 worktree、linked worktree 上の session branch、INDEX.md 変更の merge、preflight indexing、join commit、INDEX.md conflict 解決を変更または調査する。
- review oracle 実行中に INDEX.md 以外の差分が生成された場合の拒否挙動や、processing failure 時の report 出力を変更または調査する。

## Do not read this when
- review oracle 以外の review サブコマンドや通常の session 操作だけを調べる場合。
- Codex 実行そのものの品質、LLM 出力内容、prompt 文面の詳細を検証したい場合は、対応する実装や prompt builder のテストを直接読む。
- oracle file の正本仕様本文を確認したい場合は、oracle 配下の該当文書を読む。
- 汎用的な Git helper、runtime preflight、indexing の単体挙動だけを確認したい場合は、それぞれの実装または専用テストを読む。

## hash
- 8f9544479db593c17e5a54d9ba47e1f89000aad759b50632b038bf3bcd60d112

# `test_session_cli.py`

## Summary
- session fork/join/abandon の CLI 回帰テストをまとめ、session branch と session state のライフサイクル、linked worktree 上の実行、state cleanup、dirty worktree や不正 state の拒否、join 時の conflict 解消と失敗報告の外部挙動を検証する。
- session 状態遷移に関わる branch/state fixture を共有する大きなテスト群であり、分割せず一箇所で読むことで fork、join、abandon の相互影響を追える。

## Read this when
- session fork が session branch と state file を作成する挙動、session-id 衝突時の retry/失敗、既存 state の保護、cmoc ignore 初期化を確認したいとき。
- session abandon が home branch へ戻り、session branch を削除し、state を abandoned に更新する挙動や、home branch 不在・cleanup 失敗時の rollback とエラー出力を確認したいとき。
- session join が session branch の変更を home branch へ統合し、state を joined に更新し、session branch 削除可否を出力へ反映する挙動を確認したいとき。
- linked worktree から session fork/join/abandon を実行した場合に、root 側 branch を汚さず linked 側 branch と HEAD を基準に処理するか確認したいとき。
- join の conflict 解消 agent 呼び出し、oracle conflict への repo write profile、conflict marker 検出、delete conflict の staging、conflict 解消以外の差分拒否を確認したいとき。
- session コマンドの失敗時に、既知の前提条件エラーを stdout に出す場合と、merge 後の予期しない失敗を stderr に出す場合の境界を確認したいとき。

## Do not read this when
- session 以外のサブコマンドの CLI 外部挙動を確認したいだけのとき。
- session state のデータ構造や永続化 helper の実装そのものを変更したいときは、まず session 実装側の state 管理コードを読む。
- agent call の一般的な profile 生成や sandbox 設定を確認したいだけのときは、profile 構築の実装または専用テストを読む。
- git repository fixture、runner、doctor 実行などテスト支援関数の使い方だけを調べたいときは、共通 test support を読む。
- conflict marker 判定ロジックだけを局所的に変更したい場合を除き、join の統合処理全体を把握する前にこの大きな回帰テストだけを根拠にしない。

## hash
- 256ec9f2c90b8d0714705d8c547d0dc7f629dad1314144c765ba7194987eb9cd

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
