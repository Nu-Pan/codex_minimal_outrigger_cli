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
- 基礎 runtime の共通契約を横断的に固定する pytest 群。root token/path 解決、run/work/repo root の境界、config 既定値と検証、CmocError の Markdown 表示、CLI error の stdout 変換、subcommand log、`.cmoc` ignore、FileAccessMode から sandbox/profile への変換、binary 判定をまとめて扱う。
- 個別サブコマンド単位ではなく、実行前提として一緒に崩れやすい runtime 境界を回帰確認する入口として位置づけられている。

## Read this when
- runtime 共通部品の変更が、root 解決、config、error 表示、logging、sandbox/profile 生成、状態 branch 名解析、binary 判定のいずれかに影響する可能性があるとき。
- CLI 起動前後の preflight、Click parse error、想定済み CmocError、subcommand log 書き込み、completion probe の副作用抑制を確認したいとき。
- FileAccessMode の値、Codex sandbox mode、Codex cwd、追加書き込み許可 path の制限を変更または調査するとき。
- linked worktree と main worktree の扱い、`<cmoc-root>` 形式の path 表示、`.cmoc` の gitignore 反映に関わる変更を行うとき。

## Do not read this when
- 特定サブコマンド固有の正常系・業務フロー・出力内容だけを調査する場合は、そのサブコマンドの専用テストを読む。
- oracle 正本仕様そのものを確認したい場合は、実装テストではなく対応する oracle file を読む。
- 個別 helper の内部実装だけを局所的に変更し、runtime 共通契約や CLI error/log/profile/path 境界に影響しないことが明らかな場合。

## hash
- 1568a8f2ed47acf34e472a66939bc7f7fdc8de0b49d01d1d76445452b97ec1c6

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
- Codex CLI 呼び出し層の realization test。`codex exec` と TUI 起動時の profile 生成、作業ディレクトリ、sandbox 設定、出力 schema の保存先、call log、エラー変換、`.agents` 変更拒否、Codex CLI 不在時の失敗を、stub 実行ファイルと一時 repo で検証する。
- 外部の Codex 実体や LLM 出力品質ではなく、cmoc が Codex subprocess をどう起動し、どの制御・ログ・許可領域チェックを行うかを確認する入口である。

## Read this when
- Codex CLI の `exec` または TUI 呼び出し引数、`--profile`、`--cd`、`--json`、`--output-last-message`、`--output-schema` の扱いを変更する時。
- file access mode ごとの sandbox profile、特に repo write と pure oracle read の cwd・読み書き権限設定を確認または変更する時。
- run worktree から呼び出した場合の schema state 保存先を、worktree 配下ではなく repo root 配下に置く挙動を確認する時。
- Codex subprocess の process group、pid tracking、call log、subcommand logger、console 出力、returncode 記録、失敗時の `CmocError` 化を変更する時。
- Codex 実行後に `.agents` 配下の変更を検出して拒否する挙動、または TUI 起動前の extra read path 許可領域チェックを変更する時。
- Codex CLI が見つからない場合や TUI が非ゼロ終了した場合のエラー文言・ログ生成を確認する時。

## Do not read this when
- Codex 実行層ではなく、通常の git 操作、repo 作成 fixture、設定ファイル読み込み一般、または path model の正本仕様だけを調べたい時。
- Codex CLI や LLM の応答内容そのものの品質・意味を検証したい時。この対象は stub subprocess を使い、cmoc 側の起動制御と副作用だけを扱う。
- CLI サブコマンド全体の利用者向け出力や argparse 定義を調べたい時。ここで扱うのは Codex runtime 呼び出し周辺の制御ロジックに限られる。
- oracle file の正本仕様を編集・確認したい時。この対象は realization test であり、正本仕様の代替ではない。

## hash
- 46625cac601c4315bb9a33806ff07085cc05cdfa6f0fcb2122adc43bcc68c7c0

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
- Codex CLI 実行ラッパーの retry 制御を検証する realization test。schema validation 失敗時の再実行、capacity エラー時の再実行、stdout JSONL 外に出た capacity/quota 文字列を retry 判定に使わないことを、偽の codex 実行ファイルとログ出力で確認する。
- 実行結果の JSON、呼び出し回数、call log、prompt/stdout log path、subcommand log の codex_call status・returncode・error detail を観測し、retry の外部挙動とログ記録の境界を確認する入口になる。

## Read this when
- Codex CLI 呼び出しの retry 条件、retry 後の成功扱い、または CmocError への失敗変換を変更する。
- schema validation retry、capacity retry、quota/capacity marker の判定元、または stdout JSONL の解釈を変更する。
- codex call log、prompt log、stdout log、subcommand log の記録内容や、retry ごとの log path の扱いを変更する。
- run_codex_exec の外部コマンド呼び出しをテスト上で置き換える fixture や helper の使われ方を確認したい。

## Do not read this when
- Codex CLI 実行と無関係な CLI サブコマンド、設定読み込み、path model、oracle/realization 分類の仕様を調べたい。
- retry ではない通常成功・通常失敗の基本挙動だけを確認したい場合で、より直接その観点を扱うテストがある。
- Codex CLI や LLM の出力品質そのものを評価したい。ここではラッパーの制御ロジックとログ副作用だけを検証している。

## hash
- ee15da0887d4878f996c9352e878cabccda604558cc4e7f34ecaae2df5879d20

