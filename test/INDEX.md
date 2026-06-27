# `_support.py`

## Summary
- CLI テストで使う共通補助関数群。最小構成の Git リポジトリ作成、ブランチ状態確認、Codex ホームのテスト用設定、Codex profile 生成の差し替え、偽の Python 実行ファイル作成、apply 用 worktree path 解決をまとめて提供する。
- 外部コマンドとしての Git と Codex 実行制御を伴うテストの前提準備を集約し、個別テストが fixture 作成や monkeypatch の詳細を重複して持たないための入口になる。

## Read this when
- CLI テストで一時 Git リポジトリ、初期 commit、oracle 配下の最小ファイル、追跡済みかつ ignore 対象の oracle ファイルを用意する方法を確認したいとき。
- Codex CLI 実行を伴うテストで、認証済みの最小 CODEX_HOME や profile 生成差し替えの仕組みを使う、または変更するとき。
- テスト内で現在の Git ブランチ名、Git コマンド実行結果、apply 状態から導かれる worktree path を検証する補助処理を探すとき。
- 外部コマンドの代替として実行可能な Python スクリプトをテスト中に生成する必要があるとき。

## Do not read this when
- 個別サブコマンドの期待挙動、CLI 出力、終了コード、状態ファイルの仕様を確認したいだけなら、該当するテスト本文または実装を直接読む。
- pytest の個別ケースやアサーション内容を探しているだけなら、この共通補助関数群ではなく対象機能のテストを読む。
- Codex profile 生成や apply worktree 解決の本体実装を変更する場合は、ここではなく実装側の該当モジュールを読む。
- oracle file や realization file の正本上の定義・標準を確認したい場合は、このテスト補助ではなく oracle 側の文書を読む。

## hash
- 54cf181de55105f9065ad7f515d614e2705529029548b38b874d2326362e0b59

# `test_apply_abandon_cli.py`

## Summary
- apply abandon を CLI 経由で実行したときの active apply run 破棄の外部挙動を検証する realization test。
- completed/running apply run の worktree・branch・session state cleanup、cleanup 対象欠落時の警告、running process と記録済み child process の停止順、PID reuse や raced exit の扱いを固定する。
- repo root、apply worktree、linked session/apply worktree、stale apply branch など実行位置ごとの abandon 境界条件を扱う。

## Read this when
- apply abandon の成功時に apply worktree・apply branch・state・process id 記録がどう削除または ready 化されるかを確認したいとき。
- running apply process の停止、child process group の停止順、pidfd signal、PID reuse、終了済み process の許容に関する制御ロジックを変更するとき。
- apply abandon をどの worktree から実行できるか、linked session の state をどう正として扱うか、stale apply branch をどう拒否するかを確認するとき。
- cleanup 対象が先に消えている場合の warning 出力や、破損 state・process identity 欠落・dirty linked session worktree の拒否条件を変更するとき。

## Do not read this when
- apply fork の生成処理そのもの、Codex 実行結果の解釈、findings の扱いを調べたいだけのとき。
- apply abandon 以外の session fork、init、merge などの CLI 挙動を確認したいとき。
- oracle の正本仕様断片を確認したいとき。この対象は realization test であり、正本仕様ではない。
- process 停止や worktree cleanup を伴わない単純な path model、INDEX 生成、補助 fixture の責務を調べたいとき。

## hash
- f7e3591b4969ab79a729de5928c6ee1e9d8461e0eacdbfe6f0afb89f877c50a7

# `test_apply_fork_cli.py`

## Summary
- apply fork の CLI 経路と内部 body が、Codex 実行ループ、apply run の branch/state/worktree 更新、linked worktree 起点、設定読み込み失敗時の中断、.cmoc ignore 処理、.gitignore 編集対象化、target 正規化を期待どおり扱うことを検証する realization test。
- session fork 後に apply fork を実行したとき、apply state が completed になり、apply branch と run_id 別 worktree が作られ、旧 apply_worktree/apply_process_id/pid が残らず、所見列挙が呼ばれることを確認する。
- linked worktree 上で開始した session branch と HEAD commit を apply run の起点にし、apply worktree は linked worktree 配下ではなく cmoc 管理 worktree 配下へ作ることを確認する。
- apply fork が session 側の既存 .gitignore 表現を書き換えないこと、未 ignore の .cmoc は git info exclude で clean にすること、所見対象としての .gitignore は apply branch 側で編集できることを確認する。
- target 正規化について、root 直下 memo は除外しつつ入れ子の memo directory は残し、binary file も file 種別だけでは除外しないことを確認する。

