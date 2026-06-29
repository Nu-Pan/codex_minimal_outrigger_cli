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
- active apply run を破棄する CLI 挙動の realization test。apply abandon が apply worktree、apply branch、session state、process identity を cleanup する成功経路と、警告・拒否条件を検証する。
- completed/running apply run の破棄、linked session worktree からの実行、apply worktree 内からの実行、stale apply branch の拒否など、実行位置と state の整合性をまたぐ外部挙動を一箇所で扱う。
- running apply process 停止では、記録済み child process group を親 process より先に止める順序、PID reuse 回避、終了済み process や zombie leader を cleanup 失敗にしない境界を固定する。

## Read this when
- apply abandon の CLI 出力、終了コード、worktree/branch/state cleanup の期待挙動を確認・変更する場合。
- running apply run の abandon で process identity を読み、Codex child process group と親 apply process を停止する制御を変更する場合。
- apply abandon を repo root、apply worktree、linked session worktree、linked apply worktree のどこから実行できるか、またはどこで拒否するかを確認する場合。
- apply branch から worktree を導けない破損 state、running state で process identity が無い state、stale apply branch などの失敗条件を確認する場合。
- cleanup 対象が既に消えている場合を警告つき成功として扱うかどうかを確認する場合。

## Do not read this when
- apply abandon 以外の apply サブコマンドの通常フローや review/fork の詳細挙動だけを調べる場合。
- session fork、repository 初期化、git helper、test runner fixture の一般的な使い方だけを確認したい場合。
- oracle の正本仕様断片や利用者向け仕様そのものを確認したい場合。この対象は realization test であり正本仕様ではない。
- apply process 停止とは無関係な CLI command 登録、引数 parsing、表示 formatting の共通実装だけを変更する場合。

## hash
- c2f183001b4f1991f59d360ec54d8d35aee47c827749d78c3dd13ff8d69d401b

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
- cmoc の共通 runtime 契約を横断して固定する realization test。root placeholder と worktree 境界、config 既定値と検証、CmocError の Markdown 表示、CLI error の stdout 化、subcommand log、`.cmoc` ignore、FileAccessMode から sandbox/profile への変換、binary 判定、session/apply branch state 読み取り境界をまとめて検証する。
- 個別サブコマンド固有の挙動ではなく、実行前提として同時に崩れやすい基礎 runtime の回帰確認を一箇所に集めている。

## Read this when
- root 解決、`<cmoc-root>`/run root/work root、linked worktree、managed worktree path の安全性に関する runtime 挙動を確認・変更する時。
- `CmocConfig`、codex model class、reasoning effort、config 読み込みエラーの扱いを確認・変更する時。
- `CmocError`、CLI 引数解析 error、preflight 失敗、起動 wrapper の error report 表示や stdout/stderr 境界を確認・変更する時。
- subcommand log の作成条件、timestamp 衝突時の log file 名、pre-log check 失敗時の副作用抑制を確認・変更する時。
- FileAccessMode の永続化値、Codex sandbox mode、Codex cwd、profile の writable roots、追加書き込み許可 path の制限を確認・変更する時。
- `.cmoc` の `.gitignore` 追加、binary 判定の読み取り範囲、session/apply branch 名からの state 解決を確認・変更する時。

## Do not read this when
- 特定のサブコマンドの業務ロジック、入出力 schema、個別 workflow の詳細だけを調べたい時は、そのサブコマンドや機能に対応するテストを先に読む。
- oracle 正本仕様断片の内容や文書構成を確認したい時は、oracle 側の本文を読む。
- 単体 helper の内部実装だけを変更し、root/worktree/config/error/profile/log/state などの共通 runtime 契約に影響しないことが明確な時は、該当する実装ファイルまたはより狭いテストを読む。

## hash
- 6f491c918974572010c987f4877164720a9be15f3ff2ac5996a768ca4e5181a0

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
- Codex CLI 実行連携の realization test。exec/TUI 呼び出しで生成される profile、作業ディレクトリ、sandbox 設定、schema 保存先、prompt 入力、呼び出しログ、外部 apply tracking 環境変数の遮断、子プロセスの process group、Codex CLI 不在や非ゼロ終了時のエラー処理を検証する。
- テスト用の擬似 codex 実行ファイルと一時 repository/worktree を使い、runtime が Codex CLI を起動する直前・直後に守るべき制御ロジックと副作用を確認する入口になる。

