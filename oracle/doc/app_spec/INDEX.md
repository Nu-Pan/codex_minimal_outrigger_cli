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
- cmoc が `codex exec` を呼び出す際の正本規約。agent call ごとの path context、環境変数、CLI 引数上書き、sandbox と詳細なファイルアクセス制限、model/provider、prompt の受け渡し、feedback reporter、ログ保存、Structured Output 検証・補正、並列実行、失敗時の retry・quota 待機を定める。Codex CLI 呼び出しの実装、AgentCallParameter builder、実行ログ、出力補正、障害時の挙動を確認・変更するときの入口となる。

## Read this when
- cmoc の `codex exec` または `codex exec resume` 呼び出しの argv、環境、sandbox、provider、model、reasoning effort を確認・変更するとき
- agent call の path context、ファイルアクセス制限、prompt 生成・stdin 渡し、Codex call のログ保存を実装・検証するとき
- Structured Output の schema 保存、検証、同一 session での補正、差分不変性、失敗時処理を確認するとき
- feedback reporter の call-scoped context や Codex CLI の quota・一時障害・並列呼び出しへの対応を確認するとき

## Do not read this when
- 個別の agent call の意味上の責務や判断基準を確認する場合は、先に対応する oracle doc を読む
- Codex CLI 呼び出し以外の実装責務、一般的な開発環境、テスト実行規約を確認する場合は、対応する別の oracle 文書へ直接進む

## hash
- 1bd2c78042f2799bcd68e8a3725cf2f9414f1cd2c2b26d577fe3ea3117cc2e34

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
- 日本語の自然言語、時間・パス表示、非対話サブコマンドの console 出力、primary report、terminal result、サブコマンドログ、TUI と自動補完の境界に関する共通契約を定める正本文書。個別サブコマンド仕様へ進む前の共通出力・記録規則の入口となる。

## Read this when
- 非対話サブコマンドの stdout/stderr、進行通知、primary report、terminal result の表示や保存契約を確認するとき
- サブコマンドログの JSON Lines 形式、保存場所、flush、診断イベント要件を確認するとき
- TUI、自動補完プローブ、内部サブコマンド呼び出しの出力境界を確認するとき

## Do not read this when
- 個別サブコマンド固有の result、completion_reason、primary report 内容、終了コードだけを確認したいとき
- Windows toast 通知、自動補完の詳細判定、エラー処理、feedback observation の通知境界そのものを確認したいときは、それぞれの正本仕様を直接読む場合

## hash
- 079544d60eb1a021769ba387a657293e962cacb2c736c455f3eb7f62af41e61f

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
- agent による observation 報告の基準と、cmoc_feedback reporter の入力・結果・受け入れ検査を定める文書。collector が確定する context、保存経路、call 終了処理も扱う。
- allowlist 済み rule に基づく機械的な log 検出、issue key、threshold、除外条件、および raw observation の durable 保存・retention・terminal warning を定義する。feedback observation の収集から保存・publication 後の cleanup までを確認する入口である。

## Read this when
- agent が現在の workload 外の人間対応を要する問題を報告する条件や、報告後に本命 workload を継続する規則を確認するとき
- cmoc_feedback の MCP interface、入力 schema、結果形式、受け入れ検査、secret masking、rate limit を確認するとき
- collector が call-scoped capability から context を確定する方法、reporter から raw observation までの保存経路、call 終了順序を確認するとき
- machine observation の detector 境界、初期 allowlist rule、recurrence threshold、issue key の構成を確認するとき
- raw observation の保存単位、durability、publication 後の cleanup、pending 数に関する terminal warning を確認するとき

## Do not read this when
- feedback observation の正本 prompt 文面や完全 prompt への配置だけを確認する場合は、本文が指定する feedback_reporting.py または complete_prompt.py を直接読む
- reporter input の具体的な JSON schema 定義だけを確認する場合は、本文が指定する reporter_input.json を直接読む
- feedback 以外の issue の同一性、集約、現在状態、report cut の判断を確認する場合は、該当する report 仕様を直接読む
- 通常の subcommand の実装責務や一般的な log schema を確認する場合は、この文書ではなく対象機能の仕様・設計文書を読む

## hash
- 6bbf12559715306bc04139a246308a33978307b422a088e95ff265ed09473a7e

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
- cmoc が各ディレクトリへ自動配置する `INDEX.md` の役割、対象外条件、目次情報の構成を定める。
- 目次情報は、対象の責務と本文を読むべき条件・読まなくてよい境界を示す routing 情報として扱う。
- インデックス処理では、対象ディレクトリを深い順に処理し、ファイルシステムとの差分やハッシュ不一致を検出して目次情報を生成・削除・再生成する。
- 目次情報の生成は対象ごとの独立した agent call で行い、同一階層など安全な範囲では並列実行できる。
- インデックス由来の `INDEX.md` 差分は呼び出し単位で自動コミットされ、その他の既存差分はコミット対象から除外される。

## Read this when
- `INDEX.md` の配置対象・目次作成対象・除外規則を確認するとき。
- `INDEX.md` の形式や、Summary・Read this when・Do not read this when に求められる routing 情報の意味要件を確認するとき。
- ディレクトリのインデックス作成順序、ハッシュによる更新判定、生成・削除・再生成の挙動を確認するとき。
- 目次情報生成の agent call、並列実行、インデックス実行の前提条件、自動コミット範囲を確認するとき。

