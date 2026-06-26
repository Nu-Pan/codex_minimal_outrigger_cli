# `_support.py`

## Summary
- CLI テストで使う最小 Git リポジトリ、認証済み Codex home、偽の Python 実行ファイル、apply 用 worktree パス解決などを用意するテスト補助関数をまとめる。
- Git コマンド実行や現在ブランチ取得を通じて、テスト内の Git 状態確認と fixture 構築を支える共有入口として位置づけられる。

## Read this when
- CLI テストで一時 Git リポジトリを作成し、初期 commit 済みの状態や oracle 配下の tracked/ignored ファイルを準備する方法を確認したいとき。
- テストから Git コマンドを実行する helper、現在ブランチ名の取得、または apply の session state から worktree パスを導く処理を使う・変更するとき。
- Codex home の環境変数設定や fake external command 用の実行可能 Python スクリプトを、テスト fixture として用意する箇所を探すとき。

## Do not read this when
- 個別サブコマンドの期待挙動や assertion 内容を確認したいだけで、共有 fixture や helper の実装を変更しないとき。
- プロダクト本体の CLI 実装、状態管理、path model、oracle 仕様を調べたいとき。
- pytest や Typer のテスト runner の利用箇所そのものではなく、特定テストケースの入力・出力・失敗条件を確認したいとき。

## hash
- 8c09c548f4da0311169d9185be843e85179ae5fd86b54b1709052e34000c6938

# `test_apply_abandon_cli.py`

## Summary
- apply abandon CLI と apply process 停止処理の realization test。active apply run の破棄時に、apply worktree と apply branch の削除、session state の ready への復帰、警告出力、実行中 process の停止、linked worktree からの実行時の基準ディレクトリ復帰を検証する。
- 欠損済み cleanup 対象、running state だが process id がない状態、worktree を導出できない apply branch、stale apply branch など、破棄処理を中断または警告付き成功にする境界条件を扱う。
- pidfd ベースの signal 送信について、終了済み process、PID 再利用、停止完了待ちの race を apply runtime の制御ロジックとして検証する。

## Read this when
- apply abandon の外部挙動、CLI 出力、session apply state の更新、apply worktree と apply branch の cleanup 条件を変更または確認したいとき。
- apply が running のまま abandon される場合の process 停止順序、process id 記録の削除、停止できない状態の扱いを変更または確認したいとき。
- apply worktree 内、linked session worktree 内、stale apply branch 上など、実行場所によって abandon 対象をどう判定するかを確認したいとき。
- apply runtime の process signal 送信、終了済み process の無視、PID 再利用検出、停止待ち race の扱いを変更または確認したいとき。

## Do not read this when
- apply fork の Codex 実行結果や review findings の内容そのものを検証したいだけのとき。
- apply abandon 以外の session fork、init、worktree 作成 helper の一般的な挙動を調べたいとき。
- oracle 仕様断片、ルーティング文書、または INDEX.md 生成規則を確認したいとき。
- git worktree や branch 操作の低レベル helper 全般を調べたいが、apply abandon の cleanup 境界には関心がないとき。

## hash
- 54b682faa7a06cf27ea4ff719b3abc053fa5b6ea98122d9b34e99983e3aeff54

# `test_apply_fork_cli.py`

## Summary
- apply fork コマンドの realization test。Codex 実行を fake に差し替え、apply run の開始から完了までの状態更新、apply worktree 作成、apply branch 名、旧 apply_worktree/apply_process_id/pid の非保持、所見列挙呼び出しを検証する。
- session 側の .gitignore を書き換えないこと、.cmoc が git 追跡対象の場合に session を dirty にせず拒否すること、設定読み込み失敗時に apply run の branch/state/pid を開始しないことを検証する。
- 所見対象として .gitignore を扱う場合は apply branch 側で編集できること、apply 対象正規化では root 直下の memo を除外しつつ入れ子の memo directory を対象に残すことを検証する。

