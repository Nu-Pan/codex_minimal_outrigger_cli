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
- 非対話サブコマンドの console、primary report、terminal result、JSONL 診断ログに共通する出力契約を定める。実行 ID・時間・パスの表示、進行通知と診断記録の責務、および TUI と自動補完での適用境界を扱う。

## Read this when
- 非対話サブコマンド共通の console 出力先や表示内容、実行 ID・時間・パスの書式、進行通知、terminal result の確定順序や表示項目を変更するとき。
- primary report の共通掲載内容や、Structured Output と feedback observation の report 内での表示を変更するとき。
- サブコマンドの JSONL 診断ログの記録内容・flush、回復待ちの追跡、TUI 送信元情報との対応を変更するとき。

## Do not read this when
- 個別サブコマンド固有の結果、report の形式や保存先、次の操作、終了コードを確認・変更するときは、そのサブコマンドの仕様を直接読む。
- Codex call の実行条件、Structured Output の受理・補正、回復待ちや再開の判断を変更するときは、それらを定める Codex 呼び出し規則を直接読む。この文書は primary report 内での表示方法を扱う。
- TUI 通知の内容・発火条件や、自動補完プローブ固有の出力抑止を変更するときは、それぞれの境界を定める仕様を直接読む。
- ログ名に使う timestamp の構文を確認・変更するときは、タイムスタンプ形式の仕様を直接読む。

## hash
- adb8a86c45b45fc795edf7cbe5a7940b1d369ee13610625eed441daece87817e

# `doctor_preprocess.md`

## Summary
- 各サブコマンドに共通する、本命処理前の検証と可能な修復を定める。git 追跡状態や refactor state の同期、reporter/client の事前確認をまとめ、修復で生じた tracked 差分の commit も扱う。
- reporter/client が利用できない場合の degraded warning と処理継続も定める。コマンド固有の事前条件は対象外。

## Read this when
- 本命処理の開始前に cmoc が何を検証・修復し、どの条件でエラー終了または処理継続するかを確認するとき。
- 共通の追跡保証、refactor state の同期時点、reporter/client の事前確認を変更するとき。

## Do not read this when
- 個別コマンドの事前条件や working tree・staging area の clean 要件を確認するときは、対象コマンドの仕様へ直接進む。
- feedback MCP の protocol 契約、refactor state の schema・entry 同期の詳細、merge conflict 時の責務を確認するときは、それぞれの正本仕様へ直接進む。

## hash
- 5776a52b3700f67ee537196d414f8bce5c1f795286ff0ba7df6d40e53d8c61f5

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
- feedback subsystem の目的、共通用語と結果分類、既存 workload との境界を定める。
- 観測収集、repository-local state、CLI report の詳細仕様へ責務を振り分ける、feedback 全体の入口。

## Read this when
- feedback issue の結果分類や正常 publication と incomplete 診断の使い分けを確認するとき。
- 既存 workload の成果が observation になる条件や、feedback が他の workload に及ぼす影響を確認するとき。
- feedback の要求が観測収集、state、report のどの仕様責務に属するか判断するとき。

## Do not read this when
- agent observation の報告基準、受け入れ検査、detector、raw 保存の詳細だけを調べるときは、feedback observation の収集仕様へ進む。
- active issue、intake wave、checkpoint、current pointer、publication、cleanup の詳細だけを調べるときは、feedback state の仕様へ進む。
- `cmoc feedback report` の実行手順、agent call、merge、表示、終了結果の詳細だけを調べるときは、feedback report の仕様へ進む。

## hash
- 101ff455edc774a92b037732d9fd4a9c342da3e52df21e1dff1f2fbc766ef6ba

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
- feedback remediation run が使う repository-local active state と immutable artifact の役割、保持境界を定める。
- active issue から intake wave・high-watermark、checkpoint・report cut、publication、cleanup・recovery まで、永続化と参照整合性を確認する入口。

## Read this when
- active issue と threshold 未満の machine aggregate の保持内容や、state の所有単位を確認・変更するとき。
- intake wave、high-watermark、checkpoint、report cut の固定条件や、run の recovery に必要な state を調べるとき。
- 正常 publication・incomplete 診断 report の保存、current state の切替、処理済み artifact の cleanup と失敗後の復旧条件を調べるとき。

## Do not read this when
- observation の報告基準、受付・検査、MCP transport、detector、raw observation の保存を調べるときは、observation 収集仕様から読む。
- feedback report の事前条件、normalization、remediation call、wave loop、利用者向け report と終了結果を調べるときは、コマンド固有仕様から読む。
- feedback 全体の目的、用語、結果分類、処理モデルを確認するときは、feedback の概要仕様から読む。
- 編集 run 共通の join・abandon と lifecycle を調べるときは、編集 run の共通仕様から読む。

