# `_support.py`

## Summary
- realization test 群で共通利用するテスト補助モジュール。Typer の CLI runner、git 操作、最小リポジトリ作成、Codex home 準備、Python 実行ファイル生成、apply 用 worktree 解決など、CLI テストの前提環境を組み立てる小さな helper をまとめている。
- 実装本体や個別サブコマンドの仕様を直接検証する本文ではなく、複数のテストが同じセットアップや状態確認を共有するための入口として位置づけられる。

## Read this when
- CLI テストで一時 git repository、初期 commit、user 設定、oracle ディレクトリ、ignored な oracle file などの共通 fixture を作る helper を確認・再利用したいとき。
- テスト内で CODEX_HOME、auth.json、実行可能な Python スクリプト、Typer CliRunner、現在 branch 名、apply branch に対応する worktree path を準備・取得する既存 helper を探すとき。
- テスト失敗の原因が共通セットアップ、git command 呼び出し、テスト用 repository の初期状態、または shared import の差し替え対象にありそうなとき。

## Do not read this when
- 個別サブコマンドの期待動作、入出力、永続状態、エラー条件を確認したいだけのときは、対象サブコマンドの実装または個別テストを読む。
- path token、sandbox mode、preflight、TUI prompt parsing などの本体ロジックを理解・変更したいときは、対応する implementation module を直接読む。
- テストケース固有の assertion や scenario を探しているときは、この共通 helper ではなく該当する test module を読む。

## hash
- f6f7fe7881a530da660ffebd31555224dfde6ff5aee8d86792527e253c949bad

# `test_apply_abandon_cli.py`

## Summary
- `apply abandon` コマンドの realization test。apply run 破棄時に apply worktree と apply branch を掃除し、状態を `ready` に戻す外部挙動を CLI 経由で検証する。
- cleanup 対象が既に消えている場合の warning、running 状態の process 停止、process id 不在時の拒否、apply worktree を導出できない状態の拒否、apply worktree 内からの実行、stale apply branch からの誤破棄拒否を扱う。

## Read this when
- `apply abandon` の CLI 挙動、出力文言、終了コード、session state の更新、apply worktree・apply branch の削除条件を変更または確認するとき。
- apply run の running/completed/ready 状態遷移、apply process id の扱い、cleanup 失敗や対象欠落時の warning/error 境界を確認するとき。
- 現在位置が apply worktree や stale apply branch の場合に、破棄対象をどう判定するかを調べるとき。

## Do not read this when
- `apply fork` の生成処理そのもの、Codex 実行結果の品質、review findings の内容を調べたいだけのとき。
- session fork、init、git worktree helper など、apply abandon 以外の CLI 基盤挙動を直接確認したいとき。
- oracle file の正本仕様を確認したいとき、または実装ファイル側の内部関数分割や helper 実装を読むべきとき。

## hash
- d9e1345db5eb3885badbb85781e46d4b37406d7a34cec2b8daeecf11b6b48904

# `test_apply_fork_cli.py`

## Summary
- apply fork コマンドの realization test。Codex 実行を fake に差し替え、apply fork が session から apply branch/worktree を作って完了状態へ進めること、設定読み込み失敗時に apply run を開始しないこと、.gitignore と memo 対象の扱いが期待どおりであることを検証する。

## Read this when
- apply fork の CLI 挙動、状態更新、apply branch/worktree 作成、apply_process pid の削除、完了後 state の内容に関するテストを確認・変更するとき。
- apply fork が Codex loop や findings 列挙・適用・commit message・change summary 生成をどのように呼ぶ前提でテストされているか確認するとき。
- apply fork の設定ファイル読み込み失敗時に、branch/state/pid などの apply run 副作用を発生させない挙動を検証するとき。
- apply fork 実行時の .gitignore 保持、apply branch 側での .gitignore 編集、root 直下 memo 除外と入れ子 memo 対象維持のテスト観点を確認するとき。

## Do not read this when
- apply fork 以外の CLI サブコマンド、session fork や init そのものの仕様・実装を調べたいとき。
- Codex 実行結果の品質、LLM 出力内容、実際の Codex CLI 呼び出し統合を検証したいとき。
- apply fork の実装詳細を変更したいが、テスト上の期待ではなく本体処理の責務・分岐・helper を先に確認すべきとき。
- oracle の正本仕様断片を確認したいとき。

## hash
- 96334821599926930ec6a5ce4705019aba251f4e40f3d480201b275906dfa39b