## Read this when
- Codex CLI の exec または TUI 呼び出し処理、profile 生成、sandbox の read-only/workspace-write 切り替え、PURE_ORACLE_READ 時の oracle 配下への cwd 制限を変更する時。
- Codex 呼び出し時の prompt 入力、output-last-message、output-schema、schema state の保存場所、linked worktree での状態保存や writable_roots を調べる時。
- Codex subprocess の起動 wrapper、apply process tracking、process group、継承環境変数の扱い、Codex CLI 不在・非ゼロ終了のエラー表示や call log 生成を変更する時。
- TUI 呼び出しで extra read path を開始前に検査する制御、complete prompt の許可範囲、保護領域や memo 配下の拒否挙動を確認する時。

## Do not read this when
- Codex CLI 連携ではなく、通常の CLI コマンド引数解析、設定ファイル読み込み一般、または repository/path model の仕様だけを確認したい時。
- runtime の実装詳細ではなく、oracle file の正本仕様断片を確認したい時。
- テスト支援関数そのものの実装、repository fixture 作成、擬似実行ファイル作成、git helper の詳細だけを調べたい時。
- LLM の応答品質や Codex CLI 自体の内部挙動を検証したい時。

## hash
- 074f17b14b4ec18b7d63b6a87f79a26da0706fb4ef0d81ec156bfea4f78b880b

# `test_codex_runtime_home.py`

## Summary
- Codex CLI 実行時の Codex home 解決と事前検証を対象にした realization test。環境変数が未設定の場合の既定 home、環境変数で指定された home の保持、Codex 実行 cwd に対する相対 home の解決、home や認証情報が不正な場合に Codex CLI 起動前に失敗することを検証する。

## Read this when
- Codex CLI 呼び出しで使用する CODEX_HOME の決定、相対パス解決、実行結果へ記録される codex_home や profile_path の挙動を確認・変更するとき。
- Codex home が存在しない、ディレクトリではない、auth.json がない場合の CmocError の summary・detail・next_actions を確認・変更するとき。
- ファイルアクセスモードによって Codex CLI の作業ディレクトリが変わる状況で、相対 CODEX_HOME がどこから解決されるかを検証するとき。

## Do not read this when
- Codex CLI の容量待機、標準出力イベント処理、プロンプト生成など、Codex home の解決や検証に直接関係しない実行制御を調べるとき。
- 実際の Codex CLI や LLM の出力品質を検証したいとき。ここでは fake executable を使い、home 解決と事前検証の制御ロジックだけを扱う。
- oracle file 側の正本仕様を確認・変更したいとき。この対象は realization test であり、正本仕様そのものではない。

## hash
- f113426a3f92145e9b5bff3bfd809dd949834c6dbb9c2471815903cec09de7fe

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex exec が quota exceeded になった後の待機、availability probe、resume token を使った復帰、resume 不能時の再実行を外部挙動として検証する realization test。
- fake Codex subprocess、call log、subcommand log、標準出力、CODEX_HOME と cwd、並列実行時の代表 probe 共有を観測し、quota retry 状態機械の回帰をまとめて扱う。
- 16,000 文字を超えるが、probe 共有、resume、retry、ログ、実行ディレクトリが同じ fake 呼び出し列に強く結び付くため、一つの quota retry 回帰テストとして凝集させている。

## Read this when
- Codex exec の quota exceeded 検出後に、probe を挟んで resume または再実行する制御を変更・調査するとき。
- quota availability probe の生成、成功・非 quota 失敗・quota 継続失敗の扱い、待機中呼び出しへの失敗伝播を確認するとき。
- Codex 呼び出しログ、subcommand log、prompt/stdout/stderr/output の保存内容、console 表示、result の call_log_path を quota retry 文脈で確認するとき。
- CODEX_HOME が相対パスの場合の実行 cwd、`--cd` の向き先、PURE_ORACLE_READ での oracle root 利用を quota probe と合わせて確認するとき。
- 複数の Codex exec が同時に quota exceeded になった場合に、代表 probe を一回だけ実行し、各呼び出しが resume または失敗する挙動を確認するとき。

