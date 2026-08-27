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
- Codex CLI の `codex exec` 呼び出しに関する正本規約。agent call と Codex call の単位、path context、`CODEX_HOME`、preflight、argv による設定上書き、sandbox・ファイルアクセス制限、prompt の受け渡し、feedback reporter、ログ・session ID・Structured Output、補正 turn、並列実行、失敗時の retry・quota 待機を定義する。Codex CLI 呼び出し実装の責務や挙動を確認する際の入口であり、詳細な path model、prompt builder、feedback、通知などは本文から参照される各 oracle doc・oracle src に委譲される。

## Read this when
- Codex CLI の `codex exec` または `codex exec resume` の起動引数、環境変数、設定上書き、model/provider/reasoning effort を変更・確認するとき
- agent call の cwd、worktree root、ファイルアクセス mode、sandbox、prompt stdin、ログ保存先を設計・実装するとき
- Structured Output の schema 保存、検証、同一 session での補正、差分不変性、失敗処理を扱うとき
- feedback reporter、Codex call context、並列呼び出し、quota 待機、server capacity retry の実装や挙動を確認するとき

## Do not read this when
- Codex CLI 呼び出し規約そのものではなく、参照先 oracle doc が所有する path model、prompt rendering、feedback observation、Windows toast の詳細仕様を直接確認する場合
- 単に対象 repository の一般的な開発手順、テスト実行手順、または realization 実装の責務だけを確認する場合は、それぞれ対応する開発規約・テスト規約・実装対象へ直接進むとよい

## hash
- 7af70272a4cc832a9b159a3ed590b668464c8fe257ff7b07f0f801b38ef42786

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
- 日本語の自然言語、時間・パス表示、非対話サブコマンドの console 出力、primary report、terminal result、サブコマンドログ、TUI と自動補完の境界に関する共通契約を定める正本文書。個別サブコマンド仕様へ進む前の共通出力・記録規則の入口となる。

## Read this when
- 非対話サブコマンドの stdout/stderr、進行通知、primary report、terminal result の表示や保存契約を確認するとき
- サブコマンドログの JSON Lines 形式、保存場所、flush、診断イベント要件を確認するとき
- TUI、自動補完プローブ、内部サブコマンド呼び出しの出力境界を確認するとき

## Do not read this when
- 個別サブコマンド固有の result、completion_reason、primary report 内容、終了コードだけを確認したいとき
- Windows toast 通知、自動補完の詳細判定、エラー処理、feedback observation の通知境界そのものを確認したいときは、それぞれの正本仕様を直接読む場合

## hash
- 079544d60eb1a021769ba387a657293e962cacb2c736c455f3eb7f62af41e61f

# `doctor_preprocess.md`

## Summary
- doctor preprocess は、cmoc の本命処理開始前に、リポジトリ共通の実行前提を検証し、可能な範囲で修復する共通入口である。
- `.cmoc/gu` の非追跡保証、`.agents`・config・refactor state の追跡保証と同期、feedback reporter/client の protocol 互換性を扱う。
- 修復困難な前提違反は cmoc をエラー終了させるが、feedback reporter/client の利用不能だけは構造化 warning を記録して本命 workload を継続する。
- git working tree または staging area の clean 状態や、個別サブコマンド固有の事前条件は担当しない。前者は必要なサブコマンドが、後者は doctor preprocess 正常終了後の各サブコマンドが検査する。

## Read this when
- cmoc の任意のサブコマンドが本命処理を開始する前に、共通のリポジトリ状態を検証または修復するとき
- `.cmoc/gu`、`.agents`、`.cmoc/gt/ar/config.json`、refactor state の追跡状態や同期条件を確認するとき
- feedback MCP reporter/client の起動可能性、collector との protocol 互換性、利用不能時の degraded warning の扱いを確認するとき

## Do not read this when
- git working tree または staging area の clean 状態だけを検査するとき
- 特定サブコマンド固有の事前条件や本命処理の仕様を確認するとき
- doctor preprocess が正常終了した後の個別サブコマンド処理だけを確認するとき

## hash
- 50bb558ffc38cea1710fcf9ea020c74f6fe543c8289e477593712220dfce31f4

# `error_handling.md`

