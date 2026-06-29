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
- init と TUI 起動直前の CLI 前処理について、外部挙動として守るべき回帰条件をまとめて検証する realization test。
- cmoc 初期化時の .cmoc ignore、既存 staged/unstaged 差分の保護、設定 JSON の初期生成と既存値を保った default 同期、linked worktree での repository root/runtime root の扱いを確認する。
- TUI 起動時の editor 実行、Markdown prompt のコメント除去と完成 prompt 保存、resolve parameter の解釈、Codex TUI 呼び出し parameter、linked worktree での log/schema 保存先を一続きの CLI 境界として検証する。

## Read this when
- init の外部挙動、特に .cmoc を Git 追跡対象から外す処理、.gitignore や info/exclude への ignore 追加、既存のユーザー差分を commit に巻き込まない制御を変更・確認する時。
- 初期設定ファイルの default 値、既存設定を上書きしない同期、sub command log の command_invoked 記録を変更・確認する時。
- linked worktree 上で init または TUI を実行した時の保存先、ignore 状態、commit 対象、root/cwd の渡し方を変更・確認する時。
- TUI の editor 起動、入力 Markdown の前処理、完成 prompt の構成、resolve parameter 用 Codex exec と実際の Codex TUI 呼び出し parameter の組み立てを変更・確認する時。
- file access mode の解決値が空の場合の default 挙動や、TUI log/schema が repository root 側に保存される挙動を確認する時。

## Do not read this when
- 個別の CLI command 実装だけを読みたい時は、まず対応する implementation を読む方が直接的である。
- init や TUI 前処理を通らない subcommand、agent 実行、review、apply、index 生成の挙動だけを調べる時。
- 設定 schema の全体構造や path model の定義そのものを確認したい時は、対応する仕様または実装を読む方が直接的である。
- Codex CLI や editor 実体の品質・出力内容そのものを検証したい時。この対象は外部ツールを stub し、cmoc 側の呼び出し境界と副作用だけを扱う。

## hash
- a2d4409d80ad812d7b867eb299254b72efe3542b28662d136ba9d3b7681955af

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 呼び出しを実行・追跡する runtime 周辺の realization test。exec/TUI 起動時の profile 生成、作業ディレクトリ、sandbox 設定、schema 状態保存先、許可外パス検査、失敗時エラーとログ、CLI 未検出時のエラーを検証する。
- 実体の Codex CLI には依存せず、テスト用実行ファイルと一時リポジトリを使って、subprocess 呼び出しの引数・環境・標準入力・出力ファイル・例外変換を観察する入口になる。

## Read this when
- Codex exec/TUI の起動引数、profile TOML、CODEX_HOME、作業ディレクトリ、sandbox mode、writable roots の期待挙動を変更・確認したいとき。
- FileAccessMode ごとの Codex 実行制御、特に repo write と pure oracle read の cwd・sandbox・追加読み取りパス制限を調べるとき。
- Codex 実行結果の output text/json/schema path、schema 状態ファイルの保存場所、protected diff 検査の有無に関するテスト期待を確認するとき。
- Codex TUI の失敗時表示、call log、非ゼロ終了、Codex CLI 未検出時の CmocError 変換を変更・検証するとき。
- run_tracked_codex_subprocess のプロセスグループ分離と tracking path の扱いを確認するとき。

## Do not read this when
- Codex runtime 以外の CLI サブコマンド、設定読み込み一般、git worktree 作成一般、または path model の仕様を調べたいだけのとき。
- Codex CLI や LLM の実際の出力品質、対話内容、モデル選択の妥当性を検証したいとき。
- 実装本文を修正する入口を探しているだけなら、runtime 実装や profile 生成実装の対象ファイルを先に読む方が適切なとき。
- テスト補助関数そのものの実装、fixture 作成、テスト用 executable 生成の詳細を調べたいだけのとき。

## hash
- 3664cb4c7d045f19509f2f5c4adcb12a79e2e2a658672d82733416dddd750d26

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
- agent prompt を構成する標準文書、routing、file access rule、各種 ACP builder parameter、structured output schema の生成結果を横断的に検証する realization test。
- prompt 構築まわりの回帰観点を一箇所に集め、render 結果、root token の保持、builder の file access mode・model 設定、schema と oracle source の一致、packaged layout からの import を確認する。
- 16,000 文字を超えるが、標準 prompt、routing、file access、builder parameter が最終 prompt の同じ読み取り文脈で組み合わさるため、分割せず凝集性を優先している。

## Read this when
- prompt builder の標準文書が期待する markdown 断片を含むか、routing rule や file access rule が complete prompt に組み込まれるかを確認したいとき。
- ACP builder parameter の model class、reasoning effort、file access mode、prompt 内容、structured output schema path の期待値を変更・検証するとき。
- apply fork、review oracle、session join、tui resolve parameter、indexing index entry など複数 builder をまたぐ prompt/schema 回帰を調べるとき。
- root token や work root placeholder の扱い、oracle source と realization 側 schema の一致、packaged layout での import 互換性に関わるテストを確認するとき。
- render_as_markdown の空行圧縮や code block 内空行保持など、StructDoc の markdown rendering の基本挙動を確認するとき。

## Do not read this when
- 個別 builder の実装詳細や prompt 文面の生成ロジックそのものを修正したいだけで、テスト期待値を確認する必要がないとき。
- 単一の structured output schema の定義内容だけを確認したい場合で、対応する schema JSON や oracle source を直接読む方が早いとき。
- routing 文書、file access rule、各 standard 文書の本文内容を理解したい場合で、生成結果のテストではなく標準文書の定義元を読むべきとき。
- 特定の CLI 挙動や外部コマンド実行結果を検証したい場合で、prompt builder や ACP parameter 生成に関係しないとき。

## hash
- 70de642673972d207931d96d713c329eaf69e223bc468b8bc8fa91b1ec76d87c

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
