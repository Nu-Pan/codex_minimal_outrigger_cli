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
- `codex exec` による agent call の実行規約を定める正本。path context、環境変数、preflight、argv 上書き、sandbox と詳細な file access policy、prompt の構築・受け渡し、feedback MCP、Structured Output、ログ、並列化、quota 待機、retry、失敗処理までを扱う。

## Read this when
- Codex CLI を呼び出す agent call の引数・cwd・root placeholder・model/provider・reasoning effort・sandbox・承認設定を決めるとき。
- prompt、stdin、stdout/stderr、session ID、output-last-message、Structured Output の schema 保存・検証・補正を実装または確認するとき。
- feedback reporter、editor input handoff MCP、Codex call ログ、並列実行、quota 回復待ち、既知の一時障害 retry、失敗時の扱いを確認するとき。

## Do not read this when
- 個別 agent call の意味上の責務や判断基準を決めるときは、まず対応する oracle doc を読む。
- AgentCallParameter の正確な field 定義・型・既定値を確認するときは、指定された oracle source を直接読む。
- path context、prompt builder、file access policy、feedback reporting、editor input handoff、quota probe、Structured Output の正確な実装文面を確認するときは、本文が委譲する各 oracle source または oracle doc を直接読む。

## hash
- c7e8982afb6b77332992ba37b9ee2a7197e961293ecc9ab833747c4d8fe10217

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
- 非対話サブコマンドの console、primary report、サブコマンドログ、terminal result に関する共通契約を定める正本。個別サブコマンド仕様へ進む前に、出力先・表示順序・終端分類・ログ記録の共通ルールを確認する入口。

## Read this when
- 非対話サブコマンドの stdout/stderr、実行 ID、時間やパスの表示形式を確認・変更するとき
- primary report の保存要件、共通掲載内容、terminal result の確定・表示条件を確認するとき
- サブコマンドログの保存場所、JSON Lines 形式、即時 flush、診断記録の要件を確認するとき
- TUI・自動補完と非対話サブコマンドの通知境界を確認するとき

## Do not read this when
- 個別サブコマンド固有の result、completion_reason、report 内容、保存先、終了コードだけを確認したいときは、そのサブコマンド仕様を直接読む
- feedback observation の分類・保持・通知境界や Windows toast の詳細を確認したいときは、参照先の個別仕様を直接読む
- エラー終了の確定やエラー表示規則だけを確認したいときは、error_handling の該当仕様を直接読む

## hash
- 3b5717343ad4bd14de1e0ff3d18d5aa5e1a3171623ddbef9fcc71c5e70d50cdf

# `doctor_preprocess.md`

## Summary
- 各サブコマンドの本命処理開始前に共通検証・修復を行い、cmoc の実行基盤と管理対象ファイルの追跡・整合状態を保証する前処理の仕様。
- feedback MCP reporter/client の起動可能性と collector との protocol compatibility を確認し、利用不能時は degraded warning として本命処理を継続する境界を定める。

## Read this when
- サブコマンド共通の事前検証・修復、git 追跡状態、refactor state の schema・entry 集合同期、または前処理後の commit 条件を確認するとき。
- feedback reporter/client の事前検証、protocol 不一致、利用不能時の warning と degraded 扱いを確認するとき。
- realization_refactor または feedback_report の active run における state 同期タイミングを確認するとき。

## Do not read this when
- git working tree や staging area の clean 状態を、個別サブコマンド固有の事前条件として確認するとき。
- doctor preprocess 完了後に行うサブコマンド固有の事前条件や、本命処理そのものの仕様を確認するとき。
- reporter の repo-local executable の作成・配置・修復や、agent call の sandbox・schema・retry 条件を確認するとき。

## hash
- dc23aed86b94978b836335794d864e43b55f3aa6ca48a985b5e53480a05b3a84

# `editor_input_handoff.md`

## Summary
- Codex TUI の agent が、待機中の prompt editor input の editor work file へ完成済み内容を渡す handoff の責務と契約を定義する。
- active target の登録・受付終了・submission 完了・無効化・最終読み取りまでのライフサイクルと、`cmoc_editor_input.overwrite` による全体置換の境界を示す。

## Read this when
- prompt editor input への handoff の流れ、active target の扱い、submission の直列化や検証条件を確認するとき。
- agent-facing MCP interface、agent の利用条件、拒否時の扱い、handoff の non-goal を確認するとき。
- 正本仕様や input schema、handoff instruction の詳細から確認を始める前に、この機能の責務と参照先を把握するとき。

## Do not read this when
- prompt editor input の writer 境界や最終確定手順だけを確認したいときは、指定された prompt editor input の正本を直接読む。
- Codex の詳細なファイルアクセス制限や書き込み主体の責任分界だけを確認したいときは、指定された codex exec rule の正本を直接読む。
- `cmoc_editor_input.overwrite` の厳密な input schema だけを確認したいときは、指定された schema を直接読む。
- handoff instruction の正確な文面だけを確認したいときは、指定された policy 実装を直接読む。

## hash
- e1452119a39cfc6a9599348ec3cbdb18a0d382959684437303995e8b8bce37db

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
- feedback remediation run が使用する repository-local state の正本。active generation、current pointer、観測の intake wave と high-watermark、checkpoint、report cut、atomic publication、incomplete report、cleanup、および run lifecycle との整合を定める。

