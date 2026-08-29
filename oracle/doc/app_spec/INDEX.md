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
- cmoc が Codex CLI を呼び出す際の agent call・Codex call の基本規約、path context、環境変数、CLI 引数、sandbox、ファイルアクセス、provider/model、prompt、feedback、editor input handoff、ログ、Structured Output、並列実行、失敗時処理を定める入口。

## Read this when
- `codex exec` または `codex exec resume` の起動仕様、呼び出し単位の設定、cwd・worktree root の扱いを確認するとき。
- sandbox と詳細なファイルアクセス制限、permission profile 禁止、model/provider/reasoning effort の argv 上書き規則を確認するとき。
- prompt の stdin 渡し、feedback reporter、editor input MCP、ログ保存、session ID、Structured Output の検証・補正・失敗処理を実装または調査するとき。
- quota 枯渇、レートリミット、モデル容量不足、その他の Codex CLI 失敗時の retry・待機・resume 方針を確認するとき。

## Do not read this when
- 個別 agent call の意味上の責務や判断基準だけを確認する場合は、先に対応する oracle doc を読む。
- AgentCallParameter の正確な field 名・型・既定値だけを確認する場合は、委譲先の basic.py を直接読む。
- path context の導出アルゴリズムだけを確認する場合は、委譲先の path_model.py と prompt builder を直接読む。
- Windows toast 通知、feedback observation、editor input handoff など個別機能の詳細な正本仕様だけを確認する場合は、各 app_spec oracle doc を直接読む。

## hash
- 33d225382ef43bf3bb71e3e4302e77c993b9bb5b6aee7c76f5625d9191424f5c

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
- editor work file への完成内容の限定的な上書き引き渡しを定義する共通機能の仕様。target lifecycle、MCP overwrite interface、上書き条件、失敗時の扱いを扱う。
- prompt editor input の writer 境界や最終読み取り順序、Codex call 側の capability・sandbox 境界、canonical schema・policy・prompt placement の正本への入口を示す。

## Read this when
- prompt editor input から待機中の editor work file へ agent の成果物を渡す設計・実装・検証を行うとき。
- handoff target の発行から受付停止、submission の drain、無効化、最終読み取りまでの lifecycle を確認するとき。
- cmoc_editor_input.overwrite の入力、accepted/rejected result、target 検証、単純な全体上書き、retryable 判定を確認するとき。
- handoff が agent の filesystem 権限や sandbox 境界を拡張しないこと、直接書き込みへの fallback を禁止する責務を確認するとき。

## Do not read this when
- prompt editor input 自体の writer 境界や target 終了後の最終読み取り順序だけを確認する場合は、指定された prompt editor input の正本を直接読む。
- Codex call の MCP 設定、call-scoped capability、approval behavior、sandbox 境界だけを確認する場合は、指定された Codex exec rule の正本を直接読む。
- overwrite tool の厳密な field、型、pattern、上限を確認する場合は、canonical JSON Schema を直接読む。
- handoff policy の agent 向け文面や complete prompt への条件付き配置だけを確認する場合は、指定された prompt builder の正本を直接読む。
- handoff とは無関係なサブコマンド固有の receiver、target、MCP interface、一般的な file write や command execution の仕様を確認する場合。

## hash
- 78bf79689501c3a43517e554b4aa9ef72c69c73164e7685d544ee66633cf79ac

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
- オリジナルプロンプトを入力する editor work file の lifecycle と確定手順を定める仕様書です。
- editor 初期内容の構築委譲先、handoff の扱い、work file と保存コピーの責務分離を確認する入口です。
- 検証済みファイルの一度きりの読み取り、未加工保存、HTML コメント除去、成功時の削除と失敗時の保持を扱います。

## Read this when
- editor work file の生成・編集受付・handoff・終了処理を実装または確認するとき
- editor input の最終確定、保存コピー、オリジナルプロンプト抽出の挙動を確認するとき
- editor input と保存記録の書き込み主体や信頼境界を確認するとき
- 初期コメントや template の構築定義がどこへ委譲されるかを確認するとき

