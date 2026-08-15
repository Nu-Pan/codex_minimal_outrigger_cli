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
- cmoc から Codex CLI を呼び出す際の正本規約。agent call の path context、環境変数、argv による設定上書き、sandbox と詳細なファイルアクセス制限、prompt の保存・stdin 渡し、feedback reporter、ログ、Structured Output の検証・補正、並列実行、quota・一時障害・想定外エラーの扱いを定める。Codex 呼び出しの構築・実行・検証・障害対応の実装やレビューにおける入口であり、個別 agent call の意味仕様や参照先の詳細仕様は各 oracle doc へ委ねる。

## Read this when
- cmoc の Codex CLI 起動処理、AgentCallParameter builder、prompt builder、path context、argv、sandbox、ファイルアクセス制限を変更またはレビューするとき。
- Codex exec の Structured Output、session resume、補正 turn、ログ保存、feedback reporter、並列実行、quota 待機、サーバー障害 retry の挙動を確認するとき。
- Codex CLI 呼び出し規約全体の適合性や責務境界を確認するとき。

## Do not read this when
- 個別 agent call の意味上の責務・判断基準を確認するときは、対応する oracle doc を直接読む。
- Windows toast 通知、model provider、prompt 標準、feedback observation などの個別仕様の詳細を確認するときは、本書が参照する各正本仕様を直接読む。
- cmoc の開発環境、実装配置、テスト要件、テスト実行手順を確認するときは、本書ではなく対応する開発環境・設計・テストの oracle 文書を読む。

## hash
- 0902b87fe999baf97adfe2c21892c4b807cfa683d69de903caee6c50ae1aeb2a

# `codex_model_provider.md`

## Summary
- Codex CLI の model provider 設定仕様と、cmoc が担う責務境界を定義する正本文書。`CmocConfigCodex`、provider-local 設定、値の制約、secret 保存禁止、および provider 管理を行わない方針を確認する入口。

## Read this when
- Codex CLI 呼び出しの model/provider 設定、provider ID の検証、provider-local key の扱いを変更・確認するとき
- cmoc が model provider の管理・保証・自動起動を担うか判断するとき
- Codex 設定に保存できる値や secret の扱いを確認するとき

## Do not read this when
- model provider の argv への具体的な反映方法だけを確認したいときは、指定された codex_exec_rule.md を直接読む
- Codex CLI や provider 自体の稼働、認証、推論品質、model pull、cache 管理を調査するとき

## hash
- 928d25ace53f88c12fadd5a3b8fd311001343c040e43aa5dd25945d939bb0d82

# `console_and_file_log.md`

## Summary
- 非対話サブコマンドの console 出力、terminal result、サブコマンドログ、および TUI・自動補完との出力境界を定める共通契約の正本。時間・パス表示、stdout/stderr の責務、終端結果の確定順序と表示内容、JSON Lines ログの診断要件を確認する入口。

## Read this when
- 非対話サブコマンドの進行通知、warning、エラー、terminal result、終了コード、primary report 表示を実装・変更するとき
- サブコマンドログの保存場所、イベント記録、flush、Codex call や failure の診断情報を扱うとき
- TUI 終了時、自動補完プローブ、または内部サブコマンド呼び出しの出力境界を確認するとき
- console の時間表示やフルパス表示の形式を確認するとき

## Do not read this when
- 個別サブコマンド固有の result、completion_reason、primary report、次の操作、終了コードだけを確認する場合は、そのサブコマンド仕様を直接読む
- Windows toast の対象・順序・内容を確認する場合は、専用の通知仕様を直接読む
- feedback observation の通知境界や detector 用イベント契約を確認する場合は、feedback observation 仕様を直接読む
- 自動補完プローブの判定・処理境界だけを確認する場合は、自動補完仕様を直接読む

## hash
- 04ee45199064908a67e0d72875b17027228c57b6dbbb5af19012a12161206087

# `doctor_preprocess.md`

## Summary
- cmoc の各サブコマンド開始前に、リポジトリを実行可能な状態へ検証・修復する doctor preprocess の正本仕様。共通前提の保証、修復困難時のエラー終了、tracked 差分の commit、feedback reporter/client の degraded warning を扱う。doctor preprocess の具体的な検証・修復要件を確認する入口であり、個別サブコマンドの本命処理仕様ではない。

