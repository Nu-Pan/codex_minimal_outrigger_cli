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
- `cmoc oracle edit` の目的、引数、ユーザー指示からの prompt 構築、本命・仕様削減 agent call の実行順序と成功条件を定義する仕様書。
- doctor preprocess、indexing preflight、main worktree・active session context の事前条件、oracle file の編集境界、未コミット差分の扱いを確認する入口。
- agent call の失敗時処理、primary report、console・ログ・Windows toast、終了状態、および中断・排他制御を含むサブコマンド固有契約を扱う。

## Read this when
- `cmoc oracle edit` の起動条件、実行順序、2 回の agent call の責務や成否を確認するとき。
- oracle edit の prompt、oracle file 編集境界、差分維持、report またはログの仕様を変更・実装するとき。
- doctor preprocess、indexing preflight、session context、terminal result との連携を調査するとき。

## Do not read this when
- oracle file の内容自体の編集方針や判断基準を確認する場合は、本文が参照する `oracle_and_realization.md` などの正本仕様を直接読む。
- エディタ入力の詳細、Codex exec の共通規約、console・toast の一般仕様だけを確認する場合は、本文から参照される各正本文書へ直接進む。
- `cmoc oracle investigation` など別サブコマンドの固有挙動だけを扱う場合。

## hash
- 038bcad4cc0d4f0c581ebdd2515d6a3f4e2aa9ad915285621ed6dfd4d987176b

# `oracle_investigation.md`

## Summary
- oracle file に関するユーザーの調査指示を受け取り、oracle file を根拠とする調査結果を回答する Codex CLI の TUI を起動するサブコマンド。調査指示の入力、起動パラメータの構築、Codex CLI の TUI 起動までを扱う。oracle file の調査を開始する際の入口となる。

## Read this when
- oracle file に関する調査指示を受け取り、調査結果を TUI で回答する実行経路を確認するとき
- prompt editor input の lifecycle に従う調査指示の入力から、TUI 起動パラメータの構築と Codex CLI の起動までを確認するとき
- oracle file を扱う調査境界や、調査結果・変更の扱いを確認するとき

## Do not read this when
- oracle file 自体の具体的な仕様内容を調査するとき
- TUI 起動パラメータの正確な prompt 文面、prompt part、AgentCallParameter、選択理由を確認するときは、指定された builder を直接読む
- エディタ入力、oracle file を扱う判断基準、Codex CLI 起動時の詳細設定、Windows toast 通知の正本仕様を確認するときは、それぞれ指定された正本文書を直接読む

## hash
- eae3c5cd6f1887e9ac5d4c89c9f11d6c3c87587a438183de4b63bf30b280377d

# `oracle_review.md`

## Summary
- `cmoc oracle review` は、現在の oracle ファイル群を対象に、明白な仕様上の致命的問題や文意を損なう軽微な問題を agent call で列挙・統合・検証・採否判定し、人間向け Markdown レポートとして保存・提示するサブコマンド。レビュー対象の選択、所見の品質化、隔離 run、ユーザー中断時の部分結果、レポート形式と責務境界を定義する。
- レビュー処理の各段階における正確な agent call の構築は oracle review 用 builder 群へ、所見成立条件の伝達は oracle findings policy へ委譲する。実装や自動生成ファイルのレビュー、問題修正の提案、レビュー漏れの保証は責務外。

## Read this when
- oracle ファイルのスナップショットをレビューし、`session` または `full` スコープで所見を人間向けレポートにまとめる処理を実装・変更・確認するとき
- 所見の成立条件、fatal/minor の重大度、列挙・マージ・検証・採否判定ループの上限や dirty flag の扱いを確認するとき
- 隔離 run、未コミット差分の事前条件、ユーザー中断時の部分結果、レビュー結果の保存先や Markdown レポート形式を確認するとき

## Do not read this when
- oracle の具体的な記述内容やレビュー基準そのものを確認する場合は、ここではなく `oracle_and_realization.md`、対象 oracle、または所見 policy を直接読むとき
- agent call の prompt 構築や起動パラメータを変更・確認する場合は、この仕様全体ではなく対応する oracle review builder を直接読むとき
- 自動生成された `INDEX.md` や realization 実装のレビュー・修正を行うとき
- レビュー結果を受けた次の対応方針や oracle の改善案を検討するとき

