# `cli_auto_completion.md`

## Summary
- `_CMOC_COMPLETE` が存在する呼び出しを自動補完用プローブとして扱う境界と、通常実行向け処理・副作用・出力を補完処理より前に行わない規則を定める。

## Read this when
- 自動補完プローブと通常の cmoc 実行を区別する条件を確認したいとき
- 自動補完時に許可される前処理、副作用、標準出力・標準エラー出力の範囲を確認したいとき
- Windows toast 通知に固有の自動補完境界の正本を確認したいとき

## Do not read this when
- 自動補完以外の通常実行フローや CLI 全体の仕様を確認したいとき
- Windows toast 通知の自動補完境界そのものを確認する場合で、正本資料を直接参照できるとき

## hash
- 19a87ab36b08cee626abd4da7ef2d29e708e381fa9990323519ee6f00db6cb96

# `codex_exec_rule.md`

## Summary
- cmoc から Codex CLI を呼び出す際の agent call と Codex call の区別、path context、CODEX_HOME、preflight validation、argv による設定上書き、sandbox と詳細な file access policy、書き込み責任分界、差分検証、model provider・model・reasoning effort、prompt literal の規則を定める app_spec の規約。関連する実装・個別 workload の責務は、本文中で委譲先として示される oracle doc/src を確認するための入口。

## Read this when
- Codex CLI の呼び出し引数、承認設定、sandbox、model/provider 設定、CODEX_HOME の扱いを実装・検証するとき。
- agent call の識別、call-scoped path context、work root/repo root の導出、prompt への placeholder 反映を確認するとき。
- file access mode に応じた直接ファイルアクセス制限、MCP・Structured Output・cmoc 管理処理との責任分界、または agent call 差分検証の境界を判断するとき。
- prompt literal の役割・制限や、個別 builder・path model・complete prompt などの委譲先をたどる必要があるとき。

## Do not read this when
- 特定の AgentCallParameter の正確な field 定義・型・既定値だけを確認したいときは、本文が委譲する oracle src を直接読む。
- 個別 agent call の意味上の責務や workload 固有の判断基準だけを確認したいときは、対応する oracle doc を直接読む。
- 実行 ID の表示、Windows toast 通知、model provider の正本規則、prompt 全体の統合条件など、本文が明示する別の正本を直接確認できる場合。

## hash
- 94ccf40217a4fbca2a1e9526ed4a16b67abfd0d7d4ac815484bed79cf90fe54b

# `codex_model_provider.md`

## Summary
- Codex の agent call 設定と provider 定義を定める正本仕様。call 種別ごとの model provider・Model・Reasoning Effort の直接指定、provider-local 設定、未知値の事前エラー、Codex CLI への委譲範囲を扱う。

## Read this when
- Codex provider の設定値、provider-local 設定、agent call 種別ごとの直接設定、または cmoc の責務境界を確認・変更するとき。
- Codex CLI に渡す設定の意味や、cmoc が provider の運用・認証・推論環境を保証しないことを確認するとき。

## Do not read this when
- 設定データ構造・field 名・型・既定値の正確な定義だけを確認したい場合は、指定された cmoc_config.py の定義を直接読む。
- agent call 設定を Codex CLI の argv へ反映する詳細だけを確認したい場合は、codex_exec_rule.md の該当節を直接読む。
- prompt、sandbox、file access policy、network access、通知設定の仕様だけを確認したい場合。

## hash
- 4d7551997d7651bcc8f39f51bdff5a2d533178146c6ba53bf4fcee2e0ee17c9a

# `console_and_file_log.md`

## Summary
- 非対話サブコマンドの console、primary report、サブコマンドログ、terminal result に関する共通契約を定義する正本仕様。
- 自然言語・実行 ID・時間・パスの表示形式、stdout/stderr の責務、進行通知、終端結果の分類・確定順序・表示内容を定める。
- primary report の保存条件と掲載内容、JSON Lines 形式のサブコマンドログ、診断記録、TUI 送信元情報の記録要件を定める。
- TUI・自動補完と非対話サブコマンドの通知境界、および本書が要求しない表示・機械可読化・個別仕様への非介入範囲を示す。
- コンソールやログの共通動作、report と terminal result の生成・表示順序、サブコマンドログの記録要件を確認する際の入口となる。

