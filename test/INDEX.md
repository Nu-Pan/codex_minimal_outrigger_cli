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
- active apply run を破棄する CLI 挙動のテスト群。apply worktree と branch の cleanup、state の ready 復帰、missing target の warning、running process の停止、実行位置ごとの安全判定をまとめて検証する。
- running apply process の pidfd 経由停止に関する制御ロジックも含み、PID 再利用や既に終了した process を誤って扱わないことを確認する。

## Read this when
- apply abandon の外部挙動、出力、終了コード、state 更新、worktree/branch 削除を変更または確認したいとき。
- apply abandon が running 状態を扱う処理、process id の読み取り・削除、process 停止、stale PID 判定に関わる変更をするとき。
- apply worktree 内、linked session worktree、stale apply branch など、実行位置による abandon 可否や復帰先 cwd の挙動を確認したいとき。
- active apply run の cleanup 対象が既に存在しない場合の warning 扱い、または cleanup 前に拒否すべき失敗条件を確認したいとき。

## Do not read this when
- apply abandon 以外の apply サブコマンド、session fork、init などの基本動作だけを確認したいとき。
- apply run の作成・実行・成功判定そのものを調べたいとき。abandon 前提の state と cleanup 境界だけが関心でないなら、より直接のテストや実装を読む。
- CLI を介さない汎用的な git helper、path model、INDEX 生成規則を調べたいとき。
- process 停止の OS 依存 helper 単体ではなく、他サブコマンドの process 管理全般を調べたいとき。

## hash
- 236d85fa1945b2c81705e9be26795d22180a7fc5fa6c400d1d509ee224972c4e

# `test_apply_fork_cli.py`

## Summary
- apply fork サブコマンドの実行ループ、apply run の状態更新、worktree 配置、branch 作成、設定読み込み失敗時の中断、.gitignore と .cmoc の扱い、対象 path 正規化を検証する realization test。
- Codex 実行は fake に差し替え、CLI 呼び出し、git 状態、session state、apply branch の内容を通じて外部挙動と制御ロジックを確認する。

## Read this when
- apply fork の正常完了時に session state が completed へ更新されること、apply branch と apply worktree が run ごとの場所に作られることを確認したいとき。
- linked worktree 上で開始した session branch と HEAD を apply run の起点にする挙動を変更・確認するとき。
- apply fork が session 側の .gitignore 表現を書き換えないこと、追跡済み .cmoc を session 側で解除しないこと、.gitignore を apply branch 側の所見対象として編集できることを確認するとき。
- cmoc config の欠落や不正 JSON で apply run の branch/state/pid を開始しない失敗時挙動を扱うとき。
- apply target 正規化で root 直下 memo を除外し、入れ子の memo directory は対象に残す挙動を確認するとき。

## Do not read this when
- apply fork 以外のサブコマンドの CLI 挙動や session 作成そのものを調べたいとき。
- Codex 実行結果の品質、実 LLM の出力内容、prompt 本文を検証したいとき。
- apply fork の実装詳細を変更したいが、まず仕様・実装本文から制御フローや helper の責務を確認する必要があるとき。
- root 直下 memo の読み書き禁止に関する一般規則だけを確認したいとき。

## hash
- 0d3122fa9d55794b144b6a466a0b2cc8dc1fe1421a38083a958fb885751dcb0b

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
- apply run を session へ join する CLI 外部挙動を検証する realization test。成功時の apply worktree と apply branch の後片付け、state 更新、join report 生成を確認する。
- apply worktree からの join、stale apply branch の拒否、dirty apply worktree の拒否、想定外差分、force resolve、merge conflict 処理など、同じ join 操作の正常系と拒否条件をまとめて扱う。

## Read this when
- apply join の CLI 挙動、終了コード、標準出力・標準エラー、report 生成、state 遷移、worktree・branch cleanup を変更または確認したいとき。
- apply fork 後の state を前提にした join の成功条件や、dirty worktree、stale branch、想定外差分、merge conflict による拒否条件をテストで確認したいとき。
- apply join を session worktree と apply worktree のどちらから実行しても正しく扱えるかを確認したいとき。

## Do not read this when
- apply fork 自体の Codex 実行、apply run の生成、または fork の state 初期化だけを確認したいとき。
- session fork、init、git helper、テスト fixture の一般的な仕組みを調べたいだけで、apply join の外部挙動に関心がないとき。
- oracle file の正本仕様や INDEX.md 生成規則を確認したいとき。

## hash
- 031e0217a85ce5aa4a3171fa1b66dcbae5f0c3ae32ecdffb20224d5d3d2691c6

# `test_basic_runtime.py`

