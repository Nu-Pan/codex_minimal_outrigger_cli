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
- 各サブコマンドの本命処理前に行う共通の検証・修復、refactor state の同期時点、reporter の利用不能時の扱いを定める。
- 共通前処理が担う範囲を、個別サブコマンドの事前条件や専用処理と区別する。

## Read this when
- 本命処理前の共通検証・修復や、それに伴う差分の確定方法を確認・変更するとき。
- 共通前処理における refactor state の同期時点、または reporter の利用不能時の継続動作を確認・変更するとき。

## Do not read this when
- 明示的な doctor コマンドの実行手順や実行要約の保存を調べるときは、doctor コマンドの仕様を読む。
- 特定サブコマンド固有の事前条件や、working tree・staging area の clean 状態確認を調べるときは、そのサブコマンドの仕様を読む。
- feedback observation の報告基準、MCP interface、収集・保存 protocol を調べるときは、feedback observation の仕様を読む。
- refactor state の schema や entry 集合の同期規則を調べるときは、realization refactor の仕様を読む。

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
- feedback subsystem の目的と repair-first の公開方針を定め、自動修正後も人間の対応が必要な問題だけを正常な issue 一覧に残す。
- observation の発生源、結果分類、再確認の原則、既存 workload との境界、non-goal を横断的に示す。
- observation 収集、repository-local state、`cmoc feedback report` の詳細仕様へ案内する全体の入口となる。

## Read this when
- feedback subsystem の目的や、正常 publication と `incomplete` 診断の使い分けを確認するとき。
- observation の発生源、issue の結果分類、判定根拠の再確認、既存 workload との境界を確認するとき。
- 収集・state 管理・report 実行のどの仕様を参照すべきか判断するとき。

## Do not read this when
- agent observation の報告基準、reporter interface、受け入れ検査、log detector、raw 保存の詳細を確認するときは、observation 収集の仕様を読む。
- state artifact、intake wave、high-watermark、checkpoint、publication、cleanup の詳細を確認するときは、repository-local state の仕様を読む。
- CLI の事前条件、run の処理、remediation、join、表示、終了結果の詳細を確認するときは、`cmoc feedback report` の仕様を読む。

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
- feedback の repository-local active state における issue と machine aggregate の保持条件、record 構成、identity を規定する。
- collector の受理境界から intake wave・high-watermark・checkpoint・report cut を経て、publication・current pointer・cleanup と recovery へ至る永続化の整合性を定める。

## Read this when
- active issue や threshold 未満の machine aggregate の取込、再確認、昇格、保持条件を確認または変更するとき。
- feedback run の high-watermark、immutable artifact、checkpoint、report cut、publication、cleanup、失敗後の recovery の状態遷移を確認するとき。

## Do not read this when
- observation の報告基準、収集経路、raw 保存形式、機械 detector を確認するときは、観測収集の仕様から読む。
- 結果分類の意味や feedback 全体の処理モデル・完了条件を確認するときは、feedback の意味仕様から読む。
- CLI の事前条件、issue の処理順序、agent call、report 表示や終了結果を確認するときは、feedback report のコマンド仕様から読む。
- workload 共通の run join・abandon の規則を確認するときは、編集 run の共通仕様から読む。

## hash
- cf33a074e6eee3fc16a8f43b0eadd58941291e68225be95179316405856f77be

# `indexing.md`

## Summary
- 作業領域の目次情報について、配置・掲載対象、意味要件、生成と更新の仕組みを定める仕様書。
- 自動生成の順序や並列化、事前生成、マージ中の扱いを横断して確認する入口。コマンド固有の手順は各コマンド仕様が担う。

## Read this when
- どの内容を目次へ載せ、いつ再生成するかを判断するとき。
- 自動生成の順序や並列化、agent call 前の事前生成、マージ中の生成・commitの扱いを確認するとき。