## Read this when
- 非対話サブコマンドの stdout、stderr、進行通知、実行 ID、経過時間、パス表示を確認・変更するとき。
- primary report の保存条件、共通掲載内容、terminal result の分類・表示順序・終了処理を確認するとき。
- サブコマンドログの保存先、JSON Lines 形式、flush、診断イベント、Codex call や TUI 送信元情報の記録要件を確認するとき。
- TUI や自動補完に対して、非対話サブコマンド用の report・terminal result・通知規則が適用される境界を確認するとき。

## Do not read this when
- 個別サブコマンド固有の result、completion_reason、primary report の本文形式・保存先・終了コードを確認する場合は、該当する個別サブコマンド仕様を直接読むとき。
- エラー分類や primary report 保存失敗時の扱いを詳細に確認する場合は、error_handling.md を直接読むとき。
- feedback observation の掲載対象・通知境界や detector event 契約を詳細に確認する場合は、feedback.md または feedback_observation.md を直接読むとき。
- Codex exec の出力取得方法や call 識別子、editor input handoff の境界を詳細に確認する場合は、codex_exec_rule.md または editor_input_handoff.md を直接読むとき。
- Windows toast、自動補完、または TUI 固有の通知仕様そのものを確認する場合は、windows_toast_notification.md または cli_auto_completion.md を直接読むとき。
- 実際の出力・ログ生成処理の実装を調べる場合は、この正本仕様ではなく対応する realization code を読むとき。

## hash
- cad7192b5d672a86bfdee8559ade0677c06c179f2d991ccc515b6f30aa660114

# `doctor_preprocess.md`

## Summary
- doctor preprocess は、cmoc の本命処理開始前にリポジトリ状態、管理対象ファイル、refactor state の追跡・schema・同期、feedback reporter/client の利用可能性と protocol 互換性を検証し、可能な範囲で修復する共通前処理。修復困難な状態では終了し、reporter の利用不能や protocol 不一致だけは degraded warning として本命処理を継続する。

## Read this when
- doctor preprocess の検証・修復手順、追跡保証、refactor state の同期条件を確認するとき
- feedback MCP reporter/client の事前検証や、reporter 障害時の degraded 扱いを確認するとき
- 本命処理の前に cmoc が保証すべきリポジトリ状態を調べるとき

## Do not read this when
- サブコマンド固有の事前条件や git working tree・staging area の clean 検査を確認したいとき
- feedback observation の MCP interface や collector protocol の正本仕様そのものを確認したいとき
- refactor state の詳細な JSON schema や entry 集合同期仕様を直接確認したいとき

## hash
- db70bf2db665438f032491cdd4dbfc50a5aa63492f5294662ee4b54bc53ffaa1

# `editor_input_handoff.md`

## Summary
- Codex TUI の prompt editor input に対する agent 間 handoff の正本仕様。active target の lifecycle、handoff ガイド、MCP の取得・上書き interface、本文生成、送信元情報、agent の責務と非目標を定める。
- handoff の共通仕様や入力 schema・本文構築の詳細は、prompt editor input、codex exec rule、console and file log、指定された oracle source/schema へ委譲する構成を示す。

## Read this when
- Codex TUI から別の prompt editor input へ依頼を handoff する機能の lifecycle、target 管理、受付条件、無効化順序を確認するとき。
- get_handoff_guide または overwrite MCP の責務、検証、入力・出力境界、上書き動作、失敗時の扱いを確認するとき。
- handoff ガイドに基づく agent の依頼作成手順、参照情報の渡し方、送信元情報の扱い、本文生成の責務分担を確認するとき。

## Do not read this when
- prompt editor input 全般の writer 境界や最終確定手順だけを確認したい場合は、prompt_editor_input.md を直接読む。
- editor input handoff MCP の実装上の起動経路・注入手順だけを確認したい場合は、codex_exec_rule.md の該当節を直接読む。
- handoff ガイドの正確な文面や完全 prompt skeleton を確認したい場合は、guide.py の build_editor_input_handoff_guide を直接読む。
- overwrite の入力 field、型、必須条件、参照指定形式を確認したい場合は、overwrite_input.json の root schema を直接読む。
- handoff 本文の見出し・順序・送信元情報の配置を確認したい場合は、body.py の build_editor_input_handoff_body を直接読む。

