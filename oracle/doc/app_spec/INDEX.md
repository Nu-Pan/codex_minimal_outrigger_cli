# `cli_auto_completion.md`

## Summary
- `_CMOC_COMPLETE` が存在する呼び出しを自動補完用プローブとして扱うための境界と規則を定める。
- 自動補完処理より前に cmoc 通常実行向けの前処理・検査・副作用を行わず、補完に必要な出力だけを許可する。

## Read this when
- 自動補完用プローブで通常実行向けの前処理・検査・副作用を抑止する条件を確認するとき
- 自動補完用プローブの stdout/stderr 出力制約を確認するとき
- 通常の cmoc 実行と CLI ライブラリの補完処理との境界を確認するとき

## Do not read this when
- Windows toast 通知に固有の自動補完プローブ境界だけを確認したいとき
- サブコマンド未指定判定、カレントディレクトリ変更、session/run 状態検査、ログ作成、INDEX 更新、cmoc 形式のエラーレポートなど、通常実行時の個別規則だけを確認したいとき

## hash
- 5984f914f917b5166222542c4723e63cd36412462c22c9e76f7862c766e5f755

# `codex_exec_rule.md`

## Summary
- Codex CLI 呼び出し全体の正本規約。agent call の path context、引数・sandbox・provider 設定、prompt の受け渡し、ログ、Structured Output、quota・retry・並列実行・失敗処理など、cmoc が `codex exec` を起動・管理する際の横断的な契約を定める。

## Read this when
- `codex exec` または `codex exec resume` の起動処理を実装・変更するとき
- agent call の cwd、worktree root、sandbox、file access policy、provider/model/reasoning effort の扱いを確認するとき
- prompt、MCP reporter、ログ、session ID、Structured Output の補正・検証を実装するとき
- quota 枯渇、レート制限、モデル容量超過、その他の Codex CLI 失敗時の処理を確認するとき

## Do not read this when
- 個別 agent call の意味上の責務や判断基準だけを確認したいときは、対応する oracle doc を直接読む
- `AgentCallParameter` の正確な field 定義・型・既定値だけを確認したいときは、指定された builder の正本を直接読む
- Codex CLI 呼び出しを伴わない機能の仕様や、単独の実装コード品質を確認するとき

## hash
- 987af56ac9b1b2bc5d4d7ff866b1eb819d74682f28dbda18f5402203e658d3f8

# `codex_model_provider.md`

## Summary
- agent call 種別ごとに model provider ID、Model 名、Reasoning Effort 名を直接設定し、Codex CLI の argv へそのまま渡す仕様を定義する。
- provider 定義 mapping と provider-local 設定の扱い、未知の設定を起動前にエラーとする条件、および secret を保存しない制約を定義する。
- cmoc は provider の取得・起動・管理や応答品質・認証を保証せず、model provider 設定以外の prompt・sandbox・通知設定は変更しない。

## Read this when
- agent call 種別に応じた model provider、Model、Reasoning Effort の設定方針を確認するとき
- provider ID、provider-local 設定、未知の provider の扱い、または Codex CLI 起動前の検証範囲を確認するとき
- cmoc が model provider に対して担う責務と担わない運用・保証範囲を確認するとき

## Do not read this when
- CodexCallConfig、CodexModelProviderConfig、CmocConfigCodex の具体的な field 名・型・既定値を確認したいとき
- agent_call_kind から Codex CLI の argv へ設定を反映する詳細規則を確認したいとき
- prompt、sandbox、file access policy、network access、通知設定の一般的な仕様だけを確認したいとき

## hash
- 861ec8aa33a7e3c8bdd04cdc715ba222522cbce11dfce8374e40989c3511a373

# `console_and_file_log.md`

## Summary
- 非対話サブコマンドの console、primary report、サブコマンドログ、terminal result に関する共通契約を定める正本。
- 自然言語・実行 ID・時間・パスの表示規則、出力先、primary report の掲載内容、terminal result の分類と確定順序、JSON Lines ログの記録要件を扱う。
- TUI、自動補完、内部呼び出しとの境界と、本書が要求しない表示・通知・機械可読形式の範囲を確認する入口。