## Read this when
- apply fork の外部挙動、state 遷移、apply branch 名、apply worktree 配置、apply_process pid の後始末に関するテスト期待値を確認したいとき。
- linked worktree から apply fork を走らせる場合の oracle snapshot commit、apply branch の開始 commit、worktree 配置の期待値を確認したいとき。
- apply fork 実行時の .cmoc ignore 処理、session 側 .gitignore の保持、git info exclude への追加、.gitignore 自体を所見対象として編集する挙動を確認したいとき。
- cmoc config が壊れている、または存在しない場合に、apply run の branch/state/pid を開始せず stdout にエラーを出す挙動を確認したいとき。
- apply fork の target 正規化で root 直下 memo、入れ子の memo directory、binary file、oracle 配下 file の扱いを確認したいとき。
- Codex 実行を fake に差し替えて apply fork の制御フローや副作用をテストする既存パターンを参照したいとき。

## Do not read this when
- apply fork の実装本体、永続 state の読み書き helper、git worktree 作成処理、Codex 呼び出し処理を変更したいだけで、テスト期待値ではなく実装詳細を確認したいとき。
- session fork、init、git helper、runner fixture など apply fork 以外の CLI テスト基盤そのものを調べたいとき。
- apply fork 以外の apply サブコマンド、review、oracle、path model などの仕様やテストを探しているとき。
- Codex CLI や LLM 出力品質そのものの検証方針を知りたいとき。この対象は Codex 実行結果を fake 化し、apply fork 側の制御と副作用だけを検証する。

## hash
- afa9543f71fb61a087b92aa30f464282ad3d4815a4d75b7a289e83836f07ff5d

# `test_apply_fork_report_cli.py`

## Summary
- apply fork の CLI 実行を通じて、所見列挙、所見適用、commit message 生成、変更要約、report 出力、session state 更新までの制御を検証する realization test。
- 収束、未収束、error、変更ファイル再調査、未追跡ファイルの変更要約、編集禁止対象差分の拒否、rolling apply fork の対象選定を、同じ loop と report schema の観測結果として扱う。
- 16,000 文字を超えるが、apply fork report の読み取り文脈を一箇所に保つため、分割より凝集性を優先している。

## Read this when
- apply fork の CLI 終了コード、stdout に返す report path、report 本文の result・finding count・変更要約の期待値を確認する時。
- apply fork が所見適用後に変更ファイルを再調査し、特定のルーティング文書を再調査対象から外す制御を確認する時。
- apply fork が回数上限、空所見、差分なし適用、調査対象なしをそれぞれ収束または未収束として扱う条件を確認する時。
- apply fork の error report が commit 前の working tree 差分や未追跡ファイルを変更要約に含める挙動を確認する時。
- apply fork が編集禁止対象への差分を検出して error state と report に反映する挙動を確認する時。
- apply join 後の rolling apply fork が、前回 apply join の oracle snapshot 以後の変更だけを調査対象にする挙動を確認する時。

## Do not read this when
- apply fork の実装手順、内部 helper の詳細、Codex 実行 wrapper の本体を確認したいだけの場合。
- apply join、session fork、init などの各サブコマンド単体の仕様や実装を確認したい場合。
- report schema の生成規則そのものや、変更要約 helper の内部実装だけを確認したい場合。
- apply fork と関係しない CLI、一般的な repository 初期化、path model、oracle/realization の基本概念を調べる場合。

## hash
- 89a5b080919691a165d01283c9923d3262aaeaf5fe32f85eddab16dae1e412bb

# `test_apply_join_cli.py`

## Summary
- apply run を session へ join する CLI 外部挙動を検証する realization test。成功時の apply worktree と apply branch の後片付け、session state 更新、report 生成、apply worktree からの実行、linked session worktree への merge を扱う。
- join を拒否または中止する境界条件として、古い apply branch、dirty apply worktree、想定外差分、削除・rename を含む managed branch 差分判定、gitignore 変更、merge conflict と index conflict 解決後の継続を同じ操作文脈で確認する。

