# `cli_auto_completion.md`

## Summary
- `_CMOC_COMPLETE` が存在する呼び出しを自動補完用プローブとして扱うための境界と規則を定める。
- 自動補完処理より前に cmoc 通常実行向けの前処理・検査・副作用を行わず、補完に必要な出力だけを許可する。

## Read this when
- 自動補完用プローブで通常実行向けの前処理・検査・副作用を抑止する条件を確認するとき
- 自動補完用プローブの stdout/stderr 出力制約を確認するとき
- 通常の cmoc 実行と CLI ライブラリの補完処理との境界を確認するとき

## Do not read this when
- Windows toast 通知に固有の自動補完プローブ境界だけを確認したいとき
- サブコマンド未指定判定、カレントディレクトリ変更、session/run 状態検査、ログ作成、INDEX 更新、cmoc 形式のエラーレポートなど、通常実行時の個別規則だけを確認したいとき

## hash
- 5984f914f917b5166222542c4723e63cd36412462c22c9e76f7862c766e5f755

# `codex_exec_rule.md`

## Summary
- `codex exec` を用いる agent call の共通規約を定義し、path context、sandbox・詳細なファイルアクセス制限、prompt、Structured Output、ログ、quota・retry・resume、並列実行などの判断基準を示す入口。
- Codex CLI 呼び出しの引数上書き、`$CODEX_HOME`、feedback reporter、editor input handoff、および call・session 情報の保存要件を確認するための正本。

## Read this when
- cmoc の `codex exec` 呼び出し、AgentCallParameter の構築、Codex CLI の sandbox や設定上書きを変更・実装するとき。
- agent call の path context、file access policy、prompt 構築、Structured Output の検証・補正、session resume、quota 待機、retry、並列化を判断するとき。
- Codex CLI のログ、session ID、feedback observation、editor input handoff の lifecycle や保存形式を確認するとき。

## Do not read this when
- 個別 agent call の意味上の責務や workload 固有の判断基準だけを確認する場合は、対応する oracle doc を先に読む。
- Codex CLI を呼び出さない実装、または本書が扱う共通呼び出し規約と無関係な仕様・テストを直接調べる場合。

## hash
- e7d60bf2ed16309b0179073ab07e46ab8eefb9f0692eec9ee72f202fc261563e

# `codex_model_provider.md`

## Summary
- agent call 種別ごとに model provider ID、Model 名、Reasoning Effort 名を直接設定し、Codex CLI の argv へそのまま渡す仕様を定義する。
- provider 定義 mapping と provider-local 設定の扱い、未知の設定を起動前にエラーとする条件、および secret を保存しない制約を定義する。
- cmoc は provider の取得・起動・管理や応答品質・認証を保証せず、model provider 設定以外の prompt・sandbox・通知設定は変更しない。

## Read this when
- agent call 種別に応じた model provider、Model、Reasoning Effort の設定方針を確認するとき
- provider ID、provider-local 設定、未知の provider の扱い、または Codex CLI 起動前の検証範囲を確認するとき
- cmoc が model provider に対して担う責務と担わない運用・保証範囲を確認するとき

## Do not read this when
- CodexCallConfig、CodexModelProviderConfig、CmocConfigCodex の具体的な field 名・型・既定値を確認したいとき
- agent_call_kind から Codex CLI の argv へ設定を反映する詳細規則を確認したいとき
- prompt、sandbox、file access policy、network access、通知設定の一般的な仕様だけを確認したいとき

## hash
- 861ec8aa33a7e3c8bdd04cdc715ba222522cbce11dfce8374e40989c3511a373

# `console_and_file_log.md`

## Summary
- 非対話サブコマンドの console、primary report、サブコマンドログ、terminal result に関する共通契約の正本。
- 実行 ID、時間・パス表示、進行通知、終端結果の確定・表示順序、JSON Lines ログの要件を定める。
- TUI、自動補完、個別サブコマンド仕様との適用境界を示す共通ルール。

## Read this when
- 非対話サブコマンドの出力、primary report、terminal result、終了処理、またはサブコマンドログの仕様を確認・変更するとき。
- 共通の表示形式、ログ記録項目、feedback observation の記録、TUI・自動補完への適用範囲を判断するとき。

