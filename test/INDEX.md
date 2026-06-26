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
- cmoc の基本ランタイム挙動を広く検証する realization test。パス token 解決、時間表示、repo root/work root 判定、設定 default、エラー markdown、CLI エラー出力、補完 probe、.cmoc ignore、file access mode、Codex profile の権限設定を扱う。

## Read this when
- 基本的な runtime helper、設定 default、エラー表示、CLI preflight、gitignore 更新、file access mode から sandbox mode への変換、または Codex profile の permission 設定に関する既存テストを確認・更新したいとき。
- work root と repo root の区別、linked worktree 上の root 解決、session branch 名の形の拒否、stdout/stderr へのエラー出力先など、cmoc の基礎的な外部挙動の回帰を確認したいとき。
- 権限 profile が read/write/deny_read/read_only/writable_roots をどう出すべきかを、実装変更に対する realization test として確認したいとき。

## Do not read this when
- 個別サブコマンドの通常成功フロー、セッション状態の詳細、oracle 文書の正本仕様、または実装本体の責務を調べたいだけの場合。
- Codex CLI や LLM の出力品質そのもの、外部サービス連携、UI 表示、永続ログ内容の詳細を調べる場合。
- 対象となる helper や CLI 挙動の実装場所を直接読みたい場合は、該当する src 配下の実装を読む方が適切なとき。

## hash
- e2a9c702735fb2b3e209b419ff7e7cc558d2c4161951d3bb4262319072940066

# `test_cli_init_tui.py`

## Summary
- CLI の初期化と対話起動まわりの外部挙動を検証する realization test。初期化時の `.cmoc` 管理対象外化、`.gitignore` 更新、既存 staged/unstaged 変更の保全、linked worktree での root/cwd/state/log の扱い、既定設定ファイルの生成と既存設定値の保持、サブコマンドログ、対話起動時のプロンプト編集・パラメータ解決・Codex 起動条件を扱う。
- Markdown プロンプト解析について、 fenced code block 内の見出し記法を見出し扱いしないこと、見出し前の本文を本文セクションとして保持することも検証する。

## Read this when
- `init` コマンドの git 操作、`.cmoc` の ignore/untrack、初期コミット、`.gitignore` への追記、既存 index/worktree 変更を壊さない挙動を変更または確認するとき。
- 初期設定ファイルの既定値、既存設定との同期、既存の人間設定値を上書きしない挙動を変更または確認するとき。
- linked worktree 上での `init` や対話起動が、main worktree 側と linked worktree 側のどちらに config・log・state・schema・complete prompt を置くかを確認するとき。
- 対話起動でエディタを開き、コメント除去済みの依頼文から実行パラメータを解決し、その結果に応じて Codex TUI を起動する流れを変更または確認するとき。
- サブコマンド起動ログの event、command、argv など、起動した CLI コマンドを識別するログ挙動を確認するとき。
- Markdown プロンプトを見出し単位に分解する処理で、コードブロック内の `#` や見出し前本文の扱いを確認するとき。

## Do not read this when
- 個別の `init` 実装内部 helper の責務やアルゴリズムだけを調べたい場合は、対応する実装ファイルを直接読む方がよい。
- 設定 schema の全項目や正本仕様上の既定値そのものを確認したい場合は、設定定義や oracle 側の該当文書を読む方がよい。
- 対話起動後の Codex/LLM の出力品質や実際の対話 UI 表示を検証したい場合は、この対象は制御ロジックのテストであり直接の入口ではない。
- Markdown 一般仕様や parser 全体の網羅的な挙動を調べたい場合は、ここで扱うのは見出し分解の限定的なケースだけなので、parser 実装またはより直接のテストを読む方がよい。

## hash
- e6b4d44cacfedc87208e49827c66651cfb7cdbeb8976627d0aa935b87643e165

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 呼び出しを包む実行系の realization test。exec 経路ではプロンプトを stdin で渡すこと、CLI 引数へプロンプト本文を露出しないこと、JSON 出力 schema と最終メッセージを扱うこと、CODEX_HOME・profile・call log・stdout/stderr log・subcommand log・console 表示を記録することを検証する。
- worktree を cwd にした exec 呼び出しで、schema 保存先が root 側ではなく cwd 側の `.cmoc/state/schema` になることを検証する。
- TUI 経路では `codex` コマンドを直接起動し、`exec` サブコマンドを使わず、プロンプトを最後の argv として渡すこと、sandbox profile の writable/read-only 設定、call log、subcommand log、console 表示、戻り値を検証する。
- リポジトリ設定から Codex model と reasoning effort を読み込み、生成 profile に反映されることを検証する。

## Read this when
- Codex CLI を実行する runtime 層、特に exec/TUI の argv・stdin・cwd・環境変数・profile 生成・sandbox 設定を変更する時。
- Codex 呼び出しのログ出力、call log、stdout/stderr log、subcommand log、console 表示の仕様や実装を確認する時。
- Structured Output schema の保存場所、worktree 配下での schema パス、`.cmoc/state/schema` の扱いを変更する時。
- `.cmoc/config.json` から Codex model や reasoning effort を読み込む処理を変更する時。

## Do not read this when
- Codex CLI 呼び出しではない通常の git 操作、path model、oracle/realization 分類、INDEX.md 生成だけを調べる時。
- runtime 実装の細部ではなく、CLI サブコマンド全体の入口や引数 parsing の一覧を探している時。
- LLM の応答品質や Codex CLI 本体の挙動そのものを検証したい時。このテストは cmoc 側が Codex CLI をどう起動し記録するかを対象にしている。

