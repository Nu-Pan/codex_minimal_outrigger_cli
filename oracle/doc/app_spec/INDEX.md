# `cli_auto_completion.md`

## Summary
- CLI の自動補完プローブに関する正本仕様断片。`_CMOC_COMPLETE` が存在する呼び出しを通常実行と区別し、補完処理前の cmoc 固有処理・副作用・不要な標準出力／標準エラー出力を禁止する。CLI 起動処理や補完プローブの挙動を実装・検証する際の仕様上の入口となる。

## Read this when
- `_CMOC_COMPLETE` を用いた自動補完の判定や実行順序を変更するとき
- 自動補完時の副作用、状態検査、ログ・INDEX 更新、エラー出力の扱いを確認するとき
- CLI 補完プローブの stdout／stderr の互換性を実装・テストするとき

## Do not read this when
- 通常のサブコマンド処理、session／run 状態管理、ログ作成、INDEX 更新そのものを変更するとき
- 自動補完とは無関係な CLI 入出力や一般的なエラー処理を確認するとき

## hash
- c6c8f4184e5a5408e45d6fc796612c986a7954e7b2002b30e42c241fd1b590e2

# `codex_exec_rule.md`

## Summary
- Codex CLI を用いた agent call の呼び出し規約を定義する正本仕様。呼び出し方式、path context、環境変数、preflight、argv 上書き、sandbox、provider/model、prompt 전달、feedback reporter、ログ、Structured Output、並列実行、失敗時の retry・待機・エラー処理までを扱う。Codex 呼び出し実装や関連 builder・設定・ログ・出力検証の入口となる。

## Read this when
- cmoc の Codex CLI 呼び出し仕様を実装・変更・レビューするとき
- AgentCallParameter builder、path context、file access mode、sandbox、model/provider、reasoning effort の argv 反映を確認するとき
- prompt の渡し方、Structured Output の検証・補正、session resume、Codex call ログを扱うとき
- quota 枯渇、モデル容量超過、その他の Codex CLI 失敗時の処理を確認するとき

## Do not read this when
- 個別の builder の詳細な実装責務だけを確認する場合は、builder の正本実装・関連仕様を直接読む
- path context のデータモデルや導出規則だけを確認する場合は、指定された path model の定義を直接読む
- feedback observation の event schema や collector 契約だけを確認する場合は、feedback observation 仕様を直接読む
- Codex CLI と無関係な cmoc の実装・テスト・仕様を扱う場合

## hash
- 8e56036a6b90750dd42c0f38df90da8b87a765064a825d37091ff0aa2b2f4fd4

# `codex_model_provider.md`

## Summary
- Codex CLI の model provider 設定仕様と、cmoc が担う責務境界を定義する正本文書。`CmocConfigCodex`、provider-local 設定、値の制約、secret 保存禁止、および provider 管理を行わない方針を確認する入口。

## Read this when
- Codex CLI 呼び出しの model/provider 設定、provider ID の検証、provider-local key の扱いを変更・確認するとき
- cmoc が model provider の管理・保証・自動起動を担うか判断するとき
- Codex 設定に保存できる値や secret の扱いを確認するとき

## Do not read this when
- model provider の argv への具体的な反映方法だけを確認したいときは、指定された codex_exec_rule.md を直接読む
- Codex CLI や provider 自体の稼働、認証、推論品質、model pull、cache 管理を調査するとき

## hash
- 928d25ace53f88c12fadd5a3b8fd311001343c040e43aa5dd25945d939bb0d82

# `console_and_file_log.md`

## Summary
- cmoc のコンソール出力、サブコマンドログファイル、イベント記録の正本規則を定義する。時間・パス・JSON Lines・即時 flush・必須イベント・feedback detector 向け安定契約を扱い、ログ実装や出力仕様を確認する際の入口となる。

## Read this when
- サブコマンドのログファイル出力やイベント記録を実装・変更するとき
- コンソールログの形式、ステップ通知、Codex CLI 呼び出し通知、完了サマリーを確認するとき
- 時間表示やフルパス表示の規則を確認するとき
- feedback observation の件数通知や detector rule が参照するイベント契約を扱うとき

