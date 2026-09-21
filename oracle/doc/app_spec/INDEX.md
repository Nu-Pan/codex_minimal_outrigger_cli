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
- cmoc から Codex CLI を呼び出す際の、agent call と Codex call の識別、path context、環境変数、preflight、argv 設定上書き、sandbox と詳細なファイルアクセス制限を定める実行規約。
- prompt の責務・優先関係・構築と受け渡し、Git 差分の参照、feedback reporter、editor input handoff MCP、ログ保存、stdout/stderr、session ID の扱いを定める。
- Structured Output の schema 保存、検証、同一 session での補正、補正不能時の処理、および並列実行・quota 待機・一時的なサーバー障害時の retry 規則を定める。

## Read this when
- cmoc の codex exec 呼び出し方法、引数、sandbox、prompt、ログ、Structured Output、retry、quota 待機を確認・変更するとき
- agent call と Codex call の識別や call-scoped path context、Codex CLI へ渡す設定の責務境界を確認するとき
- Codex CLI 呼び出しに関する realization implementation がどの oracle 規則に従うべきか判断するとき

## Do not read this when
- 個別 agent call の業務上の目的・判断基準・workload 固有の builder 内容を確認したいときは、対応する oracle doc または oracle src を直接読む
- AgentCallParameter の正確な field、型、既定値を確認したいときは basic.py を直接読む
- path context の導出、prompt の構築・rendering、file access policy、structured output の registry などの正確な実装仕様を確認したいときは、本文が委譲する oracle src・oracle doc を直接読む

## hash
- 73c2d13640a20017769fea504eb543e13556ed1746db9b4510180d73d42ecd1a

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
- 非対話サブコマンドの console 出力、primary report、terminal result、サブコマンドログに関する共通契約を定める正本仕様。
- 実行 ID・時間・パスの表示形式、stdout/stderr の責務、終端結果の確定順序と表示内容を扱う。
- JSON Lines 形式の診断ログ、Codex call・feedback observation・TUI 送信元情報の記録、および TUI／自動補完との適用境界を定める。
- 個別サブコマンド仕様が定める result、report 固有形式、保存先、終了コードなどへ接続する共通の入口。

## Read this when
- 非対話サブコマンドの console 出力先、進行通知、terminal result、終了時の表示を確認または変更するとき
- primary report の保存条件、共通掲載内容、表示するパスや結果情報を確認するとき
- サブコマンドログの形式、保存場所、即時 flush、診断イベント、Codex call の記録を確認するとき
- cmoc tui、cmoc oracle investigation、cmoc oracle edit、自動補完に共通ログ・通知規則を適用するとき

## Do not read this when
- 個別サブコマンド固有の result、completion_reason、primary report 本文、保存先、終了コードの仕様だけを確認するときは、該当する個別サブコマンド仕様を直接読む
- エラー分類やエラー終了の確定手順だけを確認するときは、error_handling.md を直接読む
- feedback observation の保持・通知境界や detector の詳細だけを確認するときは、feedback_observation.md または feedback.md を直接読む
- Codex exec の識別子・最終出力取得・editor input handoff の詳細だけを確認するときは、codex_exec_rule.md または editor_input_handoff.md を直接読む
- Windows toast の通知対象・発火順序・内容だけを確認するときは、windows_toast_notification.md を直接読む
- CLI 自動補完の判定や通常処理の抑止だけを確認するときは、cli_auto_completion.md を直接読む

## hash
- ed071e751f642d1fb27478dbee7a05b3c4ee9a03e02dbc8abd8a14273bc92003

# `doctor_preprocess.md`

## Summary
- doctor preprocess の共通前処理仕様。cmoc 実行前に、git 管理・ignore 状態、必要ファイルと refactor state の同期、feedback reporter/client の protocol 互換性を検証・修復し、必要な差分を commit する責務を定める。

## Read this when
- cmoc の各サブコマンド開始前に共通して行う検証・修復の条件を確認するとき
- `.cmoc/gu`、`.agents`、`.cmoc/gt` 配下の git 管理状態や refactor state の同期要件を確認するとき
- feedback MCP reporter/client が利用不能または protocol 不一致の場合の degraded 扱いを確認するとき

## Do not read this when
- doctor 本体の個別診断チェックやサブコマンド固有の事前条件を確認するとき
- feedback observation の MCP interface や collector/transport の正本仕様そのものを確認するときは feedback_observation.md を読むとき
- realization refactor の state schema や entry 同期規則そのものを確認するときは realization_refactor.md を読むとき

## hash
- ed697fd998fdf95ae354513efec4eca4a04bc0f8af5e5f29893767e9e28f9bf5