# `test_apply_fork_report_cli.py`

## Summary
- apply fork の CLI 挙動のうち、report 生成、dirty file 再検査、編集禁止対象への差分拒否、rolling apply fork の対象選択を検証する realization test。
- 未収束 report の変更要約・commit message、収束までの再検査、forbidden diff 時の error state/report、前回 apply の oracle snapshot commit を基準にした rolling apply を扱う。

## Read this when
- apply fork が Codex の所見列挙、所見適用、commit message 生成、変更要約生成をどの目的で呼び分けるかを検証したいとき。
- 未収束・収束・error の apply report に、結果、終了理由、変更要約、commit message、return code がどう反映されるかを確認したいとき。
- apply 後の dirty file を再検査し、生成された routing document を再検査対象から外す制御を確認したいとき。
- 編集禁止対象への差分を検出した場合に、error state と report へ落とし込み、変更要約生成を行わない挙動を確認したいとき。
- rolling apply fork が前回 apply の oracle snapshot commit を基準に対象を選び、join 済み snapshot 情報を session state に反映する挙動を確認したいとき。

## Do not read this when
- apply fork の基本的な state/worktree/branch 更新、設定読み込み失敗、`.gitignore` 保持、target 正規化だけを確認したいときは `test_apply_fork_cli.py` を読む。
- apply fork 以外の apply/join/session/init コマンド全般の仕様や実装入口を探しているだけのとき。
- report renderer、state model、path model、git helper などの個別実装を直接変更したいとき。

## hash
- 125ad7f741a18e3f064566dab600e1301290dd82ed60ea1f5ca0bc2a6538253a

# `test_apply_join_cli.py`

## Summary
- `apply join` の CLI 挙動を検証する realization test。apply worktree の削除、apply branch の削除、session state の ready 復帰、oracle snapshot commit の記録、report 生成、作業ディレクトリ復帰、未コミット差分・想定外差分・merge conflict・INDEX.md conflict の扱いを、実際の git repository と CLI runner で確認する。

## Read this when
- `apply join` の外部挙動、終了コード、標準出力、report 内容、state 更新、worktree/branch cleanup を変更または確認する場合。
- apply worktree から `apply join` を実行したときの cwd 復帰、cleanliness check、ログ保存先を確認する場合。
- apply 側の oracle 変更、`.gitignore` 変更、通常 merge conflict、INDEX.md conflict、`--force-resolve` の扱いに関する回帰テストを確認する場合。

## Do not read this when
- `apply fork` の Codex 実行内容そのものや fork 作成処理だけを確認したい場合。
- session 作成、path model、state schema、git helper の単体仕様を調べたい場合。
- oracle file の正本仕様や自然言語仕様を確認したい場合。

## hash
- 151af6278fea5ccce789f55154a543387ee602c7adbd4164e8c56c660d66cb68

# `test_basic_runtime.py`

## Summary
- cmoc の基礎的な runtime 挙動を横断的に検証する realization test。パス token 解決、duration 表示、repo root と work root の判別、設定 default、エラー Markdown 出力、CLI preflight と parse error、.cmoc ignore、file access mode、binary 判定、Codex profile の filesystem 権限生成を扱う。
- 個別機能の単体テストというより、runtime helper・CLI entrypoint・permission profile の基本契約が実装全体で崩れていないかを確認する入口になる。

## Read this when
- cmoc の実行場所判定、worktree 判定、path token 表記、または `<cmoc-root>` などの path model に関わる挙動を変更する時。
- CLI エラー表示、引数解析失敗、completion probe、preflight、stdout/stderr の使い分けを変更する時。
- file access mode、sandbox mode、Codex profile、oracle・memo・.agents の read/write/read_only/deny_read 権限生成を変更する時。
- 設定 default、reasoning effort、model class、.cmoc の gitignore 登録、binary 判定など、runtime の基本 helper の外部挙動を確認したい時。

## Do not read this when
- 特定サブコマンドの詳細な業務フロー、永続状態の個別 schema、または UI/TUI の表示内容を調べたいだけの時は、その責務を持つ実装・テストへ直接進む。
- oracle file の正本仕様そのものを確認したい時は、実装テストではなく該当する oracle doc または oracle src/test を読む。
- 単一 helper の内部実装方針だけを調べたい時は、まず該当する runtime module や support fixture を読む。

