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
- active apply run を `apply abandon` で破棄する外部挙動を CLI 経由で検証する realization test。apply worktree と apply branch の cleanup、session state の ready 復帰、cleanup 対象欠落時の警告、apply worktree や linked worktree から実行した場合の基準位置を扱う。
- running apply process の停止制御も同じ abandon 境界として検証する。親 process と記録済み Codex child process group の停止順、pid file の読み取り、tracking lock 待ち、終了済み process や PID reuse への扱い、process identity 欠落時の拒否を含む。
- 16,000 文字を超えるが、active apply run 破棄に関する worktree/branch/state cleanup、実行位置判定、running process 停止が同じ state fixture と境界条件を共有するため、一箇所に集約されている。

## Read this when
- `apply abandon` の CLI 成功時に、apply worktree・apply branch・session state がどう cleanup されるかを確認または変更する。
- cleanup 対象の worktree や branch が既に消えている場合の警告出力と成功扱いを確認または変更する。
- running 状態の apply run を abandon するときの process identity 読み取り、pid file lock、親 process と child process group の停止順、stale PID 判定を確認または変更する。
- apply worktree 内、linked session worktree、linked apply worktree、古い apply branch から `apply abandon` を実行した場合の拒否条件や cleanup 基準位置を確認または変更する。

## Do not read this when
- `apply fork` の生成挙動、Codex 実行結果の解釈、findings の扱いそのものを調べたいだけの場合。
- apply 以外の session 操作や git worktree 一般の helper 挙動を調べたいだけの場合。
- CLI を介さない低レベルの path model、oracle/realization 分類、INDEX.md 生成規則を調べたい場合。
- active apply run の破棄ではなく、通常の apply 実行開始・完了・結果反映の仕様や実装を調べたい場合。

## hash
- 12764ad325865ffd605e635e39d7d43cff447f02ca3a0f9c3913d1d9eb84a9fb

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
- apply fork の CLI 経由テスト群。所見列挙から適用、commit、変更要約、作業レポート生成、session state 更新までの制御を、収束・未収束・error・変更ファイル再調査・rolling apply fork の観測結果としてまとめて検証する。
- apply fork 向け ACP builder の import 可能性、標準 prompt の組み立て、file finding enumeration schema の参照先、相対 target 拒否も同じ文脈で確認する。
- 未追跡ファイルを含む fork 以降の差分抽出、fallback 変更要約、report path の stdout 抽出など、report 生成と再検査制御を支える補助挙動も扱う。

## Read this when
- apply fork の CLI 実行結果、exit code、作業レポート本文、変更要約、commit message、または session state 更新の期待値を確認・変更したいとき。
- apply fork が所見適用後に変更ファイルを再調査する条件、再調査対象から除外する対象、上限到達時の収束・未収束判定を確認したいとき。
- apply fork の error report が未 commit 差分を変更要約に含めるか、未追跡ファイルが report 用差分に含まれるかを確認したいとき。
- rolling apply fork が前回 apply join 後の oracle 側変更だけを対象にする制御や、last joined apply snapshot の扱いを確認したいとき。
- apply fork 用 prompt builder、structured output schema path、packaged layout での import、標準 prompt 断片の含有条件を変更するとき。

## Do not read this when
- apply fork 以外の CLI サブコマンドの通常動作や、session fork/join 自体の独立した仕様だけを調べたいとき。
- 作業レポートのレンダリング実装、差分抽出 helper、target 列挙実装、ACP builder 実装の詳細を直接修正する必要があるときは、対応する実装側を先に読む。
- Codex 実行基盤そのもの、runner fixture、テスト用 repository 生成 helper の詳細を調べたいだけのとき。
- INDEX.md 生成規則やルーティング文書の形式そのものを確認したいとき。

## hash
- c0c79aea781844edf0ff4e7c7b2999e17a91f19ff92c32dccf08e4fd8f65d11e

# `test_apply_join_cli.py`

