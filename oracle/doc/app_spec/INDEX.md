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
- Codex CLI を用いた agent call の呼び出し契約を定める文書。呼び出し単位の path context、環境変数、preflight、CLI 引数上書き、sandbox と詳細なファイルアクセス制限、prompt・Structured Output・ログ・session の扱い、並列実行、失敗時の retry・待機・終了規則を扱う。Codex 呼び出しを実装・変更・検証する際の横断的な契約入口であり、個別 agent call の意味上の責務や判断基準は対応する oracle doc から確認する。

## Read this when
- cmoc が `codex exec` または `codex exec resume` の起動方法、引数、環境変数、sandbox、approval、model、provider、reasoning effort を実装・変更・確認するとき
- agent call の cwd、worktree・repository root、placeholder、ファイルアクセス制限、並列実行の扱いを判断するとき
- prompt の stdin 渡し、Structured Output の schema・検証・補正、session ID、stdout・stderr・output・call log の保存規則を扱うとき
- Codex CLI の quota 枯渇、一時的な capacity エラー、Structured Output 検証失敗などのエラー処理を実装・確認するとき

## Do not read this when
- 個別 agent call の意味上の責務、作業範囲、判断基準だけを確認する場合は、対応する workload 固有の oracle doc を直接読む
- path context の厳密な型定義や prompt の共通構築・rendering を確認する場合は、本文が委譲する `path_model.py`、`basic.py`、`complete_prompt.py`、`struct_doc.py` を直接読む
- feedback observation の reporting 意味や collector・transport の詳細だけを確認する場合は、`feedback_observation.md` とそこから参照される正本を直接読む
- Windows toast notification の effective configuration や callback 検証条件だけを確認する場合は、指定された `windows_toast_notification.md` を直接読む

## hash
- 65ac2793894eff318c132a28bf19105a8d013dad7f01d7b5d810ee0fbdf1c339

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
- 非対話サブコマンドの console 出力、primary report、terminal result、サブコマンドログに関する共通契約の正本。自然言語・時間・パスの表示規則、stdout/stderr の責務、終端分類と確定順序、report 保存、JSON Lines ログ、TUI・自動補完との境界、non-goal を定義する。
- 個別サブコマンド仕様が定める result、completion_reason、report の詳細や終了コードを補完する共通ルールへの入口であり、出力・ログ・完了処理の横断的な挙動を確認する際に読む。

## Read this when
- 非対話サブコマンドの stdout/stderr、進行通知、terminal result の表示契約を確認または変更するとき
- primary report の保存条件・表示方法、終端分類、終了処理の順序を確認するとき
- サブコマンドログの保存先、JSON Lines 形式、flush、診断イベント要件を確認するとき
- TUI と非対話サブコマンドの通知境界、自動補完との関係を確認するとき

## Do not read this when
- 個別サブコマンド固有の result、completion_reason、report 本文、終了コードだけを確認する場合は、そのサブコマンド仕様を直接読む
- TUI の正常終了後の通知や Windows toast の詳細だけを確認する場合は、指定された TUI・toast の正本仕様を直接読む
- エラー分類・internal failure の処理だけを確認する場合は、error_handling.md を直接読む

## hash
- 488c3d2c418c33c4ded0c1f7bfd6aa7650485dbf5530a783c1a58b6b0900d5eb

# `doctor_preprocess.md`

## Summary
- cmoc の各サブコマンド本命処理に先立ち、リポジトリと共通管理状態の検証・修復を担う仕様書。gitignore、追跡状態、refactor state の同期、feedback reporter/client の事前互換性確認、および修復で生じた tracked 差分の commit を扱う。
- サブコマンド固有の事前条件や git working tree・staging area の clean 状態は扱わず、共通検証が必要な処理の入口として下位の修復・検証仕様を確認する際に参照する。feedback reporter/client の利用不能時は degraded warning として本命 workload を継続する境界も定義する。

## Read this when
- doctor preprocess の実行順序、共通の検証・修復責務、エラー終了条件を確認するとき
- `.cmoc/gu`、`.agents`、agent routing 設定、refactor state の git 追跡・同期要件を実装または検証するとき
- feedback MCP reporter/client の事前検証、protocol 不一致時の degraded 扱い、warning と構造化 event の要件を確認するとき
- doctor preprocess 後に個別サブコマンドが検証すべき事項との責務境界を判断するとき

## Do not read this when
- doctor preprocess 共通処理ではなく、特定サブコマンド固有の事前条件や本命処理の仕様だけを確認するとき
- git working tree または staging area の clean 状態の検査仕様を確認するとき
- refactor state の詳細な schema や oracle・realization file の列挙規則そのものを確認するときは、それぞれの正本仕様を直接読むとき
- feedback observation の reporter interface や protocol の詳細契約を確認するときは、feedback observation の正本仕様を直接読むとき

