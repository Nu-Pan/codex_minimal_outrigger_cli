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
- codex exec を用いた agent call の実行規約を定義し、path context、環境変数、preflight、argv 上書き、sandbox・詳細アクセス制限、provider/model、prompt、feedback、Structured Output、並列化、失敗時処理、ログ保存を扱う。
- Codex CLI 呼び出し仕様の実装・変更・レビューにおける、各 oracle doc と oracle src への委譲境界を示す上位の入口である。

## Read this when
- codex exec の起動引数、sandbox、承認設定、provider/model/reasoning effort、CODEX_HOME の扱いを確認するとき。
- agent call の cwd と repository/worktree root、path placeholder、ファイルアクセス制限、prompt の構築・stdin handoff、ログや session ID の保存規約を調べるとき。
- Structured Output の schema 保存・検証・補正、quota 待機、server capacity retry、想定外エラーの扱い、feedback reporter や editor input handoff の呼び出し規約を確認するとき。
- 本規約が参照する oracle doc や oracle src の責務分担を確認し、個別の実装詳細へ進む前のルーティング起点を決めるとき。

## Do not read this when
- 個別の path context、root 解決、prompt rendering、file access policy、AgentCallParameter の正確な構造を直接確認する場合は、本文が指定する対応する oracle src を読む。
- 特定の agent call の意味上の責務や作業範囲を確認する場合は、対応する oracle doc を直接読む。
- Windows toast 通知、feedback observation、editor input handoff など個別機能の正本仕様だけを確認する場合は、本文が指定する各 app_spec 文書へ直接進む。
- 既存テストの実行方法や品質検査の選択を確認する場合は、repository local の test_execution skill を読む。

## hash
- 4af46e5b9911c0c044b4eb6bc8270aecdc54fae83712bd1e8bb455dbdf05d769

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
- 非対話サブコマンドの console、primary report、サブコマンドログ、terminal result に関する共通契約の正本。自然言語、時間・パス表示、出力先、進行通知、primary report の保存、terminal result の分類・確定順序・表示内容、JSON Lines ログ、TUI と自動補完の境界を定める。個別サブコマンド固有の result、completion_reason、report 形式・保存先・終了コードなどは各サブコマンド仕様へ委ねる。

## Read this when
- 非対話サブコマンドの console 出力、primary report、terminal result、終了処理、ログ保存の共通挙動を実装・変更・確認するとき
- サブコマンドログの保存先、JSON Lines 形式、即時 flush、診断イベントの記録要件を確認するとき
- TUI、oracle investigation、oracle edit、自動補完と非対話サブコマンドの通知境界を判断するとき

## Do not read this when
- 個別サブコマンド固有の result、completion_reason、primary report の内容・保存先・要約方法、終了コードだけを確認するときは、該当するサブコマンド仕様を直接読む
- Windows toast の対象・発火順序・通知内容を確認するときは、windows_toast_notification.md を直接読む
- エラー分類や primary report 保存失敗時の詳細規則を確認するときは、error_handling.md を直接読む
- feedback observation の通知境界や detector rule を確認するときは、feedback_observation.md を直接読む
- CLI 自動補完の判定・console 出力・通常処理抑止を確認するときは、cli_auto_completion.md を直接読む

## hash
- d069aeff9f811da4a6fce18ebec8ffaa292b0a227d2ca306b83e424ce80e8ecf

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
- feedback subsystem 全体の目的、処理モデル、正本仕様の分担、既存 workload との境界、non-goal を定義する概要仕様。observation の収集、repository-local state、`cmoc feedback report` の詳細仕様へ進むための入口となる。

## Read this when
- feedback subsystem の目的や全体フローを確認するとき
- observation・active issue・report の関係や、normal publication と incomplete 診断 report の違いを確認するとき
- feedback に関する仕様書の担当範囲や既存 workload との境界を判断するとき
- feedback の詳細を読む前に、関連する正本仕様への入口を把握するとき

## Do not read this when
- observation の報告基準、収集経路、受け入れ検査、機械 detector、raw 保存の詳細だけを確認したいときは feedback_observation.md を読む
- repository-local state、report cut、checkpoint、atomic publication、cleanup の詳細だけを確認したいときは feedback_state.md を読む
- `cmoc feedback report` の事前条件、処理順序、normalization、verification、表示、終了結果の詳細だけを確認したいときは feedback_report.md を直接読む
- feedback と無関係な workload の仕様、実装、テストを調べるとき

