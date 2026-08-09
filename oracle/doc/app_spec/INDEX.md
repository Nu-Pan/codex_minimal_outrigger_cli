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
- cmoc が Codex CLI を呼び出す際の包括的な規約を定める正本仕様。agent call と Codex call の区別、path context、環境変数、preflight、argv による設定上書き、sandbox・ファイルアクセス、モデル・provider、prompt 전달、feedback reporter、ログ、Structured Output 検証・補正、並列実行、失敗時の retry・待機方針を扱う。Codex CLI 呼び出しの実装や検証に関する各仕様の入口となる。

## Read this when
- cmoc の Codex CLI 呼び出し方法、引数、sandbox、ファイルアクセス、path context、モデル設定、prompt 전달、ログ保存、Structured Output、feedback reporter、並列化、quota・一時障害時の retry を実装・変更・検証するとき
- agent call と Codex call の境界や session ID、call ID、呼び出し単位の設定を確認するとき
- Codex CLI 呼び出しに関する既存仕様が他の実装・テスト規約とどう関係するかを確認するとき

## Do not read this when
- Codex CLI 呼び出しの規約自体ではなく、Windows toast 通知、model provider の詳細、feedback observation の event schema、prompt standard、開発環境、設計、テスト実行などの個別仕様だけを確認する場合は、本文が指定する各正本へ直接進む
- INDEX.md のルーティング情報だけを確認する場合や、Codex CLI を使わない一般的な実装・文書作業の場合

## hash
- 6785ac96b8a0eb1a88f78b5033aaeda4b0fd3d455bba295202febce33e83cd7e

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
- コンソール出力、ファイルパス、サブコマンドの JSON Lines ログ、およびコンソールログの形式と必須内容を定める仕様。サブコマンド実行ログの実装・変更・検証時に、出力規則の入口として参照する。
- 時間・パスの表示形式、ログイベント、Codex CLI 呼び出し通知、完了サマリーを扱う。Windows toast 通知の詳細は専用仕様へ委譲する。

## Read this when
- サブコマンドログの保存先、JSON Lines 形式、イベント内容、即時 flush を実装または変更するとき
- cmoc の標準出力・標準エラーに出すログの形式、ステップ通知、Codex CLI 通知、完了サマリーを実装または検証するとき
- 時間表示またはフルパス表示のフォーマットを確認するとき

## Do not read this when
- Windows toast 通知の対象・順序・内容・失敗時の扱いだけを確認するときは、専用の toast 通知仕様へ直接進む
- サブコマンドやコンソール・ファイルログに関係しない機能の実装や調査を行うとき

## hash
- 865aa83147e94ce4fc48c30df3d012197c07f59b96405639e8e86cb23d6829cf

# `doctor_preprocess.md`

## Summary
- cmoc の各サブコマンド開始前に、リポジトリと実行環境の共通前提を検証し、可能な範囲で修復する処理の正本仕様。git 追跡状態、refactor state の同期、feedback reporter/client の事前検証、および修復後の tracked 差分の commit を扱う。サブコマンド固有の前提条件は対象外で、doctor preprocess 正常終了後に各サブコマンドが検証する。

## Read this when
- doctor preprocess の検証・修復手順、実行前の共通前提、または正常終了条件を変更・実装・レビューするとき
- `.cmoc/gu`、`.agents`、設定ファイル、refactor state の git 追跡保証や同期処理を確認するとき
- feedback MCP reporter/client の起動可能性、protocol compatibility、degraded warning の扱いを確認するとき

## Do not read this when
- サブコマンド固有の事前条件や本命処理だけを扱い、doctor preprocess の共通検証・修復に関係しないとき
- doctor preprocess の具体的な実装配置やテスト実行方法だけを調べるときは、対応する realization implementation または test の仕様・実装を直接確認するとき

## hash
- e0604bb0c2de87aa6960c60ddaa07519b9c7bab1f7de92a738ad8e1da8ceb659

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
- cmoc の作業中に観測された未解決かつ人間対応が必要な問題を、観測・候補化・現在状態の検証・公開に分離して扱う feedback subsystem の全体仕様。agent submission と allowlist 済み diagnostic を raw observation として収集し、report 実行時に normalization、verification、atomic publication を行う。詳細な観測、state 管理、report 処理の正本仕様へ進むための入口。

## Read this when
- feedback observation の収集経路、agent-facing MCP reporter、collector、diagnostic detector、または raw observation の責務を確認するときは観測仕様を読む。
- active issue、pending observation、report cut、一時 state、または atomic publication の状態管理を確認するときは state 仕様を読む。
- cmoc feedback report の事前条件、候補の normalization・verification、再開条件、または Markdown report の表示を確認するときは report 仕様を読む。
- feedback subsystem と realization 作業、TUI、中断、異常終了、または既存成果物との境界を確認するとき。

