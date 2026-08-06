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
- cmoc が Codex CLI を呼び出す際の包括的な規約を定める正本仕様。agent call と Codex call の識別、call-scoped path context、環境変数、preflight、CLI 引数による設定上書き、sandbox と詳細なファイルアクセス制限、モデル・provider・reasoning effort、prompt の受け渡し、feedback reporter、ログ保存、Structured Output の検証と補正、並列実行、失敗時の retry・quota 待機・エラー処理を扱う。Codex exec 呼び出し実装や関連する builder、ログ・検証・エラー処理の仕様を確認する際の入口となる。

## Read this when
- cmoc の Codex CLI 呼び出し方法、argv、sandbox、設定上書き、prompt 入力、ログ出力を変更・検証するとき
- Structured Output の schema 指定、検証、同一 session での補正、差分不変性、失敗時処理を変更・検証するとき
- agent call の path context、model/provider 解決、feedback reporter、並列実行、quota または一時障害時の retry を扱うとき
- Codex exec 呼び出し規約と AgentCallParameter builder や関連する oracle 仕様との整合性を確認するとき

## Do not read this when
- Codex CLI 呼び出しや agent call の挙動に関係せず、対象となる実装・テスト・別の正本仕様を直接確認すれば足りるとき
- 単に一般的な Codex CLI の使い方を調べるだけで、cmoc 固有の呼び出し契約を扱わないとき
- 本書が参照する個別の builder、path model、provider、feedback、prompt standard、test execution の詳細仕様そのものを確認するときは、該当する参照先を直接読む

## hash
- 2ac2b1faa885219e620a4d7b79f4cbc6f9718eed7da8502aead9ca7ce7e2e4e3

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
- cmoc の各サブコマンド実行前に、リポジトリが正常実行可能かを共通検証し、必要な修復を行う doctor preprocess の正本仕様。git 追跡状態、refactor state、feedback reporter の検証・修復条件と、修復後の commit および degraded warning の扱いを定義する。

## Read this when
- cmoc のサブコマンド共通の事前検証・修復処理を実装、変更、レビューするとき
- `.cmoc/gu`、`.agents`、設定ファイル、refactor state の git 追跡条件を確認するとき
- feedback reporter の配置、protocol version 検証、利用不能時の継続条件を確認するとき

## Do not read this when
- 個別サブコマンド固有の事前条件や本命処理だけを扱うとき
- doctor preprocess の仕様ではなく、refactor state の詳細スキーマや feedback reporter interface の正本仕様を直接確認するとき

## hash
- 4998955d88376261c975062b57221240ccd99d2c8504dbdf0d7559df716ec868

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
- cmoc の作業中に判明した人間対応対象を、agent の自己申告と allowlist 済み diagnostic のみに基づく raw observation として集約する feedback subsystem の目的・責務・データフローを定める正本仕様。
- observation、issue、machine assessment、human disposition、feedback report の境界と、report 実行時まで意味的な正規化を行わない原則を示す。
- feedback observation・state・report の詳細仕様、および realization 作業や TUI・中断時の既存 workload との接続方針への入口となる。

## Read this when
- feedback subsystem の目的、対象範囲、観測源、raw observation の扱いを確認するとき
- observation、issue、machine assessment、human disposition、feedback report の責務分離を確認するとき
- feedback と realization 作業、固有成果物、TUI・中断・異常終了の関係を確認するとき
- feedback の詳細な observation schema や state 遷移、report コマンドの挙動を調べる前に全体方針を把握するとき

## Do not read this when
- reporter、collector、detector、raw observation の具体的な schema や検出規則だけを確認したい場合は、feedback observation の正本仕様を直接読む
- issue、machine assessment、human disposition、増分処理 record の schema や状態規則だけを確認したい場合は、feedback state の正本仕様を直接読む
- cmoc feedback report の事前条件、normalization、commit、再開、表示の具体的な挙動だけを確認したい場合は、feedback report の正本仕様を直接読む
- feedback ではなく realization、oracle review、indexing、run、session、TUI の固有成果物の判定基準や lifecycle を確認したい場合は、それぞれの正本仕様を直接読む

## hash
- 45356f21628fc8e3199fe2bd03a50534970b441732405ede747d704d6b39b7c3

# `feedback_observation.md`

## Summary
- feedback observation の自己申告、機械的検出、raw observation 保存に関する正本仕様。reporter の CLI interface、入力・受入検査、collector context、sandbox/transport、安全な保存、detector の初期 allowlist、observation envelope、durability・retention・未処理件数の扱いを定義する。feedback observation の収集から保存、検出ルール、運用上の完了サマリーまでを確認する入口。

## Read this when
- reporter の配置、CLI interface、入力 schema、受入拒否、secret masking、rate limit を実装または確認するとき。
- collector が付与する実行 context、sandbox capability、transport の安全要件を扱うとき。
- 構造化 log から diagnostic observation を検出する責務境界、event contract、rule registry、初期 allowlist を実装または確認するとき。
- raw observation の保存先、ID 生成、重複・corruption 処理、envelope schema、durability、retention、未処理件数の表示や warning を扱うとき。

## Do not read this when
- observation の意味、reporter input の field 定義、または共通 prompt instruction の正本だけを確認する場合は、対応する oracle schema・prompt builder の正本を直接読む。
- feedback observation の集計・通知 threshold の実装だけを確認する場合は、report 仕様または report 実装を直接読む。
- 一般的な cmoc の開発環境、設計境界、テスト実行手順を確認する場合は、対応する dev_rule を読む。

## hash
- a141297a2717a61b8558e7661fe2b93b72b730c4055097a4ecbae657b97ceb55

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
