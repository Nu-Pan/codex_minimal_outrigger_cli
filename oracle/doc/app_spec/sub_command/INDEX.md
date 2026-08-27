# `doctor.md`

## Summary
- `cmoc doctor` コマンドの仕様を定義するエントリー。doctor preprocess の明示的な呼び出し、引数・事前条件、終了経路ごとの primary report 保存要件を確認する入口。

## Read this when
- `cmoc doctor` の引数、実行手順、事前条件を確認するとき
- doctor preprocess の実行結果を含む primary report の保存先・内容・対象終了経路を確認するとき
- `cmoc doctor` のコマンド仕様を変更または実装と照合するとき

## Do not read this when
- doctor preprocess 自体の検証・修復内容を確認したいときは、正本である `oracle/doc/app_spec/doctor_preprocess.md` を直接読む
- doctor に関連する診断用サブコマンドの個別仕様だけを確認するとき

## hash
- 3ac841bd58e673fbd25a431f4a8ea2222c30c0231315714db459e02ca50c9f8a

# `editing_run.md`

## Summary
- workload 固有の fork で開始し、`cmoc run join` または `cmoc run abandon` で終了する編集 run の共通 lifecycle を定義する仕様。
- fork の事前条件・開始処理、編集責務、想定内差分、run state 遷移、join／abandon の事前条件と後処理を扱う。
- join における差分検査・merge・hook・refactor state 同期・cleanup、および abandon における process 停止・資源破棄・cleanup の共通入口となる。
- fork、join、abandon の report と terminal result に必要な分類・状態・資源・結果の扱いも定める。

## Read this when
- 編集 run の一般的な fork・join・abandon の流れや、`joinable`／`error`／`ready` などの lifecycle 境界を確認するとき。
- run branch と worktree の作成、想定内差分の検査、session branch への merge、cleanup の共通規則を確認するとき。
- 編集 run の report 保存要件、terminal result、異常終了時の扱いを確認するとき。
- `cmoc realization apply fork` または `cmoc realization refactor fork` の workload 固有仕様を実装・レビューする際に、共通 lifecycle の前提を確認するとき。

## Do not read this when
- session の join／abandon など外側の session lifecycle を確認したいとき。
- run の隔離資源と一般 lifecycle の正本定義を確認したいとき。
- session／run の永続 state field や同時実行数の正本定義を確認したいとき。
- realization refactor 固有の join 後 state 同期や workload 固有 hook を確認したいとき。
- report の共通出力形式・field・表示順序だけを確認したいとき。
- feedback data と編集 run の境界だけを確認したいとき。

## hash
- b16e82b49839f52da1a3f68f0930a38d32ebc64fe157453977c6463ea67d47b8

# `feedback_report.md`

## Summary
- 「cmoc feedback report」サブコマンドの挙動・CLI契約・事前条件・report cut・機械処理・normalization/verification・publication・中断/再開・保存形式・終了コードを定める正本仕様。feedback state/observation、session state、ACP builder の関連仕様から本コマンドの実装や適合性を確認する入口。

## Read this when
- `cmoc feedback report` のCLI契約、事前条件、処理順序、deduplication/集約、agent呼び出し、verification verdict、正常またはincomplete publication、report保存、終了コードを実装・変更・レビューするとき。
- feedback report の state lifecycle や raw observation の扱いを確認する必要があり、指定された feedback state/observation の正本仕様から読み始めるとき。
- normalization または verification agent の prompt、Structured Output schema、受理条件を確認するとき。
- 中断・再開、incomplete 後の再実行、cleanup recovery、invocation summary report の挙動を確認するとき。

## Do not read this when
- feedback observation の収集規則だけを確認する場合は、先に feedback_observation.md を直接読む。
- repository-local state の schema、generation、cut、pointer、cleanup、incomplete 診断 report の詳細だけを確認する場合は、先に feedback_state.md を直接読む。
- session や run の状態条件だけを確認する場合は、session_state.md を直接読む。
- normalization/verification の prompt や schemaそのものを変更・確認する場合は、各 ACP builder の実装と対応する JSON schema を直接読む。

## hash
- 36ccb48943c3d371979080efb55c983c878c7c92f3373e72a315366bb49233b9

# `indexing.md`

## Summary
- `cmoc indexing` サブコマンドの仕様を定義する。現在の作業ツリーを明示的にインデクシングし、doctor preprocess、前提条件、実行手順、primary report の保存内容と終了経路を確認する入口。