## Read this when
- apply fork の CLI 挙動、状態遷移、apply worktree の配置、apply branch の作成、完了時の state cleanup を変更・確認するとき。
- apply fork が session 側の .gitignore や .cmoc 追跡状態をどう扱うか、失敗時に session worktree を汚さないことを確認するとき。
- apply fork の設定読み込み失敗時の早期終了、pid/state/branch を開始しない制御を変更・確認するとき。
- apply 対象の列挙・正規化、特に .gitignore を所見対象として扱う挙動や root 直下 memo 除外の境界を変更・確認するとき。

## Do not read this when
- Codex CLI や LLM 出力品質そのものを検証したいとき。この対象は Codex 実行結果を fake にし、apply fork 側の制御と副作用を検証する。
- apply fork 以外のサブコマンド、session fork 自体の詳細、または init の単独挙動を調べるとき。該当コマンドの実装または専用テストへ進む方が直接的。
- oracle file の正本仕様を確認したいとき。この対象は realization test であり、仕様判断の根拠としては oracle 側を読む。

## hash
- 072a67d3843e4d3f96868eefadcf9da9ea3da971ca1760673b37713b59acafe3

# `test_apply_fork_report_cli.py`

## Summary
- apply fork コマンドの report 生成、収束判定、dirty file 再検査、編集禁止対象検出、rolling 対象選定を CLI 経由で検証する realization test。
- Codex 実行を fake に差し替え、所見列挙・適用・commit message・変更要約の応答に応じて、終了コード、標準出力、report 内容、session state、apply branch の commit を確認する。
- apply fork の外部挙動と制御ロジックが、report の result 表示、変更要約の反映、INDEX.md 除外、上限到達時の収束扱い、禁止差分時の error state、前回 apply の oracle snapshot 利用にどう現れるかを読む入口になる。

## Read this when
- apply fork の report 出力、result_label、終了コード、未収束・収束・error の扱いを変更または調査するとき。
- apply fork が Codex 応答から finding application、commit message、change summary を扱う流れをテスト上で確認したいとき。
- apply 後の dirty file 再検査、INDEX.md の再検査除外、再検査が収束するまでの制御を変更または検証するとき。
- 編集禁止対象への差分検出時に、CLI 出力、report、session state、既存の変更要約がどう扱われるかを確認するとき。
- rolling apply fork が前回 apply の oracle snapshot commit とその後の変更から調査対象を選ぶ挙動を確認するとき。

## Do not read this when
- apply fork の内部 helper 単体の細かな実装だけを確認したい場合は、実装側の該当モジュールを直接読む。
- session fork、apply join、init など apply fork 以外の CLI 挙動そのものを調査する場合は、それぞれの専用テストまたは実装を優先する。
- Codex CLI や LLM 出力品質そのものを検証したい場合は、このテストは fake 応答による制御ロジック検証なので対象外。
- report の markdown レンダリング仕様全体や schema 定義を調べたい場合は、report 生成処理または schema 側を読む。

## hash
- 6d6b590fc599fc4e774e39853bdefa934798a47310bc7809808e11cb80d35ced

# `test_apply_join_cli.py`

## Summary
- `apply join` の CLI 挙動を、実際の一時 Git リポジトリと Typer runner 経由で検証する realization test。
- apply worktree と apply branch の片付け、session state の ready 復帰、oracle snapshot commit 記録、report 生成、apply worktree 内からの実行時の cwd 復帰を確認する。
- 未コミット差分、想定外の apply 差分、通常モードと force-resolve、merge conflict、INDEX.md conflict 自動解決、.gitignore 変更許容など、join の正常系・異常系・後始末をまとめて扱う。

## Read this when
- `apply join` の成功時に apply worktree や apply branch が削除されるか、session state が更新されるかを確認・変更するとき。
- apply worktree 内または session worktree 内から `apply join` を実行した場合の cwd、ログ出力先、clean worktree 要件を扱うとき。
- 想定外差分、merge conflict、force-resolve、report 内容、.gitignore の扱い、INDEX.md conflict 解決に関する CLI の外部挙動を変更するとき。
- `sub_commands.apply.join` や `sub_commands.apply.fork` 周辺の実装変更後に、join の統合的な回帰テストを探すとき。