## Summary
- エラー終了時の handled failure と internal failure の分類基準、および終了状態の確定手順を定義する共通仕様。primary report の保存、error terminal result、サブコマンド終了イベントの順序を扱う。
- handled failure と internal failure それぞれの表示内容、スタックトレースの扱い、診断用ログへの保存規則を定める。
- 正常な処理結果やユーザー中断要求をエラーと扱わない境界、および個別仕様が優先される事項を示すエラー処理の共通入口。

## Read this when
- エラー終了を handled failure と internal failure のどちらに分類するか判断するとき
- primary report、error terminal result、終了イベントの確定順序や保存失敗時の扱いを確認するとき
- エラー時の console 表示、スタックトレース、診断用サブコマンドログの契約を確認するとき
- 個別仕様に特別なエラー処理の記載がない場合の共通規則を確認するとき

## Do not read this when
- console と terminal result の出力先、表示順序、共通 field を確認したいとき
- 中断可能サブコマンドのユーザー中断要求の扱いを確認したいとき
- 個別仕様が state、rollback、report、次の操作、終了コードを明示している場合に、その具体的な処理を確認したいとき

## hash
- 09bad2d213a7377ebe276c8041544ce0bd466fd52b97b91cf5cc1a3b49c42c09

# `feedback.md`

## Summary
- feedback subsystem の目的、観測から report cut・同一性判断・現在性検証・publication までの処理モデルを定義する正本仕様。
- observation、issue candidate、active issue、normal publication、incomplete 診断 report の関係と、feedback と既存 workload の境界を確認する入口。
- 観測基準・raw 保存は feedback_observation.md、repository-local state と atomic publication は feedback_state.md、CLI サブコマンドの処理順序と終了結果は feedback_report.md が担当するため、詳細実装や個別判断はそれらを直接読む。

## Read this when
- feedback subsystem 全体の目的、処理モデル、正本仕様の責務分担を確認するとき
- observation・active issue・正常 report・incomplete 診断 report の関係や publication 条件を確認するとき
- 既存 workload の成果物を feedback へ自動変換する範囲や、feedback の non-goal を確認するとき

## Do not read this when
- observation の報告基準、収集経路、受け入れ検査、raw 保存の詳細だけを確認したいときは feedback_observation.md を直接読む
- state、report cut、checkpoint、atomic publication、cleanup の詳細だけを確認したいときは feedback_state.md を直接読む
- cmoc feedback report の事前条件、agent 処理、表示、終了結果の詳細だけを確認したいときは feedback_report.md を直接読む
- 具体的な realization 実装、テスト手順、または既存 workload の仕様だけを確認したいとき

## hash
- 5b8ffac12ebc86723652bb880e0912017acfd7886d80889cb0a02938dabf276f

# `feedback_observation.md`

## Summary
- feedback observation の報告基準、agent-facing reporter の MCP 契約、collector が確定する context と transport、機械的 detector の初期 rule、raw observation の durability・retention を定める正本仕様。feedback の報告から保存・検出・cleanup までの仕様判断の入口となる。

## Read this when
- agent が人間へ報告すべき問題の条件や、`cmoc_feedback.submit_observation` の入力・結果・rejection の扱いを確認するとき
- collector の capability、context、IPC 経路、call 終了処理、reporter failure の degradation を確認するとき
- machine observation の detector 境界、初期 allowlist rule、issue key、recurrence threshold を確認するとき
- raw observation の保存単位、atomic durability、publication 後の cleanup、pending warning の扱いを確認するとき

## Do not read this when
- 正確な agent 向け feedback prompt の文面を確認する場合は、本文が参照する `feedback_reporting.py` と `complete_prompt.py` を直接読む
- reporter input の root schema の詳細を確認する場合は、本文が参照する `reporter_input.json` を直接読む
- 実装配置や CLI の責務境界を確認する場合は、対応する design rule または realization implementation を直接読む
- test の要件や実行方法だけを確認する場合は、対応する test rule と test_execution を直接読む

## hash
- 5ab42b379b91e8055b154430116c2388200f4817835d6f3237d08187e624a285

# `feedback_state.md`