## Read this when
- doctor preprocess の責務や実行順序を実装・レビューするとき
- `.cmoc/gu`、`.agents`、`config.json`、refactor state の追跡状態や同期要件を確認するとき
- feedback MCP reporter/client の事前検証、protocol compatibility、利用不能時の扱いを確認するとき
- doctor preprocess 完了後に個別サブコマンドが検証すべき前提との境界を確認するとき

## Do not read this when
- 特定サブコマンド固有の事前条件や本命処理を確認するとき
- git working tree または staging area の clean 状態の検査仕様だけを確認するとき
- doctor preprocess が保証する対象ではなく、個別サブコマンドの仕様を直接確認すべきとき

## hash
- 7082572dae6260e1658de16f08ecc0f00e588b5d36f7097610a1776e429ac7a1

# `error_handling.md`

## Summary
- エラー終了を handled failure と internal failure に分類し、各分類の判定基準と表示・ログ・スタックトレースの共通契約を定める正本仕様。エラー処理、終了結果、console 出力、サブコマンドログ、診断動作の実装やレビュー時に、分類と表示順序の判断を始める入口となる。正常系として扱う attention などの状態やユーザー中断、個別仕様が優先される範囲も確認できる。

## Read this when
- エラー終了を handled failure と internal failure のどちらに分類するか判断するとき
- エラー terminal result の内容、stdout/stderr の出力、スタックトレース保存先や表示順序を変更・検証するとき
- エラーとして扱わない正常結果や、個別仕様との優先関係を確認するとき

## Do not read this when
- console と terminal result の共通 field、出力先、全体の表示順序そのものを確認する場合は、参照先の console_and_file_log.md を直接読む
- ユーザー中断要求の具体的な扱いだけを確認する場合は、参照先の subcommand_interruption.md を直接読む
- 個別サブコマンド固有の state、rollback、report、次の操作、終了コードを確認する場合は、そのサブコマンドの仕様を直接読む

## hash
- eff35601e9b81a2defb45b4791e1025b9c0c11d3aa2a9cebddfba7cb72067e40

# `feedback.md`

## Summary
- feedback subsystem 全体の目的、処理モデル、共通原則、正本仕様の分担、既存 workload との境界、および non-goal を定義する仕様の入口。
- 観測の raw 保存、repository-local state の publication、normalization・verification、正常 report と incomplete 診断 report の関係を横断的に確認する際に読む。

## Read this when
- feedback subsystem の責務や、agent submission と machine detector から report publication までの処理モデルを確認するとき
- observation・state・feedback_report の各正本仕様が何を定義するかを確認し、適切な下位仕様へ進むとき
- unresolved、resolved、not_actionable、inconclusive の扱い、active state、report cut、正常 publication の境界を把握するとき
- 既存 workload の成果物を feedback へ自動変換しない条件や、feedback を task state と分離する原則を確認するとき

## Do not read this when
- observation の報告基準、収集経路、受け入れ検査、機械 detector、raw 保存だけを確認したいとき
- repository-local state、report cut、checkpoint、atomic publication、cleanup だけを確認したいとき
- cmoc feedback report の事前条件、normalization、verification、表示、終了結果だけを確認したいとき
- feedback の具体的な入力 schema、normalization prompt、verification prompt の詳細を確認したいとき
- 実装詳細、テスト、または realization file の挙動だけを調べるとき

## hash
- 037a71f07a0107a2802e5d61e4ed484f2f2e96a6a1d022be78d89f192803be9e

# `feedback_observation.md`

## Summary
- agent・collector による observation の報告基準、MCP reporter の入力・結果・受け入れ検査、context 確定、保存経路、call 終了処理を定める正本仕様。
- structured log に基づく機械的 observation の detector 境界、初期 allowlist rule、issue key、threshold、除外条件を確認する入口。
- raw observation の保存単位、durability、retention、publication 後の cleanup、および通常サブコマンドへの pending warning の影響範囲を確認する入口。

## Read this when
- feedback observation を agent から報告・収集する処理、reporter/collector MCP interface、受け入れ検査、secret masking、context または capability の設計を変更するとき。
- machine observation の detector、rule registry、recurrence threshold、issue key、structured log event の扱いを実装・変更するとき。
- raw observation の durable 保存、publication、cleanup、retention、pending observation warning の挙動を実装・変更するとき。

