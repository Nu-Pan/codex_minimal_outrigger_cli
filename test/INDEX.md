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
- apply join の CLI 挙動を検証する realization test。apply 用 worktree と branch の削除、session state の ready への復帰、oracle snapshot commit の記録、report 生成、作業ディレクトリ移動、未コミット差分・想定外差分・merge conflict・INDEX.md conflict 解決時の終了コードと出力を扱う。

## Read this when
- `apply join` の成功時 cleanup、状態更新、report 出力、apply worktree からの実行可否を確認・変更する場合。
- `apply join` が dirty な apply worktree、想定外の oracle 差分、通常ファイルの未解決 merge conflict をどう扱うかを確認・変更する場合。
- apply 側の `.gitignore` 変更を join で取り込む挙動や、INDEX.md conflict を通常 mode で解決して join を継続する挙動を確認・変更する場合。
- `apply fork` で作られた apply branch/worktree と session state が、`apply join` 後にどの外部副作用を持つべきかをテスト観点から確認する場合。

## Do not read this when
- `apply join` 以外の apply subcommand、session fork、init の基本挙動だけを調べたい場合。
- CLI 実装内部の helper 分割、状態 schema の定義、path model の仕様を調べたい場合は、対応する実装または oracle を先に読む。
- Codex 実行結果の品質や LLM 出力内容そのものを検証したい場合。
- INDEX.md エントリー生成全般の方針やルーティング文書の書き方を調べたい場合。

## hash
- 90f43b5ab66bf3d9236896fcb154eddfa3d1f11dcdcb1264ad8c7733b14825f2

# `test_basic_runtime.py`

## Summary
- cmoc の基本的な実行時挙動を横断的に検証する realization test。パス表記の解決、時間表示、Git worktree における root 判定、設定既定値、構造化エラー表示、CLI エラー出力、補完プローブ時の副作用抑止、.cmoc ignore 設定、file access mode と sandbox mode の対応、Codex profile の権限制御を扱う。
- 単一機能の詳細テストというより、runtime・CLI preflight・権限 profile・補助関数の基本契約が壊れていないかを確認する入口として位置づけられる。

## Read this when
- path token と実パスの相互解決、repo root と work root の判定、linked worktree 上の挙動を変更・確認したいとき。
- CmocConfig の既定値、model class、reasoning effort、file access mode、sandbox mode、Codex profile の permission profile を変更・確認したいとき。
- CmocError の markdown 表示、CLI 引数解析エラー、preflight エラー、stdout/stderr の出し分けを変更・確認したいとき。
- completion probe 実行時に cmoc preflight や .gitignore/.cmoc 生成などの副作用を避ける挙動を確認したいとき。
- ensure_cmoc_ignored による .gitignore 更新、既存 ignore pattern を尊重する挙動、git check-ignore との関係を確認したいとき。

## Do not read this when
- 個別サブコマンドの正常系ワークフローや永続状態の詳細を確認したいだけのときは、その機能に対応する CLI または runtime のより直接的なテストを読む。
- oracle file の正本仕様や文書方針を確認したいときは、実装テストではなく oracle 側の本文を読む。
- UI 表示、LLM 出力品質、または Codex CLI 自体の外部挙動を検証したいときは、このテストの対象外。
- 特定 helper の内部実装手順だけを調べたいときは、ここでは外部契約だけを確認し、必要に応じて対応する実装本文へ進む。

## hash
- e4e46f2e8d05f15bbbc375037b905b39a267ea5adb3bcf1bfbf8d9eae531d897

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
- cmoc の indexing 機能と indexing preflight の realization test。INDEX.md 生成・更新・commit、fresh hash 時の再生成省略、壊れた既存エントリーの再生成、兄弟エントリーの並列生成、root 直下 memo の除外と入れ子 memo の対象化、git worktree 選択、Codex 呼び出し前の indexing 実行・省略条件、repository lock 待機、INDEX.md merge conflict 解消を検証する。

## Read this when
- indexing コマンド、indexing preflight、INDEX.md の生成・更新・commit、または indexing lock の挙動を変更する。
- Codex exec/TUI 呼び出し前に indexing を走らせる制御、index entry 生成時や conflict resolution 時に preflight を省略する制御を確認する。
- worktree 上での indexing 対象選択、未初期化 repository、未コミット差分、INDEX.md 以外の差分を含む repository 状態への挙動を検証する。
- INDEX.md 既存エントリーの hash freshness 判定、malformed entry の再生成、memo directory の indexing 対象境界、または sibling entry の並列処理を確認する。

## Do not read this when
- indexing 以外の CLI サブコマンドや workflow のテストだけを確認したい。
- INDEX.md エントリーの文章構造や schema そのものを調べたいだけで、生成・更新・commit・preflight の制御には触れない。
- oracle file の正本仕様や path keyword の定義を確認したいだけで、realization test の期待挙動は不要である。

## hash
- 80a020fbfa4b09b4f2139df23e82a21bcc486ce5db51253acbd75f19ac074b52

# `test_prompt_parts.py`

