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
- apply fork サブコマンドの実行フローを検証する realization test。Codex 実行を fake に差し替え、session fork 後の apply run が state、apply branch、worktree、process pid、所見列挙呼び出しを期待どおり更新・整理することを確認する。
- linked worktree 上での apply fork 開始位置、session 側 .gitignore の保持、.cmoc が追跡対象になっている場合の拒否、設定読み込み失敗時に apply run を開始しないことを検証する。
- 所見対象としての .gitignore を apply branch 側で編集できることと、apply target 正規化で root 直下 memo を除外しつつ入れ子の memo directory を対象に残すことを検証する。

## Read this when
- apply fork の CLI 挙動、session state の apply 欄、apply branch/worktree の生成・完了・後片付けを変更または調査するとき。
- linked worktree から apply fork を実行する場合の基準 commit、branch、worktree 配置に関する挙動を確認するとき。
- .gitignore や .cmoc 追跡状態が apply fork に与える影響、または session 側 worktree を汚さない失敗処理を確認するとき。
- apply fork の設定読み込み失敗時に、state・pid・branch を作成または変更しない制御を確認するとき。
- apply fork の所見列挙対象、所見適用ループ、commit message/change summary 用 Codex 呼び出しの fake 化を伴うテストを追加・修正するとき。
- apply 対象 path の正規化で、root 直下 memo の除外と入れ子の memo directory の扱いを確認するとき。

## Do not read this when
- apply fork 以外のサブコマンドや、session fork 単体の基本挙動だけを確認したいとき。
- Codex CLI の実出力品質や LLM 応答内容そのものを検証したいとき。このテストは Codex 実行を fake に置き換えて制御ロジックと副作用を確認する。
- apply fork の実装詳細そのものを読む必要があるときは、実装側の apply fork モジュールを直接読む方が適切。
- oracle 文書の正本仕様や INDEX.md 生成規則を確認したいとき。

## hash
- 3cac7de41b8905c954548167eab000c00b8e33c64062aa4830c203cdd16c31b3

# `test_apply_fork_report_cli.py`

## Summary
- apply fork CLI の report 生成と収束判定を検証する realization test。Codex 応答を fake に差し替え、所見適用、変更要約、commit message、終了コード、session state、report 内容、rolling 対象選択などの外部挙動を確認する。
- 未収束時の report には変更要約と commit message が反映され、収束時・エラー時・rolling 実行時にはそれぞれ期待される状態更新と出力になることを扱う。

## Read this when
- apply fork の CLI 終了コード、report 表示、result label、session state 更新に関するテストを確認・変更するとき。
- apply fork が所見適用後の dirty file を再検査し、生成されたルーティング index を再検査対象から外す挙動を確認するとき。
- apply fork の回数上限到達時に、最後の許可対象が空所見なら収束扱いになる制御を確認するとき。
- apply fork が編集禁止領域への差分を検出して error state と report に反映する挙動を確認するとき。
- rolling apply fork が前回 apply join 後の oracle 側変更だけを対象にする挙動を確認するとき。

## Do not read this when
- apply fork の内部実装や helper の責務分割だけを調べたいときは、実装側の apply fork サブコマンドへ進む。
- apply join 単体の仕様や join 処理全体のテストを確認したいときは、apply join を扱うテストへ進む。
- Codex 実行基盤そのもの、structured output schema、agent call parameter の一般挙動を調べたいときは、それぞれの実装または専用テストへ進む。

## hash
- a95414220bb9a8f63a087a9d82f9c0997eb33223e7c1c3172a238b481be00a77

# `test_apply_join_cli.py`

## Summary
- apply join コマンドの CLI 統合テスト。apply fork 済みセッションを join したときの worktree 削除、apply branch 削除、状態ファイル更新、join report 生成を検証する。
- session worktree 側と apply worktree 側のどちらから実行しても join が完了すること、apply worktree から実行した場合に作業ディレクトリが session root へ戻ることを確認する。
- 未コミット差分、想定外の oracle 差分、通常ファイルの merge conflict、INDEX.md conflict の自動解決など、apply join の失敗・中断・強制解決時の外部挙動を検証する。

