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
- cmoc が Codex CLI を呼び出す際の実行契約を定める正本文書。agent call と Codex call の単位、call-scoped な cwd・root・path context、環境変数、preflight、argv による設定上書きを扱う。
- Codex CLI の sandbox、詳細なファイルアクセス制限、permission profile の禁止、model/provider/reasoning effort の指定、prompt の構築・受け渡し、ログ保存、stdout/stderr、session ID の取得を規定する。
- Structured Output の schema 保存・検証・補正 turn・差分不変性・補正不能時の扱い、および並列呼び出し、quota 枯渇、サーバー一時不調、想定外エラー時の実行制御を定める。
- feedback reporter と collector context の登録・分離・終了処理、利用不能時の扱いも含み、Codex 呼び出し実装が従うべき app spec・oracle src への委譲境界を示す。

## Read this when
- Codex CLI の exec または exec resume 呼び出しを実装・変更・レビューするとき。
- agent call の cwd、worktree、root placeholder、sandbox、file access mode、model/provider、prompt、ログの扱いを判断するとき。
- Structured Output の schema 指定、機械的検証、同一 session での補正、retry、quota 待機、並列実行を実装・調査するとき。
- cmoc_feedback reporter の呼び出し単位 context、capability、受付終了・drain・無効化の設計を確認するとき。

## Do not read this when
- 対象が Codex CLI 呼び出し規約ではなく、個別 agent call の意味上の責務や判断基準を定める oracle doc の内容だけを確認するときは、対応する oracle doc を直接読む。
- prompt の共通構築順序や rendering、file access policy、path model、feedback observation の正確な実装仕様を確認するときは、本書の委譲先である対応する oracle src または正本 app spec を直接読む。
- INDEX.md の更新や一般的なリポジトリ案内だけが目的で、Codex CLI の実行契約に関係しないとき。

## hash
- ab5b6a5f13701079c677fdcd1be05f80095f645e5414f2c8f82099936ef84593

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
- cmoc の feedback subsystem 全体の目的、処理モデル、正本仕様の分担、共通原則、既存 workload との境界、non-goal を定義する概要仕様。
- 観測を pending observation として収集し、report cut 後に issue candidate の同一性・現在性・actionability を検証する流れと、normal publication／incomplete 診断 report の分岐を示す。
- 詳細な observation 収集、repository-local state、feedback report サブコマンドの仕様へ進むための入口となる上位文書。

## Read this when
- feedback subsystem の目的や全体処理モデルを把握したいとき
- observation、issue candidate、active issue、report cut、normal publication、incomplete 診断 report の関係を確認したいとき
- feedback 関連の正本仕様の責務分担や、既存 workload との境界を判断するとき
- feedback report の挙動が本命 workload の成功判定、state、retry、recovery に与える影響を確認したいとき

## Do not read this when
- observation の報告基準、収集経路、受け入れ検査、machine detector、raw 保存の詳細を確認したいときは feedback_observation.md を直接読む
- repository-local state、report cut、checkpoint、atomic publication、cleanup の詳細を確認したいときは feedback_state.md を直接読む
- cmoc feedback report の事前条件、処理順序、normalization、verification、表示、終了結果の詳細を確認したいときは sub_command/feedback_report.md を直接読む
- 実装詳細、テスト方法、または個別 issue の検証を確認したいとき

## hash
- 1e40358c79852dccc449786aa3ee9ec8f71ec88918e0980eabd285a2e193a2b8

# `feedback_observation.md`

## Summary
- feedback observation の報告基準、agent-facing MCP interface、受け入れ検査、collector/transport の境界、call lifecycle、machine log detector の allowlist・issue key、raw observation の保存・durability・retention を定める正本仕様。feedback の issue 同一性や現在状態の判断は扱わず、実装・運用仕様から確認を始める入口となる。

## Read this when
- agent や collector による observation 報告、受け入れ検査、secret masking、path/capability 検証を変更・確認するとき
- cmoc_feedback の reporter/client、collector IPC、call-scoped context、保存経路、call 終了処理を設計・実装するとき
- structured log の machine observation 検出、初期 allowlist rule、recurrence threshold、machine issue key を変更・確認するとき
- raw observation のファイル形式、atomic な durable 保存、publication 後 cleanup、pending warning の挙動を変更・確認するとき
- feedback に関する他仕様や実装の適合性を確認するため、報告から保存・検出・retention までの全体契約を参照するとき

## Do not read this when
- feedback observation の issue 集約、同一性、現在状態、report cut、current pointer の詳細を直接確認する場合は、該当する feedback report または issue 状態の仕様へ進むとき
- prompt に埋め込む agent 向け報告文面の正本や complete prompt への配置を確認するだけの場合は、指定された prompt builder の正本を直接読むとき
- Structured Output の input schema や reporter tool の機械的な入出力項目だけを確認する場合は、本文で参照される schema または interface 定義を直接読むとき

## hash
- db6f3e414fc8efc3c0965b931aacd6718c6845d7a0c9ee16937c8e6f496a2d8d

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
- cmoc がリポジトリ内の INDEX.md を自動配置・更新するための仕様を定義する文書。配置対象の除外規則、目次情報の構成、ハッシュによる鮮度確認、深いディレクトリからの処理、生成用 agent call、並列化条件を扱う。