## Do not read this when
- 個別サブコマンド固有の result、completion_reason、primary report の形式・保存先・終了コードを確認する場合は、該当する個別仕様を直接読む。
- Windows toast の詳細や CLI 自動補完の判定規則だけを確認する場合は、それぞれの専用仕様を直接読む。

## hash
- 50b250dba134651e9de90c936d222b35990f10e1c07add00e8a13934cabc3c79

# `doctor_preprocess.md`

## Summary
- 各サブコマンドの本命処理開始前に、cmoc 共通の実行環境を検証・可能な範囲で修復し、必要な追跡状態と feedback reporter/client の事前互換性を確認する preprocess の責務・手順・失敗時の扱いを定義する入口。

## Read this when
- doctor preprocess が何を検証・修復してから各サブコマンドへ進むか確認したいとき
- `.cmoc/gu`、`.agents`、agent realization 設定・refactor state の git 追跡状態や同期要件を確認したいとき
- feedback MCP reporter/client が利用不能または protocol 不一致の場合の degraded warning と本命処理継続の扱いを確認したいとき
- doctor preprocess と、各サブコマンド固有の事前条件検証や working tree の clean 状態検査との責務境界を確認したいとき

## Do not read this when
- 特定サブコマンド固有の事前条件や本命処理の仕様だけを確認したいとき
- git clean 状態の検査方法だけを確認したいとき
- feedback observation の reporter interface の完全な正本仕様を確認したいときは、feedback observation の仕様を直接読むとき
- realization refactor state の詳細な schema や oracle・realization file の分類規則そのものを確認したいときは、それぞれの正本仕様を直接読むとき

## hash
- fa92e7e3d4b741ce2964d7c9768cc7d7dff5ffe845c1118563fba114f4ee44fc

# `editor_input_handoff.md`

## Summary
- 日本語技術文書のルーティング入口として、agent から待機中の prompt editor input へ完成内容を渡す editor input handoff の責務と、MCP 経由の全体上書き・target 検証・受付順序を扱う。
- handoff の正本分担、active target のライフサイクル、agent-facing MCP interface の境界、および直接編集・最終読み取りを含む確定方法を確認する必要がある場合に読む。

## Read this when
- Codex TUI agent が人間指定の active target へ完成済み内容を渡す処理を実装・変更・レビューするとき。
- cmoc_editor_input.overwrite の利用条件、target の有効期間と同一 repository 検証、editor 終了後の最終入力確定順序を確認するとき。
- prompt editor input の writer 境界や handoff instruction、overwrite input schema の正本への委譲関係を確認するとき。

## Do not read this when
- prompt editor input の通常の writer 境界や最終読み取りだけを確認する場合は prompt_editor_input.md を直接読む。
- Codex TUI への MCP・handoff instruction の注入規則だけを確認する場合は codex_exec_rule.md の該当節を直接読む。
- overwrite の JSON input schema の形式だけを確認する場合は overwrite_input.json を直接読む。
- active target を使わない通常の aw ツリーへの agent 書き込みや、handoff 以外の editor 操作を扱う場合。

## hash
- 616c2e5129df87f81df1f8c90c999a2d74a1ce8adabb6327bd2175cd13dd91ae

# `error_handling.md`

## Summary
- handled failure と internal failure の分類、エラー終了の確定、primary report・terminal result・サブコマンドログの共通契約を定めるエラー処理の正本。
- エラー種別ごとの表示規則、スタックトレースの保存・表示条件、正常結果およびユーザー中断要求との境界を確認する入口。
- 個別仕様に特別なエラー処理の指定がない場合に適用する共通規則を扱う。

## Read this when
- エラーが handled failure または internal failure のどちらに該当するか判断するとき
- エラー終了時の state 確定、rollback、後処理、primary report 保存、terminal result 確定の順序を確認するとき
- handled failure と internal failure の console、stderr、サブコマンドログにおけるスタックトレースおよび診断情報の扱いを確認するとき
- attention、incomplete、completed_with_unresolved、またはユーザー中断要求をエラーとして扱うべきか確認するとき
- 個別仕様に特別なエラー時の指定がない場合の共通ルールを確認するとき

