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
- Codex CLI 呼び出しにおける agent call と個別 Codex call の識別、call-scoped path context、環境変数、preflight、argv による設定上書き、sandbox と詳細な file access policy、書き込み責任分界、model/provider 設定、prompt 構築規則を定める正本仕様。
- Codex CLI の起動規則や agent-facing prompt の設計を確認する際の上位エントリであり、個別フィールドの型や導出アルゴリズムは本文から委譲先の oracle src・oracle doc へ進む。

## Read this when
- cmoc が Codex CLI を起動する引数、環境、sandbox、承認設定、provider・model・reasoning effort を確認または変更するとき。
- agent call の cwd、worktree/repository root、file access mode、prompt literal、Structured Output 補正や retry の扱いを確認するとき。
- Codex CLI 呼び出しに関する仕様の責務分界や、委譲先の正本を特定するとき。

## Do not read this when
- AgentCallParameter の正確な field 定義・型・既定値だけを確認したい場合は、直接 `basic.py` の定義を読むとき。
- path context の導出、placeholder の受け渡し、prompt 統合、file access policy の正確な文面だけを調査する場合は、本文が指定する対応する oracle src を直接読むとき。
- 個別の model provider 設定値や `oracle edit` の確定時点だけを調べる場合は、本文が参照する専門の oracle doc を直接読むとき。

## hash
- 166a4ba2c8ecb7baddc6866094143b762e38b91ea70e096cc83b097741757c81

# `codex_model_provider.md`

## Summary
- 通常の agent call における model provider、Model、Reasoning Effort の直接設定と、設定不足・CLI拒否時の扱いを定める仕様。
- 一時障害の回復確認 probe だけに適用される設定継承例外と、quota待機から切り替わる場合の確認条件を定める。
- provider ID と provider-local 設定の定義、Codex CLIへ委譲する責務、および cmoc が担わない provider 運用範囲を定める。

## Read this when
- agent call 種別ごとの Codex 設定取得、直接文字列の扱い、設定欠如時のエラー条件を確認するとき。
- 一時障害の回復確認 probe がどの設定を使うべきか、通常の quota availability probe とどう区別するかを確認するとき。
- provider ID、provider-local 設定、組み込み openai provider、secret 保存禁止の扱いを確認するとき。
- cmoc が provider の起動・診断・修復・疎通確認などを担当するか判断するとき。

## Do not read this when
- Codex CLI の argv 反映、実行失敗時の処理、回復待ちと再開の詳細を確認したいときは、先に codex_exec_rule.md を読む。
- CodexCallConfig、CodexModelProviderConfig、CmocConfigCodex の正確な field 名・型・既定値を確認したいときは、指定された cmoc_config.py を直接読む。
- prompt、sandbox、file access policy、network access、通知設定の仕様を確認したいときは、この文書ではなく各設定の正本を読む。

## hash
- d81b0aff42367a14e32d9a0367ee01f90d59cdee6e69a70e4521ca2e96eede62

# `console_and_file_log.md`

## Summary
- 非対話サブコマンドに共通する console、primary report、terminal result、サブコマンドログの正本契約を定める。自然言語・時間・パスの表示形式、stdout/stderr の責務、終端結果の分類と確定順序、report の掲載内容、JSON Lines 診断記録、TUI・自動補完との境界を確認するための入口である。

## Read this when
- 非対話サブコマンドの console 出力、primary report、terminal result、終了コード、実行時間、パス表示を実装・変更・レビューするとき。
- サブコマンドログの保存先、イベント記録、flush、Codex call や回復待ちの診断情報を確認するとき。
- cmoc tui、cmoc oracle investigation、cmoc oracle edit、または自動補完に対する通知・report の適用境界を確認するとき。

## Do not read this when
- 個別サブコマンド固有の result、completion_reason、primary report 本文、保存先、終了コードを確認する場合は、先にそのサブコマンド仕様を読むべきとき。
- エラー終了の確定、feedback observation の保持・通知、Windows toast、自動補完、editor input handoff の詳細な正本契約だけを確認したいときは、本文が参照する各専門仕様へ直接進むべきである。
- ANSI 表示、verbosity/debug option、機械可読 stdout JSON schema など、本書が non-goal として要求していない機能を検討するとき。

## hash
- 2acec05eba06fdd4282bd97a3fdee737825b3da2c1382fc370608cfdf4e9bd8a

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
- Codex TUI の agent から、別の prompt editor input で待機中の active target へ依頼を引き渡す共通機能の正本仕様。handoff ガイドの取得、項目別入力による editor input file 全体の上書き、target lifecycle、送信元情報、本文・参照の構築責務、失敗時の扱い、および non-goal を定める。