## Read this when
- apply join の CLI 成功条件、後片付け、state 更新、report 出力を変更または確認したいとき。
- apply join を session worktree、apply worktree、linked session worktree のどこから実行できるかを確認したいとき。
- apply join が dirty worktree、古い apply branch、想定外差分、merge conflict をどう検出し、どの状態を残すかを確認したいとき。
- apply join の差分判定で、削除パス、rename 先、gitignore 変更、oracle 配下の想定外変更をどう扱うかを確認したいとき。

## Do not read this when
- apply fork の Codex 実行、apply worktree 作成、apply state 初期化だけを確認したいとき。
- session fork や init の基本挙動だけを確認したいとき。
- join の CLI 経由の外部挙動ではなく、内部 helper の小さな単体仕様だけを確認したいとき。ただし managed branch の変更パス判定に関する確認は対象に含まれる。
- oracle file の正本仕様そのものや、INDEX.md 生成ルールを確認したいとき。

## hash
- e233fb4e7319fc4c0ddc648b190cce2111bb5fc24a37dff2e43fab24a68eee66

# `test_basic_runtime.py`

## Summary
- cmoc runtime の基礎契約を固定する realization test 群。path token と linked worktree/run root の解決、duration 表示、subcommand log の衝突回避、config の既定値と検証、CmocError/CLI parse error の stdout report、session/apply branch state の拒否条件、`.cmoc` ignore、FileAccessMode と Codex sandbox/profile、binary 判定の読み取り範囲を扱う。
- 実装横断の小さな runtime 契約を、外部挙動・永続副作用・sandbox profile 生成結果として確認する入口であり、runtime 周辺の仕様変更が既存契約を壊していないかを見るためのテスト対象。

## Read this when
- path token、`<run-root>`、linked worktree、repo/work root 判定、または main worktree 拒否の挙動を変更・確認する。
- runtime logging、duration 表示、CmocError の Markdown report、Click parse error を含む CLI error 出力先を変更・確認する。
- config の既定 model/reasoning effort、codex 設定値の型検証、FileAccessMode の永続化値や sandbox mode 変換を変更・確認する。
- session branch/apply branch からの session id 抽出、破損 branch 名の拒否、branch に対応する state load の挙動を変更・確認する。
- `.cmoc` の gitignore 追加、起動 wrapper の missing venv report、binary 判定、Codex profile の writable roots と保護領域拒否を変更・確認する。

## Do not read this when
- 個別サブコマンドの通常フローや UI 文言だけを調べたい場合。runtime 横断の error/report/preflight/state/sandbox 契約に触れないなら、対象サブコマンドの実装または専用テストを読む。
- oracle の正本仕様断片そのものを確認したい場合。この対象は realization test であり、仕様根拠の確認は対応する oracle file を読む。
- 単一 helper の内部実装だけを局所的に変更し、外部挙動・永続副作用・CLI 出力・profile 生成契約を確認する必要がない場合。
- Codex CLI や LLM 出力品質そのものを検証したい場合。この対象は cmoc runtime の制御ロジックと外部副作用を扱う。

## hash
- bc70220de1e3f7e76f63de0fcb06a3d7ccab0ccc51e4b0e04de4f550bca1be9a

# `test_cli_init_tui.py`

## Summary
- CLI の初期化処理と対話型起動処理を、実際の一時 Git リポジトリ上で検証するテスト群。初期化時の管理ディレクトリ除外、既存ステージ状態の保持、設定ファイルの既定値同期、サブコマンドログ、通常 worktree と linked worktree の保存先・無視設定の違いを扱う。
- 対話型起動では、エディタで作成された依頼文の整形、パラメータ解決用 Codex 呼び出し、最終 Codex TUI 呼び出しへの引数伝播、完了プロンプトの保存先、空の file access mode の既定値を検証する。
- Markdown 依頼文の解析について、 fenced code block 内の見出し風文字列を見出し扱いしないことと、見出し前の前文を本文として保持することを検証する。

