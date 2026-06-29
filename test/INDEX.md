# `_profiles.py`

## Summary
- file access profile の代表的な組み合わせをテストから再利用するための補助定義を置く。oracle、realization、INDEX.md それぞれの read/write/deny 権限パターンを名前付き profile として提供する。

## Read this when
- テストで read-only、oracle-only read、realization write、oracle write、repo write のいずれかの file access profile を使いたいとき。
- 複数のテストで同じ file access profile 設定を重複定義しており、既存の共有 profile を確認したいとき。

## Do not read this when
- file access profile の構築ロジックや権限モデルそのものを確認したいとき。
- 個別機能のテストケース本体や期待される外部挙動を確認したいとき。

## hash
- 40976a0796e787decaa08b318d8e7926798ccb06d69a4c7a4f1e8fb97feb23d9

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
- active apply run を CLI 経由で破棄する外部挙動を検証する realization test。worktree、branch、session state の cleanup、cleanup 対象欠落時の警告、running process 停止、実行位置判定、linked session worktree との境界条件を同じ abandon 操作の文脈で扱う。
- apply process identity の読み取り、child process group を含む停止順序、PID reuse や race 済み終了の扱いなど、abandon 前処理として必要な process 停止ロジックの制御境界も検証する。
- 16,000 文字を超えるが、active apply run の破棄という単一責務に閉じ、同じ state fixture と境界条件を共有するため、分割せず読み取り文脈を一箇所に保っている。

## Read this when
- apply abandon の CLI 挙動、出力、終了コード、state 遷移、apply worktree と apply branch の削除を変更または確認するとき。
- running apply を abandon する際の process identity 読み取り、tracked child process group の停止、PID reuse 防止、終了 race の扱いを変更または確認するとき。
- apply worktree 内、linked session worktree、linked apply worktree、stale apply branch など、abandon 実行位置ごとの許可・拒否条件を調べるとき。
- cleanup 対象がすでに存在しない場合の警告成功、または破損 state や process identity 欠落時に cleanup 前で拒否する挙動を確認するとき。

## Do not read this when
- apply abandon 以外の apply サブコマンドの通常フローや Codex 実行結果の品質を調べたいとき。
- session fork、init、git helper、runner などの共通 fixture や補助 API 自体の実装を確認したいとき。
- oracle file の正本仕様や実装標準を確認したいとき。
- active apply run の破棄に関係しない一般的な worktree、branch、session state の挙動を調べたいとき。

## hash
- ec0375e8de29f038d1dc8b4010eae864fadb5ba208f43ab7385d198d6ddc6158

# `test_apply_fork_cli.py`

## Summary
- apply fork サブコマンドの realization test。Codex 実行を fake に差し替え、apply run の開始・完了、session state 更新、apply branch/worktree 作成、linked worktree 上の HEAD 起点、設定読み込み失敗時の中断、.gitignore の扱い、target 正規化を検証する。
- CLI 経由の統合的な挙動確認と、apply fork module の一部関数を直接呼ぶ境界条件確認の両方を含むため、apply fork の外部副作用や state/worktree/branch のライフサイクルを調べる入口になる。

## Read this when
- apply fork の実装変更により、session state の apply 状態、apply branch 名、apply worktree 配置、PID file 削除、完了判定が変わる可能性があるとき。
- linked worktree 上で apply fork を実行した場合の起点 commit、session branch、apply branch、worktree 配置の期待挙動を確認したいとき。
- apply fork 実行前の cmoc config 読み込み失敗時に、apply run を開始しないことやエラー出力先を確認したいとき。
- apply fork が .cmoc ignore を確保する処理、session 側の .gitignore を dirty にしない処理、または apply branch 側で .gitignore を編集対象にできる処理を変更するとき。
- apply fork の対象 path 正規化で、root 直下の memo 除外、入れ子の memo directory の保持、binary file の保持を確認したいとき。
- Codex 呼び出しを伴う apply fork loop の呼び出し目的、所見列挙、所見適用、変更要約の制御をテスト上で追いたいとき。

## Do not read this when
- apply fork 以外の apply 系サブコマンドや session fork 単体の仕様を調べたいだけのとき。
- Codex CLI や LLM 出力内容そのものの品質を検証したいとき。この対象は Codex 実行結果を fake にして制御フローと副作用を検証する。
- path model、oracle/realization の概念定義、INDEX routing の規約を確認したいとき。
- apply fork の内部 helper 実装そのものを読みたいとき。この対象は期待される外部挙動と重要な境界条件を示すテストであり、実装詳細の入口ではない。

