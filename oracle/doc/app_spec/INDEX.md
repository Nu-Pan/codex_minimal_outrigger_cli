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
- cmoc から Codex CLI を呼び出す際の正本規約。agent call と Codex call の単位、call-scoped path context、CODEX_HOME、preflight、argv による設定上書き、sandbox と詳細なファイルアクセス制限、model/provider、prompt・ログ・stdout/stderr・session ID の扱い、Structured Output の検証と補正、並列実行・失敗時の再試行や待機、および feedback reporter の運用を定める。Codex 呼び出しの実装や実行失敗、出力補正、ログ保存の責務を確認する際の入口となる。
- 本規約は Codex CLI 呼び出し方法とその周辺の実行契約を扱う。個別 agent call の意味上の責務や判断基準、model provider の詳細、Windows 通知、feedback event の詳細、開発環境・テスト実行などは本文が参照する対応する oracle 文書を直接確認する。

## Read this when
- cmoc が codex exec または codex exec resume を起動する実装を変更・レビューするとき
- Codex CLI の argv、sandbox、CODEX_HOME、model/provider、承認設定、prompt の stdin 渡し、ログ保存を確認するとき
- Structured Output の schema 保存、検証、同一 session での補正、差分不変性、補正不能時の扱いを実装・調査するとき
- Codex call の並列実行、quota 枯渇、モデル容量エラー、その他の失敗時処理を確認するとき
- call-scoped path context、ファイルアクセス制限、feedback reporter の起動・受付・終了境界を確認するとき

## Do not read this when
- 個別 agent call の意味上の責務や model class・reasoning effort の選択基準だけを確認する場合は、対応する agent call oracle doc を直接読む
- model provider の解決規則だけを確認する場合は、参照先の codex_model_provider oracle doc を直接読む
- Windows toast 通知の effective configuration や callback 条件だけを確認する場合は、参照先の windows_toast_notification oracle doc を直接読む
- feedback observation の event schema や安定 field だけを確認する場合は、参照先の feedback_observation oracle doc を直接読む
- 開発環境、設計責務、テスト規約、テスト実行方法だけを扱う場合は、それぞれの dev_rule oracle または skill を直接読む

## hash
- 244466cd4b8835d54f645e00beac6522443bc1587ef9b6ef78c77be5be19d02c

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
- agentおよび機械的検出によるobservationの報告基準、MCP reporterの境界と受け入れ検査、collector/transportのcontext確定・保存経路・call終了処理、allowlist済みdetector rule、raw observationのdurability・retention・cleanup・terminal表示を定める正本仕様。feedback報告、収集、検出、保存の挙動を実装・変更・検証する際の入口となる。

## Read this when
- observation報告の対象条件や、agentがreporterを呼ぶべき範囲を確認するとき
- cmoc_feedback MCP interface、入力検査、secret masking、rate limit、rejectionの契約を実装・変更するとき
- collectorのcall-scoped context、capability、IPC、保存順序、lifecycleを設計・検証するとき
- 機械的log検出のallowlist、rule threshold、issue key、期待動作の除外条件を扱うとき
- raw observationのファイル保存、atomic durability、publication後cleanup、pending warningの挙動を扱うとき

## Do not read this when
- observationやfeedback機能とは無関係なCLI機能、通常のagent workload、または別の正本仕様だけで完結する作業を行うとき
- collector内部の具体的実装配置やテスト実行手順だけを確認したいときは、該当する設計・テスト・実行ルールを直接読むとき
- issueの同一性、現在状態、集約結果、report cutの処理そのものを確認するときは、別途その責務を定める仕様を読むとき

## hash
- 23e1c7a394aede3066771236a0a9272165759608eecb3860edcba8fc29e754a4

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
- oracle file と realization file の責務分離、判断基準、適合性、および配置を定義する仕様断片。
- oracle/realization file の分類、Git ignore を含む列挙、pruning、symlink・非通常ファイル、nested repository、性能不変条件、回帰検証を扱う実装・テストの入口。
- work-root、cmoc 実行時の path context、timestamp、managed branch の意味を確認するための上位仕様。

## Read this when
- oracle と realization の責務境界や、正本仕様から実装へ反映する条件を確認するとき
- oracle/realization file の分類、Git ignore、pruning、symlink、nested repository 対応を実装または検証するとき
- ファイル列挙の性能不変条件や回帰検証の境界を確認するとき
- work-root、実行時 path context、timestamp、managed branch の定義を確認するとき

## Do not read this when
- 特定の oracle doc・oracle src・oracle test・realization implementation・realization test の具体的な要求や挙動だけを調べる場合
- oracle/realization の責務境界やファイル列挙契約に関係しない一般的な文書・実装・テスト作業を行う場合

## hash
- efc24da79d27774ab9c80a27765443be3816e4e0e69b7ff5a5694656461246fd

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

# `prompt_policy.md`

## Summary
- `prompt_policy.md` は、cmoc が agent call に渡す prompt の責務、情報量、正本との境界、policy block の選択・注入、Structured Output の受理条件、summary/goal の役割分担、および prompt 構築上の記法を定める仕様文書。prompt builder／acp builder の oracle src、関連する oracle doc、実行時生成物、installed skill、INDEX routing の責務境界を確認するための入口となる。

## Read this when
- agent call 用 prompt の内容・構築順序・policy block の選択や一対一対応を変更または確認するとき
- prompt の正本が oracle doc と oracle src のどちらにあるか、realization implementation の責務範囲を判断するとき
- Structured Output schema・決定論的事後条件・補正 prompt の受理条件の境界を確認するとき
- summary と goal の記述責務、placeholder、cmoc_block／cmoc_ref、GFM・日本語などの prompt 記法を確認するとき

## Do not read this when
- prompt の意味仕様そのものを確認する必要があり、本文で参照される個別の oracle doc を直接読むべきとき
- agent call の正確な文面や builder 実装を調査する作業で、prompt builder または acp builder の oracle src を直接読むべきとき
- prompt 生成後の realization 側の受け渡し実装だけを確認し、prompt policy の規定に触れないとき

## hash
- bf73a12e27f926c012d653517d1252c1f291ed0e1de6b9dfd46874092be605c7

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
- cmoc の主要サブコマンドと session／run lifecycle、realization、oracle、feedback、TUI に関する正本仕様をまとめた入口。各コマンドの引数・事前条件・実行手順・状態遷移・終了時 report を確認する際に、該当サブコマンド仕様へ進むために読む。
- doctor や indexing の前処理・report、editing run と session の fork／join／abandon、realization apply／refactor、oracle の investigation／review／edit、feedback report、tui の起動契約を扱う。個別機能の詳細は各仕様本文および本文が指定する下位の正本へ委譲する。

## Read this when
- cmoc のサブコマンド仕様を調査・実装・レビューし、対象コマンドの正本仕様への入口を選ぶとき
- doctor、indexing、session／run lifecycle、realization、oracle、feedback、TUI の挙動や report・終了経路を確認するとき

## Do not read this when
- 特定サブコマンドの詳細仕様が既に分かっており、対応する個別仕様を直接読む方が適切なとき
- 実装責務、テスト実行手順、個別の oracle／realization file の内容など、本文が指定する別の正本だけを確認したいとき

## hash
- 259de7492197ecfdf703bdc7f7c438936ed747d4d78f7d3731679f0618bd650d

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