## Read this when
- init サブコマンドが管理ディレクトリを Git 管理から外し、無視設定とコミットをどのように作るかを確認したいとき。
- init サブコマンドが既存の staged 変更や .gitignore の staged/unstaged 変更を壊さないことを確認・変更したいとき。
- 通常リポジトリと linked worktree で、設定ファイル、ログ、schema、.gitignore、exclude の保存先や無視状態を検証する必要があるとき。
- tui サブコマンドで、エディタ起動後の依頼文から解決用パラメータを作り、Codex TUI 呼び出しへ file access mode や extra read path を渡す流れを確認したいとき。
- 対話型依頼文の Markdown 解析で、見出し、前文、コードブロック内の見出し風行の扱いを変更・確認したいとき。

## Do not read this when
- 個別のサブコマンド実装そのものを読みたいだけの場合は、実装側の該当サブコマンドに直接進めばよい。
- Codex 呼び出し共通処理、Git helper、テスト用 fixture の詳細だけを調べたい場合は、それらを定義する支援モジュールや実装モジュールを読む方が直接的。
- 対話型起動ではない CLI コマンドの一般的なオプション解析や Typer アプリ構成を確認したい場合は、CLI エントリポイントや対象コマンドの実装を読む方がよい。
- Markdown 文書全般の仕様や汎用 parser の設計を調べたいだけの場合は、このテストで扱う依頼文解析の境界に関係しない限り読む必要はない。

## hash
- 7cad7a21835585ff3afbd64d7f33dd72d87b877c95a94660c8d869ddab872c5a

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 実行経路の realization test。tracked subprocess のプロセスグループ分離、exec/tui 起動時のプロファイル生成・呼び出しログ・終了コード処理・CLI 不在時エラー・保護領域や .agents 変更の拒否を、スタブ codex 実行ファイルと一時リポジトリで検証する。
- commons.runtime_codex、commons.runtime_codex_profile、cmoc_runtime の Codex 呼び出し制御が、外部プロセス起動前後の副作用、sandbox 設定、ログ出力、エラー変換を正しく扱うかを見る入口になる。

## Read this when
- Codex CLI の exec または tui 呼び出し処理、生成される Codex profile、sandbox_workspace_write の writable_roots、CODEX_HOME、PATH 上の codex 解決に関する挙動を変更する。
- run_tracked_codex_subprocess のプロセスグループ管理、tracking file の扱い、子プロセス起動方式を変更する。
- Codex 呼び出しログ、call_log、SubcommandLogger、コンソールに出る purpose・returncode・失敗情報の形式やタイミングを変更する。
- Codex 実行前の extra_read_paths 検査、memo などの保護領域拒否、実行後の .agents 配下変更検出を変更する。
- Codex CLI が見つからない場合、または非 0 終了した場合に CmocError へ変換する制御を確認・変更する。

## Do not read this when
- Codex CLI 呼び出しとは無関係な通常のサブコマンド引数解析、oracle/realization の文書仕様、または INDEX.md 生成ルールだけを調べる。
- LLM 出力品質や Codex 本体の応答内容を評価したいだけで、cmoc 側の subprocess 起動・ログ・保護領域検査の制御を扱わない。
- Git 操作、作業ツリー生成、path model などの基盤処理だけを調べる場合は、それらを直接扱う実装またはテストへ進む。

## hash
- d33083880a03f45c2afdae14d74215c1914fb8c6746baf9458f6628923207ad3

# `test_codex_runtime_home.py`

## Summary
- Codex CLI 呼び出し時の Codex home 解決と事前検証を扱う realization test。環境変数未設定時に通常のホーム配下を使うこと、環境変数で指定された相対パスを保持して実行しつつ記録上はリポジトリ基準で解決すること、Codex home や認証情報が不正な場合に CLI 実行前に利用者向けエラーになることを検証する。

## Read this when
- Codex CLI 実行処理で CODEX_HOME、既定の Codex home、auth.json、プロファイル配置先、呼び出しログに関する挙動を変更または確認するとき。
- Codex home が存在しない、ディレクトリでない、認証情報がない場合の CmocError の summary、detail、next_actions を確認するとき。
- Codex CLI を実際に起動せず、fake executable と monkeypatch で実行環境を組み立てるテスト例を探すとき。

