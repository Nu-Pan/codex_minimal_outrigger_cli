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
- Codex CLI 呼び出しの基本規約、path context、環境変数、preflight、argv 設定上書き、sandbox と詳細な file access、prompt、feedback、Structured Output、並列実行、失敗時の retry・quota 待機を定める正本入口。
- cmoc が Codex CLI を起動・再開・記録する実装や、agent call の設定・制約・検証条件を確認する際の上位ルールを提供する。

## Read this when
- Codex CLI の `exec` 呼び出し、`resume`、TUI 境界、agent call の path context または cwd を変更・実装・レビューするとき。
- sandbox、file access policy、permission profile、provider/model/reasoning effort、環境変数、MCP reporter、editor input handoff の呼び出し単位設定を確認するとき。
- Structured Output の schema 検証・補正・session 再開、Codex call のログ保存、quota 枯渇や一時的サーバー障害の retry 方針を扱うとき。

## Do not read this when
- 個別 agent call の意味上の責務や判断基準だけを確認する場合は、対応する oracle doc を直接読む。
- `AgentCallParameter` の正確な field 名・型・既定値、path context の導出、prompt の構築・rendering、file access policy の正確な文面を確認する場合は、本文が委譲する対応する oracle src を直接読む。
- Codex CLI を使わない通常の実装・テスト・文書作業で、呼び出し規約を変更しない場合。

## hash
- 0171cf688dfa00b759f00ed91e91f8d1c5537c61ef34d25038b47741b0b997a6

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
- cmoc の各サブコマンド本命処理に先立ち、リポジトリと共通実行環境の検証・修復を担う前処理仕様。git 追跡対象の保証、refactor state の同期、feedback MCP reporter/client の互換性確認、必要な tracked 差分の commit を扱う。サブコマンド固有の事前条件や clean 状態の検査は対象外で、正常終了後に各サブコマンドが扱う。

## Read this when
- cmoc のサブコマンド開始前に、共通の環境検証・修復、追跡状態の保証、または refactor state の同期条件を確認するとき
- feedback MCP reporter/client の起動可否・protocol compatibility と、利用不能時に本命処理を degraded warning 付きで継続する規則を確認するとき
- doctor preprocess が扱う修復対象や、修復困難時のエラー終了条件を確認するとき

## Do not read this when
- サブコマンド固有の事前条件や git working tree・staging area の clean 状態を確認するとき
- oracle file と realization file の分類結果、refactor state の詳細 schema、または個別の reporter protocol 仕様そのものを確認するとき
- doctor preprocess 後の本命 workload の処理内容を確認するとき

## hash
- 90673019a5eddc9ac7b38b80a4325087f2ef6af8d9d8457dd0f2f7790bd26957

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
- feedback subsystem 全体の目的、観測から report publication または incomplete 診断 report までの処理モデルを示す共通仕様の入口。
- feedback observation、repository-local state、`cmoc feedback report` の責務分担と、既存 workload・自動注入・外部複製を含む境界を確認できる。

## Read this when
- feedback subsystem の全体目的や observation・issue candidate・active issue・report cut の関係を確認したいとき。
- normal publication と `incomplete` 診断 report の成立条件、verification verdict の扱い、feedback が workload の成功判定や state に与えない影響を確認したいとき。
- 個別仕様へ進む前に、観測収集・state 管理・`cmoc feedback report` の正本仕様の分担を把握したいとき。

## Do not read this when
- observation の報告基準、収集経路、受け入れ検査、machine detector、raw 保存を確認したい場合は feedback observation の正本仕様を直接読む。
- repository-local state、report cut、checkpoint、atomic publication、cleanup を確認したい場合は feedback state の正本仕様を直接読む。
- `cmoc feedback report` の事前条件、処理順序、normalization、verification、表示、終了結果を確認したい場合は同サブコマンドの正本仕様を直接読む。
- 特定の realization finding、indexing 結果、agent call の Structured Output、run・session・TUI の完了結果を調べる場合は、この仕様を入口にしない。

## hash
- a40a3918f66f726685b6dd2ccb16bc9b9c0ceba9d89ecd514fd5b9ff976c8c19

# `feedback_observation.md`

## Summary
- agent による observation 報告の基準、reporter の MCP interface、collector が確定する context、call-scoped transport、終了 lifecycle を定める正本仕様。
- observation の受け入れ検査、secret masking、path 制約、rate limit、rejection code、および degradation の扱いを確認する入口。
- 構造化 log に基づく detector の境界、初期 allowlist rule、issue key、threshold、除外条件を確認する対象。
- agent・machine observation の raw record、保存経路、durability、retention、publication 後の cleanup、terminal result の warning 条件を確認する対象。
- issue の同一性や現在状態の判断は扱わないため、feedback report の集約・threshold 判定や issue lifecycle を調べる場合は別の仕様へ進む。

## Read this when
- feedback observation をいつ人間へ報告するか、または報告しない条件を確認するとき
- cmoc_feedback の submit_observation 契約、入力検査、拒否結果、secret masking、capability 制約を変更・実装・レビューするとき
- reporter、collector、IPC、Codex call context、parallel call、TUI process の lifecycle を確認するとき
- structured log detector の初期 rule、machine issue key、recurrence threshold、除外される期待動作を確認するとき
- raw observation の保存形式、durability、pending retention、publication 後の cleanup、terminal warning を確認するとき

## Do not read this when
- feedback observation の集約結果、issue の同一性、現在状態、report cut の判定や公開処理そのものを確認するとき
- agent による observation 報告や detector、raw 保存に関係しない一般的な CLI 挙動を調べるとき
- この文書が参照する prompt builder や reporter input schema の具体的な実装詳細を直接確認すべきときは、それぞれの正本ファイルへ進む