# `editor_input_handoff.md`

## Summary
- Codex TUI の agent から別の prompt editor input へ依頼を渡す共通 handoff 機能の正本仕様。target の lifecycle、handoff ガイド取得、MCP 上書き、本文生成、送信元情報、agent の責務と非目標を定める。
- prompt editor input や Codex 実行規則など別仕様へ委譲された責務との境界を示し、handoff 固有の lifecycle と入力・出力の扱いを確認するための入口となる。

## Read this when
- editor input handoff の target 登録から無効化までの lifecycle、受付条件、完了順序を確認・変更するとき。
- handoff ガイドの取得、項目別依頼の上書き、本文生成、参照情報、送信元情報、tool result・log の扱いを確認するとき。
- agent-facing MCP の責務や handoff の利用条件、禁止事項、non-goal を確認するとき。
- handoff 仕様と prompt editor input、Codex 実行規則、ログ仕様、対応する oracle source の責務分担を整理するとき。

## Do not read this when
- prompt editor input の writer 境界や最終確定手順だけを確認する場合は、prompt editor input の正本仕様を直接読んでください。
- Codex TUI への MCP 注入や file access 制限の共通規則だけを確認する場合は、Codex 実行規則の該当仕様を直接読んでください。
- 送信元情報のログ記録だけを確認する場合は、console and file log の該当仕様を直接読んでください。
- handoff ガイド、入力 schema、本文 builder、送信元情報モデルの正確な文面・型・検査規則だけを確認する場合は、本文で指定された oracle source または schema を直接読んでください。

## hash
- 54df88ab8bb6f02e87856ff0632b7da5ff7fb21aaea2f88b2f224cd1e8cb430f

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
- feedback subsystem の目的・観測経路・結果分類・処理モデルを定義する正本仕様。
- feedback observation の収集、repository-local state、`cmoc feedback report` の CLI 処理へ分担された仕様の入口であり、既存 workload や realization 作業との境界も示す。

## Read this when
- feedback の observation を issue として扱う基準、`fixed`・`human_required`・`inconclusive` などの結果分類、または正常 publication の条件を確認するとき。
- feedback report の intake wave、high-watermark、再確認、merge 後 publication の全体モデルや、他 workload からの自動変換境界を確認するとき。

## Do not read this when
- observation の具体的な報告基準・受け入れ検査・raw 保存だけを確認したいときは、feedback observation の専用仕様を直接読む。
- repository-local state、checkpoint、cleanup の詳細だけを確認したいときは、feedback state の専用仕様を直接読む。
- `cmoc feedback report` の CLI 事前条件、agent call、commit、merge、表示、終了結果の詳細だけを確認したいときは、feedback report のサブコマンド仕様を直接読む。

## hash
- 541ecb66cee829fc33b36f0fb6b60dad8ea016a9806ad73251d0a1b6c78030e2

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
- cmoc が `INDEX.md` を配置・生成・更新するための正本仕様を定義する。対象ディレクトリや目次対象の選別、ルーティング情報の意味要件、ハッシュ管理、agent call の生成・並列実行、インデクシング実行条件を扱う。

## Read this when
- `INDEX.md` の自動インデクシングの対象範囲や、目次情報を生成・更新する処理の仕様を確認するとき。
- INDEX エントリーの Summary / Read this when / Do not read this when に求められる意味要件や、本文と INDEX のどちらを優先すべきか判断するとき。
- インデクシングの処理順序、ハッシュによる再生成判定、agent call の並列化や実行条件を調査・変更するとき。

## Do not read this when
- 個別のサブコマンドの利用手順や実行順序だけを確認したい場合は、対応するサブコマンド仕様を直接読む。
- INDEX エントリー生成の具体的な prompt 構築や workload 固有の起動パラメータだけを調査する場合は、指定された実装側の builder を直接読む。
- 対象ファイルの内容や個別仕様を参照するだけで、INDEX の配置・生成・更新処理に関係しない場合。

## hash
- b7e52618b65d94d31b170096efaad4b88e5ad4b7ce39d5773b06e68f7605f4d1

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
- work-root 配下の regular file を oracle／realization／対象外へ分類するための、全体列挙、Git ignore、pruning、symlink・非通常ファイル、性能不変条件、回帰検証の正本ルールを定義する。
- oracle／realization の列挙結果や refactor state の整合性を確認する作業で、単純なファイル一覧ではなく repository context と ignore 規則を含む列挙仕様へ進むための入口となる。