## Read this when
- apply join の成功時に、apply worktree と apply branch が削除され、状態が ready に戻り、last joined 系の session 状態と report が更新される挙動を確認したいとき。
- apply join を apply worktree から実行するケース、または dirty な apply worktree を拒否するケースの CLI 挙動・ログ出力先・エラーメッセージを変更するとき。
- apply join の差分判定、oracle 配下の想定外差分、.gitignore の許容差分、--force-resolve による巻き戻し挙動を変更するとき。
- merge conflict の扱い、特に通常ファイルの unresolved conflict 報告や INDEX.md conflict を通常モードで解決して join 継続する挙動を変更するとき。

## Do not read this when
- apply fork が Codex 実行結果から apply worktree を作る処理そのものを確認したいだけのとき。
- apply join の内部 helper の単体的な分岐や、report 文字列生成だけを局所的に確認したいとき。
- セッション作成、init、git repository fixture、runner などテスト基盤の共通処理を調べたいとき。
- oracle file の正本仕様や、INDEX.md エントリー生成規則そのものを調べたいとき。

## hash
- 47fc0068032f463620d8b519547dfee6dd82f2cd4f1e86379a11b603d0572222

# `test_basic_runtime.py`

## Summary
- 基本ランタイム層の実現テストであり、パス表記、実行時間表示、work root 判定、設定既定値、構造化エラー表示、セッション branch 形状検証、CLI エラー出力、補完 probe 時の副作用抑止、`.cmoc` ignore 設定、file access mode、binary 判定、Codex profile の権限制御を横断的に検証する。
- 個別モジュール単位の詳細テストというより、利用者に見える CLI 挙動とランタイム共通処理の境界条件が期待どおりつながっているかを確認する入口になる。

## Read this when
- ランタイム共通処理、CLI preflight、エラー報告、git worktree 判定、`.cmoc` の ignore 設定、または Codex profile の sandbox/file_system 権限生成を変更する。
- `FileAccessMode`、`ModelClass`、`ReasoningEffort`、設定既定値、branch 名からの session id 抽出など、複数の実装モジュールをまたぐ基本契約の既存テスト観点を確認したい。
- CLI の失敗時出力が stderr ではなく stdout に出ること、補完 probe が通常の副作用を起こさないこと、work root 以外での実行を拒否することを検証するテストを探している。
- 権限 profile で read/write/read_only/deny_read/writable_roots が file access mode ごとにどう期待されているかを、テスト上の期待値から確認したい。

## Do not read this when
- 特定サブコマンドの正常系フローや詳細な業務ロジックだけを調べたい場合は、そのサブコマンドや対象モジュールに対応するより直接のテストを読む。
- oracle 配下の正本仕様や設計意図そのものを確認したい場合は、実現テストではなく対応する oracle doc または oracle src を読む。
- テスト支援用の repository fixture、git helper、runner の実装を調べたい場合は、支援モジュールを直接読む。
- INDEX.md の生成規則、ルーティング文書の形式、または structured output の仕様を調べたい場合は、この実行時テストではなくそれらの仕様本文を読む。

## hash
- 8641df930920543899d0ca81ae78735b56b33d38a118f2cfa677b54e40cb4a51

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
- Codex CLI 実行ラッパーが quota exceeded を受けた後に、quota availability probe を挟んで再実行または resume し、最終結果・呼び出しログ・サブコマンドイベントを整合させる挙動を検証する realization test。
- 偽の codex 実行ファイルを使い、CODEX_HOME、argv、stdin、stdout/stderr/output のログ、resume token の有無、並列実行時の probe 代表化を外部副作用として確認する。

## Read this when
- Codex CLI 呼び出しの quota exceeded 検出後の待機・probe・resume・再実行制御を変更する時。
- quota availability probe の argv、stdin、profile、出力保存、ログ記録、コンソール表示の期待値を確認したい時。
- thread.started の thread_id を使った resume と、resume token が得られない場合の通常再実行の分岐を確認したい時。
- 複数の run_codex_exec 呼び出しが同時に quota exceeded になった時、probe が 1 回に集約され各呼び出しが復帰する制御を確認したい時。