## Do not read this when
- 通常成功する Codex exec の引数組み立てや出力解析だけを確認したいときは、quota retry ではない runtime 実装または該当する通常系テストを読む。
- quota exceeded と無関係な設定読み込み、repository fixture、Codex profile stub、補助 executable 作成の詳細を調べたいときは、対応する support や config の本文を読む。
- Codex CLI や LLM の出力品質そのものを評価したいときは、このテストは対象外であり、ここでは fake subprocess による制御ロジックだけを検証している。
- oracle file の正本仕様を確認したいときは、この realization test ではなく oracle 配下の該当本文を読む。

## hash
- 5c77e55551c5c963cc706fa674788efc84b6c0edd5d0671ff74dfb818cf64a05

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
- INDEX.md の生成・更新、fresh hash による再生成省略、malformed entry の再生成、commit 対象の限定、conflict 解決、linked worktree と apply worktree 上の indexing preflight など、routing document 更新ワークフローの CLI 境界と制御ロジックをまとめて検証する回帰テスト。
- Codex によるエントリー生成結果の取り込み、schema 不一致や空白・複数行 semantic item の拒否、空ディレクトリや nested memo directory の扱い、兄弟 entry 生成の並列化も同じ indexing 更新責務の観測点として扱う。

## Read this when
- indexing subcommand や indexing preflight の外部挙動、git commit 条件、dirty worktree 拒否、linked worktree での更新先、apply worktree での repo config 利用を変更・確認したいとき。
- INDEX.md entry の生成・再利用・再生成判定、hash freshness、malformed entry 検出、render_index_entry の schema validation、空ディレクトリや memo directory の indexing 対象判定を調べたいとき。
- resolve_index_conflicts が INDEX.md の merge conflict を削除・解消して merge commit を成立させる挙動を変更・確認したいとき。
- indexing 更新処理で Codex 呼び出しをどの条件で行うか、または sibling entry 生成を並列化する制御を変更する前に既存の期待挙動を確認したいとき。

## Do not read this when
- init、apply、join などのサブコマンド全般を調べたいだけで、INDEX.md 更新や indexing preflight の挙動に触れないとき。
- routing document の正本仕様や設計意図を確認したいときは、この回帰テストではなく oracle 配下の該当仕様を読む。
- indexing の内部 helper 実装だけを局所的に確認したい場合は、まず実装側の対象モジュールを読む。
- Codex CLI や LLM 出力品質そのものを検証したい場合は、このテストは対象外であり、ここでは生成結果を fake に差し替えた制御境界だけを扱う。

## hash
- 4eca837d056016a4e977f2ebde1f2e0720c68d1c851239a907fdfa66f8b6ca42

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
- agent prompt と structured output schema の構築結果を横断的に検証する realization test。標準 prompt 部品、routing rule、file access rule、root token の扱い、apply/review/indexing/session/tui 各 ACP builder の parameter と schema 参照が期待どおり組み合わさることを確認する。
- 16,000 文字超の大きなテストファイルだが、最終 prompt の同じ読み取り文脈で共有される render/schema 期待値を一箇所で追うために凝集させている。prompt 構築まわりの回帰確認へ入る入口になる。

## Read this when
- prompt builder の標準部品、complete prompt、routing rule、file access rule、realization/review/apply/index entry standard のレンダリング期待値を確認・変更する。
- apply fork、review oracle、indexing、session join、tui resolve parameter などの ACP builder が返す model class、reasoning effort、file access mode、prompt 内容、structured output schema path を検証したい。
- oracle 側 schema JSON と realization 側 builder の schema 参照が一致しているか、また packaged layout から review oracle builder を import できるかを確認する。
- root token や placeholder が complete prompt 内でどう保持・記録されるべきか、dynamic text 内の literal token が置換されず保持されるべきかを調べる。
- prompt 構築の回帰テストを追加・更新する際に、既存の観点へケース追加できるかを判断する。

## Do not read this when
- 個別 CLI コマンドの実装挙動や通常のアプリケーションロジックを調べたいだけで、prompt/ACP builder/schema 生成に関係しない。
- StructDoc や markdown rendering の実装そのものを変更したい場合で、期待される外部挙動ではなく実装詳細を読む必要がある。
- oracle の正本仕様断片や schema 定義の内容そのものを確認したい場合。対応する oracle 配下の本文や JSON を直接読む方が適切。
- 特定 builder の実装原因を追う段階で、すでに失敗している対象 module が分かっている場合。まずその builder 本体や関連 oracle source を読む方が直接的。

## hash
- f471a714b19ed444cae5d866a464a1dd985d00a3a871a5f655808b45ea8b8a71

