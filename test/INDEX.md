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
- apply fork の CLI 経路と内部 body が、Codex 実行ループ、apply run の branch/state/worktree 更新、linked worktree 起点、設定読み込み失敗時の中断、.cmoc ignore 処理、.gitignore 編集対象化、target 正規化を期待どおり扱うことを検証する realization test。
- session fork 後に apply fork を実行したとき、apply state が completed になり、apply branch と run_id 別 worktree が作られ、旧 apply_worktree/apply_process_id/pid が残らず、所見列挙が呼ばれることを確認する。
- linked worktree 上で開始した session branch と HEAD commit を apply run の起点にし、apply worktree は linked worktree 配下ではなく cmoc 管理 worktree 配下へ作ることを確認する。
- apply fork が session 側の既存 .gitignore 表現を書き換えないこと、未 ignore の .cmoc は git info exclude で clean にすること、所見対象としての .gitignore は apply branch 側で編集できることを確認する。
- target 正規化について、root 直下 memo は除外しつつ入れ子の memo directory は残し、binary file も file 種別だけでは除外しないことを確認する。

## Read this when
- apply fork の外部挙動、state 遷移、apply branch 名、apply worktree 配置、apply_process pid の後始末に関するテスト期待値を確認したいとき。
- linked worktree から apply fork を走らせる場合の oracle snapshot commit、apply branch の開始 commit、worktree 配置の期待値を確認したいとき。
- apply fork 実行時の .cmoc ignore 処理、session 側 .gitignore の保持、git info exclude への追加、.gitignore 自体を所見対象として編集する挙動を確認したいとき。
- cmoc config が壊れている、または存在しない場合に、apply run の branch/state/pid を開始せず stdout にエラーを出す挙動を確認したいとき。
- apply fork の target 正規化で root 直下 memo、入れ子の memo directory、binary file、oracle 配下 file の扱いを確認したいとき。
- Codex 実行を fake に差し替えて apply fork の制御フローや副作用をテストする既存パターンを参照したいとき。

## Do not read this when
- apply fork の実装本体、永続 state の読み書き helper、git worktree 作成処理、Codex 呼び出し処理を変更したいだけで、テスト期待値ではなく実装詳細を確認したいとき。
- session fork、init、git helper、runner fixture など apply fork 以外の CLI テスト基盤そのものを調べたいとき。
- apply fork 以外の apply サブコマンド、review、oracle、path model などの仕様やテストを探しているとき。
- Codex CLI や LLM 出力品質そのものの検証方針を知りたいとき。この対象は Codex 実行結果を fake 化し、apply fork 側の制御と副作用だけを検証する。

## hash
- afa9543f71fb61a087b92aa30f464282ad3d4815a4d75b7a289e83836f07ff5d

# `test_apply_fork_report_cli.py`

## Summary
- apply fork の CLI 実行を通じて、所見列挙、適用、commit、変更要約、report 生成、session state 更新までの一連の制御を検証する realization test。
- 収束、未収束、error、変更ファイル再調査、未追跡ファイルの変更要約、編集禁止対象差分、rolling fork の対象選定を、同じ apply fork loop と report schema の観測結果として扱う。
- ファイル自体が大きい理由は、apply fork report の期待値と loop 制御の読み取り文脈を一箇所に保つためであり、分割すると期待値の文脈が分散するという責務境界にある。

## Read this when
- apply fork の report 出力、終了コード、収束・未収束・error 判定を変更または調査するとき。
- apply fork が Codex の所見列挙、所見適用、commit message 生成、変更要約生成をどの順に呼び、どの観測結果を report に反映するか確認したいとき。
- apply 後に変更された file を再調査する制御、特に INDEX.md を再調査対象から外す挙動を確認するとき。
- finding application が差分を作らない場合の再調査待ち、commit 抑制、apply branch の扱いを確認するとき。
- error report が commit 前の working tree 差分や未追跡 file を変更要約に含めるかを確認するとき。
- 編集禁止対象への差分を検出した場合の stdout、report、session state の error 反映を確認するとき。
- rolling apply fork が前回 apply join 後の変更だけを対象にするか確認するとき。