## hash
- fb07a839dea4888e9c5870fd3d874b710e0416846a61f331426c3d11b3e30f8f

# `error_handling.md`

## Summary
- handled failure と internal failure の分類基準、エラー終了時の state 確定・rollback・primary report 保存、terminal result とログの扱いを定める共通仕様。handled failure／internal failure の表示差異、スタックトレースの出力先、正常結果として扱う状態、および個別仕様との優先関係を確認する入口。

## Read this when
- エラー終了の種類を分類するとき。
- エラー時の state 確定、rollback、primary report、終了イベントの契約を確認するとき。
- handled failure と internal failure の console・stderr・サブコマンドログへの表示規則を確認するとき。
- エラーではなく正常系として扱う attention、incomplete、completed_with_unresolved、またはユーザー中断の扱いを確認するとき。
- 個別仕様に明記されていないエラー処理の共通規則を確認するとき。

## Do not read this when
- 特定サブコマンドが定める固有の state、rollback、report、次の操作、終了コードだけを確認したいときは、そのサブコマンドの個別仕様を直接読む。
- console と terminal result の出力先・表示順序・共通 field の正本を確認したいときは、console_and_file_log.md を直接読む。
- ユーザー中断の詳細契約だけを確認したいときは、subcommand_interruption.md を直接読む。

## hash
- e9fb772b9ff82c04863d89094041268f30ab642d5c643ef179b1dfae86f51a4e

# `feedback.md`

## Summary
- feedback subsystem 全体の目的、用語と remediation 結果分類、処理モデル、正本仕様の責務分担、既存 workload との境界、共通原則、non-goal を定義するアプリケーション仕様。
- feedback observation の収集・state 管理・`cmoc feedback report` の CLI 処理など、詳細仕様へ進むための上位ルーティング入口。

## Read this when
- feedback subsystem の目的や正常 publication・incomplete 診断の扱いを確認したいとき
- observation、issue identity、active issue、high-watermark、判定結果分類などの共通概念を確認したいとき
- feedback report の処理モデル、正本仕様の分担、既存 workload との境界を確認したいとき

## Do not read this when
- observation の報告基準・受け入れ検査・raw 保存の詳細を確認したいときは feedback_observation.md を直接読む
- repository-local state、checkpoint、publication、cleanup の詳細を確認したいときは feedback_state.md を直接読む
- `cmoc feedback report` の CLI 事前条件、agent call、commit、merge、表示、終了結果の詳細を確認したいときは sub_command/feedback_report.md を直接読む

## hash
- 892e1f5b1104895e5becf3c7c1665538fe9933a76bff6776ed054a913fa56603

# `feedback_observation.md`

## Summary
- agentによる問題報告の基準、cmoc_feedback MCP interface、受け入れ検査、collector/transportの境界、call終了処理、機械的なlog検出規則、raw observationの保存・durability・retentionを定める正本仕様。feedback observationの収集経路や保存契約を確認する入口。

## Read this when
- feedback observationを報告する条件や、仕様どおりの制約を問題として扱わない境界を確認するとき
- cmoc_feedback.submit_observationの入力・結果・互換処理・受け入れ検査を確認するとき
- collector、call-scoped capability、MCP transport、call終了時の保存順序を設計・検証するとき
- machine observationのallowlist rule、threshold、issue key、除外条件を確認するとき
- raw observationの保存単位、atomic durability、pending状態、cleanup条件を確認するとき

## Do not read this when
- 個別のprompt文面の実装を確認するだけの場合は、feedback_reporting.pyまたはcomplete_prompt.pyを直接読む
- reporter inputのJSON Schemaの詳細な型や制約だけを確認する場合は、reporter_input.jsonを直接読む
- 実装コードの具体的な挙動やテスト結果だけを調べる場合は、対応するsrcまたはtestを直接読む
- INDEX.mdの生成・更新方法そのものを確認する場合は、この仕様ではなくINDEX.md関連の規定を読む

