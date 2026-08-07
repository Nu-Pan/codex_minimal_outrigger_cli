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
- コンソール表示とサブコマンドの JSON Lines ログ出力に関する共通仕様を定義する。時間・パスの表示形式、ログの配置・イベント・即時 flush、コンソール通知の構成、完了サマリーと feedback 件数の扱いを扱う。アプリケーションのログ挙動や出力形式を確認・変更する際の入口となる。

## Read this when
- サブコマンドログのファイル配置、イベント内容、JSON Lines 形式、flush 要件を確認するとき
- コンソールログの markdown 形式、ステップ通知、Codex CLI 通知、完了サマリーを確認するとき
- 時間表示またはフルパス表示のフォーマットを確認するとき
- feedback observation 件数の通知境界や成功判定への影響を確認するとき

## Do not read this when
- ログやコンソール出力の具体的な実装箇所を直接調査・変更するだけで、仕様の確認が不要なとき
- feedback observation の検出規則そのものを確認するときは、専用の feedback observation 仕様を読む

## hash
- ab66699596c84833dfd1463899751bb5126f4c36d618af401bff9632e1652d62

# `doctor_preprocess.md`

## Summary
- cmoc の各サブコマンド開始前に、リポジトリ状態、管理対象ファイルの追跡・同期状態、feedback reporter/client の利用可能性を検証し、可能な修復と tracked 差分の commit を行う doctor preprocess の正本仕様。doctor preprocess の責務、検証・修復手順、refactor state の同期タイミング、reporter 障害時の degraded warning の扱いを定義する。

## Read this when
- doctor preprocess の検証・修復処理を実装または変更するとき
- サブコマンド共通の事前条件、refactor state の同期、または tracked 差分の commit の責務を確認するとき
- feedback reporter/client の事前検証や利用不能時の継続条件を確認するとき

## Do not read this when
- doctor preprocess 後に行う個別サブコマンド固有の事前条件や本命処理を調べるとき
- feedback observation の reporter interface と protocol の詳細を確認するときは、feedback observation の正本仕様を直接読む
- 実行対象ファイルの具体的な実装配置やテスト実行手順だけを確認するときは、対応する設計・テスト規則を直接読む

## hash
- 4c0446c5680999ea13cbe1f5d276e6aaaffc0262f9277665b214d4ed3363b77a

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
- feedback subsystem 全体の目的、観測源、raw observation から normalized state・report までの責務分離、用語、既存 workload との接続境界を定める正本仕様。詳細な observation、state、report の仕様へ進むための入口。

## Read this when
- feedback subsystem の全体像、対象範囲、non-goal、データフローを確認するとき
- feedback に関わる agent、collector、detector、normalizer、report の責務境界を判断するとき
- realization 作業、TUI、中断、既存成果物との feedback 接続方針を確認するとき

## Do not read this when
- raw observation の schema や保存規則だけを確認したい場合は observation 仕様を直接読むとき
- normalized issue、machine assessment、human disposition、state snapshot の詳細だけを確認したい場合は state 仕様を直接読むとき
- feedback report の実行条件、増分処理、再開、表示だけを確認したい場合は report 仕様を直接読むとき

## hash
- d4f6f13312254a460f175cc8563e4bc75bd91da223bdd5c924e088082385deeb

# `feedback_observation.md`

## Summary
- feedback observation の収集・保存仕様を定める文書。MCP reporter の入力契約と受け入れ検査、collector が付与する実行文脈、sandbox/transport/lifecycle、機械的な log detector の責務と allowlist、raw observation の envelope・永続化・retention・完了サマリーを扱う。feedback 機能全体の実装・仕様・運用を確認する際の入口となる。

## Read this when
- agent-facing MCP reporter の interface、入力 schema の扱い、受け入れ条件、secret masking、capability や collector context を確認するとき
- feedback observation の保存形式、ID、パス、重複処理、atomic durability、retention、未処理件数の表示を実装またはレビューするとき
- structured log event から machine observation を検出する rule、issue key、threshold、初期 allowlist を確認するとき
- feedback reporter/collector の障害や Structured Output validation exhausted の機械検出仕様を確認するとき

## Do not read this when
- feedback の人間向け observation payload schema だけを変更・確認する場合は、reporter input schema の正本を直接読む
- 共通 prompt instruction の文面や注入条件だけを確認する場合は、feedback reporting standard の正本を直接読む
- Codex 実行時の sandbox、permission profile、network 境界だけを確認する場合は、codex exec rule を直接読む
- 一般的な feedback report の集計・正規化仕様だけを確認し、raw observation の収集・保存契約を扱わない場合は、該当する report 仕様へ直接進む

## hash
- f2e6b056acb0c072cd5bf4027a0cc571d8a132b9ae483a27adeccd09966d90fd

# `feedback_state.md`

## Summary
- feedback の repository-local 永続 state の正本仕様。issue、revision、occurrence、assessment、human disposition、ingestion receipt、normalization unit、report、state snapshot の保存単位・JSON schema・ID規則・immutability・hash整合性を定義する。
- feedback の増分正規化、unit manifest による確定と再利用、effective record の選定、writer 排他制御、異常終了時の recovery、正常 report の predecessor 連鎖を扱う。feedback observation の raw形式や machine rule 自体ではなく、それらを永続 state として管理する実装の入口となる。

