# `_support.py`

## Summary
- CLI テストで使う最小 Git リポジトリ、認証済み Codex home、偽の Python 実行ファイル、apply 用 worktree パス解決などを用意するテスト補助関数をまとめる。
- Git コマンド実行や現在ブランチ取得を通じて、テスト内の Git 状態確認と fixture 構築を支える共有入口として位置づけられる。

## Read this when
- CLI テストで一時 Git リポジトリを作成し、初期 commit 済みの状態や oracle 配下の tracked/ignored ファイルを準備する方法を確認したいとき。
- テストから Git コマンドを実行する helper、現在ブランチ名の取得、または apply の session state から worktree パスを導く処理を使う・変更するとき。
- Codex home の環境変数設定や fake external command 用の実行可能 Python スクリプトを、テスト fixture として用意する箇所を探すとき。

## Do not read this when
- 個別サブコマンドの期待挙動や assertion 内容を確認したいだけで、共有 fixture や helper の実装を変更しないとき。
- プロダクト本体の CLI 実装、状態管理、path model、oracle 仕様を調べたいとき。
- pytest や Typer のテスト runner の利用箇所そのものではなく、特定テストケースの入力・出力・失敗条件を確認したいとき。

## hash
- 8c09c548f4da0311169d9185be843e85179ae5fd86b54b1709052e34000c6938

# `test_apply_abandon_cli.py`

## Summary
- active apply run を破棄する CLI 操作について、cleanup、状態更新、実行位置の扱い、running process 停止を外部挙動として検証する realization test。
- apply worktree と apply branch の削除、欠損時 warning、running 状態の process 停止、pid 再利用や終了済み process の扱い、linked worktree からの abandon 境界を同じ state fixture 文脈で扱う。
- 16,000 文字を超えるが、active apply run の abandon 成功・警告・失敗条件を一箇所で確認するための凝集したテスト群として位置づけられている。

## Read this when
- apply abandon の CLI 挙動、出力、終了コード、state cleanup、worktree/branch 削除条件を変更または確認したいとき。
- running 状態の apply process を abandon 前に停止する制御、process id ファイル削除、stale pid や終了済み process の扱いを確認したいとき。
- apply worktree 上または linked session worktree 上から abandon を実行した場合の cwd 復帰、repo state 参照、stale apply branch 拒否の挙動を確認したいとき。
- apply abandon に関するテスト分割・統合を検討しており、この大きなテストファイルが一つの責務に閉じている理由を確認したいとき。

## Do not read this when
- apply run の作成、Codex 実行、fork 成功時の生成物そのものを確認したいだけのときは、apply fork 側のテストや実装を直接読む。
- session fork、repository 初期化、git helper fixture の一般的な挙動を調べたいだけのときは、対応する session/init/support 領域を読む。
- apply abandon の内部実装だけを局所的に変更したいが、CLI 外部挙動や process 停止境界の確認が不要なときは、実装モジュールから読み始める。
- oracle の正本仕様断片を確認したいときは、この realization test ではなく oracle 配下の該当文書を読む。

## hash
- f5be2a8d0509ec4c2691f238b6b586666419300c2717b5f00384891207deee49

# `test_apply_fork_cli.py`

## Summary
- apply fork の CLI 経路を対象にした realization test。Codex 実行を fake に差し替え、apply run の開始・完了、session state、apply branch、worktree 配置、pid/state cleanup、所見列挙ループなどの外部挙動を検証する。
- linked worktree 上での session branch/HEAD の扱い、session 側 .gitignore の保持、追跡済み .cmoc に対する拒否、config 読み込み失敗時に apply run を開始しないこと、所見対象としての .gitignore 編集、apply target 正規化で root 直下 memo だけを除外することを扱う。

