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
- apply abandon CLI の realization test。active apply run の破棄で apply worktree と apply branch を削除し、session state を ready に戻す外部挙動を検証する。
- cleanup 対象が既に無い場合の warning、running apply process の停止、PID 再利用や既終了 process の扱い、異常 state で破棄を拒否して状態を保つ制御を扱う。
- 通常 repo、session worktree、apply worktree、linked session worktree から実行した場合の cwd 復帰、dirty check、stale apply branch 拒否を確認する。

## Read this when
- apply abandon の CLI 挙動、出力、終了コード、state 遷移、apply worktree・apply branch の削除条件を変更する時。
- running apply process の停止処理、process id 保存ファイルの削除、PID 再利用・既終了 process の race 対応を変更する時。
- linked session worktree や apply worktree 内からの abandon 実行、dirty worktree 検出、active apply branch 判定に関わる挙動を確認する時。

## Do not read this when
- apply fork や session fork の生成処理そのものを確認したいだけの時。
- apply abandon 以外の apply subcommand、review、init などの CLI 挙動を調べる時。
- 正本仕様断片を確認したい時。この対象は realization test であり、仕様判断の入口ではない。

## hash
- 18d63c61d6acdb7bab1a8298e26152d0942d65c9b8a6f8e9260c5d2c146ff9a9

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
- apply fork CLI の統合的な挙動を検証する realization test。Codex 実行結果を fake に差し替え、report 生成、変更要約、commit message、dirty file 再検査、収束判定、編集禁止差分の error 化、rolling apply fork の対象選択と状態更新を確認する。

## Read this when
- `apply fork` の CLI 終了コード、標準出力、report 内容、session state、apply branch commit message の挙動を変更・確認したいとき。
- apply 後に発生した dirty file を再検査する制御、特に `INDEX.md` を再検査対象から除外する挙動を確認したいとき。
- apply fork の収束・未収束・error の判定、または上限回数到達時の扱いを変更したいとき。
- `.agents` など編集禁止対象への差分検出と、その結果を CLI 出力・report・state に反映する処理を確認したいとき。
- rolling apply fork が前回 apply の oracle snapshot commit と join 後の oracle 変更から調査対象を選ぶ挙動を確認したいとき。

## Do not read this when
- apply fork 以外の apply command、session command、init command の単体挙動だけを確認したいとき。
- Codex 実行 wrapper 自体の入出力仕様や実 LLM 品質を確認したいとき。
- report の markdown レンダリング規則だけを詳細に確認したいとき。
- 個別 helper の内部実装だけを確認したいとき。ただし CLI 経由の外部挙動に影響する場合は読む。

## hash
- 096257c5874c5536189018f3a722f0c9efdae580bbf39f9b2d5b1445447ba14a

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
- cmoc の基本的な runtime 挙動を横断的に検証する realization test。パス token 解決、時間表示、repo root と work root の識別、設定既定値、構造化エラー表示、session/apply branch 状態、CLI エラー出力、補完 probe、.cmoc ignore、file access mode、binary 判定、Codex profile のファイルアクセス制御を扱う。

## Read this when
- runtime の基礎挙動や CLI 実行前後の安全制御を変更し、その外部挙動を確認したいとき。
- path model、設定既定値、エラー markdown、branch session state、gitignore 更新、file access mode から sandbox mode への変換、Codex profile の permission profile 生成に関わる実装を変更するとき。
- CLI のエラーが stdout に出ること、補完 probe で cmoc preflight や副作用を避けること、work root 以外で init を拒否することを検証したいとき。

## Do not read this when
- 個別サブコマンドの正常系 workflow やユーザー操作全体の仕様を追いたいだけで、runtime の基礎部品や安全制御に触れないとき。
- oracle file の正本仕様や自然言語仕様を確認したいとき。
- Codex CLI や LLM の出力品質そのものを検証したいとき。

## hash
- c3404b46b12a99d6f68104a300885136d78816e078619287714470bffd0cdc91

# `test_cli_init_tui.py`

## Summary
- CLI の初期化処理と TUI 起動処理の実現テストをまとめた対象。init が .cmoc の追跡解除、.gitignore 更新、既存 staged/unstaged 変更の保全、linked worktree での初期化、既定 config 生成と既存値を保った defaults 同期を行うことを検証する。
- TUI について、エディタで作成された依頼文からパラメータ解決用 prompt と実行用 prompt を生成し、Codex 呼び出しへ適切な model、reasoning effort、file access mode、extra read path、root/cwd を渡すことを検証する。
- Markdown prompt parser について、fenced code block 内の見出し記法を見出し扱いしないことと、先頭見出し前の本文を通常本文として保持することを検証する。

## Read this when
- init サブコマンドの git 操作、.cmoc の ignore 状態、初期コミット、既存 index/worktree 変更の保全、linked worktree 対応を変更または確認するとき。
- 初期 config の既定値、既存 config への default 補完、ユーザー指定値を上書きしない挙動を変更または確認するとき。
- TUI のエディタ起動、依頼文の整形、パラメータ解決用 Codex 実行、TUI 用 Codex 実行、prompt ログ保存先、linked worktree での root/cwd/schema 配置を変更または確認するとき。
- Markdown prompt を section 化する処理で、見出し検出、fenced code block、見出し前本文の扱いを変更または確認するとき。

