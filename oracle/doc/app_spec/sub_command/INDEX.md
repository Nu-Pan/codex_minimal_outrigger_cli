# `doctor.md`

## Summary
- 対象は `cmoc doctor` コマンドの仕様で、doctor preprocess を明示的に呼び出す単一目的の入口を定義する。引数はなく、固有の事前条件もない。
- doctor preprocess の開始前・途中を含む全終了経路で、検査・修復結果や残存 warning／エラー、次の操作、関連ログを要約した primary report を保存する責務を扱う。doctor preprocess の検証・修復内容そのものは、参照先の正本仕様へ進むための入口となる。

## Read this when
- `cmoc doctor` の呼び出し条件、引数、事前条件、実行手順を確認するとき。
- doctor の終了時に保存される primary report の対象経路、保存形式、記載内容を確認するとき。

## Do not read this when
- doctor preprocess 自体の検証・修復仕様を確認したいときは、このコマンド入口ではなく `oracle/doc/app_spec/doctor_preprocess.md` を直接読む。

## hash
- 78192f5cc8c533a2b68269fd3e788c6a451b58f7f95a42b039ce01d15180629e

# `editing_run.md`

## Summary
- 編集 run の開始・終了、同時実行制約、fork の共通処理、想定内差分、join/abandon の事前条件と後処理を定める共通仕様。
- realization apply/refactor の編集 run lifecycle を扱い、run state、worktree・branch、session state、report、merge・cleanup の境界を示す。
- 編集 run の fork、join、abandon の実装仕様や挙動を確認する際の共通入口であり、個別 workload の詳細仕様や session lifecycle の仕様を補完する。

## Read this when
- realization apply または realization refactor の編集 run を開始・終了する処理を実装・変更するとき
- cmoc run join または cmoc run abandon の引数、事前条件、差分検査、merge、cleanup、state 遷移を確認するとき
- 編集 run の branch、worktree、session state、report、terminal result の共通契約を確認するとき
- run の同時実行制約や、想定外差分・conflict・中断・失敗時の扱いを調査するとき

## Do not read this when
- cmoc session join/abandon など外側の session lifecycle だけを扱うとき
- cmoc oracle edit、read-only investigation/review、cmoc 自身による機械的更新、session join の conflict 解消だけを扱うとき
- realization apply/refactor 固有の編集内容や join 後 hook の詳細だけを確認するときは、先に該当する workload 固有仕様を読むとき
- run isolation や session state の正本定義そのものを確認するときは、参照先の oracle 仕様を直接読むとき

## hash
- 2454ed7f3c4ea88e6030213a51ba37d08737dca0cdf5a320d94b896f21c81698

# `feedback_report.md`

## Summary
- 対象は `cmoc feedback report` サブコマンドの正本仕様で、pending observation と直前の active state を report cut に固定し、人間対応が必要な issue のみを正常 report と新しい active state へ publication する処理を定義する。validation、deduplication、machine/agent observation の集約、normalization・verification agent の境界、inconclusive 時の incomplete 診断、再開・中断・cleanup、report 保存形式、終了コードまでを扱う。
- feedback observation と feedback state の仕様を参照しながら、report 処理の事前条件、状態遷移、agent に許可する入力、publication の受理条件を確認する必要がある作業の入口である。

## Read this when
- `cmoc feedback report` のCLI契約、事前条件、report cut、処理順序、candidate集約、normalization、verification、publication、再開・中断、report形式、終了コードを確認または変更するとき
- feedback observation の収集仕様や repository-local feedback state の lifecycle と、このサブコマンドの処理責務の対応を確認するとき
- 正常 publication と `incomplete` 診断 report、invocation summary report の使い分けや状態保持・cleanup条件を確認するとき

## Do not read this when
- raw observation の形式・収集方法だけを確認する場合は `feedback_observation.md` を直接読む
- feedback state の schema、generation、report cut、incomplete 診断 report の正本仕様だけを確認する場合は `feedback_state.md` を直接読む
- normalization または verification agent の正確な prompt、起動パラメータ、Structured Output schema を確認する場合は、本文で指定された対応する oracle 実装・JSON schema を直接読む
- session context や run.state の一般条件だけを確認する場合は `session_state.md` を直接読む
- サブコマンド共通の中断動作だけを確認する場合は `subcommand_interruption.md` を直接読む

## hash
- d897aae64a2792932f7ed6ea5562094b7d9b8150d31eba48b65208f24f34a6f0

# `indexing.md`

