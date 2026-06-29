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
- active apply run を破棄する CLI 挙動を、worktree・branch・session state の cleanup、実行位置の復帰、running process 停止、警告・拒否条件までまとめて検証する realization test。
- completed/running apply の abandon 成功経路、cleanup 対象欠落時の warning、process identity の読み取りと lock 待ち、PID reuse・終了済み process・child process group の扱いを同じ文脈で固定する。
- linked session worktree や linked apply worktree からの実行、stale apply branch、破損した apply branch、dirty worktree など、active apply run の破棄境界を外部挙動として確認する入口。

## Read this when
- apply abandon の成功時に apply worktree、apply branch、apply state、apply process id file がどう削除・初期化されるべきか確認したいとき。
- running apply を abandon する際に、親 apply process と記録済み Codex child process group をどの順序・条件で停止するかを変更または確認するとき。
- pidfd signal、PID reuse、既に終了した process、zombie leader、process id file 更新中の advisory lock など、process 停止まわりの競合・安全性を扱うとき。
- apply worktree 内、linked session worktree、linked apply worktree、stale apply branch など、現在位置から破棄対象の active apply run を特定する挙動を調べるとき。
- cleanup 対象が先に消えている場合の warning 成功、running state なのに process identity が無い場合、apply branch から worktree を導けない場合、dirty linked session worktree の拒否を確認するとき。

## Do not read this when
- apply fork の生成処理や Codex 実行結果の解釈だけを調べたいとき。この対象では fork 結果を fake にして abandon 前提の state を作るだけである。
- session fork、init、git worktree 作成の一般挙動を確認したいとき。この対象では abandon 境界条件を作るための fixture として利用している。
- apply abandon 以外のサブコマンド、または apply run を保持・継続する挙動を調べたいとき。
- CLI ではなく低レベル helper の単純な path 変換や state schema 全体を調べたいとき。ただし process identity 読み取り・停止の abandon 連動挙動を扱う場合は読む価値がある。

## hash
- 5fbd29b88af6fe300e993d8876822ef72266dde53d6c70178a81708ddbf8c55c

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
- apply fork の CLI 実行を通じて、所見列挙、所見適用、commit、変更要約、作業 report、session state 更新が一連の制御として成立することを検証する realization test。
- apply fork report の収束、未収束、error、変更ファイル再調査、rolling fork の観測結果を同じ report schema と loop 文脈で扱うためのテスト群をまとめている。
- apply fork 用 ACP builder の import 可能性、prompt 内容、structured output schema 参照、変更要約 helper の未追跡 file 扱いも、apply fork report 制御の前提として検証する。

## Read this when
- apply fork の CLI 挙動、終了 code、report 出力、変更要約、commit message、session state 更新に関するテストを確認したいとき。
- apply fork が所見適用後に変更 file を再調査する条件、再調査対象から除外する対象、収束と未収束の判定を確認したいとき。
- apply fork の error report が未 commit 差分を変更要約へ含めるか、調査対象なしの場合に未実行 loop を report しないかを確認したいとき。
- rolling apply fork が前回 apply join 後の変更だけを対象にする挙動を確認したいとき。
- apply fork 関連の ACP builder が packaged layout や src のみの PYTHONPATH で import できるか、prompt が standard と path model を含むかを確認したいとき。

## Do not read this when
- apply fork の実装本体や report rendering の処理を変更したいだけで、テスト期待値や外部挙動を確認する必要がないとき。
- apply fork 以外のサブコマンド、session fork/join 単体、init 単体の挙動を調べたいとき。
- Codex 実行基盤そのもの、ACP builder 共通基盤、path model の一般仕様を調べたいとき。
- 個別 helper の内部アルゴリズムだけを調べたい場合で、CLI report と loop 制御の期待値を読む必要がないとき。