## Do not read this when
- console と terminal result の出力先、表示順序、共通 field の詳細だけを確認するとき
- ユーザー中断要求の詳細な正常系処理だけを確認するとき
- 特定サブコマンド固有の state、rollback、report、次の操作、終了コードの指定だけを確認するとき

## hash
- a6ea2d366264052db800d4378e5d339f474267d17c29049a157d6b53c78fab63

# `feedback.md`

## Summary
- feedback subsystem 全体の正本仕様。観測の収集から issue identity の確定、intake wave と high-watermark に基づく remediation、結果分類、publication、active issue の cleanup、既存 workload との境界、および non-goal を定義する上位の入口。

## Read this when
- feedback observation の収集・保存条件、issue の remediation 結果分類、feedback report の処理モデルや publication 条件を横断的に確認するとき
- feedback 関連の各正本仕様（観測収集、repository-local state、feedback report）の責務分担や相互境界を確認するとき
- 既存 workload の成果物を feedback issue として扱えるか、または feedback が他の成功判定・state・retry・recovery に影響するかを判断するとき

## Do not read this when
- 観測の具体的な報告基準・受け入れ検査・機械 detector・raw 保存だけを確認したいときは feedback_observation.md を読む
- repository-local state、intake wave、high-watermark、checkpoint、publication、cleanup の詳細だけを確認したいときは feedback_state.md を読む
- cmoc feedback report の CLI 事前条件、agent call、commit、merge、表示、終了結果だけを確認したいときは feedback_report.md を読む

## hash
- 59eb07be774e715e2a3dffff6f206d6fef68c07a7c5a3b6c624429ffb65cd0a4

# `feedback_observation.md`

## Summary
- feedback observation の報告基準、agent-facing reporter、collector/transport、受け入れ検査、機械的な log 検出、raw observation の保存・durability・retention を定める正本仕様。feedback の issue identity、remediation 可否、現在状態の判断は扱わない。

## Read this when
- agent が workload 外で解消できず、具体的根拠のある問題を feedback observation として報告する条件や、reporter の入力・結果・互換処理を確認するとき。
- feedback reporter と collector の context 確定、call lifecycle、保存経路、capability 境界、失敗時の degradation 方針を確認するとき。
- observation の受け入れ検査、secret masking、detector rule の初期 allowlist・threshold・issue key、raw record の保存単位・durability・cleanup・pending warning を確認するとき。

## Do not read this when
- feedback observation の issue identity、remediation の可否、または現在状態を判断する必要があるとき。
- prompt への正確な feedback reporting 文面や complete prompt への配置だけを確認するときは、本文ではなく指定された prompt builder の正本実装を直接読む。
- report 切り出しや集約、remediation intake の具体的な処理仕様だけを確認するときは、それらを定める下位仕様を直接読む。

## hash
- bbe7b1de9708646ff9574877caad6ca044ea4caf4d3749e8a48366a07865d2d9

# `feedback_state.md`

## Summary
- feedback remediation run が使用する repository-local state の正本仕様。active generation、current pointer、pending observation、intake wave、high-watermark、checkpoint、report cut、publication completion、正常／incomplete report、atomic publication、cleanup、および run lifecycle との整合を定義する。
- feedback state の配置、artifact の責務、canonical JSON と hash、durability、writer lock、issue identity、active issue と machine aggregate の保持条件を確認するための入口。
- wave loop の入力固定、collector の受理境界、remediation 結果の正式 checkpoint、publication 前後の検証・merge・cleanup 順序を確認するための入口。

## Read this when
- feedback report の active state、pending observation、issue identity、recurrence aggregate の保存・更新仕様を実装または変更するとき。
- intake wave、高水位境界、checkpoint、report cut、publication completion の生成・検証・再開動作を扱うとき。
- 正常 report の atomic publication、incomplete 診断 report、cleanup、publication／join／abandon 失敗からの回復条件を確認するとき。

