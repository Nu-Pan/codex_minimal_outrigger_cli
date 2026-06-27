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
- 基礎ランタイム周辺の realization test。パストークン解決、run/work/repo root 判定、既定設定、構造化エラー表示、session/apply ブランチ形状、CLI 失敗時出力、補完プローブ時の副作用抑制、`.cmoc` ignore、ファイルアクセス mode と Codex sandbox profile、binary 判定を横断的に検証する。
- 複数の基礎モジュールと CLI 境界の統合的な期待挙動を、小さな一時 git repository や Typer runner、subprocess を使って確認する入口になる。

## Read this when
- 基礎ランタイム、パスモデル、root 判定、`.cmoc` worktree、または `<cmoc-root>` 表示に関する挙動を変更・確認する時。
- 構造化エラーの markdown 出力、CLI parse error/preflight error の stdout/stderr 振り分け、補完プローブ時の preflight skip や副作用抑制を扱う時。
- session/apply ブランチ名から session id を解釈する処理、状態ファイル読み込み、invalid branch shape の拒否条件を確認する時。
- file access mode、sandbox mode 変換、Codex profile の writable roots/read-only 設定、または repo/oracle/realization 書き込み権限の profile 生成を変更する時。
- `.gitignore` への `/.cmoc/` 追加、既存 ignore pattern との関係、または binary 判定の読み取りサイズを検証する時。

## Do not read this when
- 個別 CLI command の正常系 workflow や user-facing output を詳しく追う必要があり、対象がここで扱う preflight/error/completion 境界ではない時。
- agent 呼び出し、ログ生成、prompt 構築、または oracle/realization 文書処理など、基礎ランタイムの境界設定以外の詳細実装だけを調べたい時。
- 単一モジュールの純粋な unit 挙動を狭く確認でき、CLI runner、subprocess、一時 git repository を伴う統合的な回帰確認が不要な時。

## hash
- bac188dcb9c61cb8172515a6848331515a88206236e1f292928e6912412d8c61

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