## Summary
- 作業ツリーを明示的にインデクシングするサブコマンド。git 未コミット差分の確認後、doctor preprocess を経てインデクシングを実行し、全終了経路で実行要約を primary report に保存する。

## Read this when
- 現在の作業ツリーを明示的にインデクシングするとき
- インデクシング実行前の未コミット差分チェックや doctor preprocess の手順を確認するとき
- インデクシング結果、更新対象の INDEX.md、commit、warning・エラーを含む primary report の扱いを確認するとき

## Do not read this when
- インデクシング以外のサブコマンドの実行手順を確認するとき
- INDEX.md のルーティング情報ではなく、インデクシング仕様そのものの詳細を確認するときは、参照先の indexing 仕様を直接読む

## hash
- c5eb10d95a5181aba3e7ab7e36113347aa670a3722b005f7a38f1538447a9103

# `oracle_edit.md`

## Summary
- oracle file の最終状態に関するユーザー指示を受け取り、doctor preprocess と indexing preflight の後に、本命と仕様削減の 2 回の独立した `codex exec` agent call を直列実行するサブコマンド。
- 本命 call は指示を oracle file に反映し、成功時のみ仕様削減 call が現在の oracle file と未コミット差分を基に過剰な仕様を削減する。
- 実行前後の条件検査、agent call の成否、共通 terminal result、警告・エラー、次の操作、診断ログおよび Codex call log を primary report に保存する。
- oracle file のみを編集対象とし、INDEX.md・AGENTS.md・realization file、Git 操作、branch・worktree 操作、run section の状態管理、終了後の indexing や自動 commit は対象外とする。

## Read this when
- `cmoc oracle edit` の実行順序、agent call の起動条件、独立した本命・仕様削減 call の扱いを確認するとき
- oracle file の編集境界、仕様削減 call の判断材料、失敗時の終了挙動を確認するとき
- primary report、サブコマンドログ、terminal result、Windows toast の記録要件を確認するとき

## Do not read this when
- oracle file の編集判断基準や prompt editor input、`codex exec` の共通入出力規約を直接確認したいときは、それぞれ指定された正本を読むべき場合
- oracle edit の実装配置や builder の具体的な実装を調べたいとき
- INDEX.md の既存ルーティングや、対象本文に記載されていない session・worktree の仕様を確認したいとき

## hash
- ae8399f6f74a988959b5f205746030e19778d83e168ec394a833df40ed3a4871

# `oracle_investigation.md`

## Summary
- oracle file に関するユーザーの調査指示を受け取り、その内容を根拠に調査する Codex CLI の TUI を起動するサブコマンドの仕様を定義する。入力 lifecycle、TUI 起動パラメータの委譲、Codex CLI 起動条件、調査結果とファイル変更の扱いを確認するための入口となる。

## Read this when
- oracle file の内容に基づく調査用 TUI の起動手順や責務境界を確認するとき
- ユーザー指示のエディタ入力、doctor preprocess、または TUI 起動パラメータ構築の流れを確認するとき
- oracle file・realization file・INDEX.md の変更可否や調査結果の扱いを確認するとき

## Do not read this when
- oracle file 自体の判断基準や変更規則を確認したい場合は、正本として指定された oracle_and_realization.md を直接読むとき
- プロンプトのエディタ入力の詳細だけを確認したい場合は、prompt_editor_input.md を直接読むとき
- TUI 起動パラメータの正確な構築内容だけを確認したい場合は、launch_tui.py の builder を直接読むとき
- Codex CLI の TUI 共通仕様や Windows toast 通知の詳細だけを確認したい場合は、指定された各正本仕様を直接読むとき

## hash
- 91ed1b1a24c31a7cc11ea20cd7927855e11f1660e57feb42c4ea09ab707bb6be

# `oracle_review.md`

## Summary
- `cmoc oracle review` サブコマンドの正本仕様。oracle ファイルを対象に、スコープ選択、隔離 run、所見の列挙・統合・検証・採否判定、中断処理、Markdown レポート保存までの責務と実行規則を定義する。レビュー処理やレポート形式、所見成立条件を変更・実装・検証するときの入口となる。

## Read this when
- `cmoc oracle review` の引数、事前条件、実行手順、agent call の責務を確認するとき
- oracle レビューの所見成立条件、重大度、ループ上限、採否判定を変更または検証するとき
- レビュー中断時の部分結果の扱い、隔離 run、レポートの保存先・形式を確認するとき

