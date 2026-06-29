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
- apply fork の CLI 経由テストのうち、所見列挙から適用、commit、変更要約、report 生成、session state 更新までの一連の制御を検証する realization test。
- apply fork report の収束、未収束、error、未追跡 file を含む差分要約、変更 file の再調査、rolling apply fork の対象選定を、同じ loop と report schema の観測結果としてまとめて扱う。
- ACP builder が src のみの PYTHONPATH で import できること、file finding enumeration・finding application・change summary の prompt と structured output schema が期待される構成になることも確認する。

## Read this when
- apply fork の report 内容、終了コード、収束判定、未収束理由、error 時の report、変更要約の出力を変更または調査するとき。
- apply fork が所見を列挙し、Codex 適用後の差分を commit し、変更 file を再調査し、session state を更新する制御フローを確認するとき。
- apply fork の変更要約が commit 済み差分、未 commit 差分、未追跡 file をどう扱うかを調べるとき。
- apply fork の再検査対象から routing 用 index を除外する挙動や、新規 file を再調査対象へ入れる挙動を確認するとき。
- rolling apply fork が前回 apply join 後の oracle 変更を対象にし、無関係 branch の変更を対象外にする条件を検証するとき。
- apply fork 向け ACP builder の prompt 構成、root token 展開、schema path、相対 target path の拒否条件を変更するとき。

## Do not read this when
- apply fork 以外のサブコマンドの通常 CLI 動作だけを調べるとき。
- report 生成や再検査制御に関係しない git helper、path model、設定 loader の局所的な実装だけを確認したいとき。
- apply fork の内部 helper の単体的な入出力だけを確認でき、CLI 実行、session state、report 出力をまたぐ挙動が不要なとき。
- oracle 側の正本仕様や schema 定義そのものを確認したいとき。

## hash
- 42db647398a11f1c185bd620d6fa9cb099d1c2836dd559be4d014d3e59d02520

# `test_apply_join_cli.py`

## Summary
- apply run を session へ join する CLI 外部挙動を検証する realization test。成功時の merge、state 更新、report 生成、apply worktree/branch cleanup と、dirty worktree・stale apply branch・想定外差分・merge conflict など join 可否の境界条件を同じ文脈で扱う。
- 16,000 文字超のテストだが、apply join の成功条件と拒否条件を一箇所で読む方が fixture、git 状態、session/apply worktree の文脈が分散しないという責務境界を docstring で説明している。

## Read this when
- apply join の CLI 挙動、終了コード、標準出力、report 生成、state の ready/completed 更新を確認・変更する。
- apply join 後に apply worktree や apply branch が削除される条件、または current cwd が apply worktree の場合に cleanup を残す条件を確認する。
- linked session worktree からの join が、root ではなく現在の session worktree へ merge する挙動を扱う。
- stale apply branch、dirty apply worktree、想定外差分、削除パス、rename target、root memo、.gitignore 変更、merge conflict、force-resolve の境界条件を検証・変更する。
- apply join の差分分類 helper や managed branch の changed path 判定に関するテストを確認する。

## Do not read this when
- apply fork の Codex 実行、apply worktree 作成、Codex 出力処理そのものを調べたい場合。ここではそれらを fake 化して join 前提を作るだけである。
- session fork や init の一般挙動を調べたい場合。ここでは apply join の前提状態を作るために呼ぶだけである。
- apply join 以外の CLI サブコマンド、設定、path model、oracle/realization の一般仕様を確認したい場合。
- 単体 helper の内部実装だけを読みたい場合。外部挙動ではなく実装詳細が主目的なら、対応する実装モジュールを直接読む方が適切である。

## hash
- df328efd98cf220f4ec46636ab835300ce6203fc215042383d7795aa62e87097

# `test_basic_runtime.py`