## hash
- 8961b01452ba7a8c3079c02808be3acf6a26714966b7da9ca6b19e64e94f9bc8

# `test_cli_init_tui.py`

## Summary
- CLI の初期化処理と対話型起動処理を、実リポジトリ・Git・作業ツリー・疑似エディタ/疑似 Codex 実行を使って検証する realization test。
- .cmoc の ignore/追跡解除、初期化時コミットの対象制御、設定ファイル既定値の生成・同期、sub_command ログ、linked worktree 上の初期化と TUI プロンプト保存先を扱う。
- Markdown プロンプト解析について、コードフェンス内の見出しを無視することと、見出し前の本文を保持することも検証する。

## Read this when
- init サブコマンドが .cmoc を ignore し、既存の .cmoc 追跡ファイルを untrack し、必要な cleanup commit だけを作る挙動を確認・変更する時。
- 初期化時に利用者の既存 staged change や .gitignore の staged/unstaged 変更を壊さない Git 操作を確認・変更する時。
- linked worktree 上で init や tui を実行した時の root/cwd、.gitignore、config、ログ、schema、commit 対象の扱いを確認・変更する時。
- config の既定値生成、既存の人間設定を保持した defaults 同期、モデル名・reasoning effort・apply/review 設定の補完を確認・変更する時。
- tui サブコマンドがエディタで作成された依頼文を整形し、不要なコメントを除去し、parameter resolve 用 Codex 実行と本体 TUI 実行へ正しい parameter・purpose・extra_read_paths を渡すか確認・変更する時。
- sub_command ログに command_invoked イベント、実行 command、argv が記録される挙動を確認・変更する時。
- Markdown プロンプト parser の見出し抽出、コードフェンス内見出しの扱い、見出し前 preamble の扱いを確認・変更する時。

## Do not read this when
- init や tui の外部挙動ではなく、低レベルな path model、schema 定義、設定 dataclass だけを局所的に確認したい時は、それらの実装または単体テストへ直接進む。
- Codex CLI や外部 LLM の実際の出力品質を確認したい時。この対象は疑似実行・呼び出し parameter・保存副作用を検証しており、LLM 品質自体は扱わない。
- 一般的な CLI command 登録や Typer の配線だけを確認したい時は、CLI 実装やより小さい command 単位のテストを優先する。
- Markdown parser 以外の文書処理、INDEX.md 生成、oracle/realization ルーティング仕様を確認したい時は、それぞれの専用実装・テストへ進む。

## hash
- 5419f2b7f51994350b24a8b5fd73f3b673f998f764a0b7fd12411688e1b46444

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 呼び出しの実行系に対する realization test。exec 経路ではプロンプトを標準入力で渡すこと、構造化出力 schema の配置、CODEX_HOME と一時 profile、呼び出しログ・stdout/stderr ログ・subcommand log・コンソール表示、repository config の model/reasoning_effort 反映を検証する。
- TUI 経路では codex コマンドの引数形式、prompt 引数渡し、workspace write profile の writable/read-only 設定、call log と logger イベント、戻り値を検証する。
- realization write の exec 実行が、許可された conflict 対象以外の oracle path 変更を検出して CmocError にすることも検証する。

## Read this when
- Codex CLI を起動する runtime wrapper、特に exec/TUI の argv、cwd、環境変数、profile 生成、出力 schema、ログ出力を変更する時。
- AgentCallParameter の model class、reasoning effort、file access mode、extra read paths、target oracle paths が Codex profile や実行制御へ反映される挙動を確認する時。
- Codex 実行後の oracle 変更検査、特に conflict 対象外の oracle file 変更を拒否する制御を変更・調査する時。
- repository config の codex model や reasoning_effort が exec 用 profile に反映される挙動を確認する時。

## Do not read this when
- Codex CLI 呼び出しではなく、通常の cmoc サブコマンド引数解析や Git 操作だけを調べる時。
- oracle file の正本仕様本文を確認したい時。ここは realization test であり、仕様判断の根拠としては oracle 側を先に読む。
- INDEX.md 生成・ルーティング文書そのものの形式や schema を調べたい時。
- Codex 実行 wrapper と関係しない parser、path model、または一般的な補助関数の単体挙動だけを調べる時。

## hash
- 18d917636c9a31eaa429fff390bf86a56ef5a3a6930c5b807c0c210ea97ce549

# `test_codex_runtime_home.py`

