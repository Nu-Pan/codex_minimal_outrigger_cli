# `cli_auto_completion.md`

## Summary
- `_CMOC_COMPLETE` 環境変数がある呼び出しを自動補完プローブとして扱い、補完処理前の通常実行向け処理と、補完に不要な標準出力・標準エラーを抑止する境界を定める。
- Windows toast 通知に固有の補完時ルールは、専用仕様へ委ねる。

## Read this when
- CLI の起動経路を変更するとき、自動補完プローブの判定や補完前に抑止すべき通常処理を確認する。
- 補完プローブ中の標準出力・標準エラーの制約を確認するとき。

## Do not read this when
- 自動補完時の Windows toast 通知の初期化、transport 検査、warning の扱いを確認するときは、`windows_toast_notification.md` を読む。
- 通常実行時の console ログや report の出力規則を確認するときは、`console_and_file_log.md` を読む。
- session/run 状態や INDEX 更新そのものの要件を確認するときは、それぞれの仕様を読む。

## hash
- 19a87ab36b08cee626abd4da7ef2d29e708e381fa9990323519ee6f00db6cb96

# `codex_exec_rule.md`

## Summary
- 複数の agent call に共通する Codex CLI の起動条件、path context、sandbox と詳細なファイルアクセス制限を定める。
- prompt の受け渡しと責務の境界、Structured Output の受理・補正、並列実行、失敗時の回復規則を確認する入口となる。
- 個々の agent call の目的や判断基準ではなく、Codex CLI 実行を支える共通規則を扱う。

## Read this when
- Codex CLI の共通起動設定、実行環境、ファイルアクセス境界を変更・確認するとき。
- prompt に含める内容の境界や、Structured Output の正式な受理・補正条件を確認するとき。
- quota 枯渇や一時障害を含む Codex call の失敗分類、待機、再開を検討するとき。

## Do not read this when
- 特定の agent call の目的、作業範囲、意味上の判断基準だけを確認するときは、その call の作業仕様を参照する。
- model provider、Model、Reasoning Effort の設定値や責務境界だけを確認するときは、provider 設定の仕様を参照する。
- 正確な引数構造、prompt の組み立て・描画、path 導出の実装を確認するときは、それぞれを所有する実装を参照する。
- console 表示や診断ログの保存形式だけを確認するときは、表示・ログの仕様を参照する。

## hash
- 166a4ba2c8ecb7baddc6866094143b762e38b91ea70e096cc83b097741757c81

# `codex_model_provider.md`

## Summary
- 通常の agent call ごとに設定された provider ID、Model、Reasoning Effort を直接使い、別名変換・fallback・互換性判定を行わない規則を定める。
- provider-local 設定の要件と、一時障害の回復確認 probe が停止中の呼び出しで確定した設定を引き継ぐ例外を定める。
- provider 設定を Codex CLI に渡すまでの cmoc の責務境界を示し、実際の CLI 呼び出し規則へ案内する。

## Read this when
- 通常の呼び出しで provider、Model、Reasoning Effort をどう選び、設定が不足した場合にどう扱うか確認するとき。
- provider ID と provider-local 設定の対応付けや、その値に関する制約を定める・変更するとき。
- 一時障害の回復確認 probe がどの設定と認証適用先を引き継ぐか、quota 待機時の probe とどう区別するか確認するとき。
- provider に関する cmoc の責務範囲を確認するとき。

## Do not read this when
- 設定データ構造の正確な field 名・型・既定値を確認するときは、設定実装を直接読む。
- Codex CLI の argv への反映や呼び出し中の設定維持、失敗後の待機・再開規則を確認するときは、Codex 実行規則を直接読む。
- provider の導入・運用・診断・直接疎通や、provider-local 設定・認証要件の意味を調べるとき。この文書はそれらの手順や保証を扱わない。

## hash
- d81b0aff42367a14e32d9a0367ee01f90d59cdee6e69a70e4521ca2e96eede62

