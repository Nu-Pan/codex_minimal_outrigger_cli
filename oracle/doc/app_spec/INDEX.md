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
- cmoc が Codex CLI を呼び出す際の正本規約。agent call の path context、環境変数、preflight、argv 設定上書き、sandbox と詳細なファイルアクセス制限、model/provider、prompt の stdin 渡し、feedback reporter、ログ、Structured Output の検証・補正、並列実行、失敗時の quota・一時障害対応を定める。Codex 呼び出し実装や AgentCallParameter builder、prompt/log/schema/feedback の連携を変更・調査する際の入口となる。

## Read this when
- Codex CLI の初回・resume・TUI 呼び出しを実装、変更、レビューするとき
- agent call の cwd、work root、repo root、ファイルアクセス mode、sandbox、承認設定、model/provider、reasoning effort の扱いを判断するとき
- prompt の保存・stdin 渡し、stdout/stderr・session ID・output のログ、Structured Output schema 検証と補正処理を扱うとき
- feedback reporter の call-scoped context、並列呼び出し、Codex CLI の quota・capacity・予期せぬ失敗への対応を確認するとき

## Do not read this when
- INDEX.md のルーティングだけを確認したいとき
- Codex CLI 呼び出しや agent call の挙動に関係せず、別の実装・仕様・テスト対象を直接調査するとき
- この文書が参照する個別の oracle doc の意味仕様や、具体的な実装ファイル自体を直接確認すべきとき

## hash
- 377b7b885fc4f4def501f991ba31f8733fe39bb2fb2f182efa698444388ebea1

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
- 非対話サブコマンドの console 出力、primary report、terminal result、サブコマンドログに関する共通契約の正本。時間・パス表示、stdout/stderr の責務、進行通知、primary report の保存、terminal result の分類・確定順序・表示内容、JSON Lines ログの記録要件を定める。
- cmoc 内部呼び出しと最外側サブコマンドの出力・report 境界を定義し、TUI、自動補完プローブ、非対話サブコマンドの通知適用範囲を整理する。個別サブコマンド固有の result、completion_reason、report 形式、終了コードは各サブコマンド仕様への入口となる。

## Read this when
- 非対話サブコマンドの標準出力、標準エラー、進行通知、terminal result の契約を確認するとき
- primary report の保存条件、表示するパス、terminal result の確定順序を確認するとき
- サブコマンドログの保存場所、JSON Lines 形式、即時 flush、診断イベントの記録要件を確認するとき
- TUI や自動補完プローブが非対話サブコマンドの出力契約に該当するか確認するとき

## Do not read this when
- 個別サブコマンドの result、completion_reason、primary report の具体的な内容や終了コードを確認するとき
- Windows toast 通知、エラー処理、feedback observation、自動補完の詳細な判定規則を確認するとき
- 本書が non-goal としている ANSI color、verbosity、debug option、機械可読 stdout schema の仕様を確認するとき

## hash
- f358aafbe45d1ff074bc4590edd59996c791e2baa17777b4c967ecbe8fa07df3

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
- エラー終了時の handled failure と internal failure の分類基準、および終了状態の確定手順を定義する共通仕様。primary report の保存、error terminal result、サブコマンド終了イベントの順序を扱う。
- handled failure と internal failure それぞれの表示内容、スタックトレースの扱い、診断用ログへの保存規則を定める。
- 正常な処理結果やユーザー中断要求をエラーと扱わない境界、および個別仕様が優先される事項を示すエラー処理の共通入口。

## Read this when
- エラー終了を handled failure と internal failure のどちらに分類するか判断するとき
- primary report、error terminal result、終了イベントの確定順序や保存失敗時の扱いを確認するとき
- エラー時の console 表示、スタックトレース、診断用サブコマンドログの契約を確認するとき
- 個別仕様に特別なエラー処理の記載がない場合の共通規則を確認するとき

## Do not read this when
- console と terminal result の出力先、表示順序、共通 field を確認したいとき
- 中断可能サブコマンドのユーザー中断要求の扱いを確認したいとき
- 個別仕様が state、rollback、report、次の操作、終了コードを明示している場合に、その具体的な処理を確認したいとき

