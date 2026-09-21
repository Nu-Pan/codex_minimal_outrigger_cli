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
- cmoc から Codex CLI を agent call として実行する際の正本規約。agent call と個別 Codex call の区別、path context、環境変数、事前検証、CLI 設定上書き、sandbox、書き込み責任分界、model/provider、prompt literal の制約を定める。

## Read this when
- Codex CLI 呼び出しの構築・設定・検証・実装方針を確認するとき。
- agent call の cwd、root placeholder、ファイルアクセス制限、sandbox、model/provider、または prompt の責任境界を判断するとき。
- agent-facing prompt に何を含めるべきか、cmoc 内部仕様をどこまで伝えてよいかを確認するとき。

## Do not read this when
- 個別 agent call の意味上の責務や判断基準を確認する場合は、その call に対応する oracle doc を直接読むべきです。
- AgentCallParameter の正確な field、型、既定値を確認する場合は、委譲先の oracle src を直接読むべきです。
- Codex CLI の実行結果や実装の具体的な挙動だけを調べる場合は、対応する realization code や test を直接読むべきです。

## hash
- f3eb44334285fad1de0ee497e8bd8b46ddf7ea16e40419a1797c7c57decac61f

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
- Codex TUI の agent が、別の prompt editor input で待機中の editor work file へ項目別の依頼を handoff する共通仕様。target の lifecycle、handoff ガイド、MCP 入出力、本文生成、agent の責務、送信元情報、参照情報を定める上位の入口で、正確な schema・builder・ログ仕様は下位の oracle へ委譲する。

## Read this when
- prompt editor input への handoff の lifecycle、active target の扱い、ガイド取得から overwrite までの手順を確認したいとき
- handoff MCP の責務・制約、本文生成、送信元情報、参照情報、agent の利用条件を確認したいとき
- editor input handoff の実装や関連する正本仕様がこの共通仕様に適合しているか調べるとき

## Do not read this when
- get_handoff_guide・overwrite の正確な field、型、受理条件、tool result 形式を確認したいときは対応する JSON schema を直接読むべきとき
- handoff ガイドや handoff instruction の固定文面を確認したいときは対応する builder の oracle source を直接読むべきとき
- prompt editor input の writer 境界・確定手順、file access 制限、送信元ログの詳細だけを確認したいときは委譲先の app_spec 文書を直接読むべきとき
- handoff ではなく現在編集中の本文の読み取り・自動保存・editor 終了・排他的 writer 管理を確認したいとき

## hash
- 1e41bb8274f155f56d1eaac6c34fd3ad1ffbebcc92c54813c3ae2d2120927378

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
- feedback remediation run が使う repository-local の active state、immutable な intake wave、high-watermark、checkpoint、report cut、atomic publication、incomplete 診断 report、cleanup を定義する正本仕様です。
- 現在の human_required issue、threshold 未満の machine aggregate、run の回復情報、正常 publication の current pointer をどのように保持・検証・更新するかを扱います。

## Read this when
- feedback state の保存対象、配置、artifact の責務、排他制御、atomic publication、cleanup の挙動を確認するとき。
- feedback remediation run の wave、high-watermark、checkpoint、report cut、publication completion を実装または適合確認するとき。
- 正常 publication と incomplete 処理の境界、current pointer の有効性、active state の履歴保持方針を確認するとき。

## Do not read this when
- raw observation の収集規則や detector rule 自体を確認したいときは、feedback observation の正本仕様を直接読む。
- feedback report subcommand の call 回数・順序、intake wave loop、正常 publication 条件の詳細を確認したいときは、feedback_report の正本仕様を直接読む。
- high-watermark の用語や処理モデルを確認したいときは、feedback の用語・処理モデルを直接読む。
- 具体的な状態管理の実装やテストだけを確認したいときは、対応する realization code または realization test を直接読む。

## hash
- b2593ffba2be4b4a16a78c6879460816953b41091f40bf85fc1c6be2b4ae918e

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
- アプリケーションのサブコマンド仕様群への入口。セッション管理、編集 run、oracle／realization の編集・調査、feedback 報告、doctor・indexing・TUI など、サブコマンド単位の実行契約と終了処理を扱う。
- 共通の編集 run lifecycle を確認する場合は `editing_run.md`、個別コマンドの契約を確認する場合は対応するサブコマンド仕様へ進む構成になっている。

## Read this when
- サブコマンドの引数、事前条件、実行手順、agent call、状態遷移、primary report の要件を確認するとき。
- session や editing run の開始・join・abandon、feedback report の recovery、oracle／realization の編集処理を調べるとき。
- doctor、indexing、TUI などの実行入口と、各終了経路での報告責務を確認するとき。

## Do not read this when
- サブコマンド共通ではない基盤仕様や、branch model、session state、feedback state、run isolation などの正本を直接確認すべきとき。
- 特定のコマンド仕様が明確な場合は、このディレクトリ全体ではなく対応する個別仕様ファイルを直接読むとき。
- 実装コードの正確な prompt、起動パラメータ、Structured Output schema だけを確認したいとき。

## hash
- 467ab3337d48ec40043fce008b968d7b4eca07f70eecb3db8681a6297a22c3df

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