# `console_and_file_log.md`

## Summary
- 非対話サブコマンドに共通する console、primary report、terminal result、サブコマンドログの契約を定め、個別サブコマンド仕様や TUI・自動補完との適用境界を示す。

## Read this when
- 非対話サブコマンドで stdout と stderr の役割、進行通知、表示形式の共通規則を確認するとき
- primary report や terminal result をいつ確定し、何を表示・記録するかを確認するとき
- サブコマンドログの診断要件や、TUI・自動補完に対する共通契約の適用範囲を確認するとき

## Do not read this when
- 個別サブコマンド固有の result、completion_reason、report の形式・保存先・内容、次の操作、終了コードだけを調べるときは、そのサブコマンド仕様を直接読む
- TUI の通知判定、Codex の回復待ち判断、feedback observation の検出・保持条件など、参照先の個別規則だけを調べるときは、その規則の仕様を直接読む

## hash
- 2acec05eba06fdd4282bd97a3fdee737825b3da2c1382fc370608cfdf4e9bd8a

# `doctor_preprocess.md`

## Summary
- 各サブコマンドの本命処理前に共通実行する doctor preprocess の検証・修復範囲と失敗時の扱いを定める。
- 追跡・非追跡の保証、refactor state の同期時点、feedback reporter/client の事前検査、tracked 差分の commit を調べる入口。

## Read this when
- サブコマンド共通の事前検査・修復や、その実行順序を確認または変更するとき。
- preprocess における reporter/client の起動・protocol 検査と、利用不能時に本命処理を続ける扱いを確認するとき。

## Do not read this when
- `cmoc doctor` 固有の primary report の保存条件や記載内容だけを調べるときは、doctor コマンドの仕様へ進む。
- feedback observation の agent 向け報告条件、MCP interface、受け入れ検査、transport、保存仕様を調べるときは、feedback observation の仕様へ進む。
- refactor state の JSON schema や entry 集合の同期規則そのものを確認するときは、realization refactor の仕様へ進む。

## hash
- db70bf2db665438f032491cdd4dbfc50a5aa63492f5294662ee4b54bc53ffaa1

# `editor_input_handoff.md`

## Summary
- Codex TUI から待機中の prompt editor input へ依頼を渡す handoff の仕様を定める。active target の lifecycle、ガイド取得と上書き、agent の手順・権限・失敗時の扱いを確認する入口。
- 共通の editor input・file access・送信元情報の規定を前提に、handoff 固有の責務と関連仕様の境界を示す。

## Read this when
- 人間の明示要求と target ID に基づく handoff の設計や挙動を確認するとき。
- ガイド取得から依頼作成・送信までの agent の責務、参照情報、失敗時の扱いを確認するとき。

## Do not read this when
- 一般的な prompt editor input の確定方法、ファイルアクセス制限、Codex TUI への MCP 注入、送信元情報の記録だけを変更・確認するときは、それぞれの共通仕様を直接読む。
- ガイドや agent 向け指示の正確な文面、MCP 入出力の具体的な定義、本文の構築や参照表記の詳細だけを確認するときは、それらを定義するソースを直接読む。

## hash
- c0d22c3cc3b64aca8c9157466c57f080cbdf7a05ff0546d19abbcaaad43d0e3a

# `error_handling.md`

## Summary
- エラー終了における handled failure と internal failure の分類、およびスタックトレースの共通規則を定める正本。個別仕様に特別な指示がない場合の共通エラー処理を確認する入口。

## Read this when
- エラー終了の分類や確定方法、handled failure と internal failure の共通表示・スタックトレース規則を確認するとき。
- 個別仕様にエラー時の特別な指示がない場合に、共通規則を確認するとき。

## Do not read this when
- コンソールと terminal result の出力先、表示順序、共通 field を確認するとき。
- Codex CLI の回復待ちの可否や終了条件を確認するとき。
- ユーザー中断時の扱いを確認するとき。
- 特定サブコマンドの state、rollback、report、次の操作、終了コードの規則を確認するときは、そのサブコマンドの個別仕様から読む。