## Do not read this when
- feedback observation の同一 issue 判定や現在状態の集約・report cut を扱う場合は、こちらではなく report・集約側の仕様を直接読む。
- 個別の prompt builder 実装や reporter input schema の詳細形式だけを確認する場合は、本文が参照する各正本ファイルを直接読む。
- feedback observation と無関係な agent call、structured output、または通常サブコマンドの仕様を扱う場合。

## hash
- e64de4d3dca0c8816caec3cfccfdc5daeee37c5db912fe839ba42158b94eaeab

# `feedback_state.md`

## Summary
- feedback report が使用する repository-local state の正本。active generation、current pointer、report cut、reference、checkpoint、incomplete 診断 report の責務と保存範囲を定義し、atomic publication、排他制御、再開、cleanup、および corruption 防止の境界を示す。

## Read this when
- feedback state の配置、保持対象、JSON canonical form、hash、排他制御を確認するとき
- active issue や threshold 未満 machine aggregate の identity・保持・昇格条件を決めるとき
- report cut の固定入力、checkpoint の再利用条件、inconclusive 時の扱いを実装または検証するとき
- 正常な Markdown report の publication 順序、current pointer の切替、cleanup の条件を確認するとき
- incomplete 診断 report の durable 保存と、直前の正常 publication を維持する動作を確認するとき

## Do not read this when
- raw observation の形式や detector rule 自体を確認したい場合は、feedback observation の正本を直接読むとき
- feedback report の人間向け内容や表示形式だけを確認する場合
- active state と report publication に関係しない機能の実装・調査を行う場合

## hash
- e48bc94eb8576a2e559811a0097f633db9563055fe8dd42b07bf6122d0c3684d

# `indexing.md`

## Summary
- cmoc がリポジトリ内に INDEX.md を配置・更新する仕組みの仕様を定義する文書。配置対象、目次情報の形式と意味要件、ハッシュ、インデクシング順序、コミット、agent call の並列化、実行条件を扱う。

## Read this when
- INDEX.md の自動生成・更新処理の仕様を確認するとき
- 目次エントリーの内容、ハッシュ計算、対象範囲、更新・コミット手順を変更または検証するとき
- インデクシングの深さ優先処理や agent call の並列実行条件を確認するとき

## Do not read this when
- 個別の実装コードの詳細や CLI の一般的な責務だけを確認したいとき
- 特定ファイルの目次エントリー本文だけを読むべきで、インデクシング全体の仕様確認が不要なとき
- 既存テストの実行方法や Python 開発環境の設定を確認するときは、それぞれの専用仕様・手順を読む

## hash
- e94b7463e662ccbeb3beffe84e449e7b895dfdcf9460a9bccfe704fbc2078ce7

# `misc_spec.md`

## Summary
- cmoc における oracle file と realization file の責務、取り扱い判断基準、適合性、および列挙方法を定義する雑多な仕様の正本。oracle と realization の境界や列挙仕様を確認する際の入口であり、下位の実装・テスト仕様そのものの代替ではない。
- work-root の仮定、cmoc 実行時のパス文脈、タイムスタンプ形式、cmoc-managed-branch の対象範囲など、複数の機能領域にまたがる共通契約を扱う。

## Read this when
- oracle file と realization file の責務境界、分類、適合性、列挙対象、Git ignore、traversal、性能不変条件、または回帰検証の仕様を確認・変更するとき
- work-root、agent call の cwd、タイムスタンプ、または cmoc-managed-branch の定義を確認するとき
- doctor preprocess や realization refactor state 同期に関わる file 列挙結果の意味・境界・性能条件を調査するとき

## Do not read this when
- 特定の oracle doc・oracle src・oracle test の個別仕様だけを確認する場合は、その対象を直接読む
- realization implementation や realization test の具体的な実装詳細だけを変更・調査し、本文で定義する共通契約に関係しない場合
- INDEX.md のルーティング情報だけを確認する場合

## hash
- dd28109f5dd320f5f811caf07ae818b74afe15b2e3bdf69d63cd66cd373e14c1

# `prompt_editor_input.md`

## Summary
- cmoc がエディタ用の初期入力、完全プロンプト skeleton、編集結果の保存・コメント除去・プレースホルダー置換・後続 Agent 起動までを扱う仕様。エディタ入力処理の挙動や、可変な作業ファイルと保存記録の責務分離を確認する際の入口となる。