## Summary
- feedback report が扱う repository-local active state の正本。pending observation、unresolved issue、threshold 未満 aggregate、report cut、reference、checkpoint、publication 済み report、current pointer の所有範囲・保存形式・整合性を定める。
- report cut の固定から checkpoint の再利用、`incomplete` 診断 report、正常 report の atomic publication、current pointer 切替後の cleanup まで、feedback state の状態遷移と排他制御を確認するための入口。
- feedback observation の raw schema や detector rule の詳細ではなく、state artifact のライフサイクル、検証、耐障害性、保持・削除条件を確認する対象。

## Read this when
- `cmoc feedback report` の active state を作成、再開、検証、publication、cleanup するとき。
- active generation、current pointer、report cut、reference、checkpoint の整合性や durable 保存規則を確認するとき。
- `inconclusive` 発生時の `incomplete` 診断 report と、正常 publication 失敗時の再開条件を実装・レビューするとき。
- pending observation、active issue、threshold 未満 machine aggregate の保持範囲や compaction 条件を判断するとき。

## Do not read this when
- raw observation の形式、detector rule、machine issue key の正本を確認したいときは `feedback_observation.md` を読む。
- `cmoc feedback report` の invocation report の内容・生成条件を確認したいときは `feedback_report.md` を読む。
- 一般的な report の表示内容だけを確認したいときは、state の atomic publication や cleanup を扱うこの文書ではなく、対応する report 仕様を直接読む。

## hash
- 1300fb4185b52ab193cee4ede8580842a48a3d621fa31e17491c889d62e15ad4

# `indexing.md`

## Summary
- cmoc がリポジトリ内の INDEX.md を自動配置・更新する仕組みと、その対象範囲を定義する文書。
- INDEX.md の目次情報に必要な構成、意味要件、ハッシュ計算、更新・自動コミットの規則を説明する。
- INDEX.md エントリー生成のための agent call、階層順序、並列実行、インデクシング実行条件を定める。

## Read this when
- cmoc の INDEX.md 配置対象や目次作成対象の範囲を確認するとき。
- INDEX.md のフォーマット、routing 情報の意味要件、ハッシュの扱いを確認するとき。
- インデクシングの更新判定、自動コミット、agent call の実行順序や並列化条件を確認するとき。

## Do not read this when
- 個別の INDEX.md エントリー本文の意味や、特定ファイルの責務を確認したいとき。
- cmoc の実装コードや oracle file の配置・責務を調査するとき。
- INDEX.md と無関係な機能の仕様・実装・テストを扱うとき。

## hash
- 4f941a6b5197a2ab9a7d306ddfdd5276cef1694432c620d5c67190a3d442a741

# `oracle_and_realization.md`

## Summary
- oracle file と realization file の責務を分類し、正本仕様・実装・テスト・補助ファイルの配置と所有範囲を判断するための責務境界を定義する。
- oracle doc と oracle src の正本責務、詳細仕様の委譲、相互の優先関係、および prompt literal・generated prompt の位置づけを確認する入口である。
- oracle file と realization file を扱う判断基準、関連仕様の参照方法、未定義部分の扱い、realization file の oracle file への適合性と修正対象を確認する。

## Read this when
- oracle file、realization file、uncategorised file の分類や、それぞれの配置・責務を判断するとき。
- oracle doc と oracle src のどちらが意味仕様、exact literal、schema、構築方法、選択値を所有するかを確認するとき。
- oracle file の調査・作成・変更・レビュー、または realization file の実装・テスト・適合性を扱うとき。
- realization apply や realization refactor で、明示仕様との不整合や実行不能・致命的バグが修正対象となるか判断するとき。

## Do not read this when
- 特定の prompt literal、schema、builder の構築順序・選択値を確認する場合は、委譲先として指定された oracle src を直接読む。
- 実装の具体的な責務や挙動を確認する場合は、対象の realization implementation を直接読む。
- テストの具体的な検査内容や実行方法を確認する場合は、対象の realization test または repository のテスト実行手順を直接読む。
- 既存 INDEX.md の内容を確認・更新する作業では、この対象をルーティング情報の代わりに読まない。

## hash
- 259e160b92793af0da335a17093c70cd22908522d827fc09943dcb5e5bbda94e

# `oracle_and_realization_file_enumeration.md`

## Summary
- oracle file と realization file の分類対象を、常時対象外 root・nested Git working tree・Git ignore 判定・oracle/realization の配置条件に基づいて定義する規範文書。doctor preprocess と realization refactor の refactor state 同期が利用する列挙結果の契約を扱い、traversal の pruning、非通常ファイルや symlink の扱い、repository 単位の ignore 判定性能不変条件、回帰検証要件への入口となる。