## Summary
- cmoc の共通 runtime 契約を横断的に固定する realization test。root/worktree 判定、設定値検証、構造化エラー表示、CLI preflight と parse error、subcommand log、`.cmoc` ignore、FileAccessMode から sandbox/profile への変換、binary 判定、session/apply branch state 読み取り境界を同じ基礎 runtime 回帰として扱う。
- 個別サブコマンド固有の正常系ではなく、複数機能の実行前提になる runtime 境界が同時に崩れないことを確認する入口に位置づく。

## Read this when
- root placeholder、repo root、run root、work root、linked worktree、main worktree 拒否などの path/root 解決挙動を変更・調査する時。
- CmocConfig、config_from_dict、ModelClass、ReasoningEffort など、基礎 config の既定値や型検証を変更・調査する時。
- CmocError、render_error、CLI 引数解析 error、stdout/stderr の error report 出力方針を変更・調査する時。
- CLI preflight、shell completion probe、subcommand log の生成・失敗記録・副作用抑制を変更・調査する時。
- `.cmoc` の gitignore 追加、literal ignore pattern、既存 ignore pattern との関係を変更・調査する時。
- FileAccessMode、Codex sandbox mode、Codex cwd、writable_roots、追加書き込み許可 path の許可・拒否境界を変更・調査する時。
- session branch、apply branch、SessionState の読み取り対象 branch 形状を変更・調査する時。
- binary 判定の読み取り量や file open mode を変更・調査する時。

## Do not read this when
- 個別サブコマンドの業務ロジック、入出力 schema、成功時ワークフローだけを調べたい時は、対象サブコマンドの実装や専用テストを先に読む。
- oracle の正本仕様断片そのものを確認したい時は、対応する oracle doc/src/test を読む。このテストは realization test であり、正本仕様ではない。
- runtime と関係しない UI、ドキュメント、補助スクリプト、生成物管理だけを調べたい時は、該当する同階層または下位領域へ直接進む。
- 単一 helper の内部実装だけを局所的に確認したい時は、その helper が定義されている実装ファイルを先に読む。

## hash
- dce2d9010d1ec93248de42380fd1b05cd21885d948c6719f63e4c34b1cba2c62

# `test_cli_init_tui.py`

## Summary
- init と TUI 起動直前の CLI 外部挙動を検証する realization test。初期化時の .cmoc 無視設定、既存 staged/unstaged 差分の保護、既存 .cmoc 追跡解除、既定 config.json 生成と既存設定値の保持、sub_command ログ、linked worktree 上での root/worktree 分離を扱う。
- TUI については、エディタで作成された Markdown prompt からコメントを除去して完全版 prompt を保存し、resolve_parameter の結果から AgentCallParameter を構築して Codex TUI を起動する前処理を検証する。linked worktree ではログ保存先、schema 生成先、root/cwd、extra_read_paths が期待通り分離されることも確認する。
- 16,000 文字を超えるが、init 済み状態と TUI 前処理が同じ利用開始直後の CLI 境界を共有するため、repository/runtime 準備の回帰テストとして一箇所にまとめられている。

## Read this when
- init の外部挙動、特に .cmoc の git ignore、.gitignore 更新、既存差分の保護、tracked .cmoc file の untrack、初期 commit、config.json の既定値同期を変更または確認する場合。
- linked worktree で init または tui を実行したときの、共通 root 側 .cmoc と worktree 側 .gitignore、ログ保存先、schema 保存先、git status への影響を確認する場合。
- tui サブコマンドの起動前処理、エディタ起動、Markdown prompt のコメント除去、resolve_parameter 呼び出し、file_access_mode の既定化、AgentCallParameter の組み立て、Codex TUI 呼び出し引数を変更または確認する場合。
- sub_command ログのイベント内容や、init/tui が古いログディレクトリではなく現在の log/sub_command・log/tui 配下を使うことを確認する場合。