## Do not read this when
- Codex CLI の出力 JSON、ターン完了判定、容量待機、モデルや推論努力の引数変換だけを確認したいとき。
- Codex home 以外のリポジトリ作成 helper、プロファイル stub、Python 実行ファイル生成 helper の実装詳細を確認したいとき。
- oracle file に書くべき正本仕様や設計方針を探しているとき。このファイルは realization test であり、正本仕様そのものではない。

## hash
- 93e187f3d5ae928a9accdef37c14910cf4c9d9da4dbf4762954d601b4e8b4606

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex 実行ラッパーが quota 超過を検出した後、quota availability probe を挟んで再実行または resume する制御を検証する realization test。
- 疑似 codex 実行ファイルを使い、呼び出し引数、標準入力、CODEX_HOME、出力 JSON、call log、SubcommandLogger イベント、コンソール表示まで含めて quota retry 周辺の外部挙動を固定する。
- 並列に quota 超過した複数呼び出しで、代表となる probe が 1 回だけ実行され、それぞれの呼び出しが resume で完了することも検証する。

## Read this when
- Codex 実行中の quota 超過検出、quota availability probe、再実行、resume token 利用の挙動を変更または調査するとき。
- quota retry 時に生成される call log、stdout/stderr/prompt/output のログパス、SubcommandLogger の codex_call イベント、コンソール出力の形式や status を確認するとき。
- quota availability probe が readonly 実行中に .agents 配下を変更した場合の拒否処理と、その失敗ログの扱いを確認するとき。
- 複数スレッドから同時に quota retry が発生した場合の probe 集約と、各呼び出しの再開挙動を確認するとき。

## Do not read this when
- 通常の Codex 実行成功、quota 以外の失敗、または基本的なコマンドライン組み立てだけを確認したいときは、より直接それを扱う実装やテストを読む。
- 設定ファイルの読み込み、プロファイル生成、リポジトリ作成 fixture そのものの仕様を調べたいときは、それらを定義する補助コードを読む。
- oracle file の正本仕様や quota retry 以外のサブコマンド仕様を確認したいときは、対応する oracle doc または対象サブコマンドのテストへ進む。

## hash
- 0da8839aa5bc911c9380a39020b6feaadf6bab589dfbea0e41923aa494287b86

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 実行のリトライ制御を検証する realization test。構造化出力の schema 検証失敗時の再試行、capacity エラー時の再試行、stdout JSONL 以外に現れる capacity/quota 文言をリトライ条件として扱わないことを確認する。
- fake の Codex 実行ファイル、呼び出しログ、subcommand log、出力 JSON、retry 回数を組み合わせて、外部 CLI 呼び出しまわりの制御ロジックとログ記録の境界を検証する。

## Read this when
- Codex CLI 呼び出しの retry 条件、retry 後の成功扱い、または retry 上限到達時の失敗扱いを変更する。
- 構造化出力 schema に合わない応答を受けた場合の再実行、call log の残し方、最終結果がどの call log を指すかを確認する。
- capacity エラーの検出元、capacity retry のログ status、returncode、error detail の扱いを変更する。
- quota/capacity を示す文字列が stdout JSONL 以外に出た場合の扱いを確認する。
- Codex CLI 実行のテスト用 stub、PATH 差し替え、Codex home/profile の setup を使った runtime テストを追加・修正する。

## Do not read this when
- Codex CLI 呼び出しではないサブコマンド処理、設定読み込み、path model、repository 作成処理だけを調べたい。
- retry やログ記録に関係しない通常成功時の出力変換だけを確認したい。
- oracle file の正本仕様そのものを確認したい。
- テスト支援 helper の実装詳細だけを変更したい場合は、支援 helper 側を直接読む。

## hash
- 04ff178d04eb9548f0f9b2df64a3aef8b1cbb54c933cdda4848cf77b2186ca61

# `test_indexing_cli.py`

## Summary
- indexing コマンドと indexing preflight の実現テスト。INDEX.md 生成、Codex によるエントリー生成、fresh hash による再生成スキップ、 malformed entry の再生成、index commit の範囲、worktree 上での実行対象、dirty worktree の拒否、apply worktree での repo config 利用、root 直下 memo 除外と nested memo 対象化を検証する。
- apply 側の INDEX.md merge conflict 解消処理について、競合した INDEX.md を削除して merge commit を成立させる挙動も検証する。

