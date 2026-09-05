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
- Codex CLI の `codex exec` 呼び出しにおける、agent call と Codex call の単位、path context、環境変数、引数上書き、sandbox、ファイルアクセス、prompt、Structured Output、retry・quota 待機、並列実行、ログ保存の規約を定める正本。
- Codex CLI を呼び出す実装や、その起動パラメータ、セッション再開、出力補正、feedback reporter、editor input handoff、入出力ログの扱いを確認するための入口。

## Read this when
- Codex CLI の `codex exec` または `codex exec resume` の呼び出し経路を実装・変更・レビューするとき。
- agent call の path context、file access mode、sandbox、provider・model・reasoning effort、環境変数、MCP 設定を決めるとき。
- Structured Output の保存・検証・補正、quota 待機、capacity retry、Codex session ID、stdout・stderr・output ログの扱いを確認するとき。
- Codex CLI 呼び出しに関する feedback observation または editor input handoff の lifecycle と設定を確認するとき。

## Do not read this when
- Codex CLI 自体の一般的な利用方法や製品仕様を調べるだけで、cmoc の呼び出し規約を変更・検証しないとき。
- 特定の builder が所有する agent call の詳細だけを確認する場合は、まず対応する builder または参照先の oracle doc を読むとき。
- Codex CLI を呼び出さない realization の実装や通常のテスト手順だけを扱うとき。

## hash
- 729f32312d9e249304d31004868cf6811bea461b8f407e1d99443b213518c358

# `codex_model_provider.md`

## Summary
- 各 agent call 種別に対応する model provider、Model、Reasoning Effort の直接設定と、provider-local 設定 mapping の責務を定義する入口。
- 設定値を Codex CLI の起動前に検証し、変換・丸め・fallback せず argv へ渡す規則と、cmoc が provider の運用を担わない境界を扱う。

## Read this when
- agent call 種別ごとの model provider、Model、Reasoning Effort の設定や既定値を確認するとき
- provider 定義、provider-local key、未知の provider の扱いを確認するとき
- 設定値を Codex CLI に反映する責務境界や、cmoc が provider 運用を保証しない範囲を確認するとき

## Do not read this when
- 設定データ構造、field 名、型、既定値の正確な定義だけを確認したい場合は、指定された cmoc_config.py の定義を直接読むとき
- agent_call_kind から Codex CLI argv へ反映する詳細規則だけを確認したい場合は、codex_exec_rule.md の該当節を直接読むとき
- prompt、sandbox、file access policy、network access、通知設定の仕様を確認したい場合

## hash
- 5d18119343b2bb16952d91246f29024d921a3f1dc2a762633e0c14edd859f4d4

# `console_and_file_log.md`

## Summary
- 非対話サブコマンドの console 出力、primary report、terminal result、サブコマンドログに関する共通契約の正本。時間・パス表示、出力先、終端分類、確定順序、ログ記録要件、および TUI・自動補完との境界を定める。

## Read this when
- 非対話サブコマンドの stdout・stderr・進行通知・エラー表示を設計または確認するとき
- primary report の保存条件、表示内容、保存失敗時の扱いを確認するとき
- terminal result の分類・表示順序・終了後の出力禁止を確認するとき
- サブコマンドログの保存先、JSON Lines 形式、即時 flush、診断イベント要件を確認するとき
- TUI サブコマンドや cmoc oracle edit の report・terminal result 境界を確認するとき

## Do not read this when
- 個別サブコマンド固有の result、completion_reason、primary report 内容、保存先、終了コードだけを確認したいとき
- Windows toast の通知仕様だけを確認するときは windows_toast_notification.md を直接読むとき
- 自動補完プローブの判定や通常処理の抑止だけを確認するときは cli_auto_completion.md を直接読むとき
- エラー分類や internal failure の一般規則だけを確認するときは error_handling.md を直接読むとき

## hash
- e2176d0abe25bd024fd4780aef42816fbaa17c4570d95a390de97d6c91e77a8c