## Read this when
- apply fork コマンドの実行フロー、Codex 呼び出し、所見適用ループ、commit summary/message 周辺の挙動を変更または検証するとき。
- apply fork が session state の apply 欄、apply branch、oracle snapshot commit、apply worktree path、pid file cleanup をどう更新するべきか確認したいとき。
- linked worktree から apply fork を実行した場合の開始 commit、branch、worktree 配置に関するテスト期待値を確認するとき。
- apply fork と .gitignore/.cmoc の関係、特に session 側 .gitignore を書き換えない制約や、追跡済み .cmoc を拒否する挙動を確認するとき。
- apply fork の target 正規化で root 直下 memo を除外し、入れ子の memo directory を対象に残す境界を確認するとき。

## Do not read this when
- apply fork 以外の apply サブコマンド、review、session fork、init などの個別 CLI 挙動だけを調べるとき。
- Codex CLI や LLM 出力品質そのものを検証したいとき。このテストは Codex 実行を fake にして apply fork 側の制御と副作用を検証する。
- oracle file の正本仕様を確認したいとき。このファイルは realization test であり、仕様判断の根拠は対応する oracle file を優先する。
- root 直下 memo の読み書き禁止そのものや、INDEX.md 生成ルールを調べるとき。ここで扱うのは apply target 正規化の境界だけである。

## hash
- a811a856ca06368967ed5065ac684a9014ef2778cf20b285943ed2ef08bee58b

# `test_apply_fork_report_cli.py`

## Summary
- apply fork の CLI 実行を通じて、所見列挙から適用、commit、変更要約、report 生成、session state 更新までの制御を検証する realization test。収束、未収束、error、dirty file 再検査、編集禁止対象の検出、rolling fork の対象選定を、同じ loop と report schema の観測結果として扱う。
- 16,000 文字を超えるが、責務は apply fork report と再検査制御の検証に閉じており、期待値の文脈を一箇所に保つために分割しない意図が docstring に明示されている。

## Read this when
- apply fork の CLI 終了コード、result label、report の内容、変更要約、commit message、session state 更新の期待挙動を確認・変更するとき。
- apply fork が dirty file を再検査する条件、再検査対象から除外される対象、最後の調査対象が空所見だった場合の収束判定を確認するとき。
- apply fork 中の no-op 適用、編集禁止対象への差分、未 commit 差分を含む error report の扱いを確認するとき。
- apply join 後の rolling apply fork がどの差分だけを調査対象にするかを確認するとき。

## Do not read this when
- apply fork の内部 helper の純粋な単体ロジックだけを確認したいとき。CLI 実行後の外部挙動や report 観測を伴わないなら、実装側またはより小さい単位のテストを読む方が直接的。
- apply fork 以外の subcommand、一般的な session fork/join、初期化処理そのものの挙動を調べたいとき。
- Codex 実行結果の品質や LLM 出力内容そのものを評価したいとき。この対象は fake 応答を使って apply fork 側の制御と出力を検証している。

## hash
- 088e836a2c195117587b48262890c4fb5deec723a260090ccbb7fcc9fdcb1aca

# `test_apply_join_cli.py`

## Summary
- apply run を session へ join する CLI 外部挙動を検証する realization test。成功時の apply worktree と branch の cleanup、session state 更新、report 生成を扱う。
- apply join を session 側または apply worktree 側から実行した場合の挙動、stale apply branch の拒否、dirty worktree の拒否、想定外差分や merge conflict の検出と report 内容をまとめて確認する。
- 16,000 文字を超えるが、apply join の成功条件と拒否条件を同じ fixture と git 状態の文脈で読む必要があるため、一箇所に凝集している。

## Read this when
- apply join の CLI 挙動、終了コード、標準出力、report 生成、state 更新、apply worktree と branch の後片付けを変更または確認するとき。
- apply join が dirty apply worktree、stale apply branch、想定外の apply 差分、未解決 merge conflict をどう拒否するかを確認するとき。
- apply worktree 内から apply join を実行した場合の cwd 復帰、ログ保存先、cleanup 可否を調べるとき。
- INDEX.md の競合解決や .gitignore 変更のように、apply join が許容または自動解決する差分境界を確認するとき。