## Do not read this when
- 個別の CLI サブコマンド実装や内部 helper の詳細だけを調べたい場合は、対応する実装ファイルを先に読む。
- init や tui に関係しないサブコマンド、oracle review、apply fork、一般的な config schema の詳細を調べる場合は、より直接のテストまたは実装を読む。
- Codex CLI やエディタ実体の出力品質そのものを検証したい場合は、このテストの対象外であり、ここでは前処理と呼び出し境界だけを扱う。
- 単純な path model、repository root 検出、git helper の単体挙動だけを確認したい場合は、それらを直接検証するテストまたは実装を読む。

## hash
- 8165435f4efa3ccf701190d3ce0e4d5b01bc5cf253eef38bc3ee77c0b96fc42b

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 呼び出しの実行時挙動を検証する realization test。exec/TUI の起動引数、作業ディレクトリ、sandbox profile、出力 schema 配置、プロセス追跡、環境変数の遮断、失敗時エラー報告を、スタブ化した CLI と一時リポジトリで確認する。
- file access mode ごとの Codex 実行制御、pure oracle read 時の oracle 配下への制限、linked worktree での状態保存先、保護領域外 extra read path の拒否など、runtime 層が Codex subprocess に渡す境界条件を扱う。

## Read this when
- Codex exec/TUI 起動時の `--cd`、`--profile`、`--json`、`--output-last-message`、`--output-schema` などの引数生成や作業ディレクトリ選択を変更・確認するとき。
- Codex 用 sandbox profile の read-only / workspace-write、writable roots、memo や .agents の扱い、pure oracle read の制限を変更・確認するとき。
- Codex subprocess の process group 追跡、apply tracking 環境変数の遮断、missing CLI、nonzero exit のエラー処理やログ出力を変更・確認するとき。
- linked worktree からの Codex 呼び出しで、schema state や TUI call log、complete prompt の読み込み許可がどこに紐づくべきかを調べるとき。

## Do not read this when
- Codex runtime の外部挙動ではなく、汎用的な path model、設定 schema、CLI parser、または oracle 文書の正本仕様だけを確認したいとき。
- Codex CLI や LLM の出力品質そのもの、プロンプト内容の妥当性、生成結果の文章品質を検証したいとき。
- 実 subprocess を使わない単純なユニットロジックや、Codex 以外の外部コマンド実行制御を調べるとき。

## hash
- df375403644f1fb37b48b7ebe8520d92d6dd185dc10912db90a8da000974bccb

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
- Codex exec が quota exceeded になった後の待機、quota availability probe、resume token を使った再開、resume token が無い場合の再実行を検証する realization test。
- fake Codex 呼び出しを使い、call log、subcommand log、標準入出力ログ、出力 JSON、CODEX_HOME と cwd の扱いを、quota retry 状態機械の外部観測点としてまとめて確認する。
- 並行実行時に quota availability probe が代表 1 回だけ実行され、成功時は待機中の呼び出しが resume へ進み、失敗時は待機中の呼び出しも CmocError になることを検証する。

## Read this when
- Codex exec の quota exceeded 後の retry、probe、resume、再実行の挙動を変更または調査するとき。
- quota availability probe の argv、prompt、ログ出力、戻り値、標準出力・標準エラー・output-last-message の扱いを確認したいとき。
- resume token の抽出と利用、または resume token が無い quota retry で元 prompt を再実行する挙動を確認したいとき。
- FileAccessMode に応じた Codex 実行 cwd と、相対 CODEX_HOME の解決基準を変更または調査するとき。
- 複数の Codex exec が同時に quota exceeded になった場合の probe 共有、待機、成功時 resume、失敗時エラー伝播を扱うとき。

## Do not read this when
- quota retry と関係しない通常成功時の Codex exec 呼び出しだけを確認したいとき。
- Codex CLI や LLM の出力品質そのものを評価したいとき。
- 設定読み込み、リポジトリ作成 fixture、Codex home 構築 helper など、quota retry 状態機械の外部挙動ではなくテスト補助処理そのものを調べたいとき。
- oracle file の正本仕様やルーティング規則を確認したいとき。