## hash
- 299d8a600d3ab3b419a47ee298117556c499bfbbc77d3d80778aeade1dded333

# `test_apply_fork_report_cli.py`

## Summary
- apply fork の CLI 経由テストとして、所見列挙から適用、commit、変更要約、report 生成、session state 更新までの制御を検証する。
- apply fork report の収束・未収束・error・変更ファイル再調査・rolling fork を、同じ loop と report schema の観測結果として一箇所で扱う。
- apply fork 用 ACP builder が src のみの import path や packaged layout で読み込めること、prompt と structured output schema が正しく組み立てられることも検証する。

## Read this when
- apply fork の CLI 実行結果、終了コード、report 内容、変更要約、commit message、session state 更新を確認または変更するとき。
- apply fork が変更後の file を再調査する条件、INDEX.md を再調査対象から外す条件、差分なし適用時の未収束扱いを確認するとき。
- apply fork の error report が未 commit 差分や未追跡 file を変更要約に含める挙動を確認するとき。
- rolling apply fork が前回 apply join 後の変更だけを対象にする挙動を確認するとき。
- apply fork 用の所見列挙・所見適用・変更要約 ACP builder の import、prompt、schema path、path placeholder 検証を変更するとき。

## Do not read this when
- apply fork 以外の subcommand の一般的な CLI 挙動だけを確認したいとき。
- apply fork report の外部挙動ではなく、report markdown の細かな整形 helper 単体だけを確認したいときは、実装側の report 生成対象を直接読む。
- ACP builder 全般の共通構造だけを調べたいときは、builder 共通処理や対象 builder の実装を直接読む。

## hash
- 2f8bebf3d00717ef344a1a043518bbb9f970910c1b6ea14954ffb0a4888a4a1b

# `test_apply_join_cli.py`

## Summary
- apply run を session へ join する CLI 外部挙動を検証する realization test。join 成功時の merge、state 更新、report 生成、apply worktree・branch の cleanup と、dirty worktree、stale apply branch、想定外差分、merge conflict などの拒否・中止条件を同じ fixture と git 状態の文脈で扱う。
- 16,000 文字を超えるが、apply join の成功条件と拒否条件を一箇所で確認する凝集性を優先しているテスト群であり、worktree cleanup、branch cleanup、state 遷移、report、差分分類、conflict 処理を横断して読む入口になる。

## Read this when
- apply join の CLI 挙動、終了コード、標準出力、report 生成、state 更新、cleanup の期待値を確認・変更したいとき。
- apply worktree から join した場合、session worktree から join した場合、linked session worktree から join した場合の作業ディレクトリ別挙動を確認したいとき。
- dirty apply worktree、stale apply branch、想定外の apply 差分、削除パス、rename target、root memo、.gitignore 変更、merge conflict の扱いを検証するテストを探しているとき。
- apply join の差分分類 helper や conflict 解決後継続の制御が、CLI 経由の外部挙動としてどう期待されているかを確認したいとき。

## Do not read this when
- apply fork、session fork、init など join 以外のサブコマンド単体の挙動を確認したいだけのとき。
- apply join の実装内部構造、関数分割、git 操作 helper の実装詳細を直接変更したいときは、対応する実装側を先に読む。
- Codex 実行結果そのものや LLM 出力品質を検証したいとき。この対象では Codex 実行は fake に置き換え、join 後の外部副作用を検証している。
- 一般的な test fixture、repo 作成 helper、runner helper の仕様を確認したいだけのときは、共通 support 側を読む。

## hash
- db9c00e9643569b5c9ef444fa5ae130d8a8a2e52bb7e57173dee38a52227aa77

# `test_basic_runtime.py`

## Summary
- cmoc の基礎 runtime 契約を横断的に検証する realization test。root placeholder 解決、repo/run/work root 判定、config 既定値と不正値、CmocError の Markdown 表示、CLI error の stdout 出力、subcommand log、`.cmoc` ignore、file access profile、Codex sandbox profile、binary 判定など、サブコマンド実行前提として一緒に崩れやすい挙動を扱う。
- 個別サブコマンドより下位の共通 runtime 境界に閉じた回帰テスト群であり、共通 fixture と root 状態を共有して runtime の基本契約をまとめて確認する入口になる。