## hash
- 5be1589b159f55673b8aa806bb251dcb24129c629488bd9099703f3cc60ddb8b

# `feedback.md`

## Summary
- feedback subsystem 全体の目的、共通用語と結果分類、実行モデル、および他の workload との境界を定める。
- observation の収集、repository-local state、`cmoc feedback report` の詳細仕様へ進むための意味上の入口となる。

## Read this when
- feedback issue の結果分類、正常 publication と `incomplete` 診断の違い、人間対応が必要となる条件など、subsystem 全体で共有する意味を確認するとき。
- どの情報源が observation になり得るか、feedback が他 workload の成否や state に与える影響、および各 feedback 仕様の責務分担を確認するとき。

## Do not read this when
- agent による報告基準、MCP 受け入れ検査、collector、detector、raw observation の保存や retention を調べるときは、observation 収集の仕様から確認する。
- repository-local artifact、intake wave、checkpoint、publication point、cleanup、state recovery の詳細を調べるときは、feedback state の仕様から確認する。
- `cmoc feedback report` の実行手順、normalization、remediation call、join、report 表示、終了結果、中断やエラー処理を調べるときは、report command の仕様から確認する。

## hash
- 892e1f5b1104895e5becf3c7c1665538fe9933a76bff6776ed054a913fa56603

# `feedback_observation.md`

## Summary
- agent observation の報告基準、MCP reporter の公開範囲と受入検査、call 単位の collector context・transport を定める。
- 構造化 log からの detector と raw observation の保存・保持通知を定める、観測収集段階の仕様。

## Read this when
- observation を報告できる条件、reporter の入力互換性や受入・拒否条件を確認するとき。
- call 単位の context と collector の lifecycle、agent・machine observation の収集経路を確認するとき。
- 構造化 log の検出 rule、raw observation の耐久保存や pending 件数の通知条件を確認するとき。

## Do not read this when
- feedback 全体の目的、用語、結果分類を知りたい場合は、feedback の概要と用語を定める文書から読む。
- repository-local state、issue identity、intake wave、checkpoint、publication、cleanup を確認する場合は、state の仕様を読む。
- feedback report の CLI、normalization、remediation、commit、merge、結果公開の手順を確認する場合は、report command の仕様を読む。

## hash
- f979d5a735572c121079cebbe36caf1f971f9737a96ac5c3304b1773c446a358

# `feedback_state.md`

## Summary
- feedback remediation が使う repository-local active state の保持内容と、正常 publication によって current state を確定する仕組みを定める。
- immutable な wave、checkpoint、report cut の保存、排他制御、再開、publication、cleanup を扱うため、feedback state の永続化や復旧の判断で参照する。

## Read this when
- pending observation、active issue、run artifact の保持・更新・削除や、それらの整合性を変更するとき。
- 中断後の再開、join 後の publication、current state の切替、または cleanup の動作を確認するとき。
- feedback state の保存先、耐久性、hash 検証、writer 排他の扱いを確認するとき。

## Do not read this when
- observation の報告基準、収集経路、受け入れ検査、detector rule、raw observation の保存を定めるときは、feedback observation の収集仕様を読む。
- CLI の事前条件、normalization、agent call、issue remediation の順序、report の内容・表示、終了結果を調べるときは、feedback report の command 仕様を読む。
- feedback 全体の結果分類や処理モデルを確認するときは共通 feedback 仕様を、一般的な run の join・abandon を確認するときは編集 run の共通仕様を読む。

## hash
- 468afed690bdbf9a62b19435e6cff957892fc6e24ac6791dc9966bbacb6d3d59

# `indexing.md`

## Summary
- cmoc が INDEX.md を配置・更新する共通規則と、目次情報の意味要件、生成・並列化・コミットの扱いを定める仕様です。
- 明示的な indexing コマンドや oracle edit が利用する、全体のインデクシング動作を確認する入口です。