## Do not read this when
- oracle ファイル一般の判断基準や run 隔離の共通規則だけを確認したい場合は、本文が参照する対応する app_spec を直接読むとき
- Codex CLI の実装配置や個別 builder の詳細を変更・確認する場合は、本文で指定された実装ファイルを直接読むとき
- 自動生成された `INDEX.md` のレビューや、実装ファイルを含む一般的なコードレビューを行うとき

## hash
- 437ba9d89f9a816c5a9f3ccb82be7264f3aaa8b121d2f078760acb55c54b4272

# `realization_apply.md`

## Summary
- 直近の git commit 群から読み取れる oracle file の変更を realization file へ反映する `cmoc realization apply fork` の仕様を定義する。引数、追従対象差分、単一の本命 agent call、realization file の変更制約、fork の実行手順、report・終了コード・feedback、エラー処理、join 後 hook を扱う。realization apply の fork 実行と、関連する lifecycle・差分追従・結果報告の確認における入口となる。

## Read this when
- `cmoc realization apply fork` の引数や追従対象となる commit 差分を確認するとき
- fork で実行する agent call の回数、cwd、起動パラメータ委譲、oracle file と realization file の変更制約を確認するとき
- fork の実行手順、エラー時の状態遷移、report の保存内容、終了コード、feedback の扱いを確認するとき
- join 成功後に更新される apply fork の session state を確認するとき

## Do not read this when
- fork・join・abandon に共通する lifecycle の正本仕様だけを確認したいときは、指定された編集 run 共通仕様を直接読む
- oracle file に対する realization file の適合性判断だけを確認したいときは、指定された oracle・realization 仕様を直接読む
- agent call の正確な prompt、prompt part、起動パラメータの実装を確認したいときは、指定された launch_exec.py を直接読む
- feedback の共通仕様だけを確認したいときは、指定された feedback 仕様を直接読む
- ファイル単位の網羅的な realization 追従や realization refactor の仕様を確認したいとき

## hash
- ad680c5ec4ada37105070937ba4a9504a7ba8b12f90d775032f15bf80d2b6ace

# `realization_refactor.md`

## Summary
- oracle file と realization file の全体を対象に、current fork 内で未解決 target を除きながら、調査・realization file 修正・検証・state 同期・commit を反復する realization refactor fork の仕様。
- refactor state の entry 同期、調査対象の選択順、処理結果の正規化、unresolved target の扱い、および fork 完了条件を定義する。
- 自然完了、unresolved 付き完了、ユーザー中断、エラーの各終了経路における report、lifecycle state、終了イベント、終了コードの要件を定義する。
- realization refactor の fork 処理を実装・レビューするときの入口であり、短い変更ループの realization apply や共通 lifecycle の詳細確認には直接の対象ではない。

## Read this when
- realization refactor fork の全体フローや反復処理を実装・変更するとき。
- refactor state の保存形式、file 集合同期、調査要求、調査履歴、current fork の unresolved target を扱うとき。
- agent call の変更 path 検証、所見の正規化、処理単位の commit・rollback、調査継続条件を確認するとき。
- fork の完了判定、ユーザー中断、その他のエラー、report 生成、終了イベントや終了コードを確認するとき。

## Do not read this when
- realization apply の短い変更ループだけを扱うとき。
- fork・join・abandon の共通 lifecycle だけを確認するときは、共通 lifecycle の正本を直接読む。
- oracle file と realization file の適合性基準だけを確認するときは、適合性の正本を直接読む。

## hash
- 8820331547c471fbb20f0189d49c6c5e9477e6d2b686930a6f8be918e2961be4

# `session_abandon.md`

## Summary
- `cmoc session abandon` の正規仕様を定義する文書。現在の session branch を home branch に取り込まず破棄するコマンドの目的、引数、事前条件、破棄対象、実行手順、状態遷移、失敗時の扱い、primary report 要件を扱う。session 終了・破棄処理の仕様を確認する際の入口となる。

## Read this when
- `cmoc session abandon` の挙動、事前条件、破棄してよい資源と保持すべき資源を確認するとき
- session branch の切替・状態更新・強制削除や、cleanup 失敗時の rollback 方針を実装・検証するとき
- session abandon の全終了経路における primary report の保存内容と保存先を確認するとき

## Do not read this when
- session を本流へ取り込む `cmoc session join` の仕様だけを確認したいとき
- 未 join の編集 run の破棄方法を確認したいときは、`cmoc run abandon` の仕様を直接読む
- active session context や session 終了に共通する事前条件の詳細を確認したいときは、`oracle/doc/app_spec/session_state.md` を直接読む

## hash
- fbb79c4d37def8c284cbdda82dc4b0e333a380821805ec1d19abe0bbfce8ff40