## hash
- 78132879ba12bc37eedfb14996d9173410f40e25a021a4044b7765bf753ef610

# `realization_apply.md`

## Summary
- `realization apply fork` の目的、追従対象差分、単一の Codex agent call による realization file 追従、commit・report・run state 更新、エラー処理、join 後 hook を定義する仕様書。realization apply の fork lifecycle や oracle 変更の realization 反映手順を確認する入口であり、fork 固有の実行条件・終了結果・report 内容を扱う場合に読む。
- fork・join・abandon に共通する編集 run の lifecycle 詳細は編集 run 共通仕様を参照し、oracle と realization の適合性判断は oracle/realization 仕様を参照する。この文書は realization file の具体的な実装内容や INDEX.md 生成規則そのものを定義するものではない。

## Read this when
- realization apply fork の目的、引数、差分の始点・終点、追従範囲を確認するとき
- fork で実行する agent call の回数、cwd、起動パラメータ委譲、変更可能なファイル範囲を確認するとき
- fork の commit、report、run state、終了コード、エラー処理、feedback 記録、join 後 hook の要件を確認するとき

## Do not read this when
- fork・join・abandon に共通する lifecycle の詳細だけを確認したいときは、編集 run 共通仕様を直接読む
- oracle file と realization file の一般的な適合性基準を確認したいときは、oracle/realization 仕様を直接読む
- realization file の個別実装や、INDEX.md の内容・生成方法だけを確認したいとき

## hash
- e8d1a76adbd14bd2e6f2dc59d7d2e707339f449946ff220ae651621aab975e73

# `realization_refactor.md`

## Summary
- realization refactor fork の目的、refactor state の同期・選択・保存規則、current fork の unresolved target 管理、処理単位、完了・中断・エラー時の扱い、および report と join 後 hook の契約を定義する正本仕様。realization refactor fork の挙動や lifecycle、状態管理、終了結果を確認・変更するときの入口となる。

## Read this when
- realization refactor fork の実装、状態同期、調査対象選択、unresolved target、処理単位の commit、完了判定を確認するとき
- fork の中断・エラー処理、report、終了コード、終了イベントの仕様を確認するとき
- realization refactor と realization apply、feedback、共通 run lifecycle の責務境界を確認するとき

## Do not read this when
- 短い変更ループを担う realization apply の仕様だけを確認するときは、該当する realization apply の仕様へ進む
- fork と join、abandon に共通する lifecycle だけを確認するときは、明示的な join を必要とする編集 run の共通仕様へ進む
- oracle file と realization file の適合性判定そのものを確認するときは、oracle_and_realization.md の正本へ進む

## hash
- ab8ece599ea5b79f5a5ce8c447d6dc20e3bb4af94e8279b5fbee502cceb1f978

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
- `cmoc tui` サブコマンドの責務と実行手順を定義する正本文書。ユーザーのオリジナルプロンプトに cmoc 固有契約を注入し、構築済みの起動パラメータで AI Agent CLI/TUI を直接起動するまでを扱う。
- プロンプトのエディタ入力、全バックエンド共通の規定適用、indexing preflight、feedback observation、Windows toast 通知、および Codex CLI 起動時に必要な設定要素への委譲先を示す。

## Read this when
- `cmoc tui` の責務、引数、事前条件、実行手順を確認するとき
- TUI 起動時の cmoc 基本規定、installed skill、indexing preflight、feedback observation、終了通知の適用条件を確認するとき
- Codex CLI を `cmoc tui` から起動する際の起動コマンドや設定要素を確認するとき
- `build_tui_launch_tui_parameter` に委譲される prompt part、文面、起動パラメータの位置づけを確認するとき

## Do not read this when
- プロンプトエディタ入力の詳細なライフサイクルだけを確認する場合は、直接 `oracle/doc/app_spec/prompt_editor_input.md` を読むとき
- TUI 起動パラメータの正確な選択や文面だけを確認する場合は、直接 `oracle/src/oracle/acp_builder/tui/launch_tui.py` を読むとき
- oracle と realization の責務・適合性だけを確認する場合は、直接 `oracle/doc/app_spec/oracle_and_realization.md` を読むとき
- indexing、feedback observation、Windows toast、Codex CLI の詳細仕様だけを確認する場合は、それぞれ本書が示す正本を直接読むとき

## hash
- d3ef7e30924137554ad7007b13dc40fd3199058de016befdefca042d859b2eba