## hash
- 48ea6bc9b7545bee93cd27b450ed14a8706f2fb3887247cd68b33a4eadd03e2d

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
- indexing の preflight と CLI サブコマンドが routing document を生成・更新し、INDEX.md conflict、hash 再利用、Codex 呼び出し、commit 対象、linked worktree、dirty worktree をどう扱うかを外部挙動として検証する realization test。
- semantic entry の妥当性検証、 malformed entry の再生成、兄弟 entry の並列生成、root 直下 memo 除外と nested memo 対象化まで含め、indexing 更新ワークフローの回帰観測点を一箇所に集約している。

## Read this when
- indexing サブコマンドや indexing preflight の成功・失敗条件、git 差分がある場合の停止条件、INDEX.md 更新後の commit 条件を確認・変更するとき。
- INDEX.md conflict 解決、既存 hash が新鮮な場合の Codex 呼び出し省略、malformed entry の再生成、semantic field のバリデーションを確認するとき。
- linked worktree や apply worktree 上で indexing がどの root/config/cwd を使い、どの worktree に INDEX.md を作成するかを確認するとき。
- routing document 更新対象の列挙、兄弟 entry の並列生成、root 直下 memo と nested memo の扱いを変更するとき。

## Do not read this when
- 個別の indexing 実装ロジックや helper の責務を知りたいだけなら、対応する実装ファイルを読む。
- init、apply、join など indexing の回帰観測点として現れる範囲を超えたサブコマンド仕様を調べるだけなら、より直接の CLI テストや実装を読む。
- INDEX.md エントリーの文章生成規則や正本仕様断片を確認したいだけなら、oracle 側の該当文書を読む。

## hash
- f054171afce78e8df4c108ca283958c3d8bcaa6f3256b7eff69b64068e45fc9a

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
- prompt part と AgentCallParameter builder の生成結果を横断的に検証する realization test。標準 prompt、routing rule、file access rule、各種 standard 文書、structured output schema path、model/reasoning/file access mode の選定、packaged layout での import 可否が期待通りに組み合わさることを確認する。
- prompt 構築に関する回帰観点を一箇所に集約しており、render_as_markdown の整形、complete prompt への標準文書注入、apply/review/indexing/session/tui 系 builder の prompt・schema・parameter をまとめて検証する。

## Read this when
- prompt builder parts の出力文言、見出し、markdown rendering、または complete prompt に含まれる標準文書の有無を変更・確認したいとき。
- routing rule、file access rule、oracle/realization/review/apply/index entry standard の prompt への組み込み条件や、出力に残すべき用語・root token・placeholder の扱いを確認したいとき。
- apply fork、review oracle、indexing、session join、TUI resolve parameter の builder が返す model class、reasoning effort、file access mode、structured output schema path、schema 内容、prompt 断片を変更・検証したいとき。
- oracle schema JSON と builder が参照する structured output schema の一致、jsonschema validation、または packaged layout での builder import 可否に関わる回帰を調べたいとき。

## Do not read this when
- 個別 builder の実装詳細や prompt 文書の本文生成ロジックを直接修正したいだけで、期待される横断的な出力・schema・parameter の回帰条件を確認する必要がないとき。
- CLI の実行フロー、永続状態、git 操作、worktree 操作など、prompt part や AgentCallParameter builder の生成結果と関係しない挙動を調べるとき。
- 特定の oracle specification 本文や schema JSON の正本内容そのものを確認したいとき。この対象はそれらの内容を直接定義せず、builder が正本 schema や標準文書を参照していることを検証する側である。

## hash
- ee25c5b1d1e7d359a231b55995d5c9429c3f394f000222f83c428ef268e5429a

# `test_review_oracle_cli.py`