# `session_fork.md`

## Summary
- `cmoc session fork` は、現在のローカルブランチを session home branch として、その HEAD から一意な session branch を作成・checkout し、session 情報と初期状態を保存するサブコマンド。
- 引数はなく、detached HEAD、ローカルブランチ以外、cmoc 管理ブランチ、未コミット差分、既存の active session branch がある場合は実行できない。
- doctor preprocess、事前条件確認、ブランチ作成、session state 保存、terminal result 生成までの手順と、全終了経路で保存する fork 実行要約の primary report 要件を扱う。

## Read this when
- `cmoc session fork` の実行条件、処理順序、session branch の作成・checkout を確認するとき。
- session fork における session state の初期保存や terminal result の内容を確認するとき。
- fork の成功・失敗・事前条件終了時に作成される primary report の保存条件や記録内容を確認するとき。

## Do not read this when
- ブランチの役割、分岐関係、session branch の命名規則そのものを確認する場合は、branch model を直接読む。
- session 情報・初期状態の schema や状態遷移を確認する場合は、session state 仕様を直接読む。
- session branch に用いる timestamp の形式だけを確認する場合は、timestamp 仕様を直接読む。
- 他の `cmoc session` サブコマンドの固有動作を確認する場合は、対象サブコマンドの仕様へ直接進む。

## hash
- 6d328c35ed9ba2ae00ae74e17a15fdae427ec098fe5ca4f3755522df231671b3

# `session_join.md`

## Summary
- `cmoc session join` の仕様を確認するための入口。active session の終了処理として、session branch を home branch に merge し、conflict 解消、session state の joined 遷移、branch cleanup、primary report 保存までの責務と終了経路を扱う。通常の汎用 git merge wrapper の仕様を確認する対象ではない。
- session join の merge 元・先や default branch の扱い、session 終了前提条件、feedback state との境界を確認したい場合に読む。

## Read this when
- `cmoc session join` の引数、事前条件、実行手順を実装・確認するとき
- session branch の merge、conflict marker 解消用 agent call、merge commit、cleanup の挙動を確認するとき
- session state の joined 遷移、primary report の内容、エラー終了時の扱いを確認するとき

## Do not read this when
- 通常の git branch 間の汎用 merge wrapper の仕様を確認したいとき
- session state の共通事前条件そのものを確認したいときは `session_state.md` を直接読む
- branch model の merge source・target・default branch の正本を確認したいときは `branch_model.md` を直接読む
- feedback state の所有範囲と配置を確認したいときは `feedback_state.md` を直接読む
- conflict 解消用 agent call の具体的な prompt・parameter 生成規則を確認したいときは `conflict_resolution.py` を直接読む
- エラー分類・stack trace の共通規則を確認したいときは `error_handling.md` を直接読む

## hash
- 0f849403c52e721f2e0e443127ea72c6c4905c2b3974a6f65042d521a1a89f88

# `tui.md`

## Summary
- `cmoc tui` サブコマンドの責務と実行契約を定義する正本文書。ユーザープロンプトの受領、起動パラメータ構築、AI Agent CLI/TUI の起動、共通規定・indexing preflight・feedback・通知の適用条件を確認する入口。Codex CLI 固有の起動要素は関連する `codex_exec_rule.md` へ委譲される。

## Read this when
- `cmoc tui` の引数、事前条件、実行手順、TUI 起動条件を確認・変更するとき
- ユーザープロンプトへの cmoc 固有契約の注入や、バックエンド共通の適用規則を確認するとき
- Codex CLI を `cmoc tui` から起動する際の固有設定を確認する前に、サブコマンド全体の責務境界を把握するとき

## Do not read this when
- プロンプトエディタ入力の具体的な lifecycle だけを確認する場合は、指定された `prompt_editor_input.md` を直接読む
- 起動パラメータの正確な prompt part、文面、選択理由を確認する場合は、`launch_tui.py` の `build_tui_launch_tui_parameter` を直接読む
- Codex CLI の環境変数、preflight validation、引数による設定上書きだけを確認する場合は、`codex_exec_rule.md` を直接読む
- oracle・realization の責務や適合性、oracle review の所見成立条件だけを確認する場合は、指定された各正本文書を直接読む
- indexing preflight、feedback observation、Windows toast 通知の詳細だけを確認する場合は、それぞれ指定された正本文書を直接読む

## hash
- 9dc7bcc69cf3780b894b997bb20b3894d41d844aea1dec96a8ad8dc63ce98331