## Do not read this when
- CLI の init や TUI 起動に関係しないサブコマンドの挙動だけを調べるとき。
- Codex 呼び出し wrapper や preflight の低レベル実装だけを調べるときは、まず該当する実装または専用テストへ進めばよい。
- 設定 schema の全体構造や全設定項目の意味を確認したいだけのときは、設定定義や config 生成実装を直接読む方が適切。
- Markdown prompt parser 以外の Markdown 変換、表示、ドキュメント生成を調べるとき。

## hash
- 583100d94f6dc4d56c9feef455ebb1503feabd959eb2c2308a76daf90315f8da

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
- cmoc の indexing サブコマンドとインデックス生成処理に関する realization test。INDEX.md の生成・再生成・コミット、未初期化や未コミット差分での失敗、linked worktree 上での実行、fresh hash による Codex 呼び出し省略、衝突解消、semantic field の検証、兄弟エントリーの並列生成、root 直下 memo 除外と nested memo 対象化を検証する。

## Read this when
- indexing サブコマンドの外部挙動、git commit 対象、dirty worktree の扱い、linked worktree での実行先を変更・確認するとき。
- INDEX.md エントリー生成の Codex structured output 呼び出し、fresh hash 判定、 malformed entry の再生成、semantic field validation を変更・確認するとき。
- インデックス更新対象の探索、兄弟要素の並列処理、root 直下 memo と nested memo の扱いを変更・確認するとき。
- INDEX.md の merge conflict を自動解消する処理や、index path だけを commit する制御を変更・確認するとき。

## Do not read this when
- init コマンド自体の設定生成や .cmoc 初期状態の詳細だけを調べるときは、初期化処理側の実装・テストを読む。
- Codex 実行ラッパーの低レベルな subprocess 呼び出しやプロンプト構築の詳細だけを調べるときは、Codex 実行処理側を読む。
- oracle file の正本仕様や INDEX.md ルーティング文書の書き方自体を確認するときは、oracle 配下の該当文書を読む。

## hash
- e8a9a38b800797553edc3096b3d6fd9b97b901ff49eecb5e050169093ff1e986

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
- プロンプト部品と実行パラメータ生成のテスト群。構造化ドキュメントの Markdown 描画、routing rule や各種 standard の挿入条件、file access rule のモード別文言、apply fork・review oracle・session join・TUI resolve・indexing 向けパラメータのモデル設定や schema 制約を検証する。
- プロンプト組み立てが、oracle/realization の基準用語、INDEX ルーティング、補助プロンプト、コードブロック、空行正規化、標準文書の既定オン/オフを期待どおり扱うかを確認する入口になる。

## Read this when
- プロンプト部品を生成する関数、標準文書を組み込む complete prompt、または StructDoc の Markdown 描画仕様を変更する。
- file access mode ごとの読み書き制約文言や、apply fork・review oracle・session join・TUI resolve・indexing の実行パラメータを変更する。
- structured output schema の制約、特に変更要約、TUI パラメータ選定、review oracle finding merge の妥当性検証を確認・更新する。
- oracle file、realization file、INDEX.md、標準用語など、プロンプト内に保持すべき基準語句が欠落・混入していないか調べる。

## Do not read this when
- 個別 CLI コマンドの実行挙動やファイルシステム操作の実装だけを調べたい場合。
- プロンプト本文やパラメータ builder ではなく、アプリケーション本体の業務ロジック、永続状態、Git 操作の詳細を追う場合。
- 特定の schema ファイルそのものの定義内容を確認したいだけで、テストが期待する検証観点を知る必要がない場合。

## hash
- df8011452d8944ac440ad78a94a0f5644bd671fd2575545cea11f94673651bd2

# `test_review_oracle_cli.py`

## Summary
- レビュー用サブコマンドの oracle 検査フローに対する realization test。レポート生成、対象 oracle の選定、finding の列挙・検証・判定・マージ、レビュー用 worktree で生成されたルーティング文書の取り込み、失敗時レポート、想定外差分の拒否を検証する。
- CLI 呼び出しと内部レビュー処理の両方を扱い、Codex 実行は fake に差し替えて、外部モデル出力ではなく制御ロジックと副作用を確認する。

## Read this when
- レビュー用 oracle 検査コマンドの挙動、出力レポート、対象スコープ、短縮オプション、エラー時表示を変更する。
- oracle 対象ファイルの選定で、全体スコープ、セッションスコープ、gitignore 対象の除外、対象なしの場合の扱いを確認する。
- finding の列挙結果を次ループへ渡す条件、別 oracle への混入防止、merge operation の契約や不正操作の拒否を変更する。
- レビュー用 worktree で生成されたルーティング文書の取り込み、merge conflict 解決、レビュー後の worktree 配置や清掃条件を変更する。
- レビュー処理中の失敗時に部分結果をどうレポートするか、またレビュー処理が許可されない非ルーティング文書差分を作った場合の拒否を確認する。

## Do not read this when
- 通常の初期化、セッション作成、git helper、設定読み込みなど、レビュー用 oracle 検査フローに直接関係しない CLI 挙動だけを調べる。
- oracle 正本仕様そのものの内容や書き方を確認したい場合。
- Codex CLI や LLM の実出力品質、prompt 文面の妥当性そのものを評価したい場合。
- 一般的なテスト支援 fixture やリポジトリ作成 helper の実装詳細だけを調べる場合。

## hash
- 36dee3fd11c51a58a7b6599fd34fe951ae9616f85bd5aa19fbdc3f37af0604f0

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
