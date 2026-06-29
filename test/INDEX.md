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
- cmoc の基礎 runtime 契約を横断的に固定する realization test。root 解決、worktree 安全性、設定検証、CmocError の表示、CLI preflight、subcommand log、FileAccessMode と Codex sandbox profile、binary 判定など、個別サブコマンドより下の共通 runtime 境界をまとめて検証する。
- 16,000 文字を超えるが、共通 fixture と root 状態の読み取り文脈を共有する basic runtime 回帰として凝集しており、分割より同時確認の必要性が高いテスト群を収める。

## Read this when
- root placeholder、repo root、run root、work root、linked worktree、managed worktree の扱いを変更・確認するとき。
- CmocError、render_error、CLI parse error、stdout/stderr の error report、preflight 失敗時の副作用抑制を変更・確認するとき。
- config の既定値や codex model / reasoning effort 名の検証、FileAccessMode の永続化値や sandbox mode 変換を変更・確認するとき。
- Codex profile の cwd、writable_roots、memo・.agents・oracle・src・.cmoc log への書き込み許可境界を変更・確認するとき。
- subcommand log の生成条件、timestamp 衝突時の log file 分離、pre-log check 失敗時の log 抑制を変更・確認するとき。
- branch 名から session id を読む処理、apply branch 形状検証、branch に対応する session state 読み込みを変更・確認するとき。
- binary 判定の読み取り範囲、duration 表示、起動 wrapper の call stack path 表示など、共通 runtime helper の外部挙動を変更・確認するとき。

## Do not read this when
- 個別サブコマンド固有の通常フロー、入出力 schema、ユーザー操作単位の詳細挙動だけを確認したいときは、そのサブコマンドのテストへ進む。
- oracle file の正本仕様断片そのものを確認・更新したいときは、対応する oracle 側の文書やコードを読む。
- runtime の外部契約ではなく、特定 helper の内部実装だけを局所的に確認したいときは、該当する実装 module を直接読む。
- UI 表示、生成文書、補助スクリプト、依存関係など、root/config/error/sandbox/profile/state/log 以外の領域を扱うときは読まなくてよい。

## hash
- 6797d132c803a34721b206a43e8e2b7567a7cec0b500834805b677f1c3a0fe28

# `test_cli_init_tui.py`

## Summary
- init と対話起動前処理の外部挙動を検証する realization test。cmoc 管理領域の ignore 化、既存 staged/unstaged 差分の保護、初期設定生成と同期、linked worktree での初期化・ログ保存・schema 配置、Markdown prompt からの TUI parameter 解決と Codex 起動引数構築を扱う。
- 利用開始直後の CLI 境界で共有される repository/runtime 準備を一続きの回帰として確認するための入口であり、初期化済み状態を前提に TUI 起動へ進む挙動まで同じ文脈で読む対象。

## Read this when
- init の外部挙動、特に cmoc 管理領域を git tracking から外す処理、ignore 設定、cleanup commit、サブコマンドログ記録を確認・変更する時。
- init が利用者の既存 staged 変更や unstaged 変更、既存の ignore ファイル変更を壊さないことを確認・変更する時。
- 初期設定ファイルの default 値、既存の人間設定を保持した defaults 同期、設定項目追加時の初期化回帰を確認する時。
- linked worktree 上で init または TUI を実行した時の repository root と worktree cwd の扱い、ignore 設定、ログ保存先、schema 配置、git status の汚れ防止を確認する時。
- TUI 起動前のエディタ実行、HTML comment 除去を含む prompt 整形、parameter 解決用 Codex 呼び出し、file access mode の default、最終 prompt 保存、TUI 用 Codex parameter 構築を確認・変更する時。

## Do not read this when
- 個別サブコマンドの business logic や内部 helper の詳細だけを調べたい時。この対象は init/TUI 起動境界の外部挙動回帰に絞られている。
- Codex CLI や LLM の出力品質そのものを検証したい時。この対象は呼び出し引数・保存先・制御境界を stub で確認する。
- 一般的な test support、repository fixture、fake executable 作成 helper の実装を調べたい時。ここではそれらを利用する側の回帰だけを扱う。
- TUI 実行後の対話 UI 内部挙動を調べたい時。この対象は対話起動前の parameter 構築と起動呼び出しまでを扱う。

## hash
- 52aa8bc9dca127f656fd33da495d4ea1e1e7ffe9c5666c332a30912fc5b3584f

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 実行基盤の realization test。Codex subprocess の起動環境、process group tracking、profile 生成、sandbox 設定、作業ディレクトリ、schema 出力先、TUI 起動前検証、失敗時エラー報告を、stub codex と一時 repo で検証する。
- `run_codex_exec` と `run_codex_tui` が file access mode や linked worktree に応じて、Codex CLI の引数・cwd・profile・ログ・schema path をどう扱うかを確認する入口になる。

## Read this when
- Codex CLI 呼び出し周りの実行制御、profile 生成、sandbox writable roots、read-only / repo-write / pure-oracle-read の切り替えを変更する時。
- `commons.runtime_codex` または `commons.runtime_codex_profile` の subprocess 起動、apply process tracking、`CODEX_HOME` profile、`--cd`、`--output-last-message`、`--output-schema` の扱いを確認する時。
- TUI 実行で extra read path の許可判定、linked worktree からの完全 prompt 読み込み、Codex CLI 非ゼロ終了や CLI 不在時の `CmocError` 報告を変更・調査する時。