## Read this when
- root placeholder、repo root、run root、work root、linked worktree、run worktree 作成・削除の基本挙動を確認または変更する。
- CmocConfig、config 読み込み、model class、reasoning effort、config 不正値の扱いを確認または変更する。
- CmocError、render_error、CLI parse error、想定済み CLI error、stdout/stderr の error report 表示を確認または変更する。
- subcommand log の生成条件、timestamp 衝突時の log path、pre-log check 失敗時の副作用抑制を確認または変更する。
- `.cmoc` の gitignore 反映、file access profile、Codex profile の sandbox mode・writable_roots・extra writable path 制限を確認または変更する。
- branch session id、apply branch session id、branch からの session state 読み込み条件を確認または変更する。
- binary 判定や duration 表示など、共通 runtime helper の外部挙動を確認または変更する。

## Do not read this when
- 特定サブコマンド固有の業務フロー、出力内容、状態遷移だけを調べたい場合は、そのサブコマンドのテストまたは実装を読む。
- oracle file の正本仕様そのものを確認したい場合は、対応する oracle doc または oracle src を読む。
- 個別の実装 helper の内部構造だけを変更し、共通 runtime 契約や CLI 表示・sandbox profile に影響しないことが明らかな場合は、対象実装とより局所的なテストを読む。

## hash
- 863d517827d24b026a507681d36a7a44cf8fad9f34a3e4675bc1298f7a56055a

# `test_cli_init_tui.py`

## Summary
- init と対話起動前処理の外部挙動を検証するテスト群。cmoc 管理領域の ignore 化、既存差分を壊さない初期化 commit、既定設定の作成・同期、linked worktree での repository/runtime 準備、Markdown prompt 解析、TUI 起動 parameter 構築まで、利用開始直後の CLI 境界に属する回帰確認を扱う。
- 16,000 文字を超えるが、対象責務は cmoc 初期化と TUI 起動前の repository/runtime 準備に閉じており、初期化済み状態を共有する挙動を一箇所で読むためのテストとしてまとまっている。

## Read this when
- init の外部挙動、特に .cmoc 配下の untrack、ignore 設定、cleanup commit、既存 staged/unstaged 差分の保護を確認・変更する。
- 初期設定ファイルの既定値生成、既存値を保持した不足 default 同期、または cmoc 管理ファイルが git 管理対象に残らないことを確認・変更する。
- linked worktree 上での init や TUI 起動前処理について、repository root と作業ディレクトリの使い分け、ignore 設定、ログ保存場所、schema 生成場所を確認・変更する。
- TUI 起動時の editor 実行、HTML comment 除去を含む prompt 整形、file access profile 解決、Codex 実行 parameter、complete prompt 保存を確認・変更する。
- subcommand invocation log の生成場所や、起動された CLI command と argv の記録内容を確認・変更する。

## Do not read this when
- CLI の init/TUI 境界ではなく、個別サブコマンドの業務ロジックや出力仕様だけを確認したい。
- Codex 実行 wrapper、AgentCallParameter、file access profile の型定義や内部変換そのものを確認したい場合で、起動前処理からの利用例が不要である。
- oracle 仕様、設定 schema、path model などの正本仕様断片を確認したい場合。
- 単体 helper の細かな実装詳細だけを変更する場合で、init または TUI の外部挙動回帰を確認する必要がない。

## hash
- 479f4b1bd10e5b548053286eef6ca637bf3b6e298fa0ab5b0402aedd9c68f03f

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI の exec/TUI 呼び出し時のランタイム挙動を検証する realization test。Codex subprocess の profile 生成、cwd・sandbox・schema 配置、追跡 PID、許可外 read path、非ゼロ終了、CLI 不在時エラーなど、外部 Codex 起動境界の制御を扱う。

## Read this when
- Codex CLI を起動する runtime 層、profile 生成、sandbox/write root、cwd 決定、schema state の保存先を変更する。
- Codex subprocess の process group 追跡、APPLY_PROCESS_TRACKING_ENV の扱い、または codex 実行ラッパーの環境変数引き継ぎを変更する。
- TUI 呼び出し前の extra_read_paths 検証、pure oracle read 時の cwd、linked worktree での TUI 実行、Codex CLI 失敗時のエラー表示を変更する。
- Codex CLI が存在しない場合や非ゼロ終了した場合の CmocError の条件・メッセージを変更する。

