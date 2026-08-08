# `cli_auto_completion.md`

## Summary
- CLI 自動補完プローブと通常の cmoc 実行を区別するための境界条件を定義する仕様。環境変数によるプローブ判定、通常実行向け前処理・副作用の抑止、補完処理に必要な出力だけを許可する制約を扱う。CLI の補完経路を実装・変更・レビューする際の入口となる。

## Read this when
- 自動補完プローブの判定や処理順序を実装・変更するとき
- 補完実行時に通常実行向けの検査、副作用、エラー出力が混入していないか確認するとき
- CLI の自動補完境界に関する挙動仕様を確認するとき

## Do not read this when
- Windows toast 通知固有の自動補完プローブ境界を確認するときは、指定された Windows toast 通知仕様を直接読む
- 自動補完以外の CLI 実行や cmoc の一般的な状態管理を扱うとき

## hash
- 5d3e467991746592b1be1e88a9dfee48ee1826974290fafb96de45460efbf671

# `codex_exec_rule.md`

## Summary
- cmoc が Codex CLI を呼び出す際の包括的な運用規約を定める正本仕様。agent call の path context、環境変数、CLI 引数、sandbox と詳細なファイルアクセス制限、モデル/provider、プロンプト փոխանց送、feedback reporter、ログ保存、Structured Output 検証・補正、並列実行、失敗時の再試行・待機、および .agents 編集禁止を扱う。Codex 呼び出し実装やその設定・ログ・出力検証の挙動を確認する際の入口となる。

## Read this when
- Codex CLI の初回呼び出し、resume、TUI 呼び出し、引数構築、prompt の渡し方、ログ保存を実装・変更・レビューするとき
- AgentCallParameter の path context、file access mode、sandbox、model/provider、reasoning effort、approval 設定の適用規則を確認するとき
- Structured Output の schema 指定、検証、補正 turn、session 再開、差分不変性を扱うとき
- feedback reporter の登録・利用・終了処理、並列 call の分離、quota や一時的サーバー障害への対応を確認するとき

## Do not read this when
- Codex CLI 呼び出しや Structured Output、関連するログ・sandbox・provider・feedback の挙動を扱わず、対象外の機能だけを調査・変更するとき
- 個別 builder の詳細な実装責務だけを確認する場合は、まず対応する AgentCallParameter builder の正本へ進むとき
- Windows toast 通知の effective configuration や callback 検証だけを扱う場合は、指定された Windows toast 通知仕様へ直接進むとき
- Codex model provider の解決規則だけを扱う場合は、指定された model provider 仕様へ直接進むとき

## hash
- 25fabf9f0294cb673da6072ed4a60481cc8d1317112f86b1170382c398b1bdec

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
- コンソール表示とサブコマンドログファイルに関する正本仕様。時間・パスの表示形式、JSON Lines ログの配置・イベント・即時 flush、コンソールログの Markdown 形式、開始・ステップ・Codex CLI・完了通知の要件を定める。ログ出力や表示仕様の実装・検証時の入口となる。

## Read this when
- サブコマンドのログファイル出力、イベント記録、flush、保存先を実装または検証するとき
- コンソールの開始通知、ステップ通知、Codex CLI 通知、完了サマリーや表示フォーマットを実装または検証するとき
- 時間表示やフルパス表示の仕様を確認するとき

## Do not read this when
- feedback observation のイベント契約そのものを確認するときは、指定された feedback observation 仕様を直接読む
- Windows toast 通知の対象・順序・内容・失敗時の扱いだけを確認するときは、Windows toast notification 仕様を直接読む
- ログやコンソール表示に関係しないサブコマンドの挙動を扱うとき

## hash
- 03b116a9345a0f2cbaa067b1583e6cbd5430095524eda773b4d682acf9abef9a

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
- oracle file と realization file の列挙方法、traversal の事前 pruning、Git ignore 判定の性能不変条件、回帰検証、および work-root・実行時 cwd・タイムスタンプ・管理ブランチに関する前提を定義する雑多な仕様。関連するファイル列挙、symlink や nested repository の境界、性能要件、または cmoc 実行環境の用語を確認する際の入口となる。

## Read this when
- oracle file／realization file の分類規則や full glob 相当の列挙結果を実装・検証するとき
- pruning 境界、非通常ファイル、symlink、nested repository、Git ignore の扱いを確認するとき
- Git subprocess 数や ignore source 検証回数など、列挙性能の不変条件と回帰検証条件を確認するとき
- work-root、cmoc の実行 cwd、タイムスタンプ、cmoc-managed-branch の定義を確認するとき

## Do not read this when
- 特定の oracle または realization ファイルの内容や責務を確認することが目的で、この仕様の列挙・環境前提に関係しないとき
- テスト実行手順や開発環境の構築手順を確認するときは、それぞれの専用の開発ルール文書へ直接進む

