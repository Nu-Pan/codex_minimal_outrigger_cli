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
- apply fork を CLI から実行したときの report 生成、収束判定、再検査対象の制御、error report、session state 更新をまとめて検証する realization test。所見列挙、所見適用、commit message、変更要約、report schema の観測が同じ制御 loop に閉じるため、apply fork report 周辺の期待値を一箇所で読む入口になる。
- 未追跡 file を含む fork 後差分の抽出、fallback 変更要約、編集禁止対象差分の error 化、rolling apply fork が前回 apply join 後の変更だけを対象にすることも、この report 制御の一部として扱う。

## Read this when
- apply fork の CLI 実行結果、exit code、stdout に出る report path、report 本文の result や Finding Count、変更要約表示を確認したいとき。
- apply fork が所見適用後に変更 file を再調査する条件、INDEX.md を再調査対象から外す条件、上限到達時の converged/unconverged 判定を変更・検証するとき。
- apply fork の所見適用が差分を作らない場合、commit message 生成を行わないことや apply branch が進まないことを確認したいとき。
- apply fork 中に編集禁止対象の差分が発生した場合の stderr、error state、error report、未 commit 差分を含む変更要約を扱うとき。
- apply fork report 用の fork 後差分検出が未追跡 file を含むか、変更 path fallback summary がどう作られるかを確認したいとき。
- rolling apply fork の調査対象が前回 apply join 後の変更に限定されることや、session state の apply join snapshot 更新との関係を確認したいとき。

## Do not read this when
- apply fork の内部実装だけを局所的に変更したく、CLI 経由の report・session state・git commit まで含む外部挙動を確認する必要がないとき。
- apply join、session fork、init などの個別 command 自体の仕様や挙動を調べたいだけで、apply fork report 制御との結合を扱わないとき。
- Codex 実行 wrapper、AgentCallParameter、structured output schema の一般的な仕組みを調べたいだけで、この test が fake している apply fork 用応答の期待値に関心がないとき。
- INDEX.md 生成やルーティング文書そのものの挙動を調べたいとき。ただし apply fork の再調査対象から INDEX.md を除外する挙動を扱う場合は読む。

## hash
- 3d2195a4f9374476ac5893c8dae8c254ce0881d062e97b288c12587a508518fc

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
- CLI の初期化処理と対話起動処理に関する realization test。初期化時の .cmoc 管理除外、.gitignore 更新、既存 staged/unstaged 変更の保護、設定ファイルの既定値同期、サブコマンドログ記録、linked worktree での保存先・ignore・commit 挙動を検証する。
- 対話起動について、エディタで作られた依頼文からコメントを除去してパラメータ解決を行い、解決結果から Codex 呼び出し用パラメータを組み立て、完了プロンプトをログへ保存する制御を検証する。
- Markdown プロンプト解析について、fenced code block 内の見出し風文字列を無視し、見出し前本文と見出し階層を保持する挙動を検証する。

## Read this when
- 初期化コマンドが .cmoc を Git 管理から外し、ignore 設定を追加し、cleanup commit を作る挙動を変更・確認したいとき。
- 初期化コマンドが利用者の既存 staged 変更や .gitignore の staged/unstaged 変更を壊さないことを確認したいとき。
- linked worktree 上で初期化または対話起動を実行した場合の、repo root と worktree root の使い分け、ログ保存先、schema 保存先、ignore 設定、commit 対象を確認したいとき。
- 設定ファイルの初回生成、既定値、既存の人間設定を保持したまま不足キーを補う挙動を変更・確認したいとき。
- 対話起動でエディタ編集後のプロンプトを整形し、パラメータ解決用 Codex 実行と TUI 用 Codex 起動へ渡す値を確認したいとき。
- Markdown プロンプト parser の見出し検出、見出し前本文の扱い、階層構造の保持を変更・確認したいとき。

## Do not read this when
- 初期化、対話起動、Markdown プロンプト解析に関係しないサブコマンドの挙動だけを調べたいとき。
- Codex 実行ラッパーそのもののプロセス起動仕様や外部 CLI の詳細を調べたいときは、実装側の呼び出し処理を直接読む方がよい。
- 設定項目の正本仕様やパス概念そのものを確認したいときは、oracle 側の該当仕様を読む方がよい。
- テスト支援関数や temporary repository fixture の実装詳細だけを調べたいときは、支援モジュールを直接読む方がよい。