## Do not read this when
- apply fork 単体、session fork 単体、init 単体の基本挙動だけを確認したいとき。
- join 後の report 文面や state 副作用ではなく、内部 helper の純粋な単体ロジックだけを調べたいとき。
- Codex 実行結果の品質や LLM 出力内容そのものを検証したいとき。
- apply join 以外のサブコマンドや、oracle file の正本仕様本文を探しているとき。

## hash
- a00146402c5b62a4c89e13ef4e5f95b5d6859651f0f141f368983cf8063f2f78

# `test_basic_runtime.py`

## Summary
- cmoc の基本的な実行時挙動を横断的に検証する realization test。パスモデル、run/work/repo root 判定、設定初期値、構造化エラー出力、セッション branch 形状、CLI エラー出力、補完プローブ時の副作用抑止、.cmoc の gitignore 反映、file access mode と sandbox mode の対応、バイナリ判定、Codex profile の file access 制約を扱う。
- 単一機能の詳細テストというより、runtime 周辺の公開挙動と制御ロジックが基本契約を満たすかを確認する入口になる。

## Read this when
- runtime、path model、worktree/root 判定、構造化エラー表示、CLI preflight/parse error、gitignore 更新、file access mode、sandbox 権限、Codex profile 生成の基本挙動を変更・調査する。
- CLI エラーが stdout に出ること、補完プローブで preflight や .cmoc/.gitignore 生成が走らないこと、work root 以外での実行拒否など、利用者から見える失敗時挙動を確認したい。
- memo/oracle/.agents などの read/write/read_only/deny_read 制約や、FileAccessMode ごとの profile・sandbox_workspace_write の期待値を確認したい。
- セッション branch 名や apply branch 名の不正形状を拒否する状態管理ロジックの基本テストを探している。

## Do not read this when
- 個別サブコマンドの正常系ワークフロー、プロンプト生成、ログ生成、GitHub 連携など、このファイルに現れない機能領域の詳細テストを探している。
- oracle の正本仕様断片そのものを確認したい場合。このファイルは realization test であり、仕様の根拠としてではなく実装挙動の検証として読む。
- 特定の helper や module の実装責務を理解したいだけで、既に対象実装ファイルが分かっている場合。まずその実装本文を読む方が直接的。

## hash
- cf7cb1f76caa4fbd874fb65541d7bac601d27afad075e9b970bfcce67bdb2bbc

# `test_cli_init_tui.py`

## Summary
- CLI の初期化処理と対話起動処理に関する realization test。初期化時の `.cmoc` 配下の追跡解除、`.gitignore` への無視設定、既存 staged/unstaged 変更の保全、linked worktree での保存先や commit 対象、既定設定 JSON の生成・同期を検証する。
- 対話起動では、エディタで編集された依頼文から解決用パラメータを作り、HTML コメント除去後の完了プロンプトを保存し、Codex TUI 起動へ model class・reasoning effort・file access mode・追加 read path を渡す制御を検証する。
- Markdown 依頼文 parser について、fenced code block 内の見出し風テキストを見出し扱いしないことと、見出し前の preamble を本文として保持することを検証する。

## Read this when
- `init` サブコマンドの Git 操作、`.cmoc` 無視設定、初期 commit、既存 index/worktree 状態の保全、linked worktree 対応を変更・調査する。
- `.cmoc/config.json` の既定値生成、既存設定との同期、手動設定値を上書きしない挙動を変更・調査する。
- `tui` サブコマンドのエディタ起動、依頼文整形、パラメータ解決用 Codex 呼び出し、Codex TUI 呼び出し、ログ保存先、linked worktree での root/cwd/schema/log の扱いを変更・調査する。
- Markdown プロンプトを見出し単位に分解する parser の挙動、特に fenced code block と見出し前本文の扱いを変更・調査する。