## Do not read this when
- raw observation の収集形式や detector rule 自体を確認するだけの場合は、指定された feedback observation の正本仕様を直接読む。
- feedback report の Markdown 内容や invocation report の生成条件だけを確認する場合は、feedback_report の正本仕様を直接読む。
- 編集 run の join／abandon 共通仕様だけを確認する場合は、editing_run の正本仕様を直接読む。

## hash
- 17b0426857aedf5738ac7afac91e94f49cd9a1aabedde234468665e427b34017

# `indexing.md`

## Summary
- `{{work-root}}` における `INDEX.md` の配置対象、目次対象、記載構成、ハッシュ計算、更新・自動コミットの仕様を定義する正本仕様。
- インデクシングを深いディレクトリから処理する規則と、目次情報を独立した agent call で生成する単位・並列実行条件・実行タイミングを定める。
- `INDEX.md` を routing 情報として利用する際の意味要件と、対象本文の代替にしない境界を示す。

## Read this when
- `INDEX.md` の自動生成・更新・削除条件を確認するとき
- インデクシング対象のディレクトリやファイル、ハッシュの算出方法を確認するとき
- 目次情報生成の agent call、処理順序、並列化、実行タイミング、自動コミットの仕様を確認するとき
- `INDEX.md` の Summary、Read this when、Do not read this when に求められる routing 情報の意味要件を確認するとき

## Do not read this when
- 特定のファイルやディレクトリの実装内容・仕様内容を調べるだけで、`INDEX.md` の生成や routing の規則を確認する必要がないとき
- 個別の `INDEX.md` エントリー本文を作成する際に、対象ファイルの内容から責務や読む条件を判断でき、インデクシング全体の仕様を参照する必要がないとき
- 実際の対象本文の最新状態や詳細を確認する必要があるとき

## hash
- 1f56b1b17e5e13169a4895399e7b7cbe485d9d8aada7d017e9bab3d992edcd9e

# `oracle_and_realization.md`

## Summary
- oracle file と realization file の分類、正本責務、優先関係、および相互の適合性判断を定義する共通契約の入口。oracle doc・oracle src・oracle test と realization implementation・test・ancillary の役割分担を確認できる。
- 正本仕様の委譲、prompt literal との関係、未定義部分の扱い、仕様と実装の不整合を修正対象とする基準を扱う。

## Read this when
- oracle と realization のどちらが仕様・実装・テストを所有するか判断するとき
- oracle doc から oracle src へ委譲された exact literal、構築方法、選択値、schema の優先関係を確認するとき
- realization file を仕様へ適合させる作業の対象範囲や修正根拠を確認するとき
- 関連する oracle file や installed skill の扱い、未定義部分の補完境界を決めるとき

## Do not read this when
- 具体的な prompt の構築順序・文面・rendering・schema の定義だけを確認したい場合は、委譲先の oracle src を直接読むとき
- realization implementation、test、または ancillary の具体的な実装内容だけを調べる場合は、該当する realization file を直接読むとき
- 個別のアプリケーション要求や判断基準を確認する場合に、この共通契約だけで完結しないときは、対応する oracle doc を読むとき

## hash
- 19bdfd485f73ff97bdec11f8f6209f6e9d56e80c337fd76c019025599d8b80a5

# `oracle_and_realization_file_enumeration.md`

## Summary
- oracle file と realization file の列挙対象を決める正本仕様。常時対象外 root、nested Git working tree、Git ignore、regular file と symlink の分類、traversal/pruning 境界、および一括 ignore 判定の性能不変条件を定義する。
- doctor preprocess と realization refactor の refactor state 同期で使う列挙結果の契約と、full glob 基準に対する回帰・性能検証の入口。

## Read this when
- oracle/realization file の列挙、分類、pruning、nested repository の扱い、symlink や非通常ファイルのエラー条件を実装・変更・レビューするとき。
- Git ignore 判定を最適化するとき、または列挙結果と refactor state の整合性や回帰検証の要件を確認するとき。

## Do not read this when
- 列挙仕様そのものではなく、doctor preprocess や realization refactor の個別実装詳細を直接確認したいとき。
- 単に oracle/realization file の内容を読むだけで、列挙対象・Git ignore・traversal・性能契約に関係しないとき。

