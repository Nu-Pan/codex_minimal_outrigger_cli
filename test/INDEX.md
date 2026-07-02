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

# `test_acp_builder_parameters.py`

## Summary
- ACP builder が返す AgentCallParameter のモデル種別、reasoning effort、file access mode、prompt 文面、structured output schema 参照を検証する realization test。
- apply fork、file access rule violation recovery、TUI parameter resolution、index entry generation、review oracle finding、session join conflict resolution など複数 builder の外部挙動を横断的に確認する。
- oracle source 側の schema や builder と realization builder の対応関係を検証し、schema のコピーではなく正本参照に合っていることを担保する。

## Read this when
- ACP builder の prompt、実行パラメータ、structured output schema path の期待値を変更する。
- TUI resolve parameter の schema required 項目、enum、公開 export 名、埋め込む標準文書の範囲を確認する。
- review oracle finding 系 builder が oracle source の schema や oracle builder と一致するかを確認する。
- apply fork や session join の builder が `<repo-root>`、`<work-root>`、file access mode をどう扱うべきかをテストから確認する。

## Do not read this when
- 個別 builder の実装詳細だけを確認したい場合は、対応する実装モジュールを直接読む。
- oracle source の schema 定義そのものを編集・確認したい場合は、oracle 配下の該当 schema を読む。
- ACP parameter と関係しない CLI 挙動、path model、index entry 本文生成規則を調べる場合は、より直接のテストまたは実装へ進む。

## hash
- 07e66467d4cdb5147efa65f42cbb14819d94f70e782d5fc739e8fab4c2330269

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
- apply fork コマンドの CLI 経由の実行、Codex 呼び出し、session state 更新、apply branch/worktree 作成、設定読み込み失敗時の中断、.gitignore の扱い、対象 path 正規化を検証する realization test。
- apply fork が session branch と現在の HEAD を基準に apply run を開始し、完了時に一時的な pid や旧 apply worktree 表現を残さないことを確認する。
- realization file 判定に関わる memo、oracle、管理ディレクトリ、INDEX/AGENTS、binary file、tracked ignored file の対象選別を確認する入口になる。

## Read this when
- apply fork の外部挙動、state 遷移、apply branch 名、apply worktree 配置、Codex loop 呼び出し順を変更する。
- linked worktree 上で apply fork を実行する挙動や、oracle snapshot commit と apply branch の起点を確認する。
- apply fork 実行時の .cmoc ignore 保証、session 側 .gitignore の非破壊性、apply branch 側での .gitignore 編集可否を変更または検証する。
- apply fork の設定ファイル読み込みエラー時に apply run を開始しない挙動、標準出力へのエラー表示、pid/state/branch の未生成を確認する。
- apply fork の対象正規化で、root 直下 memo、管理 path、INDEX/AGENTS、oracle path、binary file、tracked ignored file の扱いを確認する。

## Do not read this when
- apply fork 以外のサブコマンドの CLI 挙動だけを確認したい。
- Codex 実行器そのものの統合挙動や LLM 出力品質を確認したい場合で、apply fork 側の呼び出し・状態更新は関係しない。
- path model や realization/oracle file の定義そのものを確認したい場合は、正本仕様側を先に読む。

## hash
- 8132fa30a1ec010f5fecea77ff23e4bf3b34c02c05eaad6deab39af8f9353f9b

# `test_apply_fork_report_cli.py`

## Summary
- apply fork の CLI 経由の挙動を検証する realization test。所見列挙、所見適用、commit、変更要約、report 出力、session state 更新、再検査、rolling apply fork の制御を一連の外部挙動として扱う。
- apply fork report の生成内容と収束判定、未収束判定、error 時の未 commit 差分要約、変更ファイル再調査、禁止領域汚染からの recovery を確認する入口になる。
- apply fork 用 AgentCallParameter builder が src のみの PYTHONPATH や packaged layout で import でき、oracle schema と標準 prompt を参照できることも検証する。