## Read this when
- `cmoc indexing` の引数、未コミット差分がある場合の扱い、doctor preprocess を含む実行手順を確認するとき
- インデクシング実行要約の保存先、Front Matter、本文に含める報告項目を確認するとき

## Do not read this when
- インデクシング仕様そのものの詳細を確認する必要があり、参照先の indexing 仕様を直接読むべきとき
- `cmoc indexing` 以外のサブコマンドの仕様を確認するとき

## hash
- cf37de227f8fd370f800fa7436d45825224c6e50e93afbcfef7fbf1c5a76fdd3

# `oracle_edit.md`

## Summary
- `cmoc oracle edit` サブコマンドの正本仕様。oracle file の編集指示を受け取り、doctor preprocess、indexing preflight、条件検査を経て、本命と仕様削減の独立した `codex exec` を順に実行するライフサイクルを定義する。
- ユーザー指示からの prompt 構築、agent の編集境界、失敗時の扱い、primary report、ログ・通知、差分保持、および排他制御を規定する。oracle edit の実行順序や終了状態、報告内容、agent call の権限を確認する入口となる。

## Read this when
- `cmoc oracle edit` の実行フロー、起動条件、agent call の順序または失敗処理を変更・検証するとき。
- oracle file 編集 agent のアクセス範囲、仕様削減 call の判断材料、差分の扱いを確認するとき。
- primary report、console/log、terminal result、Windows toast の生成要件を確認するとき。
- このサブコマンドが通常の edit run、fork/join lifecycle、session state の run section とどう異なるかを確認するとき。

## Do not read this when
- oracle file の編集内容そのものの仕様や、prompt editor input・`codex exec` の共通受け渡し規約を確認する場合は、それぞれ参照先として指定された正本を直接読む。
- doctor preprocess、indexing、session state、oracle と realization の一般規約の詳細だけを確認する場合は、本文が参照する各 app_spec または oracle file を直接読む。
- 実装配置や test の作成規約を確認する場合は、対応する design_rule・test_rule・test_execution を直接読む。

## hash
- 025f83c9686253d329ba02e42de83d33c37f7e36b8f1b85f2c5f5b13b65cd218

# `oracle_investigation.md`

## Summary
- oracle file に関するユーザーの調査指示を受け取り、doctor preprocess と prompt editor input の lifecycle を経て、専用 builder が構築したパラメータで Codex CLI の TUI を起動するサブコマンドの仕様。
- 調査対象の判断基準や正確な prompt・起動パラメータは、本文ではなく指定された oracle file と builder に委譲されている。調査結果は TUI で日本語を原則として回答し、oracle file と realization file の扱いにも制約を定める。

## Read this when
- oracle file に関する調査用 TUI の起動手順、入力 lifecycle、起動パラメータ構築、Codex CLI の起動方法を確認するとき
- oracle file と realization file の変更禁止、調査結果の提示方法、indexing preflight の扱いを確認するとき

## Do not read this when
- oracle file の調査判断基準や正確な prompt 文面・AgentCallParameter だけを確認したい場合は、本文が指定する oracle_and_realization.md または launch_tui.py を直接読むとき
- プロンプトエディタ入力の正本仕様だけを確認したい場合は prompt_editor_input.md を、Codex CLI の TUI 固有仕様だけを確認したい場合は tui.md を直接読むとき
- Windows toast 通知の仕様だけを確認したい場合は windows_toast_notification.md を直接読むとき

## hash
- 4400182686705983388c2c941051e346afce067099f9d2284b21fd9faa49a090

# `oracle_review.md`

## Summary
- `cmoc oracle review` サブコマンドの正本仕様。oracle ファイルを session または full スコープでレビューし、所見の列挙・統合・検証・採否判定を経て Markdown レポートを保存・提示する責務、実行手順、agent call の委譲先、所見成立条件、隔離実行、中断処理、レポート形式を定義する。oracle review の挙動、所見判定、レビュー対象範囲、レポート生成を変更・実装・検証するときの入口。

## Read this when
- `cmoc oracle review` の引数、事前条件、実行手順、終了経路を確認するとき
- oracle ファイルのレビュー所見が成立する条件や重大度、採否判定の境界を確認するとき
- agent call の builder 委譲、所見リストの反復処理、隔離 run、中断時の扱いを確認するとき
- oracle review レポートの保存先、frontmatter、本文セクション、Verdict の意味を確認するとき