## Summary
- Codex CLI 実行時に使う Codex home の決定、環境変数の引き継ぎ、認証情報の事前検証を扱う realization test。`CODEX_HOME` 未設定時は通常の home 配下を使い、設定済みの場合はその値を実行環境へ保持しつつ内部では実体パスとして扱うことを確認する。
- Codex home が存在しない、ディレクトリでない、または認証情報を欠く場合に、Codex CLI を起動する前に cmoc のエラーとして失敗する境界を検証する。

## Read this when
- Codex CLI 呼び出し前の `CODEX_HOME` 解決、既定の Codex home、相対指定された Codex home、または実行ログに記録される Codex home の扱いを変更・確認したいとき。
- Codex home や認証情報の存在確認に関する失敗条件、エラーメッセージ、next actions、または Codex CLI を起動する前に止める制御を変更・確認したいとき。
- Codex CLI を fake executable に差し替えて、渡される環境変数・引数・profile path・call log を検証する既存テストの書き方を確認したいとき。

## Do not read this when
- Codex CLI 実行そのものではなく、oracle file と realization file の分類、INDEX.md 生成、パスモデル定義などリポジトリ構造の仕様を調べたいだけのとき。
- Codex home や認証情報に関係しない model class、reasoning effort、file access mode、prompt 内容、または LLM 出力品質のテストを探しているとき。
- 実装側の Codex home 解決ロジックやエラー生成処理を変更する目的で、テストではなく本体コードから読み始めるべきとき。

## hash
- 00c1dba79050b8c04fb4dcf91e3b68e7d21dd4f7e532d774775356d9e0d59d24

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex CLI 実行が quota exceeded で失敗した後の待機、空き確認用 probe、resume または再実行、ログ記録を検証する realization test。
- 偽の codex 実行ファイルを使い、quota 復旧後に最後の出力 JSON、call log、subcommand log、コンソール表示が期待通りになることを確認する。
- 並列に quota が発生した場合、代表 1 件だけが quota availability probe を実行し、各呼び出しが resume して成功する制御も扱う。

## Read this when
- run_codex_exec の quota exceeded 検出、quota polling、resume token 利用、resume token が無い場合の再実行挙動を変更する時。
- Codex 呼び出し時の CODEX_HOME、PATH 上の codex、標準入力、--json、--output-last-message、profile 引数の渡し方に関するテストを確認する時。
- quota availability probe の call log、stdout/stderr/output 保存、SubcommandLogger の codex_call event、コンソール出力の期待値を変更・調査する時。
- 複数スレッドで同じ quota 状態に入った時、probe を重複させず各実行を復旧させる同期制御を確認する時。

## Do not read this when
- quota retry と無関係な通常成功時の Codex 実行、引数組み立て、出力解析だけを調べる場合。
- Codex CLI 以外のサブコマンド、oracle 処理、path model、リポジトリ生成などの仕様や実装を調べる場合。
- 実際の Codex CLI や LLM の応答品質、ネットワーク越しの quota 状態そのものを検証したい場合。

## hash
- a50db850f7382abc5a63081ab517215d310b587d63021d848ec6a01928539917

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 実行ラッパーの retry 挙動を検証する realization test。構造化出力の schema validation 失敗後の再試行、capacity エラー検出後の再試行、JSONL ではない stdout/stderr 上の error marker を retry 条件として扱わない境界を、fake codex 実行ファイルとログ副作用で確認する。
- retry 結果の output_json、call log、stdout log path、subcommand log の codex_call event status と returncode を合わせて検証し、外部コマンド呼び出しの制御ロジックと観測可能なログ契約の入口になる。

## Read this when
- Codex CLI 呼び出しの再試行条件、特に schema validation retry、capacity retry、quota/capacity marker の検出範囲を変更する。
- Codex CLI 呼び出しログ、call log path、stdout log path、subcommand log の codex_call event status や returncode の記録仕様を確認・変更する。
- fake codex executable を使った runtime 系テストの書き方や、AgentCallParameter、CmocConfig、SubcommandLogger を組み合わせた実行テストの既存例を確認する。

## Do not read this when
- Codex CLI のコマンドライン引数組み立て、作業ツリー権限、モデル・reasoning effort の選択など、retry 判定やログ副作用に直接関係しない実装を調べたい。
- oracle file の正本仕様や、人間が管理する仕様断片そのものを確認したい。
- 一般的なテスト補助関数、repository fixture、Codex home setup、fake executable 作成 helper の実装詳細だけを調べたい。