## hash
- f979d5a735572c121079cebbe36caf1f971f9737a96ac5c3304b1773c446a358

# `feedback_state.md`

## Summary
- feedback remediation run が利用する repository-local state の正本仕様。active generation、current pointer、observation、run manifest、intake wave、checkpoint、report cut、publication、cleanup の責務・配置・不変性・排他制御・ライフサイクル整合を定める。

## Read this when
- feedback state の保存場所、artifact の役割、active issue や high-watermark の扱いを確認するとき
- feedback report の checkpoint、report cut、atomic publication、incomplete report、cleanup の仕様を確認するとき
- feedback remediation run の join・abandon と repository-local state の整合を確認するとき

## Do not read this when
- raw observation の収集規則や detector rule を確認したいときは feedback_observation.md を読む
- feedback report の呼び出し回数・wave loop・正常 publication 条件の詳細を確認したいときは feedback_report.md を読む
- high-watermark の用語・結果分類そのものを確認したいときは feedback.md を読む
- 編集 run の join・abandon 共通仕様を確認したいときは editing_run.md を直接読む

## hash
- 15675539d0880011b20f720a5f32b951638d1533ce430a41b7354429edd9f561

# `indexing.md`

## Summary
- cmocが生成・更新するINDEX.mdの配置対象、目次対象、記述要件、ハッシュ計算、生成処理、並列実行、実行条件を定める正本仕様。

## Read this when
- INDEX.mdの自動インデクシング仕様を確認するとき
- 目次情報の意味要件やハッシュ計算、生成順序・並列化の扱いを変更または実装するとき
- インデクシング実行条件や関連するサブコマンド仕様との関係を確認するとき

## Do not read this when
- 特定のサブコマンドの詳細な実行手順だけを確認したいときは、該当サブコマンド仕様を直接読む
- 個別ファイルの内容や既存INDEX.mdの現在状態だけを確認したいとき
- 目次情報の生成ロジックの具体的な実装詳細だけを確認したいときは、指定された実装ファイルを直接読む

## hash
- b1cfcd4f9e3ff2611b6ef03b3e96dde7c877d562bbc85c8593f4a6b8c40d21a8

# `oracle_and_realization.md`

## Summary
- oracle file と realization file の責務、分類、正本責務の委譲・優先関係、および両者の適合性判断基準を定義する共通仕様。

## Read this when
- oracle と realization の責務や分類を判断するとき。
- oracle doc・oracle src・realization file 間の正本性、委譲、優先関係を確認するとき。
- realization の実装・テスト・補助ファイルが仕様へ適合しているか調査するとき。

## Do not read this when
- oracle/realization の境界や適合性に関係しない作業を行うとき。
- この文書から委譲された正確な prompt 構築、literal、schema、または分類処理の実装詳細を直接確認するときは、指定された oracle src を読むとき。
- prompt literal 固有の役割や実行時指示の優先関係だけを確認するときは、codex_exec_rule.md を読むとき。

## hash
- 552c55553d18986570ed95fb3ae1dfcf2d0c0450668e3216ddc62ed048f11275

# `oracle_and_realization_file_enumeration.md`

## Summary
- 対象ファイルは、oracle／realization／uncategorised の分類条件と、対象ファイルを列挙するための扱いを定義する正本仕様である。
- ファイル分類や列挙結果の根拠を確認したいときに、app_spec 配下の他の仕様文書より先に参照する入口となる。

## Read this when
- リポジトリ内のファイルを oracle file・realization file・uncategorised file に分類する条件を確認するとき。
- oracle・realization の対象範囲や、Git ignore・ネストした Git repository・.git metadata の扱いを含む列挙判断を確認するとき。

## Do not read this when
- 個別の oracle／realization ファイルの内容や、分類後のファイルが担う機能仕様だけを確認したいとき。
- 分類規則ではなく、INDEX.md 自体の編集手順やルーティング形式を確認したいときは、対象の INDEX.md またはその編集規定を直接読むべきである。

## hash
- 40ce795ffadbf355d93ad8abfbab7fa6de085bd06013b48ee0ba597c9ec0224c

# `prompt_editor_input.md`