## Do not read this when
- 自動生成される `INDEX.md` 自体のレビューや編集を扱うとき
- 実装ファイルを交えたレビュー、実装品質、または次に何をすべきかという提案を扱うとき
- feedback 成果物との境界だけを確認するときは、`feedback.md` の既存 workload との境界を直接読むとき
- run 隔離資源・lifecycle、共通中断動作、oracle と realization の一般的な判断基準を確認するときは、それぞれ指定された正本仕様を直接読むとき

## hash
- 1ed120ec6cee008d552a40a93e9ba846fe01fee9fcc9427af797ed866195ed4d

# `realization_apply.md`

## Summary
- 直近の git commit 群から読み取った oracle file の変更を realization file へ反映する `realization apply fork` の仕様を定める。fork の目的、追従対象差分、agent call の実行制約、完了時の検査・commit・run state、report、feedback、join 後 hook を扱い、realization apply の fork 運用全体への入口となる。

## Read this when
- realization apply の fork を開始・実行・完了判定・エラー処理するとき
- 追従対象となる commit 差分の始点・終点、agent call の回数や cwd、変更可能なファイル範囲を確認するとき
- fork report、終了コード、feedback observation、join 後の session 更新仕様を確認するとき

## Do not read this when
- fork・join・abandon に共通する編集 run の lifecycle 自体を確認したいときは、共通仕様の正本を直接読む
- oracle file と realization file の一般的な適合性判定を確認したいときは、oracle と realization の適合性仕様を直接読む
- 実際の launch prompt 構築や起動パラメータの実装を確認・変更するときは、指定された launch_exec.py を直接読む

## hash
- 4370732d4585759e5231094dce41718ef169542246d730be48326cb238626741

# `realization_refactor.md`

## Summary
- realization refactor fork の目的、refactor state の同期・調査・更新、current fork の unresolved target 管理、完了・中断・エラー時の lifecycle と report を定義する仕様書。
- oracle file と realization file の集合を対象に、未調査または再調査が必要な entry を選び、1 file 単位で調査・修正・検証・state 更新・commit を繰り返す処理の入口。
- refactor の実装、state schema と同期条件、agent call の結果判定、unresolved を含む完了条件、fork report の内容を確認する必要がある場合に読む対象。

## Read this when
- realization refactor fork の処理順序、対象 file の選択、調査履歴、current fork 固有の unresolved target の扱いを確認するとき。
- refactor state の保存形式、entry 集合の同期、不変条件、調査結果に応じた investigation_required の更新を実装・レビューするとき。
- fork の自然完了、unresolved 付き完了、中断、エラー、終了 report、終了コード、join 後の挙動を確認するとき。

## Do not read this when
- 短い変更ループを担う realization apply の仕様だけを確認する場合。
- oracle file と realization file の適合性そのものの判定基準を確認する場合は、正本である oracle_and_realization の仕様を直接読む。
- 明示的な join を必要とする編集 run の共通 lifecycle や中断共通動作だけを確認する場合は、対応する共通仕様を直接読む。

## hash
- a44effe7275b74bd4610f429803c133fcff3a85949500d8d1e9176bc21891be3

# `session_abandon.md`

## Summary
- `cmoc session abandon` は、現在の session branch を home branch に merge せず破棄し、session state を `abandoned` に更新する session 終了コマンド。join 済み結果の rollback や未 join 編集 run の破棄は担当せず、後者は `cmoc run abandon` を先に実行する。
- doctor preprocess、事前条件検証、home branch への切替、state 更新、session branch の強制削除、および失敗時の rollback を含む cleanup 手順を確認できる。
- 正常終了・エラー終了を問わず保存される session abandon の primary report 要件と、破棄対象・残存資源・次の操作・診断ログの記録内容を確認できる。

## Read this when
- session の成果物を本流へ取り込まず破棄したいとき。
- `cmoc session join` との違い、session branch と home branch の扱い、未 join の編集 run が残る場合の前提を確認したいとき。
- session abandon の実行手順、状態遷移、cleanup 失敗時の再実行条件、primary report の保存要件を確認したいとき。

## Do not read this when
- session の成果物を home branch に取り込む完了処理を確認したいときは、`cmoc session join` の仕様を直接読む。
- 未 join の編集 run を破棄したいときは、`cmoc run abandon` の仕様を直接読む。
- 既に join 済みの session 結果を取り消す rollback を確認したいとき。

## hash
- fd16472d23f6a9537220c8bb8f67d30faa267025f942dfd586175583630fa11f