## Do not read this when
- Codex runtime を経由しない通常の CLI コマンド、設定値 parsing、path model の仕様だけを確認したい。
- oracle file の本文仕様や INDEX.md 生成規則を確認したい。
- Codex subprocess の外部起動境界ではなく、agent call parameter の値オブジェクトや model/reasoning の列挙定義だけを変更する。

## hash
- e5bc57f06e60de8d0f1fc59a52370279f7e48a2b309ea7c2db766b7710d13781

# `test_codex_runtime_home.py`

## Summary
- Codex CLI 実行時の Codex home 解決と事前検証を確認する pytest 群。CODEX_HOME 未設定時の既定値、相対 CODEX_HOME の保持と解決基準、profile 配置先、call log 記録、Codex CLI 呼び出し前に失敗すべき Codex home/auth.json 不備のエラー内容を扱う。

## Read this when
- Codex CLI 呼び出し前の CODEX_HOME 解決・検証、auth.json 必須条件、profile 生成先、call log の codex_home 記録を変更・確認する。
- run_codex_exec の作業ディレクトリと相対 CODEX_HOME の関係、特に oracle 読み取り profile での解決基準を確認する。
- Codex home 不備時の CmocError の summary/detail/next_actions を変更・確認する。

## Do not read this when
- Codex CLI の出力イベント解析、capacity 制御、通常の subprocess 失敗処理など、Codex home 解決以外の run_codex_exec 挙動だけを確認する。
- profile 定義そのものや sandbox 権限 profile の内容を確認したい場合。
- oracle file や INDEX.md の生成・更新ルールを確認したい場合。

## hash
- ed1b2a2f1eae7aa8ccc18e09fa2245adeeb2bb4b4ea4b33b23d2d12fd9e1022f

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex exec が quota exceeded になった後、quota availability probe、resume token による再開、token 不在時の再実行、call log・subcommand log・CODEX_HOME・cwd の扱いを含む retry 状態機械の外部挙動を検証するテスト群。
- 並列実行時に quota probe が代表 1 回に共有され、probe 成功時は待機中の呼び出しが再開し、probe 失敗時は待機側も失敗することを確認する。

## Read this when
- quota exceeded 後の Codex exec retry、probe、resume、再実行の挙動を変更・調査する場合。
- Codex 呼び出しログ、subcommand log、probe prompt、stdout/stderr/output/prompt log path の記録内容を確認する場合。
- CODEX_HOME が相対パスのときの実行 cwd や `--cd` の扱いを調査する場合。
- 複数の Codex exec が同時に quota 待機へ入る場合の probe 共有・失敗伝播を変更または検証する場合。

## Do not read this when
- quota retry と無関係な通常の Codex exec 成功・失敗処理だけを確認したい場合。
- CLI サブコマンドの一般的な引数解析、設定読み込み、リポジトリ作成 fixture の実装を調査したい場合。
- quota 待機からの復帰ではなく、個別 profile の定義や権限プロファイルの内容そのものを確認したい場合。

## hash
- ec665fbcd238896d3d8110cc234ff8a7859bdd40684d5991572a4d172cdf0a1b

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 呼び出しの retry 制御を検証する realization test。structured output の parse/schema validation 失敗、capacity JSONL error、stdout JSONL 外の error marker を扱い、call log・prompt log・subcommand log・戻り値が期待通りになることを確認する。

## Read this when
- Codex CLI 実行 wrapper の retry 条件、structured output 検証、capacity retry、quota/capacity marker の解釈を変更する時。
- Codex call log、stdout log、prompt log、subcommand event の status・error・returncode・path 記録を変更する時。
- fake Codex executable を使った runtime retry 系テストの既存観点へケースを追加できるか確認する時。

## Do not read this when
- Codex CLI 呼び出し前の agent call parameter 構築や profile 定義だけを確認したい時。
- repository fixture、Codex home fixture、stub executable helper の実装自体を変更したい時。
- retry を伴わない通常成功時の Codex CLI 実行や、他サブコマンド固有の制御を確認したい時。

