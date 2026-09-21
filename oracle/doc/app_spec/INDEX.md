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
- Codex CLI 呼び出しにおける agent call と Codex call の区別、path context、環境・引数・sandbox・ファイルアクセス制限、model provider、prompt の責務分界を定める正本仕様。
- Codex 呼び出し規約や prompt 構築規則の実装・テストが、この仕様のどの責務と整合すべきか確認するための上位ガイド。

## Read this when
- Codex CLI の起動引数、sandbox、CODEX_HOME、provider/model/reasoning 設定、agent call の path context を確認・変更するとき。
- agent-facing prompt の内容や責務分界、ファイルアクセス制限、差分検証の扱いを確認するとき。

## Do not read this when
- AgentCallParameter の正確な field・型・既定値を確認したい場合は、委譲先の oracle src を直接読むとき。
- 個別 agent call の意味上の責務や実行 ID、Windows toast など、本文が明示する別の正本仕様の詳細を確認したいとき。

## hash
- 3214fff618b8fe21e6ed58525fc83bb0d3f8461222b1a9e90c2fde6cfdf838ec

# `codex_model_provider.md`

## Summary
- 各 agent call 種別に対する model provider、Model、Reasoning Effort の直接設定と、Codex CLI への反映境界を定義する仕様
- model provider ID と provider-local 設定の対応、未知の値を拒否する条件、secret を保存しない制約を定義する仕様
- provider の取得・運用や prompt など周辺設定の変更を cmoc の責務外とする境界を示す仕様

## Read this when
- agent call 種別ごとの Codex CLI 設定値の決定方法や、未設定時のエラー条件を確認するとき
- model provider ID と provider-local 設定の扱い、openai の位置づけ、Codex CLI への受け渡し範囲を確認するとき
- cmoc が model provider の運用や認証・品質を保証するか、周辺設定を変更するかの責務境界を確認するとき

## Do not read this when
- 設定データ構造、field 名、型、既定値の正確な定義を確認したいときは、指定された cmoc_config.py の正本を直接読む
- agent call 種別から Codex CLI argv へ反映する詳細規則を確認したいときは、指定された codex_exec_rule.md を直接読む
- prompt、sandbox、file access policy、network access、通知設定そのものの仕様を確認するとき

## hash
- 3b681b9e313608c1e20cb6717b353d3824a45567359a13d8d660a4ccfa08fb60

# `console_and_file_log.md`

## Summary
- 非対話サブコマンドの console、primary report、terminal result、サブコマンドログに関する共通契約を定める正本仕様。
- stdout/stderr の責務、実行 ID・時間・パスの表示形式、進行通知、終端結果の確定順序と表示内容を規定する。
- primary report の保存要件と共通掲載内容、JSON Lines 形式の診断ログ、TUI 送信元情報の記録、および TUI・自動補完との適用境界を扱う。
- 個別サブコマンドの固有結果や report 形式を定義する文書ではなく、それらが従う共通出力・記録契約への入口となる。

## Read this when
- 非対話サブコマンドの stdout、stderr、進行通知、terminal result の表示責務を確認するとき
- primary report の保存タイミング、掲載内容、失敗時の扱いを確認するとき
- サブコマンドログの保存先、JSON Lines 形式、即時 flush、診断イベント要件を確認するとき
- TUI または自動補完に対して通常の非対話出力規則がどこまで適用されるか確認するとき

## Do not read this when
- 個別サブコマンド固有の result、completion_reason、report 形式、終了コードを確認したいとき
- エラー分類やエラー終了の詳細だけを確認したいときは、参照先として示される error_handling.md を直接読むとき
- Codex call の取得方法や editor input handoff の詳細実装だけを確認したいとき
- Windows toast 通知や CLI 自動補完の固有規則だけを確認したいとき

## hash
- e89f1806e68437080923d100852d932d1d38d8fd55904f0d1845c20478c9a55d

# `doctor_preprocess.md`

