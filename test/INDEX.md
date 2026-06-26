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
- apply abandon CLI と apply process 停止処理の realization test。active apply run の破棄時に、apply worktree と apply branch の削除、session state の ready への復帰、警告出力、実行中 process の停止、linked worktree からの実行時の基準ディレクトリ復帰を検証する。
- 欠損済み cleanup 対象、running state だが process id がない状態、worktree を導出できない apply branch、stale apply branch など、破棄処理を中断または警告付き成功にする境界条件を扱う。
- pidfd ベースの signal 送信について、終了済み process、PID 再利用、停止完了待ちの race を apply runtime の制御ロジックとして検証する。

## Read this when
- apply abandon の外部挙動、CLI 出力、session apply state の更新、apply worktree と apply branch の cleanup 条件を変更または確認したいとき。
- apply が running のまま abandon される場合の process 停止順序、process id 記録の削除、停止できない状態の扱いを変更または確認したいとき。
- apply worktree 内、linked session worktree 内、stale apply branch 上など、実行場所によって abandon 対象をどう判定するかを確認したいとき。
- apply runtime の process signal 送信、終了済み process の無視、PID 再利用検出、停止待ち race の扱いを変更または確認したいとき。

## Do not read this when
- apply fork の Codex 実行結果や review findings の内容そのものを検証したいだけのとき。
- apply abandon 以外の session fork、init、worktree 作成 helper の一般的な挙動を調べたいとき。
- oracle 仕様断片、ルーティング文書、または INDEX.md 生成規則を確認したいとき。
- git worktree や branch 操作の低レベル helper 全般を調べたいが、apply abandon の cleanup 境界には関心がないとき。

## hash
- 54b682faa7a06cf27ea4ff719b3abc053fa5b6ea98122d9b34e99983e3aeff54

# `test_apply_fork_cli.py`

## Summary
- apply fork コマンドの realization test。Codex 実行を fake に差し替え、apply run の開始・完了、session state 更新、apply branch と worktree 作成、linked worktree からの開始、設定読み込み失敗時の未開始保証、`.cmoc` 追跡時の拒否、`.gitignore` の保持と apply branch 側での編集、root 直下 memo 除外と入れ子 memo 対象維持を検証する。

## Read this when
- apply fork の外部挙動、状態遷移、branch/worktree 作成規則、session 側 worktree を汚さない制御を変更・確認したいとき。
- apply fork が linked worktree の HEAD を oracle snapshot と apply branch の起点にする挙動を確認したいとき。
- apply fork の設定読み込み失敗、`.cmoc` が git 追跡対象になっている場合の拒否、pid/state/branch を作らない失敗時挙動を扱うとき。
- apply fork の対象列挙や所見適用で `.gitignore`、root 直下 memo、入れ子 memo directory の扱いを変更・確認したいとき。
- Codex CLI 実行そのものではなく、apply fork から Codex 呼び出しを行う制御ロジックを fake で検証したいとき。

## Do not read this when
- apply fork 以外のサブコマンド、または apply fork の実装詳細だけを先に確認したいときは、該当する実装側を読む。
- Codex や LLM の出力品質そのものを検証したいとき。この対象は fake 結果で制御ロジックと副作用を検証する。
- oracle 正本仕様断片を確認したいとき。この対象は realization test であり、正本仕様ではない。
- 一般的な test fixture、git helper、CLI runner の定義だけを確認したいときは、共通 test support 側を読む。

## hash
- fa29df4c08243b05552d03556a31e16af13367194b97793bed0fc9b86a7b0abe

# `test_apply_fork_report_cli.py`

## Summary
- apply fork CLI の制御フローを pytest で検証する realization test。Codex 実行を fake に差し替え、所見列挙、適用、commit message 生成、変更要約生成、report 出力、session state 更新、git branch/commit の副作用を統合的に確認する。
- 未収束時の report と exit code、dirty file 再検査と INDEX.md 除外、最後の許可対象が空所見だった場合の収束判定、編集禁止対象差分の error 化、rolling 実行で前回 apply join 後の変更だけを対象にする挙動を扱う。

## Read this when
- apply fork の CLI 挙動、終了コード、標準出力に出る report path や result_label、生成 report の内容を変更または調査するとき。
- apply fork が Codex 応答をどの purpose で呼び分けるか、所見適用後に commit message や change summary を使って apply branch/report を更新する流れを確認するとき。
- apply fork 後の dirty file 再検査、INDEX.md の再検査除外、収束/未収束判定、num_apply_files 上限時の扱いを変更するとき。
- apply fork が編集禁止対象の差分を検出した際のエラー出力、report、session state の error 記録を確認するとき。
- rolling apply fork の対象範囲を、前回 apply join の oracle snapshot commit 以降の変更に限定する挙動を確認するとき。

