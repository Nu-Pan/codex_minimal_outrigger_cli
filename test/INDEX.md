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
- active apply run を破棄する CLI 挙動の realization test。apply abandon が apply worktree・apply branch・session state・process id file を cleanup し、running process を停止し、成功時の出力と警告、失敗時の保護条件を外部挙動として検証する。
- 16,000 文字を超えるが、active apply run の破棄に関する worktree/branch/state cleanup、実行位置判定、running process 停止が同じ state fixture と境界条件を共有するため、一箇所で読む前提の凝集したテスト群である。

## Read this when
- apply abandon の成功時に、apply worktree と apply branch が削除され、apply state が ready に戻り、cleanup 対象が出力される挙動を確認・変更する場合。
- cleanup 対象の worktree や branch が既に存在しない場合に、失敗ではなく warnings として報告しつつ state を ready に戻す挙動を扱う場合。
- running 状態の active apply run を abandon する際、保存済み process identity を使って process 停止を cleanup 前に行い、process id file と state 上の process 情報を消す挙動を確認する場合。
- process 停止 helper の pidfd signal、race した終了、既に終了した process、PID reuse の扱いを変更する場合。
- running 状態なのに process id を特定できない時や、apply branch から worktree を導けない時に、cleanup せずエラー終了する保護条件を確認する場合。
- apply worktree や linked session worktree から apply abandon を実行した時に、実行後の cwd、repo state の参照元、dirty linked session worktree の拒否、stale apply branch の拒否を確認する場合。

## Do not read this when
- apply fork が Codex 実行結果をどう生成・保存するかだけを確認したい場合。apply abandon の前提 state を作るための範囲を超える fork の詳細は、fork 側の実装・テストを読む方が直接的である。
- session fork 自体の branch 作成、session id 生成、session state 初期化の仕様を確認したい場合。この対象では apply abandon の fixture 準備としてのみ扱う。
- git worktree や branch 操作の低水準 helper の一般仕様を確認したい場合。ここでは active apply run 破棄時の外部挙動としての副作用だけを検証している。
- INDEX.md 生成、oracle/realization の分類、ルーティング文書の規則を確認したい場合。この対象は apply abandon の CLI テストであり、ルーティング仕様の本文ではない。

## hash
- 4954c5f92c0ad1745e6964a01c20c943a8c0198981ecfb112fed315505d4249c

# `test_apply_fork_cli.py`

## Summary
- apply fork コマンドのテスト群。Codex 実行を fake に差し替え、apply run の完了状態、apply branch と worktree の作成先、session state の更新、pid など旧状態項目の不在、所見列挙呼び出しを検証する。
- linked worktree 上で開始した session branch と HEAD を apply run の起点にすること、session 側の既存 ignore 表現を壊さず必要時は git exclude で `.cmoc` を ignore して clean に保つこと、設定読み込み失敗時に apply run を開始しないことを確認する。
- 所見対象として `.gitignore` を apply branch 側で編集できること、apply 対象正規化で root 直下の private な memo を除外しつつ入れ子の memo directory と binary file を残すことを検証する。

## Read this when
- apply fork の CLI 挙動、state 遷移、apply branch/worktree の配置、完了時の後始末に関するテストを確認・変更したいとき。
- linked worktree からの apply fork、session 側 `.gitignore` の保持、`.cmoc` ignore の付与方法、設定ファイル読み込み失敗時の rollback 境界を扱うとき。
- apply 対象の列挙・正規化、`.gitignore` を所見対象に含める挙動、root 直下 memo の除外と入れ子 memo/binary file の扱いを検証したいとき。

## Do not read this when
- apply fork 以外の apply サブコマンド、review、session fork、init などの CLI 挙動を調べたいだけのとき。
- Codex CLI や LLM 出力品質そのもの、実際の Codex 実行内容、所見 schema の詳細を確認したいとき。
- 実装本体の制御フローや helper の責務を変更するために読む場合で、まず対応する実装モジュールや正本仕様断片から確認すべきとき。

## hash
- 8f80ee95c01fc38152054a76eeb0c86ea80176eb50ca170fdabd61c01aa18bed

# `test_apply_fork_report_cli.py`

## Summary
- apply fork の CLI 実行を通じて、所見列挙から適用、commit、変更要約、report 生成、session state 更新までの制御を検証する realization test。
- 収束、未収束、error、変更ファイル再調査、編集禁止対象の差分検出、rolling apply fork の対象選定を、同じ loop と report schema の観測結果としてまとめて扱う。
- 16,000 文字を超えるが、apply fork report の期待値文脈を一箇所に保つため、分割せず凝集性を優先している。

