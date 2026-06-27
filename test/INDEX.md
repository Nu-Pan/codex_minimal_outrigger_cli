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
- apply fork サブコマンドの realization test。Codex 実行を fake に差し替え、apply run の完了状態、apply branch/worktree/state の更新、linked worktree 起点の HEAD 利用、session 側の .gitignore 保持、.cmoc 追跡時の拒否、config 読み込み失敗時の副作用抑止、所見対象としての .gitignore 編集、apply target 正規化の境界を検証する。

## Read this when
- apply fork の CLI 挙動、状態遷移、apply branch/worktree 生成、Codex loop 呼び出し、または apply run の後始末を変更する。
- linked worktree 上で開始した session から apply fork する場合の基準 commit や worktree 配置を確認する。
- apply fork が session 側の .gitignore や .cmoc 追跡状態をどう扱うべきかを確認する。
- apply fork 開始前の config 読み込み失敗で、branch/state/pid などの apply run 副作用を発生させない挙動を確認する。
- apply 対象の正規化で、root 直下の memo 除外、入れ子の memo directory の扱い、binary file の保持を確認する。

## Do not read this when
- apply fork 以外の apply 系サブコマンド、review、session fork、init などの個別 CLI 挙動だけを確認したい。
- Codex CLI や LLM 出力品質そのものを検証したい。ここでは Codex 実行結果は fake 化され、cmoc 側の制御と副作用だけを検証している。
- apply fork の実装詳細を変更せず、仕様断片や利用者向け説明だけを確認したい。
- root 直下 memo の閲覧・編集を目的としている。この対象は memo を除外対象として扱うテストであり、memo 本文を読む入口ではない。

## hash
- d83fd6720f2b63478de5fdf301f10f5f7e8d71be6b2ac2107dfb5cac90d17b69

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
- apply run を session へ join する CLI 外部挙動を検証する realization test。join 成功時の apply worktree・apply branch cleanup、state 更新、report 生成に加え、apply worktree から実行した場合の復帰先と cleanup 到達性も扱う。
- 同じ join 操作の境界条件として、stale apply branch、dirty apply worktree、想定外差分、許容される gitignore 差分、merge conflict、index conflict 解決後の継続を一箇所で検証する。

## Read this when
- apply join の成功条件、拒否条件、cleanup、副作用、state 更新、report 出力を CLI 経由の外部挙動として確認・変更したいとき。
- apply join が session worktree と apply worktree のどちらから実行されても正しく動くか、失敗時に worktree・branch・state・log がどう残るかを確認したいとき。
- 想定外差分、force resolve、merge conflict、INDEX.md の conflict 解決など、apply join の差分判定や merge 失敗処理に関わるテストを探すとき。

## Do not read this when
- apply fork の Codex 実行内容や LLM 出力品質そのものを確認したいとき。この対象では fake result を使い、join 前提の apply run 作成だけを扱う。
- join の内部 helper の詳細実装だけを追いたいとき。まず実装側の join 処理を読む方が直接的で、この対象は CLI から見える結果の期待値を確認する入口である。
- session fork、init、path model など apply join の前提コマンド単体の仕様やテストを確認したいとき。

## hash
- 8d8344f01b53d4a8315b46deb8e84269e041d137a2c4de52d4835f977dbef44b

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
- session サブコマンドの CLI テスト群。fork による session branch と state 生成、abandon による home branch 復帰・branch 削除・失敗時 rollback、join による home branch への統合・conflict 解決・linked worktree 上の branch 扱い・エラー出力先を検証する。
- git worktree、session state JSON、sub command log、Codex conflict resolution 呼び出し profile、stdout/stderr の公開挙動など、session 操作の外部観測可能な副作用をまとめて確認する入口になる。

## Read this when
- session fork、session abandon、session join の CLI 挙動を変更または調査するとき。
- session branch の作成・削除、session state の state 値、session_home_branch、session_start_commit、last_joined_apply_oracle_snapshot_commit、apply state の更新条件を確認するとき。
- linked worktree 上で session 操作した場合に、root 側 branch と linked worktree 側 branch がどう保たれるかを確認するとき。
- session join の merge conflict 解決、oracle file conflict 時の Codex 実行 profile、delete conflict の staging、conflict marker 判定を調査するとき。
- session 操作失敗時の rollback、再実行案内、stdout/stderr の出力境界、sub command 完了ログに含まれる公開項目を確認するとき。

## Do not read this when
- session 以外のサブコマンド、設定読み込み、path model、一般的な git helper の仕様を調べたいだけのとき。
- CLI テストではなく session 実装本体の制御フローや helper の内部責務を直接変更したいとき。
- Codex profile 生成そのもの、FileAccessMode の定義、CmocConfig の詳細を調べたいとき。
- INDEX.md 生成規則やルーティング文書の書式だけを確認したいとき。

## hash
- 0812be4caa0c7c3c56f8c026eb7e2bfa5f2c58f40c3e93e1932addcc3b647ca4