## hash
- 0b731069e42e2fa6943b0f7076412ffc3f955e5888b3c433f026e9da9bbf1856

# `test_indexing_cli.py`

## Summary
- indexing コマンド本体と INDEX.md entry 生成・更新の realization test。INDEX.md 生成・更新・commit 対象、fresh hash による再生成スキップ、既存差分との共存、worktree 選択を検証する。
- INDEX.md エントリー生成結果の schema 検証、semantic field の欠落・型不正拒否、空リスト受理、malformed entry の再生成、sibling entry の並列生成、root 直下 memo 除外と nested memo 対象化も扱う。
- merge conflict 解決時に INDEX.md の conflict を削除して merge commit へ進める挙動、および commit_index_updates が INDEX.md 系の更新だけを commit し非 INDEX 差分を残す挙動を確認する。

## Read this when
- indexing コマンド、update_indexes、build/render index entry、fresh hash 判定、INDEX.md の commit 範囲や malformed entry 再生成の挙動を変更・調査するとき。
- INDEX.md merge conflict の自動解決、root 直下 memo の索引除外、nested memo の索引対象化、sibling entry 生成の並列性に関する回帰を確認するとき。

## Do not read this when
- Codex exec/TUI 呼び出し前に indexing preflight を走らせる制御、purpose による preflight skip、worktree 上での indexing 対象解決、repository lock 待機を扱うときは `test_indexing_preflight.py` を読む。
- 個別 CLI コマンドの通常実行フロー、session 管理、apply 処理、Codex runtime 呼び出しそのものを調べたいだけで、indexing preflight や INDEX.md 更新の副作用が関係しないとき。
- oracle file の正本仕様、path model、INDEX.md エントリー文面の設計方針を確認したいとき。対応する oracle doc や oracle src を読む方が直接的。
- テスト支援 fixture、runner、git helper、mock 用 import の定義を調べたいとき。共通 test support 側を読む方が直接的。

## hash
- eb69c7f5dd360f83c95535d52f0e9c6e934e38ac05d4307356aaf57c300897e0

# `test_indexing_preflight.py`

## Summary
- Codex exec/TUI 呼び出し前の indexing preflight を検証する realization test。preflight が Codex 呼び出し前に走ること、cwd linked worktree を優先すること、TUI でも走ること、repository lock 待機、purpose による skip を扱う。
- indexing コマンド本体の entry 生成や commit 範囲ではなく、Codex runtime preflight wrapper と indexing hook の接続を検証する。

## Read this when
- Codex exec/TUI 呼び出し前に indexing preflight を走らせる制御、purpose による preflight skip、worktree 上での indexing 対象解決、repository lock 待機を扱うとき。
- indexing preflight の登録、無効化、再入防止、skip 条件のテストを変更・調査するとき。

## Do not read this when
- indexing コマンド、update_indexes、build/render index entry、fresh hash 判定、INDEX.md の commit 範囲や malformed entry 再生成の挙動を変更・調査するときは `test_indexing_cli.py` を読む。
- Codex runtime の exec/TUI 起動そのもの、profile/schema/log path 生成、retry 制御を調べたいときは Codex runtime 側のテストを読む。

## hash
- 007e02d6231d12c34829caf2fb8da0ba7d10aab11b2aef15d8fe8cfe7dad6933

# `test_prompt_parts.py`

## Summary
- プロンプト部品と実行パラメータ生成の振る舞いを検証する realization test。レビュー基準、ルーティング規則、ファイルアクセス規則、各種 standard の挿入制御、Markdown レンダリング、構造化出力 schema、モデルクラス・reasoning effort・アクセスモードの選定が期待どおりかを確認する。
- apply fork、review oracle、session join、TUI parameter resolve、index entry 生成など、複数の prompt builder が正しい本文断片・制約語・schema 契約を持つかを横断的に検査する入口になる。

## Read this when
- プロンプト本文を組み立てる builder の変更に対して、期待される標準文書・ルーティング規則・ファイルアクセス規則が出力に含まれるか確認したいとき。
- StructuredDoc の Markdown レンダリング、とくに通常本文の連続空行の畳み込みと code block 内の空行保持に関わる挙動を変更するとき。
- apply fork、review oracle、session join、TUI parameter resolve、index entry 生成の model class、reasoning effort、file access mode、structured output schema の契約を変更または確認するとき。
- index entry standard、realization standard、apply review standard、review oracle standard などの基準文書に含めるべき用語や、含めてはいけない用語の回帰を調べるとき。