## hash
- f146c691c6ef55554c03b55114d50d8ade4f404c7d89f28876fa7a7e912a04a8

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
- cmoc の共通 runtime 契約を横断的に固定する realization test。root placeholder と worktree 境界、config 変換、CmocError の Markdown 表示、CLI error の stdout 出力、subcommand log、FileAccessMode から sandbox/profile への変換、binary 判定、状態 branch 名の検証など、個別サブコマンドより下の実行前提をまとめて検証する。
- 大きいテストだが、共通 fixture と root 状態の文脈を分散させないため、basic runtime 回帰として凝集させている。

## Read this when
- runtime の基礎契約、root 解決、linked worktree と main worktree の扱い、run/work/repo root の違いを確認または変更する。
- CmocError、CLI 引数解析 error、stdout/stderr の出力先、エラー report の構造、subcommand log の生成条件を変更する。
- config の既定値や不正値検証、FileAccessMode、Codex sandbox/profile の writable roots、追加書き込み許可 path の制御を変更する。
- branch 名から session state を読む処理、session/apply branch 形状の検証、binary 判定、`.cmoc` の ignore 設定、起動 wrapper の call stack 表示に関わる回帰を確認する。

## Do not read this when
- 個別サブコマンド固有の業務ロジック、画面文言、入出力 schema の詳細だけを調べたい。
- oracle 正本仕様そのもの、仕様文書の編集方針、INDEX.md 生成規則を確認したい。
- 単一 helper の内部実装だけを追えば足り、runtime 境界や CLI 実行前提との結合を確認する必要がない。

## hash
- d600545ccdb76d3e9db394206cd0b8862217b6f555483f16a739288fa30c1ade

# `test_cli_init_tui.py`

## Summary
- 初期化処理と対話起動前の CLI 前処理について、利用開始直後の外部挙動をまとめて検証する realization test。
- 初期化時の .cmoc ignore 設定、既存の staged/unstaged 差分保護、既存 .cmoc 追跡解除、既定設定生成と既存設定への defaults 同期、サブコマンドログ記録を扱う。
- 通常 repository と linked worktree の両方で、初期化成果物・ログ・schema・complete prompt の保存先、worktree 側の ignore 設定、TUI 起動用 parameter 構築を検証する。
- Markdown prompt 編集結果からコメントを除去し、resolve parameter の結果を TUI 起動用の AgentCallParameter と complete prompt に反映する境界を確認する。

## Read this when
- 初期化コマンドの外部挙動、特に .cmoc を git 管理から外す処理、ignore 設定、初期 commit、既存ユーザー差分の保護を変更・調査する時。
- 設定ファイルの初期生成、既存設定を壊さない defaults 同期、codex model や reasoning effort などの初期値に関わる挙動を確認する時。
- 対話起動前の editor 起動、Markdown prompt の整形、parameter resolve、TUI 用 AgentCallParameter の構築、structured output schema 指定を変更する時。
- linked worktree 上で初期化または対話起動した場合の root/cwd、ログ保存先、schema 保存先、.cmoc ignore の扱いを確認する時。
- サブコマンド実行ログの event、command、argv や、旧ログディレクトリを使わないことを検証する必要がある時。

## Do not read this when
- 個別のサブコマンド実装や CLI option の網羅的な仕様を知りたいだけで、初期化または対話起動前処理の外部挙動に関係しない時。
- Codex CLI や editor コマンドそのものの実行品質、LLM 出力内容の品質を検証したい時。
- prompt builder、parameter resolver、runtime preflight などの内部ロジック単体を詳しく追う時は、対応する実装やより局所的なテストを先に読む。
- 通常 repository と linked worktree にまたがる .cmoc 状態配置、ログ配置、ignore 設定の境界に関係しない単純な helper の変更だけを扱う時。

## hash
- cb8700def91815f6c11e29f3f43dbb2adedcc09c99902c9ced35b3ccb657b85b

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 呼び出し runtime の realization test。exec/TUI 起動時の subprocess 制御、profile 生成、sandbox と cwd の選択、schema 保存先、追加 read path 検証、失敗時エラー報告、Codex CLI 不在時の扱いを、スタブ実行ファイルと一時 repo で検証する。
- 実際の Codex CLI や LLM 品質ではなく、cmoc 側が Codex subprocess へ渡す argv・cwd・環境・profile・出力回収・ログ/状態配置を正しく制御しているかを確認する入口。

