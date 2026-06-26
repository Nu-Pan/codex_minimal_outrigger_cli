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
- apply fork CLI の realization test。Codex 実行を fake 化し、apply fork が session/apply 状態、apply branch、apply worktree、pid 管理、.gitignore、linked worktree、設定読み込み失敗時の副作用抑止、対象 path 正規化を期待どおり扱うことを検証する。

## Read this when
- apply fork の外部挙動、状態遷移、apply branch/worktree 作成、完了時 cleanup に関するテスト意図を確認したいとき。
- linked worktree から apply fork を開始した場合の基準 commit、branch HEAD、worktree 配置の期待値を確認したいとき。
- apply fork が session 側の .gitignore や tracked .cmoc をどう扱うべきか、また apply branch 側で .gitignore を編集対象にできるかを確認したいとき。
- cmoc config 読み込み失敗時に apply run の branch/state/pid を開始しないことを確認したいとき。
- apply 対象正規化で root 直下の memo は除外し、入れ子の memo directory は対象に残す挙動を確認したいとき。

## Do not read this when
- apply fork 以外の CLI サブコマンドの挙動を調べたいとき。
- Codex CLI や LLM 実行結果そのものの品質、実際の Codex 呼び出し実装、プロンプト内容を調べたいとき。
- apply fork の実装詳細を変更したいだけで、テストが固定する外部挙動や副作用境界を確認する必要がないとき。
- oracle の正本仕様断片を確認したいとき。

## hash
- 5dedbc806c2a624341a203681297f4b490988a3ee3a6f34b2ad845066fd41bcd

# `test_apply_fork_report_cli.py`

## Summary
- apply fork CLI の report 生成と収束判定を検証する realization test。Codex 応答を fake に差し替え、所見適用、変更要約、commit message、終了コード、session state、report 内容、rolling 対象選択などの外部挙動を確認する。
- 未収束時の report には変更要約と commit message が反映され、収束時・エラー時・rolling 実行時にはそれぞれ期待される状態更新と出力になることを扱う。

## Read this when
- apply fork の CLI 終了コード、report 表示、result label、session state 更新に関するテストを確認・変更するとき。
- apply fork が所見適用後の dirty file を再検査し、生成されたルーティング index を再検査対象から外す挙動を確認するとき。
- apply fork の回数上限到達時に、最後の許可対象が空所見なら収束扱いになる制御を確認するとき。
- apply fork が編集禁止領域への差分を検出して error state と report に反映する挙動を確認するとき。
- rolling apply fork が前回 apply join 後の oracle 側変更だけを対象にする挙動を確認するとき。

## Do not read this when
- apply fork の内部実装や helper の責務分割だけを調べたいときは、実装側の apply fork サブコマンドへ進む。
- apply join 単体の仕様や join 処理全体のテストを確認したいときは、apply join を扱うテストへ進む。
- Codex 実行基盤そのもの、structured output schema、agent call parameter の一般挙動を調べたいときは、それぞれの実装または専用テストへ進む。

## hash
- a95414220bb9a8f63a087a9d82f9c0997eb33223e7c1c3172a238b481be00a77

# `test_apply_join_cli.py`

## Summary
- apply join CLI の統合フローを検証する realization test。apply fork 後の apply worktree を session 側へ join し、apply worktree と apply branch の cleanup、session state の ready への復帰、join commit と oracle snapshot commit の記録、join report 生成を確認する。
- apply worktree 上から実行した join の挙動も扱い、実行後に cwd が session root へ戻ること、cleanup 結果表示、apply worktree 側にログを書かず session root 側へ記録する失敗時ログ経路を検証する。
- apply join における保護・異常系として、apply worktree の未コミット差分、想定外の apply 差分、merge conflict、INDEX.md conflict の自動解決継続、force-resolve による巻き戻しを外部挙動で確認する。

## Read this when
- apply join の成功時に、apply worktree 削除、apply branch 削除、state 更新、join report 生成、last_joined 系 state の更新が期待どおりか確認したいとき。
- apply join を session worktree から実行する場合と apply worktree から実行する場合の違い、特に cwd 復帰、cleanup 表示、ログ保存先を調べるとき。
- apply join が dirty な apply worktree を拒否する条件や、そのとき state を completed のまま保ち cleanup しない挙動を確認したいとき。
- apply join が oracle などの想定外 apply diff を検出して report に保存する挙動、または force-resolve で apply 側変更を戻して join を通す挙動を確認したいとき。
- apply join の merge conflict 処理を変更する際に、通常ファイル conflict は中止して report 化し、INDEX.md conflict は通常モードで解決後に継続する期待を確認したいとき。
- apply join で .gitignore の変更が想定外差分として扱われず、session root に反映されることを確認したいとき。

## Do not read this when
- apply fork が Codex exec をどの parameter で起動するか、または fork 時に apply worktree をどう作るかを調べたいだけのとき。
- apply join の内部 helper 単体の実装詳細、path model、state schema、report markdown の詳細な組み立て規則を読む必要があるとき。
- session fork、init、git helper、test fixture の共通セットアップ自体を変更する作業で、apply join の外部挙動を確認する必要がないとき。
- oracle file の正本仕様や INDEX.md 生成規則そのものを確認したいとき。

