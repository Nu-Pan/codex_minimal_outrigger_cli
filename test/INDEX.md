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
- apply fork の CLI 実行について、所見列挙から適用、commit、変更要約、report 生成、session state 更新までの制御を検証する realization test。
- 収束、未収束、error、変更ファイル再調査、未追跡ファイル差分、調査対象なし、rolling apply fork の基準 commit を、同じ loop と report schema の観測結果としてまとめて扱う。
- 16,000 文字を超えるが、apply fork report の読み取り文脈を一箇所に保つために分割しない構成になっている。

## Read this when
- apply fork の CLI 終了コード、report 内容、変更要約、commit message、session state 更新の期待挙動を確認したいとき。
- apply 後に変更されたファイルの再調査、INDEX.md 除外、最後の調査対象が空所見だった場合の収束判定、差分なし適用時の未収束扱いを調べるとき。
- error report が commit 前の working tree 差分や未追跡ファイルを変更要約に含める挙動を検証したいとき。
- rolling apply fork が前回 apply join 後の変更だけを対象にする基準 commit と state 更新を確認したいとき。

## Do not read this when
- apply fork の実装本体、所見列挙、report rendering、変更差分抽出 helper の処理を変更したいだけなら、対応する実装ファイルを先に読む。
- apply join、session fork、init など apply fork 以外の CLI 挙動を調べたいだけなら、それぞれの専用テストまたは実装へ進む。
- Codex 実行 fake やテスト用 repository helper の共通仕様を調べたいだけなら、共通 test support を読む。

## hash
- e37ab52b0366ab0f7a47ae7b1f6c80560e4eb5a95db9f93230deb2a4f7b6b53a

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
- indexing preflight と indexing サブコマンドが routing document を生成・更新・commit する外部挙動を検証する realization test。Codex によるエントリー生成、既存 hash の再利用、dirty worktree の拒否、linked worktree 対象化、conflict 解決、semantic field の検証、並列生成、root 直下 memo 除外と nested memo 対象化を同じ routing 更新ワークフローの観測点として扱う。

## Read this when
- indexing CLI の成功・失敗条件、commit 対象、未初期化 repo や dirty repo での停止挙動を確認・変更したいとき。
- indexing preflight が通常の indexing サブコマンドと異なり、既存の非 INDEX 差分を許容しつつ routing document だけを commit する挙動を確認したいとき。
- routing document エントリーの hash freshness、malformed entry 再生成、semantic field の妥当性検証、Codex 呼び出し省略条件を変更したいとき。
- linked worktree や apply worktree 上で、対象 root、cwd、repo config、commit 先がどう扱われるかを検証したいとき。
- root 直下 memo を indexing 対象から除外し、通常ディレクトリ配下の memo は indexing 対象にする境界を確認したいとき。

## Do not read this when
- routing document の生成・更新ワークフローではなく、個別サブコマンドの UI や一般的な CLI 起動構造だけを調べたいとき。
- Codex 実行 wrapper、config model、path model などの実装詳細そのものを変更したいだけで、このテストが観測する indexing 外部挙動に触れないとき。
- 単一の小さな helper の純粋な内部処理を確認したいだけで、git 状態、commit、worktree、routing document 更新の副作用を伴わないとき。

## hash
- b577ba759f1311d8f153cc859e5dbf03d375f4e57944016a55663e2d1738be93

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
- prompt part 群と ACP builder 群が生成する StructDoc、最終 prompt、file access rule、routing rule、各種 standard、Structured Output schema、AgentCallParameter の主要属性を横断的に検証する realization test。
- 標準 prompt の組み立て、root path の置換、cmoc 呼び出しメタデータ除去、oracle 由来 schema との一致、review/apply/session/tui/indexing 各 builder のモデル・reasoning・file access mode 選択を一箇所で確認する。
- 16,000 文字を超えるが、agent prompt と structured output schema の構築結果を同じ読み取り文脈で検証するために凝集させている、prompt 構築回帰の入口となるテスト群。

## Read this when
- prompt part の markdown render 結果、blank line 折り畳み、standard 文書の必須語句、または complete prompt に含める補助 standard の有無を確認・変更するとき。
- ACP builder が返す model class、reasoning effort、file access mode、prompt 本文、structured output schema path の期待値を調べるとき。
- apply fork、review oracle、session join、TUI parameter resolution、index entry generation に関する builder の回帰テストや schema 一致検証を追加・修正するとき。
- absolute root path を現在の repository root に置換する挙動、code block 内外の置換、literal root token コメント要件、cmoc 呼び出しメタデータ除去の期待値を確認するとき。

## Do not read this when
- 個別 builder や prompt part の実装詳細を変更したいだけで、該当する実装ファイルや oracle schema を直接読めば十分なとき。
- CLI の実行経路、ファイル探索、差分適用、セッション管理など、prompt/schema 生成結果以外の外部挙動を確認したいとき。
- 特定の JSON schema の正本内容そのものを確認したいとき。このテストは一致を検証する入口であり、schema の内容理解には対応する oracle source を読む方が直接的。

## hash
- 818aaa05b3ae11a80d0f666b69213dd89e1325060c244ec86c8935a7dd9ba2c8

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