# `doctor_preprocess.md`

## Summary
- 各サブコマンドの本命処理開始前に共通して実行される doctor preprocess の検証・修復責務と実行手順の入口。
- git 追跡・非追跡状態、refactor state の schema／entry 同期、feedback reporter/client の protocol 互換性を含む前処理条件を扱う。

## Read this when
- doctor preprocess が何を検証・修復し、どの条件で cmoc をエラー終了または degraded warning とするか確認したいとき。
- `.cmoc/gu`、`.agents`、`.cmoc/gt/ar/config.json`、refactor state の追跡状態や同期規則を確認するとき。
- feedback MCP reporter/client の事前検証範囲と、利用不能時に本命 workload を継続する扱いを確認するとき。

## Do not read this when
- 特定サブコマンド固有の事前条件や clean 状態の検査だけを確認したいとき。
- doctor preprocess 共通処理ではなく、feedback observation の reporter protocol の正本仕様そのものを確認したいとき。
- 実際の oracle／realization file の列挙内容や refactor state の詳細 schema を直接確認できる対象があるとき。

## hash
- 202af51afd65b87c28120f47260fe8ed717519cac323b77cfebef61d4a9fabd2

# `editor_input_handoff.md`

## Summary
- Codex TUI の agent が、待機中の prompt editor input の editor work file 全体へ完成済み内容を渡すための MCP handoff 機能。
- active target の検証、単純な全体上書き、受付期間、直列化、最終読み取りまでの handoff 境界と非目標を定義する。
- prompt editor input や Codex 実行規則、overwrite input schema、handoff instruction の正本へ進むための入口を示す。

## Read this when
- Codex TUI の agent から editor work file へ内容を渡す handoff の仕様を確認するとき。
- cmoc_editor_input.overwrite の利用条件、target の有効期間、上書き動作、submission の直列化を確認するとき。
- handoff と通常の aw ツリー書き込み、sandbox、file access mode、editor の最終確定方法との境界を確認するとき。

## Do not read this when
- prompt editor input の writer 境界や最終読み取りそのものを確認したい場合は、prompt_editor_input.md を直接読むとき。
- Codex TUI への MCP や handoff instruction の注入規則を確認したい場合は、codex_exec_rule.md の該当節を直接読むとき。
- cmoc_editor_input.overwrite の厳密な input schema を確認したい場合は、overwrite_input.json を直接読むとき。
- handoff instruction の正確な文面を確認したい場合は、editor_input_handoff.py の該当関数を直接読むとき。
- target の自動発見、editor の自動保存・終了、排他的 writer 管理など、本文の non-goal に含まれる機能だけを調べるとき。

## hash
- 0f80dd7f18a47c52a1b592ce0bc2b4c1c2d9194dba4d8d17b00a60bee8c2491c

# `error_handling.md`

## Summary
- handled failure と internal failure の分類、およびエラー終了時の state 確定・primary report 保存・terminal result 確定に関する共通規則を定める。
- handled failure と internal failure の表示内容、スタックトレースの扱い、正常結果として扱う状態、個別仕様との優先関係を確認するための入口。

## Read this when
- エラー終了を handled failure または internal failure に分類する必要があるとき。
- primary report、terminal result、サブコマンド終了イベント、終了コード、スタックトレースの共通契約を実装・確認するとき。
- エラー時の console 表示や、attention・incomplete・completed_with_unresolved・ユーザー中断要求の扱いを確認するとき。
- 個別仕様にエラー時の state、rollback、report、次の操作、終了コードの記載がない事項の共通規則を確認するとき。

## Do not read this when
- console と terminal result の具体的な出力先、表示順序、共通 field を確認することが目的のときは、正本である console_and_file_log.md を直接読む。
- 中断可能サブコマンドのユーザー中断要求の詳細を確認することが目的のときは、subcommand_interruption.md を直接読む。
- 個別サブコマンド固有の state、rollback、report、次の操作、終了コードの仕様を確認することが目的のときは、その個別仕様を直接読む。