## hash
- 82d9e638cced5347c06435366a69d9b535c21f86a4a74ff0ee1e401d483ef799

# `test_basic_runtime.py`

## Summary
- 基本ランタイム、設定既定値、パスモデル、エラー表示、状態ブランチ判定、CLI 失敗時出力、gitignore 更新、ファイルアクセス権限、バイナリ判定、Codex profile 生成を横断的に検証する realization test。
- cmoc の中核ランタイム補助関数と CLI preflight/error handling が、外部に見える挙動や権限制御として期待どおり働くかを確認する入口になる。

## Read this when
- ランタイム補助関数、CLI エラー出力、作業ルート判定、セッション状態ブランチ名、`.cmoc` ignore 処理、ファイルアクセスモード、Codex profile の権限生成に関するテストを確認・更新したいとき。
- `CmocError` の markdown 表示、stderr/stdout の使い分け、completion probe 時の副作用抑止、linked worktree と repo root の区別に関する既存期待値を知りたいとき。
- 設定の論理モデルクラス既定値、所要時間表示、初期チャンクだけ読むバイナリ判定など、共有 runtime helper の外部挙動を変更する前後に影響範囲を確認したいとき。

## Do not read this when
- 個別サブコマンドの正常系フロー、プロンプト生成、oracle 文書処理など、このファイルで import されていない領域の詳細仕様やテストを探しているとき。
- 実装本文の責務分割や内部アルゴリズムを理解したいだけで、テストが固定している外部挙動や制御上の期待値を確認する必要がないとき。
- 同階層の専用テストが扱う、より狭い機能領域の期待値だけを確認すれば足りるとき。

## hash
- 69e42a31f2d52e9b3d1c1f9a2c1feebadcc5ae920ee3cbc1830d20dea33e875b

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
- Codex 実行が quota exceeded で失敗した後、quota availability probe を挟んで再実行または resume する制御を検証する realization test。
- quota 待機時の呼び出し順、標準入力、CODEX_HOME 伝播、resume token 利用、call log と subcommand log の記録内容、コンソール出力をまとめて確認する。
- 並行実行時に quota probe が代表 1 回に集約され、各実行が resume して成功することも検証する。

## Read this when
- Codex 実行の quota exceeded 検出後に、probe、retry、resume を行う制御ロジックを変更する。
- Codex 実行ログ、call_log_path、stdout/stderr/output の保存、subcommand logger の codex_call event を変更する。
- quota probe の argv、profile、標準入力、出力ファイル、CODEX_HOME など、Codex CLI 呼び出し条件を確認したい。
- 複数スレッドから同時に quota exceeded が発生した場合の probe 集約や resume 挙動を変更・調査する。

## Do not read this when
- Codex CLI の通常成功時や一般的な失敗時だけを扱い、quota exceeded 後の待機・probe・resume 制御に触れない。
- oracle file の正本仕様を確認したい。これは実装挙動を検証する realization test であり、仕様本文ではない。
- Codex 実行とは無関係なサブコマンド、設定読み込み、path model、INDEX.md 生成処理だけを調査する。
- LLM 出力品質や Codex CLI 自体の内部挙動を確認したい。ここでは fake codex を使って cmoc 側の制御とログだけを検証している。

## hash
- 8a391a1b2ae8c80eee70ffea050c1797c06ea15953441d15f80ed91e0f83c2a3

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
- indexing サブコマンドと INDEX.md 生成周辺の realization test。競合した INDEX.md の解決、Codex によるエントリー生成、生成結果の commit、未初期化・未コミット差分・linked worktree・fresh hash・malformed entry・semantic field validation・並列生成・memo 除外境界を検証する。

## Read this when
- indexing サブコマンドの外部挙動、preflight、commit 対象、linked worktree 上での更新先を変更または確認したいとき。
- INDEX.md エントリーの生成・再生成判定、hash freshness、semantic field validation、rendering の仕様に関わる realization code を変更するとき。
- apply join 側の INDEX.md merge conflict 解決が、競合ファイル削除と merge commit にどう反映されるかを確認したいとき。
- root 直下の memo を indexing 対象外にしつつ、通常ディレクトリ配下の memo は indexing 対象にする境界を確認したいとき。

## Do not read this when
- Codex 実行基盤そのもの、LLM 出力品質、または structured output schema の内容だけを確認したいとき。
- indexing 以外のサブコマンドの CLI 挙動や git 操作を調べたいとき。
- oracle file の正本仕様を確認したいとき。

## hash
- 531d80c05871041e2127e474429e3692ef537f513913d406de25ea051c72f3e9

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
- prompt parts と builder parameter のテスト群。StructDoc の Markdown 描画、complete prompt への標準文書注入、file access rule、routing rule、各種 builder が期待する実行パラメータ・schema・root 表現を検証する。
- プロンプト生成まわりの標準文書、ファイルアクセス制約、INDEX エントリー基準、TUI パラメータ解決、apply fork / review oracle / session join の builder 挙動を横断的に確認する realization test。