## Read this when
- 非対話サブコマンドの stdout/stderr、進行通知、primary report、terminal result、終了コードの共通挙動を確認または変更するとき。
- サブコマンドログの保存先、JSON Lines 形式、即時 flush、診断イベントの記録要件を確認するとき。
- TUI・自動補完・内部サブコマンド呼び出しに対する primary report や terminal result の適用境界を確認するとき。

## Do not read this when
- 個別サブコマンド固有の result、completion_reason、primary report の内容・保存先・終了コードだけを確認するときは、そのサブコマンド仕様を直接読む。
- Windows toast の対象・順序・内容・失敗時の扱い、または自動補完の固有判定規則を確認するときは、各専用仕様を直接読む。
- エラー分類や internal failure の詳細な扱いだけを確認するときは、error_handling.md など該当する正本仕様を直接読む。

## hash
- c7d09d785792ea2646c187273261ace3c0626694bef4bd56d41783a6f68b2841

# `doctor_preprocess.md`

## Summary
- 日本語技術文書の INDEX.md 用エントリー生成として、対象の責務と下位の検証・修復内容への入口を簡潔に示します。

## Read this when
- 各サブコマンドの本命処理前に、cmoc 共通の検証・修復、追跡状態の保証、または reporter/client の事前互換性確認を調べるとき。
- `.cmoc/gu`、`.agents`、設定・refactor state の git 追跡保証や、doctor preprocess 後に個別サブコマンドの事前条件へ進む境界を確認するとき。

## Do not read this when
- 特定サブコマンド固有の事前条件や本命処理だけを確認したいとき。
- git clean 状態の検査、または reporter/client の詳細な正本仕様そのものを直接確認したいとき。

## hash
- 3b9e9a959bd2ea84d72aec222e8808ce7c99d63637c11189112fe3be4278a23f

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
- handled failure と internal failure の分類、エラー終了の確定、primary report・terminal result・サブコマンドログの共通契約を定めるエラー処理の正本。
- エラー種別ごとの表示規則、スタックトレースの保存・表示条件、正常結果およびユーザー中断要求との境界を確認する入口。
- 個別仕様に特別なエラー処理の指定がない場合に適用する共通規則を扱う。

## Read this when
- エラーが handled failure または internal failure のどちらに該当するか判断するとき
- エラー終了時の state 確定、rollback、後処理、primary report 保存、terminal result 確定の順序を確認するとき
- handled failure と internal failure の console、stderr、サブコマンドログにおけるスタックトレースおよび診断情報の扱いを確認するとき
- attention、incomplete、completed_with_unresolved、またはユーザー中断要求をエラーとして扱うべきか確認するとき
- 個別仕様に特別なエラー時の指定がない場合の共通ルールを確認するとき

## Do not read this when
- console と terminal result の出力先、表示順序、共通 field の詳細だけを確認するとき
- ユーザー中断要求の詳細な正常系処理だけを確認するとき
- 特定サブコマンド固有の state、rollback、report、次の操作、終了コードの指定だけを確認するとき

## hash
- a6ea2d366264052db800d4378e5d339f474267d17c29049a157d6b53c78fab63

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
- feedback observation の報告基準、agent-facing reporter interface、受け入れ検査、collector transport、call lifecycle、機械的 log detector の初期 rule、raw observation の保存・durability・retention を定める正本仕様。

## Read this when
- feedback observation をいつ報告すべきか、reporter の入力・結果・拒否条件を確認するとき。
- collector が context を確定し、observation を保存・無効化する経路や call 終了処理を変更するとき。
- 構造化 log から machine observation を検出する rule、threshold、issue key を追加・変更するとき。
- raw observation のファイル単位、idempotency、publication 前後の保持・cleanup、pending warning の扱いを確認するとき。

## Do not read this when
- feedback observation の issue identity、remediation の可否、現在状態そのものを判断するとき。
- prompt への正確な agent 向け文面や完全 prompt の配置だけを変更するときは、本文が委譲する prompt builder の正本を直接読む。
- report cut や remediation wave の集約・threshold 判定だけを扱うときは、該当する report 処理の仕様を直接読む。

## hash
- c6ec761df96b576b74040ac045e81ec88dd2b84c76101212d9bfea8e98173e50

# `feedback_state.md`