## Read this when
- Codex exec/TUI 呼び出しの argv、cwd、stdin、output-last-message、profile、CODEX_HOME、PATH、subprocess 起動方法を変更する。
- file access mode ごとの sandbox 設定、PURE_ORACLE_READ の oracle cwd/read-only 化、REPO_WRITE の writable_roots、linked worktree 上での writable root や schema 保存先を確認・変更する。
- apply process tracking、process group、継承環境変数の遮断、Codex CLI subprocess の起動失敗・非ゼロ終了・CLI 不在時の CmocError 表示を扱う。
- TUI 呼び出し前の extra_read_paths 検証、complete prompt の許可条件、codex call log に残す profile/argv 情報に関するテストを探す。

## Do not read this when
- Codex runtime 以外の CLI サブコマンド、設定ロード一般、path model、git worktree 管理そのものの仕様や実装を調べたいだけの場合。
- LLM の応答内容、Codex CLI 本体の機能、プロンプト品質、モデル選択の妥当性を検証したい場合。
- 単体 helper の細かな実装だけを確認したい場合で、呼び出し側の外部挙動や subprocess 境界を確認する必要がない場合。

## hash
- bee0aa4ffcbc5fb766ca6f15dc5e2fbebf5b7d877e76243888e18b4bb790029f

# `test_codex_runtime_home.py`

## Summary
- Codex CLI 実行時に使う Codex home の決定・検証に関する realization test。環境変数が未設定の場合の既定値、相対パス指定時の基準ディレクトリ、実行前検証で発生するエラー内容、実行結果や call log に記録される Codex home を確認する。
- Codex CLI 本体の品質や応答内容ではなく、run_codex_exec が Codex CLI を呼び出す前後で CODEX_HOME、profile 配置先、認証ファイル存在確認をどう扱うかを検証する入口になる。

## Read this when
- run_codex_exec の CODEX_HOME 解決、既定の Codex home、相対 Codex home、Codex home 配下への profile 作成に関する挙動を確認・変更する時。
- Codex home が存在しない、ディレクトリではない、auth.json がない場合に、Codex CLI 起動前にどの CmocError を返すべきかを確認する時。
- Codex CLI 呼び出し環境に渡す CODEX_HOME と、実行結果や call log に保存される解決済み Codex home の関係を確認する時。
- file access mode によって Codex CLI の cwd が変わる場合でも、相対 CODEX_HOME がその cwd 基準で検証されることを確認する時。

## Do not read this when
- Codex home とは無関係な run_codex_exec の一般的な subprocess 実行、出力解析、capacity 待機、モデル・推論設定の引き渡しだけを調べる時。
- CLI や設定全体の仕様、oracle と realization の関係、パスモデルの定義を確認したい時。
- Codex CLI や LLM の実際の出力品質、認証フローそのもの、外部 Codex CLI の実装詳細を検証したい時。
- test helper の実装、fake executable 作成、stub profile 作成の詳細を調べたい時。

## hash
- b92995fbdd0a93c847ae8a31d4ea6534df7c8b4185810379c129ee1b456241d7

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex exec が quota exceeded で失敗した後の待機、availability probe、resume token を使った復帰、resume できない場合の再実行を外部挙動として検証する realization test。
- fake Codex 呼び出し列、call log、subcommand log、CODEX_HOME と cwd、並列実行時の代表 probe 共有を同じ retry 状態機械の観測点として扱う。
- 16,000 文字を超えるが、quota 待機から復帰する Codex exec の制御に責務が閉じており、同じ fake 呼び出し列を追う文脈を一箇所に保つ意図が docstring に明示されている。