## Do not read this when
- Codex CLI の通常成功時、通常失敗時、設定変換、または quota 以外のエラー処理だけを確認したい時。
- AgentCallParameter、CmocConfig、SubcommandLogger の基本構造や生成規則そのものを調べたい時。
- 実際の Codex CLI や LLM の応答品質を検証したい時。
- リポジトリ作成、CODEX_HOME 準備、偽実行ファイル作成のテスト支援関数そのものを変更したい時。

## hash
- 41648e73004d1e8cd44eab18f909248b78cd18783acd796920a90c6c2454f754

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
- インデックス生成 CLI と関連 helper の realization test。初期化済み・未初期化リポジトリ、linked worktree、既存差分、fresh hash、malformed entry、semantic field validation、並列生成、root 直下 memo 除外と nested memo 対象化、merge 時のインデックス衝突解消を検証する。
- Codex 実行を monkeypatch して構造化されたエントリー生成結果を返させ、インデックス更新・コミット対象・作業ツリー清潔性・エラー出力を外部挙動として確認する。

## Read this when
- インデックス生成コマンドの実行条件、失敗条件、コミット挙動、linked worktree での対象 root 判定を変更する。
- インデックスエントリーの fresh 判定、malformed entry の再生成、semantic field の検証、空リストや空文字の rendering 挙動を変更する。
- インデックス更新対象の探索、兄弟エントリーの並列生成、root 直下 memo の除外、下位階層にある memo の扱いを変更する。
- merge conflict 解消時にインデックスファイルを削除して merge commit を成立させる処理を変更する。

## Do not read this when
- 通常のサブコマンド登録、CLI 全体の起動構造、runner fixture の基本だけを確認したい場合は、より直接それらを定義する実装または support test を読む。
- インデックスエントリーの文章品質や Codex の生成内容そのものを評価したい場合は、このテストではなく生成プロンプトや schema 側を読む。
- oracle file の正本仕様を確認したい場合は、この realization test ではなく oracle 側の該当文書を読む。

## hash
- 5c4faf3c479e5af409849ec66e7b3812ef40afb42c408c39ca95c462100914e4

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
- プロンプト構成部品と関連する実行パラメータ builder のテストをまとめた realization test。構造化ドキュメントの Markdown レンダリング、routing rule や各種 standard の挿入条件、file access rule の mode 別文言、apply fork・TUI parameter・review oracle・session join 向け parameter の model/reasoning/file access/schema 連携を検証する。

## Read this when
- プロンプト本文に routing rule、oracle/realization/review/apply/index standard、補助プロンプト、コードブロックが期待通り含まれるかを変更・確認する時。
- StructDoc や StructCodeBlock の Markdown 出力、連続空行の畳み込み、コードブロック内空行の扱いを変更・確認する時。
- FileAccessMode ごとの file access rule 文言や、apply fork・TUI resolve parameter・review oracle merge finding・session join conflict resolution の parameter 属性や schema 参照を変更・確認する時。
- index entry 生成用 parameter の model class、reasoning effort、readonly mode、または index entry standard の出力文言を変更・確認する時。

## Do not read this when
- 個別 CLI コマンドの実行挙動、永続状態操作、git 操作そのものの仕様や実装を調べたいだけの場合。
- プロンプト部品 builder の期待出力ではなく、アプリケーション本体の business logic や UI 表示を調べたい場合。
- oracle 側 schema の正本内容そのものを確認したい場合は、schema を複製利用しているテストではなく、対応する oracle source を直接読む。

## hash
- 57e3e687f4af40dd694ca83b3b3730794006e91f78cb93112920a999da73754a

# `test_review_oracle_cli.py`