## Do not read this when
- apply fork の内部 helper 単体の細部だけを調べたい場合。まず実装側の対象 module を読む方が直接的。
- apply join、session fork、init などの各サブコマンド自体の仕様や実装を調べたい場合。ただし apply fork との統合副作用を確認する目的なら読む価値がある。
- Codex CLI や LLM 出力品質そのものを検証したい場合。このテストは Codex 応答を fake 化して、cmoc 側の制御ロジックと副作用を検証している。

## hash
- b6df3c3799f989f788cd8e9347e8b049e465027d0b04dddbbf0ca4f8345b7f2c

# `test_apply_join_cli.py`

## Summary
- apply join サブコマンドの結合・後片付け・状態更新・異常検出を、CLI 経由の外部挙動として検証する realization test。
- apply fork で作成された apply worktree と apply branch を join が削除し、session state を ready に戻し、join report を生成することを確認する。
- apply worktree から実行した場合の作業ディレクトリ復帰、古い apply branch からの join 拒否、dirty な apply worktree での停止とログ出力先を扱う。
- 想定外の apply 差分、force resolve、許可される .gitignore 差分、通常ファイルの未解決 merge conflict、INDEX.md conflict の通常モード解決を検証する。

## Read this when
- apply join の成功時に apply worktree・apply branch・session state・last_joined_apply_oracle_snapshot_commit・report がどう変わるべきかを確認したいとき。
- apply join を session worktree から実行する場合と apply worktree から実行する場合の違いを確認したいとき。
- 古い apply branch、未コミット差分、想定外差分、merge conflict に対する apply join の終了コード・出力・後片付け可否を変更または調査するとき。
- apply join の force resolve、.gitignore 変更の扱い、INDEX.md conflict の自動解決に関わる実装や仕様断片を読む前後で、既存の realization test の期待値を確認したいとき。

## Do not read this when
- apply fork の Codex 実行内容そのもの、LLM 出力品質、または apply worktree 作成処理だけを調べたいとき。
- session fork、init、git helper、runner fixture など、apply join の外部挙動ではなくテスト基盤や別サブコマンドの詳細を確認したいとき。
- apply join の内部 helper 単体のアルゴリズムだけを調べたいとき。ただし CLI 出力、状態ファイル、worktree/branch 削除、report 生成の期待値を確認する場合は読む。

## hash
- 5210ebc91b591cdf1aa681f4e31fa063302930a7fe42255760e1f9b509938f38

# `test_basic_runtime.py`

## Summary
- 基本的なランタイム挙動を横断的に検証する realization test。パス表記の解決、時間表示、work root 判定、設定既定値、構造化エラー出力、branch/session 状態の不正形状、CLI エラー出力先、補完プローブ時の副作用抑止、.cmoc の ignore 設定、file access mode と sandbox mode の対応、binary 判定、Codex profile のファイルアクセス権限生成を扱う。
- 単一機能の詳細テストというより、cmoc の基礎ランタイム契約が複数モジュール間で崩れていないかを確認する入口になる。

## Read this when
- パスモデル、repo root と work root の判定、linked worktree 上の挙動を変更・確認する。
- CmocError の markdown レンダリング、CLI 例外処理、引数解析エラー、stdout/stderr の出し分けを変更・確認する。
- session/apply branch 名から session id を取り出す処理、または branch に対応する状態読み込みの不正入力処理を変更・確認する。
- init や session fork など、CLI 実行前提条件、補完プローブ、.cmoc 関連の副作用、.gitignore 更新処理を変更・確認する。
- FileAccessMode、sandbox mode 変換、Codex profile の permission profile、read/write/read_only/deny_read/writable_roots の生成規則を変更・確認する。
- binary 判定や設定既定値など、共通ランタイム helper の外部挙動を変更した後に、基礎的な回帰範囲を確認する。

## Do not read this when
- 特定サブコマンドの正常系フロー、出力 schema、プロンプト生成など、このテストで直接扱わない機能別挙動だけを調べたい場合。
- oracle file の正本仕様そのものを確認したい場合。ここは realization test なので、仕様判断の根拠には対応する oracle file を読む。
- 個別モジュールの実装構造や内部 helper の分割方針を詳しく追いたい場合。まず対象の実装ファイルを直接読む。
- INDEX.md エントリー作成やルーティング文書の方針を調べたい場合。ここはランタイム挙動のテストであり、ルーティング規約は扱わない。