## Summary
- feedback remediation run が使用する repository-local state の正本。active generation、current pointer、run manifest、immutable intake wave、high-watermark、checkpoint、report cut、publication completion、incomplete report、および atomic publication・cleanup の責務と整合条件を定義する。

## Read this when
- feedback state の配置、artifact の役割、active issue と threshold 未満 aggregate の保持規則を確認するとき
- intake wave、高水位境界、checkpoint、report cut、publication または cleanup の順序と不変条件を実装・検証するとき
- 正常 publication、incomplete 診断、run join・abandon 後の state 保持を確認するとき

## Do not read this when
- raw observation の収集規則や detector rule 自体を確認するときは feedback_observation の正本を読む
- feedback report の call 回数、intake wave loop、incomplete 条件、正常 publication の詳細手順を確認するときは feedback_report の正本を読む
- 編集 run の join・abandon に関する共通仕様だけを確認するときは editing_run の正本を読む

## hash
- de856108b7f7bb4ef869151ad581f6b39e8c07e6cd40a5f3458ebbff5c2782ca

# `indexing.md`

## Summary
- `{{work-root}}` における `INDEX.md` の配置対象、目次対象、記載構成、ハッシュ計算、更新・自動コミットの仕様を定義する正本仕様。
- インデクシングを深いディレクトリから処理する規則と、目次情報を独立した agent call で生成する単位・並列実行条件・実行タイミングを定める。
- `INDEX.md` を routing 情報として利用する際の意味要件と、対象本文の代替にしない境界を示す。

## Read this when
- `INDEX.md` の自動生成・更新・削除条件を確認するとき
- インデクシング対象のディレクトリやファイル、ハッシュの算出方法を確認するとき
- 目次情報生成の agent call、処理順序、並列化、実行タイミング、自動コミットの仕様を確認するとき
- `INDEX.md` の Summary、Read this when、Do not read this when に求められる routing 情報の意味要件を確認するとき

## Do not read this when
- 特定のファイルやディレクトリの実装内容・仕様内容を調べるだけで、`INDEX.md` の生成や routing の規則を確認する必要がないとき
- 個別の `INDEX.md` エントリー本文を作成する際に、対象ファイルの内容から責務や読む条件を判断でき、インデクシング全体の仕様を参照する必要がないとき
- 実際の対象本文の最新状態や詳細を確認する必要があるとき

## hash
- 1f56b1b17e5e13169a4895399e7b7cbe485d9d8aada7d017e9bab3d992edcd9e

# `oracle_and_realization.md`

## Summary
- oracle file と realization file の分類、正本責務、優先関係、および相互の適合性判断を定義する共通契約の入口。oracle doc・oracle src・oracle test と realization implementation・test・ancillary の役割分担を確認できる。
- 正本仕様の委譲、prompt literal との関係、未定義部分の扱い、仕様と実装の不整合を修正対象とする基準を扱う。

## Read this when
- oracle と realization のどちらが仕様・実装・テストを所有するか判断するとき
- oracle doc から oracle src へ委譲された exact literal、構築方法、選択値、schema の優先関係を確認するとき
- realization file を仕様へ適合させる作業の対象範囲や修正根拠を確認するとき
- 関連する oracle file や installed skill の扱い、未定義部分の補完境界を決めるとき

## Do not read this when
- 具体的な prompt の構築順序・文面・rendering・schema の定義だけを確認したい場合は、委譲先の oracle src を直接読むとき
- realization implementation、test、または ancillary の具体的な実装内容だけを調べる場合は、該当する realization file を直接読むとき
- 個別のアプリケーション要求や判断基準を確認する場合に、この共通契約だけで完結しないときは、対応する oracle doc を読むとき

## hash
- 19bdfd485f73ff97bdec11f8f6209f6e9d56e80c337fd76c019025599d8b80a5

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
- cmoc workflow における session と編集 run のライフサイクル、およびそれらを永続化する state のスキーマと状態遷移を定める仕様。
- session の active context、編集 run 開始、session 終了、join・abandon に共通する事前条件を確認するための入口。
- session と run の各 field の意味、初期値、workload 種別、自動 join・recovery を含む状態遷移を確認する対象。

## Read this when
- session state の JSON 構造、保存対象、各状態や field の意味を確認したいとき。
- session fork、編集 run、join、abandon、feedback report の状態遷移や事前条件を実装・検証するとき。
- apply の追従対象 commit や feedback state の責務分担を確認するとき。