## Do not read this when
- Codex CLI 呼び出しではなく、一般的な CLI command parsing、oracle 文書、path model、config schema そのものの仕様を調べる時。
- LLM 出力品質や Codex 本体の振る舞いを検証したい時。この対象は cmoc が Codex CLI をどう起動・制御するかを stub subprocess で検証する。
- runtime 以外の realization test、または pytest helper / fixture の一般構造だけを探す時は、より直接の test support や該当機能のテストへ進む。

## hash
- 1f0890b94acc48a58c6dfd2f451c9ef58a54b01b3e034d5510fb5f236831be09

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
- Codex exec が quota exceeded になった後、quota availability probe を挟んで resume または再実行へ進む retry 状態機械の外部挙動を検証する realization test。
- probe の共有、resume token の利用有無、call log と subcommand log、CODEX_HOME と cwd の扱いを、fake Codex 呼び出し列とログ出力を通じて確認する。
- 並列実行時に代表 probe が 1 回だけ実行されること、代表 probe 失敗時に待機中の呼び出しも失敗して resume しないことを扱う。

## Read this when
- Codex exec の quota exceeded 検出後の待機、probe、resume、再実行の制御を変更・調査する場合。
- quota availability probe の引数、標準入力、出力ファイル、ログ記録、subcommand event の期待値を確認したい場合。
- CODEX_HOME が相対パスのとき、Codex 呼び出し cwd と --cd がどこを指すべきかを確認する場合。
- 複数の Codex exec が同時に quota 待機へ入ったときの probe 共有や、probe 失敗時のエラー伝播を変更・検証する場合。

## Do not read this when
- quota retry と無関係な通常の Codex exec 成功系、プロンプト構築、モデル選択、ファイルアクセスモード全般だけを調べる場合。
- Codex CLI そのものの出力品質や LLM 応答内容を検証したい場合。
- ログ基盤全体の形式や保存先だけを調べる場合で、quota exceeded 後の probe/resume/retry に関係しない場合。
- oracle file や正本仕様断片の内容を確認したい場合。

## hash
- 3fc5e457350652875417908918966047c9e87c2f7592e8078ab436bb3861593c

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
- prompt part と ACP builder の生成結果を横断的に検証する realization test。標準 prompt、routing、file access rule、各種 builder parameter、structured output schema path と schema 内容、root token や placeholder の扱いが期待通りに組み合わさることを確認する。
- prompt 構築まわりの回帰観点を一箇所に集約しており、StructDoc の markdown render、complete prompt の標準文書注入、apply/review/session/indexing/TUI 各 builder の model class・reasoning effort・file access mode・schema 参照を検証する入口になる。

## Read this when
- prompt builder の出力文言、標準文書の注入条件、routing rule や file access rule のレンダリング結果を変更・調査するとき。
- ACP builder が生成する AgentCallParameter の model class、reasoning effort、file access mode、prompt 内容、structured output schema path を確認するとき。
- apply fork、review oracle、session join、indexing、TUI resolve parameter に関する schema 参照や prompt への root 表記・placeholder 展開の回帰を調べるとき。
- StructDoc や StructCodeBlock の markdown rendering、特に連続空行の畳み込みや code block 内空行の扱いを変更するとき。

## Do not read this when
- 個別コマンドの実装挙動そのものを調べたいだけで、prompt 生成や ACP builder parameter の契約に関係しないとき。
- oracle file の正本仕様本文を確認したいとき。標準文書の期待断片は検証しているが、仕様内容の根拠として読む対象ではない。
- 特定の JSON schema の完全な定義を確認したいとき。このテストは schema との一致や validate 例を扱うが、schema 本文は対応する schema 定義を直接読む方がよい。

## hash
- c3bbfa47c5f15061311e3cb2ea25bc300da5f430a64f93824004425ad0142bc7

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
- session の fork・join・abandon に関する CLI 外部挙動をまとめて検証する realization test。session branch と session state のライフサイクルを軸に、状態ファイル生成・更新・破損検出、home branch への復帰、branch 削除、linked worktree 上での操作、dirty worktree 拒否、join 時の conflict resolution とエラー出力先を扱う。
- 大きなテストファイルだが、session branch/state fixture を共有する回帰テスト群として凝集しており、分割せず同一文脈で読むべき理由が冒頭 docstring に明示されている。

## Read this when
- session fork が session branch と state file を作成する挙動、session-id 衝突時の retry・失敗・既存 state 保護、初期 ignore 設定や linked worktree の branch/head 扱いを確認・変更する時。
- session abandon が home branch へ戻り session branch を削除して state を abandoned にする挙動、home branch 欠落時や cleanup 失敗時の rollback・エラー報告を確認・変更する時。
- session join が home branch へ変更を取り込み state を joined にする挙動、oracle conflict resolution の Codex 呼び出し権限、delete conflict の staging、session branch 削除失敗時の警告、dirty worktree や merge 後の予期しないエラー出力先を確認・変更する時。
- session completion 系コマンドが不正な session state file を拒否する共通挙動や、conflict marker block 検出ロジックの期待値を確認する時。

## Do not read this when
- session 以外の CLI サブコマンド、設定読み込み、runtime profile 生成、git helper 単体の挙動だけを調べる時。
- session コマンドの内部実装構造や関数分割を確認したいだけで、CLI 実行結果・branch/state 副作用・エラー出力の回帰観点を必要としない時。
- Codex CLI や LLM の出力品質そのものを検証したい時。このテストは join conflict resolution 呼び出しの権限・副作用を fake で観測するだけで、生成品質は対象にしない。

## hash
- 4c336e5cd265ec18d7aec7006ea53cd2b83a40be57438e6e92ff26b6291f0726
