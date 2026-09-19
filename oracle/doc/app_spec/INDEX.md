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
- Codex CLI の agent call と Codex call の呼び出し規約を定める正本仕様。path context、CODEX_HOME、preflight、argv による設定上書き、sandbox と詳細なファイルアクセス制限、model provider、prompt 構築・優先関係を扱う。

## Read this when
- cmoc が Codex CLI を呼び出す処理の引数、環境、sandbox、アクセス制限、識別子、provider 設定、または prompt 構築を確認・変更するとき。
- agent call の cwd や root placeholder、preflight validation、Codex call の retry・resume を含む実行規則の適合性を確認するとき。

## Do not read this when
- 個別 workload の意味上の責務や判断基準を確認する場合は、まずその workload に対応する oracle doc を読むべきとき。
- AgentCallParameter の正確な field 構造、path context の導出実装、prompt builder の詳細、model provider の個別仕様を直接確認する場合は、本文が委譲する対応する oracle src または oracle doc を読むべきとき。
- 最外側の実行 ID、Windows toast 通知、実経路統合テストなど、本文が別の正本へ明示的に委譲している個別規則だけを調べるとき。

## hash
- bb49c57bf6bf9588bf37239df0a65e310e19400bb15afa8b7e3617aee0c4719a

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
- 非対話サブコマンドの console、primary report、terminal result、サブコマンドログ、および TUI・自動補完との境界を定める共通契約。個別サブコマンド仕様から参照される出力・保存・終端処理の基盤。

## Read this when
- 非対話サブコマンドの stdout・stderr、進行通知、実行 ID、時間表示、パス表示を確認・変更するとき
- primary report や terminal result の生成条件、掲載内容、表示順序、終端確定処理を確認するとき
- サブコマンドログの保存先、JSON Lines 形式、記録イベント、flush、診断情報を確認するとき
- TUI、editor input handoff、自動補完と非対話サブコマンドの出力境界を確認するとき

## Do not read this when
- 個別サブコマンド固有の result、completion_reason、primary report 形式、保存先、終了コードだけを確認したいときは、そのサブコマンド仕様を直接読む
- エラー分類・エラー終了の確定、feedback の保持・通知、Windows toast、自動補完の詳細判定を確認したいときは、それぞれの参照先仕様を直接読む
- 実装コードや個別テストの具体的な手順だけを調べるとき

## hash
- 374254fec64a847fe830b2dce55d3cf0c788f1a03bb074e906352ea094062d73

# `doctor_preprocess.md`

## Summary
- 各サブコマンドの本命処理開始前に共通して実行される検証・修復処理を定義し、cmoc の実行基盤、追跡状態、refactor state、feedback reporter/client の事前条件を扱う。

## Read this when
- サブコマンド共通の事前検証・修復、git 追跡／非追跡保証、refactor state の schema・entry 同期、または feedback reporter/client の利用不能時の degraded warning を確認するとき。

## Do not read this when
- git working tree や staging area の clean 状態など、doctor preprocess 後に各サブコマンド固有の仕様で検査される条件だけを確認するとき。

## hash
- 5524033594108d46485f83c748f533c89d8827f82f29f9c4e76a943821bb0ef3

# `editor_input_handoff.md`

## Summary
- Codex TUI の agent が、人間指定の active target に対して、editor work file 全体を MCP 経由で上書きする editor input handoff の正本仕様です。
- handoff target の登録・受付期間・無効化、上書きの検証と直列化、agent の利用条件、送信元情報、失敗時の責務、および non-goal を定めています。
- prompt editor input の確定手順、Codex のファイルアクセス制限、送信元ログの詳細、MCP input schema、handoff instruction の文面は、関連する正本仕様や oracle source へ委譲されています。

## Read this when
- Codex TUI から待機中の prompt editor input へ完成済み内容を引き渡す処理の条件や責務を確認するとき。
- active target の受付状態、同一 target への上書き、対象 file の検証、送信元情報、または handoff 失敗時の扱いを確認・変更するとき。
- handoff に関する複数の正本の分担を把握し、MCP schema や prompt 文面など具体的な定義の参照先を特定するとき。

## Do not read this when
- prompt editor input の writer 境界や最終読み取り手順だけを確認したいときは、prompt editor input の正本仕様を直接読んでください。
- Codex の詳細なファイルアクセス制限や handoff instruction の注入方法だけを確認したいときは、Codex 実行規則の該当仕様を直接読んでください。
- MCP の input schema や handoff prompt の正確な実装定義だけを確認したいときは、対応する oracle source を直接読んでください。
- 送信元情報の記録方法や保存済みログへの到達だけを確認したいときは、console と file log の正本仕様を直接読んでください。

## hash
- 69b532a1b64993d0870431bd55e443fc16ae9893bf8534bc9a6ec7609e50b5c9

# `error_handling.md`