## Do not read this when
- `apply fork` 単体の Codex 実行内容、プロンプト、fork 作成処理だけを確認したいとき。
- session fork、init、path model、状態ファイル schema など、join の実行結果として現れる範囲を超えた個別仕様を調べたいとき。
- 低レベル helper の単体挙動や、Git 操作 wrapper の詳細だけを確認したいとき。
- INDEX.md エントリー生成やルーティング文書そのものの仕様を確認したいとき。

## hash
- b1e6ed2337638d1b1f2c43e259c58740f40b6e5f57ba07313dda49260c1ae7fc

# `test_basic_runtime.py`

## Summary
- cmoc の基本的な実行時挙動を横断的に検証する realization test。パスモデル、時間表示、work root 判定、設定既定値、構造化エラー表示、session/apply branch 形状、CLI エラー出力、completion probe、.cmoc の ignore 設定、ファイルアクセス mode、binary 判定、Codex profile の filesystem 権限制御を扱う。
- 個別モジュール単位の細部よりも、runtime・config・state・CLI entrypoint・permission profile が組み合わさった外部挙動の回帰確認に入るためのテスト群である。

## Read this when
- cmoc の基本 runtime 挙動、CLI preflight、エラー表示、stdout/stderr の出力先、work root 判定、linked worktree 判定を変更または調査するとき。
- FileAccessMode、sandbox mode、Codex profile、memo/oracle/.agents への read/write/read_only/deny_read 制御を変更または確認するとき。
- SessionState の branch 名解釈、state 読み込み、invalid branch shape の拒否挙動を変更または確認するとき。
- cmoc 初期化時の .gitignore 更新、.cmoc ignore pattern の有効性、既存 ignore pattern を保つ挙動を変更または確認するとき。
- format_duration、is_binary、設定既定値など、複数の小さな runtime helper の現行期待値をまとめて確認したいとき。

## Do not read this when
- 特定サブコマンドの正常系フローや詳細な業務ロジックだけを調べたい場合は、そのサブコマンドや対象モジュールの実装・専用テストを先に読む。
- oracle の正本仕様を確認したい場合は、この realization test ではなく該当する oracle file を読む。
- 個別 helper の実装責務や内部アルゴリズムを理解したいだけの場合は、対象 helper が定義されている実装ファイルを直接読む。
- テスト共通 fixture やリポジトリ生成 helper の使い方を調べたい場合は、このテスト本文ではなくテスト support 側を読む。

## hash
- 42c80ded9d6296d0469afe21c9da0d484288c240b18afc89f97a861f2fb4f365

# `test_cli_init_tui.py`

## Summary
- CLI の初期化処理と対話起動処理に関する realization test。初期化時の `.cmoc` 配下の追跡解除、`.gitignore` への無視設定、既存 staged/unstaged 変更の保全、linked worktree での保存先や commit 対象、既定設定 JSON の生成・同期を検証する。
- 対話起動では、エディタで編集された依頼文から解決用パラメータを作り、HTML コメント除去後の完了プロンプトを保存し、Codex TUI 起動へ model class・reasoning effort・file access mode・追加 read path を渡す制御を検証する。
- Markdown 依頼文 parser について、fenced code block 内の見出し風テキストを見出し扱いしないことと、見出し前の preamble を本文として保持することを検証する。

## Read this when
- `init` サブコマンドの Git 操作、`.cmoc` 無視設定、初期 commit、既存 index/worktree 状態の保全、linked worktree 対応を変更・調査する。
- `.cmoc/config.json` の既定値生成、既存設定との同期、手動設定値を上書きしない挙動を変更・調査する。
- `tui` サブコマンドのエディタ起動、依頼文整形、パラメータ解決用 Codex 呼び出し、Codex TUI 呼び出し、ログ保存先、linked worktree での root/cwd/schema/log の扱いを変更・調査する。
- Markdown プロンプトを見出し単位に分解する parser の挙動、特に fenced code block と見出し前本文の扱いを変更・調査する。