## hash
- 8dc8c4e76aaee3fbf6f911d7e36281451d54c962873602a793500d2e964dc653

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
- Codex CLI 呼び出しの runtime テスト。exec 経路が prompt を標準入力で渡し、schema・profile・CODEX_HOME・stdout/stderr/call log・subcommand log を期待どおり扱うことを検証する。
- Codex TUI 経路が exec サブコマンドを使わず prompt 引数で起動し、workspace write profile の writable/read-only 設定、call log、console 表示、戻り値を記録することを検証する。
- repo 側 config が Codex profile の model と reasoning_effort に反映されること、worktree cwd 実行時に schema 保存先が cwd 側の work root になることを確認する。

## Read this when
- Codex CLI を起動する runtime 実装、特に exec と TUI の argv・cwd・環境変数・profile 生成・ログ出力を変更する時。
- AgentCallParameter の model class、reasoning effort、file access mode、output schema が Codex profile や CLI 引数へどう反映されるかをテスト観点から確認したい時。
- Codex 呼び出しログ、stdout/stderr ログ、subcommand logger の codex_call event、console 表示の期待値を変更または調査する時。
- worktree 上で Codex exec を実行する場合の schema 保存先、root 側と cwd 側の .cmoc state/log の使い分けを確認する時。
- repo config の codex model や reasoning_effort 設定が実行時 profile に反映されない不具合を調べる時。

## Do not read this when
- Codex runtime ではなく、git 操作、oracle 生成、INDEX 生成、path model など別領域の挙動だけを調べる時。
- Codex CLI の実物の出力品質や LLM 応答内容を検証したい時。このテストは fake codex と subprocess 差し替えで runtime の制御と副作用を検証する。
- Codex profile 生成の実装詳細そのものを変更する場合で、まず実装の責務や helper 境界を知りたい時は、対応する runtime 実装を先に読む。
- config schema や既定値の定義そのものを調べる時は、設定定義や同期処理の実装を先に読む。

## hash
- be5c7105c0d916cd3989f402ac9d4c72e7c29fb82414c1641a19b58e7239da84

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
- Codex 実行が quota exceeded で失敗した後、quota availability probe を挟んで再実行または resume する制御を検証する realization test。
- quota 待機時の呼び出し順、標準入力、CODEX_HOME 伝播、resume token 利用、call log と subcommand log の記録内容、コンソール出力をまとめて確認する。
- 並行実行時に quota probe が代表 1 回に集約され、各実行が resume して成功することも検証する。

## Read this when
- Codex 実行の quota exceeded 検出後に、probe、retry、resume を行う制御ロジックを変更する。
- Codex 実行ログ、call_log_path、stdout/stderr/output の保存、subcommand logger の codex_call event を変更する。
- quota probe の argv、profile、標準入力、出力ファイル、CODEX_HOME など、Codex CLI 呼び出し条件を確認したい。
- 複数スレッドから同時に quota exceeded が発生した場合の probe 集約や resume 挙動を変更・調査する。

## Do not read this when
- Codex CLI の通常成功時や一般的な失敗時だけを扱い、quota exceeded 後の待機・probe・resume 制御に触れない。
- oracle file の正本仕様を確認したい。これは実装挙動を検証する realization test であり、仕様本文ではない。
- Codex 実行とは無関係なサブコマンド、設定読み込み、path model、INDEX.md 生成処理だけを調査する。
- LLM 出力品質や Codex CLI 自体の内部挙動を確認したい。ここでは fake codex を使って cmoc 側の制御とログだけを検証している。

## hash
- 8a391a1b2ae8c80eee70ffea050c1797c06ea15953441d15f80ed91e0f83c2a3

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 実行ラッパーの retry 制御を検証する realization test。schema validation 失敗後の再実行、capacity エラー検出時の再実行、stdout JSONL 以外に出た capacity/quota 文言を retry 条件として扱わないことを、fake codex 実行ファイルと呼び出しログで確認する。
- AgentCallParameter、CmocConfig、SubcommandLogger、run_codex_exec の組み合わせで、出力 JSON、呼び出し回数、call log、subcommand log の status・returncode・error detail が期待どおりになるかを見る入口になる。