## hash
- 61dd4d6219f504a3701062572aae99c6684d00f41f1ec6bf36195d32f32525d9

# `prompt_editor_input.md`

## Summary
- オリジナルプロンプトを入力する editor work file のライフサイクルと、確定後の保存・抽出・削除を定める仕様。
- editor 初期内容、editor input handoff、完全 prompt の構築仕様へ進むための入口。

## Read this when
- editor work file の生成、handoff による上書き、最終読み取り、検証、保存、コメント除去、削除または失敗時の保持を確認するとき。
- オリジナルプロンプトの入力結果と保存コピーを分離する責務、または後続 agent の参照禁止を確認するとき。
- editor input と完全 prompt・prompt skeleton の責務境界や、builder・サブコマンド固有仕様への委譲先を判断するとき。

## Do not read this when
- 初期コメントや template の正確な構築方法だけを確認したい場合は、editor input builder の仕様へ直接進むとき。
- handoff の target lifecycle、MCP interface、上書き条件、失敗処理だけを確認したい場合は、editor input handoff の正本へ直接進むとき。
- 完全 prompt skeleton やサブコマンドごとの prompt 構築規則だけを確認したい場合は、該当する TUI・oracle investigation・oracle edit の仕様へ直接進むとき。

## hash
- 41a5b59b12bd3d0eade984f80ffa12e14954a22c0f4dd0ef0a90e6302379c212

# `run_isolation.md`

## Summary
- run の fork から join または abandon までの隔離作業ライフサイクル、branch/worktree の扱い、および run-root 外への書き込み例外を定める作業規則。

## Read this when
- run の開始・終了方法、明示的な join が必要な編集 run と self-joining／read-only 等の境界を確認するとき。
- run の branch、worktree、agent call の作業場所、または cmoc 管理データの書き込み先に関する扱いを確認するとき。
- run と session、feedback state、ログ、session state の境界を確認するとき。

## Do not read this when
- run の永続化フィールド定義そのものを確認する場合は session_state.md を直接読むとき。
- run branch の命名・分岐元・worktree の正本定義を確認する場合は branch_model.md を直接読むとき。
- agent call の詳細な path context や Git metadata の読み取り制限を確認する場合は codex_exec_rule.md を直接読むとき。
- ログ、feedback observation、feedback state の保存仕様だけを確認する場合は、それぞれの指定された正本仕様を直接読むとき。

## hash
- b9a15bef02fe27b8f494d4fcf2f8e2604ed93c29f9edfd03b905f2cfa32c3be2

# `session_state.md`

## Summary
- cmoc session と編集 run の lifecycle を一意に定める永続 JSON state の正本。session/run の状態、所属 branch、fork commit、join 済み apply の基準を定義し、開始前提条件と状態遷移を規定する。

## Read this when
- session の新規作成、active session context の検証、編集 run の開始・join・abandon・recovery の挙動を確認するとき。
- session または run の state、kind、branch、fork commit の意味や、feedback_report の自動 join・失敗 recovery を確認するとき。

## Do not read this when
- feedback の repository-local state の保存対象や lifecycle を確認したいときは、feedback state の正本仕様を直接読む。
- session/run state の具体的な実装配置や CLI の責務分担だけを確認したいときは、対応する設計仕様・実装を直接読む。

## hash
- 7215bb34b07a7a985256395c064c78aa694c858e6d65a9f3d149c8b51dbcfcaf

# `sub_command`