## hash
- 90c542e7cc45c1b8d0170f3561ec20c85610e1a3e0ac1e3f212fe1bee12683ad

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
- run を workload 固有の fork から join または abandon まで隔離して扱う作業規則の入口
- run の lifecycle、branch、worktree、および run-root 外の cmoc 管理データ書き込み例外を定める上位規則

## Read this when
- run の fork・join・abandon の lifecycle や、run とサブコマンド呼び出しの関係を確認するとき
- run の branch・commit・worktree と agent call の作業場所を確認するとき
- run-root 外へ保存できるログ、session state、feedback 関連データの扱いの入口を確認するとき

## Do not read this when
- 永続化する run field の定義を確認したいときは session_state.md を直接読む
- run の branch・worktree の命名や分岐元 commit を確認したいときは branch_model.md を直接読む
- agent call の path context の正確な導出規則を確認したいときは codex_exec_rule.md を直接読む
- ログ、feedback observation、feedback state の保存先や lifecycle の詳細を確認したいときは各参照仕様を直接読む

## hash
- a53e17db8f55d1939a945f24f21b3f61bfc3a6ff0a4ecd41e636dacdcdb9dbe3

# `session_state.md`

## Summary
- cmoc workflow における session と、明示的な join を必要とする realization 編集 run の lifecycle、およびそれらを保持する JSON state の正本。session の状態、fork 元・commit、最後に join した apply run、active run の workload・branch・fork commit、状態遷移と共通事前条件を扱う。session 系サブコマンド、realization 編集 run の fork・join・abandon、または session state の整合性を確認・変更する実装や仕様を読む際の入口となる。

## Read this when
- session の作成・終了・fork・join・abandon に関する挙動を確認するとき
- realization apply/refactor run の状態、fork 情報、join・abandon 前提条件を実装または調査するとき
- session state JSON の field、初期値、状態遷移、差分検査の責務を確認するとき

## Do not read this when
- feedback の repository-local state やその lifecycle だけを扱うときは、feedback state の正本仕様を直接読む
- realization workload 固有の処理内容や編集責務だけを扱うときは、各 workload の仕様・実装を直接読む
- session や run の lifecycle、state 保存、join・abandon 条件に関係しない CLI 機能を扱うとき

## hash
- 9444cdd51d8c5f612690ba9b51a17c1606531bcc9cb66eb404f89c1e918598d0

# `sub_command`

## Summary
- cmoc のサブコマンド単位の実行契約を定義する仕様書群への入口。doctor、indexing、feedback、TUI、oracle 操作、session／run lifecycle、realization 操作の責務を扱う。
- 各サブコマンドの引数、事前条件、処理手順、状態遷移、agent call、report、終了経路、cleanup を確認するための上位ルーティング対象。

## Read this when
- 特定の cmoc サブコマンドの実装、テスト、仕様照合、または挙動調査を行うとき。
- session／run の開始・終了、oracle／realization の編集・調査、feedback report、indexing、doctor、TUI のいずれかの固有契約を確認するとき。
- 複数の処理段階や終了経路を持つサブコマンドについて、該当する個別仕様書を選ぶとき。

## Do not read this when
- branch model、共通 state schema、timestamp、interruption など、サブコマンド固有ではない正本仕様だけを確認したいとき。
- feedback observation／state、oracle と realization の一般原則、またはその他の共通仕様を直接確認したいとき。
- 特定仕様書の正確な prompt、Structured Output schema、起動パラメータ、または実装詳細だけを確認したいとき。

## hash
- 6a82ef731d1ca5b9fe46f6823a038e59e56e3491a12b04d4fafc223037a7f5bf

# `subcommand_interruption.md`

## Summary
- 実行中の中断可能サブコマンドに対する Ctrl+C の受け付け、確定済み部分結果の保持、正常系としての完了、primary report と terminal result の保存・出力を定める共通仕様。
- `realization refactor fork` と `feedback report` の中断対象、個別仕様への委譲、中断後の state・再開・checkpoint の扱いを確認する入口。

## Read this when
- 中断可能サブコマンドの対象範囲や、Ctrl+C をユーザー中断要求として処理する条件を確認するとき。
- 中断時の処理単位、state 更新、primary report、terminal result、Codex CLI 呼び出し停止などの共通動作を確認するとき。
- `realization refactor fork` または `feedback report` の中断後の state、再開方法、checkpoint 保存可否を確認するとき。

## Do not read this when
- 自然完了時や通常のエラー処理だけを確認する場合。
- 中断後の個別サブコマンドの詳細な state 遷移や再開手順を確認する場合は、各サブコマンド仕様を直接読む。
- ログの共通保存・出力形式や Windows toast 通知の詳細だけを確認する場合は、参照先の共通仕様を直接読む。

## hash
- 7897822644433226bba11d87a43a5e6c5c66c7c12c939cac37576d2c120e99ae

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
- cmoc の初回準備から session fork、oracle・realization の編集ループ、session join までの標準 workflow を案内する利用者向け入口。
- 各 workload の目的と、editing run に共通する lifecycle を正本仕様へ案内する。

## Read this when
- cmoc を初めて使用するときに、必要な初回操作と標準的な session 運用の全体像を確認したい場合。
- oracle edit、realization apply、realization refactor の使い分けや、編集 run の join・abandon の流れを確認したい場合。

## Do not read this when
- 特定 workload の詳細な目的や仕様だけを確認したい場合は、本文から案内される各 workload の正本仕様を直接読む。
- 実装、設計、テスト、環境構築など cmoc の内部開発規則を確認したい場合。

## hash
- 61819dfd7fd5fc71561c921dbf1c964446ac3d9b175e30f9cfeeb044d8f0e813

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