## Read this when
- Codex exec の quota exceeded 検出後に、probe が成功したら元の prompt を resume または再実行する挙動を確認・変更する場合。
- quota availability probe の prompt、profile、JSON 出力、call log、subcommand log、console 出力、戻り値の関係を検証したい場合。
- resume token が得られる場合と得られない場合の retry 経路、または probe の非 quota 失敗時の即時失敗を扱う場合。
- 相対 CODEX_HOME が Codex 実行 cwd と組み合わされる挙動、特に oracle 読み取りモードの cwd を確認する場合。
- 複数の quota 待機中 Codex 呼び出しで代表 probe を 1 回だけ実行し、成功時は待機呼び出しが復帰し、失敗時は全待機呼び出しが失敗する制御を扱う場合。

## Do not read this when
- quota retry に関係しない通常の Codex exec 成功・失敗、CLI 引数構築、または出力 JSON 解析だけを確認したい場合。
- Codex CLI や LLM の応答品質そのものを検証したい場合。ここでは fake Codex による外部プロセス制御とログ副作用だけを扱う。
- INDEX 生成、oracle 文書、path model など、quota 待機後の Codex exec 復帰制御と無関係な領域を調べる場合。

## hash
- 0a30f0b70db0ab7bf8389f4f98b8e15ac849abe651f620a206f7d85d4c7fec75

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 実行ラッパーの retry 制御を検証する realization test。構造化出力の schema 不一致、出力ファイル欠落・空・不正 JSON、容量エラー JSONL に対して再試行し、成功時の結果・呼び出しログ・イベント状態が期待どおり記録されることを確認する。
- stderr や通常 stdout に出た容量・quota 風メッセージを retry 判定に使わず、Codex CLI 失敗として扱う境界も検証する。

## Read this when
- Codex CLI 呼び出しの再試行条件、schema validation retry、capacity retry、quota/capacity marker の解釈境界を変更する。
- 呼び出しごとの call log、prompt log、stdout log、subcommand logger の codex_call event に含める status・returncode・error・call_log_path の期待値を確認したい。
- 構造化出力の読み取り失敗や JSON Schema 検証失敗から成功に回復する挙動をテストで確認・修正したい。

## Do not read this when
- Codex CLI に渡す引数構築、profile 設定、sandbox 設定など、再試行後のログ・出力検証に関係しない通常呼び出し経路だけを調べたい。
- repository 作成、Codex home 設定、fake executable 作成などの test fixture 自体の実装を調べたい場合は、support 側の helper を直接読む。
- INDEX 生成、oracle/realization の分類、またはルーティング文書の仕様を調べたいだけで、Codex runtime の retry 挙動を扱わない。

## hash
- 4756b71f801ab3d2753b1ac5ab73749a3bb338f0e6f7a177a3daa1c7451cab3b

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
- Codex 呼び出し前に索引更新を走らせる preflight 制御の realization test。exec/TUI 経由の実行順、更新後コミット、作業ツリー選択、リポジトリロック待機、特定 purpose での索引更新スキップを検証する。

## Read this when
- Codex 実行ラッパーが索引更新を先に行うか、更新後に専用コミットを作って作業ツリーを clean に戻すかを確認・変更したいとき。
- root と cwd が異なる場合に、どの worktree を索引更新対象にするかを確認・変更したいとき。
- 索引更新の排他ロック取得待ち、または索引エントリー生成・衝突解決の purpose で preflight をスキップする条件を扱うとき。

## Do not read this when
- 索引本文の生成内容、ディレクトリ走査、エントリー構造化出力そのものを確認したいだけのとき。
- Codex 実行パラメータの定義や runtime 実行関数の通常動作だけを調べたいとき。
- Git worktree やロックを伴わない一般的なテスト補助関数だけを探しているとき。

## hash
- 5549e75d6493464e59f5f4cb68232c1fbd9fc7d03b85ee5f6cb6ea3ad4e04099

# `test_prompt_parts.py`

## Summary
- prompt 構築系の回帰テストを横断的に扱う realization test。標準 prompt 部品、routing rule、file access rule、complete prompt への標準文書注入、root token と placeholder の保持、ACP builder parameter の model/reasoning/file access mode/schema path/prompt 内容を検証する。
- prompt part と ACP builder の生成結果が同じ最終 prompt 文脈で結合されるため、共通の render 期待値、structured output schema 期待値、oracle 側 schema との一致、packaged layout からの import 可否を一箇所で確認する入口になる。
- 16,000 文字を超えるテストだが、agent prompt と structured output schema の構築結果をまとめて検証する凝集性を優先していることが冒頭 docstring で明示されている。