## Summary
- review oracle の CLI 経由の外部挙動と、所見の列挙・検証・judge・merge を含む評価 loop の制御を検証する realization test。report の構成、scope ごとの対象選択、linked worktree での review 実行、INDEX.md 変更の取り込み、エラー report、想定外差分の拒否まで、同じ review run の状態と出力を共有する観点をまとめて扱う。
- 対象は 16,000 文字を超えるが、fake Codex 応答、report 文脈、review worktree の状態確認が強く結びついているため、oracle review の読み取り文脈を一箇所に保つ構成になっている。

## Read this when
- review oracle command の report 出力、判定結果、件数表示、エラー時 report、または stdout/stderr の振る舞いを変更・確認する。
- oracle review の所見 loop について、enumerate、challenger/advocate validation、judge、merge の呼び出し順・入力文脈・結果反映を変更・確認する。
- full scope または session scope で、review 対象 oracle の選択、gitignored oracle、binary、symlink、memo 配下との境界、対象 0 件時の挙動を確認する。
- linked worktree 上の session branch、review 用 worktree、fork commit、join commit、INDEX.md 変更の merge、conflict 解決に関する挙動を変更・確認する。
- review oracle 実行中に生成された INDEX.md 以外の差分を拒否し、元の作業ツリーへ戻さない保証を確認する。

## Do not read this when
- review oracle 以外の command や、一般的な session/init/fork の基本挙動だけを調べたい場合。
- Codex 実行 wrapper、設定 loader、git helper などの低レベル実装だけを変更しており、review oracle の外部挙動や loop 制御に影響しないことが明らかな場合。
- oracle file の正本仕様そのものを確認・編集したい場合。この対象は realization test であり、正本仕様の代替ではない。
- 単一 helper の純粋な入力検証だけを確認したい場合。ただし所見 merge operation の contract や reused target 拒否に関係する場合は読む。

## hash
- 27b2d74b61abecd54e93d474cec75368d64d7971b72b8b08cffd658587f2d053

# `test_session_cli.py`

## Summary
- session 系 CLI の fork、join、abandon に関する外部挙動回帰をまとめて検証する realization test。session branch と session state のライフサイクルを中心に、linked worktree、state cleanup、dirty worktree 拒否、join conflict resolution、エラー出力先を一連の状態遷移として扱う。
- 16,000 文字超の大きなテストファイルだが、分割すると同じ branch/state fixture と session 状態遷移の文脈が散るため、session CLI 回帰として凝集させる意図が docstring に明記されている。

## Read this when
- session fork が session branch と state file を作る挙動、session-id 衝突時の retry や既存 state 非破壊、壊れた state file の拒否を確認・変更したいとき。
- session abandon が home branch へ戻る、session branch を削除する、state を abandoned に更新する、cleanup 失敗時に state と branch を巻き戻す挙動を確認・変更したいとき。
- session join が home branch へ統合する、join 後 state を joined にする、session branch 削除失敗を warning として扱う、delete conflict resolution を staging する挙動を確認・変更したいとき。
- linked worktree 上で fork、join、abandon が root worktree ではなく現在の linked worktree branch/head を基準に動くかを確認したいとき。
- oracle conflict resolution で Codex 呼び出しの file access mode、conflict marker 検出、解決後に marker が残った場合の stderr 報告を確認・変更したいとき。
- session join/abandon のエラー報告が stdout と stderr のどちらへ出るべきか、sub command log や elapsed などの完了レポートを含めて確認したいとき。

## Do not read this when
- session 以外の CLI サブコマンド、init や apply など独立した外部挙動だけを確認したいとき。
- session state の JSON schema や branch 操作 helper の実装詳細だけを確認したいときは、対応する実装モジュールやより局所的なテストを先に読む。
- Codex 実行そのものの品質や LLM 出力内容を検証したいとき。この対象は fake_run_codex_exec による制御ロジックと外部副作用の確認に限られる。
- 個別 helper の純粋関数的な単体挙動だけを調べたいとき。ただし conflict marker block 検出については、この対象に直接の小さな回帰テストがある。

## hash
- e1b97a78183f137330182536dd41ca271a393d493f2b3b5f6d8aef66b9a81609