## Do not read this when
- 個別サブコマンドに依存しない CLI 登録や Typer の一般的な entrypoint だけを確認したい。
- Git 操作や `.cmoc` 状態に関係しない純粋な設定 loader、schema 定義、モデル enum の詳細だけを確認したい。
- Codex CLI やエディタ実行そのものの外部品質、LLM 出力内容の妥当性を検証したい。
- Markdown parser 全般の網羅仕様を探しており、fenced code block 内見出しと preamble 保持以外の構文を扱うテストが必要である。

## hash
- c1265830784b4cbbcfcbda1b16f91cedf1e5c9880f77122e02d39be58637340f

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 呼び出しの runtime テスト。exec 経路が prompt を標準入力で渡し、schema・profile・CODEX_HOME・stdout/stderr/call log・subcommand log を期待どおり扱うことを検証する。
- Codex TUI 経路が exec サブコマンドを使わず prompt 引数で起動し、workspace write profile の writable/read-only 設定、call log、console 表示、戻り値を記録することを検証する。
- repo 側 config が Codex profile の model と reasoning_effort に反映されること、worktree cwd 実行時に schema 保存先が cwd 側の work root になることを確認する。

## Read this when
- Codex CLI を起動する runtime 実装、特に exec と TUI の argv・cwd・環境変数・profile 生成・ログ出力を変更する時。
- AgentCallParameter の model class、reasoning effort、file access mode、output schema が Codex profile や CLI 引数へどう反映されるかをテスト観点から確認したい時。
- Codex 呼び出しログ、stdout/stderr ログ、subcommand logger の codex_call event、console 表示の期待値を変更または調査する時。
- worktree 上で Codex exec を実行する場合の schema 保存先、root 側と cwd 側の .cmoc state/log の使い分けを確認する時。
- repo config の codex model や reasoning_effort 設定が実行時 profile に反映されない不具合を調べる時。

## Do not read this when
- Codex runtime ではなく、git 操作、oracle 生成、INDEX 生成、path model など別領域の挙動だけを調べる時。
- Codex CLI の実物の出力品質や LLM 応答内容を検証したい時。このテストは fake codex と subprocess 差し替えで runtime の制御と副作用を検証する。
- Codex profile 生成の実装詳細そのものを変更する場合で、まず実装の責務や helper 境界を知りたい時は、対応する runtime 実装を先に読む。
- config schema や既定値の定義そのものを調べる時は、設定定義や同期処理の実装を先に読む。

## hash
- be5c7105c0d916cd3989f402ac9d4c72e7c29fb82414c1641a19b58e7239da84

# `test_codex_runtime_home.py`

## Summary
- Codex CLI 実行ラッパーが利用する Codex home の決定・検証を確認する realization test。環境変数未設定時の既定 home、相対パス指定の保持と解決、存在しない home・ファイルである home・認証情報欠落を Codex CLI 起動前にエラーにする挙動を扱う。
- fake の Codex 実行ファイルで呼び出し時の環境変数と引数を記録し、実行結果に含まれる Codex home、profile 配置、call log の内容が期待どおりかを検証する。

## Read this when
- Codex CLI 呼び出し前に CODEX_HOME をどの値へ設定するか、未設定時にどの home を使うかを変更・確認する時。
- Codex home の存在確認、ディレクトリ種別確認、auth.json 必須チェック、またはそれらの CmocError の summary・detail・next_actions を変更する時。
- run_codex_exec の戻り値に含まれる codex_home、profile_path、call_log_path と Codex CLI へ渡す profile 引数の関係を確認する時。

## Do not read this when
- Codex CLI の標準入出力プロトコル、turn.completed 以外のイベント処理、または LLM 応答品質の検証を調べたい時。
- Codex home とは無関係な AgentCallParameter のモデル種別、reasoning effort、ファイルアクセスモードの変換だけを調べたい時。
- リポジトリ作成 helper や fake 実行ファイル生成 helper の実装詳細を調べたい時。