## hash
- 56be7abd47ec53e9bcd3b8005cbf5e667104ebf66a959d85779903c9a6bea450

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
- run の fork から join または abandon までのライフサイクル、branch・worktree の隔離、run とサブコマンドの関係、および run-root 外への書き込み例外を定める規則文書。run の開始・終了、成果物の取り込み、隔離資源、管理データの保存境界を確認するための入口。

## Read this when
- run の fork、join、abandon の lifecycle や、編集 run と read-only investigation/review の扱いを確認するとき
- run の branch、commit、worktree、agent call の作業場所や path context を確認するとき
- run-root 外への書き込みが許される cmoc 管理データの境界を確認するとき

## Do not read this when
- run の永続化フィールドの具体的なスキーマを確認する場合は session state の run field を直接読むとき
- branch や worktree の命名・分岐元 commit の正本を確認する場合は branch model を直接読むとき
- ログ、feedback observation、feedback state の保存先や lifecycle の詳細を確認する場合は各専用仕様を直接読むとき

## hash
- a394e9c8c59241ed528734fb475e75175ea2d8a47d052e2540cf8a290745fec7

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
- `cmoc doctor` の明示的な preprocess 実行、引数・事前条件、全終了経路の primary report 保存を定義する入口。
- 編集 run の fork・join・abandon 共通 lifecycle、状態遷移、差分検査、merge、cleanup、report 要件を定義する共通入口。
- `cmoc feedback report` の report cut、agent 委譲、candidate 検証、publication、再開、失敗時 state・report 処理を定義する入口。
- `cmoc indexing` による作業ツリーの明示的インデクシング、事前条件、実行手順、primary report 保存を定義する入口。
- `cmoc oracle edit` のユーザー指示入力、本命・仕様削減 agent call、実行順序、編集境界、差分・report の扱いを定義する入口。
- `cmoc oracle investigation` の oracle file 調査指示入力、TUI 起動、調査境界、回答方針を定義する入口。
- `cmoc oracle review` のレビュー対象 scope、所見列挙・統合・検証・採否判定、隔離実行、レポート生成を定義する入口。
- `cmoc realization apply fork` の直近 oracle 差分を realization file へ反映する短い編集 workload、agent call、fork lifecycle、report、join 後処理を定義する入口。
- `cmoc realization refactor fork` の oracle／realization file 単位の追従調査・修正、refactor state 同期、unresolved target、編集 run lifecycle を定義する入口。
- `cmoc session abandon` の session branch と成果物を merge せず破棄する手順、未 join run の前提、state 更新、cleanup、report を定義する入口。
- `cmoc session fork` の local branch から session branch を作成する条件、初期 state 保存、branch 命名、失敗経路、primary report を定義する入口。
- `cmoc session join` の session branch を home branch へ merge して session を完了する条件、conflict 解消、state 更新、branch cleanup、report を定義する入口。
- `cmoc tui` のユーザープロンプト入力、cmoc 基本規定の注入、indexing・feedback 連携、AI Agent CLI／TUI 起動条件を定義する入口。

## Read this when
- doctor の引数、preprocess 実行、終了経路別 primary report を確認・変更・実装するとき。
- 編集 run の fork・join・abandon 共通条件、run state、隔離資源、想定内差分、merge・cleanup・report を確認するとき。
- feedback report の CLI 契約、report cut、normalization／verification、publication、再開、incomplete 診断、失敗時処理を確認するとき。
- indexing の引数、未コミット差分の扱い、doctor preprocess、INDEX.md 更新、実行要約 report を確認するとき。
- oracle edit のユーザー指示 handoff、本命・仕様削減 call、起動前検査、編集範囲、差分や commit の扱いを確認するとき。
- oracle file を根拠に調査する TUI の入力 lifecycle、起動手順、調査結果の回答方針を確認するとき。
- oracle のレビュー scope、所見成立・検証・採否、agent call の段階、隔離実行、レポート保存を確認するとき。
- apply fork の差分始点・終点、oracle rename、agent call 回数、realization 編集境界、fork 終了・report・join 後 hook を確認するとき。
- refactor fork の state schema、entry 同期、調査要求、file 単位の agent call、変更 path 検証、unresolved target、完了状態を確認するとき。
- session の成果物を home branch へ取り込まず破棄する際の前提、対象、state 遷移、cleanup、primary report を確認するとき。
- `cmoc session fork` の実行可能 branch、clean 条件、session branch 命名、初期 state、terminal result、primary report を確認するとき。
- session branch の home branch への merge、conflict、session state 更新、branch 削除、終了報告を確認するとき。
- `cmoc tui` の prompt editor input、cmoc 規定注入、indexing preflight、feedback observation、Codex CLI 起動、toast 通知を確認するとき。