## Summary
- editor work file のライフサイクルと、オリジナルプロンプトを確定するまでの入力処理を定義する仕様。人間の直接入力と editor input handoff の双方を対象に、案内・ファイル分離・エディタ起動・検証・保存・削除の責務を扱う。

## Read this when
- editor work file の生成、エディタ起動、入力内容の検証・保存・削除の挙動を確認するとき。
- 人間入力または editor input handoff からオリジナルプロンプトを確定する処理の仕様を確認するとき。
- console 案内や handoff、完全 prompt 構築の正本がどの文書・builder に委譲されるかを確認するとき。

## Do not read this when
- editor input handoff 自体の target lifecycle、ガイド生成・保持・取得、MCP interface の詳細だけを確認したいときは editor_input_handoff.md を読む。
- 完全 prompt や prompt skeleton のサブコマンド固有の構築を確認したいときは、該当するサブコマンド仕様または builder の正本を直接読む。
- 出力先や stderr、TUI と自動補完の境界だけを確認したいときは console_and_file_log.md を読む。

## hash
- 4c1360bd05c1e4ada0948670e2460c773767b48e607139d7090d46c9a9197763

# `run_isolation.md`

## Summary
- run を fork から join または abandon まで隔離して扱う lifecycle、branch・worktree、agent call の path context、cmoc 管理データと feedback state の責任境界を定めるアプリ仕様。

## Read this when
- run の開始・終了条件や、サブコマンド呼び出しとの関係を確認するとき。
- run の branch、commit、worktree、agent call の cwd・path context を確認するとき。
- run 中のファイルアクセス境界、cmoc が管理するログ・session state・feedback state、join・abandon との責任分界を確認するとき。

## Do not read this when
- 永続化される run field の具体的なスキーマを確認したいときは session_state.md を読むべき場合。
- branch や worktree の命名・分岐元 commit の正本を確認したいときは branch_model.md を読むべき場合。
- agent call の詳細な実行規則やアクセス制限を直接確認したいときは codex_exec_rule.md を読むべき場合。
- ログ、feedback observation、feedback state など個別の保存形式や lifecycle の詳細だけを確認したいときは、それぞれの専門仕様を直接読むべき場合。

## hash
- 8361c9fb69ca4127a5e51a3ad71c61c01fbf8043e4a7b540784d7b22e810224f

# `session_state.md`

## Summary
- cmoc workflow における session と編集 run の永続状態を定義する正本仕様。JSON の各フィールド、状態値、開始・終了時の共通事前条件、feedback state との責務分離、状態遷移を扱う。
- session/run の状態管理、join・abandon・自動 join、error recovery、apply の追従対象を確認する際の基準となる。

## Read this when
- session または編集 run の状態、ライフサイクル、永続化項目を確認するとき。
- workload の開始、join、abandon、session 終了に必要な branch・state・未コミット差分の事前条件を確認するとき。
- feedback report の自動 join・recovery と session state の責務分離、または apply の追従対象 commit を確認するとき。

## Do not read this when
- feedback の repository-local state 自体の保存対象や lifecycle を確認したいときは、feedback_state.md を直接読む。
- apply の join 後 hook や commit 更新条件の詳細を確認したいときは、realization_apply.md を直接読む。
- oracle edit の仕様や個別 workload の処理内容だけを確認したいときは、この状態モデルではなく対応するサブコマンド仕様を直接読む。

## hash
- ec7c9d9c8103ab3c0fef8ca67c374ba50a73e27996ff987a61d26a26e64020ac

# `sub_command`

## Summary
- cmoc のサブコマンド仕様をまとめた入口で、doctor、indexing、TUI、oracle 編集・調査、realization の apply/refactor、feedback report、session の fork/join/abandon、および編集 run の共通 lifecycle を扱う。
- 個別サブコマンドの引数、事前条件、実行手順、状態遷移、report、cleanup、agent call 境界を確認したい場合に、配下の対応する仕様書へ進むための階層である。
- 複数の編集 workload に共通する run の隔離、同時実行制約、join/abandon、差分検査、merge、post-join、report 規則は editing_run.md が入口となる。