## Do not read this when
- 個別サブコマンドに依存しない CLI 登録や Typer の一般的な entrypoint だけを確認したい。
- Git 操作や `.cmoc` 状態に関係しない純粋な設定 loader、schema 定義、モデル enum の詳細だけを確認したい。
- Codex CLI やエディタ実行そのものの外部品質、LLM 出力内容の妥当性を検証したい。
- Markdown parser 全般の網羅仕様を探しており、fenced code block 内見出しと preamble 保持以外の構文を扱うテストが必要である。

## hash
- c1265830784b4cbbcfcbda1b16f91cedf1e5c9880f77122e02d39be58637340f

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 呼び出しを包む実行系の realization test。`codex exec` と TUI 起動が、プロンプト受け渡し、生成 profile、`CODEX_HOME`、sandbox 設定、schema 保存先、実行 cwd、標準出力・標準エラーのログ分離、call log、subcommand logger、コンソール表示、repository config の反映を期待どおり扱うことを検証する。

## Read this when
- Codex CLI を起動する runtime 実装、特に exec 呼び出し、TUI 呼び出し、profile 生成、sandbox workspace 設定、`CODEX_HOME` 引き継ぎ、ログ保存、schema 保存先、repository config 読み込みを変更する時。
- 外部 `codex` コマンドを fake executable や monkeypatch で置き換え、引数・stdin・cwd・環境変数・副作用を確認する realization test の書き方を確認したい時。
- `.cmoc` 配下の Codex call log、prompt/stdout/stderr log、schema state、subcommand logger event、コンソール要約表示の期待値を確認したい時。

## Do not read this when
- Codex runtime の実装仕様ではなく、oracle file に書かれた正本仕様断片を確認したい時。
- Codex CLI 呼び出し以外のサブコマンド、Git 操作、path model、設定 schema 全体、または一般的な test fixture の責務を調べたい時。
- LLM の応答品質や実際の Codex CLI の実行結果そのものを検証したい時。

## hash
- 3af4dab0d27fed1143fe0c79c404a6ec0d70fc44bfaad74d9acc706faff0a7b4

# `test_codex_runtime_home.py`

## Summary
- Codex CLI 実行ラッパーが利用する Codex home の決定・検証を確認する realization test。環境変数未設定時の既定 home、相対パス指定の保持と解決、存在しない home・ファイルである home・認証情報欠落を Codex CLI 起動前にエラーにする挙動を扱う。
- fake の Codex 実行ファイルで呼び出し時の環境変数と引数を記録し、実行結果に含まれる Codex home、profile 配置、call log の内容が期待どおりかを検証する。

## Read this when
- Codex CLI 呼び出し前に CODEX_HOME をどの値へ設定するか、未設定時にどの home を使うかを変更・確認する時。
- Codex home の存在確認、ディレクトリ種別確認、auth.json 必須チェック、またはそれらの CmocError の summary・detail・next_actions を変更する時。
- run_codex_exec の戻り値に含まれる codex_home、profile_path、call_log_path と Codex CLI へ渡す profile 引数の関係を確認する時。

## Do not read this when
- Codex CLI の標準入出力プロトコル、turn.completed 以外のイベント処理、または LLM 応答品質の検証を調べたい時。
- Codex home とは無関係な AgentCallParameter のモデル種別、reasoning effort、ファイルアクセスモードの変換だけを調べたい時。
- リポジトリ作成 helper や fake 実行ファイル生成 helper の実装詳細を調べたい時。

## hash
- b4c26ae1f025d3687713c3ca03063e1f18042933100f15eeadb4bd2979c04b1d

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex 実行がクォータ超過で失敗した後、クォータ availability probe を挟んで再試行または resume し、最終結果・呼び出しログ・サブコマンドログ・コンソール表示を正しく扱うことを検証する realization test。
- 偽の Codex 実行ファイルを用いて、初回失敗、probe 成功、resume 成功、resume token 不在時の通常再実行、並列実行時の代表 probe 共有という制御フローを外部挙動として確認する。

