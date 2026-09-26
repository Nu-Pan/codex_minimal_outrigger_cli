# `cli_auto_completion.md`

## Summary
- `_CMOC_COMPLETE` が存在する呼び出しを自動補完プローブとして扱い、通常実行向けの前処理・検査・副作用と標準出力・標準エラーを制限する CLI 共通の境界を定める。
- 自動補完プローブ中の Windows toast 通知固有の境界は、Windows toast の仕様書に委ねる。

## Read this when
- CLI 起動時に自動補完プローブを判定する条件や、補完処理より前に抑止すべき通常実行向け処理・出力を確認または変更するとき。
- 補完プローブ時の起動順序や副作用を見直すとき。

## Do not read this when
- 自動補完プローブ中の toast 初期化、transport 検査、通知警告の扱いだけを確認するときは、Windows toast の仕様書を読む。
- 通常実行時の引数やサブコマンドの挙動を確認するときは、該当する利用法またはサブコマンドの仕様書を読む。

## hash
- 74a5ed107dd4f9f3297e6456d31ea9ddce5cc89fbdcf99524330336e910184df

# `codex_exec_rule.md`

## Summary
- Codex CLI 呼び出しの cwd と path context、起動前検証、argv による設定上書き、sandbox、ファイルアクセス制限を定める。
- prompt の受け渡しや MCP 接続、呼び出し記録、session、Structured Output の検証・補正など、agent call を Codex CLI で実行する際の共通規則を扱う。
- 並列呼び出しと、quota 枯渇や一時障害時の probe・待機・再開の判断を定める。

## Read this when
- Codex CLI の起動条件、argv、cwd、sandbox、ファイルアクセス境界を変更・確認するとき。
- prompt の渡し方、呼び出し単位の MCP 設定、ログ、session、Structured Output の受理や補正を調べるとき。
- Codex 呼び出しの並列化、quota 枯渇や一時障害からの回復・再開を扱うとき。

## Do not read this when
- model provider・Model・Reasoning Effort の設定取得、値の意味、検証境界だけを調べるときは、それらを所有する provider 仕様を読む。
- Windows toast の通知境界や callback 設定だけを扱うときは、通知仕様を読む。
- 個別 agent call の目的・判断基準・file access mode の選択だけを変更するときは、その workload の仕様を読む。AgentCallParameter の正確な field、型、既定値だけを確認するときは、その構造を定義する宣言を直接読む。

## hash
- ea44f6ddbdc8b1b47970905038ef3d37bf4e43248672535b95f8141d24c15550

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
- 本命処理の前に各サブコマンドが共通で行う doctor preprocess の検証・修復と、その tracked 差分の commit を定める。管理領域の非追跡保証、必要な管理ファイルと refactor state の追跡・同期、reporter/client の事前検証を扱う。
- linked worktree や後から作成する run worktree も個別に検証する。reporter/client が利用不能または protocol 不一致の場合は warning を記録して本命処理を続ける。

## Read this when
- サブコマンド共通の事前検証・修復や、そこから生じる tracked 差分の commit を変更するとき。
- repo-root、work-root、linked worktree、run worktree の管理領域に対する非追跡保証を変更するとき。
- 編集 run の join 前後で行う refactor state 同期の時点や、reporter/client 事前検証の失敗時の扱いを変更するとき。

## Do not read this when
- 明示的な `cmoc doctor` の起動条件、実行要約、report の仕様を調べるときは、doctor サブコマンドの仕様へ進む。
- 個別サブコマンド固有の事前条件や clean 状態の検査を調べるときは、そのサブコマンドの仕様へ進む。この文書はそれらを検査しない。
- refactor state の JSON schema や entry 同期の内容を調べるときは、realization refactor の仕様へ進む。この文書はその検証と同期時点を定める。
- reporter の agent-facing interface、observation の受け入れ検査、collector transport を調べるときは、feedback observation の仕様へ進む。この文書が定めるのは事前検証と warning の扱いまで。
- 文書検索用の共有資材のセットアップを調べるときは、環境セットアップの仕様へ進む。この文書は管理領域の適用先を示す。

## hash
- c1dd6a37ff7dbcc1685e86fd512b9dbc1828ca632b9484ff47bb0b780d0e2e72

# `document_search.md`

## Summary
- cmoc の意味検索について、対象文書と閲覧範囲、本文の同期、候補検索と再ランキング、失敗の扱いまでの仕様上の判断を担う入口。
- 初期方式と製品受入条件も示し、PoC の実現性根拠と未検証事項を区別する。

## Read this when
- 検索対象となる正本文書や caller の閲覧範囲、検索結果の扱いに関する仕様を確認・変更するとき。
- 本文変更の反映、索引と cache、推論・再ランキングの失敗、保存 identity、排他や終了処理の契約を調べるとき。
- 意味検索の製品化状況や受入条件を確認するとき。