# `test_review_oracle_cli.py`

## Summary
- review oracle の CLI 経由の外部挙動と、所見列挙・検証・judge・merge を含む review loop の制御を検証する realization test。
- report の見出し構成、accepted/rejected finding の表示、件数メタデータ、error/no_targets/fatal などの結果表示、session_id 非表示、join commit 表示を確認する。
- full/session scope の oracle file 選択、gitignored oracle file や memo 配下参照 symlink の除外、linked worktree 上の session branch と oracle 対象化、review 用 worktree で生成された INDEX.md の取り込みと衝突解決を扱う。
- 所見 merge operation の kind ごとの契約、invalid operation や target 再利用の拒否、review oracle が INDEX.md 以外の差分を作った場合の拒否と元 worktree 保護も検証する。

## Read this when
- `review oracle` サブコマンドの report 生成、report 本文の構成、結果メタデータ、accepted/rejected finding の表示仕様を変更または確認したいとき。
- oracle review loop の enumerate、validate challenger、validate advocate、judge、merge の呼び出し順・入力文脈・上限回数・所見 ID 管理に関わる実装を変更するとき。
- full scope または session scope で review 対象となる oracle file の列挙条件、gitignore、binary file、symlink、memo との境界、linked worktree 上の挙動を確認するとき。
- review oracle が作成した INDEX.md 変更の取り込み、join commit、INDEX.md 削除との merge conflict 解決、review 用 worktree の配置や後片付けに関わる変更を行うとき。
- review oracle 実行中の失敗時 report、非対象時 report、INDEX.md 以外の差分作成を拒否する挙動を確認するとき。

## Do not read this when
- 通常の session fork、init、git helper、設定 loader など、review oracle の外部挙動や所見 loop と直接関係しない CLI 挙動だけを確認したいとき。
- oracle file の正本仕様そのものを確認したいとき。このファイルは realization test であり、正本仕様の代替ではない。
- review oracle 以外の review サブコマンド、または oracle 以外の対象を review する処理を調べたいとき。
- 個別 helper の実装詳細だけを変更し、report 出力、対象 oracle の選択、所見評価 loop、merge operation 契約、worktree 差分制御の外部挙動に影響しないことが明らかなとき。

## hash
- 833e47b2657a97bcdb8fa4549de0cca8b6c61a15d960d3c8159f2a555fe750f7

# `test_session_cli.py`

## Summary
- session 系 CLI の外部挙動を検証する realization test。fork、join、abandon による session branch と session state のライフサイクル、linked worktree 上の動作、状態ファイル cleanup、dirty worktree 拒否、エラー出力先、conflict resolution の実行条件を同じ session 状態遷移の観測点として扱う。
- 16,000 文字を超えるが、branch/state fixture を共有する session CLI 回帰として一箇所に保つ意図が docstring に明示されている。

## Read this when
- session fork が session branch と state file を作成する挙動、session-id 衝突時の retry・失敗・既存 state 保護を確認したいとき。
- session abandon が home branch へ戻り session branch を削除し state を abandoned にする挙動、home branch 欠落時や cleanup 失敗時の rollback・出力を確認したいとき。
- session join が session branch の変更を home branch へ統合し state を joined にする挙動、branch 削除失敗時の warning、dirty worktree 拒否、エラーの stdout/stderr 振り分けを確認したいとき。
- linked worktree 上で fork・join・abandon が root worktree の branch を不用意に切り替えず、linked 側の branch/head/state を扱うことを確認したいとき。
- oracle conflict resolution で Codex 実行 profile、REALIZATION_WRITE、追加 writable path、conflict marker 検出、削除競合の staging を検証する必要があるとき。

## Do not read this when
- session CLI の正本仕様や利用者向け仕様文を確認したいだけのとき。実装テストではなく oracle doc を読む方が適切。
- session state の schema や読み書き helper の実装だけを変更・確認したいとき。外部 CLI 回帰ではなく該当する実装 module を読む方が直接的。
- session 以外の CLI、設定読み込み、path model、logging の一般挙動を調べたいとき。
- 単体 helper の小さな仕様だけを確認したいとき。ただし conflict marker block 検出の回帰確認はこの対象に含まれる。

## hash
- 1ecdecd6b75a674ab6c06552e333c024c39e17f5722ead997d3d891c0e3498d1