## Read this when
- Codex CLI 呼び出しで quota exceeded を検出した後の待機、probe、resume、再実行の挙動を変更または調査するとき。
- Codex 実行ログの purpose、status、argv、profile、標準出力ログ、prompt ログ、output path、call_log_path の記録仕様を確認したいとき。
- 複数スレッドから同時に Codex 実行が quota exceeded になった場合、probe が重複せず代表 1 回だけ実行される制御を確認したいとき。
- CODEX_HOME や PATH 上の codex 実行ファイルを差し替えたテスト fixture の使い方を参考にしたいとき。

## Do not read this when
- 通常の Codex 実行成功パス、プロンプト組み立て、モデル・sandbox・承認設定など、quota retry 以外の引数生成を調べたいとき。
- 実際の Codex CLI や LLM の出力品質そのものを検証したいとき。
- oracle file の正本仕様を確認したいとき。この対象は実装側のテストであり、正本仕様ではない。

## hash
- 52577c161c22ef63a8d344b843647b0ed4fed140933e00a37c90413103f61047

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 実行ラッパーのリトライ制御を検証する realization test。スキーマ検証失敗後の再試行、capacity エラー時の再試行、JSONL 外に出た capacity/quota 文字列をリトライ条件として扱わない境界を、偽の実行ファイルとログ副作用で確認する。
- 成功時の出力 JSON、呼び出し回数、call log の保存内容、subcommand log の codex_call status と error 情報が、リトライ経路ごとに期待どおり記録されることを担う。

## Read this when
- Codex CLI 呼び出し処理のリトライ条件、再試行回数、capacity/quota 判定、またはスキーマ検証失敗時の再実行を変更する。
- Codex CLI 呼び出しログ、stdout/prompt/output の個別ログ、call log path、subcommand log の codex_call status を変更する。
- Codex CLI の stdout JSONL イベントからエラーを判定する範囲と、stderr や通常 stdout の文字列をどう扱うかを確認する。

## Do not read this when
- Codex CLI 呼び出し以外のサブコマンド、設定読み込み、パスモデル、または oracle 文書の仕様整理だけを扱う。
- リトライ制御やログ副作用に関係しない純粋なプロンプト生成、ファイルアクセスモード、モデル選択の実装だけを変更する。
- 実際の Codex CLI や LLM の出力品質そのものを検証したい場合。

## hash
- 2ce4974d0be685b2ff0a359481e956fab34aebe39c7e4bcae12e7ce4dc5bcfc8

# `test_indexing_cli.py`

## Summary
- indexing サブコマンドとその周辺処理の realization test。生成エントリーの構造化出力利用、コミット対象の限定、既存 hash による再生成スキップ、未初期化・未コミット差分・worktree・repo config の扱い、競合解消、エントリー描画時の入力検証、階層更新時の並列生成と memo 除外境界を検証する。

## Read this when
- indexing サブコマンドの起動条件、失敗時メッセージ、作業ツリーの清潔性チェック、生成後コミットの挙動を変更する。
- Codex によるエントリー生成、構造化出力 schema の利用、生成済み hash に基づく再生成判定、壊れた既存エントリーの再生成を変更する。
- linked worktree や apply 用 worktree での indexing 実行、repo 側 config の参照、生成先 root の決定を変更する。
- INDEX 系の競合解消、コミット対象を index path のみに限定する処理、非 index 差分を残したまま preflight で index だけを commit する処理を変更する。
- エントリー描画で必須 semantic field を検証する条件、空文字・非文字列・欠落をエラーにする条件を変更する。
- 階層内の sibling entry 生成を並列化する処理、root 直下 memo を除外しつつ nested memo を indexing 対象にする境界を変更する。