## hash
- b4c26ae1f025d3687713c3ca03063e1f18042933100f15eeadb4bd2979c04b1d

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex CLI 実行ラッパーが quota exceeded を受けた後に、quota availability probe を挟んで再実行または resume し、最終結果・呼び出しログ・サブコマンドイベントを整合させる挙動を検証する realization test。
- 偽の codex 実行ファイルを使い、CODEX_HOME、argv、stdin、stdout/stderr/output のログ、resume token の有無、並列実行時の probe 代表化を外部副作用として確認する。

## Read this when
- Codex CLI 呼び出しの quota exceeded 検出後の待機・probe・resume・再実行制御を変更する時。
- quota availability probe の argv、stdin、profile、出力保存、ログ記録、コンソール表示の期待値を確認したい時。
- thread.started の thread_id を使った resume と、resume token が得られない場合の通常再実行の分岐を確認したい時。
- 複数の run_codex_exec 呼び出しが同時に quota exceeded になった時、probe が 1 回に集約され各呼び出しが復帰する制御を確認したい時。

## Do not read this when
- Codex CLI の通常成功時、通常失敗時、設定変換、または quota 以外のエラー処理だけを確認したい時。
- AgentCallParameter、CmocConfig、SubcommandLogger の基本構造や生成規則そのものを調べたい時。
- 実際の Codex CLI や LLM の応答品質を検証したい時。
- リポジトリ作成、CODEX_HOME 準備、偽実行ファイル作成のテスト支援関数そのものを変更したい時。

## hash
- 41648e73004d1e8cd44eab18f909248b78cd18783acd796920a90c6c2454f754

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 実行ラッパーの retry 制御を検証する realization test。schema validation 失敗後の再実行、capacity エラー検出時の再実行、stdout JSONL 以外に出た capacity/quota 文言を retry 条件として扱わないことを、fake codex 実行ファイルと呼び出しログで確認する。
- AgentCallParameter、CmocConfig、SubcommandLogger、run_codex_exec の組み合わせで、出力 JSON、呼び出し回数、call log、subcommand log の status・returncode・error detail が期待どおりになるかを見る入口になる。

## Read this when
- Codex CLI 呼び出しの semantic output schema validation retry の挙動やログ記録を変更・調査する。
- Codex CLI が capacity を示す JSONL event を返したときの retry、sleep 抑制、失敗呼び出しの call log 記録を確認する。
- quota や capacity を示す文字列が stdout JSONL event ではなく通常出力・stderr に出た場合に、retry せず通常失敗として扱う境界を確認する。
- run_codex_exec の戻り値、call_log_path、stdout_log_path、subcommand logger の codex_call event status を変更する実装に触る。

## Do not read this when
- Codex CLI の通常成功パスだけを確認したい場合。retry や schema validation 失敗、capacity/quota 判定に関係しないならより基本的な実行テストを読む。
- CLI 引数の構築、モデル選択、ファイルアクセス設定などの入力変換だけを調べたい場合。この対象は retry とログ副作用の検証が中心である。
- oracle file の正本仕様を確認したい場合。この対象は realization test であり、正本仕様そのものではない。

## hash
- 27137103545db450aeccf58ac1a55fdb671bd971566bc45f7d06a1f52534ac69

# `test_indexing_cli.py`

## Summary
- インデックス生成 CLI と関連 helper の realization test。初期化済み・未初期化リポジトリ、linked worktree、既存差分、fresh hash、malformed entry、semantic field validation、並列生成、root 直下 memo 除外と nested memo 対象化、merge 時のインデックス衝突解消を検証する。
- Codex 実行を monkeypatch して構造化されたエントリー生成結果を返させ、インデックス更新・コミット対象・作業ツリー清潔性・エラー出力を外部挙動として確認する。

## Read this when
- インデックス生成コマンドの実行条件、失敗条件、コミット挙動、linked worktree での対象 root 判定を変更する。
- インデックスエントリーの fresh 判定、malformed entry の再生成、semantic field の検証、空リストや空文字の rendering 挙動を変更する。
- インデックス更新対象の探索、兄弟エントリーの並列生成、root 直下 memo の除外、下位階層にある memo の扱いを変更する。
- merge conflict 解消時にインデックスファイルを削除して merge commit を成立させる処理を変更する。