## Summary
- cmoc の基本的な runtime 挙動を横断的に検証する realization test。path token 解決、run/work/repo root 判定、設定既定値、エラー markdown 表示、branch session id の形、CLI エラー出力先、completion probe 時の副作用抑止、`.cmoc` ignore、file access mode と Codex sandbox profile、binary 判定を扱う。
- 単一機能の詳細テストというより、basic・runtime・state・config・profile・CLI 起動前後の境界挙動が実装上の互換性を保っているかを確認する入口として位置づく。

## Read this when
- path token、`<cmoc-root>` 表示、linked worktree と main worktree の判定、run root・work root・repo root の扱いを変更または確認する時。
- CLI の preflight、引数解析失敗、detached HEAD、work root 外実行、shell completion probe など、エラーの出力先や副作用の有無を確認する時。
- `CmocError` の markdown 表示、next actions の補完、call stack の root token 表示を変更する時。
- session/apply branch 名から session id を取り出す処理、または branch に基づく状態読み込みの失敗条件を扱う時。
- `.cmoc` を `.gitignore` に登録する処理、既存 ignore pattern がある場合の追記挙動、git による ignore 確認を扱う時。
- file access mode、sandbox mode、Codex profile の `sandbox_workspace_write`、oracle や memo など追加 writable path の扱いを変更する時。
- 初期 chunk だけで binary 判定する処理や、config の model class・reasoning effort 既定値を確認する時。

## Do not read this when
- 個別サブコマンドの通常系 workflow や成果物内容を調べたいだけで、runtime の共通境界・エラー・sandbox・状態 ID 判定に関わらない時。
- oracle file の正本仕様や自然言語ドキュメントの意図を確認したい時。対象は realization test なので、仕様判断の根拠としては oracle 側を先に読む。
- 特定 module の内部 helper 実装だけを局所的に変更し、その変更がここで扱う root 判定、CLI preflight、error rendering、state branch、sandbox profile、ignore 設定に影響しない時。
- テスト支援用の repo 作成・git 実行・runner fixture 自体の詳細を調べたい時は、支援 module を直接読む方が適切。

## hash
- fac2f0c72ddbb533eb5ed29f01377e385f136d8feab70ed802e9871567550d5c

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
- Codex CLI 呼び出しランタイムのテスト群。exec 実行での標準入力受け渡し、プロファイル生成、JSON/schema 出力、ログ保存、作業ディレクトリ別の schema 保存先、禁止領域変更検出、TUI 起動、リポジトリ設定反映を検証する。
- 外部の実 Codex ではなく一時的な fake executable や monkeypatch を使い、cmoc 側が Codex コマンドへ渡す argv/env/cwd と、生成されるログ・プロファイル・戻り値を観測する。

## Read this when
- Codex CLI を呼び出すランタイム処理、exec/TUI の起動引数、標準入力での prompt 受け渡し、`CODEX_HOME` や一時 profile の扱いを変更する時。
- Codex 呼び出しログ、prompt/stdout/stderr/call log、subcommand logger の `codex_call` event、コンソール表示の仕様に関わる実装を確認・変更する時。
- Structured Output schema の保存場所、`cwd` が worktree の場合の `.cmoc/state/schema` 配置、`--output-schema` 引数の扱いを調べる時。
- Codex 実行後に `.agents` 配下の変更を拒否する制御、またはリポジトリ設定から model/reasoning effort を profile に反映する制御を扱う時。

## Do not read this when
- Codex CLI 呼び出し以外のサブコマンド、通常の git 操作、oracle/realization の概念仕様など、ランタイムの Codex 起動経路に直接関係しない挙動だけを調べる時。
- fake executable や monkeypatch を使わない高水準の CLI 入出力テスト、または実際の Codex/LLM 出力品質そのものを検証したい時。
- 設定 schema や path model の定義そのものを確認したい場合は、実装・仕様側の設定/パス定義を先に読む方が適切。

## hash
- a45a5384d0bae827221451f39faf534c455530feb524501ee20bfbdd1ea0ffd9

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
- Codex 実行中に quota exceeded が発生した場合の再試行制御を検証する realization test。quota 回復確認用 probe、thread_id が得られた場合の resume、thread_id が無い場合の通常再実行、並行実行時に代表 probe を 1 回だけ使う制御、call log と subcommand log の記録内容を扱う。

## Read this when
- Codex CLI 呼び出しで quota exceeded 後に待機・probe・resume・再実行する挙動を変更または確認したいとき。
- quota availability probe の argv、stdin、output-last-message、ログ出力、profile_name、stdout/stderr/prompt/output の記録を検証したいとき。
- 複数の run_codex_exec 呼び出しが同時に quota exceeded になった場合の probe 集約や各呼び出しの resume 挙動を確認したいとき。
- run_codex_exec の結果に返る output_json や call_log_path が、quota 後の成功した実行に対応しているかを確認したいとき。