## Read this when
- oracle file と realization file の列挙結果、対象外 root、nested Git working tree、Git ignore の扱いを確認するとき。
- traversal の pruning 境界、symlink・FIFO・socket・device の扱い、linked worktree の .git file 対応を実装または検証するとき。
- 列挙の Git subprocess 数や ignore source 検証回数など、性能不変条件と回帰 fixture の要件を確認するとき。

## Do not read this when
- 特定の oracle file や realization file の本文仕様だけを確認したいとき。
- 列挙結果や traversal、Git ignore、pruning の挙動に関係しない機能の実装・検証を行うとき。

## hash
- a8acd4d9e48806b9fc443df9605c86acdbc2447d11bdf384b555db2642fce277

# `prompt_editor_input.md`

## Summary
- プロンプト編集用の一時作業ファイルと保存コピーを分離し、エディタ起動から入力検証・保存・確定・削除までのライフサイクルを定義する正本仕様。
- handoff の詳細、完全な prompt 構築、コンソール出力、直接編集権限などを関連仕様へ委譲し、この文書では editor input 固有の責務と確定手順を扱う。

## Read this when
- editor work file の生成・エディタ起動・handoff ガイド適用・入力検証・保存コピー作成・オリジナルプロンプト確定・成功時削除または失敗時保持の挙動を確認したいとき。
- 入力結果を保存記録として扱う範囲や、後続 agent が一時作業ファイルを参照してはならない境界を確認したいとき。

## Do not read this when
- handoff target のライフサイクルや MCP interface の詳細を確認したいときは editor_input_handoff の仕様を直接読むべきです。
- 完全 prompt や prompt skeleton の構築内容を確認したいときは、各サブコマンドおよび builder の正本仕様を直接読むべきです。
- コンソール出力先や TUI との境界だけを確認したいときは console_and_file_log の仕様を直接読むべきです。

## hash
- aff74c29022aa11c214555b696b8df0b423ca65f1d43b3535f9b77294b56156a

# `run_isolation.md`

## Summary
- run の fork から join または abandon までの隔離作業 lifecycle と、サブコマンド呼び出しとの関係を定義する。
- run の branch・worktree、agent call の cwd/path context、アクセス境界、ログ・session state・feedback state の管理責任を定義する。

## Read this when
- run の lifecycle、branch/worktree 上の成果物、join・abandon の扱いを確認したいとき。
- run 上の agent call の作業場所や path context、ファイルアクセス制限、cmoc 管理データとの責任分界を確認したいとき。

## Do not read this when
- read-only investigation、cmoc 自身による機械的更新、または session join の conflict 解消について、明示的な join を必要とする編集 run の規則を確認する必要がないとき。
- branch・worktree の命名規則や永続化 run field の正確な定義だけを確認したいとき。

## hash
- de4b790e3b7653d15e714e93ff42c426e6924581bf68112b1306102cea2e65ea

# `session_state.md`

## Summary
- cmoc workflow における session と編集 run の lifecycle、永続化する状態、共通事前条件、状態遷移を定める正本仕様。

## Read this when
- session または編集 run の state、kind、branch、fork commit の意味を確認するとき
- session fork・join・abandon、workload 開始、feedback report recovery の状態遷移や事前条件を変更・実装するとき
- session state file に保存すべき情報と保存してはいけない情報を判断するとき

## Do not read this when
- feedback の repository-local state の保存対象や lifecycle だけを確認したいときは feedback state の正本を読む
- apply 固有の join 後 hook や差分追従規則だけを確認したいときは realization apply の仕様を直接読む
- oracle edit の動作や、session state file の具体的な読み書き実装だけを確認したいとき

## hash
- 94e1fa3309b93c408839d6f4a3561c28492d26134a4b29bd10aa488b798b8c84

# `sub_command`

## Summary
- cmoc のサブコマンド仕様を定義する正本文書群。doctor、indexing、tui、session fork/join/abandon、editing run、realization apply/refactor、feedback report、oracle edit/investigation など、各コマンド固有の契約と共通 lifecycle への入口を提供する。

## Read this when
- サブコマンドの引数、事前条件、実行手順、終了状態、primary report の要件を確認するとき。
- session や editing run の lifecycle と、realization・feedback workload 固有仕様の境界を確認するとき。
- 目的のサブコマンド仕様書を特定し、その本文へ進む入口が必要なとき。

## Do not read this when
- 対象サブコマンドが特定できており、対応する個別仕様書を直接読めば足りるとき。
- サブコマンドではなく、アプリケーション全体、共通状態モデル、branch model、または実装側の詳細仕様だけを確認するとき。

## hash
- da1ba991a8a7f388f1beddac3b3b669cf9a6662eb1b4e73df196844e0d43a9b6

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