## Do not read this when
- 通常のサブコマンド登録、CLI 全体の起動構造、runner fixture の基本だけを確認したい場合は、より直接それらを定義する実装または support test を読む。
- インデックスエントリーの文章品質や Codex の生成内容そのものを評価したい場合は、このテストではなく生成プロンプトや schema 側を読む。
- oracle file の正本仕様を確認したい場合は、この realization test ではなく oracle 側の該当文書を読む。

## hash
- 5c4faf3c479e5af409849ec66e7b3812ef40afb42c408c39ca95c462100914e4

# `test_indexing_preflight.py`

## Summary
- Codex 実行・TUI 起動の直前に INDEX 更新を走らせる preflight 制御を検証する realization test。
- preflight が対象 worktree を選ぶこと、生成された INDEX 更新を cmoc indexing コミットとして残し作業ツリーを清潔に戻すこと、既存のリポジトリ単位ロックを待つこと、INDEX エントリー生成や競合解決の目的では preflight をスキップすることを扱う。
- 実際の Codex 呼び出しや INDEX 生成は monkeypatch で差し替え、git worktree、lock file、呼び出し順、コミット履歴、副作用を観察して制御ロジックを確認する。

## Read this when
- Codex 実行前に INDEX 更新を自動実行する制御を変更・調査するとき。
- preflight が root と cwd のどちらの worktree を更新対象にするかを確認するとき。
- INDEX 更新のコミット作成、作業ツリー清掃、またはリポジトリロック待機の挙動を変更するとき。
- Codex 呼び出しの purpose に応じて indexing preflight を実行またはスキップする条件を変更するとき。

## Do not read this when
- INDEX の本文生成内容、エントリー文章、差分解析そのものを確認したいとき。
- apply join の通常の競合解決処理や fork refine の詳細挙動を調べたいだけのとき。
- Codex CLI や TUI の実プロセス起動方法、モデル指定、ランタイム統合の一般仕様を調べたいとき。
- ロックの低レベル実装だけを調べたい場合で、preflight からの待機制御に関心がないとき。

## hash
- 1e43cf0d39575b2dffeea90d89f05e0c252de3a1a50fe6eb29891fc5fe95558d

# `test_prompt_parts.py`

## Summary
- プロンプト部品とパラメータ生成器のテスト群。レビュー基準、ルーティング規則、ファイルアクセス規則、各種 standard の Markdown 描画、完全プロンプトへの標準文書の注入・省略、Structured Output schema、モデル種別・推論量・アクセスモードの選定を検証する。
- realization test として、プロンプト生成まわりの仕様語彙、空行正規化、apply fork・review oracle・session join・TUI resolve・indexing のビルダーが期待する文書断片や設定を返すかを確認する入口になる。

## Read this when
- プロンプト部品、standard 文書、または complete prompt の構成・描画・含有条件を変更する。
- file access mode ごとの読書き制約文、routing rule、apply review standard、realization standard、review oracle standard、index entry standard の出力語句を確認・更新する。
- apply fork、review oracle、session join、TUI resolve、indexing の各パラメータ生成器について、モデル種別、reasoning effort、file access mode、schema path、埋め込まれるプロンプト断片の期待値を調べる。
- Structured Output schema の制約や oracle 側 schema との一致、空配列拒否、enum・required・additionalProperties などの検証観点を確認する。
- StructDoc、StructCodeBlock、render_as_markdown の Markdown 出力、とくに連続空行やコードブロック内空行の扱いを調べる。

## Do not read this when
- CLI 実行フロー、永続状態、Git 操作、ワークツリー作成など、プロンプト部品やパラメータ生成器に直接関係しない挙動を調べる。
- 個別の standard 文書本文や builder 実装そのものを修正したいだけで、テスト期待値や既存の検証観点を確認する必要がない。
- oracle file の正本仕様断片そのものをレビュー・編集提案する作業であり、realization test 側の期待値確認が不要である。
- 一般的な pytest 設定、テスト実行環境、共通 fixture の仕組みだけを調べたい。