## Summary
- cmoc の本命処理開始前に共通の検証・修復を行い、実行可能性を保証する前処理仕様。
- git 管理状態、refactor state の同期、feedback reporter/client の protocol 互換性を確認し、必要な修復と commit を定める。

## Read this when
- doctor preprocess の検証・修復手順や、本命処理前に保証されるリポジトリ状態を確認したいとき。
- feedback reporter/client の事前検証、利用不能時の degraded warning の扱いを確認したいとき。

## Do not read this when
- サブコマンド固有の事前条件や clean working tree の検査方法を確認したいとき。
- feedback observation の MCP interface や collector/transport の正本仕様そのものを確認したいとき。

## hash
- aca81bd5586cea39a31d66a223059cbf90347a61482ced981f58586bbc684de6

# `editor_input_handoff.md`

## Summary
- Codex TUI の agent から、待機中の prompt editor input へ依頼を引き渡す共通機能の正本仕様。active target の lifecycle、handoff ガイド取得、MCP 上書き、本文生成、送信元情報、agent の責務、参照情報、非目標を定める。
- 入力 schema・本文 builder・送信元情報モデルなどへ責務を委譲し、この文書では handoff 全体の境界と連携関係を確認するための入口となる。

## Read this when
- prompt editor input に対する agent からの handoff の lifecycle や active target の受付条件を確認するとき。
- handoff ガイドの取得から項目別入力の overwrite、本文生成、送信元情報の注入までの責務分担を確認するとき。
- handoff MCP の agent 責務、失敗時の扱い、sandbox や file access mode を変更しない制約を確認するとき。
- handoff 機能の非目標や、現在編集中の本文・editor lock・自動保存を扱わない境界を確認するとき。

## Do not read this when
- 正確な MCP 入力項目・型・受理条件や tool result の JSON 形式だけを確認したいときは、対応する input/result schema を直接読む。
- handoff ガイドの固定文面や完全 prompt skeleton の構築を確認したいときは、指定された guide builder または prompt editor input の正本を直接読む。
- handoff 本文の見出し・順序・送信元情報のデータ構造を確認したいときは、本文 builder と source model を直接読む。
- prompt editor input 全般の writer 境界や最終確定手順だけを確認したいときは、prompt editor input の正本を直接読む。

## hash
- 411ffe83f814bcbeea020fe26fcd43025956aeed6cfd877592d23ca31387b705

# `error_handling.md`

## Summary
- handled failure と internal failure の分類、エラー終了時の state 確定・rollback・primary report 保存、terminal result と終了イベントの確定、および report 保存失敗時の扱いを定める共通エラー処理規則。
- handled failure と internal failure の表示要件、スタックトレースの保存・表示先、診断用サブコマンドログ、次の操作や終了コードの提示方法を確認するための正本仕様。
- attention・incomplete・completed_with_unresolved やユーザー中断をエラー扱いしない境界と、個別仕様が優先される事項を示すエラー処理仕様への入口。

## Read this when
- エラー終了の分類、終了処理、rollback、primary report、terminal result、終了コードの共通契約を確認するとき
- handled failure と internal failure の表示差異、スタックトレースの扱い、診断ログの要件を確認するとき
- 個別仕様にエラー時の扱いが明記されていない事項の共通ルールを確認するとき

## Do not read this when
- 特定サブコマンド固有の state、rollback、report、次の操作、終了コードの仕様を確認する場合は、そのサブコマンドの個別仕様を直接読むとき
- console と terminal result の出力先・表示順序・共通 field の詳細を確認する場合は、console_and_file_log.md を直接読むとき
- ユーザー中断の正常系処理を確認する場合は、subcommand_interruption.md を直接読むとき

## hash
- 77294bee6f95b6cb11b5f2e8997b8d47f30559904036fc3a8b08038b77571222

# `feedback.md`

## Summary
- feedback subsystem 全体の目的、用語と結果分類、remediation の処理モデル、責務を分担する正本仕様、既存 workload との境界、および non-goal を定義する上位仕様。