## Do not read this when
- indexing とは無関係なサブコマンド、設定読み書き、git helper、CLI runner の一般的な挙動だけを調べる場合。
- Codex 実行 wrapper や構造化出力 schema の実体を確認したい場合は、対応する実装または schema 定義を直接読む。
- path 用語、oracle/realization の正本仕様、ルーティング文書の作成規則を確認したい場合は、仕様文書側を読む。
- 個別の indexing 実装詳細を追う場合は、このテストで期待される外部挙動を確認した後に実装ファイルを読む。

## hash
- 5638f4b29738202c15f91e148bfdb9355d74671c6a5c6b46ea9788892bf0d089

# `test_indexing_preflight.py`

## Summary
- Codex 実行・TUI 起動の直前に INDEX 更新を走らせる preflight 制御を検証する realization test。
- preflight が対象 worktree を選ぶこと、生成された INDEX 更新を cmoc indexing コミットとして残し作業ツリーを清潔に戻すこと、既存のリポジトリ単位ロックを待つこと、INDEX エントリー生成や競合解決の目的では preflight をスキップすることを扱う。
- 実際の Codex 呼び出しや INDEX 生成は monkeypatch で差し替え、git worktree、lock file、呼び出し順、コミット履歴、副作用を観察して制御ロジックを確認する。

## Read this when
- Codex 実行前に INDEX 更新を自動実行する制御を変更・調査するとき。
- preflight が root と cwd のどちらの worktree を更新対象にするかを確認するとき。
- INDEX 更新のコミット作成、作業ツリー清掃、またはリポジトリロック待機の挙動を変更するとき。
- Codex 呼び出しの purpose に応じて indexing preflight を実行またはスキップする条件を変更するとき。

## Do not read this when
- INDEX の本文生成内容、エントリー文章、差分解析そのものを確認したいとき。
- apply join の通常の競合解決処理や fork refine の詳細挙動を調べたいだけのとき。
- Codex CLI や TUI の実プロセス起動方法、モデル指定、ランタイム統合の一般仕様を調べたいとき。
- ロックの低レベル実装だけを調べたい場合で、preflight からの待機制御に関心がないとき。

## hash
- 1e43cf0d39575b2dffeea90d89f05e0c252de3a1a50fe6eb29891fc5fe95558d

# `test_prompt_parts.py`

## Summary
- prompt part と ACP builder が生成する StructDoc、markdown render、complete prompt、file access rule、各種 builder parameter、structured output schema の期待値を横断的に検証する realization test。
- 標準 prompt、routing、file access、review/index/realization standard、TUI parameter、apply fork、review oracle、session join など、最終 prompt と schema の組み合わせに関する回帰観点を一箇所に集約している。
- 16,000 文字を超えるが、共通の render/schema 期待値を同じ読み取り文脈で追うために凝集させていることが冒頭で説明されている。

## Read this when
- prompt part の markdown 出力、空行の畳み込み、code block rendering、standard 文書の必須文言に関するテスト期待値を確認したいとき。
- complete prompt が routing rule や各 standard をどの条件で含むか、aux prompt の文面をどう保持するかを確認したいとき。
- file access mode ごとの prompt 文言、builder parameter の model class、reasoning effort、file access mode、schema path の期待値を調べたいとき。
- apply fork、review oracle merge finding、session join conflict resolution、TUI resolve parameter、indexing index entry の parameter builder と structured output schema の回帰テストを確認したいとき。
- 大きなテストファイルを分割すべきか判断する際に、このテストが単一責務としてまとまっている理由を確認したいとき。

## Do not read this when
- 個別 builder や prompt part の実装そのものを変更したいだけで、テスト期待値や回帰観点を確認する必要がないとき。
- oracle 側の正本 schema や仕様文書の内容を確認したいとき。
- CLI 実行フロー、永続状態、git 操作、worktree 操作など、prompt/schema builder 以外の挙動を調べたいとき。
- 単一の小さな helper の内部実装だけを追えば十分で、最終 prompt や schema の組み合わせに影響しないとき。