## Do not read this when
- ログやコンソール出力を変更せず、別の機能仕様だけを調査するとき
- feedback observation の検出条件そのものを確認する場合は、feedback observation の正本仕様を直接読むとき

## hash
- c4a10b41bdd89b291cac88bfd7d50e1e3cfb21cc6d89b0610497711e1257125f

# `doctor_preprocess.md`

## Summary
- cmoc の各サブコマンド開始前に実行する共通の検証・修復処理を定義する。Git 追跡状態、設定・refactor state の整合性、feedback reporter/client の利用可能性を扱い、修復困難な場合の終了条件と reporter 利用不能時の degraded warning を定める。

## Read this when
- doctor preprocess の検証・修復処理を実装または変更するとき
- サブコマンド共通の事前条件、Git 管理対象、refactor state 同期、feedback reporter の事前検証の責務を確認するとき
- 修復後の完了判定や、reporter 利用不能時に本命処理を継続する条件を確認するとき

## Do not read this when
- 特定サブコマンド固有の事前条件や本命処理の仕様を確認するとき
- doctor preprocess と無関係な Git 操作、refactor state の詳細仕様、feedback observation の正本仕様を直接確認するときは、それぞれの個別仕様を読む

## hash
- 5cafeef78d2ac95e25e30d8f4c70e23e8856ff0822bcb7d103642ae096e6c6c1

# `error_handling.md`

## Summary
- 各仕様のエラー終了時の共通ルールを定める。特別な上書きがない場合に、処理を中断し、stdout へ簡潔な説明・次の対応候補・詳細・コールスタックを出し、エラー終了を示す終了コードを返す場面で読む。

## Read this when
- 仕様側でエラー時の既定動作をそろえたいとき。
- エラー発生時に利用者へ何を出すか、どの時点で止めるか、終了状態をどう扱うかを確認したいとき。
- 個別仕様にエラー処理の上書き指示がなく、この共通規則を適用する必要があるとき。

## Do not read this when
- 個別仕様がエラー時の振る舞いを明示しているときは、そちらを先に読む。
- エラー内容の文面や詳細な報告項目を別途定義する具体仕様を確認したいときは、その仕様本文を読む。
- 正常系の処理手順だけを確認したいときは読む必要がない。

## hash
- bfaceea1701755cbe1f24db75ea9044ad4d4ed7dc98edef844bc94e39c3bbdf8

# `feedback.md`

## Summary
- feedback subsystem 全体の目的、観測源、raw observation の保存から report 生成までのデータフロー、用語上の責務分離、non-goal、既存 workload や TUI・中断との接続境界を定める正本仕様。個別の observation schema・状態遷移・feedback report の CLI 契約は、責務ごとに分割された下位仕様への入口として扱う。

## Read this when
- feedback subsystem の全体像、適用範囲、責務分担、non-goal、agent-facing transport から report までの流れを確認するとき
- feedback を realization 作業、oracle 問題、既存成果物、TUI の中断や異常終了と接続する境界を判断するとき
- feedback 関連の個別仕様を読む前に、どの責務の正本へ進むべきかを選ぶとき

## Do not read this when
- raw observation の schema、collector・detector・MCP reporter/client の詳細を確認する場合は observation 専用仕様を直接読むとき
- normalized issue、machine assessment、human disposition、増分処理 record の状態遷移を確認する場合は state 専用仕様を直接読むとき
- `cmoc feedback report` の事前条件、normalization、commit、再開、表示を確認する場合は subcommand 専用仕様を直接読むとき
- feedback とは無関係な task 成否、run state、retry、recovery、または一般的な実装詳細を確認するとき

## hash
- 7d4a2f2cbd9b63ed3e416ae75efab3175e47e0dd9c3585a866b12faf3a8d9143

# `feedback_observation.md`