## Read this when
- feedback observation の収集基準や raw 保存の詳細を除き、feedback subsystem 全体の責務・結果分類・処理境界を確認するとき。
- feedback state や `cmoc feedback report` の詳細仕様へ進む前に、どの正本が各責務を担うかを判断するとき。
- 自動修正、human_required、inconclusive、publication、既存 workload との境界など、feedback 全体の原則を確認するとき.

## Do not read this when
- observation の報告基準、受け入れ検査、収集経路、機械 detector、raw 保存を直接確認したいときは feedback_observation の仕様へ進むとき。
- repository-local state、intake wave、high-watermark、checkpoint、publication、cleanup の詳細を確認したいときは feedback_state の仕様へ進むとき。
- `cmoc feedback report` の CLI 条件、agent call、commit、merge、表示、終了結果の詳細を確認したいときは feedback_report の仕様へ直接進むとき。

## hash
- 6f953ed0fb794d6aff7bd7b4ab8bdb96a65d4d3c077ef6931cf2cb09b8623dac

# `feedback_observation.md`

## Summary
- agent による observation 報告の基準、MCP reporter の入出力と受け入れ検査、collector・transport の境界、機械的検出ルール、raw observation の保存・保持・cleanup を定める feedback 収集仕様の正本。

## Read this when
- feedback observation を報告する条件や、reporter の失敗時に本命 workload をどう扱うか確認するとき
- feedback reporter、collector、detector、raw 保存の挙動を実装・変更・検証するとき
- observation の schema version、受け入れ制限、検出 threshold、保存 durability を確認するとき

## Do not read this when
- agent 向け prompt の正確な生成文面だけを確認したいときは、指定された prompt builder の正本実装を直接読む
- reporter の具体的な input schema の項目定義だけを確認したいときは、参照先の schema ファイルを直接読む
- feedback 以外の cmoc 機能の仕様や一般的なファイルアクセス規定を確認したいとき

## hash
- d9d990a2015c09232c0f65a5ce9a2d01108ae6da8cc187e359058c645be822f7

# `feedback_state.md`

## Summary
- feedback remediation が使う repository-local state の正本。active generation、current pointer、run manifest、immutable な intake wave、high-watermark、checkpoint、report cut、publication completion、incomplete report、atomic publication、cleanup の責務と整合条件を定める。

## Read this when
- feedback state の保存場所、artifact の役割、JSON canonicalization、排他制御、active issue と machine aggregate の保持条件を確認するとき
- feedback report の wave 処理、checkpoint、report cut、正常 publication、incomplete 処理、cleanup、または run join・abandon との整合を実装・検証するとき
- current pointer、high-watermark、immutable artifact、再開・失敗復旧の扱いを判断するとき

## Do not read this when
- raw observation の収集や detector rule 自体の正本仕様を確認するときは feedback_observation.md を読む
- feedback report の call 回数・wave loop・正常 publication・incomplete の詳細な実行手順だけを確認するときは feedback_report.md を読む
- feedback の用語・結果分類や処理モデルだけを確認するときは feedback.md を読む
- 編集 run の join・abandon 共通仕様だけを確認するときは editing_run.md を読む

## hash
- 75de4ba04b1ddee142a3516c4615569c41916c4614d59252bb4a0918dee52f99

# `indexing.md`

## Summary
- `INDEX.md` の配置・目次対象・フォーマット・意味要件と、本文との不一致時の優先規則を定める正本仕様。
- インデクシングの対象列挙、深い階層からの処理、生成 agent call、並列化、ハッシュ検証、自動コミット、および実行条件を規定する。

## Read this when
- `INDEX.md` の生成・更新・検証の仕様を確認するとき
- 目次エントリーの意味要件、対象範囲、ハッシュ計算、処理順序や並列化の扱いを判断するとき
- インデクシングを呼び出す実装や関連する正本仕様との整合性を確認するとき

## Do not read this when
- 個別ファイルの実装やテストの内容だけを確認したいとき
- 特定のサブコマンド固有の実行順序や手順を確認する場合で、参照先のサブコマンド仕様を直接読めるとき
- 既存の `INDEX.md` の記載だけを確認したいとき