## Summary
- プロンプト断片生成と実行パラメータ選定に関するテスト群。ファイルアクセス規則、ルーティング規則、各種標準文書の注入・省略、Markdown レンダリング、Structured Output schema、ビルダーが選ぶモデル種別・推論量・アクセスモードを検証する。

## Read this when
- プロンプト生成処理が、必要な標準文書やルーティング規則を含めるか、省略すべき標準文書を省略するかを確認したいとき。
- ファイルアクセスモードごとの読み書き制約文言、レビュー基準、実装保守基準、INDEX.md エントリー基準などのレンダリング期待値を変更・確認したいとき。
- TUI の実行パラメータ選定、INDEX.md エントリー生成、レビュー結果マージ、セッション join conflict 解決の各パラメータビルダーが返すモデル種別・推論量・アクセスモード・schema を検証したいとき。
- StructDoc の Markdown 出力で連続空行を畳む挙動や、プロンプト注入時の禁止語句除去の期待値を確認したいとき。

## Do not read this when
- 個別コマンドの実処理、ファイル操作、git 操作、セッション状態更新など、プロンプト断片やビルダーパラメータ以外の挙動を調べたいとき。
- 標準文書やルーティング規則そのものの正本仕様を確認したいとき。このテストではなく、対応する仕様文書や実装側の生成関数を読む方が直接的である。
- テスト基盤全体の設定、pytest の共通 fixture、依存関係、実行方法を調べたいとき。

## hash
- 0133c9f1ab458b2726ba2f2719995e2d8eba768ea4d72e598dccef536781e644

# `test_review_oracle_cli.py`

## Summary
- `review oracle` コマンドの realization test。レポート生成、scope 指定、gitignored な oracle の除外、対象なし時の扱い、レビュー用 worktree で生成された索引変更の取り込み、処理失敗時のエラーレポート、INDEX.md 以外の差分拒否を、CLI の外部挙動として検証する。
- Codex 実行部分は monkeypatch で偽装し、実際の LLM 出力品質ではなく、schema ごとの制御分岐、レポート内容、git/worktree 副作用、異常時の復元境界を確認する入口になる。

## Read this when
- `review oracle` の CLI 挙動、scope の既定値や短縮オプション、生成されるレポート内容を変更・確認したいとき。
- oracle file の列挙条件、とくに gitignore 対象の oracle を full/session scope から除外する制御を確認したいとき。
- レビュー処理が作る一時 worktree、INDEX.md 変更の取り込み、INDEX.md 以外の差分拒否、失敗時レポートの挙動を変更・検証したいとき。
- Codex exec の structured output schema ごとの呼び出し順や、finding の列挙・検証・判定が CLI レポートへ反映される経路をテスト側から追いたいとき。

## Do not read this when
- oracle 正本仕様そのものの内容や編集方針を確認したいだけのとき。
- `review oracle` 以外の CLI サブコマンド、または oracle review と無関係な session/init の一般挙動を調べたいとき。
- LLM の出力品質、プロンプト本文、structured output schema の定義そのものを確認したいとき。
- テスト支援 fixture や一時リポジトリ作成 helper の実装詳細だけを調べたいとき。

## hash
- 01ece7fdd0c949051055b1a19fa264a30cb7aaded22db4187e1961d8c6ad2911

# `test_session_cli.py`

## Summary
- session サブコマンドの realization test。session fork が session branch と状態ファイルを作ること、session abandon が home branch へ戻って状態更新・branch 削除・失敗時 rollback を行うこと、session join が conflict 解決・削除 conflict の stage・session branch 削除失敗時 warning を扱うことを検証する。
- 実際の git repository を一時領域に作り、CLI runner、git command、状態 JSON、Codex 実行の monkeypatch を組み合わせて、session 操作の外部挙動と重要な制御分岐を確認する入口である。

## Read this when
- session fork / abandon / join の CLI 挙動、branch 遷移、session 状態ファイル、apply 状態、出力メッセージに関するテストを確認・変更したいとき。
- session abandon の home branch 不在時エラー、cleanup 失敗時 rollback、session branch 削除や状態更新の失敗系を扱う実装変更の影響範囲を確認したいとき。
- session join の merge conflict 解決で Codex 実行を呼ぶ条件、file access mode、削除 conflict 解決後の staging、session branch 削除失敗 warning を検証したいとき。
- session 操作が git branch、README 変更、状態 JSON、CLI 出力をどう組み合わせて観測されているかを、realization test 側から確認したいとき。

## Do not read this when
- session 以外の CLI サブコマンドや、一般的な init・path・oracle・review などの挙動を調べたいだけのとき。
- session 機能の正本仕様断片を確認したいとき。この対象は realization test であり、仕様判断の根拠は oracle file を優先する。
- session 実装の内部構造や helper の責務を直接確認したいとき。実装本文を読む方が適切である。
- テスト支援 helper、CLI runner fixture、git repository fixture の定義そのものを調べたいとき。

## hash
- b09f4a2e18d429df8c1995d33fcee22ccde2b3f01fe2aef6208bf756babfc026