## Read this when
- INDEX.md の自動インデクシングの対象範囲や除外条件を確認するとき。
- 目次情報の形式・意味要件・ハッシュ計算方法を確認するとき。
- インデクシングの処理順序、差分コミット、生成 agent の起動条件、並列実行条件を変更または検証するとき。

## Do not read this when
- 特定の実装の詳細や CLI の責務境界を確認したい場合。
- テストの追加・変更方針や実行手順だけを確認したい場合。
- INDEX.md の個別エントリー本文を確認する場合は、対象階層の INDEX.md または対象本文を直接読む。

## hash
- 73392d00b1aedb69538ad9e80cbe4143f6eccc81e15542b730708fede08e7588

# `oracle_and_realization.md`

## Summary
- oracle file と realization file の責務・分類・配置先を定義し、oracle doc/src/test と realization implementation/test/ancillary の役割を整理する正本仕様。
- 正本責務の重複禁止、oracle doc から oracle src への委譲、責務に基づく優先関係、oracle・realization の判断基準、realization の適合性判定を定める。関連する分類仕様、prompt 構築規則、実装・テスト作業の入口となる。

## Read this when
- oracle file と realization file の責務、分類、配置先を確認するとき
- oracle doc と oracle src の正本責務、委譲範囲、優先関係、重複禁止を確認するとき
- oracle file を扱う判断基準、realization file の作成・変更基準、または oracle file への適合性を判断するとき

## Do not read this when
- 個別の prompt literal、schema、builder の構築順序や選択値だけを確認したいときは、委譲先の oracle src を直接読む
- prompt literal の役割・制限や cmoc の実行規則だけを確認したいときは、該当する codex 実行規則を直接読む
- oracle と realization の分類・責務・適合性に関係しない個別仕様を確認するとき

## hash
- 9faf4b339fe03a40577ff8a0a575f2fa97eb1aae1544dbbb1ac4e05c7ca630f7

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
- プロンプト編集用の一時ファイルについて、入力内容・生成責務・保存コピーとの分離・エディタ起動・検証、保存、コメント除去、削除までのライフサイクルを定義する仕様書。prompt 構築の正本や editor work file の扱いを確認する入口となる。

## Read this when
- editor input の初期コメントや template の構築責務を確認するとき
- editor work file の配置、検証、読み取り、保存コピー、コメント除去、削除の確定手順を変更・調査するとき
- 起動エディタの優先順位や `--wait` 要件を確認するとき
- 編集済み入力からオリジナルプロンプトを確定する仕様を確認するとき

## Do not read this when
- 完全 prompt skeleton や抽出後の完全 prompt の構築仕様だけを確認したいときは、各 agent call の builder または指定されたサブコマンド仕様を直接読む
- editor lifecycle や prompt 文面の正本ではない実行時生成物を確認したいとき
- editor input と無関係なサブコマンド、CLI 実装、テストの仕様を確認するとき

## hash
- 3f1eb66d98f87a8635b1159b905cc2a52660245e5e7ede35de04614ec06e1278

# `run_isolation.md`

## Summary
- run の fork から join または abandon までのライフサイクル、workload と run の関係、成果物の記録・取り込み規則を定義する。
- run branch と linked worktree の作成・利用、および agent call の path context を扱う。
- run-root 外への書き込みが許可される cmoc 管理データと、join・abandon 時の feedback state の扱いを示す。

## Read this when
- run の fork、join、abandon のライフサイクルや、明示的な join が必要な編集 run の扱いを確認するとき。
- run の branch、worktree、agent call の作業場所や path context を決めるとき。
- run-root 外への書き込み例外、実行ログ・session state・feedback state の保存先と lifecycle 操作時の扱いを確認するとき。

## Do not read this when
- read-only の investigation や review の一般的な進め方だけを確認するとき。
- cmoc の機械的更新や session join の conflict 解消自体の手順を確認するとき。
- run の隔離や lifecycle に関係しない CLI の仕様、実装責務、テスト規則を確認するとき。

## hash
- d96b5373fb02298665a3f05c635ef19568039fb4a71a31869404754d319f510c

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
- cmoc のサブコマンド単位の正本仕様を集約するディレクトリ。doctor、indexing、oracle／realization、session／run、feedback、TUI などのコマンド契約と、関連する実行・報告・状態遷移への入口を提供する。

## Read this when
- cmoc の特定サブコマンドの引数、事前条件、実行手順、終了経路、primary report、状態遷移を確認するとき
- 複数のサブコマンドにまたがる仕様の入口を探すとき
- doctor preprocess、indexing、agent call、fork／join／abandon、feedback report など、サブコマンドの挙動を変更・実装・レビューするとき

## Do not read this when
- 個別サブコマンドの詳細仕様が明確な場合は、このディレクトリ全体ではなく該当する仕様書を直接読むとき
- サブコマンドから参照される共通仕様、個別 builder の実装、保存済み report の実例、raw feedback schema などだけを確認したいときは、それぞれの直接の正本・実装対象へ進むとき
- cmoc のサブコマンド以外の仕様や、一般的な Git 操作だけを確認するとき

## hash
- 1306244d4cb8c22f1d458b7a1cbfc7920a850f7396c000733b6bde9cc7176de2

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