## hash
- 09bad2d213a7377ebe276c8041544ce0bd466fd52b97b91cf5cc1a3b49c42c09

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
- agent・collector による observation の報告基準、MCP reporter の入力・結果・受け入れ検査、context 確定、保存経路、call 終了処理を定める正本仕様。
- structured log に基づく機械的 observation の detector 境界、初期 allowlist rule、issue key、threshold、除外条件を確認する入口。
- raw observation の保存単位、durability、retention、publication 後の cleanup、および通常サブコマンドへの pending warning の影響範囲を確認する入口。

## Read this when
- feedback observation を agent から報告・収集する処理、reporter/collector MCP interface、受け入れ検査、secret masking、context または capability の設計を変更するとき。
- machine observation の detector、rule registry、recurrence threshold、issue key、structured log event の扱いを実装・変更するとき。
- raw observation の durable 保存、publication、cleanup、retention、pending observation warning の挙動を実装・変更するとき。

## Do not read this when
- feedback observation の同一 issue 判定や現在状態の集約・report cut を扱う場合は、こちらではなく report・集約側の仕様を直接読む。
- 個別の prompt builder 実装や reporter input schema の詳細形式だけを確認する場合は、本文が参照する各正本ファイルを直接読む。
- feedback observation と無関係な agent call、structured output、または通常サブコマンドの仕様を扱う場合。

## hash
- e64de4d3dca0c8816caec3cfccfdc5daeee37c5db912fe839ba42158b94eaeab

# `feedback_state.md`

## Summary
- feedback report が扱う repository-local active state の正本。pending observation、unresolved issue、threshold 未満 aggregate、report cut、reference、checkpoint、publication 済み report、current pointer の所有範囲・保存形式・整合性を定める。
- report cut の固定から checkpoint の再利用、`incomplete` 診断 report、正常 report の atomic publication、current pointer 切替後の cleanup まで、feedback state の状態遷移と排他制御を確認するための入口。
- feedback observation の raw schema や detector rule の詳細ではなく、state artifact のライフサイクル、検証、耐障害性、保持・削除条件を確認する対象。

## Read this when
- `cmoc feedback report` の active state を作成、再開、検証、publication、cleanup するとき。
- active generation、current pointer、report cut、reference、checkpoint の整合性や durable 保存規則を確認するとき。
- `inconclusive` 発生時の `incomplete` 診断 report と、正常 publication 失敗時の再開条件を実装・レビューするとき。
- pending observation、active issue、threshold 未満 machine aggregate の保持範囲や compaction 条件を判断するとき。

## Do not read this when
- raw observation の形式、detector rule、machine issue key の正本を確認したいときは `feedback_observation.md` を読む。
- `cmoc feedback report` の invocation report の内容・生成条件を確認したいときは `feedback_report.md` を読む。
- 一般的な report の表示内容だけを確認したいときは、state の atomic publication や cleanup を扱うこの文書ではなく、対応する report 仕様を直接読む。

## hash
- 1300fb4185b52ab193cee4ede8580842a48a3d621fa31e17491c889d62e15ad4

# `indexing.md`

## Summary
- cmoc がリポジトリ内に INDEX.md を配置・更新する仕組みの仕様を定義する文書。配置対象、目次情報の形式と意味要件、ハッシュ、インデクシング順序、コミット、agent call の並列化、実行条件を扱う。

## Read this when
- INDEX.md の自動生成・更新処理の仕様を確認するとき
- 目次エントリーの内容、ハッシュ計算、対象範囲、更新・コミット手順を変更または検証するとき
- インデクシングの深さ優先処理や agent call の並列実行条件を確認するとき

## Do not read this when
- 個別の実装コードの詳細や CLI の一般的な責務だけを確認したいとき
- 特定ファイルの目次エントリー本文だけを読むべきで、インデクシング全体の仕様確認が不要なとき
- 既存テストの実行方法や Python 開発環境の設定を確認するときは、それぞれの専用仕様・手順を読む

## hash
- e94b7463e662ccbeb3beffe84e449e7b895dfdcf9460a9bccfe704fbc2078ce7

# `misc_spec.md`

## Summary
- cmoc における oracle file と realization file の責務、取り扱い判断基準、適合性、および列挙方法を定義する雑多な仕様の正本。oracle と realization の境界や列挙仕様を確認する際の入口であり、下位の実装・テスト仕様そのものの代替ではない。
- work-root の仮定、cmoc 実行時のパス文脈、タイムスタンプ形式、cmoc-managed-branch の対象範囲など、複数の機能領域にまたがる共通契約を扱う。