## Read this when
- feedback state の配置・所有範囲・保持対象を確認するとき
- feedback report の観測取り込み、wave loop、high-watermark、checkpoint、report cut を設計・実装するとき
- active issue や threshold 未満 aggregate の identity、bounded evidence、publication 対象を確認するとき
- 正常 publication、incomplete 診断、atomic pointer 切替、cleanup、失敗回復の境界を確認するとき
- feedback run の join または abandon が state に与える影響を確認するとき

## Do not read this when
- raw observation の収集規則だけを確認したいときは feedback observation の正本へ進むとき
- feedback report の call 回数・処理順序・incomplete 条件・正常 publication の詳細だけを確認したいときは feedback_report の正本へ進むとき
- 編集 run の join または abandon の共通仕様だけを確認したいときは editing_run の正本へ進むとき
- feedback state の保存や publication に関係しない一般的な subcommand の仕様を確認するとき

## hash
- 35c173fd2ec9e7a1aa758feb3a7b004988467544d0f3c051a9f228b24e83dc46

# `indexing.md`

## Summary
- `INDEX.md` の自動生成・更新に関する正本仕様を定義し、配置対象、目次項目、ルーティング情報、ハッシュ、処理順序、並列実行、実行条件を扱う。

## Read this when
- `INDEX.md` のインデクシング処理の仕様や実行手順を確認・変更するとき。
- 目次情報の生成単位、深さ優先の処理順序、並列化条件、既存差分や自動コミットの扱いを判断するとき。

## Do not read this when
- 個別ファイルやディレクトリの実装内容そのものを調べるとき。
- 目次エントリーの具体的な文章だけを生成・確認する場合は、対象本文や生成処理の定義を直接読む。

## hash
- 35388a7b547055265de2268f2b38171d327408430d8c17d8f25416383d1754e1

# `oracle_and_realization.md`

## Summary
- oracle file と realization file の責務、分類、正本責務の委譲・優先関係、および両者を扱う判断基準を定義する共通契約。oracle doc・oracle src・oracle test と realization implementation・test・ancillary の境界を確認する入口。

## Read this when
- oracle file と realization file の役割や配置区分を判断するとき
- oracle doc と oracle src のどちらを正本として扱うか、または仕様の不整合を整理するとき
- oracle file の調査・レビュー、realization file の実装・テスト・リファクタリング方針を確認するとき
- realization file が oracle file の明示要求に適合しているかを判定するとき

## Do not read this when
- 特定の prompt literal、schema、builder の構築順序や選択値そのものを確認したいときは、委譲先の oracle src を直接読む
- codex_exec_rule に定義された prompt literal 固有の役割や実行時指示の優先関係だけを確認したいとき
- 対象ファイルの具体的な実装挙動やテスト結果だけを調べるとき

## hash
- 46c7c03ba471f72b893a854823ddd22b774518f557c34531fd677686cffb481c

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
- エディタ入力用の作業ファイルについて、初期構築の委譲先、handoff 上書き、検証済み最終読み取り、保存・抽出・削除までの lifecycle と責任分界を定める仕様。
- editor work file と保存コピーの役割・書き込み主体、起動エディタの優先順位、確定時の検証条件と失敗時の復旧境界を確認する入口。

## Read this when
- editor input の作成、handoff による全面上書き、エディタ起動、最終確定、保存コピー、HTML コメント除去、work file 削除の挙動を確認・変更するとき。
- editor lifecycle と prompt 構築仕様の境界や、cmoc・人間・後続 agent のファイル責任分界を確認するとき。

## Do not read this when
- 完全な prompt skeleton や抽出後 prompt の構築内容だけを確認したいときは、各 agent call の builder または該当サブコマンド仕様を直接読む。
- handoff target の共通 lifecycle や MCP による上書き仕様だけを確認したいときは、editor input handoff の正本を直接読む。

## hash
- 2c36a3ba4d5a25e728014de5f392b3263e61265243ddd0c87c48d0f8278e66ac

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
- cmoc の主要サブコマンドと編集・セッション lifecycle の正本仕様への入口。doctor・indexing・tui、oracle investigation/edit、realization apply/refactor、feedback report、session fork/join/abandon、editing run 共通処理を扱う。

## Read this when
- cmoc のサブコマンド実行契約、事前条件、処理手順、終了経路、primary report の要件を確認するとき。
- oracle・realization・feedback に関する workload 固有の処理や、session／editing run の fork・join・abandon lifecycle を確認するとき。
- 複数のサブコマンド仕様の責務分担や、共通仕様と workload 固有仕様のどちらを読むべきか判断するとき。

## Do not read this when
- 個別サブコマンドの詳細実装、正確な prompt 文面、builder 引数、起動パラメータを確認したいときは、指定された実装や個別の正本仕様を直接読む。
- doctor preprocess、feedback observation・feedback state、oracle／realization の適合性、prompt editor、Codex CLI、session state など、参照先の共通仕様だけを確認したいとき。
- 特定の oracle file、realization file、実行結果、診断ログそのものを調査・編集したいとき。

## hash
- 709f9856f48540e49ca98924ba5674d495fffe5adea7d74c458fcc1702810c13

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