## Summary
- feedback observation の収集・検査・保存に関するアプリケーション仕様。MCP reporter の agent-facing 契約、入力 schema の正本、共通 prompt instruction、受け入れ検査、collector が付与する context、sandbox・transport・lifecycle、機械的 log 検出の event 契約と初期 rule、raw observation の envelope・durability・retention・完了サマリーを定める。feedback 機能の実装・検証・関連仕様を確認する際の入口となる。

## Read this when
- feedback observation の reporter、collector、MCP transport、raw 保存、secret masking、rate limit、capability lifecycle を実装またはレビューするとき
- structured log event から machine observation を検出する rule、threshold、issue key、recurrence 集計を実装または検証するとき
- raw observation の envelope、保存 path、atomic durability、retention、未処理件数の表示仕様を確認するとき
- feedback の agent prompt 生成、入力 schema、Codex call lifecycle との連携仕様を調査するとき

## Do not read this when
- feedback の入力 JSON schema の具体的な field 定義だけを確認する場合は、指定された reporter input schema を直接読む
- 共通 prompt instruction の文面だけを確認する場合は、feedback reporting standard の builder を直接読む
- Codex 実行時の sandbox、permission profile、network 境界だけを確認する場合は、codex exec rule を直接読む
- feedback report の集約・ingestion receipt・snapshot manifest の詳細だけを確認する場合は、その report 仕様を直接読む

## hash
- ddc423b39c33480da77be1b5f61d45a751a83dfa02408134354c627ec5f3da59

# `feedback_state.md`

## Summary
- feedback の issue、revision、occurrence、assessment、human disposition、ingestion receipt、report を git 追跡下の分割 JSON record として保存する正本仕様。ID 生成、canonical JSON、append-only 更新、effective record の選択、branch merge 時の競合停止規則を定める。feedback の永続 state と record schema を確認する入口である。

## Read this when
- feedback report の保存先、record 構造、ID・hash・canonical form の規則を実装または検証するとき
- issue の effective revision・assessment・human disposition の決定方法を確認するとき
- append-only record の branch merge と同一 path の競合処理を確認するとき

## Do not read this when
- raw observation の形式や machine rule の定義だけを確認したいときは、観測・rule の正本を直接読む
- agent の reporter input category enum だけを確認したいときは、その入力 schema を直接読む
- CLI の具体的な実装配置や test 実行手順だけを確認したいときは、対応する設計・テスト規則を直接読む

## hash
- 3b1249d36a2e2d2cc491fa349d5759bf48f8a3199b6c15d9d5527c833c3d7a9d

# `indexing.md`

## Summary
- - `cmoc` による `INDEX.md` 自動配置と、その目次情報の生成・更新ルールを定める。
- - どのディレクトリとファイルを目次対象に含めるか、除外するかの判断基準を定める。
- - `INDEX.md` 生成時の処理順、差分の扱い、自動コミットの条件を定める。

## Read this when
- - `INDEX.md` を自動生成・再生成・更新する処理を実装または修正するとき。
- - あるディレクトリをインデックス対象に含めるか除外するかを判断するとき。
- - `INDEX.md` の生成タイミング、再帰順、差分処理、コミット単位を決めるとき。
- - インデクシング処理の正しさを確認するテストや検証を作るとき。

## Do not read this when
- - `INDEX.md` ではなく、個別機能の実装内容や利用者向け仕様を確認したいだけのとき。
- - 目次生成そのものではなく、別の `cmoc` 機能の設計や実装を扱うとき。
- - 手書きの `INDEX.md` 内容を考える作業で、自動配置や更新ルールが関係しないとき。
- - この仕様に含まれない具体的なハッシュ計算手順やコミット実装の細部だけを探したいとき。

## hash
- 61ab6318a773747ce71141f365f5aaf26fec36e326e42a08c8cb699b32cd199e

# `misc_spec.md`

## Summary
- cmoc の雑多な仕様を定義する文書。oracle file・realization file の列挙方法、work-root の前提、cmoc 実行時のパス関係、タイムスタンプ形式、cmoc-managed-branch の対象範囲を扱う。これらの用語や運用条件を確認する際の入口となる。