## Do not read this when
- 個別の observation schema や collector の実装詳細だけを確認したい場合は、全体方針ではなく観測仕様を直接読む。
- active state の保存形式や publication の処理だけを確認したい場合は、state 仕様を直接読む。
- feedback report の具体的な実行手順や verdict の判定だけを確認したい場合は、report 仕様を直接読む。
- feedback と無関係な realization 実装、テスト、または一般的な indexing の作業を行う場合。

## hash
- d1ce5a8444f167bea8b8d4c1f72479efcdfccd5c1d5cf07b918b3f0faa90a0e9

# `feedback_observation.md`

## Summary
- feedback observation の agent 自己申告、機械的な log 検出、reporter/collector の受け入れ検査、context 付与、raw observation の atomic 保存・保持・削除条件を定める正本仕様。feedback 機能の実装、検査、保存形式、運用上の pending 判定を確認する際の入口となる。

## Read this when
- MCP reporter の agent-facing interface、入力検査、secret masking、capability と lifecycle を実装または確認するとき
- 構造化 log event から diagnostic observation を検出する rule、allowlist、recurrence 集約の仕様を確認するとき
- raw observation の envelope、保存先、重複処理、durability、retention、pending warning を実装または検証するとき
- feedback の report state や codex 実行境界と observation の連携を調査するとき

## Do not read this when
- feedback の current pointer、report cut、normalization、publication の状態遷移だけを調査するときは、feedback state の仕様を直接読む
- agent prompt に注入する共通 feedback instruction だけを確認するときは、共通 instruction の正本を直接読む
- reporter input の field、enum、サイズ制限だけを確認するときは、reporter input schema を直接読む
- feedback observation と無関係な CLI 機能や一般的な log 処理を調査するとき

## hash
- 2aead678c6985503affd6a5c550a50ec4f5d57c08b75732f476c3647081d3ef6

# `feedback_state.md`

## Summary
- feedback の active issue、threshold 未満 machine aggregate、report cut、checkpoint、atomic publication、および legacy state 移行を含む repository-local active state の正本仕様。collector・reporter・normalizer・verification・cleanup 実装が保存先、耐久性、排他、整合性、再開条件を確認する際の入口。

## Read this when
- feedback report の active state や current pointer の読み書きを実装・変更するとき
- report cut の固定、checkpoint の再利用、publication、cleanup、異常終了からの再開を扱うとき
- active issue、machine aggregate、issue identity、threshold、legacy state 移行の挙動を確認するとき

## Do not read this when
- raw observation の形式や machine rule registry だけを確認するときは、feedback observation の正本を直接読む
- feedback の利用者向け要求や全体方針だけを確認するときは、feedback の上位仕様を直接読む
- 保存 state を扱わない通常の CLI 機能や、既存 state と無関係なテストを変更するとき

## hash
- 4151c5742273f7e72d194b092c52e2fb52639493f35da264102446c3f0e4d5f5

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
- cmoc がユーザーのオリジナルプロンプトを入力・抽出し、完全プロンプトへ確定するまでの仕様を定義する文書。skeleton の構造、プレースホルダー、エディタ起動、コメント除去、置換、保存に関する契約を扱う。

## Read this when
- プロンプトエディタの入力形式や初期表示内容を確認するとき。
- オリジナルプロンプトの抽出規則と完全プロンプト確定の条件を確認するとき。
- エディタ起動方法、編集対象、完全プロンプトの保存先に関する仕様を確認するとき。

## Do not read this when
- サブコマンド固有の skeleton や起動パラメータの内容を実装・確認するときは、対応する build_*_parameter の仕様や実装を直接読む。
- エディタの実際の起動処理を調査するときは、エディタ起動を実装する対象を直接読む。
- 完全プロンプトの保存処理やログ管理を調査するときは、対応する保存・起動パラメータ処理を直接読む。

## hash
- f380190a508a0f4ffb4df40e89be29d7048dee309e27c7fe4f8e2e6173d51eb8

# `prompt_standard.md`

## Summary
- cmoc が agent call に渡すプロンプトの正本規範を定める oracle doc。cmoc 固有契約と installed skill の責務境界、規範・feedback の注入、Structured Output の受理条件、動的プロンプト構築、プレースホルダと参照記法、言語方針を扱う。プロンプト生成や受理判定、cmoc 固有記法の設計・変更時に参照する入口となる。

## Read this when
- agent call のプロンプト構築規則、prompt builder の責務、または cmoc 固有契約と installed skill の境界を確認するとき
- Structured Output の schema・決定論的事後条件・補正 turn の受理条件を変更または検証するとき
- プレースホルダ、cmoc_block、cmoc_ref、GFM、または Codex CLI の言語方針を扱うとき