## Summary
- apply run を session へ join する CLI 外部挙動を検証する realization test。正常 join、apply worktree からの実行、linked session worktree への反映、cleanup、state 更新、report 生成を扱う。
- join 可否の境界条件として、stale apply branch、dirty apply worktree、想定外差分、削除・rename を含む managed branch path 判定、root memo の分類、gitignore 変更、merge conflict の報告と index conflict 解決後の継続を一箇所で確認する。
- 16,000 文字を超えるが、apply join の成功条件と拒否条件が同じ fixture、session state、git worktree/branch 状態の文脈に強く結合しているため、分割せず外部挙動のまとまりとして読む対象である。

## Read this when
- apply join の CLI 挙動、終了コード、標準出力、report 生成、state 更新、apply worktree と apply branch の cleanup を変更・確認したいとき。
- apply join が dirty worktree、stale apply branch、想定外差分、merge conflict をどの条件で拒否し、何を残すべきかを確認したいとき。
- apply join が session worktree、apply worktree、linked session worktree のどの作業ツリーへ反映し、current cwd によって cleanup 可否がどう変わるかを確認したいとき。
- apply join の managed branch path 分類、memo 配下の扱い、gitignore 変更の許可、削除 path や rename target の扱いを変更する前に既存の期待挙動を確認したいとき。

## Do not read this when
- apply fork の Codex 実行内容や apply run の生成処理そのものを調べたいだけのとき。
- session fork、init、基本的な repository setup の仕様や実装を調べたいだけのとき。
- apply join の内部 helper 実装だけを局所的に変更し、CLI から観測される join 成功・拒否条件や git/state/report 副作用を確認する必要がないとき。
- oracle file の正本仕様を確認したいとき。この対象は realization test であり、正本仕様そのものではない。

## hash
- 4d09bd57be56809c77766c5a899573b645e7d033020eed65c0071cd990cbd42a

# `test_basic_runtime.py`

## Summary
- cmoc の共通 runtime 契約を横断的に固定する realization test。root placeholder と worktree 境界、config 既定値と検証、CmocError の Markdown 表示、CLI error の stdout 化、subcommand log、`.cmoc` ignore、FileAccessMode から sandbox/profile への変換、binary 判定など、個別サブコマンドより下位の実行前提をまとめて検証する。
- 16,000 文字を超えるが、共通 fixture と root 状態の読み取り文脈を分散させないため、基礎 runtime 回帰として一箇所に保持する意図が docstring で明示されている。

## Read this when
- cmoc の runtime 共通契約や基礎的な実行前提を変更・確認する。
- root 解決、run/work root、linked worktree、managed worktree の作成・削除条件に関する回帰を確認する。
- CmocError、CLI 引数解析 error、preflight 失敗、shell completion probe、起動 wrapper の error report 表示を変更する。
- config の既定値・型検証、FileAccessMode の永続化値、sandbox mode、Codex profile の writable roots を変更する。
- subcommand log の生成条件、`.cmoc` の `.gitignore` 追記、binary 判定の読み取り範囲を変更する。

## Do not read this when
- 個別サブコマンド固有の業務フロー、入出力 schema、状態遷移だけを確認したい場合。
- oracle 正本仕様やドキュメント本文の意味内容を確認したい場合。
- 特定の実装 helper の内部アルゴリズムだけを調べれば足り、runtime 境界の外部挙動や CLI 表示に触れない場合。
- Codex CLI や LLM の出力品質そのものを検証したい場合。

## hash
- 7bb27055255701b2b21c39e7c4cd4cf8d861a2502c57e9e4f3e77baa3d5801fb

# `test_cli_init_tui.py`

## Summary
- init 実行と TUI 起動直前の CLI 境界で発生する外部挙動を検証する realization test。`.cmoc` の ignore 化、既存 staged/unstaged 差分の保護、初期設定 JSON の作成・同期、linked worktree での repository/runtime 準備、Markdown prompt の整形、TUI 用 Codex parameter 構築とログ保存先を扱う。
- 16,000 文字を超えるが、初期化済み状態を前提に共有される init/TUI 前処理回帰を一箇所で確認するためのテスト群であり、CLI 利用開始直後の repository/runtime 準備の挙動をまとめて見る入口になる。