## hash
- c139a3e90adaad0680365d76716c69838fb85bf28016992e4963a42abad7d02e

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
- `prompt_editor_input.md` は、プロンプト編集用の editor work file のライフサイクルと、入力確定後の保存・抽出・削除手順を定義する正本ドキュメントです。
- 人間による直接編集と editor input handoff の双方を対象に、案内文・handoff・prompt 構築など関連仕様への責務委譲も示します。

## Read this when
- editor work file の生成、編集、検証、最終読み取り、保存コピー作成、オリジナルプロンプト抽出、確定後の削除や失敗時の保持を確認するとき。
- プロンプト編集入力に関するエディタ起動条件、入力主体の責任分界、handoff との連携を確認するとき。

## Do not read this when
- 完全な prompt skeleton や完全 prompt の構築内容そのものを確認したいとき。
- editor input handoff の詳細な target lifecycle や MCP interface を確認したいとき。
- console 出力先や TUI 境界など、本文書が参照先へ委譲している個別仕様を直接確認したいとき。

## hash
- c1e425abded344e04fc33795e8001d1915b3d02749fe24d65e5f66d9245c21f6

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
- cmoc のサブコマンド別正本仕様をまとめた入口。doctor・indexing・tui、oracle の編集／調査、session の fork／join／abandon、realization の apply／refactor、feedback report、および編集 run 共通 lifecycle の責務と実行契約を扱う。
- 特定サブコマンドの引数、事前条件、実行手順、状態遷移、agent call、差分処理、report、cleanup を確認する際の下位仕様への入口。複数の編集 workload に共通する run の開始・終了・排他規則を確認する場合は、共通 lifecycle 仕様から読み始める。

## Read this when
- cmoc のサブコマンドが担う処理と、同階層のどの仕様を読むべきかを判断するとき。
- 特定のサブコマンドの CLI 契約、実行前提、状態更新、エラー処理、report または cleanup を確認するとき。
- realization apply／refactor や feedback report に共通する編集 run の lifecycle を確認するとき。

## Do not read this when
- サブコマンド共通の実装規則、session state、branch model、agent call の詳細など、本文が参照する専門仕様だけを確認したいとき。
- 特定サブコマンドの詳細が明確で、そのサブコマンド固有の仕様を直接読めるとき。
- 実装コードやテストの実際の挙動を確認したいとき。

## hash
- 4ce68fdb44334ffb8cba843caf0f83e2a628fe31b1fbabfa02d497f4a1b337f6

# `subcommand_interruption.md`

## Summary
- 中断可能なサブコマンド、Ctrl+C によるユーザー中断要求、処理単位の完了または rollback、確定済み部分結果の保存、primary report と terminal result の出力、および中断後の再開禁止を定める共通仕様。
- refactor run と feedback report における中断後の詳細な state・次操作は、それぞれの個別仕様へ委譲する上位入口。

## Read this when
- `cmoc realization refactor fork` または `cmoc feedback report` の Ctrl+C、中断完了、部分結果保存、terminal result を実装・レビューするとき。
- 中断後に Codex CLI の再呼び出しや retry を行わない制御、primary report の保存、正常系とエラー系の境界を確認するとき。
- refactor run や feedback report の中断後 state と次の操作を確認する前に、共通の中断規則と個別仕様への委譲先を把握するとき。

## Do not read this when
- 対象が中断可能サブコマンドではなく、通常実行や一般的なエラー処理だけを扱うとき。
- refactor run の中断後 state だけを確認したい場合は `realization_refactor.md` を、feedback report の中断後処理だけを確認したい場合は `feedback_report.md` を直接読むとき。
- ログの共通保存・出力形式、エラー処理、Windows toast の詳細だけを確認したいときは、それぞれ指定された個別正本を直接読むとき。

## hash
- 927a066890436e0445051f386a53d6ee5d7c1c21c587833f988d401fcae22d27

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