## Read this when
- apply fork の report 内容、終了コード、収束判定、未収束判定、error report の挙動を確認・変更したいとき。
- apply fork が Codex 応答から所見を列挙し、所見適用後に commit message と変更要約を生成し、apply branch と session state を更新する流れを検証したいとき。
- apply 後の変更ファイル再調査、INDEX.md の再調査除外、差分なし適用時の扱い、調査対象なしの場合の report 表示を確認したいとき。
- 編集禁止対象への差分が検出された場合に、error state、stderr、report、未 commit 差分を含む変更要約がどう扱われるかを確認したいとき。
- rolling apply fork が前回 apply join 後の変更だけを対象にする制御を確認したいとき。

## Do not read this when
- apply fork 以外の apply join、session fork、init などの個別コマンド実装そのものを調べたいとき。
- report renderer や session state 永続化の内部 helper 単体の詳細だけを確認したいとき。
- Codex CLI や LLM の実出力品質を検証したいとき。ここでは fake 応答を使って cmoc 側の制御と観測結果を検証している。
- 一般的な test fixture、repository 作成 helper、git wrapper、CLI runner の使い方だけを調べたいとき。

## hash
- 931332ad9a54f022bfb36dfbc9c3724c8948a76d18f73b1dd4efba82900895cc

# `test_apply_join_cli.py`

## Summary
- apply run を session へ join する CLI 経由の外部挙動を検証する realization test。成功時の apply worktree と branch の削除、state 更新、report 生成、apply worktree や linked session worktree からの実行、dirty worktree・stale branch・想定外差分・merge conflict での拒否や継続条件を扱う。
- 16,000 文字を超えるが、apply join の成功条件と拒否条件を同じ fixture と git 状態の文脈で読む必要があるため、単一の join 操作に関する境界条件としてまとまっている。

## Read this when
- apply join の CLI 挙動、終了コード、標準出力、report 内容、state の apply/session 更新を変更または確認したいとき。
- apply join 成功時の apply worktree cleanup、apply branch 削除、last joined oracle snapshot commit の記録を確認したいとき。
- apply worktree、session worktree、linked session worktree のどこから join を実行するかによる merge 先や cwd 復帰の挙動を確認したいとき。
- dirty な apply worktree、現在 branch と state 上の apply branch の不一致、想定外の apply diff、削除・rename・gitignore 変更、merge conflict の扱いを確認したいとき。
- apply join の unexpected changes 検出や managed branch 上の変更 path 抽出に関するテストを探しているとき。

## Do not read this when
- apply fork が Codex 実行結果から apply worktree や state を作るまでの挙動だけを確認したいとき。
- session fork、init、path model、ログ基盤など apply join の成否判定に直接関係しない CLI 挙動を確認したいとき。
- 実装側の join 処理、unexpected changes の収集ロジック、git 操作 helper の詳細を変更したいだけで、外部 CLI テストの期待値をまだ確認する必要がないとき。
- oracle file の正本仕様を確認したいとき。この対象は realization test であり、正本仕様ではない。

## hash
- dc6edf08dc6b464905021255fc0873e24a0f1a9c443a2f49deb2016657a08334

# `test_basic_runtime.py`

## Summary
- 基本的なランタイム挙動を横断的に検証する realization test。path token 解決、run/work/repo root 判定、既定設定、構造化エラー表示、CLI エラー出力先、補完 probe 時の副作用抑制、`.cmoc` ignore、file access mode から sandbox/profile への変換、binary 判定の読み取り範囲など、低層の共通契約をまとめて扱う。
- 個別サブコマンドの正常系シナリオよりも、CLI 全体の前提条件・失敗時表示・sandbox 設定・状態 branch 名の妥当性といった基盤的な外部挙動を確認する入口になる。

## Read this when
- path token、`<run-root>`、linked worktree、repo root/work root の解決挙動を変更・確認する。
- `CmocConfig` の既定 model class、reasoning effort、parallel 数など、基本設定の初期値を変更・確認する。
- `CmocError` の markdown 表示、next action 補完、call stack 表記、CLI parse/preflight error の stdout/stderr 出力先を変更・確認する。
- session/apply branch 名から session id を取り出す検証、または不正 branch shape の拒否条件を変更・確認する。
- CLI completion probe、missing venv 時の起動 wrapper 表示、`.cmoc` の `.gitignore` 登録など、CLI 起動前後の副作用や補助ファイル操作を変更・確認する。
- file access mode の JSON 値、sandbox mode 変換、Codex profile の sandbox_workspace_write 構成、extra writable path の扱いを変更・確認する。
- binary 判定が先頭 chunk だけを読む制御を変更・確認する。