## Do not read this when
- apply fork の内部 helper 単体の純粋な実装詳細だけを確認したいときは、該当する実装 module を直接読む方がよい。
- apply fork 以外の apply join、session fork、init などの CLI 挙動そのものを調査するときは、それぞれの専用テストや実装を読む方がよい。
- Codex 実行結果 fake やテスト用 repository fixture の共通的な作り方だけを確認したいときは、共通 support 側を読む方がよい。
- report markdown の整形関数や差分収集 helper の局所的な仕様だけを確認したいときは、対象 helper の実装またはより小さい単位のテストを優先する。

## hash
- 2876ba06713f97e07fd4138dd41dd55d00dcb4501e016c9c42450671c6121b2f

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
- cmoc の `init` と TUI 起動直前の CLI 前処理について、利用開始直後に共有される外部挙動を検証する realization test。`.cmoc` の ignore 設定、既存 staged/unstaged 差分の保護、既定設定の作成と既存設定への同期、linked worktree での repository/runtime 準備、TUI の prompt 保存と Codex 起動 parameter 構築、Markdown prompt 解析の見出し構造を扱う。
- 16,000 文字を超えるが、初期化済み状態を読む文脈が分散しないよう、cmoc 初期化と対話起動前の repository/runtime 準備という同じ CLI 境界の回帰検証を一箇所にまとめている。

## Read this when
- `init` の外部挙動、特に `.cmoc` 配下を追跡対象から外す処理、`.cmoc` ignore の維持、初期化 commit の対象、sub command log の記録を確認または変更するとき。
- 既存の staged 変更や `.gitignore` の staged/unstaged 変更を、`init` が壊したり勝手に commit したりしないことを確認したいとき。
- 既定の設定ファイル生成、既存設定に対する default key の補完、人間が書いた設定値の保持を確認または変更するとき。
- linked worktree からの `init` または TUI 起動で、repository root と作業 worktree の `.cmoc`、`.gitignore`、log、schema、commit 対象がどこに作られるべきかを確認するとき。
- TUI が editor で作成した Markdown prompt から HTML comment を除去し、parameter 解決用 Codex 呼び出しと本体 TUI 用 Codex 呼び出しをどう組み立てるかを確認または変更するとき。
- TUI の resolved parameter から file access mode、model class、reasoning effort、structured output schema、extra read paths を構築する挙動を検証するとき。
- Markdown prompt parser が fenced code block 内の見出しを無視し、見出し前本文と階層構造を保持する挙動を確認または変更するとき。

## Do not read this when
- CLI 全体のコマンド定義や option 一覧を把握したいだけで、`init` と TUI 起動前処理の外部挙動を検証しないとき。
- Codex 実行 wrapper や AgentCallParameter の一般的な仕様だけを調べたいとき。
- `.cmoc` の path model や repository/worktree root 判定そのものの実装詳細を調べるときは、該当する実装または仕様を直接読む方がよい。
- TUI の画面描画、継続的な対話 UI、または Codex CLI の出力品質そのものを検証したいとき。
- Markdown 全般の parser 仕様を網羅的に調べたいとき。この対象は TUI prompt 分割に必要な見出し・本文・fenced code block の回帰だけを扱う。

## hash
- 84ead6e56fa7c20ea13f689db248fffa248f0b896e22402a301d2b00cf882174

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 実行系の realization test。`codex exec` と `codex tui` の起動引数、作業ディレクトリ、生成される Codex profile、構造化出力 schema の保存場所、呼び出しログ、終了コード異常、Codex CLI 不在時のエラーを検証する。
- ファイルアクセスモードごとの保護領域制御を、`.agents`、`oracle`、`memo`、追加 read path、pure oracle read の complete prompt 例外を含めて確認する。
- Codex subprocess を専用 process group で追跡し、追跡用 pid ファイルの既存内容を壊さず子プロセス情報を記録する制御も扱う。

## Read this when
- Codex CLI 呼び出し処理、Codex profile 生成、`--cd`、`--json`、`--output-last-message`、`--output-schema` などの実行引数を変更する。
- `FileAccessMode` と Codex 実行時 sandbox、writable roots、pure oracle read の作業ディレクトリ、repo worktree 配下での状態保存先を確認または変更する。
- Codex 実行後に `.agents`、`oracle`、`memo` などの保護領域変更を検出して拒否する処理や、そのエラー詳細・ログ出力を変更する。
- `run_codex_exec`、`run_codex_tui`、`run_tracked_codex_subprocess`、Codex subprocess の失敗処理、Codex CLI 不在時のエラー処理を変更する。
- Codex 呼び出しログや `SubcommandLogger` に記録される `codex_call` の status、returncode、call log path、console 表示を確認する。