## hash
- b1c7747c5568d8b6cb0e6b94cc43332046e1ff3625709099a1763dbf3d85f60f

# `test_indexing_cli.py`

## Summary
- indexing preflight と indexing subcommand が routing document を生成・更新・commit する CLI 境界の回帰テストをまとめる realization test。
- INDEX.md conflict 解決、未初期化・dirty worktree の拒否、linked worktree 対象化、repo config 利用、fresh hash による再生成スキップ、index path だけの commit を外部挙動として検証する。
- INDEX.md エントリーの schema 検証、 malformed entry の再生成、空ディレクトリ・memo 除外境界・symlink cycle・並列生成など、routing 更新ワークフローの観測点を扱う。

## Read this when
- indexing CLI の実行条件、失敗時メッセージ、commit 条件、linked worktree での対象 root 判定を変更・確認するとき。
- INDEX.md の生成・更新、hash 再利用、entry schema validation、malformed entry 再生成、空ディレクトリへの INDEX.md 配置を変更・確認するとき。
- indexing preflight が通常の indexing subcommand と異なり、既存の非 INDEX.md 差分を許容しつつ INDEX.md だけ commit する挙動を確認するとき。
- routing document 更新処理の並列化、memo ディレクトリの扱い、directory symlink cycle の除外を変更・確認するとき。
- apply 側の INDEX.md conflict 解決が conflict 中の INDEX.md を削除して merge commit を完了する挙動を確認するとき。

## Do not read this when
- 個別の indexing 実装 helper の内部アルゴリズムだけを調べたい場合は、実装モジュールを直接読む方が適切。
- Codex が生成する自然言語エントリーの品質や内容そのものを評価したい場合は、このテストではなく生成プロンプトや schema 側を確認する。
- indexing 以外の CLI subcommand、通常 apply workflow、設定ファイル全般の仕様を調べる場合は、該当する実装・テストへ進む方が適切。

## hash
- ba84ba2a5f8fac06dd16494e65b04728e1b72568d45ca51a5e25aa2604e2bf43

# `test_indexing_preflight.py`

## Summary
- Codex 実行前の indexing preflight が、CLI/TUI 呼び出し前に INDEX.md を更新してコミットする制御、cwd が worktree 内にある場合の更新対象選択、repository lock 待機、特定 purpose での preflight skip を検証する pytest 群。
- runtime_codex_preflight と commons.indexing の連携を、実 Codex 実行は monkeypatch で差し替え、git worktree とロック競合を含む外部挙動として確認する。

## Read this when
- Codex 呼び出し前に INDEX.md 更新を走らせる条件、順序、コミット有無、作業ツリーの clean 状態を変更または確認したいとき。
- root と cwd が異なる worktree を指す場合に、どちらのリポジトリへ indexing preflight を適用するかを確認したいとき。
- indexing lock による排他制御や、他プロセスがロックを保持している間の待機挙動を変更するとき。
- index entry 生成や conflict resolution など、indexing preflight を再帰・衝突回避のために skip する purpose 判定を変更するとき。

## Do not read this when
- INDEX.md の本文生成ロジック、ルーティング文書の内容、または index entry の品質を確認したいだけの場合。
- Codex runtime の subprocess 実行、TUI 表示、AgentCallParameter 自体の構造を確認したい場合。
- git repository や worktree を作るテスト補助関数の実装を確認したい場合。

## hash
- 742c9edc161f5b6158e2a5d9c0ff3d27d03640517780bf4aaa9ff1d0ea27f5cd

# `test_prompt_parts.py`

## Summary
- agent prompt の標準部品、routing、file access、structured output schema、各種 ACP builder parameter の生成結果を横断的に検証するテスト群。
- prompt 構築で同じ読み取り文脈に入る render 結果、root token、schema path、file access profile、model class、reasoning effort、動的文字列保持を一箇所で確認する。
- 16,000 文字を超えるが、agent prompt と structured output schema の構築結果を検証する責務に閉じており、分割すると共通期待値の追跡に複数ファイルが必要になる。

## Read this when
- prompt builder の標準文書や complete prompt の出力内容を変更し、render 結果や含まれる標準 section の回帰を確認したいとき。
- ACP builder parameter の model class、reasoning effort、file access profile、schema path、prompt に含める root token や動的入力保持を変更するとき。
- review oracle、apply fork、indexing、session join、TUI parameter 解決に関する builder の structured output schema 連携を確認するとき。
- StructDoc や StructCodeBlock の markdown render における空行処理を変更するとき。