## Summary
- handled failure と internal failure の分類、およびエラー終了時の state 確定・rollback・primary report・terminal result の共通規則を定める正本。
- エラー種別ごとの表示内容、スタックトレースの扱い、診断ログへの保存、および正常結果として扱う attention 等との境界を示す。
- 個別仕様に特別なエラー処理がない場合に適用する、エラーハンドリング共通規則への入口。

## Read this when
- エラー終了を handled failure または internal failure に分類する必要があるとき
- エラー時の report 保存、terminal result、終了イベント、終了コード、rollback、または state 確定の共通契約を確認するとき
- console・stderr・サブコマンドログにおけるスタックトレースやエラー詳細の扱いを確認するとき
- 個別仕様に明示されていないエラー処理の共通規則を確認するとき

## Do not read this when
- 対象サブコマンドの個別仕様がエラー時の state、rollback、report、次の操作、終了コードを明示しており、その個別規則だけを確認すればよいとき
- console と terminal result の出力先・表示順序・共通 field の正本を確認したいときは、まずコンソール・ファイル、ログ出力規則を読むとき
- ユーザー中断の正常系処理だけを確認したいときは、サブコマンドのユーザー中断を直接読むとき

## hash
- 3fe9e3ef1b5bb8f0de010ff5978ad83e8c33c6b71f7759b87551d3122a7171ff

# `feedback.md`

## Summary
- feedback subsystem 全体の目的、用語と issue 結果分類、remediation run の処理モデル、正本仕様の責務分担、既存 workload との境界、および non-goal を定義する上位仕様。
- feedback の収集・状態管理・`cmoc feedback report` の責務境界を確認し、automatic remediation 後に人間対応が必要な issue と判定不能な `incomplete` 診断の扱いを理解するための入口。

## Read this when
- feedback observation、active issue、intake wave、high-watermark、publication、または issue remediation の結果分類を確認するとき。
- `cmoc feedback report` の処理モデルや、normalization・agent call・commit・merge・publication の責務分担を確認するとき。
- feedback に関する三つの正本仕様のどこを読むべきか判断するとき。
- 既存 workload の成果物を feedback issue に自動変換してよいか、また feedback が他 workload の状態や成功判定へ影響するかを確認するとき。

## Do not read this when
- observation の具体的な報告基準、受け入れ検査、機械 detector、raw 保存の詳細だけを確認したいときは、feedback observation の正本仕様へ進む。
- repository-local state、checkpoint、publication、cleanup、または high-watermark の実装詳細だけを確認したいときは、feedback state の正本仕様へ進む。
- CLI の事前条件、表示、終了結果、agent prompt、commit・merge・join 後の確定処理だけを確認したいときは、`cmoc feedback report` の正本仕様へ進む。
- 個別の realization file の実装責務や既存 realization の挙動を確認するだけのとき。

## hash
- 4ede5c6040dc5275b935a5eac247006de95340f6a5928a4f14015326492a8fab

# `feedback_observation.md`

## Summary
- feedback observation の報告基準、agent-facing MCP reporter の契約、collector と transport の境界、機械的検出 rule、raw observation の保存・durability・retention を定める正本仕様。feedback の収集経路や受け入れ条件、保存ライフサイクルを確認する入口。

## Read this when
- agent がセッション外対応候補となる問題の報告可否や報告条件を確認するとき
- `cmoc_feedback.submit_observation` の input、result、互換処理、受け入れ検査を確認するとき
- collector の context 確定、capability、MCP/IPC transport、call 終了処理の境界を確認するとき
- structured log からの machine observation 検出 rule、threshold、issue key の仕様を確認するとき
- raw observation の保存単位、durability、pending retention、cleanup 条件を確認するとき

## Do not read this when
- feedback observation の issue identity、remediation 可否、現在状態を判断したいとき
- prompt へ埋め込む正確な agent 向け文面や完全 prompt の組み立てを確認したいときは、指定された prompt builder の正本を直接読むとき
- 実装の具体的な module 構成や内部 API を確認したいとき。本文は実装裁量を残しており、対応する実装を直接読むべきとき
- 既存 observation の集約・report cut・remediation intake の運用判断だけを確認したいとき

## hash
- 2245fd6dd3f4d20ddbd13f8945405a3f6d72cade53757540f6b13d928752a099

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
- `INDEX.md` の自動インデクシングに関する仕様を定義し、処理対象の列挙、目次情報の生成・更新、ハッシュ検証、コミット、および agent call の実行方針を扱う。
- インデクシングの実行手順や、目次情報生成の動作条件・並列化条件を確認するための入口となる。

## Read this when
- `INDEX.md` の生成・更新処理の仕様を確認するとき。
- インデクシング対象の判定、処理順序、ハッシュ不一致時の再生成、または生成 agent call の実行条件を変更・検証するとき。
- `INDEX.md` による routing の意味要件や、目次情報に含めるべき内容を判断するとき。

## Do not read this when
- 個別ファイルやディレクトリの実装内容そのものを確認したいとき。
- 特定の目次エントリーの内容だけを確認したいときは、対象階層の `INDEX.md` を優先する。
- インデクシングとは無関係な oracle app spec の仕様や、通常のファイル編集手順だけを調べるとき。