## Read this when
- oracle file と realization file の責務境界、分類、適合性、列挙対象、Git ignore、traversal、性能不変条件、または回帰検証の仕様を確認・変更するとき
- work-root、agent call の cwd、タイムスタンプ、または cmoc-managed-branch の定義を確認するとき
- doctor preprocess や realization refactor state 同期に関わる file 列挙結果の意味・境界・性能条件を調査するとき

## Do not read this when
- 特定の oracle doc・oracle src・oracle test の個別仕様だけを確認する場合は、その対象を直接読む
- realization implementation や realization test の具体的な実装詳細だけを変更・調査し、本文で定義する共通契約に関係しない場合
- INDEX.md のルーティング情報だけを確認する場合

## hash
- dd28109f5dd320f5f811caf07ae818b74afe15b2e3bdf69d63cd66cd373e14c1

# `prompt_editor_input.md`

## Summary
- エディタで入力する完全プロンプト skeleton と、初期 HTML コメントの役割・正本の所在を定義する仕様。
- skeleton からオリジナルプロンプトを確定し、editor work file の検証、最終読み取り、保存コピー作成、コメント除去、後続 Agent への受け渡し、作業ファイル削除までの処理境界を定義する。
- editor work file、保存コピー、正本仕様、実行時生成物を分離し、エディタ起動条件と安全なファイル検証条件を示す。

## Read this when
- prompt editor の初期入力、完全プロンプト skeleton、{{original-prompt-here}} の確定方法を変更・確認するとき。
- editor work file の作成、エディタ起動、パス・regular file・symlink 検証、最終読み取り、保存、コメント除去、削除処理を変更・確認するとき。
- 初期コメントの責務や表示文面の正本、後続 AI Agent に渡すプロンプトとの境界を確認するとき。

## Do not read this when
- prompt editor の仕様ではなく、個別の prompt_builder 実装コードだけを直接調査・変更するとき。
- 一般的なエディタの利用方法や、editor input と無関係なサブコマンド仕様を確認するとき。
- 既に確定したオリジナルプロンプトの後続処理だけを調査し、editor input の生成・確定手順に触れないとき。

## hash
- 09024319bebef185e27b83b3de5d86e3d70d96f5b87fc5b543f2a7605e7ab460

# `prompt_standard.md`

## Summary
- cmoc の agent call 用 prompt に関する正本と実行時生成物の責務境界、prompt に含める情報、文面の所有・受け渡し、規範の決定論的注入、Structured Output 契約、summary/goal の役割分担、構築記法と言語原則を定める仕様書。prompt builder や acp builder の意味仕様、共通 prompt part、または prompt 生成規則を確認する際の入口となる。

## Read this when
- agent call に渡す prompt の責務、情報量、参照 routing、作業範囲・完了条件の配置を確認するとき
- oracle src と realization implementation の prompt 責務境界を確認するとき
- Structured Output の schema と決定論的事後条件の役割分担、受理条件、補正規則を確認するとき
- summary と goal の記述範囲、prompt placeholder や cmoc block/ref の構築規則を確認するとき

## Do not read this when
- 個別の意味仕様やサブコマンド固有の判断基準だけを確認する場合は、対応する oracle doc を直接読む
- prompt の正確な文面や builder の実装を変更・確認する場合は、対応する oracle src を直接読む
- 実行時に生成された prompt、skeleton、editor input の内容だけを確認する場合

## hash
- c8eac0e1115bd730f57ad41d2f4243310514c7d51bdb5f659de106f2e4b33248

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
- cmoc の主要サブコマンド仕様を集約する入口。doctor、indexing、oracle／realization の編集・調査・レビュー、session／run lifecycle、feedback report、tui など、各コマンドの正本仕様へ進むためのルーティング情報を提供する。
- サブコマンドの引数・実行条件・処理手順・状態遷移・終了経路・primary report 要件を確認する際に、対象コマンドの仕様を選択して読む。共通の編集 run lifecycle は専用仕様へ、個別処理や保存形式は本文が指定する下位の正本へ進む。

## Read this when
- cmoc の特定サブコマンドの正本仕様を探すとき
- サブコマンドの実行条件、処理フロー、状態遷移、エラー・中断時の挙動、report 要件を確認するとき
- oracle／realization の編集・調査・レビュー、session／run の fork・join・abandon、feedback report、tui の仕様を変更・実装・検証するとき

