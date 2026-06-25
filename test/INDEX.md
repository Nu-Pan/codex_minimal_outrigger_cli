# `_support.py`

## Summary
- テスト内で共通利用する補助関数群をまとめた realization test の支援モジュール。git リポジトリ作成、テスト用 CODEX_HOME 設定、ブランチ取得、apply 用 worktree 解決など、CLI テストの前提環境を小さく構築する入口になる。
- Typer のテスト runner や主要な cmoc 実装モジュールを同じ場所から参照できるようにし、複数テストで共有される setup と状態参照を集約している。

## Read this when
- CLI テストで一時 git リポジトリ、初期 commit、oracle 配下の fixture、または追跡済み ignore 対象ファイルを用意する helper を確認・追加したいとき。
- テスト中に CODEX_HOME を一時ディレクトリへ向ける処理や、認証ファイルを含む最小の Codex home fixture を再利用したいとき。
- apply 系テストで保存状態から apply branch の worktree path を復元する共通処理を確認したいとき。
- 複数のテストファイルにまたがって同じ subprocess git 操作や CLI runner setup が重複しそうなとき。

## Do not read this when
- 個別サブコマンドの期待出力、エラー条件、状態遷移を確認したいだけなら、該当するテスト本文を直接読む。
- プロダクト実装の CLI 定義、runtime 処理、path token 解決、sandbox mode 変換の挙動を変更したいときは、対応する実装側の本文を読む。
- oracle file の正本仕様断片や仕様文書を確認したいときは、このテスト支援モジュールではなく oracle 側の本文を読む。

## hash
- 177bd3430c87ab5f9b7100c81bd29747aefe79b9e5248eaa456c01e737e6345d

# `test_apply_abandon_cli.py`

## Summary
- apply run を破棄する CLI 挙動を検証する realization test。apply 用 worktree と branch の削除、apply 状態の ready への戻し、永続状態からの apply_branch・apply_worktree・apply_process_id の消去、利用者向け出力の要点を扱う。
- cleanup 対象が既に無い場合の warning、running 状態の apply process 停止、process id が無い running 状態の許容、apply worktree 上からの実行時に元 root へ戻る挙動を検証する。
- 破棄対象を特定できない apply_branch や、現在の apply branch が active apply run と異なる stale branch の場合に、状態と cleanup 対象を壊さずエラーにする境界を検証する。

## Read this when
- apply abandon の正常系、cleanup、状態更新、警告出力、エラー境界を変更・確認したいとき。
- apply fork 後に作られる apply branch・apply worktree・session state のライフサイクルをテスト側から追いたいとき。
- running 中の apply を abandon する際の process id file、stop 処理、cleanup 順序に関わる挙動を確認したいとき。
- apply worktree 内から CLI を実行する場合や、stale apply branch から誤って abandon する場合の保護挙動を確認したいとき。

## Do not read this when
- apply abandon 以外の apply サブコマンド、session 操作、init 操作そのものの仕様や実装を調べたいとき。
- Codex exec の出力品質や findings 内容そのものを検証したいとき。
- git worktree や branch 操作の低レベル helper 実装だけを調べたいとき。
- oracle file の正本仕様断片を確認したいとき。

## hash
- 1f1d569b4a676d9882640619423f66d878c7207b4c3b7194fd434a6a7c84fa40

# `test_apply_fork_cli.py`

## Summary
- apply fork の CLI 挙動を検証する realization test。apply fork 実行時の Codex ループ、状態更新、apply worktree 配置、レポート生成、収束・未収束・エラー時の扱い、禁止対象差分、rolling 時の差分対象選定を扱う。
- CLI 経由で session fork から apply fork / apply join までを動かし、git branch・worktree・永続状態・レポート・作業ツリー差分が期待通りになるかを確認する入口。

## Read this when
- apply fork コマンドの外部挙動、終了コード、出力レポート、状態ファイル更新、apply branch / worktree の生成規則を変更または確認したいとき。
- apply fork が Codex 呼び出しをどの目的で行うか、finding 列挙・適用・commit message・change summary の呼び出し制御をテスト上で確認したいとき。
- apply fork が .gitignore を不要に書き換えないこと、ただし finding の対象として .gitignore を編集できることを確認したいとき。
- config 読み込みエラー時に apply run を開始せず、状態・pid・branch を汚さない挙動を確認したいとき。
- root 直下の memo を apply target から除外しつつ、ネストした memo ディレクトリは対象として残す正規化挙動を確認したいとき。
- apply fork の未収束レポート、収束レポート、エラーレポート、change summary の描画、commit message 採用を確認したいとき。
- apply fork が変更後の dirty file を再検査して収束判定する制御を確認したいとき。
- apply fork が編集禁止対象の差分を検出してエラー状態にし、それまでの変更要約をレポートへ残す挙動を確認したいとき。
- apply join 後の rolling apply fork が、前回 apply の oracle snapshot commit を使って実装差分と oracle 差分の両方を再検査対象にする挙動を確認したいとき。