## Summary
- doctor の実行契約と終了時の primary report 保存要件を定義するコマンド仕様。
- 編集 run の共通 lifecycle、状態遷移、隔離資源、join・abandon、report、merge 後処理を定義する上位共通仕様。
- cmoc feedback report の remediation run、observation 正規化、issue 処理、publication、recovery、結果分類を定義する正本仕様。
- cmoc indexing の実行条件、doctor preprocess、INDEX.md 更新、commit、primary report を定義するサブコマンド仕様。
- cmoc oracle edit の editor input、agent call、oracle file 編集境界、report、終了処理を定義するサブコマンド仕様。
- oracle file を根拠に調査結果を回答する oracle investigation の入力、TUI 起動、変更禁止、結果報告を定義するサブコマンド仕様。
- oracle file の変更を realization file へ反映する realization apply fork の差分範囲、agent call、変更境界、commit、run state、report を定義する仕様。
- oracle file と realization file の調査・修正ループ、refactor state、unresolved target、完了・中断・エラー時の report を定義する realization refactor fork の正本仕様。
- アクティブな session を home branch へ merge せず破棄する session abandon の事前条件、cleanup、状態遷移、rollback、primary report を定義する仕様。
- 現在の branch から cmoc session branch を作成し、session state と primary report を保存する session fork の実行契約。
- 完了済み session branch を home branch へ no-ff merge する session join の事前条件、conflict 解消、state 更新、cleanup、primary report を定義する仕様。
- cmoc 固有契約の注入から doctor preprocess、editor input、起動パラメータ構築、AI Agent CLI/TUI 起動までを定義する tui の全体仕様。

## Read this when
- doctor コマンドの引数、事前条件、実行手順、または全終了経路の primary report を確認するとき。
- 編集 run の fork、join、abandon、run state、branch/worktree、差分、merge、cleanup、terminal report の共通要件を確認するとき。
- feedback observation を issue candidate に集約し、remediation、wave 処理、commit/rollback、publication、recovery、終了コードを確認するとき。
- 明示的な indexing の実行条件、未コミット差分の扱い、doctor preprocess、INDEX.md 更新、commit、完了報告を確認するとき。
- oracle edit の実行順序、起動条件、editor input、agent call、oracle file の編集境界、primary report、失敗時の扱いを確認するとき。
- oracle file を根拠に調査する command の入力 lifecycle、専用 TUI 起動、調査結果の報告、変更禁止を確認するとき。
- realization apply fork の追従差分、対象 file、agent call、realization file のみの変更、commit、run state、fork report を確認するとき。
- realization refactor fork の調査・修正順序、refactor state、unresolved target、完了・中断・エラー処理、report を確認するとき。
- session を home branch に取り込まず破棄する手順、保護対象、cleanup、状態遷移、rollback、primary report を確認するとき。
- session fork の実行条件、分岐元、session branch、session state、成功時の terminal result、失敗時の rollback と report を確認するとき。
- session join の merge 条件、source/target branch、conflict 解消、session state 更新、branch cleanup、primary report を確認するとき。
- cmoc tui の実行手順、契約注入、未コミット差分の扱い、indexing preflight、feedback observation、Windows toast、Codex CLI 起動条件を確認するとき。

## Do not read this when
- doctor preprocess の検証・修復内容や個別診断の正本仕様だけを確認するとき。
- workload 固有の intake、issue 処理、publication、refactor 同期、session lifecycle、session state、run isolation の詳細だけを確認するとき。
- raw observation の収集形式、feedback 全体の用語・結果分類、repository-local state schema、agent prompt/schema の具体定義だけを確認するとき。
- インデクシング処理の詳細仕様、doctor の診断動作、実装内部構造、INDEX.md のルーティング規則、report の一般形式だけを確認するとき。
- oracle file の一般的な編集判断、prompt 構築、Codex exec 共通規約、indexing、doctor、session state、toast の詳細だけを確認するとき。
- oracle file 自体の内容、editor handoff 共通仕様、TUI 共通仕様、builder の正確な prompt 文面、realization file の実装を直接確認するとき。
- 共通の editing run lifecycle、prompt/builder、oracle-realization 適合性、または特定 realization file の内容だけを確認するとき。
- realization apply の詳細、共通 fork/join/abandon lifecycle、oracle-realization 適合性基準だけを確認するとき。
- session join、run abandon、session state の schema・状態遷移だけを確認するとき。
- session fork 以外の session サブコマンド、branch model、session state schema、timestamp 形式だけを確認するとき。
- 通常の git merge wrapper、session state、branch model、feedback state、error handling の詳細だけを確認するとき。
- editor input lifecycle、prompt part と workload 固有 builder、oracle-realization、indexing、feedback observation、toast の詳細だけを確認するとき。