## hash
- cf33a074e6eee3fc16a8f43b0eadd58941291e68225be95179316405856f77be

# `indexing.md`

## Summary
- `{{work-root}}` 配下の `INDEX.md` を cmoc が配置・生成・更新する際のルールを定める仕様です。対象の選定、目次情報の意味要件、ハッシュによる再生成、処理順序、並列実行、preflight、join 中の管理を扱います。

## Read this when
- `INDEX.md` の配置場所や掲載対象、目次情報の要件を変更・確認するとき。
- インデクシングの処理順序、更新・コミット条件、生成の並列実行、preflight、join 中の連携を変更・確認するとき。

## Do not read this when
- 通常作業で既存の `INDEX.md` を使って読む本文を選ぶだけのときは、目次情報に従って対象の本文へ進んでください。
- 明示的な indexing コマンドの実行手順だけを知りたいときは、そのコマンドの手順を定める仕様を参照してください。
- agent に渡す目次情報生成 prompt の具体的な内容や起動パラメータを変更するときは、それを組み立てる実装を直接参照してください。
- oracle edit の実行順序や join の競合解消責務だけを確認・変更するときは、それぞれの手順・責務を定める仕様を直接参照してください。

## hash
- 99a714eb44e3749cfd7e1ac80ff528205bfc402a3382037a0ff6bdf06eb14f6a

# `merge_conflict_resolution.md`

## Summary
- 複数の join 方式に共通する内容競合の判断基準を定める入口。両 branch の変更意図と oracle に基づく統合、必要な付随編集・検証、agent と cmoc の責務分担、受理と報告の考え方を扱う。
- 個別コマンドの編集範囲や復旧手順、管理物の処理、agent に渡す正確な文面は、それぞれのコマンド仕様や実装に委ねる。

## Read this when
- run join、自動 join、session join で内容競合が起き、両側の意図をどう統合し、初期の競合一覧外を含む付随編集や検証をどう扱うか確認するとき。
- 競合解消 agent と cmoc の責務境界、完了判断、受理条件、報告に含める根拠を確認するとき。

## Do not read this when
- 特定の join の編集範囲、失敗時の復旧、post-join、publication などのコマンド固有動作だけを調べるときは、そのコマンドの仕様を読む。
- 競合が INDEX.md や refactor state など cmoc 管理物だけに限られるときは、indexing または refactor state の管理仕様を読む。
- 競合解消 prompt の正確な文面や構築、provider・model の設定を確認するときは、該当する prompt builder 実装や設定を読む。

## hash
- c7e930f9781e7b0fddcd62c25119b9fd8edf6ad454d60779c6527964bdfdf909

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
- run を workload ごとの隔離作業単位として定義し、サブコマンドの invocation との違いを含む共通 lifecycle と、branch・worktree 上での作業関係を説明する。
- 複数 workload に共通する run の隔離境界を確認する入口。状態の永続化や詳細なアクセス規則は、それぞれの正本仕様へ委ねている。

## Read this when
- 作業が run に当たるか、複数 invocation にまたがるか、同一 invocation 内で join できるかを判断するとき。
- workload 共通の run lifecycle や、隔離された branch・worktree と agent call の作業場所との関係を確認するとき。
- run 上の作業と cmoc による管理処理の境界を把握するとき。

## Do not read this when
- 特定 workload やサブコマンド固有の事前条件、差分検査、report、join・abandon の処理を確認するときは、その workload または lifecycle の仕様へ進む。
- branch・commit・worktree の正確な命名や配置を確認するときは、branch model の仕様へ進む。
- 永続 state の保存先、field、状態遷移を確認するときは、session state の仕様へ進む。
- agent call の正確な path context や詳細なファイルアクセス制限を確認するときは、Codex 呼び出し規約へ進む。

## hash
- e336f54de3916bce8e03b3c7c825bb38c3453fb0fdac416ba14995e0ef9eb55a

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
- 個別サブコマンドの目的、引数、事前条件、実行手順、変更権限、状態管理、失敗時の扱い、報告を定める仕様群です。
- 編集 run の共通 lifecycle と、各 workload 固有仕様との責任分担も扱います。

## Read this when
- 特定のサブコマンドの契約や実行・失敗時の動作を実装、変更、または適合確認するとき。
- realization apply/refactor、feedback report、run の join/abandon で、workload 固有処理と共通 lifecycle の関係を確認するとき。
- session lifecycle、oracle の編集・調査、TUI、doctor、indexing のコマンド固有動作を確認するとき。

## Do not read this when
- 調べたいのが branch や session state、file 分類、indexing、doctor preprocess、prompt 構築など共有契約そのものだけなら、その契約を定義する仕様へ直接進んでください。

## hash
- 30ff18fa4ef63046c5bf5c3f0be62e87bb4f662c42b3e548d1249626c45fa8db

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