## Do not read this when
- 特定サブコマンドの詳細な成功フロー、出力内容、永続状態更新だけを調べたい場合は、そのサブコマンド専用のテストや実装を直接読む。
- oracle file の正本仕様を確認したい場合は、realization test ではなく対応する oracle doc または oracle src/test を読む。
- 個別 helper の内部実装だけを変更し、ここで検証される外部挙動や共通契約に影響しないことが明確な場合は、対象実装とより近い単体テストを優先する。

## hash
- 6d8f163e0118264e2480925093c18c937cbd7bd2f864dd1f2ee2474671b5071f

# `test_cli_init_tui.py`

## Summary
- CLI の初期化処理と対話型依頼入力の外部挙動を検証する realization test。Git 管理下の既存状態を壊さず `.cmoc` を無視対象化すること、初期設定を作成・同期すること、サブコマンド実行ログを残すこと、linked worktree ではリポジトリ実体と作業ツリー側の保存先を使い分けることを扱う。
- 対話型入力ではエディタで作成された Markdown 依頼を補完済みプロンプトへ変換し、parameter 解決用の Codex 実行と本処理用 Codex TUI 実行へ適切な引数・権限・追加 read path を渡す挙動を検証する。
- Markdown prompt parser について、fenced code block 内の見出し風行を見出し扱いしないことと、最初の見出しより前の本文を保持することも検証する。

## Read this when
- 初期化サブコマンドが `.cmoc` 配下の追跡解除、`.gitignore` 更新、cleanup commit、既存 staged/unstaged 変更の保護、既定設定 JSON の作成・同期をどう扱うべきか確認したいとき。
- linked worktree 上で初期化または対話型入力を実行した場合に、設定・ログ・schema・補完済みプロンプトの保存先や git status への影響を確認したいとき。
- 対話型入力サブコマンドがエディタ起動後の Markdown 依頼から不要コメントを除去し、解決済み parameter に基づいて Codex TUI を起動する制御ロジックを変更・検証するとき。
- Markdown prompt parser の見出し分割、fenced code block、preamble の扱いに関する期待挙動を確認するとき。

## Do not read this when
- 初期化や対話型入力ではないサブコマンドの CLI 挙動を調べたいだけのとき。
- 設定値の型定義や path model など、実装側のデータ構造そのものを確認したいとき。
- Codex 実行 wrapper の汎用的な引数構築や preflight の詳細を調べたいとき。
- Markdown parser の実装方式そのものを読みたいとき。

## hash
- 64e6ca7a1377ad17cdf2861ae884a6815a0239a6e99e63bc08b9fe51dbfa28b5

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
- indexing サブコマンドと indexing preflight、INDEX.md 更新・コミット、既存エントリーの再生成判定、Codex 実行呼び出し、merge 時の INDEX.md conflict 解決を検証する realization test。
- git worktree 上での indexing 対象、未初期化・未コミット差分・fresh hash・malformed entry・semantic field validation・並列エントリー生成・memo ディレクトリ除外境界を扱う。

## Read this when
- indexing の CLI 挙動、preflight 挙動、INDEX.md 生成・更新・コミットの制御ロジックを変更または確認したいとき。
- INDEX.md conflict 解決、index entry の schema validation、fresh hash による Codex 呼び出し省略、兄弟要素の並列生成に関する回帰テストを探すとき。
- root worktree と linked/apply worktree で indexing がどの repository/config を使うべきかを確認したいとき。
- root 直下の memo は indexing 対象外だが、下位階層の memo は対象になり得る境界を確認したいとき。

## Do not read this when
- indexing 以外のサブコマンドや一般的な CLI 初期化だけを調べたいとき。
- INDEX.md エントリー本文の生成ルールそのものではなく、oracle の正本仕様断片を確認したいとき。
- 実装詳細を変更せず、既存テストの失敗原因が indexing と無関係な git 操作・設定読み書き・共通 test helper にあると分かっているとき。

## hash
- 97096bb1f4549b7d80702640aceb98fe2d8bc8774490bff8b39fe3119035167d

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
- prompt 構成部品、file access/routing/review/index entry/realization などの標準文書、complete prompt の組み立て、各種 ACP builder の実行パラメータと structured output schema を横断的に検証する realization test。
- 標準 prompt、routing、file access、builder parameter が最終 prompt の同じ読み取り文脈で組み合わさることを前提に、render 結果、schema 制約、モデル種別、reasoning effort、file access mode、root path の扱い、用語 sanitization の回帰観点を一箇所に集約している。

## Read this when
- prompt part の markdown render 結果や complete prompt への標準文書の含まれ方を変更・確認したいとき。
- file access rule、routing rule、apply/review/index/realization standard の文言やタイトルが期待どおり prompt に現れるかを確認したいとき。
- ACP builder が返す model class、reasoning effort、file access mode、structured output schema path、prompt 本文の主要断片を検証したいとき。
- structured output schema の required、enum、additionalProperties、空配列拒否、oracle 側 schema との一致などの回帰を調べたいとき。
- root token や worktree/repo root の解決が apply fork 系 prompt にどう反映されるかを確認したいとき。
- complete prompt の入力文や標準文書から、禁止されたプロジェクト固有語・path token・用語表記が sanitization される挙動を調べたいとき。