## hash
- 6b81243275084b0f4d7e944e9f083dff3403d91c4cf90f6eb2cdcef87be09d01

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
- cmoc の feedback subsystem 全体の目的・処理モデル・正本仕様の分担・既存 workload との境界・non-goal を定義する概要仕様。agent または allowlist 済み detector が収集した raw observation を、report 実行時に issue candidate として正規化・検証し、unresolved のみを通常 report と active state に反映する。
- verification が inconclusive の場合は normal publication を行わず、確定判定と判定不能理由を incomplete 診断 report として提示する。feedback は本命 workload の成功判定、state、retry、recovery から独立している。
- observation の収集、repository-local state と atomic publication、feedback report の実行手順・判断・表示は、それぞれ指定された下位の正本仕様への入口として整理されている。

## Read this when
- feedback observation の収集経路、受け入れ検査、raw 保存の全体像を確認するとき
- feedback report が issue candidate をどのように正規化・検証し、normal または incomplete report を公開するかを理解するとき
- feedback と既存 workload、run state、retry、recovery、後続 Codex call の境界を確認するとき
- feedback 関連の下位仕様へ進む前に、責務分担と共通原則を把握するとき

## Do not read this when
- observation の具体的な報告基準・収集 API・machine detector・raw 保存だけを確認したい場合は feedback_observation.md を直接読む
- repository-local state、report cut、checkpoint、atomic publication、cleanup の仕様だけを確認したい場合は feedback_state.md を直接読む
- cmoc feedback report の事前条件、処理順序、normalization、verification、表示、終了結果だけを確認したい場合は sub_command/feedback_report.md を直接読む
- feedback と無関係な workload の成功判定、run/session/TUI 完了結果、一般的な realization や oracle の作業を確認する場合

## hash
- 0162d33fcf58c4ee20677f7746bb2f21d42a1fc0c11c29e0326e93dd2514dd12

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
- oracle file と realization file の分類、正本責務、相互の優先関係、および適合性判断の共通契約を定義する文書。oracle doc・oracle src・oracle test、realization implementation・test・ancillary の役割を区別し、仕様の委譲、重複禁止、実装追従時の判断基準を示す。oracle と realization の責務境界や、関連する prompt builder・policy の詳細へ進むための入口となる。

## Read this when
- oracle file と realization file の役割や分類を判断するとき
- oracle doc と oracle src の正本責務、委譲、優先関係を確認するとき
- realization implementation・test・ancillary の配置と責務を確認するとき
- realization の仕様適合性や修正対象の判断基準を確認するとき

## Do not read this when
- 対象となる個別 oracle doc、oracle src、oracle test、realization file の具体的内容を直接確認すれば足りるとき
- prompt の正確な文面・構築方法・選択値を確認するときは、指定された oracle src を直接読むとき
- cmoc 固有の開発環境、設計、テスト実行手順だけを確認するときは、対応する dev_rule 文書を直接読むとき

## hash
- 8ab0718841213c60c572383f63c048c374d30c71f2460c5aa416197b43ffb862

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
- `prompt_editor_input.md` は、ユーザーが入力したオリジナルプロンプトを editor work file で確定し、保存コピーと呼び出し元向けプロンプトへ分離する lifecycle の正本である。初期内容の構築委譲先、work file と保存領域の役割、エディタ起動条件、検証・一度だけの読み取り・保存・コメント除去・削除の確定手順を扱う。

## Read this when
- editor work file の生成、編集完了後の検証、最終読み取り、保存コピー作成、コメントブロック除去、work file 削除の挙動を確認するとき
- prompt editor の初期コメントや template、またはサブコマンドへ渡すオリジナルプロンプトの構築責務を確認するとき
- `.cmoc/gu/aw/editor_input` と `.cmoc/gu/ar/log/editor_input` の役割分離や、後続 agent の参照境界を確認するとき

## Do not read this when
- editor lifecycle や入力確定手順ではなく、完全 prompt skeleton・抽出後 prompt の具体的な構築仕様を確認するときは、各 agent call の builder または該当するサブコマンド仕様を直接読む
- editor 起動処理そのものではなく、一般的な TUI 共通仕様や oracle 調査・oracle 編集の個別仕様だけを確認するときは、それぞれの正本仕様を直接読む

## hash
- 4b8f093bfabe83b72a8d411c36896fb20565a8e8d3b304909f4be11313c93455

# `run_isolation.md`

## Summary
- run の fork から join または abandon までの作業隔離とライフサイクルを定義する正本仕様。run とサブコマンドの関係、branch・worktree 上での成果物管理、明示的 join が必要な編集 run と対象外の read-only 調査・機械更新などの境界を扱う。
- run の branch、worktree、永続 state、ログ、feedback state などを定義する別の正本仕様への参照起点として機能する。

## Read this when
- run の fork・join・abandon のライフサイクルや、編集 run と read-only run の扱いを確認するとき
- run の branch、worktree、agent call の cwd/path context、成果物の merge・破棄規則を確認するとき
- run 作業における run-root 外への書き込み例外や、ログ・session state・feedback state との境界を確認するとき