# `test_indexing_cli.py`

## Summary
- indexing preflight と indexing サブコマンドが routing document を生成・更新・commit する外部挙動を検証する realization test。対象列挙、既存 hash の再利用、Codex によるエントリー生成、commit 対象の限定、linked worktree、dirty worktree の拒否、未初期化 repo の失敗、INDEX.md conflict 解決、semantic field validation、並列生成、root 直下 memo 除外と nested memo index 化を同じ routing 更新ワークフローの観測点として扱う。

## Read this when
- indexing CLI または indexing preflight の回帰テストを確認・変更したいとき。
- INDEX.md の生成・更新・commit 条件、既存 hash が fresh な場合の Codex 呼び出し抑制、malformed entry の再生成、entry semantic field の validation を調べたいとき。
- linked worktree や apply worktree 上で indexing がどの root・cwd・config を使うか、dirty worktree をどう拒否するかを検証したいとき。
- routing document 更新時の git 状態、commit 対象、INDEX.md conflict 解決、memo ディレクトリの index 対象境界をテストから確認したいとき。

## Do not read this when
- indexing の実装本体や helper の処理順を直接変更したいだけなら、対応する implementation を先に読む。
- Codex 実行基盤、ACP parameter、model config の一般挙動を調べたいだけなら、この CLI 境界テストではなくそれぞれの実装・設定定義を読む。
- routing document 以外のサブコマンド挙動、または indexing と無関係な git worktree 操作の仕様を調べたいだけなら、より直接のテストや実装へ進む。

## hash
- 91aa0b22dbcff027edeab27830f436ab0565b4956bc7153ba8565434389d94b6

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
- agent prompt 構成部品と ACP builder の生成結果を横断的に検証する realization test。標準 prompt、routing、file access、各種 standard、builder parameter、structured output schema の期待値が、最終 prompt や schema に正しく反映されることをまとめて確認する。
- prompt part の markdown render、root token 解決、cmoc 呼び出しメタデータ除去、file access mode ごとの文言、各 builder の model・reasoning・file access mode・schema path・prompt 内容を回帰検証する入口になる。

## Read this when
- agent prompt、routing rule、file access rule、各 standard 文書の render 結果や complete prompt への組み込み挙動を変更・確認したいとき。
- ACP builder が返す parameter の model class、reasoning effort、file access mode、prompt 文面、structured output schema path の期待値を変更・確認したいとき。
- apply fork、review oracle、session join、TUI parameter resolution、indexing index entry まわりの builder と schema の回帰テストを追いたいとき。
- structured output schema が oracle 側の schema 断片と一致しているか、jsonschema validation 可能な形になっているかを確認したいとき。

## Do not read this when
- 個別の prompt part や builder の実装詳細そのものを調べたいだけで、テスト期待値や回帰観点を確認する必要がないとき。
- 特定の oracle schema の正本内容を確認したいとき。このテストではなく対応する oracle 側の schema 本文を直接読む方がよい。
- prompt や ACP builder と無関係な CLI 挙動、永続状態、ファイル操作、UI 処理のテストを探しているとき。

## hash
- 81102fcbd1bd9f107f00779aa765d331239448a5ab49f0b94e77e466c847c8af

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
- session fork/join/abandon の CLI 回帰テストをまとめた realization test。session branch と session state のライフサイクルを軸に、状態ファイル生成・衝突時の保護、linked worktree 上の home branch/head、abandon/join 後の branch/state 更新、cleanup 失敗時の rollback、dirty worktree や不正 state の拒否、join conflict resolution とエラー出力先を外部挙動として検証する。
- 16,000 文字を超えるが、fork、join、abandon、linked worktree、state cleanup、dirty worktree 拒否が同じ branch/state fixture と状態遷移を共有するため、session CLI 回帰として一箇所に保つ意図を docstring で明示している。

## Read this when
- session fork が session branch と state file を作る条件、session-id 衝突時の retry/失敗、既存 state を上書きしないこと、corrupt state の扱いを確認・変更する時。
- session abandon が home branch へ戻ること、session branch を削除すること、state を abandoned にすること、home branch 欠落や cleanup 失敗時の復旧・出力を確認・変更する時。
- session join が session branch の変更を home branch に統合すること、join 後の state、session branch 削除失敗 warning、delete conflict resolution、oracle conflict resolution の Codex 実行 profile を確認・変更する時。
- session CLI が linked worktree で実行された場合に、main worktree ではなく実行中 worktree の branch/head を基準にする挙動を確認・変更する時。
- session CLI の失敗報告が stdout と stderr のどちらへ出るべきか、特に事前拒否と merge 後の unexpected error の境界を確認・変更する時。

## Do not read this when
- session 以外の CLI サブコマンド、または init/apply/review など別領域の外部挙動だけを調べる時。
- session の内部 helper の純粋な単体仕様だけを調べたい時。ただしその helper が CLI の fork/join/abandon 外部挙動に影響する場合は読む。
- session state schema の一般定義や path model の正本仕様を調べたい時は、まず対応する oracle file または実装本文を読む。
- Codex CLI や LLM の出力品質そのものを検証したい時。このテストは join conflict resolution の制御と副作用を stub で観測しており、生成品質は対象にしていない。

## hash
- 64e50fe8a7d228e149ac77ed9be6c668e1f4ae94a387dbf6736009b8c8e12a22