## Read this when
- エディタ入力の初期表示、オリジナルプロンプトの取得、HTML コメントの扱い、完全プロンプト確定手順を変更または確認するとき。
- editor work file、保存コピー、確定済み完全プロンプトの保存場所や書き込み主体を確認するとき。
- エディタの選択・起動条件、対象ファイルの検証、処理成功時と失敗時の後始末を確認するとき。

## Do not read this when
- サブコマンド固有の prompt skeleton や Agent 呼び出し契約そのものを確認するときは、対応する build_*_parameter の仕様・実装を直接読む。
- 初期コメントの正確な表示文面を確認または変更するときは、editor_input.py を直接読む。
- 一般的なエディタ操作や、保存記録領域の実装詳細だけを調べるときは、より直接的な実装・仕様対象へ進む。

## hash
- 81a1f4cdfeb6ffe1de7a95da82803262dc6c470d376aaef687b63085da7a1391

# `prompt_standard.md`

## Summary
- cmoc が agent call に渡す prompt の責務、正本仕様との境界、構築規則、および出力契約を定める文書。prompt builder・acp builder の文面管理、共通 instruction の注入、placeholder と参照関係、Structured Output の schema／事後条件の分担を確認する入口となる。

## Read this when
- agent call の prompt、prompt builder、acp builder、prompt part、完全 prompt の受け渡しを変更またはレビューするとき
- prompt に注入する cmoc 固有契約、INDEX.md routing、file access、feedback reporting の責務境界を確認するとき
- Structured Output の schema、決定論的事後条件、validator、補正 prompt の責務分担を確認するとき
- prompt の placeholder、cmoc_block／cmoc_ref、言語、summary と goal の構成規則を確認するとき

## Do not read this when
- cmoc の意味仕様そのものを変更または確認する場合は、対応する oracle doc を直接読むとき
- prompt 文面や構築規則に関係しない realization implementation、テスト、または対象 repository 固有の手順だけを扱うとき
- 生成済み prompt、AgentCallParameter.prompt、log、editor input の内容だけを確認するとき

## hash
- 98581dbe5e6e88d5acc674e71e1a27676f74718b482b21ba045ef6dc91325d06

# `run_isolation.md`

## Summary
- run の fork から join または abandon までのライフサイクル、専用 fork サブコマンドによる編集 run、read-only 調査や機械的更新などの例外を定義する作業隔離規則。run 固有の branch・linked worktree、成果物の commit、session branch への merge、run-root 外へ書き込める cmoc 管理データの範囲を確認するための正本。

## Read this when
- run の fork・join・abandon のライフサイクルや、編集 run と非編集 run の扱いを確認するとき
- run branch、fork 時点の commit、linked worktree、成果物の merge・破棄規則を確認するとき
- run-root 外への書き込み例外や、feedback・session state など cmoc 管理データの保存場所を確認するとき

## Do not read this when
- CLI サブコマンドの具体的な引数・実装を確認したいときは、該当する CLI 仕様または実装を直接読む
- feedback の詳細な状態遷移や report 形式だけを確認したいときは、feedback state・feedback observation の正本仕様を直接読む
- run 隔離や lifecycle、branch/worktree、管理データの書き込み範囲に関係しない作業のとき

## hash
- 3aabd242a7edaf586c84b94a72a9ca44eb1325cf6e6031d5743aaceafc35d0ab

# `session_state.md`

## Summary
- cmoc workflow における session と、明示的な join を必要とする realization 編集 run の lifecycle を定義する正本仕様。永続化する最小限の session/run 状態、識別情報、状態遷移を扱う。session・run の開始、実行、join 待ち、中断、失敗、join/abandon 後の状態を確認する入口であり、feedback state や report などの repository-local state の仕様は別文書から確認する。

## Read this when
- session または realization 編集 run の JSON state の項目、初期値、状態遷移、join/abandon に伴う更新規則を実装・確認するとき
- cmoc session 系または cmoc run join/abandon の lifecycle と永続化範囲を確認するとき

## Do not read this when
- feedback の pending observation、active issue、generation、checkpoint、report など repository-local feedback state の仕様を確認するとき
- oracle edit の workload や、session/run state を直接扱わない cmoc workflow の仕様を調べるとき

## hash
- a51826f9117628aed11af12abea90cb9d81df228584fb1457e70afad67115828

# `sub_command`

