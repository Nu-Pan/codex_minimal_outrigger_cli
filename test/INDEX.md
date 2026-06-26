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
- apply fork の CLI 挙動を検証する realization test。Codex 実行を fake に差し替え、apply run が session state、apply branch、worktree、process pid、対象 path を期待どおり更新・削除・保持するかを確認する。
- 通常 repository と linked worktree の両方で、apply run の開始位置、oracle snapshot commit、apply branch の HEAD、worktree 配置が正しく扱われることを検証する。
- 設定読み込み失敗、.cmoc が git 追跡対象になっている場合、root 直下 memo の除外、.gitignore の保持・編集対象化といった apply fork 周辺の境界条件を扱う。

## Read this when
- apply fork サブコマンドの正常完了時に session state、apply branch、apply worktree、process pid のライフサイクルがどう検証されているかを確認したいとき。
- linked worktree 上で apply fork を実行した場合の branch、HEAD、worktree 配置に関するテストを確認したいとき。
- apply fork が .gitignore や .cmoc 追跡状態をどう扱うべきか、session 側を dirty にしない条件を確認したいとき。
- apply fork の設定読み込み失敗時に apply run を開始しないこと、または対象 path 正規化で root 直下 memo だけを除外することを確認したいとき。

## Do not read this when
- Codex 実行そのものの品質や LLM 出力内容を検証したいとき。このテストは Codex 呼び出しを fake にして制御ロジックと副作用だけを確認する。
- apply fork 以外の apply サブコマンド、review 系コマンド、または session fork 単体の挙動を調べたいとき。
- CLI の利用者向け仕様文や正本仕様断片を確認したいとき。この対象は realization test であり、正本仕様そのものではない。
- 実装 helper の内部設計だけを調べたいとき。外部挙動や永続状態の検証ではなく内部実装を読む必要がある場合は、対応する実装側を直接読む。

## hash
- 3cac7de41b8905c954548167eab000c00b8e33c64062aa4830c203cdd16c31b3

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
- `apply join` CLI の結合処理を対象にした realization test。apply worktree の通常 join、apply worktree 内からの実行、成功時の worktree・branch cleanup、session 状態更新、join report 生成を検証する。
- apply worktree が dirty な場合の失敗、失敗時に apply 状態を completed のまま保つこと、ログ保存先が session root 側になること、エラー文言の出力先も検証する。
- apply 側の想定外差分、`--force-resolve` による差分破棄、許容される `.gitignore` 差分、merge conflict の報告、INDEX conflict の通常モード解決継続をまとめて扱う。

## Read this when
- `apply join` の外部挙動、成功時 cleanup、状態ファイル更新、join commit 記録、report 出力を変更・確認したいとき。
- apply worktree から `apply join` を実行する場合の cwd 復帰、cleanliness check、ログ保存先、dirty worktree エラー表示を確認したいとき。
- apply branch の差分分類、oracle などの想定外差分検出、`.gitignore` 差分の許容、`--force-resolve` の挙動を変更・確認したいとき。
- `apply join` 中の merge conflict 報告、未解決 conflict 時の中止、INDEX conflict を通常モードで解決して継続する制御を確認したいとき。

## Do not read this when
- `apply fork` 単体の Codex 実行、apply worktree 作成、fork 時の状態生成だけを確認したいとき。
- session fork、init、git helper、test fixture の基本挙動だけを確認したいとき。
- oracle file の正本仕様、ルーティング文書、INDEX.md 生成規則そのものを確認したいとき。
- `apply join` 以外のサブコマンドの CLI 出力や状態遷移を調べたいとき。

## hash
- 47fc0068032f463620d8b519547dfee6dd82f2cd4f1e86379a11b603d0572222

# `test_basic_runtime.py`

## Summary
- cmoc の基本ランタイム挙動を広く検証する realization test。パスモデル、実行 root 判定、設定既定値、エラー表示、session/apply branch 形状、CLI preflight、補完プローブ、.cmoc ignore、file access mode、binary 判定、Codex profile のファイルアクセス制御を扱う。
- 単一機能の詳細テストというより、runtime・state・config・CLI・profile など横断的な基礎挙動の回帰検出入口として位置づけられる。

## Read this when
- cmoc の基本 runtime API、CLI 起動前後のエラー処理、work root 判定、linked worktree 判定、または .cmoc の gitignore 管理を変更する。
- file access mode、sandbox mode、Codex profile における read/write/read_only/deny_read の組み立てや、memo・oracle・.agents のアクセス制御を変更する。
- branch 名から session id を解釈する処理、apply branch の形状検証、branch ごとの state 読み込みを変更する。
- 設定既定値、model class、reasoning effort、duration 表示、binary 判定など、複数箇所から使われる小さな基礎 helper の互換性を確認する。
- CLI のエラー出力先、Typer の引数解析失敗時の表示、shell completion probe 時の副作用抑制を確認する。

## Do not read this when
- 特定サブコマンドの正常系 workflow や入出力詳細だけを確認したい場合は、そのサブコマンド専用のテストまたは実装を先に読む。
- oracle file の正本仕様そのものを確認・編集したい場合は、realization test ではなく該当する oracle doc または oracle src を読む。
- UI 表示、LLM 出力品質、外部サービス連携など、このテストが扱っていない領域の挙動を調べる場合は読まなくてよい。
- 単純に import 先の関数やクラスの実装責務を理解したい場合は、この横断テストではなく該当する実装モジュールを直接読む。