## Do not read this when
- quota exceeded と無関係な通常の Codex 実行成功・失敗処理だけを確認したいとき。
- Codex CLI の実体や LLM 出力品質そのものを検証したいとき。
- リポジトリ作成、CODEX_HOME 設定、fake executable 作成などの共通テスト補助だけを調べたいときは、対応するテスト支援コードを直接読む。
- quota retry の外側にある設定読み込み、ACP パラメータ定義、パスモデルの仕様を調べたいときは、それぞれの実装または oracle を直接読む。

## hash
- 303b529189ac45b682b005b08c2e429e53edf2d1d0367c1180715e88428a8c71

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 実行ラッパーの retry 制御に関する realization test。schema validation 失敗後の再実行、capacity エラー時の再実行、JSONL イベント外に出た capacity/quota 風メッセージを retry 条件として扱わないことを、fake codex 実行ファイルとログ検証で確認する。
- run_codex_exec が返す output_json、call log、prompt/stdout log、SubcommandLogger の codex_call イベント status・returncode・error detail まで含めて、retry 判定とログ記録の外部挙動を検証する入口になる。

## Read this when
- Codex CLI 呼び出しの retry 条件、特に schema validation retry、capacity retry、quota/capacity marker の判定範囲を変更・調査するとき。
- run_codex_exec の call log、prompt log、stdout log、SubcommandLogger の codex_call イベントに記録される status、returncode、error、call_log_path の期待値を確認するとき。
- fake codex executable を使った runtime 系テストの作り方や、Codex CLI の失敗・成功シナリオを tmp_path と monkeypatch で再現する既存パターンを参照するとき。

## Do not read this when
- Codex CLI の通常のコマンドライン引数組み立て、設定読み込み、ファイルアクセス制御など、retry 判定以外の実行準備を調べたいとき。
- Codex CLI や LLM の出力品質そのもの、生成内容の妥当性、プロンプト文面の設計を検証したいとき。
- oracle file 側の正本仕様断片を確認したいとき。この対象は realization test であり、正本仕様ではない。

## hash
- 274bcf39312389cb9c5e78f6b382ac3f48de31bc278ef7df3e5adefee1e0a87d

# `test_indexing_cli.py`

## Summary
- indexing サブコマンドと INDEX 生成処理の realization test。競合した INDEX の解決、未初期化・dirty repo・linked worktree・apply worktree での実行条件、生成済み hash による再生成スキップ、INDEX だけを commit する制御、entry 検証、兄弟 entry の並列生成、root 直下 memo 除外とネストした memo の扱いを検証する。

## Read this when
- indexing サブコマンドの外部挙動、git commit 副作用、preflight 実行、worktree 上での対象 root 判定を変更・確認する時。
- INDEX entry の生成・描画・検証、fresh hash 判定、malformed entry の再生成条件、Codex 呼び出し有無を変更・確認する時。
- INDEX 生成対象の走査ルール、root 直下 memo の除外、ネストした memo の indexing、同階層 entry 生成の並列化を変更・確認する時。

## Do not read this when
- Codex 実行パラメータや indexing 実装の内部構造だけを確認したい場合は、実装側の indexing モジュールを先に読む。
- apply join の merge conflict 解決全般を確認したい場合は、INDEX conflict 解決に関係する場合を除き、apply 側の実装や専用テストを読む。
- INDEX.md ルーティング文書の記述方針や schema そのものを確認したい場合は、この realization test ではなく該当する仕様・schema を読む。

## hash
- c1123c66f6e79096a88f5adf228d07d9dfbbeffda0ccff69a6284277dc22988b

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
- prompt 構築と ACP builder の生成結果を横断的に検証する realization test。標準 prompt、routing、file access、各種 standard の注入、structured output schema、builder parameter の model/reasoning/file access mode など、最終 prompt と schema の回帰観点を一箇所で扱う。
- agent prompt と structured output schema は同じ読み取り文脈で組み合わさるため、分割せず凝集した検証対象として維持していることが冒頭 docstring に明示されている。

## Read this when
- prompt parts の markdown rendering、空行の畳み込み、補助 prompt の保持、standard 文書の注入有無や用語保持を変更・確認する。
- routing rule、file access rule、apply/review/oracle/realization/index entry standard の生成内容に期待する主要文言を確認する。
- ACP builder が返す実行 parameter の model class、reasoning effort、file access mode、prompt 内容、structured output schema path を変更・検証する。
- change summary、TUI resolve parameter、review oracle merge finding などの JSON schema の required、enum、validation 制約、oracle source との一致を確認する。
- apply fork、session join、indexing、review oracle 系 builder の prompt root 表現や conflict 対象表現に関する回帰を調べる。

