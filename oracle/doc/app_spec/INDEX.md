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
- cmoc が `codex exec` を呼び出す際の正本規約。agent call と Codex call の定義、call-scoped path context、環境変数、CLI 引数、sandbox、ファイルアクセス、モデル・provider、prompt の受け渡し、ログ、session、Structured Output、補正、並列実行、失敗時の扱いを定める。Codex CLI 呼び出しの構築・検証・障害対応の実装や仕様を確認する際の入口となる。

## Read this when
- cmoc の Codex CLI 呼び出し方法、argv 上書き、sandbox、provider/model/reasoning effort、prompt stdin、ログ保存を変更または確認するとき
- Structured Output の schema 保存・検証・同一 session での補正、quota・一時障害・想定外エラーへの対応を変更または確認するとき
- agent call ごとの path context、ファイルアクセス制限、feedback reporter、並列呼び出しの規約を確認するとき

## Do not read this when
- Codex CLI 呼び出し規約ではなく、個別 agent call の意味上の責務や判断基準を確認する場合は、対応する oracle doc を直接読む
- Windows toast 通知、model provider の詳細仕様、feedback observation の詳細仕様、prompt standard など個別の正本が対象の場合は、それぞれの参照先を直接読む
- INDEX.md のエントリー生成や一般的なリポジトリ開発手順だけを確認する場合

## hash
- e0cfdb5a44a946e0dfbe8931cb419fd2bfe4f084625fc3dad595fa6ffa5589bf

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
- 非対話サブコマンドの console 出力、terminal result、サブコマンドログ、時間・パス表示、TUI／自動補完との境界を定める共通契約の正本。個別サブコマンド仕様が定める result、completion_reason、primary report、次の操作、終了コードと組み合わせて、最外側サブコマンドの表示・記録挙動を確認するための入口となる。ANSI 色、動的表示、verbosity、stdout 用 JSON schema、report 内容、Windows toast 拡張、feedback event 契約の変更は対象外。

## Read this when
- 非対話サブコマンドの stdout／stderr、進行通知、terminal result、終了順序、終了コード表示を実装・変更・検証するとき
- サブコマンドログの保存場所、JSON Lines 形式、即時 flush、記録対象イベント、Codex call や failure の診断情報を扱うとき
- 時間表示やフルパス表示の共通フォーマットを確認するとき
- cmoc 内部呼び出しでの terminal result 抑制、TUI 終了後の表示、自動補完プローブの出力境界を確認するとき

## Do not read this when
- 個別サブコマンド固有の result、completion_reason、primary report、次の操作、終了コードの意味だけを確認する場合は、そのサブコマンド仕様を直接読む
- Windows toast の対象・発火順序・通知内容を確認する場合は、Windows toast 通知仕様を直接読む
- feedback observation の通知境界や detector rule を確認する場合は、feedback observation 仕様を直接読む
- 自動補完プローブの判定・処理境界を確認する場合は、CLI 自動補完仕様を直接読む
- report 本文の内容や判定基準、ANSI color、verbosity、debug option、動的表示を追加・変更する場合

## hash
- de3a07649a5f7c7b9fb4035f5e12f2f26bdee52209b486f660e7abd87387702f

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
- cmocがエディタ向け入力文面を生成し、ユーザーのオリジナルプロンプトを完全プロンプトへ組み込む仕様を定義する。初期コメントの責務、完全プロンプトのskeleton、エディタ起動、コメント除去、プレースホルダー置換、保存までを扱う。プロンプト編集入力や完全プロンプト確定処理の仕様を確認する際の入口となる。

## Read this when
- エディタに提示する初期入力文面の構成や責務を確認するとき
- skeletonへのオリジナルプロンプト挿入条件を確認するとき
- エディタの選択、起動待機、入力読み出し、完全プロンプト保存の挙動を確認するとき

## Do not read this when
- 正確な初期コメントの表示文面そのものを確認したいときは、指定された正本実装を直接読む
- サブコマンド固有のプロンプト契約やパラメータ構築を確認したいときは、対応するbuild_*_parameterの仕様・実装を直接読む
- 実行時生成物の内容や個別のログを確認したいとき

## hash
- 2c21fa7b9fffb3d90522994106ad255df4d918ec8bb68ec6fdbe7448427c1264

# `prompt_standard.md`