## hash
- d54257e6201d3f23187ea47dc9e99aa3be007fb4821bffe4774ae11062f14991

# `feedback.md`

## Summary
- feedback subsystem の目的、用語・結果分類、処理モデル、正本仕様の分担、既存 workload との境界、および non-goal を定義する上位仕様。
- observation の収集から `cmoc feedback report` による remediation、publication、active issue cleanup までの全体方針を確認する入口。

## Read this when
- feedback observation の報告基準や保存対象と、feedback report の実行・表示・終了結果の境界を確認したいとき。
- intake wave、high-watermark、checkpoint、publication、issue の結果分類を含む feedback の状態遷移と処理モデルを把握したいとき。
- feedback の正本仕様が observation、repository-local state、feedback report にどう分担されるかを確認したいとき。

## Do not read this when
- 個別の observation 受け入れ検査や機械 detector の詳細だけを確認したいときは、feedback observation の正本を直接読む。
- repository-local state、checkpoint、high-watermark、publication、cleanup の詳細だけを確認したいときは、feedback state の正本を直接読む。
- `cmoc feedback report` の CLI 事前条件、agent call、commit、merge、表示、終了結果の詳細だけを確認したいときは、feedback_report の正本を直接読む。
- realization apply や realization refactor の仕様、または通常 workload の完了判定を確認したいとき。

## hash
- 2e611d9f0fa101b09c951e8ad35ffd1f9ed1e6826aa9fdb57c73848b20afaa8c

# `feedback_observation.md`

## Summary
- feedback observation の報告基準、agent-facing reporter/collector transport、受け入れ検査、機械的 detector rule、raw observation の保存と retention を定める正本仕様。
- 現在の workload で解消できず、再発防止・反復的浪費の削減・外部挙動に関わる人間意図の確定につながる、根拠ある問題だけを報告するための入口。

## Read this when
- feedback observation を agent から報告する条件、v1/v2 submission の互換処理、rejection code、secret masking、件数・rate の受け入れ制約を確認するとき。
- reporter から collector までの call-scoped context、capability 境界、終了処理、durable 保存経路を設計・実装・検証するとき。
- structured log から machine observation を検出する allowlist rule、threshold、issue key、除外条件を確認するとき。
- raw observation の保存単位、idempotency、durability、publication 後の cleanup、pending warning の扱いを確認するとき。

## Do not read this when
- 個別の prompt 文面や prompt builder の実装を変更・確認するだけで、feedback observation の報告・収集契約自体を扱わないとき。
- 既存 observation の issue identity、remediation 可否、人間対応の要否、現在状態や report の集約を確認するとき。
- 通常の subcommand の結果や run state など、feedback observation の保存・warning が変更してはならない本命 workload の仕様だけを確認するとき。

## hash
- f2d868890635af501e05233a0278aa173ec290c0361b035a808e54e56fe59eab

# `feedback_state.md`

## Summary
- feedback remediation が使う repository-local state の正本仕様。active generation、current pointer、pending observation、immutable な intake wave、高水位境界、checkpoint、report cut、publication completion、incomplete 診断 report、および cleanup の責務とライフサイクルを定義する。
- 正常 publication と再開・失敗回復を検討する際に、active issue と threshold 未満 aggregate の保持範囲、atomic publication、hash 検証、排他、cleanup の境界を確認するための入口。

## Read this when
- feedback state の配置、artifact の意味、canonical JSON・hash・durability・排他制御を実装または検証するとき。
- feedback report の wave loop、high-watermark、normalization/remediation checkpoint、report cut、publication、incomplete 処理、または cleanup と run lifecycle の整合を確認するとき。

## Do not read this when
- raw observation の収集規則そのものを確認する場合は、feedback observation の正本を直接読む。
- feedback report の invocation 中断・エラー報告形式を確認する場合は、feedback_report 仕様を直接読む。
- 編集 run の join・abandon 共通仕様だけを確認する場合は、editing_run 仕様を直接読む。