## Do not read this when
- branch の具体的な命名や分岐元 commit の正本定義だけを確認したいときは branch model を直接読む
- 永続化される run field のスキーマだけを確認したいときは session state 仕様を直接読む
- ログ、feedback observation、feedback state の保存形式や lifecycle の詳細だけを確認したいときは、それぞれの参照先仕様を直接読む

## hash
- 4ba9dd896227ab938acecb1822ee3995f78db17e8b481447415b79d7af8bae77

# `session_state.md`

## Summary
- cmoc workflow における session と、明示的な join を必要とする realization 編集 run の lifecycle を定義する JSON state file。
- session の状態、fork 元 branch と commit、最後に join した apply run、および active run の kind・branch・fork commit を管理する。
- active session context の検証条件、編集 run の fork・join・abandon に共通する事前条件、run の状態遷移を確認するための入口となる。

## Read this when
- session state の JSON スキーマや初期値を確認するとき
- session の active・joined・abandoned・error の状態遷移を実装または確認するとき
- realization 編集 run の ready・running・joinable・error と、kind・branch・fork commit の扱いを確認するとき
- session fork、run join、run abandon の事前条件や完了時の state 初期化を確認するとき

## Do not read this when
- feedback の repository-local state の保存対象や lifecycle を確認するときは、feedback_state.md を直接読む
- oracle edit の run ではない扱いを確認するときは、該当する oracle edit の仕様を直接読む
- session/run state を参照せず、別の workload 固有処理だけを確認するとき

## hash
- 963d5e02d0f5c832382b1f0ae4129cb28af61a65fa8f6a1cf1bdb3752f40804b

# `sub_command`

## Summary
- cmoc の主要サブコマンドおよび編集・session lifecycle、feedback report、indexing、TUI の正本仕様へのルーティング入口。各文書は、対応するコマンドや共通処理の引数・事前条件・実行手順・状態遷移・report・エラー処理と、より詳細な正本仕様への境界を定義する。

## Read this when
- cmoc のサブコマンド、session や編集 run の lifecycle、feedback report、indexing、TUI の挙動を確認・実装・変更するとき
- コマンド実行条件、agent call、branch/worktree、state、report、終了経路、cleanup の仕様について、対象サブコマンドの入口を探すとき
- 複数のサブコマンドに共通する編集 run の join・abandon、または session の fork・join・abandon の仕様を確認するとき

## Do not read this when
- 特定サブコマンドの詳細仕様、agent prompt や Structured Output schema、state schema、branch model、共通エラー・中断規則など、本文が示す下位の正本を直接確認すべきとき
- INDEX.md の生成規則や realization file の具体的な実装内容だけを確認するとき
- 対象サブコマンド以外の一般的な git 操作や、session・run・feedback の正本定義そのものだけを確認するとき

## hash
- 03e5fd2749b406bf468957ed1d59a41d0bbd75ae340de90ada913dc8a4073ccc

# `subcommand_interruption.md`

## Summary
- 中断可能なサブコマンドにおけるユーザー中断の適用範囲、Ctrl+C の通知処理、確定済み部分結果の扱い、primary report・state・terminal result の保存と出力を定める仕様。中断後の各サブコマンド固有の再開境界や state は、列挙された個別仕様への入口として示す。

## Read this when
- 中断可能サブコマンドへ Ctrl+C によるユーザー中断を実装・変更するとき
- ユーザー中断時の正常終了、部分結果の確定、後処理、ログ・console 出力、再開可否を確認するとき
- realization refactor fork、oracle review、feedback report の中断後の扱いを調べるとき

## Do not read this when
- 中断をサポートしないサブコマンドの通常動作だけを確認するとき
- 特定サブコマンドの中断後 state や再開境界の詳細を確認する場合は、本文からリンクされる個別仕様を直接読むとき
- サブコマンド共通の保存・出力形式そのものを確認する場合は、console_and_file_log.md を直接読むとき

## hash
- 4fab277fe60d8ab609821085d135a6454ac040124dd7fde44e8ba9c4bc4cefcd

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
- cmoc の初回準備、セッション開始から oracle 編集・realization 実行・run の取り込みまたは破棄・セッション統合までの標準 workflow を案内する利用手順書。各 workload の使い分けと共通 lifecycle を確認する入口でもある。

## Read this when
- cmoc を初めて呼び出すとき
- cmoc session fork/join、oracle edit/review、realization apply/refactor、run join/abandon の一連の進め方を確認するとき
- realization apply・realization refactor・oracle edit の使い分けや共通 lifecycle の参照先を確認するとき

## Do not read this when
- 特定 workload の目的や詳細仕様だけを確認したいときは、本文から直接案内される各 workload の正本仕様を読むとき
- oracle investigation の調査方法など、この手順書が概要として扱っていない個別機能を確認するとき

## hash
- 87076b42190c9593aa3c8750d6ee477de7017ae5a3bf178e2cef7dcf728adc45

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