## Summary
- `review oracle` サブコマンドの実行フローとレポート生成を、Typer runner と一時 Git リポジトリで検証する realization test。通常完了、対象なし、処理失敗、短縮オプション、linked worktree 上のセッション branch と oracle の扱いを含む。
- oracle レビューで列挙・検証・判定に渡す Codex 呼び出しを fake に差し替え、structured output schema ごとの制御分岐、対象 oracle の選別、レビュー用 worktree で生成されたルーティング文書の取り込みを確認する。
- finding の merge operation 適用ロジックについて、delete・replace・merge の契約、採番、初期フィールド付与、不正 operation の拒否を単体で検証する。
- oracle 配下の binary file、gitignore 対象ファイル、セッション差分、INDEX.md 競合解決、レビュー中に生成された想定外差分の拒否など、`review oracle` が扱う境界条件をまとめて検証する。

## Read this when
- `review oracle` の対象 oracle 選別、scope 指定、レポート内容、Codex 呼び出し回数や purpose、linked worktree での実行挙動を変更・調査するとき。
- レビュー処理が生成した INDEX.md だけを session worktree へ取り込む挙動、INDEX.md 競合解決、レビュー用 worktree の配置や cleanup に関わる実装を変更するとき。
- finding merge operation の契約、finding_id の再採番、validate・judge 前後の finding 状態を扱うロジックを変更するとき。
- oracle レビュー中のエラー報告、対象なしレポート、gitignored oracle file の除外、binary oracle file の対象化、想定外の作業ツリー差分拒否を確認したいとき。

## Do not read this when
- `review oracle` 以外の CLI サブコマンドや session 操作そのものの基本挙動だけを調べるときは、より直接その機能を検証するテストを読む。
- Codex 実行ラッパー、設定モデル、Git helper、path model などの個別 API の実装詳細だけを調べるときは、それぞれの実装または単体テストを読む。
- oracle 正本仕様の内容やルーティング文書の記述規約そのものを確認したいときは、このテストではなく oracle file を読む。
- 一般的な pytest fixture や一時リポジトリ作成 helper の使い方だけを確認したいときは、共通テスト支援コードや該当 helper の利用箇所を読む。

## hash
- 971097a7295ff76cdcf84a1405d5c1c474a6fd606faa7ca4e835ad73d82e464c

# `test_session_cli.py`

## Summary
- セッション系 CLI の realization test であり、fork、abandon、join が Git ブランチ、linked worktree、セッション状態ファイル、標準出力、競合解決時の Codex 実行権限に与える外部挙動を検証する。
- セッションブランチの作成・削除、home branch への復帰、join 後の状態更新、削除競合の staging、ブランチ削除失敗時の警告など、セッション操作の統合的な期待挙動を確認する入口になる。

## Read this when
- session fork、session abandon、session join の CLI 挙動、出力、終了コード、Git branch 操作、またはセッション状態 JSON の生成・更新を変更するとき。
- linked worktree 上でセッション操作した場合に、root worktree と linked worktree の現在ブランチや HEAD をどう扱うかを確認したいとき。
- session join の競合解決で Codex 実行に渡す file access mode、書き込み許可、read-only 対象、または競合解消後の staging を確認・変更するとき。
- session abandon の失敗時ロールバック、home branch 不在時の失敗出力、cleanup 失敗時の再実行案内を確認・変更するとき。
- session join 後に session branch を削除できない場合の成功扱いと警告出力を確認・変更するとき。

## Do not read this when
- init コマンド単体、設定ファイル読み込み、path model、またはセッション操作を伴わない一般的な Git helper の挙動だけを調べるとき。
- oracle file や realization file の定義、INDEX.md 生成規則、またはルーティング文書そのものの仕様を確認したいとき。
- session 以外のサブコマンドの CLI 出力や状態遷移を調べる場合で、fork、abandon、join のブランチ・状態ファイル挙動に関係しないとき。
- Codex CLI や LLM の出力品質そのものを検証したいとき。このテストは join 競合解決で渡す権限と副作用を fake 実行で確認しているだけである。

## hash
- 3a0eaf0b33b63a15ac5b335cd6b59ed96c60a488715fc01181be60f72fa9dd3a
