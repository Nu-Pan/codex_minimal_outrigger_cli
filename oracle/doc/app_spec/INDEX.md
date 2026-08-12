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
- Codex CLI の `codex exec` 呼び出しに関するアプリケーション仕様。agent call の path context、環境変数、preflight、CLI 設定上書き、sandbox とファイルアクセス制限、model/provider、prompt・ログ・Structured Output、並列実行、失敗時の retry・quota 待機、`.agents` 編集禁止を定義する。Codex 呼び出し構築や実行制御の仕様を確認するための入口。

## Read this when
- Codex CLI の初回呼び出し、resume、TUI 呼び出し、または agent call の実行条件を実装・変更・レビューするとき
- sandbox、ファイルアクセス、permission profile、model/provider、reasoning effort、環境変数の扱いを確認するとき
- prompt、ログ、Structured Output の保存・検証・補正、session ID の扱いを確認するとき
- quota 枯渇、レートリミット、モデル容量エラーなど Codex 呼び出し失敗時の処理を確認するとき

## Do not read this when
- 個別 agent call の責務や判断基準そのものを確認する場合は、対応する oracle doc を直接読む
- AgentCallParameter builder の実装詳細や path model のデータモデルを確認する場合は、指定された oracle src を直接読む
- Windows toast 通知、model provider の詳細、feedback observation のイベント仕様を確認する場合は、それぞれ指定された専用 oracle doc を直接読む

## hash
- 7d18f4117a3b7cb80baf366c94c83d063742c17b869bba7a34851fd7dfd799f0

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
- cmoc の各サブコマンド開始前に、リポジトリを実行可能な状態へ検証・修復する doctor preprocess の正本仕様。共通前提の保証、修復困難時のエラー終了、tracked 差分の commit、feedback reporter/client の degraded warning を扱う。doctor preprocess の具体的な検証・修復要件を確認する入口であり、個別サブコマンドの本命処理仕様ではない。

## Read this when
- doctor preprocess の責務や実行順序を実装・レビューするとき
- `.cmoc/gu`、`.agents`、`config.json`、refactor state の追跡状態や同期要件を確認するとき
- feedback MCP reporter/client の事前検証、protocol compatibility、利用不能時の扱いを確認するとき
- doctor preprocess 完了後に個別サブコマンドが検証すべき前提との境界を確認するとき

## Do not read this when
- 特定サブコマンド固有の事前条件や本命処理を確認するとき
- git working tree または staging area の clean 状態の検査仕様だけを確認するとき
- doctor preprocess が保証する対象ではなく、個別サブコマンドの仕様を直接確認すべきとき

## hash
- 7082572dae6260e1658de16f08ecc0f00e588b5d36f7097610a1776e429ac7a1

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
- feedback subsystem 全体の目的、処理モデル、共通原則、正本仕様の分担、既存 workload との境界、および non-goal を定義する仕様の入口。
- 観測の raw 保存、repository-local state の publication、normalization・verification、正常 report と incomplete 診断 report の関係を横断的に確認する際に読む。

## Read this when
- feedback subsystem の責務や、agent submission と machine detector から report publication までの処理モデルを確認するとき
- observation・state・feedback_report の各正本仕様が何を定義するかを確認し、適切な下位仕様へ進むとき
- unresolved、resolved、not_actionable、inconclusive の扱い、active state、report cut、正常 publication の境界を把握するとき
- 既存 workload の成果物を feedback へ自動変換しない条件や、feedback を task state と分離する原則を確認するとき

## Do not read this when
- observation の報告基準、収集経路、受け入れ検査、機械 detector、raw 保存だけを確認したいとき
- repository-local state、report cut、checkpoint、atomic publication、cleanup だけを確認したいとき
- cmoc feedback report の事前条件、normalization、verification、表示、終了結果だけを確認したいとき
- feedback の具体的な入力 schema、normalization prompt、verification prompt の詳細を確認したいとき
- 実装詳細、テスト、または realization file の挙動だけを調べるとき

## hash
- 037a71f07a0107a2802e5d61e4ed484f2f2e96a6a1d022be78d89f192803be9e

# `feedback_observation.md`

## Summary
- feedback observation の報告基準、agent 向け reporter と MCP interface、collector の context 確定・transport・保存経路、call lifecycle、機械的 log detector の境界と初期 rule、raw observation の保存・durability・retention を定める正本仕様。issue の同一性や現在状態の判断は扱わない。

## Read this when
- agent が現在の作業外の人間対応を要する observation の報告条件や、報告してはならない問題の境界を確認するとき。
- feedback reporter の input、result、受け入れ検査、masking、rate limit、failure degradation を実装・検証するとき。
- collector が call context、capability、transport、call 終了処理、raw observation の保存と cleanup を扱うとき。
- structured log event から machine observation を検出する rule、issue key、threshold、除外条件を設計・検証するとき。
- feedback observation の raw record、durability、publication 後の retention、pending warning の仕様を確認するとき。