## Read this when
- prompt builder の標準文書、routing rule、file access rule、realization/review/apply/index entry standard が最終 prompt にどう描画・注入されるかを確認したいとき。
- ACP builder が返す parameter の model class、reasoning effort、file access mode、structured output schema path、prompt 内の標準文書や動的テキスト保持を変更・検証するとき。
- oracle 配下の JSON schema と realization 側 builder の schema path・schema 内容が一致しているかを確認したいとき。
- root token、work root placeholder、oracle-root placeholder、動的 prompt 中のリテラル文字列の置換・非置換境界を変更する前後に回帰観点を確認したいとき。
- review oracle の enumerate/merge/validate、apply fork の finding application/file finding enumeration/change summary、session join conflict resolution、TUI resolve parameter、indexing index entry の builder 挙動を横断的に確認したいとき。

## Do not read this when
- 個別の prompt 文言や標準文書の正本仕様そのものを確認したいだけなら、対応する oracle 側の prompt builder part や schema を直接読む。
- 実装本体の内部アルゴリズムや helper 分割を理解したいだけなら、対象 builder や prompt rendering 実装を直接読む。
- 単一の小さな unit test の期待値だけを探していて、prompt/schema/root placeholder の横断的な回帰観点が不要なとき。
- INDEX.md エントリー生成規則や routing 文書そのものを確認したい場合は、このテストではなく index entry standard や routing rule の本文を読む。

## hash
- 7a274f9bb1e5ce91654cd57a0bb4cc564bcd391387429035068d39a3228f7837

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
- session の fork、join、abandon に関する CLI 外部挙動をまとめて検証する realization test。session branch と session state のライフサイクルを中心に、状態ファイル生成・更新、home branch への復帰、session branch 削除、linked worktree 上での挙動、dirty worktree 拒否、cleanup 失敗時の rollback、join conflict 解決時の Codex 呼び出し条件、stdout/stderr のエラー出力境界を扱う。
- 16,000 文字を超えるが、fork、join、abandon、linked worktree、state cleanup、dirty worktree 拒否が同じ branch/state fixture と状態遷移の観測点に閉じているため、session CLI 回帰として一箇所にまとまっている。

## Read this when
- session fork が session branch と session state をどのように作るか、session-id 衝突や壊れた state file をどう拒否するかを確認したいとき。
- session abandon が home branch へ戻り、session branch を削除し、state を abandoned にする挙動や、home branch 不在・cleanup 失敗時の失敗処理を確認したいとき。
- session join が home branch へ変更を取り込み、state を joined にし、session branch 削除可否を出力へ反映する挙動を確認したいとき。
- session 操作を linked worktree から実行した場合に、root worktree ではなく実行中 worktree の branch/head/state を基準にする外部挙動を確認したいとき。
- join conflict 解決で oracle 配下の衝突ファイルだけを REALIZATION_WRITE profile の追加 writable path として Codex に渡す制御を確認したいとき。
- session CLI のエラー報告が、想定内の CmocError では stdout、merge 後の想定外エラーでは stderr に出る境界を確認したいとき。

## Do not read this when
- session 以外のサブコマンド、設定読み込み、prompt 構築、ログ出力一般のテストを探しているとき。
- fork、join、abandon の内部 helper 実装や状態 schema の定義そのものを確認したいとき。対応する implementation や状態モデルの本文を読む方が直接的。
- Codex CLI や LLM の出力品質そのもの、または conflict 解決内容の妥当性を検証したいとき。この対象は Codex 呼び出し条件と解決後の外部状態を検証する。
- 単純な git helper、repository fixture、Typer runner などテスト基盤の使い方だけを確認したいとき。共通 fixture 側を読む方が直接的。

## hash
- e0a237c3c2ea7a5280d26c2e314e2cece061625b8a601a038ca7b70b6836bab4