## Read this when
- Codex CLI 呼び出しの semantic output schema validation retry の挙動やログ記録を変更・調査する。
- Codex CLI が capacity を示す JSONL event を返したときの retry、sleep 抑制、失敗呼び出しの call log 記録を確認する。
- quota や capacity を示す文字列が stdout JSONL event ではなく通常出力・stderr に出た場合に、retry せず通常失敗として扱う境界を確認する。
- run_codex_exec の戻り値、call_log_path、stdout_log_path、subcommand logger の codex_call event status を変更する実装に触る。

## Do not read this when
- Codex CLI の通常成功パスだけを確認したい場合。retry や schema validation 失敗、capacity/quota 判定に関係しないならより基本的な実行テストを読む。
- CLI 引数の構築、モデル選択、ファイルアクセス設定などの入力変換だけを調べたい場合。この対象は retry とログ副作用の検証が中心である。
- oracle file の正本仕様を確認したい場合。この対象は realization test であり、正本仕様そのものではない。

## hash
- 27137103545db450aeccf58ac1a55fdb671bd971566bc45f7d06a1f52534ac69

# `test_indexing_cli.py`

## Summary
- cmoc の indexing と INDEX.md 更新処理に関する realization test。CLI 実行時の初期化前エラー、未コミット差分の拒否、生成済みエントリーの再利用、linked worktree 対象化、INDEX.md だけをコミットする制御、競合解消時の INDEX.md 削除コミット、エントリー描画時の semantic field 検証を扱う。
- indexing 実装が Codex によるエントリー生成、hash freshness 判定、malformed entry の再生成、兄弟要素の並列生成、ルート直下 memo 除外とネストした memo の扱いを満たすか確認する入口となる。

## Read this when
- indexing サブコマンド、INDEX.md の生成・更新・コミット、または既存 INDEX.md の freshness 判定を変更する。
- 未初期化リポジトリ、dirty worktree、linked worktree、merge conflict など、indexing 周辺の git 状態制御を変更する。
- render_index_entry や build_index_entry の structured output 受け入れ条件、空リスト・非文字列・欠落 field のエラー処理を変更する。
- ルート直下の memo を indexing 対象から外す処理、または下位階層にある同名ディレクトリを通常対象として扱う処理を確認する。
- INDEX.md 更新処理の並列化や、同階層要素のエントリー生成順序・実行制御に関わる実装を触る。

## Do not read this when
- 個別サブコマンドの通常動作だけを調べたい場合は、そのサブコマンドの実装または対応する専用テストを先に読む。
- INDEX.md エントリー本文の正本仕様や人間向けルーティング文書の書き方を確認したい場合は、oracle 側の仕様断片を読む。
- Codex 実行基盤そのもの、CLI runner の共通 fixture、git test helper の詳細を調べるだけなら、支援モジュールや実装側の該当箇所を読む。
- 生成された INDEX.md の内容を人間がどう解釈するかだけが関心で、indexing の制御フローや副作用を検証しない場合は、このテストを読む優先度は低い。

## hash
- 68a9ca8e65c3b1750cfffb92daa8a88aaff50a543981bc16fade83083575dbd1

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
- プロンプト構成部品と実行パラメータ builder の realization test 群。標準文書、ルーティング規則、ファイルアクセス規則、完全プロンプトへの任意標準の注入・省略、禁止語の置換、Markdown レンダリング、schema 制約、model class・reasoning effort・file access mode の選定が期待どおりになることを検証する。
- apply fork、indexing、review oracle、session join、TUI resolve parameter など複数領域の builder が生成する prompt・schema・実行モードの契約を横断的に確認する入口として位置づけられる。

## Read this when
- 標準文書やルーティング規則、ファイルアクセス規則、index entry standard、review/apply/realization standard の文言がプロンプトに含まれるかどうかを変更・確認する時。
- complete prompt の構成、補助プロンプトの注入、禁止された path placeholder や agent 表現の除去、標準文書のデフォルト省略・明示追加の挙動を確認する時。
- StructDoc や code block の Markdown レンダリング、特に連続空行の畳み込みに関する挙動を変更する時。
- apply fork、indexing、review oracle、session join、TUI resolve parameter の builder が返す model class、reasoning effort、file access mode、prompt 断片、structured output schema の契約を確認する時。
- schema の required、additionalProperties、enum、空配列拒否、oracle source との一致など、出力 schema の検証条件を変更する時。
- worktree 内で実行される apply fork prompt が対象リポジトリの root をどう扱うか、placeholder を実パス表現へどう変換するかを確認する時。