## Summary
- cmoc の主要サブコマンドおよび session・editing run・feedback に関する正本仕様を集約するディレクトリ。各文書は、対応する CLI の実行条件・責務・状態遷移・agent 呼び出し・成果物やエラー処理を確認するための入口となり、共通 lifecycle や個別の内部仕様へルーティングする。

## Read this when
- cmoc のサブコマンド仕様を横断的に確認したいとき。
- 特定のサブコマンド、session、editing run、feedback の実装・テスト・仕様適合性を調査する際に、対象仕様の入口を選びたいとき。

## Do not read this when
- 特定サブコマンドの詳細を既に特定できている場合は、対応する個別仕様を直接読む。
- doctor preprocess、indexing の本体、共通 prompt editor、ログ、通知、run isolation など、本文から参照される下位仕様だけを確認したい場合は、その正本を直接読む。

## hash
- aab978eada8e2f96272089bed34c65ffdfac00a2281b33b0787f19a9712b8529

# `subcommand_interruption.md`

## Summary
- 中断可能な cmoc サブコマンドについて、Ctrl+C によるユーザー中断要求の定義、対象範囲、共通の正常系処理、ログ・state・report の扱い、中断後の再開可否を定める仕様書。サブコマンドの中断対応を実装・レビューする際の入口となる。

## Read this when
- 中断可能サブコマンドを追加・変更・実装・レビューするとき
- Ctrl+C 受信後の処理単位、部分結果、terminal result、ログ出力、state 更新を確認するとき
- 中断後の run の join、再開、新規 run、report publication の扱いを確認するとき

## Do not read this when
- 通常完了や一般的なエラー処理だけを確認する場合
- 特定サブコマンド固有の中断時 report・state 仕様を確認する場合は、併記された個別仕様を直接読む方が適切
- console の出力形式や Windows toast 通知の詳細だけを確認する場合は、それぞれの正本仕様を直接読む方が適切

## hash
- 302a9f80669cdd645a6eaeb4b29f03a5c02bbfadc379a54ca4dfc6d4b91795bb

# `usage.md`

## Summary
- cmoc の標準的な利用手順を示す入口文書。初回の doctor 実行から session fork、oracle と realization の変更・レビュー、run の join/abandon、session join までの一連の workflow を扱う。
- 短い仕様・実装変更を realization apply で反映する流れと、差分に依存せず全体を追従させる realization refactor の使い分けを確認するための案内役である。

## Read this when
- cmoc を初めて利用するとき
- oracle の変更を realization に反映する手順や、各 workload の使い分けを確認するとき
- session、run、oracle、realization の lifecycle を確認するとき

## Do not read this when
- 個別の仕様や実装の内容を調査するとき
- oracle file の編集内容や review 規則そのものを確認するとき
- realization file の具体的な実装責務を確認するとき

## hash
- d56038df9b029f41ace3a407e3648c28af24bf8a5a98333a7fd44761c818ff69

# `windows_toast_notification.md`

## Summary
- Windows 11 上の WSL2 で、cmoc の最外側サブコマンド完了・入力待ち・異常終了を Windows toast で通知する仕様。非対話サブコマンド、TUI、通知内容、決定論的な発火境界、Codex CLI 設定、外部契約検証、通知 transport、自動補完プローブの制約を定める。Windows toast 通知の実装方針や lifecycle 境界を確認する入口であり、具体的な transport や未確定の Codex callback interface は realization の責務として残す。

## Read this when
- Windows toast 通知の要否、発火タイミング、重複排除、通知内容、失敗時の扱いを実装・レビューするとき
- cmoc の非対話サブコマンドまたは TUI に通知境界を追加・変更するとき
- Codex CLI の callback 設定や、WSL2 から Windows へ安全に通知を transport する方式を検討するとき
- 自動補完プローブで通知処理を抑止する挙動を確認するとき

## Do not read this when
- 通知を伴わない通常のサブコマンド lifecycle や terminal result の分類だけを確認するときは、共通仕様を直接読む
- Codex CLI の callback interface の現在の実装・利用可能性だけを調査するときは、利用中 CLI の外部契約を直接検証する
- 具体的な transport 実装や callback realization の詳細だけを変更するときは、対応する realization の実装・テストを直接読む

## hash
- 9a36838b712bd62f7d7114646d11a3b50d1d078ab7fa436706f45fb1f0c229f1
