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
- apply fork の CLI 実行を通じて、所見列挙、所見適用、commit、変更要約、report 生成、session state 更新までの制御を検証する realization test。
- apply fork report の収束、未収束、error、変更ファイル再調査、rolling fork を、同じ loop と report schema の観測結果としてまとめて扱う。
- apply fork 用 ACP builder の import 条件、prompt 内容、schema 同期、変更要約用 diff/path/fallback 処理も、CLI 経由の apply fork report 文脈に必要な前提として検証する。

## Read this when
- apply fork CLI の exit code、report 内容、変更要約、commit message、session state 更新の期待挙動を確認または変更するとき。
- apply fork が所見適用後に変更ファイルを再調査する制御、再調査対象から除外する path、上限回到達時の収束・未収束判定を確認するとき。
- apply fork の error report が未 commit 差分や未追跡 file を変更要約に含める挙動を確認するとき。
- rolling apply fork が前回 apply join 後の変更だけを対象にする挙動を確認するとき。
- apply fork 関連の ACP builder が src の PYTHONPATH だけで import できること、標準 prompt や structured output schema を正しく選ぶことを確認するとき。

## Do not read this when
- apply fork 以外の CLI サブコマンドや、apply join 単体の通常成功経路だけを確認したいとき。
- report の markdown 描画や変更要約 helper の実装詳細だけを局所的に直したい場合で、該当する実装ファイルやより小さい単体テストを直接読めば足りるとき。
- ACP builder 全般の設計や prompt 標準部品そのものを確認したい場合で、apply fork report の CLI 制御と関係しないとき。

## hash
- 66c9763922953bb1a3b03110f327028150a160012dbbf561c1b6d4b0576c2c12

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
- 基礎 runtime の共通契約を横断的に固定する pytest 群。root token/path 解決、linked worktree と run/work root、設定既定値と不正値、CmocError の Markdown report、CLI error の stdout 出力、subcommand log、`.cmoc` ignore、FileAccessMode 変換、Codex sandbox profile、binary 判定など、個別サブコマンドより下位の実行前提をまとめて検証する。
- 大きめのテストファイルだが、分割すると共通 fixture と root 状態の文脈が散るため、basic runtime 回帰として一箇所に集約されている。

## Read this when
- 基礎 runtime の回帰テストを確認・変更する。
- root token、repo root、run root、work root、linked worktree の扱いを変更する。
- CmocConfig、config_from_dict、model class、reasoning effort、FileAccessMode の既定値・検証・変換を変更する。
- CmocError、render_error、Click parse error、CLI preflight error、stdout/stderr のエラー表示契約を変更する。
- subcommand log、pre-log check failure、起動 wrapper の missing venv report、`.cmoc` の gitignore 追加を変更する。
- Codex profile の sandbox mode、writable_roots、extra writable paths、memo・oracle・.agents へのアクセス制限を変更する。
- binary 判定の読み取り範囲や先頭 chunk 判定を変更する。

## Do not read this when
- 個別サブコマンド固有の業務ロジックや出力だけを調べたい場合。
- oracle 正本仕様そのものを確認したい場合。
- runtime の共通境界に触れない UI、文書、補助ファイル、または特定機能の局所テストだけを扱う場合。
- テスト補助の make_repo、run_git、runner 自体の実装を調べたい場合は、先にテスト support 側を読む。

## hash
- de4d6c5eb4a1d893a3c688a328dd6eb334e0c387998d5efbd1fd1eb24043b8a9

# `test_cli_init_tui.py`

## Summary
- init と対話起動前処理の CLI 境界を検証する realization test。cmoc 初期化時の .cmoc ignore、既存の staged/unstaged 差分保護、既定設定生成と人間設定の保持、linked worktree での repository/runtime 準備、sub command log、Markdown prompt 補完、TUI 起動用 AgentCallParameter 構築を外部挙動としてまとめて扱う。
- 16,000 文字を超えるが、利用開始直後の init/TUI 前処理で共有される初期化済み状態の読み取り文脈を一箇所に保つための回帰テスト群として位置づけられている。