## Do not read this when
- oracle 編集の正確な実行順序や、明示的なインデクシングの実行手順を確認するときは、それぞれのコマンド仕様を直接読む。
- 目次エントリー生成の正確な prompt 文面や起動パラメーターを確認するときは、その構築を担う実装を直接読む。
- マージ競合の解消方針や、各 join コマンド固有の条件・復旧手順を確認するときは、競合解消仕様または該当コマンド仕様を直接読む。

## hash
- 99a714eb44e3749cfd7e1ac80ff528205bfc402a3382037a0ff6bdf06eb14f6a

# `merge_conflict_resolution.md`

## Summary
- `cmoc run join`、feedback report の自動 join、`cmoc session join` で内容競合が起きた際の共通解消方針を示す。両側の意図と関連する oracle に基づく統合、検証、未解消事項の報告を扱う。
- agent の調査・統合・検証と、cmoc の staging・commit・管理 state 更新の責務分界を示し、各 join の報告で扱う判断根拠を定める。

## Read this when
- 対象の join で内容競合が起き、共通の解消基準、完了判断、agent と cmoc の責務分界を確認するとき。
- 両側の変更意図と関連 oracle を踏まえた統合方針や、付随編集・検証・未解消報告の判断基準を確認するとき。
- agent による内容の解消完了と、管理物の競合や staging 後の cmoc の確認を区別したいとき。

## Do not read this when
- run join 固有の編集範囲、取り込み、失敗時の復旧、post-join、cleanup を確認するときは、run join のコマンド固有契約を読む。
- feedback の封印後の調整・検証、publication、publication failure の扱いを確認するときは、feedback report のコマンド固有契約を読む。session join 固有の編集範囲や失敗時の扱いを確認するときも、session join の契約を読む。
- INDEX.md や refactor state の同期、prompt の正確な文面・構築、provider や model の設定を確認するときは、それぞれの管理仕様や実装の定義へ直接進む。

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
- run を workload 固有の隔離単位として扱う共通 lifecycle を定め、明示的な join を行う編集 run と self-joining workload の境界を示す。
- run worktree での作業場所、agent call の cwd、cmoc 管理データの扱いについて共通規則と参照先を示す。

## Read this when
- ある作業が明示的な join を要する編集 run か判断するとき。read-only investigation、cmoc 自身の機械的更新、session join の競合解消との境界も含む。
- run とサブコマンド invocation の関係や、run 上の作業場所と agent call の cwd を確認するとき。

## Do not read this when
- branch・commit・worktree の名前や導出規則を確認するときは、branch model を直接読む。
- session/run の永続 state の field、schema、遷移を確認するときは、session state の仕様を直接読む。
- 特定 workload の開始処理、想定差分、join・abandon・recovery の規則を確認するときは、共通編集 run と該当 workload の仕様を直接読む。
- agent call の path context 導出や詳細なファイルアクセス制限を確認するときは、Codex exec 呼び出し規約を直接読む。
- ログや feedback data の保存先・lifecycle を確認するときは、それぞれの専用仕様を直接読む。

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
- cmoc のサブコマンド別契約として、引数、事前条件、処理手順、終了報告を定める。doctor と indexing、TUI と oracle の調査・編集、session 操作、realization の apply・refactor、feedback report の仕様へ進む入口となる。
- 編集 run の共通 lifecycle と、各 workload 固有の処理との境界も扱う。

## Read this when
- 特定のサブコマンドの引数、事前条件、実行順序、報告、または recovery の契約を確認・変更するとき。
- realization apply・refactor、feedback report、run join・abandon の共通 lifecycle と workload 固有処理の分担を確認するとき。
- session 操作や oracle の調査・編集が、編集 run の lifecycle とどう異なるかを確認するとき。

## Do not read this when
- 複数のサブコマンドに共通する state、run isolation、doctor preprocess、prompt editor input、indexing、oracle と realization の適合性、feedback state、ログ出力などの規則を確認するときは、それぞれの共通仕様を直接読む。
- 特定の agent call の正確な prompt、prompt part、または起動パラメータを確認するときは、該当する builder の定義を直接読む。

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