## Read this when
- oracle file または realization file の列挙条件を確認するとき
- work-root、repo-root、cmoc process、agent call のパス関係を確認するとき
- タイムスタンプの形式を確認するとき
- cmoc-managed-branch 上の変更範囲を判断するとき

## Do not read this when
- 個別の oracle 仕様や実装の詳細を確認したいとき
- cmoc の一般的な開発手順や言語・ツール固有の手順を確認したいときは、対応する仕様文書や skill を直接読む

## hash
- 77d23570d567556574348b40f8db0ff01bb9215863ecc0993c8d2a41176280ee

# `prompt_editor_input.md`

## Summary
- cmoc がユーザーのプロンプトをエディタで入力・編集する際の仕様を定める。エディタ選択の優先順位、`code --wait` の要件、編集対象と初期値の出典、自動注入指示の扱い、編集完了判定、プロンプト読み出し時のコメント除去と空白除去を扱う。プロンプト編集フローやエディタ起動仕様を確認する際の入口となる。

## Read this when
- ユーザー入力用エディタの起動・選択・待機動作を変更または確認するとき
- エディタ入力ファイルの場所、初期値、自動注入指示、編集完了判定を確認するとき
- 編集後のプロンプトのコメント除去や前後空白除去の挙動を変更または確認するとき

## Do not read this when
- エディタを介さないプロンプト生成や、入力後のプロンプト処理だけを調べるとき
- エディタ入力の初期値を具体的に構築する実装を変更するときは、参照先の実装を直接読む

## hash
- b47670393941a74a64ff654dbc87f66c8cbc4d215130089c24b53b1f89b03284

# `prompt_standard.md`

## Summary
- cmoc が agent call に渡すプロンプトの標準規範を定める oracle doc。cmoc 固有契約と installed skill の責務境界、決定論的な規範注入、Structured Output の schema・事後条件・受理条件、プロンプト構築関数、プレースホルダと参照記法、使用言語を扱う。プロンプト生成や出力契約の設計・変更時に、app_spec 配下の関連仕様へ進む入口となる。

## Read this when
- agent call の初回プロンプト、補正プロンプト、Structured Output、受理条件の設計または変更を行うとき
- cmoc 固有契約と installed skill の責務境界、feedback instruction の共通注入、プレースホルダや cmoc_ref の扱いを確認するとき
- プロンプトの記法、言語方針、oracle src の prompt builder との関係を確認するとき

## Do not read this when
- 個別のプロンプト builder 実装の詳細だけを調査・変更する場合は、対応する oracle src の実装を直接読む
- feedback の観測・保存責務だけを確認する場合は、feedback observation の仕様を直接読む
- Structured Output の補正処理の具体的な実行規則だけを確認する場合は、codex exec rule を直接読む

## hash
- cf3dd3c6498b114980635132e3eee9a0ea56aff71c233297af3132268f7920e9

# `run_isolation.md`

## Summary
- run の fork から join または abandon までのライフサイクル、専用ブランチ・linked worktree、成果物の取り込みと隔離資源の破棄に関する作業隔離規則を定義する。run を使う workload の開始・終了方法や、run-root 外への cmoc 管理データ保存の扱いを確認するための仕様入口。

## Read this when
- run の fork、join、abandon の挙動や適用条件を実装・レビューするとき
- run 用の git branch、linked worktree、agent call の cwd・path context を扱うとき
- session branch への成果物取り込み、run の破棄、または run-root 外の cmoc 管理データ保存を確認するとき

## Do not read this when
- read-only investigation/review など、明示的な join を必要としない run の個別仕様だけを確認するとき
- run の具体的な workload 固有ルールや CLI サブコマンド仕様を確認したいときは、それぞれの workload・CLI 仕様を直接読む

## hash
- bc6eb3a42a5da52906a45fe181dcc9a65aadf45114d838ed7e6fd5970c01d172

# `session_state.md`