## Read this when
- feedback state の保存先、record schema、ID生成、canonical JSON、immutable file の扱いを実装または確認するとき
- normalization unit の確定条件、checkpoint の再利用、effective record の選定、ingestion receipt による増分処理を扱うとき
- feedback report、state snapshot、human disposition、writer 排他制御、異常終了後の再開や corruption 対応を実装・検証するとき
- feedback の repository-local state と report の正常連鎖や retention の契約を確認するとき

## Do not read this when
- raw observation の形式や machine rule の判定規則を確認するだけのときは、feedback observation の正本を直接読む
- feedback の利用者向け issue 概要、カテゴリ enum、agent report 入力項目だけを確認するときは、対応する feedback 仕様または reporter input 定義を直接読む
- feedback state の具体的な CLI 実装やテスト手順だけを確認するときは、該当する realization implementation、oracle の design rule、または test rule を読む

## hash
- d7162dc794f33afa2f45d82d30ae1d56d16cc7b1580c9421d8c29be159bf7b60

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
- run の fork から join または abandon までのライフサイクルと、各操作の扱いを定義する仕様書。
- run 固有のブランチ・linked worktree・パスコンテキスト、および run-root 外へ書き込める cmoc 管理データの例外を扱う。

## Read this when
- run の開始、成果物の取り込み、破棄、または session との関係を確認するとき
- run 用の git branch、worktree、agent call の作業パスを確認するとき
- feedback state や実行ログなど、run の隔離範囲外に保存される管理データの扱いを確認するとき

## Do not read this when
- 通常のサブコマンド仕様や workload 固有の処理内容だけを確認したいとき
- run のライフサイクル、隔離、または git/worktree の運用に関係しない仕様を調べるとき

## hash
- b9ad96574a3885a7ba811c3204635430b4604cef6b3a146f306dd21c37e82865

# `session_state.md`

## Summary
- cmoc workflow における session と、明示的な join を要する realization 編集 run の lifecycle を定義する正本仕様。session/run の状態、識別情報、fork 情報、状態遷移を扱い、feedback 関連の永続状態は対象外とする。

## Read this when
- session の新規作成、fork、状態確認、または session lifecycle の挙動を確認するとき
- realization 編集 run の開始、実行、joinable/error、join、abandon の状態や保持情報を確認するとき
- session と run の state schema や状態遷移を実装・レビューするとき

## Do not read this when
- feedback observation、issue、assessment、disposition、receipt、normalization、checkpoint、report、snapshot の保存仕様を確認するときは feedback state の正本を読む
- oracle edit の run 扱いを確認するときは、この仕様ではなく oracle edit 固有の仕様を読む
- 一般的な session/run CLI 操作の実装詳細や fork・merge の手順だけを確認するときは、対応する CLI・設計仕様を直接読む

## hash
- 94620a5709e5d68ce8d81fe5ea3650c68f7e37e9492e98d75e110217d05ddfbc

# `sub_command`

## Summary
- cmoc の各サブコマンドおよび主要なセッション・編集 run の正本仕様を集約するディレクトリ。doctor、indexing、tui、oracle 操作、realization apply/refactor、session 操作、feedback report などのコマンド単位の挙動確認に進む入口となる。

## Read this when
- cmoc サブコマンドの引数、事前条件、実行手順、終了条件を確認・変更するとき
- oracle 編集・調査・レビュー、realization の apply/refactor、session の fork/join/abandon、feedback report の仕様を確認するとき
- 対象コマンド固有の責務と、共通 lifecycle や下位処理仕様との境界を判断するとき

## Do not read this when
- サブコマンド固有ではなく、doctor preprocess、Codex 起動、プロンプト入力、feedback schema、共通編集 run lifecycle などの共通仕様だけを確認したいときは、各参照先の正本仕様へ直接進む
- 具体的な realization 実装やテストの詳細だけを調べるときは、対応する realization file または realization test を直接読む
- INDEX.md のルーティング情報だけを確認する必要があるとき

## hash
- 2f847238402357a2a69c4fe1d56a32df1b0e3d8e8d3da1a8dcf0a027bc6efc77

# `subcommand_interruption.md`

## Summary
- 中断可能な cmoc サブコマンドについて、対象範囲、Ctrl+C によるユーザー中断要求の通知、共通の完了・状態更新・報告・終了ログ要件を定める仕様。各サブコマンドの中断後の再開可否、確定済み部分結果、checkpoint、normalization の扱いを確認する入口となる。

## Read this when
- 中断可能サブコマンドの追加・変更・実装適合性を確認するとき
- Ctrl+C、正常系としての中断完了、report・終了 log、state 更新の仕様を調べるとき
- refactor fork、oracle review、feedback report の中断後の扱いを確認するとき

## Do not read this when
- 中断処理ではなく、個別サブコマンドの通常時の処理仕様だけを調べるとき
- Codex CLI の呼び出し・retry・quota 待機の一般規則だけを調べるときは、専用の実行規則を直接読むとき

## hash
- d5eedb81caf0c6d8c73e2ccb3688d039a28a59d9ad85f8d46089eab351e13307

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