## Read this when
- どのディレクトリや項目をインデクシングするか、目次情報をどんな routing 情報にするか、いつ生成・再生成・コミットするかを確認するとき。
- agent call の並列実行範囲や、自動 preflight を含む共通処理と呼び出し元の責務分担を確認するとき。

## Do not read this when
- 明示的な `cmoc indexing` の引数、事前条件、実行手順、実行報告だけを確認するときは、そのコマンドの仕様を直接参照してください。
- oracle edit がインデクシングを呼び出す順序だけを確認するときは、oracle edit の実行順序を直接参照してください。
- 目次生成 agent call の正確な prompt 文面や起動パラメータを確認するときは、それらを構築する実装を直接参照してください。

## hash
- b1cfcd4f9e3ff2611b6ef03b3e96dde7c877d562bbc85c8593f4a6b8c40d21a8

# `oracle_and_realization.md`

## Summary
- oracle doc と oracle src の正本責務、委譲された詳細の扱い、両者が食い違う場合の判断基準を示す。
- 人間が所有する仕様と AI が作る realization の役割を分け、仕様から実装・テストを変更またはレビューする際の基準を示す。
- 適合性の所見を明確な仕様不整合や致命的な実装不具合に絞る基準を示す。

## Read this when
- ある仕様事項について oracle doc と oracle src のどちらを正本として扱うか、委譲範囲や両者の不整合を判断するとき。
- oracle file と realization file の責務を踏まえて、変更の置き場所や関連仕様の確認範囲を決めるとき。
- realization apply や refactor で、修正対象となる不適合や所見の根拠を判断するとき。

## Do not read this when
- 未追跡ファイルや ignore 判定を含む具体的なファイル分類だけを調べるときは、分類結果を定める関連仕様を直接読む。
- 委譲済みの prompt の正確な文面、構築方法、選択値、schema だけを変更・確認するときは、その詳細を所有する oracle src を直接読む。

## hash
- 552c55553d18986570ed95fb3ae1dfcf2d0c0450668e3216ddc62ed048f11275

# `oracle_and_realization_file_enumeration.md`

## Summary
- oracle file と realization file の列挙・分類契約を定め、Git ignore、nested repository、pruning、symlink、非通常ファイルの扱いを説明する。
- 列挙結果を保つための Git ignore 判定の性能条件と回帰検証の境界を定める。

## Read this when
- どのファイルを oracle file または realization file として列挙するか、分類結果が期待と異なる理由を確認するとき。
- 列挙時の traversal、pruning、nested repository、Git ignore、symlink、非通常ファイルの扱いを変更または調査するとき。
- doctor preprocess や realization refactor の同期で、列挙対象集合や path・hash・調査要求の意味を保つ必要があるとき。

## Do not read this when
- oracle file と realization file の基本的な責務や正本関係を確認するときは、両者の責務を定める文書から読む。
- doctor preprocess のうち列挙や refactor state の同期以外を扱うときは、その前処理の仕様を読む。
- realization refactor の処理手順や終了条件など、列挙・同期以外を扱うときは、そのサブコマンドの仕様を読む。

## hash
- 40ce795ffadbf355d93ad8abfbab7fa6de085bd06013b48ee0ba597c9ec0224c

# `prompt_editor_input.md`

## Summary
- オリジナルプロンプトを受け取る editor input の作成、編集待機、入力検証、確定保存までのライフサイクルを定める。
- 人間の直接編集と handoff による上書きを同じ確定手順につなぎ、確定後の入力の扱いと失敗時の復旧用ファイル保持を示す。

## Read this when
- エディタ入力の起動条件、編集中の本文の扱い、確定時の検証・読み取り・保存を確認するとき。
- 確定後に使う入力、失敗時の復旧、既存ログや旧配置の扱いを確認するとき。