## Do not read this when
- apply fork の内部 helper 単体の純粋な入出力だけを確認したいときは、対象 helper を定義する実装またはより狭い単体テストを読む。
- apply 以外の CLI サブコマンド、初期化、通常の session 操作、review 系の挙動だけを調べたいとき。
- Codex 実行結果の品質そのものや LLM の出力内容を検証したいとき。このテストは Codex 呼び出しを fake 化して制御ロジックと副作用を検証する。
- oracle file の正本仕様を確認したいとき。この対象は realization test であり、仕様判断の根拠としては oracle file を読む。

## hash
- 02e02d36539504385039d5d8d26cb629bcde9259370996e4ebd4ae08d40b8be1

# `test_apply_join_cli.py`

## Summary
- `apply join` の CLI 挙動を検証する realization test。apply worktree と apply branch の後片付け、session state の ready 復帰、oracle snapshot commit の記録、join report の生成を確認する。
- session 側と apply worktree 側のどちらから実行した場合も扱い、apply worktree 内からの実行時に元の root へ戻ることや、ログが root 側へ保存されることを検証する。
- 未コミット差分、想定外の apply 差分、`.gitignore` 変更、merge conflict、`INDEX.md` conflict の解決継続など、join 時の失敗・force resolve・cleanup 境界を確認する入口になる。

## Read this when
- `apply join` の正常終了後に削除される worktree・branch、更新される session state、出力される report の期待挙動を確認したいとき。
- apply worktree 内から `apply join` を実行するケース、実行後の cwd、cleanup 到達性表示、root 側ログ保存の扱いを変更または調査するとき。
- apply worktree に未コミット差分がある場合の失敗、stderr/stdout の出し分け、state を completed のまま残す挙動を確認するとき。
- oracle や `.gitignore` への想定外差分を検出し、通常モードでは失敗し、`--force-resolve` では session 側の内容へ戻す挙動を調べるとき。
- 通常ファイルの merge conflict を unresolved として report に残す挙動、または `INDEX.md` conflict を通常モードで解決して join を継続する挙動を確認するとき。

## Do not read this when
- `apply fork` の生成処理、Codex 実行の詳細、または apply worktree の作成条件そのものを調べたいだけのとき。
- session 作成、branch 命名、状態ファイル schema 全体など、join 後の更新対象ではない基盤仕様を調べたいとき。
- oracle file や realization file の概念、ルーティング文書、INDEX エントリー生成規則を確認したいとき。
- CLI 全体のコマンド登録、Typer app 構成、またはテスト支援 fixture の実装を確認したいとき。

## hash
- c3fe3ec9bbf23f9b06b3b9971f4b9610e91f36bd40c4ef971af13f021279fee8

# `test_basic_runtime.py`

## Summary
- cmoc の基礎的な runtime 挙動を検証する realization test。path token 解決、duration 表示、repo root と linked worktree の区別、設定既定値、構造化エラー表示、CLI エラー出力先、実行場所 preflight、completion probe、`.cmoc` ignore、file access mode と Codex profile の権限制御を扱う。
- runtime の小さな共通 helper と CLI 起動前後の安全制御が、利用者に見える出力や filesystem permission profile にどう反映されるかを確認する入口になる。

## Read this when
- path token、repo root、work root、linked worktree の解決挙動を変更・確認したいとき。
- duration 表示、設定の既定 model class / reasoning effort、file access mode の文字列表現や sandbox mode 変換を変更・確認したいとき。
- CmocError の markdown 表示、CLI 引数解析失敗、detached HEAD、work root 以外での実行など、エラーが stderr に構造化出力される挙動を確認したいとき。
- shell completion 用 probe で通常の cmoc preflight や副作用を抑止する挙動を確認したいとき。
- `.cmoc` を `.gitignore` に追加する処理や、既存 ignore pattern を尊重して不要な差分を出さない挙動を確認したいとき。
- Codex profile における read / write / deny_read / read_only / writable_roots が file access mode ごとにどう構成されるかを確認したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、session 状態遷移、agent 呼び出し内容そのものを調べたいときは、より直接その機能を検証するテストへ進む。
- oracle file の正本仕様や routing 文書の規則を調べたいときは、oracle 側の本文を読む。
- 実装本体の責務分割や helper の内部構造を理解したいだけなら、対応する implementation を直接読む。
- LLM 出力品質、Codex CLI の外部サービス挙動、長い end-to-end workflow を検証したいときは、この対象ではなく該当する統合テストや呼び出し境界のテストを探す。