## Do not read this when
- 個別 builder の実装詳細だけを調べたい場合は、対応する builder 実装や oracle source を直接読む。
- prompt や schema の生成結果ではなく、CLI 実行経路やファイル探索の実処理を確認したい場合は、その責務を持つ実装・テストへ進む。
- oracle file の仕様文そのものを確認したい場合は、このテストではなく oracle 配下の該当本文を読む。

## hash
- 61bb5aae0d3dcb1bf9183cf8b7ebd5dec1795426b5ed60d168610e390ce692d9

# `test_review_oracle_cli.py`

## Summary
- review oracle の CLI 実行を通じて、report 生成、所見の列挙・検証・judge・merge、scope ごとの対象選択、review 用 worktree と join commit、エラー時 report、許可されない差分の拒否を外部挙動として検証する realization test。
- 16,000 文字超の大きなテストだが、同じ review run の fake Codex 応答、report 文脈、所見 loop 状態を共有するため、oracle review の外部挙動確認を一箇所に集約している。

## Read this when
- review oracle command の出力 report 構成、metadata、accepted/rejected finding の表示順や件数集計を変更・確認する時。
- review oracle の full scope または session scope で、gitignored oracle、binary oracle、memo 形状の path、変更対象なしの場合の扱いを確認する時。
- 所見 loop における enumerate、validate challenger、validate advocate、judge、merge の呼び出し順、prompt に含める既存所見、merge operation の契約を変更・確認する時。
- review oracle が linked worktree 上の session branch を扱う挙動、review worktree の場所、review index 変更の merge、index conflict 解決を確認する時。
- review oracle 処理中の失敗時 report、標準出力への error 表示、review 側が生成した許可外差分の拒否と復元挙動を確認する時。

## Do not read this when
- oracle file の正本仕様そのものや、人間が管理する仕様文書の内容を確認したいだけの時。
- 通常の session fork、init、git helper、設定読み込みなど、review oracle の外部挙動に直接関係しない CLI 基盤を調べる時。
- report renderer や merge helper の実装詳細だけを局所的に確認したい時。ただし期待される外部出力や制御契約を確認する場合は読む。
- Codex CLI や LLM の品質評価そのものを調べる時。この対象は fake 応答を使い、cmoc 側の制御と出力を検証している。

## hash
- 4cba81a523f4670b96bf50c1a44aa9d4624cfa0be71338e3d3fbb14c2cb57cd5

# `test_session_cli.py`

## Summary
- session fork/join/abandon の CLI 外部挙動を、git branch と session state のライフサイクルとしてまとめて検証する pytest ファイル。
- session branch 作成、session state 作成・更新・破損時拒否、linked worktree 上の home branch 扱い、join/abandon 後の branch 削除や cleanup 失敗時 rollback を扱う。
- join 時の conflict resolution agent 呼び出し、oracle conflict 書き込み権限、delete conflict staging、dirty worktree 拒否、エラー出力先の stdout/stderr 境界も検証する。

## Read this when
- session fork、join、abandon の CLI 挙動や回帰テストを確認・変更したいとき。
- `.cmoc/sessions/*.json` の session state、session home branch、session branch の作成・削除・状態遷移に関わる変更をするとき。
- linked worktree 上で session 操作がどの branch と HEAD を使うべきか確認したいとき。
- session join の merge conflict 解決、oracle file conflict に対する Codex 実行 profile、conflict marker 検出、delete conflict staging を変更するとき。
- session join/abandon の失敗時出力、stdout/stderr の使い分け、cleanup 失敗時の rollback や再実行案内を確認するとき。

## Do not read this when
- session 以外のサブコマンドや、session CLI と関係しない共通 helper の単体挙動だけを確認したいとき。
- fork/join/abandon の外部挙動ではなく、内部関数の純粋な unit test や低レベル git wrapper の詳細だけを確認したいとき。
- oracle file の正本仕様そのものを確認したいとき。このファイルは realization test であり、正本仕様ではない。
- INDEX.md エントリー生成やルーティング文書の形式だけを確認したいとき。

## hash
- 332d57cbb46324bfcc84ee560eba5f0aa2f12ffe397b77f07269c3ebd489318d