## Do not read this when
- editor input handoff の target lifecycle や MCP interface の詳細仕様を確認したいとき
- 完全 prompt skeleton やサブコマンド固有の完全 prompt 構築を確認したいとき
- editor の起動パラメータや prompt 構築そのものの正本仕様を確認したいとき
- 実行時に生成された editor input や skeleton を保存仕様・文面仕様として参照したいとき

## hash
- 179acdc39281fb894b94a07931f15ae09baad0e1c159ae63a61d7df90b8aefa7

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
- `cmoc doctor` の実行契約、事前条件、doctor preprocess 呼び出し、および全終了経路の primary report 保存を定義する仕様。
- workload 固有の編集 run に共通する fork・join・abandon lifecycle、状態遷移、差分検査、merge、cleanup、report を定義する仕様。
- `cmoc feedback report` の report cut、observation 検証・集約、agent による normalization／verification、正常 publication と incomplete report の処理を定義する仕様。
- `cmoc indexing` の引数、作業ツリー差分の扱い、doctor preprocess、インデクシング実行、および primary report を定義する仕様。
- `cmoc oracle edit` の入力、agent call の順序、oracle file の編集境界、indexing preflight、session 条件、report と終了処理を定義する仕様。
- oracle file を対象とする調査サブコマンドの入力受け渡し、TUI 起動、読み取り専用境界、調査結果の回答責務を定義する仕様。
- oracle snapshot のレビュー対象、所見の成立条件、agent call 段階、統合・検証・採否判定、および report を定義する仕様。
- 直近の oracle file 変更を realization file に反映する realization apply fork の対象差分、agent call、編集境界、report、join 後処理を定義する仕様。
- realization refactor fork の対象選択、refactor state、調査ループ、未解決 target、完了・中断・エラー、および join 後同期を定義する仕様。
- `cmoc session abandon` による session branch の破棄、state 更新、cleanup、rollback、および primary report を定義する仕様。
- `cmoc session fork` の分岐元、branch 作成、session state 初期化、事前条件、命名、および primary report を定義する仕様。
- `cmoc session join` の session branch merge、conflict 解消、state 更新、branch cleanup、および primary report を定義する仕様。
- `cmoc tui` のユーザープロンプト受領、cmoc 契約の注入、起動パラメータ構築、AI Agent CLI/TUI 起動、および関連する handoff・indexing・feedback 規則を定義する仕様。

## Read this when
- 該当するサブコマンドの引数、事前条件、実行順序、状態遷移、終了経路、report 要件を実装・変更・レビューするとき。
- 編集 run の共通 lifecycle、workload 固有 fork、join／abandon、差分検査、merge、cleanup の責務境界を確認するとき。
- feedback observation から active issue を生成し、report cut、候補検証、publication、incomplete 診断を扱うとき。
- oracle file の編集・調査・レビュー、または realization file への反映・refactor を行うとき。
- session の fork、join、abandon における branch 操作、session state、conflict、cleanup を確認するとき。
- ユーザー入力から AI Agent CLI/TUI を起動するサブコマンドの共通契約を確認するとき。

## Do not read this when
- doctor preprocess、indexing、feedback state／observation、run isolation、session state、branch model、editor input、Codex CLI 起動規則など、本文が正本として委譲する詳細だけを確認したいときは、対応する正本を直接読む。
- 編集 run ではなく外側の session lifecycle を確認したいときは、session fork／join／abandon の該当仕様を読む。
- workload 固有の処理ではなく、編集 run 共通 lifecycle だけを確認したいときは、対象 workload の仕様ではなく共通仕様を読む。
- 正確な prompt 文面、Structured Output schema、起動パラメータの選択理由、agent builder の実装詳細を確認したいときは、委譲先の builder または schema を直接読む。
- report の共通形式や state schema だけを確認したいときは、各サブコマンド仕様ではなく対応する共通正本を直接読む。

## hash
- 7910059570de3a1b0ca581dd41da8d26f960fccce2a65cf7a316b8782af319a9

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