## Read this when
- init の外部挙動、特に .cmoc 配下の追跡解除、.gitignore または exclude への ignore 反映、cleanup commit、既存ユーザー差分を commit しない保証を確認・変更するとき。
- 初期設定ファイルの既定値、既存設定への defaults 同期、人間が設定した値を上書きしない挙動を確認・変更するとき。
- linked worktree 上で init や tui を実行した場合の root/cwd、ログ保存先、schema 保存先、ignore 状態、worktree 側に不要な .cmoc 状態を残さない保証を確認・変更するとき。
- tui 起動で editor が更新した Markdown prompt から HTML comment を除去し、補完済み prompt を保存し、parameter 解決用 Codex exec と TUI 用 Codex 起動へ渡す値を確認・変更するとき。
- file_access_mode の解決結果、空の解決値の既定値、model class、reasoning effort、structured output schema、extra read paths など TUI 用 AgentCallParameter の組み立てを確認・変更するとき。
- sub command log の command_invoked event、argv、ログディレクトリ構成など、init/tui の起動直後に残るログ形式を確認・変更するとき。

## Do not read this when
- 個別の CLI 実装内部だけを調べたい場合。外部挙動の期待値ではなく処理本体を追うなら、対応する実装側へ進む方が直接的。
- init や TUI 前処理と無関係なサブコマンド、review、apply、oracle 操作、通常の Codex 実行フローを扱う場合。
- Codex CLI や LLM の出力品質そのものを検証したい場合。この対象は fake/stub を使って cmoc 側の制御と渡し値を検証している。
- 単純な path model、設定 schema の全体定義、または git helper の単体仕様だけを確認したい場合。ここではそれらを init/TUI 境界の副作用としてしか扱わない。

## hash
- 79e2e340673bef7b1e014fb8f82b247ea4be8687bc1cf5674efc68f6332ea792

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 実行ラッパーのテスト群。exec/TUI 呼び出し時のプロファイル生成、作業ディレクトリ、sandbox 設定、schema 保存先、外部 Codex プロセス起動失敗時のエラー処理、プロセスグループ追跡を検証する。
- 実際の Codex CLI の代わりに一時ディレクトリ上の stub 実行ファイルを使い、引数・標準入力・環境変数・生成ログ・例外を観測して runtime_codex 系の制御ロジックを確認する。

## Read this when
- Codex CLI の exec/TUI 呼び出し処理、プロファイル生成、sandbox/read-only/workspace-write 設定、PURE_ORACLE_READ 時の cwd 制限を変更する時。
- Codex 呼び出しに渡す引数、標準入力、output schema の保存場所、CODEX_HOME 配下の profile ファイル生成を変更する時。
- Codex subprocess の process group 追跡、missing CLI、非ゼロ終了、許可領域外 extra read path のエラー処理を確認・変更する時。
- run_codex_exec または run_codex_tui の外部挙動を壊していないか、stub Codex CLI を使った realization test を追加・整理したい時。

## Do not read this when
- Codex CLI 呼び出しではなく、通常のリポジトリ作成 fixture、git helper、テスト支援関数そのものの実装だけを調べる時。
- runtime の実装詳細を確認したいだけで、テストが期待する外部挙動や回帰条件を読む必要がない時。
- oracle file の正本仕様断片を確認したい時。このファイルは realization test であり、仕様本文の代替にはならない。

## hash
- c126a1639b866793c055fab3f70db456954abc5ce53369675742f36fd82a3b0e

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
- Codex exec が quota exceeded になった後の待機、probe、resume、再実行の外部挙動を検証する realization test。fake Codex 呼び出し列、call log、subcommand log、CODEX_HOME と cwd、並列実行時の probe 共有を観測し、quota retry 状態機械の回帰を一箇所で扱う。

## Read this when
- Codex exec の quota retry 制御、quota availability probe、resume token 利用、resume token が無い場合の再実行挙動を変更・調査するとき。
- Codex 呼び出しの call log、subcommand log、標準出力ログ、prompt log、output-last-message の記録内容や順序を変更・検証するとき。
- CODEX_HOME が相対パスの場合の実行 cwd、oracle root を使う file access mode、または並列実行時に代表 probe を共有する制御を確認するとき。
- quota exceeded 後の状態遷移を外部プロセスの引数、stdin、環境変数、ログ副作用から追う必要があるとき。