## hash
- b9c225c1b152f1b190bcc9dad4c9733a87d86c0dff35bc4eba57d121dcb57f1a

# `test_review_oracle_cli.py`

## Summary
- review oracle の CLI 経由の外部挙動と、所見列挙・検証・judge・merge の制御を検証する realization test。report 生成、対象 oracle の選択、scope 指定、gitignored oracle file の除外、linked worktree 上の review、review 用 worktree の join commit、INDEX.md 変更の取り込みと衝突解決、処理失敗時の error report、review 中に許可されない差分の拒否を扱う。
- 16,000 文字を超えるが、同じ review run の状態、fake Codex 応答、report 文脈を共有する oracle review の外部挙動確認として一箇所に集約されている。

## Read this when
- cmoc review oracle の CLI 挙動、report の内容、終了コード、scope full/session の対象選択を確認・変更する時。
- review oracle が oracle file を列挙する条件、binary oracle の扱い、gitignored oracle file の除外、session scope で対象なしになる挙動を確認する時。
- review oracle の所見 loop で、enumerate finding に渡る文脈、validate/judge の呼び出し、merge operation の契約、invalid operation の拒否を確認する時。
- linked worktree や session branch 上で review oracle がどの worktree と oracle を対象にするかを確認する時。
- review oracle が生成・変更した INDEX.md を本体 worktree に取り込む処理、join commit の report 表示、INDEX.md 削除との merge conflict 解決を確認する時。
- review oracle の途中失敗時に error report を書く挙動や、review 中に INDEX.md 以外の差分が作られた場合の拒否・復元を確認する時。

## Do not read this when
- review oracle 以外の review サブコマンド、または oracle review と関係しない CLI の挙動だけを確認する時。
- Codex 実行 wrapper、設定読み込み、git helper、repo fixture などの下位 helper の詳細実装を調べたいだけの時は、それぞれの実装または support test を直接読む。
- oracle file の正本仕様そのものや、oracle/review の仕様文書を確認したい時は、実装テストではなく oracle 側の該当文書を読む。
- INDEX.md ルーティング生成そのものの仕様や一般的な INDEX.md エントリー形式を調べたいだけの時。

## hash
- 54f6f8ccbf8b69e45a94557a2883c79ab801aaceec911640c101a08ba5199c58

# `test_session_cli.py`

## Summary
- cmoc の session 系 CLI の realization test。session fork/abandon/join が Git branch・linked worktree・session state・cleanup・conflict resolution・出力先をどう扱うかを、Typer runner と一時 Git repo で検証する。
- session state JSON の読み取り helper と branch helper を使い、通常 worktree と linked worktree の両方で、session branch の作成・削除・home branch 復帰・状態遷移を確認する入口になる。

## Read this when
- session fork が session branch と state file を作成する挙動、`.cmoc` ignore 初期化、開始 commit、linked worktree 上での branch/head 扱いを確認または変更するとき。
- session abandon の正常系、home branch 不在時の失敗、cleanup 失敗時の rollback、出力される完了レポートやエラーメッセージを確認または変更するとき。
- session join の正常系、linked worktree での join、session branch 削除失敗時の warning、未コミット差分エラーの stdout/stderr 分離を確認または変更するとき。
- session join の conflict resolution で Codex 実行 profile の file access mode や writable/read-only path、delete conflict の stage 解消、conflict marker 検出を確認または変更するとき。

## Do not read this when
- session 以外のサブコマンド、設定読み込み、path model、oracle 文書生成など、session CLI の外部挙動に関係しない実装だけを調べるとき。
- Git 操作 helper や test runner fixture そのものの定義を調べたいときは、共通 test support や該当 helper の本文へ直接進む。
- session command の内部実装を先に修正したいときは、該当する session サブコマンド実装を読んでから、外部挙動の回帰確認としてこの対象を読む。

## hash
- 2e4a7600edcb887fcc6652452894813210a435f7ad0ec483b3faf3140f38cd14