## hash
- 2aba772e50cf05962d67261550ecb2211862c10f1d234cbee723ae523119a1ed

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
- プロンプト部品と実行パラメータ生成の挙動を検証する realization test。レビュー基準、ルーティング規則、ファイルアクセス規則、各種 standard の Markdown 描画、complete prompt への標準文書の注入・省略、TUI resolve parameter の schema、各 builder の model class・reasoning effort・file access mode を扱う。

## Read this when
- プロンプトを構成する標準文書や complete prompt の出力内容が期待語句を含むか確認したいとき。
- ファイルアクセスモードごとのプロンプト文言、routing rule、realization standard、index entry standard、review/apply review standard の描画テストを確認したいとき。
- apply fork、indexing、review oracle、session join、TUI resolve parameter などの builder が選ぶ model class、reasoning effort、file access mode、schema 内容を変更・検証するとき。
- StructDoc と render_as_markdown の基本的な Markdown 出力、空行の正規化、コードブロック保持を変更するとき。

## Do not read this when
- 実際のプロンプト文書を生成する実装本体だけを確認したい場合は、対応する prompt_parts や builder の実装へ進む。
- CLI コマンドの実行フロー、永続状態、git 操作など、プロンプト生成以外の挙動を調べたい場合は対象機能の実装・テストを読む。
- oracle file の正本仕様そのものを確認したい場合は、このテストではなく oracle 配下の該当文書を読む。

## hash
- d6700f30c83b0221cd43b5c88b06215d5d9255a6512926705ac6007000fc95ee

# `test_review_oracle_cli.py`

## Summary
- `review oracle` の CLI 挙動を検証する realization test。レビュー対象 oracle の選定、レポート出力、Codex 呼び出し制御、レビュー用 worktree からの `INDEX.md` 反映、失敗時レポート、`INDEX.md` 以外の差分拒否を扱う。

## Read this when
- `review oracle` コマンドの外部挙動、終了コード、標準出力、生成レポート内容を変更・確認するとき。
- レビュー範囲の既定値、`full` 指定、短い scope option、session scope で対象がない場合の扱いを確認するとき。
- gitignored な oracle file を full scope や session scope のレビュー対象から除外する制御を変更するとき。
- oracle ごとの発見事項列挙ループで、別 oracle の発見事項をプロンプトへ混ぜない制御を確認するとき。
- レビュー用 worktree で生成された `INDEX.md` だけを元 worktree に反映し、その他の差分を拒否する処理を変更するとき。
- レビュー処理中の例外で error report を残し、未判定 finding を通常の却下結果として扱わない挙動を確認するとき。

## Do not read this when
- `review oracle` 以外の CLI コマンド、session 作成、init 処理そのものの仕様を調べたいとき。
- oracle 本文の正本仕様や、oracle file と realization file の定義を確認したいとき。
- Codex 実行 wrapper の低レベルな引数組み立て、外部プロセス実行、設定読み込みの実装だけを調べたいとき。
- レビュー finding の判定基準や LLM 出力品質そのものを確認したいとき。

## hash
- cdfbee61f9eb8ba6aef5748350f8b40b1a426e6836a8d9eb2bf9acf872581815

# `test_session_cli.py`

## Summary
- session サブコマンドの CLI 挙動を検証する realization test。session fork による session branch と session state の作成、linked worktree 上での fork、session abandon の正常終了・home branch 不在・cleanup 失敗時 rollback、session join の conflict resolution・linked worktree・delete conflict・session branch 削除失敗時 warning を扱う。
- Git branch、worktree、`.cmoc/sessions` の状態 JSON、Typer runner の CLI 出力、Codex conflict resolution 呼び出し、git branch 削除失敗時の制御をまたぐ session 系の外部挙動を確認する入口になる。

## Read this when
- session fork、session abandon、session join の CLI 挙動やテスト期待値を変更する。
- session state JSON の `state`、`session_home_branch`、`session_start_commit`、`last_joined_apply_oracle_snapshot_commit`、`apply.state` など、session 操作で保存・更新される状態を確認する。
- session 操作が通常 worktree と linked worktree でどの branch を home として扱い、どの worktree の current branch を切り替えるかを確認する。
- session abandon の失敗時に、home branch 不在、session branch 削除失敗、状態 rollback、利用者向け出力をどう扱うかを確認する。
- session join の merge conflict 解決で Codex 実行を呼ぶ条件、file access mode、解決後の staging、home branch への切り替え、session branch 削除 warning を確認する。

## Do not read this when
- session 系ではない CLI サブコマンド、path model、oracle review、INDEX 生成などの挙動だけを確認したい。
- session 実装内部の関数分割、git helper の詳細、Codex 実行 wrapper の実装そのものを調べたい場合で、まず実装ファイルを読む方が直接的である。
- session state schema 全体の正本仕様や、利用者向け文書としての session 概念を確認したい場合で、oracle doc または関連仕様断片を読む必要がある。
- テスト支援 fixture、`make_repo`、`runner`、`run_git`、`CmocError`、`FileAccessMode` の定義や共通テスト基盤だけを確認したい。

## hash
- fa29ae5f52aef12140f003927bf2db689352b51ef2c8ef0cc84aa3458fdfdf31