## Read this when
- indexing コマンド、run_indexing_preflight、update_indexes、render_index_entry、commit_index_updates の外部挙動や回帰テストを確認・変更する。
- INDEX.md の生成・再生成・hash freshness・malformed entry 判定・semantic fields の validation に関するテスト観点を確認する。
- cmoc indexing が clean/dirty な通常 worktree・linked worktree・apply worktree でどの root/cwd/config を使い、何を commit するかを確認する。
- INDEX.md の merge conflict を apply 側でどう処理するか、または memo ディレクトリを indexing 対象からどう扱うかのテストを探す。

## Do not read this when
- CLI 全体のコマンド定義、設定モデル、path model、Codex 実行 wrapper の実装詳細だけを確認したい場合は、対応する実装ファイルを直接読む。
- oracle file の正本仕様を確認したい場合は、この realization test ではなく oracle 配下の該当本文を読む。
- indexing 以外のサブコマンドや、INDEX.md 生成と無関係な git 操作の挙動を調べたい場合は、より直接のテストまたは実装へ進む。

## hash
- 5116be4af0a7ffa3f454bb5ebcfc8b31571db6b4d1c6a4f43ecc57b9d47514e8

# `test_indexing_preflight.py`

## Summary
- Codex 実行・TUI 呼び出しの直前に indexing preflight が実行される制御を検証する realization test。preflight が対象 worktree を選ぶ順序、生成された index 変更の commit と clean 状態、repository lock 待機、特定 purpose での preflight skip を扱う。
- 実際の index 本文生成品質ではなく、Codex 呼び出しラッパーと indexing preflight の実行順序・副作用・抑止条件の入口として位置づけられる。

## Read this when
- Codex exec または TUI 呼び出し前に indexing preflight を走らせる制御を変更する時。
- root と cwd が異なる場合に、どの worktree を indexing 対象にするかを確認・変更する時。
- indexing preflight が作った変更を `cmoc indexing` として commit し、作業ツリーを clean に戻す挙動を確認する時。
- 複数処理の同時実行に対する indexing lock の待機挙動を変更する時。
- index entry 生成や conflict resolution のように indexing preflight を skip する purpose 判定を変更する時。

## Do not read this when
- INDEX.md の本文生成アルゴリズム、要約文の品質、ディレクトリ走査規則そのものを調べたい時。
- Codex 実行ラッパーを通らない純粋な indexing API の入力・出力だけを確認したい時。
- git worktree、commit、lock、purpose-based skip のいずれにも関係しない通常の CLI サブコマンド挙動を調べたい時。

## hash
- 001ef8bbaefb02a24c6e94426c4a65388bb8db8a8c91af26d0c0624eb1f5af8d

# `test_prompt_parts.py`

## Summary
- prompt 部品と AgentCallParameter builder が生成する prompt、file access rule、routing rule、各種 standard、structured output schema、model/reasoning/file access 設定を横断的に検証する realization test。
- 標準 prompt の組み立て、markdown rendering、apply fork・review oracle・session join・TUI resolve・indexing builder の期待値が、実装および oracle 側 schema と一致することを確認する入口。
- 16,000 文字を超えるが、agent prompt と structured output schema の構築結果を同じ読み取り文脈で検証するため、共通の render/schema 期待値を一箇所に集約している。

## Read this when
- prompt 構築に含まれる routing rule、file access rule、各種 standard の出力内容や既定の含有有無を変更・確認したいとき。
- AgentCallParameter builder の model class、reasoning effort、file access mode、prompt 本文、structured output schema path の期待値を確認したいとき。
- apply fork、review oracle、session join、TUI resolve、indexing index entry など複数 builder にまたがる schema 同期や prompt 回帰を調べるとき。
- StructDoc や StructCodeBlock の markdown rendering、とくに連続空行や code block 内空行の扱いを確認したいとき。

## Do not read this when
- 個別 builder の実装詳細、prompt 文面の生成ロジック、schema ファイル本体を確認したいだけなら、対応する実装または oracle 側 schema を直接読む。
- 単一機能の外部挙動や CLI 実行結果だけを調べたい場合は、その機能を直接扱う実装・テストを優先する。
- INDEX.md エントリー生成の出力規則そのものを確認したい場合は、index entry standard を生成・検証する対象や関連 standard を読む。