## Summary
- cmoc workflow の session と、明示的な join を必要とする編集 run の lifecycle を一意に定める JSON state の正本である。session と run の最小限の永続状態、各 field の意味、初期値、状態遷移、join・abandon 後のリセット条件を扱う。feedback の tracked state は対象外であり、関連する正本仕様への入口ではない。

## Read this when
- session state JSON のスキーマ、field の意味、初期値、状態遷移を確認するとき。
- session fork、編集 run の開始・終了・中断・失敗、cmoc run join・abandon に伴う state 更新を実装またはレビューするとき。
- session と active run の branch、fork commit、workload kind の保持条件を確認するとき。

## Do not read this when
- feedback の observation、issue、machine assessment、human disposition の tracked state を確認するとき。
- session/run コマンドの詳細仕様や workload 固有の処理を確認するときに、session state JSON の構造・遷移が確認対象でない場合。

## hash
- ff460c0d6432b557f5e6c86763072fa0365fa62c7581b552d1d387dd976268e3

# `sub_command`

## Summary
- cmoc の各サブコマンド仕様をまとめた正本ドキュメント群。doctor・indexing・tui、oracle 編集／調査／レビュー、realization apply／refactor、session と run の lifecycle、feedback report を扱う。サブコマンドの挙動や実行条件を調べる際に、目的の仕様文書へ進むための入口となる。

## Read this when
- cmoc のサブコマンドの引数、事前条件、実行手順、状態遷移、終了条件を確認するとき
- oracle または realization の編集・調査・レビュー処理の仕様を確認するとき
- session／run lifecycle や feedback report のサブコマンド仕様を確認するとき
- 複数のサブコマンド仕様から、対象の責務に対応する正本文書を選ぶとき

## Do not read this when
- サブコマンド共通の詳細仕様や個別の builder・agent call・TUI 実装だけを確認したいとき
- インデクシング、feedback observation、feedback state など、サブコマンドが参照する別の正本仕様そのものを確認したいとき
- 対象サブコマンドの仕様文書がすでに特定できており、その本文へ直接進めるとき

## hash
- 62f28f521ecc31357432aad71cf6d95da5770de36761ae0090610bfbb826a10c

# `subcommand_interruption.md`

## Summary
- 中断可能な cmoc サブコマンドにおける Ctrl+C によるユーザー中断の正本仕様。対象サブコマンド、共通の中断処理、正常系としての完了条件、report・終了 log の識別要件、および各サブコマンドの中断後の扱いを定める。

## Read this when
- 中断可能なサブコマンドの追加・変更や、Ctrl+C の通知処理を実装・検証するとき。
- ユーザー中断時の state 更新、後処理、report 保存、終了 log、Codex CLI 呼び出し停止の要件を確認するとき。
- refactor fork、oracle review、feedback report の中断後の再開・再実行方針を確認するとき。

## Do not read this when
- 通常のサブコマンドのエラー処理や、ユーザー中断を個別仕様で扱わない処理を確認するとき。
- 中断対象の具体的なサブコマンド仕様そのものを確認する場合は、各サブコマンドの個別仕様を直接読むとき。

## hash
- dd18f014ca079f3bfdfc412dfc3d8b3a11fcefab00f0cf7d2955ef783ee39219

# `usage.md`

## Summary
- cmoc の基本的な呼び出し方法、初回準備、通常の session・oracle・realization の workflow、および apply と refactor の使い分けを説明する利用手順書。cmoc を使った開発 lifecycle の入口にあたる。

## Read this when
- cmoc の初回セットアップや基本的な呼び出し方法を確認するとき
- session fork/join、oracle 編集・レビュー、realization apply/refactor の手順を確認するとき
- realization apply と realization refactor の使い分けを判断するとき

## Do not read this when
- 特定の oracle file の仕様や編集内容を確認したいとき
- cmoc の内部実装や個別コマンドの詳細な技術仕様を調査するときは、対象コマンドまたは実装の文書を直接読む

## hash
- 67c1e11a5d4ebc3936273d706933419f4e789856bd1afb62c8baeed5896e0296