## Do not read this when
- 個別 builder や prompt part の実装詳細だけを変更したい場合で、期待される外部挙動ではなく内部処理の構造を読みたいとき。
- CLI コマンド、永続状態、git 操作、セッション管理など prompt 生成以外の機能領域を調べたいとき。
- 特定の structured output schema の正本定義そのものを確認したい場合で、テスト期待値ではなく schema 本文を直接読むべきとき。
- 単一の小さな render helper や path helper の実装だけを追えば足りる場合で、prompt 構築全体の回帰観点が不要なとき。

## hash
- 671da574c121bfb135f6da3ca5439ef943442f74f6e4b5d23875be79eacda8e0

# `test_review_oracle_cli.py`

## Summary
- review oracle の CLI 経由の外部挙動を検証する realization test。report 生成、scope 指定、対象 oracle の選択、所見列挙・検証・judge・merge、結果集計、エラー report、review 用 worktree と join commit、INDEX.md 差分の取り込みや競合解決、review 実行中の許容外差分拒否を扱う。
- 16,000 文字を超えるが、review oracle run の状態、fake Codex 応答、report 文脈を共有する挙動群を一箇所で検証するための凝集したテスト群として位置づけられている。

## Read this when
- review oracle コマンドの report 内容、終了コード、scope の扱い、対象 oracle の選定条件を変更または確認する時。
- 所見の列挙・検証・judge・merge loop、finding の verdict や severity による並び順・集計・表示を変更または確認する時。
- review 実行用 worktree、session branch、fork commit、join commit、INDEX.md 変更の取り込み、INDEX.md 競合解決に関わる挙動を変更または確認する時。
- review oracle が gitignored oracle、binary、symlink、memo 配下に見える path、session scope の変更対象をどう扱うか確認する時。
- review oracle 実行中の Codex 処理失敗時の error report、または INDEX.md 以外の worktree 差分を拒否する制御を変更または確認する時。

## Do not read this when
- review oracle 以外の CLI サブコマンドや一般的な session 操作だけを確認したい時。
- oracle review の仕様本文や人間意図そのものを確認したい時。この対象は realization test であり、正本仕様ではない。
- report rendering や merge operation の内部実装だけを局所的に読みたい時は、まず実装側の該当関数を直接確認すればよい。
- INDEX.md 生成一般、routing entry の書式、またはテスト基盤全般を確認したいだけの時。

## hash
- ea7d3f24f774abdb135ebb656a95428d110ed907232765d5023af12e591d0c1f

# `test_session_cli.py`

## Summary
- session サブコマンドの CLI 挙動を検証する realization test。session fork による session branch と状態ファイル作成、session-id 衝突時の retry/失敗、cmoc ignore 初期化、linked worktree 上での fork/abandon/join の branch・HEAD 扱いを確認する。
- session abandon の正常終了、home branch 欠落時の失敗報告、cleanup 失敗時の状態と branch の rollback を検証する。
- session join の merge・conflict resolution・状態更新・branch 削除警告・エラー出力先を検証する。oracle file の conflict 解決では REALIZATION_WRITE profile と writable roots が使われること、削除 conflict 解決が stage されること、conflict marker block 検出が markdown 見出しと衝突しないことも扱う。

## Read this when
- session fork、session abandon、session join の CLI 外部挙動、終了コード、標準出力/標準エラー、git branch 操作、session 状態ファイルの更新を変更または確認したいとき。
- session サブコマンドが linked worktree 上で現在 worktree の branch と commit を基準に動くかを確認したいとき。
- session-id の衝突処理、session branch 削除失敗時の警告、abandon cleanup 失敗時の rollback など、session 操作の失敗時挙動を確認したいとき。
- session join の conflict resolution で Codex 実行 profile、FileAccessMode、writable roots、conflict marker 残存検出、delete conflict の stage 処理を確認したいとき。

## Do not read this when
- session サブコマンド以外の CLI や、session 状態に関係しない実装・テストを調べたいとき。
- session の内部 helper の細かな実装だけを確認したい場合で、該当する実装モジュールを直接読めるとき。
- Codex CLI や LLM の出力品質そのもの、または一般的な git 操作 helper の単体挙動を調べたいとき。
- oracle file の正本仕様断片を確認したいとき。この対象は realization test であり、正本仕様の代替として読まない。

## hash
- cd0f997fa91f4a14380c5ed1facc2972b6cfcd34a6fce63ef6f536b233af3ce3