## Do not read this when
- feedback の repository-local state の保存対象や lifecycle 自体を確認したいときは、feedback state の正本仕様を直接読む。
- apply 後の hook における last_joined_apply_fork_commit の更新規則を確認したいときは、realization apply の正本仕様を直接読む。
- oracle edit 固有の仕様や、個別 workload の詳細な処理手順だけを確認したいとき。

## hash
- 952da2b406d2dee7b88866e693ce53b39ee6010760e358d5b34675286c7e63b1

# `sub_command`

## Summary
- cmoc のサブコマンド仕様への入口。doctor、indexing、tui、oracle・session・run の各操作、および feedback report に関する実行契約・ライフサイクル・終了報告を扱う。
- サブコマンド固有の実行条件や処理手順を確認するための上位入口であり、共通する編集 run lifecycle、session lifecycle、branch、state、prompt builder、realization・oracle の詳細仕様へ案内する。

## Read this when
- cmoc のサブコマンドの呼び出し条件、実行手順、状態遷移、agent call、差分処理、cleanup、または primary report の仕様を調べるとき。
- doctor、indexing、tui、feedback report、oracle edit・investigation、realization apply・refactor、session fork・join・abandon、run join・abandon のどの仕様から読み始めるべきか判断するとき。

## Do not read this when
- 特定サブコマンドの内部処理、state schema、branch・run isolation、prompt 構築、realization・oracle の適合性、feedback state などの詳細だけを確認したいときは、対応する正本仕様を直接読む。
- サブコマンド以外の一般的な実装構造や、既存の実行結果・診断ログだけを確認したいとき。

## hash
- ec57c9c16ea29afa49a33e201ad53200651c9cb97ab2e12b8b34f05e928729a0

# `subcommand_interruption.md`

## Summary
- 対象は、ユーザーの Ctrl+C による中断要求を正常系として扱うサブコマンド共通仕様の入口であり、中断可能サブコマンドの範囲、通知、確定済み結果の保持、完了報告、再開・join/abandon の扱いを確認するために読む。
- `realization refactor fork` または `feedback report` の中断時の共通動作や、個別仕様へ進む前の中断処理の全体像を確認する際に使う。

## Read this when
- 中断可能サブコマンドの対象範囲や追加条件を確認するとき。
- Ctrl+C の受け付け、finalization 区間、処理単位の停止・完了、primary report と terminal result の保存・出力要件を確認するとき。
- ユーザー中断後の refactor run の扱い、feedback report の joinable 状態、publication・cleanup・再開可否の共通境界を確認するとき。

## Do not read this when
- 中断対象が `realization refactor fork` または `feedback report` に限定され、個別サブコマンドの state・checkpoint・publication 手順だけを確認したいときは、それぞれの個別仕様を直接読む。
- 通常完了や一般的なエラー処理、通常のログ保存・console 出力の規則だけを確認したいときは、対応する個別仕様または `console_and_file_log.md` を直接読む。

## hash
- 46b74e94867381fa209f59fc8c458cc5950299955eb909d9cdba362827339b8e

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
- Windows 11 上の WSL2 から表示する toast 通知の適用範囲、通知境界、内容、発火条件、安全な transport、自動補完時の抑止条件を定義する正本仕様。
- 非対話サブコマンドの terminal result と TUI の agent turn 完了を通知する際の重複排除、失敗時の非干渉、Codex CLI 設定境界を確認する入口。

## Read this when
- サブコマンドまたは TUI の Windows toast 通知を追加・変更するとき
- 通知対象の lifecycle event、terminal result の分類、turn ごとの重複排除を確認するとき
- Codex CLI callback の設定境界や未検証 interface の扱いを判断するとき
- WSL2 の通知 transport、自動補完プローブ、通知失敗時の扱いを確認するとき

## Do not read this when
- 通知仕様の確認を要しない具体的な realization 実装だけを調べるとき
- 通知と無関係な console/file log、割り込み、または一般的な Codex CLI 呼び出し仕様を確認するとき

## hash
- bcb50e63f23dac9adc42205d47ab494cdc9ac3ea18c5d44ff168296bc5749278