# `session_fork.md`

## Summary
- `cmoc session fork` の引数なしサブコマンドについて、実行可能なブランチ条件、未コミット差分などの事前条件、セッションブランチ作成から初期状態保存までの実行手順を定義する。
- セッションブランチの命名、分岐元変更時の扱い、terminal result へのブランチ情報、および全終了経路で保存する primary report の要件を扱う。
- session fork のCLI挙動、セッション状態保存、ブランチ操作、終了報告の仕様を確認する際の入口となる。

## Read this when
- `cmoc session fork` の実装またはテストで、実行前提条件や処理順序を確認するとき
- セッションブランチの命名規則や任意 start point を受け付けない仕様を確認するとき
- session state の初期化、terminal result の固有結果、または primary report の保存内容を扱うとき
- fork の失敗経路、doctor preprocess、rollback、残存資源の報告要件を確認するとき

## Do not read this when
- ブランチの一般的な役割や分岐関係だけを確認したい場合は、正本である `oracle/doc/branch_model.md` を直接読むとき
- session state の schema や状態遷移の詳細だけを確認したい場合は、`oracle/doc/app_spec/session_state.md` を直接読むとき
- timestamp の形式だけを確認したい場合は、`oracle/doc/app_spec/timestamp.md` を直接読むとき
- `cmoc session fork` 以外のサブコマンドの固有仕様を確認するとき

## hash
- 9463c501aad0b1af8be915ed4edf1b2a8161a0a8b2d80958cf60ff31c54af4a8

# `session_join.md`

## Summary
- `cmoc session join` のセッション終了処理を定義する仕様書。現在の session branch を session home branch へ merge し、conflict 解消、session state の `joined` 更新、安全な branch cleanup、primary report 保存までの責務と実行順序を扱う。session 終了、branch merge、conflict 対応、終了報告の仕様を確認する際の入口となる。
- merge source・merge target・default branch の意味は branch model、事前条件と session context は session_state、feedback state との所有境界は feedback_state、エラー分類は error_handling、conflict 解消用 agent call の詳細は指定された realization oracle を参照する。

## Read this when
- `cmoc session join` の引数、事前条件、実行手順、merge 対象、session state 遷移を確認するとき
- session branch を home branch に戻す処理、merge conflict の解消手順、branch cleanup の安全条件を実装・変更するとき
- session join の成功・失敗時に保存する primary report の内容や終了経路を確認するとき

## Do not read this when
- 通常の git branch 間の汎用 merge wrapper の仕様を確認したいとき
- session 作成や session 中の編集 run fork の仕様だけを確認したいときは、session_state を直接読む
- feedback state の所有範囲・配置だけを確認したいときは、feedback_state を直接読む
- merge conflict 解消用 agent call の具体的な prompt 構築を確認したいときは、指定された conflict resolution realization oracle を直接読む

## hash
- cb418ac5f4c9671c1e3623617d076d754aaf61f60d4ae27af564b73f64e44778

# `tui.md`

## Summary
- `cmoc tui` サブコマンドの責務と実行フローを定義する。ユーザーのオリジナルプロンプトに cmoc 固有契約を注入し、起動パラメータを構築して AI Agent CLI/TUI を直接起動する処理の入口。
- プロンプトエディタ入力、TUI 共通契約、indexing preflight、feedback observation、Windows toast 通知、および Codex CLI 起動時に持ち込む要素への参照境界を示す。

## Read this when
- `cmoc tui` の責務、引数、事前条件、実行手順を確認するとき
- ユーザープロンプトへの cmoc 基本規定の注入条件や、TUI 起動前後の共通処理を確認するとき
- Codex CLI を `codex` として起動する仕様、または起動パラメータ構築への委譲範囲を確認するとき

## Do not read this when
- プロンプトエディタ入力の正確な lifecycle を確認したいときは、直接 `oracle/doc/app_spec/prompt_editor_input.md` を読む
- TUI の正確な prompt part、起動パラメータ、選択理由を確認したいときは、直接 `oracle/src/oracle/acp_builder/tui/launch_tui.py` を読む
- oracle と realization の責務・適合性や oracle review の所見成立条件を確認したいときは、指定された各正本仕様を直接読む
- indexing、feedback observation、Windows toast 通知、または Codex CLI の詳細規則だけを確認したいときは、それぞれ指定された正本仕様を直接読む

## hash
- 296f3e174599ccfbc1a219bdf257f6666e7f862683ce7675c9ef4c283ee781cf
