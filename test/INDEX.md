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
- cmoc の基礎的な runtime 挙動を横断的に検証する realization test。パストークン解決、run/work/repo root 判定、設定既定値、構造化エラー表示、session/apply branch の状態 ID 検証、CLI preflight と補完プローブ、gitignore 更新、sandbox mode 変換、binary 判定、Codex profile の sandbox 設定を扱う。
- 単一機能の詳細テストというより、basic・runtime・config・main・commons にまたがる公開挙動と制御ロジックの回帰検出入口として位置づけられる。

## Read this when
- runtime の基礎挙動、root path 解決、`<cmoc-root>` などの token path 表示、linked worktree と main worktree の扱いを変更する。
- `CmocError` の markdown 表示、CLI エラーの stdout/stderr 出力先、preflight 実行条件、completion probe の副作用抑制を変更する。
- session branch または apply branch の名前形式、状態ファイル読み込み、branch から session id を取り出す制御を変更する。
- `.cmoc` の gitignore 登録、file access mode から Codex sandbox mode/profile への変換、binary 判定の読み取り範囲を変更する。
- 設定既定値、model class、reasoning effort、sandbox writable roots など、複数モジュールにまたがる基本契約の回帰を確認したい。

## Do not read this when
- 個別 CLI サブコマンドの正常系フローや user-facing 出力の詳細だけを確認したい場合は、そのサブコマンド専用の実装またはテストへ進む。
- oracle の正本仕様断片そのものを確認・変更したい場合は、oracle 配下の該当文書を読む。このテストは realization test であり正本仕様ではない。
- テスト共通 fixture、repo 作成 helper、runner の実装だけを確認したい場合は、support 側のテスト補助コードを直接読む。
- 単一モジュール内の内部 helper 実装だけを変更し、ここで検証される外部挙動や制御ロジックに影響しないことが明確な場合は読まなくてよい。

## hash
- dd32024d5f5822b1e2fcc02614d47d6b43f00328bfad4c7775c22c343a2bd9b7

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
- Codex CLI 呼び出しラッパーの realization test。exec 経路では prompt を stdin で渡し、schema・profile・CODEX_HOME・stdout/stderr・call/prompt log・subcommand event・console 表示が期待どおりになることを検証する。
- worktree 上の cwd で exec した場合、出力 schema の保存先が root 側ではなく cwd 側の work root 配下になり、call log は root 側に残ることを検証する。
- TUI 経路では exec サブコマンドを使わず prompt を argv 末尾に渡し、capture なしで起動し、workspace-write profile と call log・subcommand event・戻り値を検証する。
- repo config の model と reasoning_effort 設定が Codex profile に反映されることを検証する。

## Read this when
- Codex CLI の exec/TUI 起動引数、prompt の渡し方、CODEX_HOME、profile 生成、sandbox 設定、出力 schema 指定を変更する時。
- Codex 呼び出しの call log、prompt log、stdout/stderr log、subcommand logger event、console 表示の仕様や実装を確認・変更する時。
- worktree を cwd にした Codex exec の schema 保存先や、root 側と cwd 側の `.cmoc` 状態・ログ配置の違いを確認する時。
- repo config から Codex model 名や reasoning effort を読み込んで profile に反映する処理を変更する時。

## Do not read this when
- Codex CLI 呼び出しではなく、汎用的な git 操作、repo 作成 fixture、またはテスト支援 helper 自体の挙動だけを調べる時。
- agent call parameter の enum や config schema の定義そのものを調べる時は、定義側の実装・テストを先に読む。
- Codex CLI や LLM の実際の出力品質を評価したい時。このテストは fake command と subprocess monkeypatch による制御ロジックと副作用の検証を対象にしている。

## hash
- f17410ce82ffbf5b6d3864bbde6184d5c7470df966efa9280da3eeb1f5858c10

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
- prompt part と ACP builder が生成する prompt、routing rule、file access rule、standard 文書、structured output schema、実行パラメータの期待値を横断的に検証する realization test。
- 標準文書の markdown render 結果、complete prompt への標準注入有無、apply fork/review/session/tui/indexing builder の model・reasoning・file access mode・schema 制約を一箇所で確認する。
- 対象は長いが、agent prompt と structured output schema の構築結果を同じ読み取り文脈で検証するため、共通の render/schema 期待値を追う入口としてまとまっている。

## Read this when
- prompt_parts や builder が生成する最終 prompt の構成、標準文書の挿入条件、routing/file access 文言の回帰を確認したいとき。
- StructDoc、StructCodeBlock、render_as_markdown の markdown 出力や空行折り畳みの期待挙動を確認したいとき。
- apply fork、review oracle merge、session join conflict resolution、TUI resolve parameter、indexing index entry の builder parameter や structured output schema のテスト観点を確認したいとき。
- standard 文書に含めるべき用語、含めてはいけない表記、schema enum や required property の期待値を変更に合わせて更新する必要があるとき。