## Do not read this when
- handoff の対象ライフサイクル、ガイドの生成・保持・取得・上書き、失敗時の責務を確認するときは、handoff 専用の正本仕様を読む。
- console 案内の正確な文面を確認するときは、その案内を構築する実装を読む。
- 完全 prompt skeleton や入力確定後の完全 prompt の構築を確認するときは、該当するサブコマンドの正本仕様を読む。

## hash
- 810c41249f4b7af561b6803c4d6e4adb9eecf965a26581136435c36ac3161a61

# `run_isolation.md`

## Summary
- run の隔離単位と workload を位置づけ、fork から join または abandon までの lifecycle と、run branch・worktree の利用規則を定める。
- run 上の agent call の path context、アクセス境界、cmoc による管理処理を示し、branch 定義や永続 state、ログ、feedback の詳細は個別仕様に委ねる。

## Read this when
- run の開始・終了方式や、1 回のサブコマンド呼び出しと run の関係を確認するとき。
- run の branch・worktree の使い方、agent call の path context、run 上のアクセス境界や cmoc 管理データの扱いを確認するとき。

## Do not read this when
- branch や worktree の命名・分岐元 commit・管理パスを確定するときは、それらを定義する仕様を直接読む。
- agent call の詳細な path 導出、ファイルアクセス権限、書き込み責任を調べるときは、それらを定義する実行規則を直接読む。
- 永続 state のスキーマ、ログや feedback の保存先・lifecycle、または特定 workload の完了・成果物取り込み規則を調べるときは、それぞれを定義する仕様を直接読む。

## hash
- 8361c9fb69ca4127a5e51a3ad71c61c01fbf8043e4a7b540784d7b22e810224f

# `session_state.md`

## Summary
- session と編集 run の永続 JSON 状態について、field の意味と初期値、共通事前条件、状態遷移を定める仕様です。
- コマンドや workload の実行手順ではなく、それらが参照する session/run 状態の定義と不変条件を確認する入口です。

## Read this when
- session/run 状態の構造、field の意味、許される値や初期値を調べるとき。
- active session の条件や、編集 run の開始・終了・join・abandon に伴う状態遷移を実装または確認するとき。
- feedback report の run 状態が自然完了、自動 join、recovery でどう遷移するかを確認するとき。

## Do not read this when
- feedback の repository-local state の artifact、保存・publication・cleanup の詳細だけを調べるときは、その state を定める仕様へ進んでください。
- 編集 run の fork、join、abandon の実行手順、差分検査、cleanup、report の詳細だけを調べるときは、共通 lifecycle 仕様へ進んでください。
- realization apply の追従範囲や、join 後に比較始点を更新する条件だけを調べるときは、apply の workload 仕様へ進んでください。

## hash
- ec7c9d9c8103ab3c0fef8ca67c374ba50a73e27996ff987a61d26a26e64020ac

# `sub_command`

## Summary
- cmoc の各サブコマンドの引数、事前条件、実行手順、状態や差分の扱い、終了結果を定める仕様群への入口です。
- 個別コマンドの仕様に加え、編集 run の開始・join・abandon に共通する lifecycle も扱います。

## Read this when
- doctor、indexing、TUI、oracle investigation/edit、realization apply/refactor、session lifecycle、feedback report の動作を確認または変更するとき。
- 編集 run の共通開始・終了条件や、個別コマンドと共通 lifecycle の関係を確認するとき。

## Do not read this when
- 単一コマンドの引数、事前条件、実行手順、終了動作だけを確認するときは、そのコマンドの仕様へ直接進んでください。
- CLI 全体のコマンド構成や登録を確認するときは、CLI 全体の仕様へ進んでください。
- session state、run isolation、prompt と agent call、file 分類、ログやエラー処理などの共通規則だけを確認するときは、それぞれの正本仕様へ直接進んでください。

## hash
- 621a80ce5ebb3bdd1463fd95f277509491154a727c6d73bd364f1bf5d9c7b777

# `subcommand_interruption.md`