## Read this when
- `apply fork` の report 内容、終了コード、収束・未収束・error の扱いを変更または調査する。
- 所見適用後に変更された file を再調査対象へ戻す制御、新規 directory 配下の展開、最後の調査対象が空所見だった場合の収束判定を確認する。
- apply fork の変更要約で未追跡 file、削除済み tracked file、commit 前 working tree 差分をどう扱うかを確認する。
- apply fork が禁止領域を汚した Codex 実行を recovery し、許可差分だけを apply branch に commit する挙動を確認する。
- rolling apply fork が前回 apply join 後の oracle 変更だけを調査対象にする session state 更新を確認する。
- apply fork 関連の ACP builder、Structured Output schema path、標準 prompt 組み立て、packaged layout import を変更する。

## Do not read this when
- apply fork 以外の subcommand の CLI 挙動だけを調査する場合。
- report の表示内容ではなく、低レベルな git wrapper や共通 runtime Codex 実行処理だけを調査する場合。
- apply fork の所見列挙・適用 loop ではなく、個別 prompt 文面や schema 定義そのものを確認したい場合は、対応する builder または oracle source を直接読む。
- INDEX.md エントリー生成や routing 文書の仕様だけを確認する場合。

## hash
- f8dfe753b40a2eace94c5b42d13807d14e5d30c741119b8ecde6d319a502251b

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
- cmoc の基礎 runtime 契約を横断的に検証する realization test。root placeholder 解決、linked worktree 判定、run worktree 作成・削除の安全条件、config 既定値と型検証、CmocError の Markdown 表示、CLI error の stdout 化、subcommand log、`.cmoc` ignore、FileAccessMode と Codex sandbox profile、binary 判定など、個別サブコマンドより下位の共通実行前提をまとめて扱う。
- 16,000 文字を超えるが、共通 runtime fixture と root 状態を同時に読む必要がある basic runtime 回帰として凝集している。分割判断をする場合は、個別サブコマンドではなく共通 runtime 契約のまとまりが崩れないかを確認する入口になる。

## Read this when
- root placeholder、repo root、work root、run root、linked worktree の解決や拒否条件を変更する。
- CmocError、render_error、CLI 引数解析 error、想定済み CLI error の表示先や Markdown report 形式を変更する。
- SubcommandLogger、subcommand log の生成条件、pre-log check 失敗時の副作用を変更する。
- CmocConfig、config_from_dict、model class、reasoning effort の既定値や型検証を変更する。
- FileAccessMode、Codex sandbox mode、Codex profile の writable roots、extra writable/read paths、session join conflict 書き込み許可を変更する。
- `.cmoc` の gitignore 追加、run worktree の managed path 判定、worktree 削除安全条件を変更する。
- runtime content の binary 判定や、起動 wrapper の missing venv call stack 表示を変更する。

## Do not read this when
- 個別サブコマンド固有の業務ロジックだけを確認したい場合は、そのサブコマンドの実装または専用テストへ進む。
- oracle file の正本仕様本文を確認したい場合は、この realization test ではなく対応する oracle doc または oracle src を読む。
- INDEX.md エントリー生成やルーティング文書の形式だけを確認したい場合は、対象本文の責務確認に必要な範囲を超えてこのテスト全体を読む必要はない。
- 単一 helper の純粋な内部実装だけを変更し、root 状態、CLI 表示、sandbox profile、永続状態、git worktree 安全条件に影響しないことが明確な場合は、より近い単体テストを優先する。

## hash
- beb8337945c974d5562130ab2f25645b50b42534d3bad354a6e804fa0cc43c4a

# `test_cli_init_tui.py`

## Summary
- init と TUI 起動直前の CLI 前処理を外部挙動として検証するテスト。cmoc 初期化、.cmoc ignore、既存差分保護、設定既定値同期、linked worktree、Markdown prompt 整形、Codex TUI 起動 parameter 構築を同じ利用開始境界の回帰として扱う。