## hash
- 02e84c11cf877184c9eb1d2121f57234164a39f1283fad3a421e4c5d3d73108c

# `test_review_oracle_cli.py`

## Summary
- `review oracle` サブコマンドの realization test。レビュー対象 oracle の選定、Codex 呼び出しループ、finding の merge 操作、レポート生成、review 用 worktree からの INDEX.md 反映、エラー時レポート、review 側が INDEX.md 以外を変更した場合の拒否を検証する。
- CLI 経由の正常系だけでなく、内部関数を直接呼んで finding merge operation の契約違反や、対象別 enumerate prompt に渡る既存 finding の隔離も確認する。

## Read this when
- `review oracle` の外部挙動、出力レポート、scope option、対象 oracle の数え方や除外条件を変更・確認するとき。
- review 処理で Codex structured output を使う enumerate、validate、judge、merge の制御フローや、finding merge operation の delete、replace、merge 契約を変更・確認するとき。
- review 用 worktree で生成された INDEX.md だけを session 側へ取り込み、その他の差分を拒否する挙動を変更・確認するとき。
- review 処理の途中失敗時にエラーレポートを残し、CLI 出力でエラーを見せる挙動を変更・確認するとき。
- gitignored oracle、binary oracle、session scope で変更対象がない場合など、レビュー対象選定の境界条件を扱うとき。

## Do not read this when
- oracle file そのものの正本仕様を確認したいだけのとき。まず oracle 配下の本文を読む。
- `review oracle` 以外の CLI サブコマンドや session 操作一般の挙動を調べるとき。より直接の実装またはテストを読む。
- Codex CLI や LLM の出力品質そのものを検証したいとき。このテストは fake result による制御ロジックと外部副作用の検証に集中している。
- INDEX.md エントリー生成規則やルーティング文書の仕様を確認したいとき。対象は review oracle の realization test であり、INDEX.md の仕様本文ではない。

## hash
- 5a84d75fdb388db3eb119926ec21914da2ae5e0ec80a7002386f24781c594ceb

# `test_session_cli.py`

## Summary
- cmoc の session サブコマンド群について、CLI 実行後の Git branch、linked worktree、session state JSON、標準出力、競合解決時の Codex 実行 profile を検証する realization test。
- fork が session branch と active state を作ること、abandon が home branch へ戻して state を abandoned にすること、join が home branch へ統合して joined state にすることを、通常 worktree と linked worktree の両方で確認する。
- abandon の home branch 不在時の失敗出力、cleanup 失敗時の rollback、join の oracle conflict 解決、delete conflict staging、session branch 削除失敗時の warning など、session 操作の失敗・境界条件も扱う。

## Read this when
- session fork、session abandon、session join の外部挙動、保存される session state、branch 切り替え・削除の期待値を確認または変更する時。
- session サブコマンドが linked worktree 上で現在の worktree branch と HEAD を基準に動くかを確認する時。
- session join の競合解決で Codex 実行に渡す file access mode や oracle read-only / repo write permission を検証する時。
- abandon や join の失敗時に、出力内容、rollback、session branch の残存、未解決 conflict の staging を含む回復挙動を変更する時。

## Do not read this when
- session 以外のサブコマンド、init 単体、設定読み込み、path model などの挙動だけを調べる時。
- session 実装の内部 helper 分割や型定義だけを確認したい時。ただし外部挙動との対応確認が必要なら読む。
- oracle file の正本仕様そのものを調べる時。この対象は realization test であり、仕様判断の根拠としてではなく既存挙動確認の補助として扱う。
- Codex CLI や LLM 出力品質そのものの検証を探している時。この対象は cmoc の session 制御ロジックと副作用を検証する。

## hash
- d8b7781025e30eeb64970a94bbe2d802147b9d7530e45ad8cc45025e750d1620