## Read this when
- init が `.cmoc` 配下を git 管理から外し、ignore 設定を追加し、必要な cleanup commit を作る挙動を確認・変更する時。
- init が利用者の既存 staged 変更や `.gitignore` の staged/unstaged 変更を commit に巻き込まないことを確認する時。
- default config の内容、既存 config への default key 同期、人間が書いた値を上書きしない挙動を変更・確認する時。
- linked worktree 上で init または TUI を実行した時の root/cwd、ignore 設定、config/log/schema の保存先、git status の扱いを確認する時。
- TUI 起動前に editor で作成された Markdown prompt から HTML comment を除去し、complete prompt を保存し、resolve parameter と launch parameter を組み立てる流れを確認する時。
- TUI の resolved file access mode が空文字の場合に readonly default へ戻る挙動や、launch 用 structured output schema の選択を確認する時。
- sub command log に呼び出された CLI command と argv が記録される挙動を確認する時。

## Do not read this when
- CLI command の実装本体や helper の内部設計を調べたい時は、対応する実装側を直接読む方がよい。
- init/TUI 以外のサブコマンドの外部挙動やテストを探している時は、対象サブコマンドのテストへ進む方がよい。
- Codex 実行 wrapper、preflight、AgentCallParameter などの共通部品単体の仕様を確認したい時は、その部品の実装・専用テストを読む方がよい。
- INDEX.md 生成、oracle/realization の概念、またはルーティング文書そのものの仕様を確認したい時は、このテストではなく該当する正本仕様や専用テストを読む方がよい。

## hash
- 22b776e499758bb0e3492591d94fbbd0f540373a274df1e4d5598ef4e939fd36

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 呼び出し runtime の realization test。exec/TUI 起動時の profile 生成、sandbox 設定、cwd 選択、schema 状態保存先、プロセスグループ追跡、適用追跡環境変数の遮断、許可外 read path の事前拒否、非ゼロ終了と CLI 未検出時のエラー報告を検証する。
- 実物の Codex CLI ではなく一時的な stub 実行ファイルと一時 repo/worktree を使い、外部プロセス起動時の argv、cwd、stdin、生成 profile、ログ、副作用を観測するテスト群である。

## Read this when
- Codex CLI の exec/TUI 起動処理、subprocess 呼び出し、profile 生成、sandbox mode、writable roots、cwd 決定、prompt stdin、output schema 引数、call log の挙動を変更する時。
- PURE_ORACLE_READ、REPO_WRITE、readonly などの file access mode が Codex runtime の作業ディレクトリ・許可領域・extra read path 検証へ与える影響を確認したい時。
- Codex 呼び出し時のプロセスグループ分離、apply process tracking、継承された追跡用環境変数の扱いを調べる時。
- Codex CLI が非ゼロ終了した場合や見つからない場合の CmocError、コンソール出力、呼び出しログの期待値を確認する時。
- linked worktree 上での exec/TUI 呼び出しや、schema 状態を worktree 側へ保存する挙動を変更・検証する時。

## Do not read this when
- Codex runtime 以外の CLI command、設定読み込み一般、path model、oracle 文書生成などの挙動を調べるだけの時。
- 実際の Codex CLI や LLM の応答品質、モデル選択、プロンプト内容そのものを検証したい時。
- Git 操作、repo fixture、stub 実行ファイル作成などのテスト支援 helper の実装詳細を調べたい時は、支援 helper 側を直接読む方がよい。
- sandbox や file access mode の正本仕様を確認したい時は、テストではなく対応する oracle file を読む方がよい。

## hash
- 71cef4cdeb2245fe5ada7e2eae0306d1f9fcb77ab7b19c96d6a17529a9c463c7

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
- Codex exec が quota exceeded になった後の待機、availability probe、resume token 利用、resume 不能時の再実行、失敗伝播を外部挙動として検証する realization test。
- fake Codex CLI と subprocess stub を使い、呼び出し順、標準入力、CODEX_HOME/cwd、call log、subcommand log、console 出力を同じ quota retry 状態機械の観測点として扱う。
- 並列に quota 待ちになった複数呼び出しで representative probe が 1 回だけ実行され、成功時は各呼び出しが resume し、probe 失敗時は待機中呼び出しも CmocError になることを検証する。