## Read this when
- oracle file または realization file の完全な列挙条件、対象外 subtree、nested repository、Git ignore の意味を確認するとき
- ファイル traversal、pruning 境界、symlink・非通常ファイルのエラー条件を実装または検証するとき
- doctor preprocess や realization refactor の refactor state 同期で、列挙結果や性能不変条件の根拠を確認するとき
- 分類結果の回帰 fixture や Git subprocess・ignore source・traversal 回数の検証条件を確認するとき

## Do not read this when
- 単一の oracle file または realization file の本文内容だけを確認したいときは、対象ファイルを直接読む
- INDEX.md のルーティング情報や文書構成だけを確認したいときは、該当する INDEX.md を読む
- 列挙・traversal・Git ignore・回帰検証に関係しない機能の仕様や実装を扱うとき

## hash
- 816b4fa3fe98ff0ee3f0a55d6123630f0198e52394d4cf3702191aaaaa78c8ba

# `prompt_editor_input.md`

## Summary
- オリジナルプロンプトを入力する editor work file のライフサイクルと、入力結果の保存・抽出・削除手順を定義する仕様書。editor work file と cmoc 管理の保存コピーを分離し、パス・regular file・symlink であることの検証後に一度だけ読み取る確定手順を扱う。
- エディタの選択順、起動条件、初期内容の構築元、および後続 agent が editor work file を参照しない境界を示す。prompt skeleton や完全 prompt の構築自体は builder と各サブコマンド仕様が担うため、それらを確認する入口ではなく、editor input の入出力 lifecycle を確認するための文書である。

## Read this when
- オリジナルプロンプトの editor work file の作成、編集後の検証、一回読み取り、保存コピーへの保存、コメント除去、work file 削除または失敗時の保持を実装・変更するとき。
- 利用するエディタ、editor input の初期内容、work file と保存記録の責務分離、または後続 agent の参照制約を確認するとき。
- editor input からオリジナルプロンプトを確定する処理の安全性や lifecycle を調査するとき。

## Do not read this when
- 完全 prompt skeleton や agent call ごとの prompt 構築仕様そのものを確認するときは、各 builder および該当サブコマンド仕様を直接読む。
- editor input の保存記録や oracle 実装の正本を確認するときは、本文が参照する対応する oracle source または app specification を直接読む。
- editor work file の内容を保存記録として参照する運用や、editor lifecycle と無関係な prompt 編集を扱うとき。

## hash
- 3cded0fa35e4a6458acbb63845dc40a9841f91cd5bfc6899ee12853309ebde1e

# `run_isolation.md`

## Summary
- run の fork から join または abandon までのライフサイクル、workload ごとの隔離作業の扱いを定義する仕様。
- run のブランチ、linked worktree、agent call の作業コンテキスト、および成果物の merge・破棄方法を定める。
- run-root 外に保存できる cmoc 管理データと、join・abandon 時の feedback state の扱いを示す。

## Read this when
- run の開始・終了、fork・join・abandon の要否や関係を確認するとき。
- run のブランチ、worktree、agent call の cwd・path context、成果物の記録方法を扱うとき。
- run-root 外への書き込みや、session 側の cmoc 管理データ・feedback state の扱いを判断するとき。

## Do not read this when
- run の隔離ライフサイクルや作業領域を扱わず、個別 workload の実装・編集手順だけを確認したいとき。
- feedback の保存形式・状態遷移そのものを確認したいときは、feedback observation または feedback state の仕様を直接読む。
- agent call の path context の詳細な導出規則だけを確認したいときは、指定された codex_exec_rule を直接読む。

## hash
- 5f6c50cbadea16e905e296b1a738dd6f972860ac47ead4c209911d5c055abc03

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
- cmoc の主要サブコマンド仕様を集約したディレクトリ。doctor、indexing、oracle 操作、realization の編集 run、session lifecycle、feedback report、TUI などの正本仕様へのルーティング入口として機能する。各ファイルは個別コマンドまたは共通 lifecycle の実行条件、処理手順、状態遷移、報告・終了要件を扱う。