## hash
- 248a41d4e4249d72aa5b6ce6c8eaa349866291e97abddddac9237c80c2cfc652

# `subcommand_interruption.md`

## Summary
- 対象は、ユーザーの Ctrl+C による中断要求を正常系として扱うサブコマンド共通仕様の入口であり、中断可能サブコマンドの範囲、通知、確定済み結果の保持、完了報告、再開・join/abandon の扱いを確認するために読む。
- `realization refactor fork` または `feedback report` の中断時の共通動作や、個別仕様へ進む前の中断処理の全体像を確認する際に使う。

## Read this when
- 中断可能サブコマンドの対象範囲や追加条件を確認するとき。
- Ctrl+C の受け付け、finalization 区間、処理単位の停止・完了、primary report と terminal result の保存・出力要件を確認するとき。
- ユーザー中断後の refactor run の扱い、feedback report の joinable 状態、publication・cleanup・再開可否の共通境界を確認するとき。

## Do not read this when
- 中断対象が `realization refactor fork` または `feedback report` に限定され、個別サブコマンドの state・checkpoint・publication 手順だけを確認したいときは、それぞれの個別仕様を直接読む。
- 通常完了や一般的なエラー処理、通常のログ保存・console 出力の規則だけを確認したいときは、対応する個別仕様または `console_and_file_log.md` を直接読む。

## hash
- 46b74e94867381fa209f59fc8c458cc5950299955eb909d9cdba362827339b8e

# `timestamp.md`

## Summary
- 実行時のローカルタイムゾーンを用いるタイムスタンプの文字列表現と、各構成要素のゼロ埋め桁数を定義する仕様。

## Read this when
- タイムスタンプの生成・解析・表示形式、各日時要素の桁数、またはタイムゾーンの扱いを確認するとき。

## Do not read this when
- タイムスタンプ形式そのものではなく、実行時刻の取得方法や処理ロジックを確認・変更するとき。

## hash
- fdee683f00be4a26b05890895f8b4de3bf6d39a1ec7910a70edc96f4e2fbfc84

# `usage.md`

## Summary
- cmoc の初回セットアップから session fork、仕様・実装変更、feedback、session join までの標準 workflow を案内する入口。
- realization apply/refactor、oracle edit、feedback report の使い分けと、編集 run に共通する lifecycle の参照先を示す。

## Read this when
- cmoc を初めて使うとき、または session を開始して仕様・実装変更を進める手順を確認したいとき。
- 各 workload の使い分けや、編集 run の共通 lifecycle の参照先を確認したいとき。

## Do not read this when
- 特定 workload の目的・制約・操作仕様だけを確認したい場合は、本文が参照する各 workload の正本仕様を直接読むとよい。
- cmoc の内部実装や個別コマンドの詳細を調査する場合。

## hash
- fabf1f9f88b48030e38309dcace56857ab21589ff025ba80779cbc42a5538e45

# `windows_toast_notification.md`

## Summary
- Windows 11 上の WSL2 から表示する toast 通知の適用範囲、通知境界、内容、発火条件、安全な transport、自動補完時の抑止条件を定義する正本仕様。
- 非対話サブコマンドの terminal result と TUI の agent turn 完了を通知する際の重複排除、失敗時の非干渉、Codex CLI 設定境界を確認する入口。

## Read this when
- サブコマンドまたは TUI の Windows toast 通知を追加・変更するとき
- 通知対象の lifecycle event、terminal result の分類、turn ごとの重複排除を確認するとき
- Codex CLI callback の設定境界や未検証 interface の扱いを判断するとき
- WSL2 の通知 transport、自動補完プローブ、通知失敗時の扱いを確認するとき

## Do not read this when
- 通知仕様の確認を要しない具体的な realization 実装だけを調べるとき
- 通知と無関係な console/file log、割り込み、または一般的な Codex CLI 呼び出し仕様を確認するとき

## hash
- bcb50e63f23dac9adc42205d47ab494cdc9ac3ea18c5d44ff168296bc5749278