## hash
- 53b15cea33961341f0c436adc1b552686a1cada0eee7e5e7e534651ec6de68be

# `test_cli_init_tui.py`

## Summary
- CLI の初期化と TUI 起動に関する realization test。初期化時の `.cmoc` 配下の git 管理解除、ignore 設定、既存 staged/unstaged 変更の保持、linked worktree での作業場所、既定設定ファイルの生成・同期、サブコマンド実行ログを検証する。
- TUI ではエディタで作成された依頼文からパラメータ解決用 Codex 実行と TUI 用 Codex 起動へつなぐ制御、生成された完全プロンプトの保存場所、不要な HTML コメント除去、旧ログパスを使わないことを検証する。
- Markdown prompt parser が fenced code block 内の見出し風テキストを見出し扱いしないこと、見出し前の前文を本文セクションとして保持することを検証する。

## Read this when
- `init` サブコマンドの git 操作、`.gitignore` 更新、`.cmoc` 配下の ignore・untrack・config 生成、既存 index/worktree 変更を壊さない挙動を変更または確認するとき。
- linked worktree 上で `init` や `tui` を実行した場合の root/cwd、`.cmoc` state・log・config の配置、親 worktree へ副作用を出さない挙動を確認するとき。
- `tui` サブコマンドのエディタ起動、依頼文の整形、パラメータ解決用 structured output schema、Codex TUI へ渡す model・reasoning effort・file access mode・prompt を変更するとき。
- サブコマンド実行ログの保存先や `command_invoked` event の内容を変更するとき。
- Markdown 依頼文 parser の見出し分割、fenced code block の扱い、見出し前テキストの扱いを変更するとき。

## Do not read this when
- CLI の初期化・TUI・Markdown prompt parsing と関係しないサブコマンドの仕様やテストを探しているとき。
- Codex 実行ラッパーそのものの低レベルな subprocess 組み立て、外部コマンド共通処理、設定 schema 全体の詳細だけを調べたいときは、対応する実装や専用テストを先に読む。
- oracle の正本仕様を確認したいときは、realization test であるこの対象ではなく oracle 側の本文を読む。

## hash
- 228fed3a02ac1c474c76f32497cb7d88320bc0ae08146418d002e1bd10fc3f99

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 呼び出しを包む runtime 層の realization test。exec 実行ではプロンプトを stdin で渡し、出力 schema・profile・CODEX_HOME・ログ・Structured Output の読み取りが期待どおりになることを検証する。
- worktree 上の cwd で exec した場合に、schema の保存先が実行 cwd 側の work root 配下になり、call log は repo root 側のログ領域に残ることを検証する。
- TUI 起動では exec サブコマンドを使わず、プロンプトをコマンド引数として渡し、capture しない subprocess 呼び出し、sandbox profile、call log、subcommand log、コンソール表示を検証する。
- repo 設定から Codex model と reasoning effort を読み込み、生成 profile に反映されることを検証する。

## Read this when
- Codex CLI の exec/TUI 呼び出し方法、引数構成、stdin と prompt 引数の使い分けを変更・確認するとき。
- Codex 呼び出し用 profile、CODEX_HOME、sandbox writable/read-only paths、repo 設定の反映を扱う runtime 実装を変更するとき。
- Codex 呼び出しログ、stdout/stderr ログ、subcommand log、コンソール表示、call result オブジェクトの挙動を変更・確認するとき。
- output schema のコピー先、worktree を cwd にした実行、Structured Output 読み取りの挙動を確認するとき。

## Do not read this when
- Codex CLI 呼び出しではなく、Git 操作、path model、INDEX 生成、oracle review など別領域の挙動だけを確認するとき。
- runtime 実装の外部挙動ではなく、テスト補助関数や fixture の定義そのものを調べたいときは、補助モジュールを直接読む。
- Codex や LLM の回答品質そのもの、プロンプト本文の内容設計、モデル選定方針の正本仕様を調べたいとき。

## hash
- 54ece639c73e67bed45444024eb270fe150d0625555e82d2972edac42103076f