## Do not read this when
- 通常の issue 管理や feedback report の集約・現在状態の判断を確認したいとき。
- feedback observation と無関係な agent prompt、CLI 機能、ログ、または repository 文書の仕様を扱うとき。
- 既存の raw observation の個別内容や保存ファイルを直接調べるときは、保存経路の仕様ではなく該当する observation を直接読む。

## hash
- 0bae6de598e146d6f9728360c36a03d0a4b3b517b07e20802a17297edb9c356c

# `feedback_state.md`

## Summary
- feedback report が使用する repository-local state の正本。active generation、current pointer、report cut、reference、checkpoint、incomplete 診断 report の責務と保存範囲を定義し、atomic publication、排他制御、再開、cleanup、および corruption 防止の境界を示す。

## Read this when
- feedback state の配置、保持対象、JSON canonical form、hash、排他制御を確認するとき
- active issue や threshold 未満 machine aggregate の identity・保持・昇格条件を決めるとき
- report cut の固定入力、checkpoint の再利用条件、inconclusive 時の扱いを実装または検証するとき
- 正常な Markdown report の publication 順序、current pointer の切替、cleanup の条件を確認するとき
- incomplete 診断 report の durable 保存と、直前の正常 publication を維持する動作を確認するとき

## Do not read this when
- raw observation の形式や detector rule 自体を確認したい場合は、feedback observation の正本を直接読むとき
- feedback report の人間向け内容や表示形式だけを確認する場合
- active state と report publication に関係しない機能の実装・調査を行う場合

## hash
- e48bc94eb8576a2e559811a0097f633db9563055fe8dd42b07bf6122d0c3684d

# `indexing.md`

## Summary
- `cmoc` が `INDEX.md` を配置・更新するためのインデクシング規則、目次情報の要件、処理順序、並列実行条件、実行タイミングを定義する。
- `INDEX.md` の個別エントリー生成時に参照する、インデクシング仕様の正本である。

## Read this when
- `INDEX.md` の自動生成・更新処理の仕様を確認するとき。
- 目次情報の対象範囲、意味要件、ハッシュ、処理順序、並列化、コミット条件を実装または検証するとき。
- インデクシング前後の agent call や `run_indexing_preflight` の扱いを確認するとき。

## Do not read this when
- 個別の実装ファイルやテストの具体的な挙動だけを確認する場合。
- 目次情報から読むべき対象を選ぶだけで、インデクシング仕様そのものを確認・変更しない場合。
- アプリケーション固有の仕様や一般的なドキュメント作成規則を調べる場合。

## hash
- cbfe78d28a5d079d389e9d5753bd8ed3a9c53913d87f522fa5985f950c377138

# `misc_spec.md`

## Summary
- cmoc における oracle file と realization file の責務、判断基準、適合性、分類方法、列挙時の traversal・Git ignore・性能不変条件・回帰検証、および work-root や実行時刻などの共通仮定を定義する雑多な正本仕様。これらの概念や列挙処理の仕様を確認する際の入口となる。

## Read this when
- oracle file と realization file の責務や配置を確認するとき
- oracle と realization の判断基準、適合性、仕様優先関係を確認するとき
- oracle file または realization file の分類・列挙方法を実装、変更、検証するとき
- Git ignore、pruning、symlink、nested repository、linked worktree の扱いを確認するとき
- 列挙処理の性能不変条件や回帰検証の境界を確認するとき
- work-root の仮定、cmoc 実行時の cwd、タイムスタンプ、managed branch の定義を確認するとき

## Do not read this when
- 特定の oracle doc・src・test の個別仕様だけを確認すれば足りるとき
- 実装配置や CLI 責務境界を判断する場合は design_rule を直接読むとき
- テスト追加・変更の規則を確認する場合は test_rule を直接読むとき
- 既存テストの実行方法だけを確認する場合は test_execution の手順を直接読むとき

## hash
- 849da108e141534024127d65879d7d2fd7d367be895bbb080d0c8095d57a973b

# `prompt_editor_input.md`

## Summary
- cmocがエディタ向け入力文面を生成し、ユーザーのオリジナルプロンプトを完全プロンプトへ組み込む仕様を定義する。初期コメントの責務、完全プロンプトのskeleton、エディタ起動、コメント除去、プレースホルダー置換、保存までを扱う。プロンプト編集入力や完全プロンプト確定処理の仕様を確認する際の入口となる。

## Read this when
- エディタに提示する初期入力文面の構成や責務を確認するとき
- skeletonへのオリジナルプロンプト挿入条件を確認するとき
- エディタの選択、起動待機、入力読み出し、完全プロンプト保存の挙動を確認するとき

## Do not read this when
- 正確な初期コメントの表示文面そのものを確認したいときは、指定された正本実装を直接読む
- サブコマンド固有のプロンプト契約やパラメータ構築を確認したいときは、対応するbuild_*_parameterの仕様・実装を直接読む
- 実行時生成物の内容や個別のログを確認したいとき