## hash
- 935565fd5bbe27dc1fab1611fcff207f94f87f7a4019c82d91bc157aa38fdba8

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
- review oracle の CLI 経由の report 生成、所見列挙・検証・judge・merge の loop 制御、対象 oracle 選択、review worktree での実行と INDEX.md 変更の取り込み、失敗時 report、想定外差分の拒否をまとめて検証する realization test。
- 16,000 文字を超えるが、同じ review run の状態、fake Codex 応答、report 文脈を共有する外部挙動群を一箇所で扱うため、oracle review の読み取り文脈を保つ凝集したテスト群として位置づけられている。

## Read this when
- review oracle の report に含める verdict、評価対象、accepted/rejected findings、件数、no_targets、error 表示などの外部出力仕様を確認・変更する。
- review oracle の対象選択で full/session scope、短縮 option、gitignored oracle、binary、memo 形状の path、linked worktree 上の oracle をどう扱うかを確認・変更する。
- 所見評価 loop で enumerate の再実行文脈、challenger/advocate reason の受け渡し、judge 結果、merge operation の契約と不正 operation 拒否を確認・変更する。
- review oracle 実行用 worktree、review が生成した INDEX.md の merge、INDEX.md 削除 conflict 解決、INDEX.md 以外の想定外差分の拒否を扱う実装を変更する。
- review oracle の途中失敗時に error report を残し、CLI がどこへ何を出力するかを確認・変更する。

## Do not read this when
- review oracle 以外のサブコマンド、session 管理、設定読み込み、git helper の一般挙動だけを調べたい場合。
- oracle file や realization file の概念定義、正本仕様断片そのもの、または人間が編集する oracle 文書の内容を確認したい場合。
- review oracle の内部 helper の細かな実装だけを局所的に読む必要があり、外部挙動や CLI report との対応を確認しない場合。
- 通常の INDEX.md ルーティング文書の生成規則や schema だけを確認したい場合。

## hash
- fb1bcbdd95446c0d256449bfb602a0ddb48d543d23892e05de28e4c8fc41cc3a

# `test_session_cli.py`

## Summary
- session サブコマンドの CLI レベルの挙動を検証する realization test。session fork が session branch と state を作成し、session-id 衝突時に既存 state や元 branch を壊さず retry または失敗することを扱う。
- session abandon が home branch へ戻り session branch を削除して state を abandoned にする正常系と、home branch 欠落や cleanup 失敗時の rollback・エラー出力を扱う。
- session join が session branch の変更を home branch へ取り込み、oracle conflict 解決時の Codex 実行条件、conflict marker 判定、削除 conflict の staging、session branch 削除失敗時の警告、stdout/stderr のエラー出力境界を扱う。
- 通常 worktree と linked worktree の両方で、session 操作が現在作業中の worktree branch と head を基準にし、root worktree の branch を不要に切り替えないことを検証する。

## Read this when
- session fork、session abandon、session join の CLI 外部挙動、出力、終了コード、git branch/state file の副作用を変更する時。
- session state の state 値、session_home_branch、session_start_commit、last_joined_apply_oracle_snapshot_commit、apply state など、session 操作で保存・更新される永続状態を変更する時。
- session-id 生成の衝突処理、retry 回数、既存 session state を上書きしない保証、失敗時に元 branch へ戻す挙動を確認する時。
- linked worktree 上で session 操作を実行した場合の branch 判定、head commit、root worktree への副作用を確認する時。
- session join の merge conflict 解決、oracle file への REALIZATION_WRITE profile 適用、conflict marker 検出、削除 conflict 解決後の staging を変更する時。
- session subcommand のエラー報告を stdout に出すべき既知エラーと、merge 後の予期しないエラーを stderr に出す境界を確認する時。

## Do not read this when
- session 以外のサブコマンド、または CLI を通さない低レベル helper の単体仕様だけを確認したい時。
- session 操作の実装構造や内部 helper の詳細を調べたいだけで、CLI から見える挙動・出力・git 副作用を確認する必要がない時。
- oracle file の正本仕様そのものを確認・変更したい時。realization test は正本仕様ではないため、対応する oracle file を優先する。
- Codex 実行結果の品質や LLM 出力内容そのものを検証したい時。この対象は session join が Codex を呼ぶ条件や file access mode を検証するだけで、生成品質は扱わない。

## hash
- ff6ce6aa3615ede4afa7cdbf715cb862dbb6d34521356ec5884fbcb7dc359ce5