# `test_codex_runtime_home.py`

## Summary
- Codex runtime wrapper の CODEX_HOME default、既存 CODEX_HOME 維持、missing home、file home、missing auth.json の事前失敗を検証する realization test。

## Read this when
- Codex CLI 呼び出し前の CODEX_HOME 解決、環境変数引き継ぎ、auth.json validation、事前エラー文面を変更する。

## Do not read this when
- subprocess stdin/log/schema 保存や quota retry/resume の挙動を確認したい。

## hash
- edede0989727c4367d407b9fa2be3dfac723e7f2300fb9f5fda3bd51396503f4

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 呼び出しの retry 制御を検証する realization test。schema 検証失敗後の再実行、capacity 検出時の再試行、quota 検出時の availability probe と resume/rerun、並列呼び出し時の代表 probe 共有、各 call log と subcommand log の記録内容を扱う。

## Read this when
- Codex CLI 実行ラッパーの retry 条件、retry 後の成功結果、または失敗時の扱いを変更・調査するとき。
- stdout JSONL 上の capacity/quota error marker の解釈、stderr や通常出力に出た marker を retry 対象外にする境界を確認するとき。
- quota 待機後の availability probe、thread id を使った resume、resume token が無い場合の prompt 再実行、並列実行時に probe を 1 回に集約する制御を確認するとき。
- Codex call log、stdout/stderr/output path、subcommand logger の codex_call event、console 表示に記録される retry 状態や purpose を検証するとき。

## Do not read this when
- Codex CLI の通常成功パスだけを確認したいときは、retry ではない実行結果や基本ログを扱うテストを先に読む。
- 作業対象が path model、oracle/realization 分類、INDEX.md 生成規則など Codex CLI 実行 retry と無関係な仕様・ルーティングであるとき。
- Codex CLI 本体の引数組み立てや profile 設定だけを調べたい場合で、capacity/quota/schema retry や call log の retry 状態に触れないとき。

## hash
- e51aeba28342f8ed0a8dbfc509a105f56e89207aea20648b71adf155b0149a40

# `test_indexing_cli.py`

## Summary
- indexing コマンドと indexing preflight の realization test。INDEX 生成・更新・commit 対象の限定、既存 hash による再生成 skip、不正 entry の再生成、同階層 entry の並列生成、root 直下 memo 除外と入れ子 memo 対象化、linked worktree 対象化、Codex 呼び出し前の indexing 実行、lock 待機、特定 purpose での preflight skip を検証する。
- merge conflict 解決時に INDEX を削除して merge commit を成立させる挙動と、未初期化 clean repo で indexing が非 INDEX 差分を残さず失敗する挙動も扱う。

## Read this when
- indexing コマンドの外部挙動、commit される path、dirty worktree の扱い、未初期化 repository での失敗条件を変更・確認するとき。
- INDEX entry 生成のための Codex structured output 呼び出し、fresh hash による再生成 skip、不正または欠落した entry の再生成判定を変更・確認するとき。
- worktree 上で indexing がどの repository を対象にするか、Codex exec/tui 呼び出し前に indexing preflight が走る条件、または preflight を skip する purpose 条件を変更・確認するとき。
- indexing lock の待機、同階層 entry 生成の並列化、root 直下 memo と入れ子 memo の indexing 対象境界を変更・確認するとき。
- INDEX merge conflict の解決処理が conflict path を削除して commit する制御を変更・確認するとき。

## Do not read this when
- INDEX.md のルーティング文書としての書式や entry 文面の仕様だけを確認したいとき。正本仕様断片または schema の方が直接の入口になる。
- Codex 呼び出し一般の parameter 定義、model class、reasoning effort、file access mode の意味を確認したいだけのとき。support module や実装側の型定義がより直接の入口になる。
- indexing 以外の CLI サブコマンド、session/apply/review などの挙動を確認したいとき。ただしそれらが Codex 呼び出し前の indexing preflight と接続する場合は読む。
- git helper、repository fixture、runner fixture の作りそのものを変更したいとき。共通 test support の定義がより直接の入口になる。

## hash
- 7f919eed81196ee108970e3921c3fd2b0d09c423f1a8c148b30477a7364d9190

# `test_prompt_parts.py`