## Read this when
- cmoc のサブコマンド仕様を横断的に探すとき
- doctor、indexing、oracle、realization、session、run、feedback、TUI のいずれかのコマンド挙動を確認・変更・レビューするとき
- 個別コマンドの正本仕様へ進む入口や、複数コマンドに共通する編集 run lifecycle を確認するとき

## Do not read this when
- 特定サブコマンドの実装詳細、prompt 構築、agent call パラメータ、永続化契約などを直接確認したい場合は、該当する個別正本ファイルへ進むとき
- サブコマンドに共通するが別ディレクトリで定義される oracle・realization 関係、feedback 保存、run 隔離、中断、テスト・設計規則だけを確認したいとき

## hash
- 5a6478e0791a6ef58ee203a3ed5999ab145c281643cedce956d193831a4850f3

# `subcommand_interruption.md`

## Summary
- cmoc の中断可能サブコマンドに対するユーザー中断要求（Ctrl+C）の共通仕様を定める文書。中断対象の範囲、処理単位の停止、確定済み部分結果の保持、state 更新、primary report と terminal result の保存・出力、中断後の再開方針を確認するための入口となる。個別サブコマンドの詳細やログ・通知形式は、本文が参照する個別仕様および共通仕様へ進む。

## Read this when
- Ctrl+C によるユーザー中断を正常系として設計・実装・レビューするとき
- 中断可能サブコマンドの対象範囲や、中断時の結果・state・report の扱いを確認するとき
- 中断後に同じ run を再開できるか、新しい run や fork が必要かを判断するとき

## Do not read this when
- 特定サブコマンド固有の中断時 state や report 保存形式だけを確認するとき
- ログ形式、エラー処理、Windows toast 通知などの詳細だけを確認するとき

## hash
- 1695e21c641e63d7de727bfc19095fa695223e72e7b844f146664e76fd25bf5e

# `timestamp.md`

## Summary
- タイムスタンプ文字列の正規フォーマットと、各構成要素の桁数・ゼロ埋め規則・ローカルタイムゾーンを定義する仕様文書。タイムスタンプの生成・解析・検証条件を確認する際の入口となる。

## Read this when
- タイムスタンプの文字列表現、各フィールドの桁数、ゼロ埋め、ミリ秒精度、タイムゾーンの扱いを確認するとき。

## Do not read this when
- タイムスタンプの具体的な生成処理や呼び出し箇所を実装・調査するときは、まずその実装対象を直接読む場合。

## hash
- 76873df5347a74035c75e23ec5ae779eec11c2741a6234fc754ab5e503a9c40e

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
- Windows 11 上の WSL2 から Windows toast 通知を行う仕様。cmoc の非対話サブコマンドの terminal result と、TUI の agent turn 完了を通知対象とし、通知境界・状態分類・重複排除を定める。
- 通知内容の必須情報、秘密情報やフルパスの除外、Codex CLI callback 設定の呼び出し単位管理、および未検証の外部契約を正本仕様に断定しない方針を定める。
- 外部 module や新規 Python package に依存しない Windows toast transport の安全な受け渡し、有限時間、通知失敗時の本命処理への非干渉、自動補完プローブでの無効化条件を定める。
- 具体的な callback interface と transport 方式は realization に委ねられるため、仕様の境界を確認したうえで実装・外部契約検証へ進むための入口となる。

## Read this when
- Windows toast 通知機能を実装、変更、または仕様適合性レビューするとき。
- cmoc tui、cmoc oracle investigation、その他の最外側末端サブコマンドに通知境界を適用するとき。
- terminal result の分類、TUI turn の完了通知、callback の重複排除、または通知失敗時の非干渉を確認するとき。
- WSL2 からの toast transport、自動補完プローブ、Codex CLI の通知 callback 外部契約を扱うとき。

## Do not read this when
- terminal result の共通分類や primary report の確定条件だけを確認するときは、console_and_file_log.md を直接読む。
- ユーザー中断要求の成立条件や完了処理だけを確認するときは、subcommand_interruption.md を直接読む。
- 具体的な callback 設定 key、event、payload、発火保証の検証結果を確認するときは、検証済みの外部契約資料または対象実装を直接読む。

## hash
- 1160a9c967d32a54499d7c991062f44bc2e8973e2cf1a3cfe81b5fb495205456