## Do not read this when
- Codex CLI 呼び出し一般の正常系だけを確認したいとき、quota exceeded 後の待機・probe・resume・再実行に関係しないなら読む優先度は低い。
- 設定読み込み、リポジトリ生成 helper、Codex profile stub などの test support 自体を調査したいときは、先に対応する support 実装を読む。
- quota retry 以外の runtime、CLI、oracle/realization 仕様、または INDEX 生成規則を調べるときは、より直接その責務を持つ文書やテストへ進む。

## hash
- 1cbdcb9f63f87eec975749a9e63809ea44788b2c5b7f5f7622e0a7c91164ef29

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
- indexing preflight と indexing subcommand が routing document を生成・更新・commit する外部挙動を検証する realization test。
- 未初期化・dirty worktree・linked worktree・apply worktree 設定参照・fresh hash 再利用・malformed entry 再生成・semantic field validation・sibling 並列生成・memo 除外境界を、routing 更新ワークフローの回帰としてまとめて扱う。
- routing document conflict 解決で対象 document を削除して merge commit を完了させる apply 側の境界も、同じ routing 更新ワークフローの観測点として含む。

## Read this when
- indexing CLI が clean repo だけで実行され、routing document 更新後に indexing commit を作る条件を確認したいとき。
- indexing preflight が通常の indexing subcommand と異なり、既存の非 routing document 差分を許しつつ routing document だけを commit する挙動を確認したいとき。
- linked worktree や apply worktree から indexing を実行したとき、対象 worktree・参照する repository config・commit 先が正しいかを確認したいとき。
- 既存 hash が fresh な entry の Codex 呼び出し省略、malformed entry の再生成、semantic list の受理・拒否条件を確認したいとき。
- routing document 生成対象の列挙、sibling entry の並列生成、root 直下の memo 除外と nested memo indexing の境界を確認したいとき。
- routing document conflict 解決の delete-and-commit 挙動を apply workflow 側から確認したいとき。

## Do not read this when
- 個別の indexing 実装アルゴリズムや parser helper の内部構造を変更したいだけで、CLI・preflight・git commit 境界の回帰確認が不要なとき。
- routing entry の文面そのものや Codex 生成結果の品質を評価したいとき。
- init、apply、git helper、runtime config の一般的な仕様を調べたいだけで、indexing workflow との接続条件を扱わないとき。
- 単一の小さな rendering 仕様だけを確認したい場合で、より局所的な unit test や実装本文から直接確認できるとき。

## hash
- 44b3240ac87938539cea96444edb51175fc76ee5286f694be5600fa56a23dc1e

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
- agent prompt と structured output schema の構築結果を横断的に検証する realization test。prompt builder parts、complete prompt、ACP builder parameter、schema path、oracle schema との一致、file access mode、model/reasoning 設定、root placeholder の扱いをまとめて回帰確認する。
- 標準 prompt、routing、file access、builder parameter が最終 prompt 上で同じ読み取り文脈に合流することを前提に、共通の render/schema 期待値を一箇所で検証する入口として位置づけられている。

## Read this when
- prompt builder parts が生成する markdown の見出し・本文断片・空行畳み込みの期待値を確認または変更する時。
- complete prompt に routing rule、oracle/realization/review/apply/index entry standard、root token、work root placeholder、補助 prompt がどう含まれるかを確認する時。
- apply fork、review oracle、session join、TUI parameter、indexing index entry などの ACP builder が返す model class、reasoning effort、file access mode、prompt 内容、structured output schema path を検証する時。
- realization 側の JSON schema が oracle 側の schema と一致しているか、また jsonschema validate の最小例が通るかを確認する時。
- oracle package の配置や packaged layout から review oracle enumerate builder を import できるかに関する回帰を追う時。

## Do not read this when
- 個別 builder の実装詳細や prompt 文面の生成ロジックを直すだけなら、対応する src または oracle 配下の builder/prompt parts 本体を直接読む方がよい。
- 特定の structured output schema の正本内容を確認したいだけなら、対応する oracle 側 JSON schema を直接読む方がよい。
- CLI の利用者向け挙動やコマンド実行フローを調べる時は、この横断的な prompt/ACP 回帰テストではなく対象コマンドの実装・テストを読む方がよい。
- INDEX.md エントリー生成規則そのものの内容を確認したい時は、このテストではなく index entry standard を生成する prompt part またはその正本仕様を読む方がよい。

## hash
- e8793091799005bd88a3c8d33409fcaf852b7abd7256762f36e0fa4c2ed977f1

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