## Do not read this when
- Codex 実行ではなく、通常の Git 操作、設定ファイル読み込み、path model、oracle 文書そのものの仕様だけを調べる。
- LLM の応答品質、prompt 内容の妥当性、または Codex CLI 自体の内部挙動を検証したいだけで、cmoc 側の呼び出し制御や保護領域検査を扱わない。
- 実装ファイルの責務や API 仕様を先に把握したい場合は、対応する runtime 実装や profile 生成実装を直接読む。

## hash
- c05b0118945c085da5cedbb414da2b2279334c007118e2388e78fda23022ae2d

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
- Codex exec が quota exceeded になった後の待機、quota availability probe、resume token による再開、token 不在時の再実行を外部挙動として検証する realization test。
- fake Codex 呼び出し列、call log、subcommand log、CODEX_HOME と cwd、並行実行時の代表 probe 共有、probe による .agents 変更検出を同じ retry 状態機械の観測点として扱う。

## Read this when
- quota exceeded 後の Codex exec retry 制御、probe 実行、resume と再実行の分岐を変更または調査するとき。
- Codex 呼び出しログ、subcommand log、stdout/stderr/prompt/output の記録内容、quota 待機中や復帰後の status を確認するとき。
- CODEX_HOME が相対パスの場合の実行 cwd、file access mode による codex --cd の向き先、probe 後の .agents 変更拒否を確認するとき。
- 複数の Codex exec が同時に quota exceeded になった場合に、quota availability probe を共有しつつ各呼び出しが resume される挙動を確認するとき。

## Do not read this when
- quota retry ではない通常成功時の Codex exec 引数構築、出力 JSON 読み取り、一般的な subprocess 実行だけを確認したいとき。
- Codex CLI や LLM 自体の出力品質、実際の quota 状態、外部サービスとの通信を検証したいとき。
- oracle file の正本仕様や設計意図を確認したいとき。
- retry 状態機械ではなく、個別 helper の単体的な実装詳細だけを調べたいとき。

## hash
- 384ace0d6b6e8dd3c53494b005fb7c0314bf2a87c2eef952c1a5ace3a2244bb0

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
- prompt part と AgentCallParameter builder の生成結果を横断的に検証する realization test。標準 prompt、routing、file access、各種 standard 文書、root token 解決、structured output schema、builder の model/reasoning/file access 設定が期待どおりに組み合わさることを確認する。
- prompt 構築の回帰観点を一箇所に集約し、render_as_markdown の整形、complete prompt への標準文書注入、apply fork・review oracle・session join・TUI resolve・indexing 用 builder の schema や実行パラメータを検証する入口になっている。

## Read this when
- prompt part の文言、StructDoc/StructCodeBlock の markdown render、または complete prompt の構成を変更し、その回帰テスト観点を確認したいとき。
- file access rule、routing rule、realization/review/apply/index entry standard の生成内容や、complete prompt にそれらを含める条件を変更するとき。
- apply fork、review oracle、session join、TUI resolve、indexing の AgentCallParameter builder が返す model class、reasoning effort、file access mode、prompt、structured output schema の期待値を確認するとき。
- oracle 側 JSON schema と realization 側 builder が参照する schema の一致を検証するテストを探しているとき。
- root token の実パス解決、cmoc 呼び出しメタデータ除去、code block 内外での置換挙動など、complete prompt の文字列変換仕様に関わる変更を行うとき。

## Do not read this when
- 個別 CLI コマンドの外部挙動や実行結果だけを確認したいとき。
- prompt 生成や ACP builder ではなく、低レベルの path model、git 操作、ファイルシステム操作そのものの実装を調べたいとき。
- 単一の schema ファイルの正本仕様内容だけを確認したい場合で、builder 経由の一致検証や prompt への組み込み条件を追う必要がないとき。
- テスト基盤全体の設定、pytest の起動方法、fixture 共有設計を調べたいだけのとき。

## hash
- bd173fa0a6e9294f9a11097899e9ba8a8894eaf2a2dcae635fcb15147acf421b

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