## Read this when
- cmoc のサブコマンド仕様を横断的に確認したいとき。
- 対象コマンドの個別仕様書がどれかを判断したいとき。
- 編集 run の開始・終了、join、abandon、差分検査など共通 lifecycle を確認したいとき。
- session lifecycle、feedback remediation、realization 操作、oracle 操作、または TUI の仕様を確認したいとき。

## Do not read this when
- 特定のコマンドの詳細挙動が明確で、その個別仕様書を直接読めるとき。
- doctor preprocess、indexing、branch model、session state、feedback state など、サブコマンドから参照される共通正本そのものを確認したいとき。
- 実装コードの prompt 構築や agent 起動パラメータの詳細だけを確認したいとき。

## hash
- 5299f6f5544a68cc77ff0076ffd9e4feaa4e167456146328150c17eed47009b4

# `subcommand_interruption.md`

## Summary
- 中断可能なサブコマンド、Ctrl+C によるユーザー中断の扱い、共通の完了処理と正常系としての結果、ならびに中断後の個別仕様へのルーティングを定める仕様。

## Read this when
- `cmoc realization refactor fork` または `cmoc feedback report` の実行中断時の挙動を確認したいとき。
- Ctrl+C を受け付けるサブコマンドの範囲、新規処理や Codex CLI 呼び出しの停止、確定済み部分結果の保存・報告方法を確認したいとき。
- 中断後の refactor run や feedback report の扱いを、個別仕様へ進む前に確認したいとき。

## Do not read this when
- 中断後の refactor run の state や次の操作の詳細を確認したい場合は、realization_refactor.md を直接読むべきとき。
- feedback report の issue 処理単位、run state、publication、observation retention の詳細を確認したい場合は、feedback_report.md を直接読むべきとき。
- 一般的なログ出力、エラーハンドリング、Windows toast 通知の詳細だけを確認したいときは、それぞれの個別仕様を直接読むべきとき。

## hash
- 94528cdef2a9e0e7e08890fa8a816581222faa3575e00c31ad52904df9f10f4d

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
- cmoc の導入、初回 doctor 実行、session fork から session join までの基本 workflow と、oracle 編集・realization 追従・feedback 報告の使い分けを定義する利用手順。

## Read this when
- cmoc の初回セットアップや呼び出し方法を確認するとき
- 仕様変更から realization apply/refactor、feedback report、session join までの標準 workflow を確認するとき
- 各 workload の目的に応じて、どのサブコマンドを使うか判断するとき

## Do not read this when
- realization apply や realization refactor の詳細な処理規則、agent call、state 管理を確認したいときは各 workload の仕様を直接読む場合
- oracle edit、feedback report、editing run の個別仕様だけを確認したいときは対応するサブコマンド仕様を直接読む場合
- session や run の永続 state、隔離、join/abandon の共通規則を詳細に確認したいときは session_state、run_isolation、editing_run を直接読む場合

## hash
- c06672e712eb081c4728b10871c4e87e305670133f2cd6621cdddc1eb678d8ad

# `windows_toast_notification.md`

## Summary
- 対象は、WSL2 上の cmoc が非対話サブコマンドの terminal result と TUI の agent turn 完了を Windows toast で通知する仕様を定める。通知境界、状態分類、通知内容、Codex CLI 設定境界、未検証外部契約、Windows transport の制約、自動補完時の扱いを確認する入口である。

## Read this when
- Windows toast 通知の発火条件、非対話サブコマンドと TUI の通知境界、通知状態や必須内容を実装・レビューするとき。
- Codex CLI の callback 契約を検証するとき、または通知 transport の安全性・独立性・失敗時の非干渉を確認するとき。
- 自動補完プローブで通知を抑止する条件や、通知対象外の内部処理を確認するとき。

## Do not read this when
- Windows toast 通知の具体的なコンソールログ分類や primary report の確定順序だけを確認する場合は、参照先の console_and_file_log 仕様を直接読む。
- ユーザー中断の成立条件や完了処理だけを確認する場合は、subcommand_interruption 仕様を直接読む。
- Windows 11・WSL2 の基本環境だけを確認する場合は、development_environment 仕様を直接読む。

## hash
- f2e4656a7af56decf9e282a1f5f146f44255c7dfc15c4bfef7808e8af0a755ac