## Read this when
- prompt editor input への handoff 機能の lifecycle、MCP interface、target 検証、上書き処理、本文生成、送信元情報、または agent の handoff 手順を確認したいとき。
- handoff ガイド、入力 schema、本文 builder、参照情報などの責務分担を確認し、対応する委譲先の正本へ進む入口を探すとき.

## Do not read this when
- prompt editor input の writer 境界や最終確定手順だけを確認したいときは、prompt_editor_input.md を直接読む。
- Codex TUI への MCP 注入や file access 制限の共通仕様だけを確認したいときは、codex_exec_rule.md を直接読む。
- 送信元情報の記録・保存ログの仕様だけを確認したいときは、console_and_file_log.md を直接読む。
- 正確なガイド文面、instruction 文面、入力・結果 schema、本文 builder、または DocRef の実装・形式を確認したいときは、本書の委譲先ファイルを直接読む。

## hash
- c0d22c3cc3b64aca8c9157466c57f080cbdf7a05ff0546d19abbcaaad43d0e3a

# `error_handling.md`

## Summary
- handled failure と internal failure の分類基準、エラー終了時の state 確定・rollback・primary report 保存、terminal result とログ・コンソールへの表示契約を定める共通エラーハンドリング仕様。

## Read this when
- エラー終了の原因を handled failure と internal failure のどちらに分類するか判断するとき。
- エラー時の state 確定、rollback、primary report 保存、終了イベントの順序や失敗時の扱いを確認するとき。
- エラー terminal result、stdout・stderr、サブコマンドログに表示・保存すべき内容やスタックトレースの扱いを確認するとき。
- attention、incomplete、completed_with_unresolved、ユーザー中断要求をエラー扱いしない条件を確認するとき。
- 個別仕様にエラー時の指定がない事項へ適用する共通規則を確認するとき。

## Do not read this when
- console と terminal result の出力先・表示順序・共通 field だけを確認したい場合は、参照先の console_and_file_log.md を直接読む。
- codex exec の回復待ち可否や終了条件だけを確認したい場合は、codex_exec_rule.md を直接読む。
- ユーザー中断要求の詳細な正常系処理だけを確認したい場合は、subcommand_interruption.md を直接読む。
- 特定サブコマンド固有の state、rollback、report、次の操作、終了コードを確認したい場合は、そのサブコマンドの個別仕様を直接読む。

## hash
- 5be1589b159f55673b8aa806bb251dcb24129c629488bd9099703f3cc60ddb8b

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
- feedback remediation run が利用する repository-local state の正本仕様で、active generation、current pointer、run manifest、intake wave、checkpoint、report cut、publication completion record の責務と保持範囲を定める。
- feedback state の配置、canonical JSON と排他制御、high-watermark、正常・中断時の publication、incomplete report、cleanup、および run lifecycle との整合を扱う。

## Read this when
- feedback state の artifact 構成、保持対象、所有範囲、または保存・排他制御の規則を確認したいとき。
- feedback remediation の wave、high-watermark、checkpoint、report cut、atomic publication、incomplete、cleanup の扱いを確認したいとき。
- current pointer が選ぶ正常 publication や、失敗・中断後に保持すべき recovery state の境界を判断したいとき。

## Do not read this when
- raw observation の収集や detector rule の正本を確認したいときは、feedback observation の仕様を直接読む。
- cmoc feedback report の呼び出し回数、wave loop、incomplete 条件など subcommand 固有の手順を確認したいときは、feedback_report の仕様を直接読む。
- 編集 run の join・abandon 共通仕様だけを確認したいときは、editing_run の仕様を直接読む。

## hash
- 468afed690bdbf9a62b19435e6cff957892fc6e24ac6791dc9966bbacb6d3d59

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
- オリジナルプロンプトを受け取る editor input file のライフサイクル、編集待機中から確定保存までの責務、エディタ起動条件、入力検証・固定・strip処理、および既存データの扱いを定める正本仕様。
- editor input handoff の詳細や失敗時の責務、完全 prompt の構築、console出力境界、agent のファイルアクセス責任は、本文中で参照される別仕様へ委譲している。

## Read this when
- editor input file の作成・編集・保存・再利用・削除方針を確認するとき。
- エディタ選択、codeの--wait、入力ファイルの安全な検証、最終読み取り結果の固定、オリジナルプロンプト抽出の挙動を変更または調査するとき。
- 確定保存失敗時に入力を保持する要件や、既存の保存ログ・旧復旧ファイルの扱いを確認するとき。