## Do not read this when
- 個別 builder の実装詳細や prompt 文面の生成ロジックそのものを調べたいだけなら、対応する実装側を直接読む。
- oracle の正本仕様断片そのものを確認したい場合は、テスト期待値ではなく対応する oracle 本文を読む。
- 特定の CLI 実行フロー、永続状態、git 操作など prompt/schema builder 以外の挙動を調べている場合は、より直接のテストや実装を読む。

## hash
- a4089fd9752c0138da485de49821061d8d08e9e405cdac69b54d7ab1036ab940

# `test_review_oracle_cli.py`

## Summary
- review oracle の CLI 経由の外部挙動を検証する realization test。report 生成、対象 oracle の選択、所見列挙・検証・judge・merge、結果分類、エラー report、review 用 worktree と join commit、INDEX.md 差分の取り込みや競合解決、想定外差分の拒否を同じ review run 文脈で確認する。
- 所見 merge 操作の kind ごとの契約、無効操作、target 再利用拒否も検証し、review oracle loop が対象 oracle ごとの関連所見だけを次回 prompt に渡す制御を押さえる。
- 16,000 文字を超えるが、fake Codex 応答、report 文脈、review run の状態を一箇所に保つ方が凝集性が高いという責務境界を docstring で明示している。

## Read this when
- review oracle コマンドの出力 report、終了コード、scope 指定、対象 oracle の数え方や除外条件を変更・確認するとき。
- review oracle の所見 loop、finding の verdict・severity 集計、merge 操作、validate・judge の呼び出し制御を変更・確認するとき。
- review oracle が linked worktree、session branch、review 用 worktree、join commit、INDEX.md の生成差分や競合解決をどう扱うべきかを確認するとき。
- review oracle 実行中の失敗時 report、標準出力へのエラー表示、INDEX.md 以外の予期しない差分の拒否と復元挙動を検証するとき。

## Do not read this when
- review oracle 以外の subcommand の CLI 挙動を調べるだけなら、対象 subcommand のテストへ進む。
- review oracle の実装詳細を直す必要があり、期待される外部挙動ではなく関数本体や git 操作の実装を読みたい場合は、実装側の review command へ進む。
- oracle file の正本仕様そのものや INDEX.md ルーティング規則を確認したい場合は、oracle 側の本文を読む。
- テスト共通 fixture、runner、repo 作成 helper の使い方だけを確認したい場合は、test support 側を読む。

## hash
- ea7d3f24f774abdb135ebb656a95428d110ed907232765d5023af12e591d0c1f

# `test_session_cli.py`

## Summary
- session サブコマンドの CLI 挙動を検証する realization test。session fork による session branch と状態ファイル生成、.cmoc ignore 初期化、linked worktree 上での分岐元 branch と開始 commit の扱いを確認する。
- session abandon の正常系と失敗系を検証する。home branch への復帰、session branch 削除、状態の abandoned 化、既存 home branch 必須条件、cleanup 失敗時の branch と状態 rollback、利用者向け出力を扱う。
- session join の正常系、衝突解決、linked worktree、削除衝突、session branch 削除失敗 warning、エラー出力先を検証する。oracle file 衝突解決時に Codex 実行へ REALIZATION_WRITE profile と適切な writable roots が渡ることも確認する。

## Read this when
- session fork、session abandon、session join の CLI 外部挙動、git branch/worktree 操作、session 状態 JSON、実行ログ、stdout/stderr の期待値を変更・調査する時。
- session branch の生成・削除、home branch への復帰、linked worktree での current branch 維持、session_start_commit や session_home_branch の保存内容を確認する時。
- session join の merge conflict 解決フロー、conflict marker 判定、削除衝突の staging、Codex 実行 profile、FileAccessMode.REALIZATION_WRITE、oracle file 解決時の書き込み権限を変更・検証する時。
- session abandon/join の失敗時挙動、cleanup 失敗時の rollback、未コミット差分エラー、警告やエラーレポートの出力先を確認する時。

## Do not read this when
- session サブコマンド以外の CLI コマンド、設定読み込み、path model、oracle 文書の正本仕様そのものを調べるだけなら、より直接の実装または oracle 側を読む。
- session の内部 helper の詳細実装だけを局所的に変更する場合で、CLI 経由の外部挙動、git 副作用、状態ファイル、出力互換性を確認する必要がないなら、対象の実装モジュールを先に読む。
- Codex CLI や LLM の出力品質そのもの、一般的な sandbox 設定全体、session 以外の apply/review 系 profile を調べる場合は、このテストではなく該当する profile 実装や別テストを読む。

## hash
- 2fec9690580720f4d85bcedc291221277d381a800d0fc93374f47a9b1f0fa62b