## hash
- 8641df930920543899d0ca81ae78735b56b33d38a118f2cfa677b54e40cb4a51

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
- cmoc の indexing と INDEX.md 更新処理に関する realization test。CLI 実行時の初期化前エラー、未コミット差分の拒否、生成済みエントリーの再利用、linked worktree 対象化、INDEX.md だけをコミットする制御、競合解消時の INDEX.md 削除コミット、エントリー描画時の semantic field 検証を扱う。
- indexing 実装が Codex によるエントリー生成、hash freshness 判定、malformed entry の再生成、兄弟要素の並列生成、ルート直下 memo 除外とネストした memo の扱いを満たすか確認する入口となる。

## Read this when
- indexing サブコマンド、INDEX.md の生成・更新・コミット、または既存 INDEX.md の freshness 判定を変更する。
- 未初期化リポジトリ、dirty worktree、linked worktree、merge conflict など、indexing 周辺の git 状態制御を変更する。
- render_index_entry や build_index_entry の structured output 受け入れ条件、空リスト・非文字列・欠落 field のエラー処理を変更する。
- ルート直下の memo を indexing 対象から外す処理、または下位階層にある同名ディレクトリを通常対象として扱う処理を確認する。
- INDEX.md 更新処理の並列化や、同階層要素のエントリー生成順序・実行制御に関わる実装を触る。

## Do not read this when
- 個別サブコマンドの通常動作だけを調べたい場合は、そのサブコマンドの実装または対応する専用テストを先に読む。
- INDEX.md エントリー本文の正本仕様や人間向けルーティング文書の書き方を確認したい場合は、oracle 側の仕様断片を読む。
- Codex 実行基盤そのもの、CLI runner の共通 fixture、git test helper の詳細を調べるだけなら、支援モジュールや実装側の該当箇所を読む。
- 生成された INDEX.md の内容を人間がどう解釈するかだけが関心で、indexing の制御フローや副作用を検証しない場合は、このテストを読む優先度は低い。

## hash
- 68a9ca8e65c3b1750cfffb92daa8a88aaff50a543981bc16fade83083575dbd1

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
- `review oracle` サブコマンドの realization test。レポート生成、scope 指定、対象 oracle の選別、linked worktree 上のレビュー、finding の列挙・検証・判定フロー、merge operation の契約、レビュー用 worktree が作る `INDEX.md` 差分の取り込みと衝突解決、処理失敗時の error report、許可されない非 `INDEX.md` 差分の拒否を検証する。
- CLI 経由の結合的な挙動と、review oracle 処理を支える一部の制御ロジックを同じテスト群で扱う入口。Codex 実行は fake に差し替え、git repository と worktree を一時領域に作って外部から見える出力・副作用を確認する。

## Read this when
- `review oracle` の CLI 挙動、出力される review report、scope の既定値や `full` 指定、短縮 option の扱いを変更・確認したいとき。
- review 対象となる oracle の選別条件を確認したいとき。特に session scope と full scope、gitignored oracle、binary oracle、linked worktree 上の oracle の扱いが関係するとき。
- finding の列挙ループ、過去 findings を同一 target にだけ渡す制御、validate・judge の呼び出し、merge operation の delete・replace・merge 契約を変更するとき。
- review oracle が作成した `INDEX.md` 差分の取り込み、review worktree の配置、不要な review worktree の残存防止、merge conflict 解決の挙動を扱うとき。
- review 処理中の例外時に error report を残す挙動や、review oracle が `INDEX.md` 以外の差分を作った場合の拒否・復元挙動を変更するとき。

## Do not read this when
- oracle 正本仕様そのものの記述方針や内容を確認したいだけのとき。この対象は realization test であり、正本仕様の代替ではない。
- review oracle 以外のサブコマンド、設定読み込み一般、session fork 一般、path model 一般の挙動を調べたいとき。より直接その機能を扱う実装またはテストへ進む方がよい。
- Codex CLI や LLM の実際の出力品質を検証したいとき。この対象は Codex 実行を fake に差し替え、cmoc 側の制御と副作用を検証している。
- 単体の helper 実装詳細だけを確認したいとき。まず対象 helper の実装や、より局所的なテストを読む方がよい。

## hash
- 971097a7295ff76cdcf84a1405d5c1c474a6fd606faa7ca4e835ad73d82e464c

# `test_session_cli.py`

## Summary
- session サブコマンドの CLI 挙動を検証する realization test。session fork による session branch と state file の作成、linked worktree からの fork、session abandon の home branch 復帰・branch 削除・state 更新・失敗時 rollback、session join の conflict 解決・linked worktree handling・delete conflict staging・branch 削除失敗時 warning を扱う。
- 一時 Git repository を作り、Typer runner と git command を通して外部挙動、永続 state、現在 branch、出力内容、Codex 実行 profile の file access mode と writable/read-only path を確認する。

## Read this when
- session fork、session abandon、session join の CLI 挙動や状態遷移を変更する。
- session branch の命名、作成、削除、home branch への復帰、linked worktree 上での session 操作を変更する。
- session state JSON の key、state 値、session_home_branch、session_start_commit、join/abandon 後の保存内容を変更する。
- join 時の merge conflict 解決、Codex 実行 purpose、REALIZATION_WRITE profile、oracle/memo/.agents などの file access permission を変更する。
- abandon や join の失敗時出力、cleanup failure の rollback、session branch 削除失敗時の warning 出力を変更する。

## Do not read this when
- session 以外のサブコマンドや、CLI entrypoint 全体の構造だけを確認したい。
- Git 操作 helper、repository fixture、runner fixture の汎用的な作りだけを調べたい場合は、test support 側を直接読む。
- Codex profile 生成そのものの詳細や permission schema の実装を変更する場合は、profile 生成側の実装を直接読む。
- oracle 正本仕様や routing 文書の方針を確認したいだけで、session CLI の realization test の期待値を確認する必要がない。

## hash
- 3a0eaf0b33b63a15ac5b335cd6b59ed96c60a488715fc01181be60f72fa9dd3a