## Do not read this when
- editor input handoff のtarget lifecycle、handoffガイド、MCP interface自体を確認したいときは、参照先のeditor_input_handoff仕様を直接読む。
- 完全promptやprompt skeletonの構築内容を確認したいときは、対象サブコマンドのprompt構築仕様または対応するbuilderを直接読む。
- console出力先やTUIと自動補完の境界だけを確認したいときは、console_and_file_log仕様を直接読む。
- agentによるファイルアクセス制限や書き込み主体の責任分界だけを確認したいときは、codex_exec_rule仕様を直接読む。

## hash
- 810c41249f4b7af561b6803c4d6e4adb9eecf965a26581136435c36ac3161a61

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
- cmoc のサブコマンド仕様群の入口。doctor・indexing、session の fork/join/abandon、editing run 共通 lifecycle、oracle の edit/investigation、realization の apply/refactor、feedback report、TUI の責務と実行・終了・レポート規則を扱う。
- セッションや編集 run のライフサイクル、agent call を伴う編集・調査、feedback の intake/remediation/publication、ならびに各コマンドの事前条件・差分境界・状態遷移・cleanup を確認するための下位仕様へのルーティング単位。

## Read this when
- cmoc のサブコマンド全体の仕様構成や、対象コマンドの詳細仕様へ進む入口を確認したいとき。
- session lifecycle、editing run、oracle/realization 操作、feedback report、または TUI の実行条件・終了処理を調べるとき。
- 複数のサブコマンドにまたがる状態遷移、agent call、report、merge・cleanup の責務分担を確認するとき。

## Do not read this when
- 特定コマンドの引数や実行手順だけを確認したい場合は、そのコマンド名に対応する個別仕様を直接読む。
- 編集 run の複数 workload に共通する lifecycle だけを確認したい場合は、editing_run.md を直接読む。
- doctor preprocess や indexing の共通仕様、branch model、session state、feedback state など、別ディレクトリにある参照仕様の詳細確認が目的の場合は、それらの正本を直接読む。

## hash
- 621a80ce5ebb3bdd1463fd95f277509491154a727c6d73bd364f1bf5d9c7b777

# `subcommand_interruption.md`

## Summary
- 中断可能な2つのサブコマンド（`realization refactor fork` と `feedback report`）における Ctrl+C の扱いと、確定済み部分結果を保った正常完了の共通規則を定める。
- 中断要求の受付、不可分な finalization 区間、quota・障害待機中の優先順位、state 更新・primary report 保存・terminal result 出力までの完了手順を扱う。
- 中断後の各サブコマンド固有の state や次の操作は、対応する個別仕様へ案内する上位仕様である。

## Read this when
- `cmoc realization refactor fork` または `cmoc feedback report` の Ctrl+C 中断動作を実装・レビューするとき。
- 中断時に新規処理を止める条件、実行中処理の完了または rollback、finalization の境界を確認するとき。
- 中断後も部分結果を保持して primary report と `user_interruption` terminal result を保存・出力する流れを確認するとき。
- 中断後の個別 state や次の操作を調べる前に、共通規則と対応する個別仕様への入口を確認するとき。

## Do not read this when
- 中断を伴わない通常のサブコマンド実行仕様だけを確認するとき。
- `realization refactor fork` の中断後 state・次の操作だけを確認する場合は、対応する realization refactor 個別仕様を直接読むとき。
- `feedback report` の issue 処理単位・run state・publication・observation retention だけを確認する場合は、対応する feedback report 個別仕様を直接読むとき。
- コンソールやファイルへの一般的な出力規則、エラー処理、Windows toast の詳細だけを確認する場合は、それぞれの個別正本仕様を直接読むとき。

## hash
- f6c9b45edee50bd7faee4fded3f9410f6eeae81c61ab9e7d92b017786b1d8699

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
- Windows 11 の WSL2 環境で、非対話サブコマンドの terminal result と TUI の agent turn 完了を Windows toast で通知する境界・通知内容・発火決定性・Codex CLI callback 契約検証・安全な transport 制約を定める正本仕様。

## Read this when
- Windows toast 通知の対象範囲、通知タイミング、terminal result の分類、TUI の turn 完了通知を確認・変更するとき
- Codex CLI の callback 設定や event 契約を検証し、通知を cmoc の lifecycle event と結び付けるとき
- 通知 transport の依存関係、安全なデータ受け渡し、有限時間、失敗時の非干渉、自動補完時の抑制条件を確認するとき

## Do not read this when
- console/file log における primary report や terminal result の確定規則そのものを確認したいときは console_and_file_log.md を直接読む
- ユーザー中断の成立条件や完了処理を確認したいときは subcommand_interruption.md を直接読む
- 具体的な実装コード、テスト、または Codex CLI の実測結果だけを確認したいときは対応する realization・検証資料を直接読む

## hash
- cbe3d0bba1c661dc1b92c4d2876fb72fb85f82ed0fc122eae2badefd5d798d98