## Summary
- cmoc の agent call 用 prompt に含める情報、正本仕様・oracle src・realization implementation の責務境界、および実行時生成物の位置づけを定める。
- prompt part の決定論的な注入、共通 feedback instruction、Structured Output の schema・事後条件・受理条件の境界、`summary` と `goal` の使い分けを扱う。
- prompt 構築時の参照関係、placeholder、Markdown 記法、言語方針を確認するための共通ルーティング入口である。

## Read this when
- agent call の prompt に指示や参照先を追加・変更するとき
- oracle doc、oracle src、realization implementation、実行時生成物の責務境界を判断するとき
- Structured Output の schema、決定論的事後条件、補正 prompt の責務を設計・レビューするとき
- `summary`、`goal`、prompt part、placeholder、`cmoc_block` / `cmoc_ref` の扱いを確認するとき

## Do not read this when
- cmoc の個別機能に固有の意味仕様だけを確認する場合は、対応する oracle doc を直接読む
- prompt の正確な文面や builder の実装を変更する場合は、対応する oracle src を直接読む
- realization 側の保存・受け渡し実装だけを確認する場合は、対象 realization file とその担当仕様を読む

## hash
- 94c675220dcadb58d65458abde1ae6ac94b166b8e54809b7e4dd6e558be1b240

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
- cmoc のサブコマンド仕様を、個別の正本文書へ振り分けるルーティング入口。doctor、indexing、tui、oracle 操作、realization の apply/refactor、session の fork/join/abandon、編集 run lifecycle、feedback report の実行条件・状態遷移・責務境界を確認する文書群を扱う。

## Read this when
- cmoc サブコマンドの挙動仕様を調査・実装・レビューする際に、対象コマンドの正本仕様を特定したいとき。
- session lifecycle と編集 run lifecycle、oracle 操作、realization 操作、feedback report のどの仕様を読むべきか判断するとき。

## Do not read this when
- 特定サブコマンドの詳細仕様、内部処理、状態 schema、agent prompt、Structured Output schema を直接確認したいときは、対応する個別の正本文書へ進む。
- 一般的な git 操作、共通中断処理、indexing の意味論、feedback observation/state の詳細だけを確認したいときは、該当する参照先を直接読む。

## hash
- added83b6cf5fcade1cb761e9d29d9eb0c5ebf3b6733d1eb1c93c73dc37005a9

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
- `cmoc` の初回セットアップ、セッション分岐・統合、oracle の調査・編集・レビュー、realization の apply/refactor 実行と run lifecycle を含む標準 workflow を説明する利用手順。cmoc の運用手順や workload の使い分けを確認する入口。

## Read this when
- cmoc を初めて導入・実行するとき
- oracle 変更から realization 反映までの workflow や session/run lifecycle を確認するとき
- realization apply と realization refactor の使い分けを確認するとき

## Do not read this when
- 個別の oracle 仕様や realization 実装の内容を確認したいとき
- cmoc の内部設計・開発環境・テスト実行規則を確認したいときは、それぞれの専用文書を直接読む

## hash
- 39da44eb91651a997184df522e971bdc5bad67987fc185cf451173fd7e95b4fb

# `windows_toast_notification.md`

## Summary
- Windows 11 上の WSL2 で cmoc が表示する Windows toast 通知の正本仕様。非対話サブコマンドの terminal result 通知と TUI の agent turn 完了通知を対象に、通知境界、重複排除、必須内容、Codex CLI 設定境界、transport 制約、自動補完時の除外条件、non-goal を定める。

## Read this when
- Windows toast 通知の適用対象や、非対話サブコマンドと TUI の発火タイミングを確認・変更するとき。
- terminal result の分類、user_interruption の扱い、通知内容の制約、通知失敗時の本命処理への影響を確認するとき。
- Codex CLI の callback を呼び出し単位で設定・無効化する要件や、未検証の外部 interface を正本仕様に断定してはならない境界を確認するとき。
- WSL2 から Windows toast transport を実装・変更するとき、依存関係、データ transport、安全性、有限時間、失敗時の扱いを確認するとき。

## Do not read this when
- 共通の terminal result 分類やユーザー中断要求の成立条件そのものを確認する場合は、それぞれの正本仕様を直接読む。
- 通知の具体的な実装方式、callback の実際の設定 key・event・payload、transport の具体方式を確認する場合は、検証結果または realization implementation を読む。
- 通知を適用しない Codex 内部処理や non-goal の機能だけを確認する場合は、該当する下位仕様や実装へ直接進む。

## hash
- 2eb8af13277c396ec835842bb9a6d0c22128f90809a28afa31571eb13329c455