## Read this when
- `init` の git ignore 更新、.cmoc 配下の追跡解除、cleanup commit、既存 staged/unstaged 差分保護を変更・確認する。
- 初期設定ファイルの既定値生成、既存 human value を保持した設定同期、sub_command log の記録内容を変更・確認する。
- linked worktree での init/TUI の root/cwd、ignore、config/log/schema 保存先、git status への影響を確認する。
- TUI 起動前の editor 実行、HTML comment 除去、complete prompt 保存、resolve parameter の解釈、AgentCallParameter 構築を変更・確認する。

## Do not read this when
- 個別サブコマンドの本体処理や agent call 実行結果を確認したいだけで、init または TUI 起動前処理に関係しない。
- 設定値の定義元や prompt 構築仕様そのものを確認したい場合は、対応する oracle または実装側を直接読む。
- INDEX.md 生成規則や oracle/realization 標準の内容を確認したいだけで、この CLI 境界の回帰テストを見ない。

## hash
- b78e4d3a16f472b8ec6f743589c4e5f1fc8915248148f5d95c2f1a348d42db08

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI の exec/TUI 呼び出しをテストする realization test。Codex profile 生成、作業ディレクトリ、sandbox writable_roots、prompt/stdin/output/schema の受け渡し、process group tracking、欠落 CLI や非ゼロ終了時のエラー報告を検証する。
- agent call 後のファイルアクセス規則検査を扱い、readonly・realization write・repo write・pure oracle read 各 mode で、oracle/memo/.agents/.codex/.git、ignored file、temporary cache、venv、session join conflict 対象の差分を許可または拒否する境界を確認する。
- linked worktree での schema state 配置、repo log read 例外、TUI complete prompt の読み取り許可など、Codex runtime が work-root/repo-root/oracle-root を切り替える挙動の入口になる。

## Read this when
- Codex CLI の exec または TUI 起動引数、profile 生成、sandbox 設定、cwd、stdin/output/schema の扱いを変更する。
- agent call 実行後の file access violation 検出、復旧 retry、preexisting forbidden diff、ignored/untracked/cache/venv 差分の許可条件を変更する。
- PURE_ORACLE_READ、READONLY、REALIZATION_WRITE、REPO_WRITE の runtime 挙動や、extra_read_paths、extra_writable_paths、allow_oracle_conflict_writes の扱いを変更する。
- linked worktree 上での Codex runtime 実行、schema state の保存先、repo log prompt/read 例外、TUI complete prompt の扱いを確認する。
- Codex CLI が存在しない場合、または TUI が非ゼロ終了した場合の CmocError と console/log 出力を確認する。

## Do not read this when
- AgentCallParameter、FileAccessMode、ModelClass、ReasoningEffort そのものの型定義や意味だけを確認したい場合は、それらの basic 層を読む。
- Codex runtime の実装を直接変更したい場合は、まず runtime 実装側を読み、このテストは期待挙動の確認が必要になった時に読む。
- git repository fixture、Codex home fixture、stub executable 作成などテスト支援関数の詳細だけを確認したい場合は、support 側を読む。
- oracle file の正本仕様や path model の定義を確認したい場合は、oracle 側の文書または source を読む。

## hash
- 627eb1590ed92c3f709ba6db7df594f1996ae0b67d9597b489cfd75ff8569221

# `test_codex_runtime_home.py`

## Summary
- Codex CLI 実行時の Codex home 解決と事前検証を扱う realization test。環境変数未設定時の既定値、相対値の解決基準、プロファイル配置、呼び出しログへの記録、Codex CLI 起動前に失敗すべき認証環境不備を検証する。

## Read this when
- Codex CLI 呼び出しに渡す CODEX_HOME、プロファイル、作業ディレクトリ、呼び出しログの挙動を変更または確認したいとき。
- Codex home が存在しない、ディレクトリではない、認証情報がない場合のエラー文言や失敗タイミングを変更または確認したいとき。
- file access mode によって Codex CLI の実行 cwd が変わるケースで、相対 CODEX_HOME の解決挙動を確認したいとき。

## Do not read this when
- Codex CLI の標準出力イベント処理、capacity wait、一般的な agent call 結果処理だけを確認したいとき。
- Codex home ではなく、repository path、oracle path、run root、work root の一般的なパスモデルを確認したいとき。
- CLI 利用者向けコマンド定義や設定ファイル全体の schema を確認したいとき。