## Read this when
- Codex exec の quota exceeded 検出後に、probe 待機、resume、resume token 不在時の再実行、または retry 上限まわりの挙動を変更する。
- quota availability probe の prompt 生成、実行引数、profile、CODEX_HOME、cwd、または PURE_ORACLE_READ 時の作業ディレクトリ扱いを確認する。
- Codex call log、stdout/stderr/prompt/output log、subcommand log、console 表示に quota retry 中の呼び出しがどう記録されるかを確認する。
- 複数の Codex exec が同時に quota exceeded になった場合の probe 共有、代表 probe 失敗時のエラー伝播、並列 retry 制御を変更・検証する。

## Do not read this when
- quota exceeded 後の Codex exec retry 状態機械と無関係な通常の Codex exec 成功・失敗だけを確認したい。
- cmoc の CLI 引数、設定読み込み、リポジトリ生成 fixture など、quota retry の観測点ではない個別機能を調べたい。
- Codex CLI や LLM の出力品質そのもの、または実際の外部 Codex サービスの可用性を検証したい。
- oracle file の正本仕様を確認したい場合。この対象は realization test であり、正本仕様ではない。

## hash
- 99c3c73f72875b3a6aee51af659c453f9ea1dd410c2a3e77f89f4d0d0086dbb5

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
- indexing preflight と indexing サブコマンドが routing document を生成・更新・commit する外部挙動を検証する realization test。未初期化・dirty worktree・linked worktree・apply worktree の config 利用、fresh hash による Codex 呼び出し省略、INDEX.md conflict 解決、entry schema 検証、空ディレクトリ・memo 除外・symlink cycle・並列生成などを同じ indexing 更新ワークフローの回帰として扱う。

## Read this when
- indexing CLI の preflight 条件、commit 対象、linked worktree 上での更新先、または git dirty 状態での拒否挙動を変更・確認するとき。
- routing document の entry 生成、既存 hash 再利用、壊れた entry の再生成、entry schema の拒否条件、空ディレクトリへの INDEX.md 配置を変更・確認するとき。
- INDEX.md conflict 解決、root memo 除外と nested memo indexing、ディレクトリ symlink cycle の除外、兄弟 entry の並列生成に関する回帰を確認するとき。

## Do not read this when
- indexing の正本仕様断片そのものを確認したいとき。まず oracle 側の indexing 仕様を読む。
- routing document 以外のサブコマンドの CLI 境界、または apply/join の conflict 解決全般を調べたいだけのとき。より直接の実装または対象テストを読む。
- Codex CLI や LLM 出力の品質そのもの、あるいは実際の INDEX.md 本文の内容を評価したいとき。このテストは生成器の外部制御と schema 境界を検証する。

## hash
- f20a2be1e1c46de724ba0e71ec3f8f4d18cb6143d46ac1054d45133dd171ffaf

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
- prompt 構築部品と ACP builder の出力を横断的に検証する realization test。routing rule、file access rule、各 standard 文書、complete prompt への組み込み、root token の保持・置換、structured output schema の参照先と内容、builder の model/reasoning/file access mode をまとめて確認する。
- 16,000 文字を超えるが、標準 prompt、routing、file access、builder parameter が最終 prompt の同じ読み取り文脈で組み合わさるため、共通の render/schema 期待値を一箇所で追う構成になっている。

## Read this when
- prompt_builder の各 standard/rule が期待する語句を markdown rendering に含むか確認・変更したいとき。
- complete prompt が routing rule や optional standard を含む条件、root token・work root placeholder・dynamic prompt の保持挙動を検証したいとき。
- apply fork、indexing、review oracle、session join、TUI resolve parameter などの ACP builder が返す model class、reasoning effort、file access mode、prompt 内容、schema path を変更・確認するとき。
- oracle 側 JSON schema と realization 側 builder が参照する structured output schema の一致、または schema validation 用の最小例を確認したいとき。
- prompt 構築回帰テストを分割するかどうか判断する際に、責務境界と凝集性の説明を確認したいとき。

## Do not read this when
- 個別 builder の実装詳細や prompt 生成ロジックそのものを修正する場合は、対応する実装モジュールを先に読む。
- 特定の JSON schema の正本内容だけを確認する場合は、oracle 配下の該当 schema 本文を直接読む。
- StructDoc や markdown renderer の内部実装を理解したいだけなら、構造化文書と rendering の実装を読む。
- CLI の実行フローやユーザー向けコマンド挙動を調べる作業では、対象コマンドの実装・テストへ進む。