## Do not read this when
- 個別の実装ファイルの責務や CLI の具体的な挙動だけを調べるとき。
- 既存の `INDEX.md` の現在のエントリー内容を確認する必要があるときは、対象階層の実際の `INDEX.md` を直接読む。
- インデックス処理と無関係な仕様変更、テスト、開発環境、または一般的な文書作成の規則を調べるとき。

## hash
- a0fe6bff137b1bce89c7ca9e1f94144b866756e6c14c803a072c14260478efbc

# `misc_spec.md`

## Summary
- oracle file と realization file の正本責務、配置、委譲、優先関係、および相互の適合性判断を定義する雑多な仕様の入口。oracle file の扱い、realization file の実装・テスト方針、仕様から導ける修正対象を確認するときに読む。
- oracle file と realization file の分類規則、対象外 subtree、Git ignore、symlink・非通常ファイル、nested repository、列挙性能不変条件、回帰検証を扱うファイル列挙仕様の入口。doctor preprocess や realization refactor state の対象集合・列挙結果を調べるときに読む。
- work-root、cmoc 実行時の cwd、タイムスタンプ、cmoc-managed-branch など、cmoc の実行環境と変更範囲を解釈する補助仕様をまとめている。これらのプレースホルダーや履歴上の変更範囲の意味を確認するときに読む。

## Read this when
- oracle doc・oracle src・oracle test・realization implementation・realization test・realization ancillary の責務境界を判断するとき
- oracle file の分類、Git ignore を含む列挙、symlink や nested repository の扱い、列挙性能または回帰検証を扱うとき
- work-root、agent call の cwd、タイムスタンプ、cmoc-managed-branch の定義を確認するとき

## Do not read this when
- 個別の oracle doc、oracle src、oracle test の具体的な仕様や exact literal・schema・algorithm を直接確認する場合
- realization の具体的な実装責務やテスト手順だけを確認する場合は、それぞれ対象の src・test または専用の開発手順へ直接進む
- INDEX.md の既存エントリーや、本文に記載されていない将来用途・実装詳細を調べる場合

## hash
- 972bc96839e81baf79b1d1b4dfc9ab422660920e3db4e3bfd1e48d585ebe68b6

# `prompt_editor_input.md`

## Summary
- `prompt_editor_input.md` は、オリジナルプロンプトを入力する editor work file のライフサイクルを定義する仕様書です。初期内容・prompt 構築定義の参照先、work file と保存コピーの役割分担、エディタ起動条件、検証・一度だけの読み取り・保存・コメント除去・削除までの確定手順を扱います。editor lifecycle や prompt 入出力の挙動を確認・変更する際の入口であり、具体的な prompt 構築ロジック自体は本文が案内する oracle 実装を直接参照します。

## Read this when
- editor work file の生成、エディタ起動、入力確定、検証、保存コピー、コメント除去、削除の挙動を調査または変更するとき
- オリジナルプロンプトと完全プロンプトの境界、または editor input の信頼性・保存領域の扱いを確認するとき
- editor lifecycle の仕様と oracle 実装の参照先を把握してから関連実装を調査するとき

## Do not read this when
- prompt の具体的な初期テンプレートや完全 prompt の組み立てを直接確認したい場合は、本文が示す対応する oracle 実装を読むとき
- editor input の lifecycle に関係しない CLI 機能や別の仕様を調査するとき

## hash
- a8558b090259a2e9101f8ab4f6daf914c3299b086d73727437579a16b16f2a7e

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
- `oracle/doc/app_spec/sub_command` は、cmoc の各サブコマンドおよび主要な session・run lifecycle の正本仕様を集約する入口です。doctor、indexing、tui、oracle 操作、realization apply/refactor、feedback report、session fork/join/abandon などの実行条件、処理手順、状態遷移、report・終了経路を扱い、共通 lifecycle や個別仕様へ進むためのルーティング起点になります。

## Read this when
- cmoc のサブコマンドの仕様、引数、事前条件、実行手順、終了コードを確認・変更するとき
- primary report、診断結果、ログ、feedback、cleanup、エラー経路など、サブコマンド横断の完了契約を確認するとき
- session fork/join/abandon や realization fork、run join/abandon の lifecycle と状態遷移を確認するとき
- 対象サブコマンドの個別仕様から、参照される共通 lifecycle・feedback・prompt・起動規則へ進む必要があるとき

## Do not read this when
- 特定サブコマンドの内部実装、prompt の正確な文面、Structured Output schema、起動パラメータの詳細だけを確認したいとき
- raw observation、feedback state、normalization/verification、indexing 処理、merge conflict 解消など、本文から委譲される専用仕様を直接確認できるとき
- 実装責務、テスト規則、実行手順、oracle file や realization file の一般的な編集規則だけを確認したいとき
- 保存済み report の具体的な実例や生成物だけを調査するとき

## hash
- 1bb7dc7867bfdb96491eea03593c5b94df519577d03b33d68be96ce67ab3fe45

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