## hash
- 2641417fa6a7330408ae9a33d871bd3c51c795b01ffeed07856171e56e2b4562

# `test_review_oracle_cli.py`

## Summary
- review oracle の CLI 経由の外部挙動と、所見列挙・検証・judge・merge の制御 loop を検証する realization test。report の生成内容、accepted/rejected finding の集計、scope ごとの対象選択、linked worktree 上の review、INDEX 変更の取り込み、処理失敗時の error report、review 実行中に許可される差分境界を扱う。
- 16,000 文字超のテストファイルだが、同じ review run の状態、fake Codex 応答、report 文脈を共有する oracle review の挙動確認として凝集している。

## Read this when
- review oracle コマンドの report 出力、result 判定、finding の採否集計、error report の挙動を変更・確認するとき。
- review oracle の full scope/session scope における oracle 対象選択、gitignored oracle file の除外、binary file や oracle 配下の memo 形状ディレクトリの扱いを確認するとき。
- review oracle が linked worktree、session branch、review worktree、review_fork_commit、review_join_commit をどう扱うべきかを確認するとき。
- 所見の列挙 loop が対象 oracle ごとに関連 finding だけを prompt 文脈へ渡すこと、または merge operation の delete/replace/merge 契約と不正操作拒否を変更するとき。
- review oracle 実行中に生成された INDEX 変更だけを session 側へ取り込み、INDEX 以外の差分を拒否・巻き戻す挙動を確認するとき。

## Do not read this when
- review oracle 以外の review サブコマンド、または一般的な session/init/git helper の仕様だけを確認したいとき。
- Codex CLI の実出力品質や LLM の推論内容そのものを検証したいとき。このテストは fake Codex 応答で制御 flow と外部挙動を確認する。
- oracle file の正本仕様や oracle review の人間向け要求を調べたいとき。まず oracle 側の正本仕様断片を読むべきで、この realization test だけから仕様を逆算しない。
- 単体の merge helper 実装詳細だけを読む場合で、期待する契約が既に明確なときは対象実装を直接読む方が早い。

## hash
- 257e87798cdeb89c1d51d8923c92d5475e3ee4ee3e08f6e9fe69ce0e5738a579

# `test_session_cli.py`

## Summary
- session サブコマンドの CLI 挙動を検証する realization test。session fork / abandon / join について、Git branch・worktree・session state JSON・標準出力/標準エラー・conflict 解決時の Codex 実行条件を、実リポジトリ操作に近い形で確認する。
- session state の生成・更新、session branch と home branch の遷移、linked worktree 上での操作、cleanup 失敗時の rollback、join 時の conflict marker 判定や削除 conflict 解決など、session lifecycle の外部挙動を読む入口になる。

## Read this when
- session fork が session branch と state をどのように作り、session-id 衝突時に既存 state を壊さず retry または失敗するかを確認したいとき。
- session abandon が home branch へ戻る条件、session branch 削除、state の abandoned 化、home branch 不在時や cleanup 失敗時のエラー出力・rollback を確認したいとき。
- session join が session branch の変更を home branch に統合し、linked worktree、branch 削除失敗 warning、未コミット差分エラー、merge 後の予期しない conflict marker 残存エラーをどう扱うかを確認したいとき。
- oracle 配下の conflict 解決で Codex 実行に REALIZATION_WRITE profile と対象ファイルの extra writable path が渡ること、また解決後の conflict marker 検出条件を確認したいとき。
- session サブコマンドの利用者向け出力が stdout と stderr のどちらに出るべきか、成功・失敗時の report 項目がどう検証されているかを確認したいとき。

## Do not read this when
- session 以外のサブコマンドや、CLI 全体の option parsing・command 登録だけを確認したいとき。
- session state の schema や path モデルの正本仕様を確認したいときは、対応する oracle file または実装側の state/path 定義を直接読む。
- Git helper、test fixture、runner、temporary repository 作成方法そのものを調べたいときは、共通 test support を読む。
- Codex 実行 wrapper の一般仕様や file access mode 全体の意味を確認したいだけのときは、runtime や basic.acp 側を読む。

## hash
- ae141d375590381560fd4e95d8616f4ed3ce06bd3b0199ca58742db2f87d7c87