## hash
- 264015e5526f632f2c55d11933fca7f3bacd22fb5966cfc92a431c98c1bae5c9

# `oracle_and_realization.md`

## Summary
- oracle file と realization file の分類、正本責務、優先関係、および相互適合性を定義する共通契約。oracle doc・oracle src・oracle test と realization implementation・test・ancillary の役割を区別し、仕様と実装を扱う際の判断基準を示す。

## Read this when
- oracle file または realization file の新規作成・変更・レビューで、正本仕様の所有者、委譲された exact detail、または仕様適合性の判断基準を確認するとき。
- oracle doc と oracle src の記述が競合している、あるいは realization file へ仕様を複製せず参照・生成・変換で対応する必要があるとき。
- realization apply/refactor の修正対象を、明示仕様との不整合または realization file だけで確認できる致命的な不具合に限定するとき。

## Do not read this when
- 個別の oracle file が所有する具体的な要求や prompt・schema の exact detail だけを確認したいときは、その参照先の oracle doc または oracle src を直接読む。
- 一般的な実装品質改善、未定義部分の網羅的な分類、または INDEX.md の構造自体を確認したいとき。

## hash
- b537a66957cc2885b4b401e3d9578d00e0c807711a2d183312385046bd006229

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
- オリジナルプロンプトを入力する editor work file のライフサイクル、handoff による上書き、検証・最終読み取り・保存・コメント除去の確定手順を定める正本仕様。
- editor work file と保存コピーの責任分界、エディタ起動順序、後続 agent が参照してはならない境界を示す。
- 初期コメントや完全 prompt の構築詳細は別の builder・サブコマンド仕様へ委譲し、本書では editor input の入出力 lifecycle に限定する。

## Read this when
- editor input の生成、エディタ起動、handoff target の適用、最終入力の検証・保存・抽出、失敗時の work file 保持を確認または変更するとき。
- editor work file と保存コピーの書き込み主体や、確定済み入力を再取得・更新しない制約を確認するとき。

## Do not read this when
- 初期コメントや template の正確な構築方法を確認したいときは、指定された builder の正本仕様を直接読む。
- 完全 prompt や prompt skeleton の構築、サブコマンド固有の prompt 反映規則を確認したいときは、該当するサブコマンド仕様を直接読む。
- editor input の lifecycle ではなく、共通 handoff の詳細な target lifecycle や agent の責務・権限だけを確認したいときは、editor_input_handoff の該当節を直接読む。

## hash
- 913591426b05e6c810c191c4b2449f493e890b3c861fff30c2ddd5779d015cd2

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
- サブコマンドごとの正本仕様をまとめる領域。セッション管理、編集 run、realization の apply／refactor、feedback report、oracle 編集、調査、doctor、indexing、TUI など、cmoc の個別 CLI 操作に固有の契約を扱う。
- 各仕様は、CLI の引数・事前条件・実行手順・状態遷移・終了結果・primary report と、共通仕様や下位処理へ委譲する境界を定める。

## Read this when
- 特定の cmoc サブコマンドの実行条件、処理手順、終了状態、報告要件を確認するとき
- サブコマンドの実装や変更が、共通の session／run lifecycle と workload 固有処理のどちらに属するかを判断するとき
- 個別サブコマンドの正本仕様を、アプリケーション仕様の総論や共通モデルから切り分けて確認するとき

## Do not read this when
- サブコマンドに共通する branch model、session state、run isolation、feedback state などの一般モデルだけを確認したいときは、それぞれの共通仕様を直接読む
- 特定サブコマンドの詳細が既に特定できている場合は、このディレクトリ全体ではなく該当する個別仕様を直接読む
- 実装コード、agent call の具体的な builder、Structured Output schema、診断ログの実データだけを確認したいとき

## hash
- 34f50aef313167217b082c4f8fa3020f01198f009278d5064ceac5f86e767bba

# `subcommand_interruption.md`

## Summary
- 中断可能なサブコマンドにおける Ctrl+C のユーザー中断要求、共通の完了処理、結果保存、terminal result、および中断後の扱いを定める仕様。

## Read this when
- `cmoc realization refactor fork` または `cmoc feedback report` の実行中断を実装・確認するとき。
- 中断要求後の処理単位、state 更新、primary report 保存、再試行禁止、または正常系としての終了を確認するとき。
- 新たなサブコマンドを中断可能にする個別仕様を検討するとき。

## Do not read this when
- 中断後の refactor run の詳細な state や次の操作を確認する場合は realization refactor の個別仕様を読むとき。
- feedback report の issue 処理単位、run state、publication、observation retention、次の操作を確認する場合は feedback report の個別仕様を直接読むとき。
- コンソール・ファイルの共通出力規則や Windows toast 通知の詳細を確認する場合は、それぞれの正本仕様を直接読むとき。

## hash
- 864db649d924cdadc03c512bb9f08026ef5f39d714aac580f28f87e5f991421f

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