## hash
- b92995fbdd0a93c847ae8a31d4ea6534df7c8b4185810379c129ee1b456241d7

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex quota exceeded 後に、quota availability probe、resume token、再実行、call log、subcommand log、CODEX_HOME/cwd が同じ retry 状態機械として期待どおり連動することを検証する realization test。
- quota 待機から復帰する Codex exec の外部挙動を、単一呼び出し、resume token あり/なし、probe 失敗、並列呼び出し時の代表 probe 共有まで含めて確認する。

## Read this when
- Codex exec が quota exceeded を返した後の polling、probe、resume、rerun の挙動を変更または調査するとき。
- quota retry 中に記録される call log、subcommand log、prompt/stdout/stderr/output の保存先や status/purpose の期待値を確認するとき。
- CODEX_HOME が相対パスの場合の cwd 解決、PURE_ORACLE_READ 時の実行ディレクトリ、または probe が使う profile/argv/stdin を確認するとき。
- 複数の Codex exec が同時に quota exceeded になった場合に、probe を代表 1 回に共有し、各呼び出しが復帰または失敗する制御を確認するとき。

## Do not read this when
- 通常の成功する Codex exec 呼び出しだけを調べたいとき。
- quota retry と無関係な CLI 引数生成、設定読み込み、リポジトリ作成 fixture の詳細を調べたいとき。
- Codex CLI や LLM の出力品質そのものを評価したいとき。
- oracle file の正本仕様を確認したいとき。

## hash
- 0a30f0b70db0ab7bf8389f4f98b8e15ac849abe651f620a206f7d85d4c7fec75

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 実行ラッパーの retry 挙動を検証する pytest テスト。構造化出力の schema 不一致・JSON 解析失敗・capacity エラー時に再試行し、call log と subcommand log に期待する状態が記録されることを確認する。
- stdout JSONL 以外に出た capacity/quota 風の文字列を再試行条件として扱わず、通常の CLI 失敗として扱う境界も検証する。

## Read this when
- `run_codex_exec` の再試行条件、構造化出力検証、capacity/quota 判定、call log 記録、subcommand log の `codex_call` event を変更する時。
- Codex CLI の fake executable を使った retry 系テストの既存パターンを確認したい時。
- `AgentCallParameter`、`CmocConfig`、`SubcommandLogger` と `run_codex_exec` の結合テストを追加・修正する時。

## Do not read this when
- Codex CLI 呼び出しの通常成功系や引数組み立てだけを確認したい時は、より直接その挙動を扱う runtime テストを読む。
- repository fixture、Codex home setup、fake executable 作成 helper の実装を確認したい時は、テスト支援モジュールを直接読む。
- oracle file や INDEX.md の生成仕様を確認したい時は、該当する oracle doc または生成処理のテストを読む。

## hash
- 4756b71f801ab3d2753b1ac5ab73749a3bb338f0e6f7a177a3daa1c7451cab3b

# `test_indexing_cli.py`

## Summary
- INDEX.md 生成・更新、indexing preflight、indexing subcommand、INDEX.md conflict 解決の外部挙動を検証する回帰テスト群。
- 対象列挙、hash 再利用、Codex 生成、commit 対象、dirty worktree 拒否、linked worktree、空ディレクトリ、並列生成、memo 除外、symlink cycle 回避を routing document 更新ワークフローとしてまとめて扱う。

## Read this when
- indexing CLI が INDEX.md を生成・更新・commit する条件を確認したいとき。
- indexing preflight と通常の indexing subcommand で dirty worktree、linked worktree、repo config、commit 対象の扱いがどう違うかを確認したいとき。
- 既存 INDEX.md entry の hash 再利用、malformed entry の再生成、Structured Output schema 不一致の拒否を変更・検証するとき。
- INDEX.md conflict 解決、空ディレクトリへの INDEX.md 配置、並列生成、root 直下 memo 除外、入れ子 memo 対象化、directory symlink cycle 回避に関わる実装を変更するとき。

