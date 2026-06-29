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
- cmoc の共通 runtime 契約を横断的に固定する realization test。root placeholder と worktree 境界、config 既定値と検証、CmocError の Markdown report、CLI error の stdout 化、subcommand log、FileAccessMode から sandbox/profile への変換、binary 判定など、個別サブコマンドより下位の実行前提をまとめて検証する。
- 16,000 文字を超えるが、共通 fixture と root 状態の読み取り文脈を分散させないため、basic runtime 回帰として一箇所に置かれている。runtime の共有境界が複数モジュールにまたがって崩れていないかを見る入口になる。

## Read this when
- root placeholder、repo root、run root、work root、linked worktree、run worktree 作成・削除の安全境界に関する実装や回帰を確認するとき。
- CmocConfig、config_from_dict、ModelClass、ReasoningEffort の既定値や不正値処理を変更するとき。
- CmocError、render_error、Click parse error、CLI preflight error、起動 wrapper error など、利用者向けエラー report と stdout/stderr の扱いを確認するとき。
- subcommand log の生成条件、timestamp 衝突時の log file 名、pre-log check 失敗時の副作用抑制を変更するとき。
- FileAccessMode、Codex sandbox mode、Codex cwd、writable_roots、extra_writable_paths、oracle conflict write の許可境界を変更するとき。
- SessionState の branch 名からの session id 抽出、apply branch 形状検証、branch に対応する state 読み取りを変更するとき。
- binary 判定の読み取り量や、`.cmoc` の gitignore 追加挙動を変更するとき。

## Do not read this when
- 特定サブコマンド固有の入出力、状態遷移、ユーザーフローだけを確認したいときは、そのサブコマンドの専用テストを読む。
- oracle file の正本仕様や仕様文書のルーティングを確認したいときは、oracle 側の本文を読む。
- runtime の実装詳細を直接変更する前に API や関数本体を確認したいときは、対応する実装モジュールを読む。
- 単一の小さな helper の純粋な単体挙動だけを確認したいときは、その helper により近い専用テストがあればそちらを優先する。

## hash
- 8688d6642cd0dcbb9aa7f9f74bb561c3b2a6d07fd8c416170b780246b39faaaa

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
- Codex CLI 実行・TUI 起動まわりの runtime 制御を検証する realization test。Codex subprocess の profile 生成、sandbox 設定、作業ディレクトリ、schema 保存先、追加 read path の事前検査、失敗時エラー、CLI 未検出時の扱いを、stub 実行ファイルと一時 repo/worktree で確認する。
- tracked subprocess が専用 process group で起動し、apply process tracking 用環境変数を継承・汚染しないことも検証対象に含む。

## Read this when
- Codex CLI を呼び出す runtime 層、profile 生成、sandbox_workspace_write、read-only 実行、作業ディレクトリ選択、または output schema の一時配置を変更する。
- Codex TUI 起動時の extra_read_paths 検査、pure oracle read と repo write の cwd 切り替え、linked worktree 上の profile writable_roots を確認・変更する。
- Codex subprocess の起動方法、process group、apply tracking pid ファイル、継承環境変数の扱い、または CLI 不在・非ゼロ終了時の CmocError 表示を変更する。

## Do not read this when
- Codex runtime 以外の CLI command、設定読み込み全般、path model、oracle 文書生成など、このファイルが扱う subprocess 起動・sandbox・cwd・schema・TUI 制御に触れない作業をしている。
- Codex CLI や LLM の実際の応答品質を確認したいだけで、cmoc 側が渡す argv、profile、stdin、cwd、ログ、エラー制御を変更しない。
- 個別の helper fixture や repo 作成補助の実装だけを調べたい場合で、その補助の呼び出し元としての runtime 挙動テストを確認する必要がない。

## hash
- 69db57d781c4bc63de09dc4c328cdcf20c5d089f4d63fe5edc5f177ff05ebbf0

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
- Codex exec が quota exceeded になった後の待機、probe、resume または再実行の制御を検証する realization test。
- quota availability probe の共有、resume token の利用有無、call log と subcommand log、CODEX_HOME と cwd の扱いを、同じ retry 状態機械の外部挙動としてまとめて扱う。
- 並列実行時に代表 probe が 1 回だけ使われること、代表 probe 失敗時に待機中の呼び出しも失敗することを確認する。

## Read this when
- Codex exec の quota exceeded 後の retry、resume、再実行、quota availability probe の挙動を変更または確認するとき。
- quota retry 中に作られる call log、subcommand log、prompt/stdout/stderr/output の記録内容やステータスを確認するとき。
- CODEX_HOME が相対パスの場合の subprocess cwd、--cd、oracle root との関係を確認するとき。
- 複数の Codex exec が同時に quota exceeded になった場合の probe 共有、resume 実行、失敗伝播を変更または調査するとき。

## Do not read this when
- quota exceeded 後の Codex exec retry 制御に関係しない通常の Codex exec 成功・失敗処理だけを確認したいとき。
- Codex CLI や LLM の出力品質そのものを検証したいとき。
- 設定読み込み、リポジトリ作成 fixture、Codex profile stub など、retry 状態機械の観測点ではない補助処理の詳細だけを確認したいとき。

## hash
- 27ddbad855496a7d383ac07315bb3e72d2737cd029e5725888c781063cbd17bd

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
- session の fork、join、abandon に関する CLI 外部挙動をまとめて検証する realization test。session branch と session state のライフサイクルを中心に、状態ファイル作成・更新、home branch への復帰、branch 削除、linked worktree 上での挙動、cleanup 失敗時の rollback、dirty worktree 拒否を扱う。
- join 時の merge conflict 解決では、oracle file 競合に対する realization write profile、conflict marker 検出、削除競合の stage、session branch 削除失敗時の警告、想定内エラーと merge 後の想定外エラーの stdout/stderr 出力境界を検証する。
- 16,000 文字を超えるが、session branch/state fixture を共有する session CLI 回帰として凝集させる意図を docstring で明示している。

## Read this when
- session fork が session branch と state file をどう作るか、session-id collision や壊れた state file をどう拒否するかを確認・変更するとき。
- session abandon が home branch へ戻り、session branch を削除し、state を abandoned にする挙動や、home branch 不在・cleanup 失敗時の出力と rollback を確認・変更するとき。
- session join が session branch の変更を home branch へ取り込み、state を joined にし、linked worktree や branch 削除失敗をどう扱うかを確認・変更するとき。
- session join の conflict resolution 呼び出し、oracle file 競合時の writable path 制限、conflict marker 残存判定、削除競合解決の stage を確認・変更するとき。
- session 系 CLI のエラー報告が stdout と stderr のどちらへ出るべきか、未コミット差分拒否や merge 後エラーの外部出力を確認するとき。

## Do not read this when
- session サブコマンド以外の CLI 外部挙動を確認したいだけのとき。
- session の実装詳細、helper の内部設計、永続 state schema の正本仕様を調べたいときは、対応する実装または oracle 側の仕様を先に読む。
- 単体 helper の小さな入力出力だけを確認したいとき。ただし conflict marker block 判定はこの対象内で直接検証している。
- Codex 実行基盤、config 読み込み、runtime profile 全般を調べたいとき。ただし session join の oracle conflict 解決で渡される file access mode と writable roots の境界を確認する場合は読む。

## hash
- f68fc13ab8ba6ee106cc677e28119beb59127eb54374c963df178c941bb5ea69