## Do not read this when
- 個別 builder の実装そのもの、prompt 文書本文の生成ロジック、または schema 定義の正本を読みたい時は、対応する実装・定義ファイルを直接読む方がよい。
- CLI コマンドの外部挙動やサブコマンド実行フローを調べたいだけで、プロンプト構成や parameter builder の契約に関係しない時。
- INDEX.md エントリー生成の一般規則だけを確認したい時は、標準文書の生成元や仕様側を読む方が直接的である。
- 単一の低レベル helper の内部アルゴリズムを調べたい時は、この横断テストではなく、その helper の実装と近接テストを読む方がよい。

## hash
- 9721975d7cabf49cf36781ca3044d2ce3e197f13ab99ff352cd30a19a583b68c

# `test_review_oracle_cli.py`

## Summary
- `review oracle` サブコマンドの実現テスト群。レビュー対象 oracle の選定、Codex 呼び出しループ、レポート生成、finding の merge 操作、レビュー用 worktree の扱い、失敗時レポート、INDEX.md 以外の差分拒否を外部挙動として検証する。
- セッションスコープとフルスコープの違い、gitignored oracle file の除外、binary oracle file の扱い、linked worktree 上の session branch を対象にする挙動など、oracle review の対象決定と実行環境に関する回帰確認の入口になる。

## Read this when
- `review oracle` の CLI オプション、scope、レポート内容、終了コード、エラー表示を変更する。
- oracle review が評価対象に含める oracle file の条件、gitignored file の除外、binary file の扱い、対象 0 件時の挙動を確認または変更する。
- oracle review 中の Codex structured output 呼び出し、finding の列挙・検証・判定・merge 操作、関連 finding だけを次ループへ渡す制御を変更する。
- review 用 worktree の作成場所、linked worktree での branch 解決、レビュー後の INDEX.md 変更の取り込み、merge conflict 解決、不要 worktree の残存防止を扱う。
- レビュー処理が途中で失敗した場合の report 生成、fatal finding の扱い、標準出力・標準エラーへのエラー表示を検証する。
- review oracle が生成してよい差分を INDEX.md に限定する制御や、想定外の staged・unstaged・untracked 変更を拒否する挙動を変更する。

## Do not read this when
- oracle review 以外のサブコマンド、セッション作成そのもの、設定読み込み単体、または一般的な git helper の挙動だけを調べたい。
- oracle file の正本仕様本文やレビュー観点そのものを確認したい場合で、CLI の実現テストではなく oracle 配下の仕様断片を読むべき。
- INDEX.md ルーティング文書の生成規則や entry の文章品質だけを扱う場合で、review oracle の実行挙動に関心がない。
- Codex CLI や LLM の実出力品質を評価したい場合。このテストは出力品質ではなく、fake result を使った制御ロジックと外部挙動を検証する。

## hash
- 932f0d4105979a9fdf8de536c480aa9b23b0d37ab7e88e92cfd4ea68b7563ab7

# `test_session_cli.py`

## Summary
- session サブコマンドの realization test。session fork/abandon/join が Git branch、linked worktree、session state JSON、CLI 出力、競合解決時の Codex 実行権限をどう扱うかを、実リポジトリ操作に近い形で検証する。

## Read this when
- session fork が session branch と session state を作成し、home branch や start commit を記録する挙動を確認・変更するとき。
- session abandon が home branch へ戻ること、session branch を削除すること、state を abandoned にすること、失敗時に状態と branch を保つことを確認・変更するとき。
- session join が session branch の変更を home branch に取り込み、linked worktree 上の branch を維持し、state を joined にする挙動を確認・変更するとき。
- session join の oracle 競合解決で Codex を REALIZATION_WRITE profile で呼び、競合対象を writable、memo や .agents を read-only として扱う権限設定を確認・変更するとき。
- session join の削除競合の staging や、session branch 削除失敗時の警告出力を確認・変更するとき。

## Do not read this when
- session 以外のサブコマンドや、CLI 全体の引数構造だけを確認したいとき。
- session の内部 helper の細かな実装だけを調べたい場合で、外部挙動・state・Git 副作用のテスト観点が不要なとき。
- oracle file の正本仕様そのものを確認・変更したいとき。
- Codex profile 生成の一般仕様だけを確認したいとき。ただし session join の競合解決で使われる権限境界を調べる場合は読む。

## hash
- 03bb5087d2618a43993a67fc03372042272e6029a1f96236764b114c811dd04b