## Do not read this when
- INDEX.md entry の自然言語内容そのものを設計・更新したいだけで、CLI 境界や git 状態の回帰確認が不要なとき。
- routing document 生成に関係しない subcommand、設定、agent call、apply join の挙動を調べたいとき。
- 単体 helper の内部実装だけを確認したく、外部 CLI 挙動、commit、worktree、git conflict の観測が不要なとき。

## hash
- ba84ba2a5f8fac06dd16494e65b04728e1b72568d45ca51a5e25aa2604e2bf43

# `test_indexing_preflight.py`

## Summary
- Codex 実行前の indexing preflight が、exec/TUI 呼び出し前に INDEX.md 更新を実行し、必要な commit と worktree 選択を行うことを検証する realization test。
- repository lock 待機、index entry 生成や conflict resolution 用途で preflight を skip する条件も扱う。

## Read this when
- Codex 呼び出し前に indexing preflight が走る順序、commit、clean worktree を確認・変更する。
- cwd が別 worktree 配下にある場合、root ではなく cwd 側 worktree を index 更新対象にする挙動を確認・変更する。
- indexing lock の排他待機や、特定 purpose で preflight を skip する条件を確認・変更する。

## Do not read this when
- INDEX.md の本文生成ロジックやエントリー内容の仕様を確認したい場合。
- Codex 実行ラッパーではなく、個別の git helper や repository fixture の詳細を確認したい場合。
- oracle file の正本仕様や INDEX.md ルーティング規則そのものを確認したい場合。

## hash
- 5549e75d6493464e59f5f4cb68232c1fbd9fc7d03b85ee5f6cb6ea3ad4e04099

# `test_packaged_import.py`

## Summary
- packaged layout から review oracle enumerate builder を import できることと、packaging 設定が oracle package を期待した配置で公開していることを検証するテスト。
- 一時的な import 環境を組み立て、builder が schema path と prompt を正しく返せることをサブプロセスで確認する。

## Read this when
- packaged layout、setuptools package-dir、oracle package の import 境界を変更する。
- review oracle enumerate builder の依存関係、schema 参照、prompt 組み立てが配布後の import 環境で壊れていないか確認する。
- oracle src と realization src の配置分離に関わるテスト失敗を調査する。

## Do not read this when
- builder の prompt 本文や schema 内容そのものの詳細仕様を確認したい場合。
- 通常の CLI 動作、入出力、状態管理など packaged import 境界と無関係な挙動を調査する場合。
- 単体の helper ロジックを直接検証するテストを探している場合。

## hash
- cccc21d8925cdcc0798ceaddea1bf75e25fbadf671e8b6ee5e76317db75fb27f

# `test_prompt_parts.py`

## Summary
- 標準 prompt parts と complete prompt の組み立て結果を検証する realization test。各 standard builder が期待する見出し・本文断片を返すこと、complete prompt が指定された standard 群・routing rule・file access rule・root placeholder を適切に含めるまたは省くことを確認する。

## Read this when
- prompt parts の出力内容、見出し、含まれるべき語句のテストを確認・変更する。
- complete prompt が routing rule、file access rule、各種 standard、補助 prompt、root placeholder をどう組み込むかの期待挙動を確認・変更する。
- file access mode ごとの prompt 文言や、standard の既定での省略・明示指定時の追加に関するテストを探している。

## Do not read this when
- prompt parts や complete prompt の実装を変更したいだけで、テスト期待値を確認する必要がない場合は、対応する実装側を直接読む。
- StructDoc や markdown rendering の汎用仕様を確認したい場合は、その構造化文書処理の実装やテストを読む。
- oracle file の正本文言そのものを確認したい場合は、対応する oracle 側の文書または生成元を読む。

## hash
- b9fef4ddaeb2f0e1b881f9a3685913297160ea4124bfa48ab10ce916c6c54096

# `test_review_oracle_cli.py`

## Summary
- review oracle コマンドの CLI 経由の外部挙動を検証する realization test。対象 oracle file の列挙、report 生成、所見の列挙・検証・judge・merge、上限到達時や処理失敗時の report、review 用 worktree からの INDEX.md 変更の取り込み、非 INDEX.md 差分の拒否を扱う。