## hash
- 2c21fa7b9fffb3d90522994106ad255df4d918ec8bb68ec6fdbe7448427c1264

# `prompt_standard.md`

## Summary
- プロンプトの意味仕様と実行時 prompt 文面の正本を分離し、agent call に必要な情報だけを動的に注入・受け渡しするための責務境界と構築規則を定める文書。prompt の情報量、cmoc 固有契約、feedback、Structured Output、placeholder、参照関係、言語などを扱う。prompt builder／acp builder の設計や変更、agent call の契約・注入規則を確認する入口であり、個別の意味仕様そのものを確認する場合は参照先の oracle doc、正確な prompt 文面を確認する場合は対応する oracle src へ進む。

## Read this when
- prompt builder または acp builder の責務、正本、動的 prompt 構築規則を変更・確認するとき
- agent call に注入する情報、cmoc 固有契約、installed skill、routing rule の境界を確認するとき
- feedback reporting や Structured Output の schema・validator・決定論的事後条件の責務分担を確認するとき
- placeholder や cmoc_block／cmoc_ref を含む prompt 記法と参照関係の検証規則を確認するとき

## Do not read this when
- 個別の cmoc 意味仕様や file access の詳細な判断基準だけを確認する場合は、本文で指定された対応する oracle doc を直接読む
- 子 agent に渡す正確な prompt 文面を確認・変更する場合は、この文書ではなく対応する oracle src を直接読む
- 生成済み prompt、ログ、editor input の内容だけを確認する場合
- prompt と無関係な実装、テスト、またはリポジトリ固有の開発手順を確認する場合

## hash
- a7597c976cb355d28698b4aefb330f58dc774789363bc379f47c4bbd9ce8952a

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
- cmoc のサブコマンドごとの正本仕様を集約するディレクトリ。doctor、indexing、tui、oracle／realization の各 workload、session／run lifecycle、feedback report など、個別コマンドの契約と実行条件を確認する入口である。

## Read this when
- 特定の cmoc サブコマンドの引数、事前条件、実行手順、終了条件、状態遷移を確認したいとき。
- oracle／realization の編集・調査・レビュー、session／run の fork・join・abandon、feedback report の仕様を調べるとき。
- 対象コマンドを特定でき、対応する個別仕様へ進む前にサブコマンド仕様群の構成を把握したいとき。

## Do not read this when
- サブコマンドではなく、doctor preprocess、indexing の意味そのもの、feedback state、prompt editor、共通 interruption など委譲先の正本仕様だけを確認したいとき。
- 特定の realization 実装や TUI 実装の内部詳細だけを調べるときは、対応する realization file や実装を直接読む。

## hash
- 2f964924f3a4db85873c0d40cff357dfad7107eea951445540c3bdb3ed4c792f

# `subcommand_interruption.md`

## Summary
- 中断可能な cmoc サブコマンドにおけるユーザー中断要求の共通仕様と、対象サブコマンドごとの中断後の扱いを定める。Ctrl+C の受け付け、確定済み部分結果の扱い、state・後処理・終了 log、正常系としての完了、再実行や再開の制約を確認するための入口となる。

## Read this when
- 中断可能サブコマンドの追加・変更や、Ctrl+C による中断処理を実装・レビューするとき
- 中断時の部分結果、state 更新、report、終了 log、再開可否の仕様を確認するとき
- `cmoc realization refactor fork`、`cmoc oracle review`、`cmoc feedback report` の中断後動作を確認するとき

## Do not read this when
- 中断処理を持たないサブコマンドの通常動作だけを調べるとき
- 個別サブコマンドの通常時の保存・再開仕様だけを確認する場合は、そのサブコマンドの個別仕様を直接読むとき
- 中断時の Windows toast 通知の正本を確認する場合は、通知仕様を直接読むとき

## hash
- bb0aac85965f69c8d9f29792292334917a42b4ef744e2a387873a9d537fa78cd

# `usage.md`

## Summary
- `cmoc` の初回セットアップ、セッション分岐・統合、oracle の調査・編集・レビュー、realization の apply/refactor 実行と run lifecycle を含む標準 workflow を説明する利用手順。cmoc の運用手順や workload の使い分けを確認する入口。

## Read this when
- cmoc を初めて導入・実行するとき
- oracle 変更から realization 反映までの workflow や session/run lifecycle を確認するとき
- realization apply と realization refactor の使い分けを確認するとき

## Do not read this when
- 個別の oracle 仕様や realization 実装の内容を確認したいとき
- cmoc の内部設計・開発環境・テスト実行規則を確認したいときは、それぞれの専用文書を直接読む

## hash
- 39da44eb91651a997184df522e971bdc5bad67987fc185cf451173fd7e95b4fb

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