## hash
- a87272b7244eabf156238f3c394adf15f62e678a6417130d98ea7ab286044d6d

# `indexing.md`

## Summary
- 対象は、cmoc が作成する INDEX.md の配置対象、目次情報の形式・意味要件、routing、インデクシング処理、および並列実行・実行条件を定義する。
- INDEX.md の自動生成・更新の仕組みと、目次情報生成を agent call に委譲する境界を確認するための入口である。

## Read this when
- INDEX.md の生成・更新対象や、目次情報のフォーマットと routing 要件を判断するとき。
- インデクシングの処理順序、ハッシュによる更新判定、自動コミット、並列実行の可否を確認するとき。
- INDEX.md エントリー生成 agent call の責務や実行条件を確認するとき。

## Do not read this when
- 個別のアプリケーション仕様や実装の挙動を確認したいだけで、INDEX.md の運用やインデクシング規則を扱わないとき。
- 特定ファイル・ディレクトリの内容や最新状態を判断する場合。INDEX.md の routing で対象を絞った後、実際の対象本文を直接読むべきとき。

## hash
- 59e02dd5f8106a8b5dbd29076504ed438195e152aa57fc8f8124986fb72c8e24

# `oracle_and_realization.md`

## Summary
- oracle file と realization file の役割・分類、および oracle doc、oracle src、oracle test、realization implementation、realization test、realization ancillary の責務を定義する共通契約。
- 正本責務の重複禁止、oracle doc から oracle src への委譲、正本責務に基づく優先関係を定める。
- oracle file、realization file、INDEX.md、既存実装や test を扱う際の判断基準と、realization file の適合性を判断する基準を示す。関連する詳細な prompt 構築規則や個別仕様への入口となる。

## Read this when
- 対象ファイルを oracle file、realization file、uncategorised file のいずれに分類するか判断するとき。
- oracle doc と oracle src のどちらが仕様事項の正本を担うか、または正本間の不整合を扱うとき。
- realization implementation、realization test、realization ancillary の責務境界を確認するとき。
- oracle file の要求に対する realization file の修正要否や適合性を判断するとき。
- oracle file を扱う判断基準、realization file を扱う判断基準、または INDEX.md のルーティング根拠を確認するとき.

## Do not read this when
- 個別の正本仕様、prompt の正確な文面・構築順序・schema を確認するだけの場合は、対応する oracle doc または oracle src を直接読む。
- realization implementation の具体的な挙動や realization test の具体的な検証内容を調べる場合は、対象の src または test を直接読む。
- prompt literal 固有の実行時指示や優先関係を確認する場合は、指定された codex_exec_rule.md を読む。
- 通常の実装方法、テスト実行方法、または一般的な品質改善だけを調べる場合は、この責務分類文書を起点にしない。

## hash
- 2a00bba8b6eca689c24875c926ffe7cee1eedc9d12046de44be63c161af2a130

# `oracle_and_realization_file_enumeration.md`

## Summary
- oracle file と realization file の分類対象を、常時対象外 root・nested Git working tree・Git ignore 判定・oracle/realization の配置条件に基づいて定義する規範文書。doctor preprocess と realization refactor の refactor state 同期が利用する列挙結果の契約を扱い、traversal の pruning、非通常ファイルや symlink の扱い、repository 単位の ignore 判定性能不変条件、回帰検証要件への入口となる。

## Read this when
- oracle file または realization file の完全な列挙条件、対象外 subtree、nested repository、Git ignore の意味を確認するとき
- ファイル traversal、pruning 境界、symlink・非通常ファイルのエラー条件を実装または検証するとき
- doctor preprocess や realization refactor の refactor state 同期で、列挙結果や性能不変条件の根拠を確認するとき
- 分類結果の回帰 fixture や Git subprocess・ignore source・traversal 回数の検証条件を確認するとき