## Read this when
- review oracle の report 形式、件数、section 順、accepted/rejected finding の出力、error/no_targets/fatal/ok verdict を変更または確認したいとき。
- review oracle が full scope または session scope でどの oracle file を対象にするかを変更または確認したいとき。
- review oracle の所見 loop、challenger/advocate/judge/merge の制御、prompt に渡す既存所見の範囲、merge operation の契約を変更または確認したいとき。
- review oracle が linked worktree、session branch、review worktree、join commit、INDEX.md 変更の merge conflict をどう扱うかを変更または確認したいとき。
- review oracle 実行中に Codex が作成した差分のうち、INDEX.md だけを許し、それ以外を拒否して元 worktree を汚さない挙動を確認したいとき。

## Do not read this when
- review oracle 以外の review サブコマンドや通常の session 操作だけを扱うとき。
- 実装内部の helper 分割や型定義だけを確認したく、CLI 実行結果、report 内容、git/worktree 副作用を検証する必要がないとき。
- oracle file の正本仕様本文を確認したいとき。

## hash
- 1a8726db12b961d86532ae2594f48bb2d46607622497863717b193de359e1c47

# `test_session_cli.py`

## Summary
- session fork、join、abandon の CLI 回帰テストをまとめる。session branch と session state のライフサイクル、linked worktree 上の挙動、状態 cleanup、dirty worktree や壊れた state の拒否、join 時の conflict 解決とエラー出力先を外部挙動として検証する。
- 16,000 文字を超えるが、同じ session 状態遷移と branch/state fixture を共有する観測点を一箇所に集めたテストファイルである。

## Read this when
- session fork が session branch と state を作成する挙動、session-id 衝突時の retry や既存 state 非破壊を確認・変更するとき。
- session abandon が home branch へ戻る挙動、state を abandoned にする挙動、session branch 削除、cleanup 失敗時の rollback、home branch 不在時の失敗出力を確認・変更するとき。
- session join が session branch の変更を home branch へ統合する挙動、branch 削除可否、state 更新、linked worktree 上の current branch 維持を確認・変更するとき。
- session join の conflict 解決で Codex 実行 profile、oracle conflict 書き込み許可、delete conflict の staging、conflict marker 検出を確認・変更するとき。
- session 系 CLI のエラー報告が stdout と stderr のどちらへ出るべきかを確認・変更するとき。
- session state file の必須 field 検証や壊れた state への拒否挙動を確認・変更するとき。

## Do not read this when
- session コマンド以外の CLI 外部挙動だけを確認する場合。
- session fork、join、abandon の内部 helper 単体の詳細だけを確認したい場合。ただし CLI から見える branch/state 副作用との整合が必要なら読む。
- session と無関係な path model、oracle 文書構成、設定読み込み、一般的な git helper の挙動だけを確認する場合。

## hash
- 80a2286a0d351566ca7e0266cd40874ac259773c4ae2b8f9d3c48f1bda09f850

# `test_struct_doc_rendering.py`

## Summary
- StructDoc の Markdown renderer が本文中の連続空行を正規化する挙動を検証する単体テスト。通常テキストとコードブロックを対象に、過剰な空行が折りたたまれ、期待される Markdown 文字列になることを確認する。

## Read this when
- StructDoc の Markdown 出力で空行の扱いを変更・確認したいとき。
- 通常テキストまたはコードブロック内の連続空行がどのように描画されるべきかをテストから確認したいとき。
- render_as_markdown の整形挙動に関するテストを追加・修正したいとき。

## Do not read this when
- StructDoc のデータ構造そのものや renderer 全体の実装を確認したいときは、実装側を読む。
- Markdown renderer 以外の prompt builder 分割根拠や正本仕様を確認したいときは、対応する oracle 側の文書を読む。
- CLI 挙動、ファイル操作、永続状態など StructDoc の Markdown 整形と無関係な挙動を調べたいとき。

## hash
- 51580019f3a5f35c894b459980668eec4b098eecee22f1645f571c7c2084f811