## Do not read this when
- 個別 builder や prompt part の実装詳細だけを調べたい場合は、対応する実装側の本文へ直接進めばよい。
- 単一の standard 文書の仕様文そのものを確認したいだけなら、その standard を生成する prompt part または正本仕様断片を読む方が直接的である。
- テスト基盤全体、fixture 配置、または他領域の CLI 挙動を調べる場合は、この横断 prompt/schema 回帰テストから読み始める必要はない。
- INDEX.md エントリー生成の出力形式だけを確認したい場合は、schema や呼び出し側の定義を読む方が適切である。

## hash
- bb67d485ed7b785f5db46a62bc309dd6bb4c96042e783aa6215cbc39f195f665

# `test_review_oracle_cli.py`

## Summary
- review oracle の CLI 経由の外部挙動と、所見評価 loop の制御を検証する realization test。report 生成、対象 oracle の選択、所見の列挙・検証・judge・merge、結果分類、上限やエラー時 report、review 用 worktree と join commit、INDEX.md 差分の取り扱いを同じ review run の文脈で確認する。
- ファイル自体は大きいが、fake Codex 応答と report 文脈を共有する oracle review の一連の挙動確認に責務を閉じており、分割より同じ読み取り文脈に集約する意図がある。

## Read this when
- review oracle コマンドの report 出力、結果判定、所見の並び順、fatal/minor/reject/accept の集計表示を変更・確認したいとき。
- review oracle の対象ファイル選択を扱うとき。特に full scope と session scope、gitignored oracle、binary、symlink、memo 配下や memo 風パス、linked worktree 上の oracle の扱いを確認したいとき。
- 所見評価 loop の Codex 呼び出し順、enumerate に渡す既存所見の範囲、validate・judge・merge の制御、merge operation の契約や不正 operation の拒否を変更・確認したいとき。
- review oracle が作成した INDEX.md 変更の取り込み、join commit の report 記録、review worktree の配置、conflict 解決、INDEX.md 以外の差分を拒否して元 worktree を汚さない挙動を確認したいとき。
- review oracle の処理途中失敗時に error report を残し、CLI の stdout/stderr と終了コードをどう扱うかを確認したいとき。

## Do not read this when
- oracle review ではない通常の session 操作、init、run 管理、設定読み込みだけを確認したいとき。
- review oracle の内部 helper の局所実装だけを調べたい場合で、外部挙動や loop 全体の期待値を確認する必要がないとき。
- Codex CLI や LLM の出力品質そのものを評価したいとき。このテストは fake 応答を使い、cmoc 側の制御と出力を検証する。
- oracle file の正本仕様本文を確認したいとき。この対象は realization test であり、仕様判断は oracle file を直接読む必要がある。

## hash
- a56fbc01dc7664e00bd1dcdcb2c9972636d41388634d73df7de29222d6c6af0b

# `test_session_cli.py`

## Summary
- session サブコマンドの CLI 挙動を検証する realization test。session fork による session branch・状態ファイル作成、.cmoc ignore 初期化、linked worktree 上の branch/head 取り扱いを確認する。
- session abandon の正常系・linked worktree 対応・home branch 不在時の失敗・cleanup 失敗時の rollback と stderr/stdout 出力境界を検証する。
- session join の正常系・linked worktree 対応・oracle conflict 解決時の Codex 実行 profile・conflict marker 判定・delete conflict 解決・session branch 削除失敗時 warning・未コミット差分エラー出力を検証する。

## Read this when
- session fork、session abandon、session join の CLI 外部挙動、git branch/worktree 操作、session state の生成・更新・削除失敗時挙動を変更または確認するとき。
- session join の conflict resolution、REALIZATION_WRITE profile、oracle file 競合時の書き込み許可範囲、conflict marker 検出、delete conflict staging を調べるとき。
- session サブコマンドのエラー報告が stdout と stderr のどちらへ出るべきか、成功時・失敗時の出力項目が何を保証しているかを確認するとき。
- linked worktree 上で session 操作を実行した場合に、main worktree と linked worktree の current branch がどう保たれるべきかを確認するとき。

## Do not read this when
- session 以外のサブコマンド、設定読み込み、path model、oracle 文書構造など、session CLI の外部挙動に関係しない領域だけを扱うとき。
- session state や git branch/worktree 操作に触れない内部 helper の小変更で、既存の session CLI 契約を確認する必要がないとき。
- Codex 実行 profile 一般、FileAccessMode 一般、CmocConfig 一般の詳細だけを調べたいとき。session join の conflict resolution 経由の利用でなければ、より直接の実装または単体テストを読む方がよい。

## hash
- 6f05d7cfd0850a2c8bd2d0efd834c1b7417af7579f311a191520d26048f3ed68