## Summary
- 中断可能なサブコマンドに共通する、中断要求の受付範囲、処理停止、確定済み部分結果の保持、および完了処理を定める。
- 正常な中断完了を認める対象と、新たな対象を追加する条件を扱う。各コマンド固有の中断後の状態や次の操作は個別仕様に委ねる。

## Read this when
- Ctrl+C による中断を正常系で扱うサブコマンドの範囲や、共通の停止・完了動作を確認するとき。
- 中断要求と回復待ち・確認処理の優先関係、または中断できない finalization 区間を扱うとき。
- 新しいサブコマンドに中断完了を認める条件を検討するとき。

## Do not read this when
- refactor fork または feedback report の中断後の状態、保存内容、次の操作を決めるときは、該当コマンドの個別仕様を直接読む。
- 中断要求が論点に含まれず、一般的なログ出力、Codex CLI の回復待ち、エラー分類、または Windows toast の契約だけを確認するときは、それぞれの領域の仕様を直接読む。

## hash
- f6c9b45edee50bd7faee4fded3f9410f6eeae81c61ab9e7d92b017786b1d8699

# `timestamp.md`

## Summary
- プロジェクトで使うタイムスタンプの文字列表現と、基準にするタイムゾーンを定める。

## Read this when
- プロジェクトのタイムスタンプ出力を実装・変更するときや、その表記規則を確認するとき。

## Do not read this when
- 時刻の取得元や時計精度など、文字列表現以外の挙動を調べるとき。
- タイムスタンプと関係しない日付・時刻の表記を調べるとき。

## hash
- fdee683f00be4a26b05890895f8b4de3bf6d39a1ec7910a70edc96f4e2fbfc84

# `usage.md`

## Summary
- cmoc の初回準備から session の開始・終了まで、標準的な利用手順を案内する入口です。
- 短い仕様変更・実装変更の反復と、必要に応じたファイル単位の追従や feedback 報告の流れを示し、各 workload の詳細仕様へ案内します。

## Read this when
- cmoc を使い始めるとき、または session 全体の利用手順や workload の流れを確認したいとき。
- 仕様変更から実装反映、成果の取り込みまでの大まかな進め方を確認したいとき。

## Do not read this when
- 個別 workload の目的や実行規則を確認するときは、その workload の仕様を直接読んでください。
- 編集 run に共通する join・abandon などの lifecycle を確認するときは、共通 lifecycle の仕様を直接読んでください。

## hash
- c06672e712eb081c4728b10871c4e87e305670133f2cd6621cdddc1eb678d8ad

# `windows_toast_notification.md`

## Summary
- Windows 11/WSL2 で、最外側サブコマンドの terminal result と TUI の agent turn 完了を Windows toast で知らせる条件や境界を定める。toast 固有の通知仕様を確認・変更する際の正本。
- 通知内容、Codex CLI callback の設定と事前検証、transport の失敗時の扱い、自動補完時の抑止も扱い、共通の console 表示規則から toast 固有要件を切り分ける。

## Read this when
- Windows toast の対象となる処理、通知タイミングや重複排除、通知内容の制限を実装・レビューするとき。
- Codex CLI の TUI と codex exec で通知 callback をどう設定するか、実装前に何を検証するか確認するとき。
- toast transport の失敗が本処理へ及ぼす影響や、自動補完プローブ時の通知処理の抑止を確認するとき。

## Do not read this when
- terminal result の共通分類、primary report、console への表示順序を調べるときは、console_and_file_log.md を読む。
- cmoc tui または cmoc oracle investigation の起動条件や個別の処理手順を調べるときは、それぞれのサブコマンド仕様を読む。
- Codex CLI の一般的な呼び出し・回復動作を調べるときは codex_exec_rule.md を、toast に限らない自動補完規則を調べるときは cli_auto_completion.md を読む。

## hash
- cbe3d0bba1c661dc1b92c4d2876fb72fb85f82ed0fc122eae2badefd5d798d98