## Do not read this when
- 単一の oracle file または realization file の本文内容だけを確認したいときは、対象ファイルを直接読む
- INDEX.md のルーティング情報や文書構成だけを確認したいときは、該当する INDEX.md を読む
- 列挙・traversal・Git ignore・回帰検証に関係しない機能の仕様や実装を扱うとき

## hash
- 816b4fa3fe98ff0ee3f0a55d6123630f0198e52394d4cf3702191aaaaa78c8ba

# `prompt_editor_input.md`

## Summary
- エディタ作業ファイルにオリジナルプロンプトを入力・確定するライフサイクルの正本。初期内容の構築委譲先、handoff の適用、検証・最終読み取り・保存・コメント除去・削除、および作業ファイルと保存コピーの役割分離を定める。
- プロンプトエディタ入力の仕様や保存記録の扱いを確認するための入口であり、完全な prompt skeleton や抽出後 prompt の構築仕様そのものは担当しない。

## Read this when
- editor work file の生成から確定・削除までの lifecycle、handoff による全面上書き、対象パス・regular file・symlink の検証条件を確認するとき
- 最終読み取り結果の保存コピー、HTML コメント除去後のオリジナルプロンプト、agent が editor work file を参照してはならない境界を確認するとき
- editor 初期入力の構築先や、完全 prompt の構築を担う別の正本仕様への参照関係を確認するとき

## Do not read this when
- 完全 prompt skeleton や抽出後の完全 prompt の正確な構築手順を確認したいとき
- editor input handoff の target lifecycle、MCP interface、上書きや失敗の詳細だけを確認したいときは、本文が指定する handoff の正本を直接読むとき
- 実行時に生成された editor input や skeleton の内容自体を正本仕様として確認したいとき

## hash
- b806eedf76a951aed434eda6db62b809ae91d8d6cedcca6a47f7f476cd28cd3c

# `run_isolation.md`

## Summary
- run の fork から join または abandon までの隔離作業 lifecycle と、run の成果物・状態を管理する境界を定める。
- run 固有の branch、worktree、agent call の path context、および run-root 外への cmoc 管理データ書き込み例外を確認する入口。

## Read this when
- run の作成、完了、取り込み、破棄の lifecycle を実装・確認するとき。
- run の branch、worktree、agent call の作業場所や path context を判断するとき。
- run 作業と session state、ログ、feedback state など repository-local 管理データの境界を確認するとき。

## Do not read this when
- branch、commit、worktree の具体的な命名規則だけを確認したいときは、正本である branch model を直接読む。
- 永続化する run field のスキーマだけを確認したいときは、session_state の run field を直接読む。
- ログ、feedback observation、feedback state の保存仕様だけを確認したいときは、それぞれの指定された正本仕様を直接読む。

## hash
- 5575f423b305dead5e687877f02a52581dfb267c69053f153ac31a29b90887b8

# `session_state.md`

## Summary
- cmoc session と編集 run の lifecycle を管理する JSON state の正本。session/run の状態、所属 branch、fork commit、join 後の apply commit、および状態遷移を定義する。

## Read this when
- session fork、join、abandon、workload 開始、session 終了などで active session context や編集 run の事前条件・状態遷移を確認するとき
- session state file の schema、run kind の扱い、feedback report の自動 join・recovery、join 後の初期化規則を実装または検証するとき

## Do not read this when
- feedback の repository-local state の保存対象や lifecycle を確認する場合は feedback state の正本を読むとき
- 具体的な CLI サブコマンドの実装責務や realization の配置を確認する場合は、対応する実装または設計仕様を直接読むとき
- session state 以外の JSON schema や、既存 state file の実データを確認するだけのとき

## hash
- f110d4b4f98de844e95d2461e20b3943ea2719fabf9c2852823dc04180973be4

# `sub_command`