## Do not read this when
- 検索 MCP を call に接続する規則や、閲覧制限に基づく call 開始判断を調べるときは、agent 実行規則を参照する。
- 閲覧範囲・設定・tool 入出力・モデル資材の正確な型、既定値、識別情報を調べるときは、それらを所有する実装定義を参照する。
- 環境構築や検索資材の取得・準備手順を調べるときは、開発環境の手順を参照する。
- 実際の実装挙動、live discovery、性能、製品受入の達成状況を確かめるときは、実装・統合検証の証拠を直接確認する。

## hash
- f960a104fc2fdd2f1f6881d3a31db8923e317ea71ef2edbcf7e986edc22e67d2

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

# `merge_conflict_resolution.md`

## Summary
- run join、feedback report の自動 join、session join に共通する競合解消の判断基準と agent・cmoc の責務を定める。コマンドをまたぐ統合方針や責任分界を確認する入口。

## Read this when
- 競合解消で両側の意図と oracle をどう扱うか、付随編集や検証・報告をどこまで行うかを確認・変更するとき。
- 内容解消を担う agent と、staging や merge などを担う cmoc の境界を確認するとき。

## Do not read this when
- 特定コマンドの編集範囲、復旧、後処理だけを確認するときは、そのコマンドの仕様を直接読む。
- agent 向け prompt の正確な文面、構築方法、設定値だけを確認するときは、該当する prompt 構築処理や設定の oracle src を直接読む。

## hash
- 7c68ee584d9f3f608e7c11411346d4c445132b94a84aebdfb11c8497641f1fee

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
- oracle と realization の列挙結果と分類条件を定め、Git ignore と nested repository の扱いを明確にする。
- traversal と pruning、symlink・非通常ファイルの処理、ignore 判定の性能条件、回帰検証の境界を確認する入口。

## Read this when
- 列挙対象に含めるファイルや除外条件を判断するとき、特に nested repository、tracked 状態、ignore 規則を扱う場合。
- 列挙処理の traversal、pruning、symlink や非通常ファイルの扱い、ignore 判定の性能・検証条件を変更またはレビューするとき。

## Do not read this when
- 列挙結果を使う doctor preprocess や refactor state 同期の個別の挙動だけを確認するときは、それぞれの処理仕様や実装を直接読む。
- ファイルの発見・分類や列挙時の制約が関係しない作業では読む必要はない。

## hash
- b417230daa33c7d8d323a02230b9e68561409276946ed9dc0a38a2d0f9409b62

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
- session 内で workload を隔離実行する共通 lifecycle と、run の branch・worktree、agent call の作業場所やアクセス境界を横断的に定める。
- 個別 workload や公開コマンドの手順ではなく、run に共通する規則を確認する入口。正確な資源定義、永続 state、workload 固有の処理は、それぞれの専門仕様が正本となる。

## Read this when
- 作業が run を使うか、明示的な join・abandon を待つか、同じ invocation 内で join するかを判断するとき。
- run の隔離資源、agent call の cwd・path context、ファイルアクセス境界を確認するとき。
- ログ、feedback state、文書検索などの管理データと run lifecycle の境界を追うとき。

## Do not read this when
- 特定のサブコマンドや workload の引数、事前条件、処理手順、固有の cleanup・recovery を調べるだけなら、その個別仕様へ進む。
- branch・commit・worktree の正確な定義や、永続 session/run state の field・状態遷移が必要なら、それぞれの定義仕様へ進む。
- agent call の詳細なアクセス規則や merge conflict の解消方法だけを確認するなら、それぞれの専用仕様へ進む。

## hash
- 355dd544fcb80f1a8fddd9f5bbb1f9a2512a4edc0a8d9fcf43bdde4bb749ee3d

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
- コマンド固有の仕様と編集 run の共通ライフサイクルをまとめる。各仕様は引数、前提条件、処理の流れを定め、対象に応じて agent 起動、編集範囲、状態遷移、報告も扱う。
- doctor、文書索引、oracle の調査・編集、TUI、realization の追従、feedback 処理、session の開始・終了に関する仕様を探す入口。

## Read this when
- 特定のサブコマンドの挙動、引数、前提条件、副作用、終了報告を確認または変更するとき。
- realization apply/refactor や feedback report の編集 run と join・abandon の関係を確認するとき。
- 複数のコマンドをまたいで、コマンド固有の契約を比べたり追跡したりするとき。

## Do not read this when
- 一つのサブコマンドの挙動だけが対象なら、該当するコマンド仕様へ直接進むとき。
- 共通の state、branch・merge、文書検索、入力 handoff、ログ規則そのものを確認するときは、それぞれの共通仕様へ直接進む。
- agent 向け prompt の正確な文面や起動パラメータの構築内容を確認するときは、委譲先の定義へ直接進む。

## hash
- 8f298c22a33c5da8708fee4f71a508a30cff5bdb67fb32c56acbb255a764cf5d

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
