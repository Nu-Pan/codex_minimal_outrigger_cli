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
- apply fork CLI の統合的な挙動を検証する realization test。セッション fork 後の apply fork 実行、状態更新、apply 用 worktree/branch、Codex 呼び出し、レポート生成、収束判定、エラー時状態、禁止対象差分の拒否、rolling apply の再対象化を扱う。
- apply fork が `.gitignore` や README、oracle 差分、`.agents` 配下などの対象をどう扱うかを、CLI 実行結果・Git 状態・セッション状態 JSON・生成レポートから確認する入口になる。

## Read this when
- apply fork サブコマンドの外部挙動、終了コード、状態遷移、apply branch/worktree の配置、pid 状態の削除条件を変更・確認したいとき。
- apply fork が Codex の所見列挙、所見適用、commit message 生成、change summary 生成をどのタイミングで呼ぶかをテストから確認したいとき。
- apply fork のレポート内容、収束/未収束/エラー表示、変更サマリの描画、コミットメッセージ反映を検証したいとき。
- apply fork の対象正規化、root 直下 memo の除外、入れ子の memo ディレクトリの保持、`.gitignore` を対象として編集できる挙動を確認したいとき。
- apply fork が編集禁止対象の差分を検出した場合の失敗、レポート生成、状態更新を変更・確認したいとき。
- apply join 後の rolling apply が前回 apply の oracle snapshot commit を使って対象を選ぶ挙動を確認したいとき。

## Do not read this when
- apply fork 以外の apply サブコマンドや session 操作の詳細だけを確認したいとき。
- CLI 統合挙動ではなく、個別 helper の純粋な単体仕様やデータ構造だけを確認したいとき。
- oracle file の正本仕様を確認したいとき。このファイルは realization test であり、仕様本文の代替ではない。
- Codex CLI や LLM 出力品質そのものを検証したいとき。このテストは fake の Codex 実行結果を使って cmoc 側の制御と副作用を検証している。

## hash
- 02e02d36539504385039d5d8d26cb629bcde9259370996e4ebd4ae08d40b8be1

# `test_apply_join_cli.py`

## Summary
- apply join の CLI 挙動を検証する realization test。apply worktree と apply branch の cleanup、session state の ready 復帰、join report 生成、apply worktree 上からの実行時の cwd 復帰を扱う。
- apply join の失敗系として、apply worktree の未コミット差分、想定外の apply diff、未解決 merge conflict を検証し、失敗時に worktree・branch・completed state が保持されることを確認する。
- INDEX.md や .gitignore のような特定ファイル差分に対する apply join の扱いも含み、index conflict は通常 mode で解決継続できること、.gitignore 変更は想定外差分扱いしないことを確認する。

## Read this when
- apply join の正常終了時に削除される apply worktree・apply branch、更新される session state、出力される report の期待挙動を確認したいとき。
- apply join を session worktree または apply worktree のどちらから実行した場合でも同じ cleanup・cwd 復帰・ログ保存先になるかを調べるとき。
- apply worktree に未コミット差分がある場合、想定外の oracle 変更がある場合、merge conflict が残る場合の apply join のエラー出力・状態保持・report 内容を確認したいとき。
- apply join の --force-resolve が想定外 apply diff を破棄して session 側を維持する挙動、または .gitignore と INDEX.md の conflict・差分処理を変更するとき。

## Do not read this when
- apply fork で Codex を起動する処理や apply worktree を作成する前段の仕様だけを調べたいとき。
- session fork、init、git repository 初期化など、apply join 前提を作るコマンド自体の詳細を確認したいとき。
- apply join 以外の CLI サブコマンド、または join 後の report 形式ではなく一般的なログ・状態ファイル schema を調べたいとき。
- oracle file や realization file の概念定義、INDEX.md エントリー生成規則そのものを確認したいとき。

## hash
- fbecf0368d24681948a83545cbdbf305aecfc3639bbd47f27693231a460aeda1

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
- プロンプト部品とパラメータ生成のテスト群であり、レビュー基準、ルーティング規則、ファイルアクセス規則、INDEX エントリー基準などが構造化文書として期待語句を含んで描画されることを検証する。
- 完全なプロンプト生成が、指定された補助基準を含める条件、既定では省略する条件、Codex CLI 向けに禁止語を除去する条件、ルーティング規則を常に含む条件を満たすことを確認する。
- apply fork、TUI resolve、indexing、review oracle、session join などのパラメータビルダーが、想定するモデルクラス、推論量、ファイルアクセスモード、スキーマ、作業ツリー表記を使うことを検証する。

## Read this when
- プロンプト部品の文言、構造化文書のタイトル、Markdown 描画結果、または空行正規化の期待挙動を変更・確認したいとき。
- 完全なプロンプトに含める補助基準のオンオフ、Codex CLI 向け文言変換、ルーティング規則の常時挿入、ファイルアクセス規則のモード別出力を調べるとき。
- apply fork、TUI resolve、indexing、review oracle、session join の各パラメータ生成で、モデル種別、reasoning effort、file access mode、スキーマ、プロンプト本文への埋め込み内容が壊れていないか確認するとき。

## Do not read this when
- 個別のプロンプト部品やビルダーの実装を変更したいだけで、テストが期待する外部挙動や文言断片を確認する必要がないとき。
- CLI コマンド実行、永続状態、Git 操作、作業ツリー作成など、プロンプト生成以外の機能テストを探しているとき。
- INDEX エントリーの生成基準そのものの仕様を読みたいとき。ここでは基準文書の描画結果と完全プロンプトへの挿入だけを検証している。

## hash
- b638b246cff591c590e30db000e391bbad9e672e2504a46427ba76a82a3e5966

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
- `cmoc session` 系 CLI の realization test。session branch と state file の生成、abandon の正常系・失敗時 rollback、join の conflict resolution、delete conflict の staging、session branch 削除失敗時の警告出力を、実際の git repo と Typer runner を使って検証する。
- session state path や session home branch を読み出す小さな補助関数を持ち、session サブコマンドの外部挙動、永続状態、branch 遷移、出力メッセージ、Codex 実行時の file access mode を確認する入口になる。

## Read this when
- `cmoc session fork` が session branch を作る条件、session state の初期値、home branch 記録、apply state 初期化を確認・変更するとき。
- `cmoc session abandon` の branch 切り替え、session branch 削除、state 更新、表示される結果項目、home branch 不在時の失敗挙動、cleanup 失敗時の rollback を確認・変更するとき。
- `cmoc session join` の merge conflict 解決で Codex exec を呼ぶ条件、REALIZATION_WRITE mode の使用、解決後の home branch 復帰、delete conflict 解決の staging、session branch 削除失敗時の warning 出力を確認・変更するとき。
- session state JSON の `session.state`、`session.session_home_branch`、`session.joined_at`、`last_joined_apply_oracle_snapshot_commit`、`apply.state` など、session CLI が読み書きする永続状態のテスト期待値を確認するとき。

## Do not read this when
- session 以外の CLI サブコマンド、path model、oracle review、apply workflow などの挙動だけを調べるとき。
- session 機能の実装構造や helper の内部責務を先に理解したいときは、対応する実装ファイルを読む方が直接的であり、このテストは外部挙動の期待値確認に使う。
- Codex CLI や LLM の出力品質そのもの、または conflict 解決内容の品質を検証したいとき。この対象は Codex exec 呼び出しの有無・目的・file access mode と、解決後の repository 状態を検証する。

## hash
- ae51f9fba7bfdb3ccc6adb5765a20c3842c51dba7b5a0ea4604fa48fac805a5c