## Summary
- プロンプト構成部品とそれらを組み合わせるパラメータ生成処理の回帰テストを担う realization test。レビュー基準、ルーティング規則、ファイルアクセス規則、実装基準、INDEX エントリー基準、レビュー oracle 基準などが StructDoc と Markdown 出力に期待語句を含めることを確認し、完全プロンプト生成時の標準文書の同梱・省略条件も検証する。
- TUI 用パラメータ選定プロンプト、INDEX エントリー生成パラメータ、レビュー oracle merge finding、session join conflict resolution などの builder が、期待される model class、reasoning effort、file access mode、schema 内容、プロンプト断片を持つことを確認する。

## Read this when
- プロンプト部品 builder の出力タイトル、Markdown へのレンダリング内容、標準文書の同梱条件を変更・確認する。
- 完全プロンプト生成で routing rule が常に含まれることや、apply review standard、realization standard、index entry standard、review oracle standard がフラグに応じて含まれる・省略されることを確認する。
- ファイルアクセスモードごとの file access rule 文言、TUI resolve parameter の schema と enum、各種 builder の model class・reasoning effort・file access mode を変更・検証する。
- StructDoc の Markdown レンダリング、特に連続空行の折りたたみ挙動を確認する。

## Do not read this when
- 個別のプロンプト部品本文そのものの実装を理解したいだけで、テスト上の期待語句や builder の外部契約を確認する必要がない。
- CLI 実行、作業ツリー操作、GitHub 連携など、プロンプト構成・パラメータ生成と直接関係しない機能の挙動を調べる。
- oracle 側の正本仕様断片を確認したい場合。この対象は realization test であり、正本仕様の入口ではない。

## hash
- 753362288caaa105b846e4e3fc09d7ca8cfad94cc6cdc5b065b8db20f855dc62

# `test_review_oracle_cli.py`

## Summary
- `review oracle` コマンドの realization test。レビュー対象 oracle の列挙、scope 指定、gitignore 対象の除外、レポート生成、レビュー用 worktree からの INDEX.md 変更取り込み、処理失敗時の error report、INDEX.md 以外の差分拒否を、CLI 実行結果と生成レポートの内容で検証する。

## Read this when
- `review oracle` の外部挙動、レポート出力、scope の既定値や短縮オプションを変更・確認する時。
- oracle file のレビュー対象選定で、gitignore 対象や session/full scope の扱いを確認する時。
- レビュー処理中の Codex structured output 呼び出し、finding の判定失敗、処理失敗時のエラーレポートを変更・確認する時。
- レビュー用 worktree で生成された INDEX.md 変更の取り込みや、INDEX.md 以外の変更を拒否する制御を変更・確認する時。

## Do not read this when
- 通常の `init`、`session fork`、git helper、fixture 作成そのものの詳細だけを調べたい時。
- oracle の正本仕様本文を確認したい時。
- `review oracle` 以外の review サブコマンドや、一般的な CLI コマンドの挙動だけを確認したい時。

## hash
- 6ee141f5b42cdc53e0c03c910b696dcf1f6549383ccbacec10c34881ef2252e1

# `test_session_cli.py`

## Summary
- session サブコマンドの realization test。session fork による session branch と状態ファイル生成、session abandon による home branch への復帰・branch 削除・状態更新、session join による home branch への取り込みと競合解決を検証する。
- Git 操作を伴う一時リポジトリ上で CLI を実行し、branch 状態、session state JSON、標準出力・標準エラー、Codex conflict resolution 呼び出し、未解決 conflict の解消状態を確認する。

## Read this when
- session fork、session abandon、session join の外部挙動や失敗時挙動を変更する。
- session state JSON の `session.state`、`session_home_branch`、`joined_at`、`apply.state` の生成・更新条件を確認する。
- session branch の作成、削除、削除失敗時 warning、cleanup 失敗時 rollback、home branch 不在時のエラー処理を確認する。
- join 時の merge conflict 解決で Codex 実行を呼ぶ条件、file access mode、delete conflict 解決後の staging 状態を確認する。
- session 系 CLI の出力に含まれる diagnostics、成功・失敗時の stdout/stderr の出し分け、終了コードを確認する。

## Do not read this when
- session 以外の CLI サブコマンド、path model、oracle review、設定読み込みなどを調べる場合。
- session の実装構造や helper の責務を先に理解したい場合。この対象は外部挙動のテストであり、実装入口ではない。
- Codex 実行そのものの品質や LLM 出力内容を確認したい場合。この対象は Codex 呼び出しの有無と引数相当の制御だけを検証する。
- INDEX 生成規則やルーティング文書の仕様を調べる場合。

## hash
- 29d619c3245b57120f1a08659b8bdd2a886f41cc744ba7a15b7df52f75a9cf05