## Do not read this when
- doctor preprocess の検証・修復内容そのものだけを確認するときは `doctor_preprocess.md` を直接読む。
- 個別 workload の fork 固有仕様、session lifecycle、state schema、report 共通形式、feedback 境界だけを確認するときは対応する正本を直接読む。
- raw observation の収集、feedback state schema、builder の正確な prompt／schema、INDEX.md 更新手順、共通中断仕様だけを確認するときは対応する正本を直接読む。
- インデクシング仕様そのもの、または `cmoc indexing` 以外のサブコマンドを確認するとき。
- oracle file の一般判断基準、prompt editor／codex exec 共通規約、doctor・indexing・feedback の詳細だけを確認するとき。
- oracle の判断基準、TUI prompt の正確な文面・起動 parameter、editor handoff、Codex CLI 設定範囲だけを確認するとき。
- oracle 本文の内容、個別 agent prompt、一般的なコード品質、INDEX.md や実装ファイルのレビューを確認するとき。
- file 単位の網羅的追従や refactor、共通 editing run、oracle／realization 適合性、apply の正確な launch parameter だけを確認するとき。
- 短い apply 追従ループ、oracle／realization 適合性の一般原則、共通 join／abandon、共通中断、変更要約生成だけを確認するとき。
- session join、未 join run の abandon、既 join 結果の rollback、session state schema の詳細だけを確認するとき。
- branch model、session state schema、timestamp 形式、session fork 以外の固有仕様だけを確認するとき。
- 汎用 git merge、session の共通事前条件、branch model の一般原則、feedback state 所有範囲、conflict agent prompt だけを確認するとき。
- 正確な prompt part・workload parameter、prompt editor handoff、oracle／realization や review の意味仕様、個別 indexing・feedback・toast 仕様だけを確認するとき。

## hash
- f4810a647d40d46a8c871c169b5df015081ef96fcbaf9d7732259fd7a08052d7

# `subcommand_interruption.md`

## Summary
- 中断可能な cmoc サブコマンドについて、ユーザー中断要求の対象範囲、Ctrl+C の通知、共通の完了処理、正常系としての扱い、中断後の個別仕様への参照先を定める正本仕様。
- 中断時の部分結果・primary report・state・terminal result・再開可否を確認するための共通入口。

## Read this when
- 中断可能サブコマンドの対象や追加条件を確認するとき
- Ctrl+C 受信後の停止、部分結果の確定、ログ・console 出力、終了イベントの扱いを確認するとき
- realization refactor、oracle review、feedback report の中断後の扱いを調べる前に共通規則を確認するとき

## Do not read this when
- 中断処理と無関係なサブコマンドの通常動作を確認するとき
- 個別サブコマンド固有の中断後 state や再開方法を確認するときは、各サブコマンド仕様を直接読む
- ログ形式や Windows toast 通知の詳細を確認するときは、参照先の正本仕様を直接読む

## hash
- 45c91724316ed6ba8d2d5ed2faffd6ebadee6f43d02caaedfa85008f41256155

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
- cmoc の基本的な呼び出し方法、初回セットアップ、session fork から session join までの標準 workflow を案内する利用手順書。oracle edit、realization apply、realization refactor の使い分けと、各 workload・編集 run の正本仕様への入口を示す。

## Read this when
- cmoc を初めて使うとき、または doctor、session fork、session join を含む標準 workflow を確認するとき。
- oracle edit、realization apply、realization refactor の進め方や、編集 run の共通 lifecycle を確認するとき。

## Do not read this when
- 個別 workload の目的や詳細な仕様を確認したいときは、本文から案内される各 workload の正本仕様を直接読む。
- oracle file の内容や realization の実装・リファクタ方法を調査するときは、この利用手順書ではなく対象の oracle file または該当する正本仕様を直接読む。

## hash
- bfab0c1287a69037aeeee6a1aafb48dc3abff6365a79a07fb09fe4f897c3a304

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