## Read this when
- プロンプト部品が期待する見出し・用語・本文断片を Markdown として出力しているか確認したいとき。
- complete prompt に routing rule や各種 standard が含まれる条件、または既定で省略される条件を変更・検証するとき。
- file access mode ごとのプロンプト文言、READONLY / PURE_ORACLE_READ / REALIZATION_WRITE / ORACLE_WRITE / REPO_WRITE の制約表現を確認するとき。
- apply fork、review oracle、session join、TUI resolve parameter、indexing index entry の builder が設定する model class、reasoning effort、file access mode、schema path、prompt 内容を変更するとき。
- StructDoc や StructCodeBlock の Markdown rendering、特に連続空行の折りたたみ挙動を変更するとき。
- builder が参照する JSON schema の制約や oracle 側 schema との一致性を確認するとき。

## Do not read this when
- 個別 CLI コマンドの実行フローやユーザー向け入出力だけを確認したいとき。
- prompt parts や builder parameter ではなく、実際の index entry 生成ロジック本体を調べたいとき。
- oracle file の正本仕様そのものを確認したいとき。該当する oracle doc または oracle src を直接読む方が適切。
- 特定の実装関数の内部アルゴリズムだけを追うとき。対象の実装ファイルを直接読む方が適切。

## hash
- f7645913978ff0cd612281d1e272ef352a2d6ae82aa032ecd84bf5969f9f1f97

# `test_review_oracle_cli.py`

## Summary
- `review oracle` コマンド周辺の realization test。レビュー対象 oracle の列挙、scope 指定、レポート生成、linked worktree 上での実行、gitignored oracle の除外、review 用 worktree で生成された `INDEX.md` 差分の取り込み、競合解決、処理失敗時のエラーレポート、review 処理が `INDEX.md` 以外を変更した場合の拒否を検証する。
- finding の列挙・検証・判定ループに渡る情報や、finding merge operation の delete/replace/merge 契約を、外部 Codex 実行を fake に差し替えて制御ロジックとして確認する。

## Read this when
- `review oracle` の CLI 挙動、scope の既定値や短縮 option、出力されるレポート内容、対象 oracle の選別条件を確認・変更したいとき。
- review 用 worktree、linked worktree、session branch、review 結果の join commit、`INDEX.md` 変更の merge や conflict 解決に関わる実装を変更するとき。
- oracle review 中の Codex 呼び出し目的文字列、structured output schema ごとの処理分岐、finding merge operation の妥当性検証を変更するとき。
- review 処理の失敗時レポート、fatal finding の扱い、作業ツリーに `INDEX.md` 以外の差分が出た場合の rollback/拒否挙動を確認したいとき。

## Do not read this when
- 通常の `init`、`session fork`、git helper、設定読み込みの基本動作だけを確認したいときは、それらの単体テストや実装を直接読む。
- oracle 本文の正本仕様そのもの、または review が検査すべき仕様内容を確認したいときは、oracle 側の本文を読む。
- Codex CLI の実出力品質や LLM の判断内容を確認したいとき。このテストは外部 Codex 実行を fake にして、制御ロジックと副作用だけを検証している。

## hash
- 60d8e86895ba75f95c5e06d1d1c0be75df9b62dc2b851d6e7a8bd5b56e7e352a

# `test_session_cli.py`

## Summary
- session サブコマンドの realization test。fork による session branch と session state の作成、linked worktree 上での fork/join/abandon、abandon の正常終了・失敗時 rollback・home branch 不在時の出力、join の conflict resolution・削除 conflict staging・session branch 削除失敗時 warning を検証する。
- 一時 Git repository と CLI runner を使い、branch 遷移、state JSON、標準出力・標準エラー、Codex 実行時の file access profile まで含めて session 操作の外部挙動を確認する。

## Read this when
- session fork が作る branch 名、session state の初期値、session_home_branch、session_start_commit、apply state のテスト期待値を確認したいとき。
- session abandon が home branch へ戻ること、session branch を削除すること、state を abandoned にすること、home branch 不在や cleanup 失敗時の挙動を変更・確認するとき。
- session join が home branch へ戻ること、state を joined にすること、linked worktree 上の branch を保つこと、session branch 削除失敗時に成功扱いで warning を出すことを確認するとき。
- session join の conflict resolution で Codex を REALIZATION_WRITE profile で起動し、対象ファイルを writable、memo と .agents を read-only として扱う制御を確認するとき。
- session 操作のテストで使う一時 repository、current branch 判定、git command、CLI runner、session state path の扱いを追いたいとき。

## Do not read this when
- session サブコマンドの実装本体、状態更新 helper、Codex profile 生成処理そのものを変更したいだけで、テスト期待値を確認する必要がないとき。
- init や他サブコマンドの挙動、session 以外の CLI 出力、repository 作成 fixture の一般仕様を調べたいとき。
- oracle file の正本仕様を確認したいとき。これは realization test であり、正本仕様の代替として読まない。

## hash
- e346d2a3242c44dffc187aae3ff7c4bd31002c030e662baaefeda3f4b48a5dfb