## Do not read this when
- サブコマンドに共通する仕様だけを確認する場合は、本文から指定される共通正本を直接読むとき
- 特定サブコマンドの内部処理、保存データ形式、agent prompt・schema、実装配置、テスト実行手順だけを確認する場合は、本文が指定する専用仕様や開発ルールを直接読むとき
- 自動生成される INDEX.md の内容や、保存済み report の具体例だけを調査するとき

## hash
- 808d6d67743ad1bbc6bda6449d5c4d74e0b6ca4c939508d444f92a40999f4eb5

# `subcommand_interruption.md`

## Summary
- cmoc の中断可能サブコマンドに対するユーザー中断要求（Ctrl+C）の共通仕様を定める文書。中断対象の範囲、処理単位の停止、確定済み部分結果の保持、state 更新、primary report と terminal result の保存・出力、中断後の再開方針を確認するための入口となる。個別サブコマンドの詳細やログ・通知形式は、本文が参照する個別仕様および共通仕様へ進む。

## Read this when
- Ctrl+C によるユーザー中断を正常系として設計・実装・レビューするとき
- 中断可能サブコマンドの対象範囲や、中断時の結果・state・report の扱いを確認するとき
- 中断後に同じ run を再開できるか、新しい run や fork が必要かを判断するとき

## Do not read this when
- 特定サブコマンド固有の中断時 state や report 保存形式だけを確認するとき
- ログ形式、エラー処理、Windows toast 通知などの詳細だけを確認するとき

## hash
- 1695e21c641e63d7de727bfc19095fa695223e72e7b844f146664e76fd25bf5e

# `usage.md`

## Summary
- cmoc の標準的な利用手順を示す入口文書。初回の doctor 実行から session fork、oracle と realization の変更・レビュー、run の join/abandon、session join までの一連の workflow を扱う。
- 短い仕様・実装変更を realization apply で反映する流れと、差分に依存せず全体を追従させる realization refactor の使い分けを確認するための案内役である。

## Read this when
- cmoc を初めて利用するとき
- oracle の変更を realization に反映する手順や、各 workload の使い分けを確認するとき
- session、run、oracle、realization の lifecycle を確認するとき

## Do not read this when
- 個別の仕様や実装の内容を調査するとき
- oracle file の編集内容や review 規則そのものを確認するとき
- realization file の具体的な実装責務を確認するとき

## hash
- d56038df9b029f41ace3a407e3648c28af24bf8a5a98333a7fd44761c818ff69

# `windows_toast_notification.md`

## Summary
- Windows 11 上の WSL2 から Windows toast 通知を行う仕様。cmoc の非対話サブコマンドの terminal result と、TUI の agent turn 完了を通知対象とし、通知境界・状態分類・重複排除を定める。
- 通知内容の必須情報、秘密情報やフルパスの除外、Codex CLI callback 設定の呼び出し単位管理、および未検証の外部契約を正本仕様に断定しない方針を定める。
- 外部 module や新規 Python package に依存しない Windows toast transport の安全な受け渡し、有限時間、通知失敗時の本命処理への非干渉、自動補完プローブでの無効化条件を定める。
- 具体的な callback interface と transport 方式は realization に委ねられるため、仕様の境界を確認したうえで実装・外部契約検証へ進むための入口となる。

## Read this when
- Windows toast 通知機能を実装、変更、または仕様適合性レビューするとき。
- cmoc tui、cmoc oracle investigation、その他の最外側末端サブコマンドに通知境界を適用するとき。
- terminal result の分類、TUI turn の完了通知、callback の重複排除、または通知失敗時の非干渉を確認するとき。
- WSL2 からの toast transport、自動補完プローブ、Codex CLI の通知 callback 外部契約を扱うとき。

## Do not read this when
- terminal result の共通分類や primary report の確定条件だけを確認するときは、console_and_file_log.md を直接読む。
- ユーザー中断要求の成立条件や完了処理だけを確認するときは、subcommand_interruption.md を直接読む。
- 具体的な callback 設定 key、event、payload、発火保証の検証結果を確認するときは、検証済みの外部契約資料または対象実装を直接読む。

## hash
- 1160a9c967d32a54499d7c991062f44bc2e8973e2cf1a3cfe81b5fb495205456