## hash
- 9144dceef520ef4ad2cd20ee4195c520c49f53debe5d99a1413575a059bd9b48

# `test_review_oracle_cli.py`

## Summary
- review oracle の CLI 経由の外部挙動と、所見列挙・検証・judge・merge の制御を検証する realization test。report の構成、accepted/rejected 所見の表示、scope 切替、review worktree と join commit、INDEX.md 変更の merge、異常時 report、review 実行中に許されない差分の拒否を扱う。
- 16,000 文字を超えるが、同じ fake Codex 応答、report 文脈、review run 状態を共有する一連の検証として凝集しており、oracle review の読み取り文脈を一箇所に保つためのテストファイル。

## Read this when
- review oracle コマンドの report 出力、result 判定、section 順序、count、error report の期待値を確認または変更したいとき。
- review oracle の所見 loop で、enumerate finding、challenger/advocate validation、judge、merge finding の呼び出し条件や prompt へ渡る文脈を確認したいとき。
- review oracle の full scope/session scope における oracle 対象選択、gitignored oracle file、binary、memo 配下や symlink の扱いを検証したいとき。
- linked worktree 上の session branch、review 用 worktree、review_fork_commit、review_join_commit、INDEX.md 変更の取り込みや conflict 解決の挙動を確認したいとき。
- review oracle 実行中に生成された INDEX.md 以外の unstaged/staged/untracked 差分を拒否し、元 worktree を汚さない制御を確認したいとき。

## Do not read this when
- review oracle 以外の review コマンド、通常の session 操作、init などの CLI 挙動だけを調べたいとき。
- report renderer や review loop の実装詳細を変更する目的で、まず実装本体を直接読むべき段階のとき。
- oracle file の正本仕様そのもの、oracle doc/src/test の内容、または INDEX.md エントリー生成規則を確認したいとき。
- 単純な path model、設定読み込み、git helper、test fixture の一般的な使い方だけを確認したいとき。

## hash
- e338918275b95bd682d96da75bdc34736fe3d986aa43e595414fb4b428d58ff9

# `test_session_cli.py`

## Summary
- session の fork、join、abandon に関する CLI 外部挙動を横断的に検証する realization test。session branch と session state のライフサイクルを中心に、状態ファイル作成・更新、home branch への復帰、session branch 削除、linked worktree 上の挙動、dirty worktree 拒否、エラー出力先、cleanup 失敗時の rollback を扱う。
- session join の競合解決について、oracle file 衝突時に realization write profile と対象ファイル限定の書き込み権限が使われること、競合 marker 検出、削除競合の stage、session branch 削除不能時の警告を検証する。

## Read this when
- session fork が session branch と session state をどう作るか、session-id 衝突時に既存 state を上書きしないこと、衝突 retry、壊れた state の拒否を確認したいとき。
- session abandon が home branch へ戻り session branch を削除して state を abandoned にする挙動、home branch 不在時の失敗、cleanup 失敗時の state と branch の rollback を確認したいとき。
- session join が session branch の変更を home branch に統合し state を joined にする挙動、linked worktree で root 側 branch を変えない挙動、session branch 削除の成功・失敗境界を確認したいとき。
- session join の競合解決で Codex 呼び出しに渡す file access mode、extra writable paths、oracle conflict write 許可、競合 marker 残存時の失敗扱いを確認したいとき。
- session CLI のエラー報告が stdout と stderr のどちらへ出るべきか、利用者向け完了レポートに何が残るべきかを検証したいとき。

## Do not read this when
- session 以外のサブコマンド、設定読み込み、path model、ログ基盤そのものの実装詳細を調べたいだけのとき。
- fork、join、abandon の内部 helper の細かな実装方針や git wrapper の一般挙動を調べたいときは、該当する実装側を先に読む。
- oracle file の正本仕様や仕様文言を確認したいときは、テストではなく oracle 側の本文を読む。
- 単体 helper の小さな入力変換だけを確認したいときは、この統合的な CLI 回帰テストより、対象 helper に直接対応するテストがあればそちらを読む。

## hash
- ca133ab73b65c550d66a92536fdad58bfcf7a0fe9adae35a9e1967e7ed989d67