## Do not read this when
- 個別 CLI コマンドの実行フロー、永続状態、git 操作、ファイル探索そのものの実装を調べたいだけで、プロンプト生成や schema 契約に関心がないとき。
- 特定の builder の内部実装を修正するだけで、既存テストの期待値を確認する必要がない場合は、まず対象 builder の実装側を読む方が直接的なとき。
- oracle file の正本仕様断片そのものを確認したいとき。この対象は realization test であり、仕様判断の根拠にはならない。

## hash
- 8cfe3ab2ea4784cb4c2a1a7939a05f7610aafb8626f37042d87f0f91f902360f

# `test_review_oracle_cli.py`

## Summary
- `review oracle` コマンドと review oracle ループ周辺の realization test。レポート生成、対象 oracle の選別、finding の merge 操作、失敗時レポート、review 用 worktree からの `INDEX.md` 反映、想定外差分の拒否を検証する。
- Codex 実行を fake に差し替え、CLI 実行結果・生成レポート本文・gitignored oracle の除外・finding merge contract の例外条件など、外部挙動と制御ロジックを確認する入口。

## Read this when
- `review oracle` の CLI 挙動、scope option、レポート内容、エラー時出力、対象 oracle 数の扱いを変更・調査するとき。
- review oracle が gitignored oracle を full/session scope で除外する挙動、または session scope で対象がない場合に Codex 呼び出しを省略する挙動を確認するとき。
- finding の列挙・validate・judge・merge の制御、特に列挙 loop が対象ごとの既存 finding だけを prompt に渡すことや merge operation の kind contract を確認するとき。
- review 用 worktree で生成された `INDEX.md` だけを元 worktree に反映し、それ以外の差分を拒否・破棄する安全性を変更または検証するとき。

## Do not read this when
- review oracle 以外の CLI サブコマンド、session fork/init そのもの、または一般的な設定読み込みだけを調べるとき。
- oracle 正本仕様の内容や oracle file の編集方針を確認したいとき。この対象は realization test であり、正本仕様の根拠にはしない。
- Codex CLI や LLM の実出力品質を検証したいとき。この対象は Codex 実行を fake に差し替え、cmoc 側の制御と副作用を検証している。
- review oracle の実装詳細を直接修正する場所を探しているとき。まず実装側の review oracle 関連モジュールを読む方が直接的。

## hash
- 89b8d6fa3fcf79a4223723ad0951331c1b1fee32cdfa223ca324f98bba735bbb

# `test_session_cli.py`

## Summary
- session サブコマンドの CLI 結合テストをまとめた realization test。session fork による session branch と状態ファイル作成、linked worktree からの fork、session abandon の正常系・home branch 不在・cleanup 失敗時 rollback、session join の merge/conflict 解決・linked worktree・削除競合・session branch 削除失敗 warning を検証する。
- Git 操作、状態 JSON、Typer runner 経由の CLI 出力、Codex conflict resolution 呼び出し条件を同時に確認するため、session 系 CLI の外部挙動を変更する際の入口になる。

## Read this when
- session fork、session abandon、session join の CLI 挙動や状態遷移を変更・調査するとき。
- session branch、session home branch、session_start_commit、apply state、joined/abandoned/active などの session 状態 JSON の期待値を確認したいとき。
- linked worktree 上で session コマンドを実行した場合に、元 worktree と現在 worktree の branch/head がどう扱われるかを確認するとき。
- session join の merge conflict 解決で Codex 実行に渡す目的、file access mode、writable paths、削除競合の staging 処理を確認するとき。
- session abandon や session join の失敗・警告時に、branch が残るか、状態が rollback されるか、利用者向け出力に何を含めるかを確認するとき。

## Do not read this when
- session 以外の CLI サブコマンド、oracle 操作、path model、設定読み込みなどを調査しており、session branch や session 状態の外部挙動に関係しないとき。
- session コマンドの実装詳細だけを追いたい場合。まず対応する実装モジュールを読み、外部挙動の期待値確認が必要になった段階で読む。
- 単体 helper の純粋な入出力や低レベルな Git wrapper の挙動だけを確認したい場合。CLI 経由の session workflow を検証するこの対象より、該当 helper のテストや実装を優先する。

## hash
- 37fc26f35b53b9ff5482d9cb716da99ce3bc41bbc20c5844e11fb2dbfd68cc71