## hash
- 9db85fcbeb954960be775cd1d055e88636114eb836822432d93ed2e507638222

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
- cmoc が agent に渡すプロンプトの標準規範を定める oracle doc。cmoc 固有契約と installed skill の責務境界、決定論的な規範注入、Structured Output の受理条件、プロンプト構築関数の利用、プレースホルダ・参照記法・言語原則を扱う。プロンプト生成や agent call の契約を確認する際の入口となる。

## Read this when
- agent call の初回プロンプト構築規則や prompt builder の責務を確認するとき
- Structured Output の schema・決定論的事後条件・受理条件の境界を変更またはレビューするとき
- cmoc 固有契約と installed skill の責務境界、プレースホルダ、cmoc_block/cmoc_ref 記法、言語規則を確認するとき

## Do not read this when
- 個別の oracle src 実装の具体的な挙動や関数定義を直接調査するとき
- feedback の保存・収集責務そのものを確認するときは、feedback observation の正本仕様を直接読む
- 対象 repository 固有の開発手順やテスト実行方法だけを確認するときは、該当する repository 文書や開発規則を読む

## hash
- 1126905bdb1eab48d45c31c5a2a07c3f8924a3b16f3d8cdf12d30f43f0002cf0

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
- cmoc の主要サブコマンド仕様をまとめたディレクトリ。doctor、indexing、oracle edit/investigation/review、realization apply/refactor、session fork/join/abandon、run lifecycle、tui、feedback report の実行条件・責務・状態遷移・入出力を扱う。各サブコマンドの挙動や実装・テストの確認時に、該当する仕様文書へ進むための入口となる。

## Read this when
- cmoc のサブコマンドの引数、前提条件、実行手順、終了状態を確認したいとき。
- oracle 編集・調査・レビュー、realization の適用・リファクタ、session/run の fork・join・abandon、TUI、feedback report の仕様を調べるとき。
- サブコマンド間の共通 lifecycle と workload 固有仕様の境界を確認したいとき。

## Do not read this when
- doctor preprocess、feedback observation/state、Codex exec、prompt editor、通知など、各文書が委譲する詳細仕様だけを確認したいときは、参照先の正本を直接読む。
- インデクシングや refactor の内部処理そのものなど、サブコマンド入口以外の実装詳細だけを調べたいとき。
- 一般的な session 操作や git 操作の仕様だけを確認したいとき。

## hash
- 190c579c31ed97b0cb0905a8dcf9445859c9a686bd20c93955fee3fe094efce3

# `subcommand_interruption.md`

## Summary
- 中断可能な cmoc サブコマンドにおけるユーザー中断要求（Ctrl+C）の受付、共通の完了処理、正常系としての扱い、report・終了 log での識別方法を定義する仕様。
- 対象サブコマンドごとに、中断後の run の状態、再開可否、確定済み部分結果や checkpoint の扱いを定める。

## Read this when
- 中断可能なサブコマンドの挙動、Ctrl+C の処理、部分結果の確定、interrupted 完了、または中断後の再実行・再開可否を確認するとき。
- `cmoc realization refactor fork`、`cmoc oracle review`、`cmoc feedback report` の中断仕様を実装・レビューするとき。

## Do not read this when
- 通常のサブコマンドのエラー処理や、Ctrl+C を中断要求として扱うことが個別仕様に明記されていないサブコマンドを調べるとき。
- Windows toast 通知の詳細を確認するときは、専用の通知仕様を直接読む。

## hash
- bea325ca9cf30996074c014e517e8a851ea4b8c89c5be2f0018a48fdc6c16cd4

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

# `windows_toast_notification.md`

## Summary
- Windows 11 上の WSL2 で cmoc が表示する Windows toast 通知の正本仕様。通知対象となるサブコマンド境界、非対話処理と TUI の発火条件、通知内容、Codex CLI 設定境界、外部契約の事前検証、通知 transport の制約、自動補完時の禁止事項、non-goal を定める。
- Windows toast 通知の実装、サブコマンドや TUI の lifecycle event との接続、Codex CLI callback の利用可否検証、通知 transport の設計を確認する入口となる。

## Read this when
- Windows toast 通知を新規実装・変更・レビューするとき
- 非対話サブコマンドの完了通知、TUI の turn 完了通知、通知の重複排除や中断状態の扱いを判断するとき
- Codex CLI の通知 callback 設定や callback event の外部契約を検証するとき
- WSL2 から Windows へ通知する transport、自動補完プローブ時の初期化禁止、通知失敗時の独立性を確認するとき

## Do not read this when
- 通知仕様ではなく、一般的なサブコマンドの挙動やログ仕様だけを調べるときは、対象となる各サブコマンドの正本仕様を直接読む
- Windows 以外のデスクトップ通知や toast の表示カスタマイズを扱うとき
- agent turn 途中の承認要求や prompt・assistant 回答の表示を扱うとき

## hash
- ae77b082d0e9fb697d97d557fa7f6c7ba6f6fa51afbe88b7b6e5a3ad805974f2