## Do not read this when
- 個別の prompt part や builder の具体的な実装を確認することが目的で、対応する oracle src を直接読むべきとき
- feedback の判断基準や保存責務だけを確認する場合は、feedback observation の正本仕様を読むべきとき
- Windows toast 通知の責務境界だけを確認する場合は、専用の Windows toast 通知仕様を読むべきとき

## hash
- 1e9cd5e7db4c1c92d20aacef558e51e33f68c06775436477ee6654b9c276a8e9

# `run_isolation.md`

## Summary
- run の fork から join または abandon までのライフサイクル、専用 fork サブコマンドによる編集 run、read-only 調査や機械的更新などの例外を定義する作業隔離規則。run 固有の branch・linked worktree、成果物の commit、session branch への merge、run-root 外へ書き込める cmoc 管理データの範囲を確認するための正本。

## Read this when
- run の fork・join・abandon のライフサイクルや、編集 run と非編集 run の扱いを確認するとき
- run branch、fork 時点の commit、linked worktree、成果物の merge・破棄規則を確認するとき
- run-root 外への書き込み例外や、feedback・session state など cmoc 管理データの保存場所を確認するとき

## Do not read this when
- CLI サブコマンドの具体的な引数・実装を確認したいときは、該当する CLI 仕様または実装を直接読む
- feedback の詳細な状態遷移や report 形式だけを確認したいときは、feedback state・feedback observation の正本仕様を直接読む
- run 隔離や lifecycle、branch/worktree、管理データの書き込み範囲に関係しない作業のとき

## hash
- 3aabd242a7edaf586c84b94a72a9ca44eb1325cf6e6031d5743aaceafc35d0ab

# `session_state.md`

## Summary
- cmoc workflow における session と、明示的な join を必要とする realization 編集 run の lifecycle を定義する正本仕様。永続化する最小限の session/run 状態、識別情報、状態遷移を扱う。session・run の開始、実行、join 待ち、中断、失敗、join/abandon 後の状態を確認する入口であり、feedback state や report などの repository-local state の仕様は別文書から確認する。

## Read this when
- session または realization 編集 run の JSON state の項目、初期値、状態遷移、join/abandon に伴う更新規則を実装・確認するとき
- cmoc session 系または cmoc run join/abandon の lifecycle と永続化範囲を確認するとき

## Do not read this when
- feedback の pending observation、active issue、generation、checkpoint、report など repository-local feedback state の仕様を確認するとき
- oracle edit の workload や、session/run state を直接扱わない cmoc workflow の仕様を調べるとき

## hash
- a51826f9117628aed11af12abea90cb9d81df228584fb1457e70afad67115828

# `sub_command`

## Summary
- cmoc の主要サブコマンド仕様をまとめたディレクトリ。doctor・indexing・tui、oracle 操作、realization apply/refactor、session／run lifecycle、feedback report の実行条件・処理フロー・状態遷移・エラー処理を確認するための入口。各ファイルが個別サブコマンドまたは関連 lifecycle の正本仕様を担う。

## Read this when
- cmoc のサブコマンド仕様、実行条件、引数、処理フローを調査・実装・レビューするとき。
- oracle／realization の編集・調査・レビュー、session／run の fork・join・abandon、feedback report の挙動を確認するとき。
- 対象サブコマンドを特定でき、該当する個別仕様へ進む前に仕様群の構成を把握したいとき。

## Do not read this when
- サブコマンド共通ではない詳細仕様や実装・テスト配置だけを確認したいときは、各仕様が示す共通正本・設計規則・実装・テストを直接読む。
- INDEX.md の生成規則や一般的な oracle／realization の定義だけを確認したいときは、上位の共通仕様を読む。
- 対象が明確に特定のサブコマンドまたは lifecycle に限定されている場合は、このディレクトリ全体を網羅せず該当する仕様ファイルへ直接進む。

## hash
- 3b135a554004d5e8982afa7ab8cf9bda7c5f7448b862149e4955515c045f4575

# `subcommand_interruption.md`

## Summary
- 実行中サブコマンドへの Ctrl+C によるユーザー中断を、正常系として扱う共通要件と対象サブコマンド別の扱いを定義する仕様。中断受付後の処理停止、確定済み結果・state・終了 log、再実行や再開の制約を確認する入口。

## Read this when
- 中断可能サブコマンドの追加・変更、Ctrl+C の処理、ユーザー中断時の正常終了・state 更新・後処理を実装またはレビューするとき。
- refactor fork、oracle review、feedback report の中断後の再開・再実行方針を確認するとき。

## Do not read this when
- 中断処理に関係しないサブコマンドの通常動作を調査するとき。
- Windows toast 通知の詳細だけを確認するときは、通知仕様を直接読む。

## hash
- 9c53ef845a3465b5debb3db6b020f1bcfa39cb864524c16c27667b38301dcf8f

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