## Summary
- cmoc の各サブコマンド仕様を、CLI 契約、実行前提、処理手順、状態遷移、終了結果、primary report の確認先として案内する入口。
- session・editing run・feedback remediation・oracle/realization・doctor/indexing・TUI など、サブコマンド固有の責務と共通仕様との参照境界を扱う。

## Read this when
- cmoc の特定サブコマンドの引数、実行前提、処理手順、状態遷移、終了経路、primary report を確認したいとき
- 複数のサブコマンド仕様から、調べたい挙動を担う仕様ファイルを選びたいとき
- sub_command 配下の仕様を変更・実装照合し、コマンド固有仕様と共通仕様の参照境界を確認したいとき

## Do not read this when
- branch model、session state、run isolation、timestamp などサブコマンド横断の正本だけを確認したいときは、対応する正本仕様を直接読む
- 特定コマンドの実装詳細、prompt builder の選択ロジック、または doctor preprocess・indexing など参照先仕様の詳細だけを確認したいときは、対応する実装や正本仕様を直接読む
- 編集 run の共通 lifecycle だけを確認したいときは editing_run を、feedback remediation 固有の詳細だけを確認したいときは feedback_report と関連仕様を直接読む

## hash
- 29eb600f632a7bf61bb524333e8a65559f84e14f0a38da489fcf30f8b4f384c2

# `subcommand_interruption.md`

## Summary
- 中断可能サブコマンドにおける Ctrl+C のユーザー中断を、処理単位・確定済み部分結果・state 更新・primary report・terminal result の整合性を保つ正常系として定義する共通仕様。
- realization refactor fork と feedback report の中断後の扱い、および中断可能サブコマンドを追加できる条件への入口。

## Read this when
- 対象サブコマンドで Ctrl+C によるユーザー中断を正常系として扱う条件や共通動作を確認するとき。
- 中断時の処理停止境界、確定済み結果の保持、完了処理、Codex CLI の再呼び出し禁止を確認するとき。
- realization refactor fork または feedback report の中断後の state・publication・次の操作を調べる入口を探すとき。

## Do not read this when
- 中断対象ではないサブコマンドの通常動作だけを確認するとき。
- refactor run や feedback report の個別の state 遷移・再開可否・publication 規則の詳細を確認するときは、それぞれの個別仕様を直接読むべき。
- ログの共通保存・出力規則や Windows toast 通知の詳細だけを確認するときは、対応する正本仕様を直接読むべき。

## hash
- 718662c5d938046fe6e2970da200898492505b5c4098a80774cf8aa9bcfe05b2

# `timestamp.md`

## Summary
- タイムスタンプ文字列の正規フォーマットと、各構成要素の桁数・ゼロ埋め規則・ローカルタイムゾーンを定義する仕様文書。タイムスタンプの生成・解析・検証条件を確認する際の入口となる。

## Read this when
- タイムスタンプの文字列表現、各フィールドの桁数、ゼロ埋め、ミリ秒精度、タイムゾーンの扱いを確認するとき。

## Do not read this when
- タイムスタンプの具体的な生成処理や呼び出し箇所を実装・調査するときは、まずその実装対象を直接読む場合。

## hash
- 76873df5347a74035c75e23ec5ae779eec11c2741a6234fc754ab5e503a9c40e

# `usage.md`

## Summary
- cmoc の初回準備から session fork、各 workload の反復、feedback report、session join までの標準的な利用 workflow を示す。
- apply、refactor、oracle edit、feedback report の詳細仕様へ進むための利用者向け入口である。

## Read this when
- cmoc を初めて利用するとき。
- 作業 session の開始・反復・完了までの流れを確認したいとき。
- workload の使い分けや editing run の共通仕様を確認する入口を探しているとき。

## Do not read this when
- 個別 workload の目的や詳細な挙動を確認したいとき。
- editing run の lifecycle 詳細を確認したいとき。
- 特定の oracle file や realization file の内容を直接確認したいとき。

## hash
- 2d43b356139644680733e75856e03e17ba0a64a7e33922cc1608910ddbc9c097

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
