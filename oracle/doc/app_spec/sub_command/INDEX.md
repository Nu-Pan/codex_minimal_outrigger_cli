# `doctor.md`

## Summary
- `cmoc doctor` のコマンド仕様。cmoc の実行可能性を検証・修復する doctor の呼び出し条件、引数、実行手順、および全終了経路で保存する primary report の要件を確認するための入口。doctor コマンドの挙動や診断結果の報告形式を変更・レビューするときに読む。

## Read this when
- `cmoc doctor` の仕様、引数、実行手順を確認するとき
- doctor preprocess の呼び出しや、doctor 実行要約を保存する primary report の要件を実装・検証するとき
- doctor の終了コード、warning・error、次の操作、および診断用サブコマンドログの報告内容を確認するとき

## Do not read this when
- doctor preprocess 自体の詳細な処理仕様だけを確認したいとき
- doctor 以外のサブコマンドの仕様を確認するとき
- 保存済み report の具体的な実例や生成物だけを調査するとき

## hash
- 757ea535cbff4360eca1328b31ea3fb056af742ab9d6d7fe15cc06b9928ea399

# `editing_run.md`

## Summary
- 編集 run の共通 lifecycle 仕様を定義する正本。`realization apply fork` と `realization refactor fork` が開始する run の対象範囲、同時実行制約、fork 前提・開始処理、編集責務、`cmoc run join`／`cmoc run abandon` の事前条件・差分処理・state 遷移・merge／cleanup、report と terminal result の要件を扱う。
- realization 系 workload の fork、run の join または abandon、未 join run の同時実行制御、想定内差分や run state、run lifecycle の report 仕様を変更・実装・レビューするときの共通仕様への入口である。個別 workload の編集内容や refactor state 同期の詳細は、ここで定める共通境界を確認したうえで各 workload 固有仕様へ進む。

## Read this when
- `cmoc realization apply fork` または `cmoc realization refactor fork` の開始条件・開始処理・編集責務を確認するとき
- `cmoc run join` または `cmoc run abandon` の引数、事前条件、差分検査、merge・破棄・cleanup、state 遷移を変更または検証するとき
- session と未 join の編集 run の同時実行境界、run branch／worktree の扱い、想定外差分の扱いを確認するとき
- fork・join・abandon の report や terminal result に必要な共通項目と終了経路を確認するとき

## Do not read this when
- `cmoc session join` や `cmoc session abandon` の外側の session lifecycle だけを扱うとき
- `cmoc oracle edit`、read-only の investigation／review、cmoc 自身による機械的更新、session join の conflict 解消だけを扱うとき
- realization apply または realization refactor の workload 固有の編集内容・成果物・hook を確認する場合は、共通 lifecycle の確認が不要なら各 workload 固有仕様を直接読むとき
- feedback data の保存や publication の詳細だけを扱うときは、repository-local feedback 仕様を直接読むとき

## hash
- f4bcbffb2fa4d332df00c33ea54768a6ab3cea213c02ba644d2dc47148beb253

# `feedback_report.md`

## Summary
- `cmoc feedback report` の report processing と publication 全体の正本仕様。pending observation と active state の report cut 固定から、validation、機械的な deduplication・集約、candidate 形成、normalization/verification、正常 publication または `incomplete` 診断、再開・中断、report 保存、終了コードまでを定義する。feedback report の実装や挙動仕様を確認する際の入口となる。

## Read this when
- `cmoc feedback report` の CLI 契約、事前条件、report cut、処理順序、validation、machine/agent observation の扱いを確認するとき。
- normalization または verification の agent 呼び出し条件、許可する入力、Structured Output の受理条件を確認するとき。
- 正常 report、`incomplete` 診断 report、invocation summary report の publication 条件、state 維持、cleanup、再開、および終了コードを確認するとき。

## Do not read this when
- raw observation の schema、canonical hash、detector rule、recurrence window、threshold の正本を確認する場合は `feedback_observation.md` を直接読む。
- current pointer、active generation、checkpoint、publication、cleanup の state 遷移を確認する場合は `feedback_state.md` を直接読む。
- normalization agent の具体的な prompt、起動パラメータ、選択理由、schema を確認する場合は `normalize_issue.py` と `normalize_issue.json` を直接読む。
- verification agent の具体的な prompt、起動パラメータ、選択理由、schema を確認する場合は `verify_issue.py` と `verify_issue.json` を直接読む。
- 中断要求後の共通処理だけを確認する場合は `subcommand_interruption.md` を直接読む。

## hash
- e6631c1ac19d09a60dd100d200639e235a13e8513b64dbf05a674c93399be47a

# `indexing.md`

## Summary
- `cmoc indexing` の実行、事前条件、doctor preprocess、明示的なインデクシング、自動 git commit の流れを定義するサブコマンド仕様です。
- 正常終了とエラー終了の全経路で保存する primary report の内容、保存先、commit ID の扱いを確認できます。
- インデクシング処理の詳細は、本文が参照するインデクシング仕様への入口として扱います。

## Read this when
- `cmoc indexing` のコマンド仕様や実行条件を確認するとき。
- インデクシング前処理、実行、差分の commit、および終了時の report 要件を確認するとき。
- 事前条件違反や doctor preprocess 失敗を含む終了経路の報告内容を確認するとき。

## Do not read this when
- インデクシング処理そのものの詳細仕様を確認したいときは、本文が参照するインデクシング仕様を直接読む方が適切です。
- `cmoc indexing` 以外のサブコマンドの挙動を確認したいとき。

## hash
- 6da65bf626302c7e09422df55b857ba32f68cd979df32eb3e6a012829058e684

# `oracle_edit.md`

## Summary
- `cmoc oracle edit` サブコマンドの挙動仕様を定義する正本文書。oracle file 編集指示の受付から、doctor preprocess、indexing preflight、起動条件検査、本命・仕様削減の2回の独立した agent call、終了状態、primary report、ログ、通知、差分保持、中断・排他制御までを扱う。oracle edit の実装仕様や関連する app_spec との整合性を確認・変更するときの入口となる。

## Read this when
- `cmoc oracle edit` の実行順序、起動可否、agent call の構成または編集境界を確認するとき。
- 本命 agent call 後の仕様削減 agent call の判断材料や失敗時の扱いを確認するとき。
- oracle edit の終了状態、primary report、console・ログ・Windows toast、未コミット差分の扱いを確認するとき。
- oracle file 編集に関する実装や関連仕様が、このサブコマンドの契約に適合しているか確認するとき。

## Do not read this when
- oracle edit 以外のサブコマンドの仕様だけを確認する場合。
- prompt editor input や codex exec の受け渡し規則など、本文書が正本として委譲している個別仕様を直接確認する場合。
- doctor preprocess、indexing、oracle と realization の一般規則そのものを確認する場合は、本文書ではなく対応する app_spec または oracle file を直接読む場合。

## hash
- 7dbd210ffed031641017291d6f4b428c54a84cb787926385240942f83568984e

# `oracle_investigation.md`

## Summary
- oracle file に関するユーザーの調査指示を受け取り、正本 oracle file を根拠に調査結果を回答する Codex CLI の TUI を起動するサブコマンド仕様。入力 lifecycle、起動パラメータ構築、Codex CLI 起動、調査境界、結果提示と変更禁止事項を定める。oracle investigation の起動手順や責務境界を確認する入口。

## Read this when
- oracle file に関する調査指示を受け付けるサブコマンドの挙動を確認するとき
- oracle file を根拠とする調査用 TUI の起動手順、入力 lifecycle、起動パラメータ、調査結果の扱いを確認するとき
- oracle investigation と通常の TUI 起動や agent call の責務境界を確認するとき

## Do not read this when
- oracle file の具体的な内容や判断基準そのものを調査するとき
- エディタ入力の正確な文面や lifecycle の詳細を確認するときは、参照先の prompt editor input 正本を直接読む場合
- TUI 起動パラメータの正確な prompt、prompt part、AgentCallParameter、選択理由を確認するときは、指定された builder 実装を直接読む場合
- Codex CLI の共通実行設定や Windows toast 通知の仕様だけを確認するときは、指定された正本文書を直接読む場合

## hash
- a9ecac9d87203a541c19e0472677b6d18438eed2a71cdd234976f0adeb872181

# `oracle_review.md`

## Summary
- `cmoc oracle review` のサブコマンド仕様。oracle file を対象に、指定スコープで所見を列挙・統合・検証・判定し、レビュー結果を Markdown レポートとして保存・提示する一連の処理を定義する。
- レビューの事前条件、隔離実行、ユーザー中断時の扱い、所見の成立条件と重大度、agent call の責務分担、レポートの構造・判定値・保存先を扱う。oracle レビューの挙動やレポート仕様を確認する際の入口であり、詳細な隔離実行や中断の規則は参照先の仕様へ進む。

## Read this when
- `cmoc oracle review` の引数、事前条件、実行手順、スコープ、ループ上限を確認するとき
- oracle file の所見成立条件、重大度、採否判定、検証およびマージの扱いを確認するとき
- レビューの中断時の確定結果や、レポートの保存先・frontmatter・本文構成を確認するとき
- oracle review 用 agent call の責務や、関連する builder・policy 仕様への入口を確認するとき

## Do not read this when
- 隔離実行の共通動作だけを確認する場合は `oracle/doc/app_spec/run_isolation.md` を直接読むとよい
- サブコマンド共通の中断規則だけを確認する場合は `oracle/doc/app_spec/subcommand_interruption.md` を直接読むとよい
- oracle と realization の一般的な判断基準だけを確認する場合は `oracle/doc/app_spec/oracle_and_realization.md` を直接読むとよい
- 実装上の agent prompt、prompt part、起動パラメータの詳細だけを確認する場合は本文が指定する各 builder と `oracle_findings.py` を直接読むとよい

## hash
- 6716f9bf92f6584dbe593719c1d4eaf8f845c5f2357ee53cdbe604a3d9fc5ac4

# `realization_apply.md`

## Summary
- realization apply fork の正本仕様。直近の git commit 差分から oracle file の変更を特定し、単一の Codex agent call で realization file へ追従させる fork の目的、対象範囲、実行手順、エラー処理、report、join 後 hook を定義する。fork の共通 lifecycle は別の editing run 仕様を入口とする。

## Read this when
- realization apply fork の追従要否、差分の始点・終点、agent call の制約、変更可能なファイル範囲を確認するとき
- fork の実行手順、終了状態、report 保存内容、終了コード、feedback 収集、join 後の session 更新を実装・検証するとき

## Do not read this when
- fork, join, abandon に共通する lifecycle の一般仕様だけを確認したいときは editing run の正本を直接読む
- oracle file と realization file の適合性基準だけを確認したいときは oracle_and_realization.md を直接読む
- agent call parameter の構築方法や prompt 選択を確認したいときは launch_exec.py を直接読む

## hash
- 02f3244746af33b6fbcacb9859d6210a022193c83a54bc0af08d9d1621ad160a

# `realization_refactor.md`

## Summary
- oracle file と realization file の適合性調査・修正を、current fork の unresolved target を除き、未調査要求がなくなるまで繰り返す realization refactor fork の正本仕様。
- refactor state の同期、調査対象の選択、1 処理単位の変更検証・状態更新・commit、fork 完了条件を定める。
- unresolved 所見を含む正常完了、自然完了、ユーザー中断、その他のエラーにおける run state、report、終了コード、および join 後の扱いを定める。
- 短い変更ループを担う realization apply とは異なり、ファイル単位の追従調査全体を扱う workload の入口である。

## Read this when
- realization file の適合性を oracle file と対比して調査・修正するとき。
- realization refactor fork の対象選択、調査履歴、unresolved target、cycle、loop、完了条件を確認するとき。
- agent call の変更 path 検証、処理単位の commit、refactor state 同期、生成 report の要件を確認するとき。
- この fork の中断、続行不能エラー、completed_with_unresolved、joinable 状態の扱いを確認するとき。

## Do not read this when
- 短い変更ループの realization apply の動作だけを確認するとき。
- fork・join・abandon の共通 lifecycle だけを確認するときは、共通の編集 run 仕様を直接読む。
- oracle file に対する realization file の適合性基準そのものを確認するときは、正本の oracle_and_realization 仕様を直接読む。
- refactor state の JSON schema や oracle file・realization file の列挙規則だけを確認するときは、それぞれの正本仕様を直接読む。

## hash
- 845de570bd171356d6e548dd563f27bafdc6d284471931521d727d25a8c43a41

# `session_abandon.md`

## Summary
- `cmoc session abandon` の正規仕様を定義するエントリー。session を本流へ merge せず破棄する操作について、実行条件、破棄対象と保護対象、cleanup 手順、状態遷移、失敗時の rollback、primary report 要件を確認するための入口。session の abandon 実装、CLI 挙動、エラー経路、report 保存仕様を扱う作業では、session の join や run abandon の仕様ではなく本対象を読む。

## Read this when
- `cmoc session abandon` の挙動や事前条件を実装・検証するとき
- session branch の破棄、home branch への切替、session state の abandoned 遷移を扱うとき
- abandon の失敗時 rollback、cleanup、primary report の内容や終了経路を確認するとき

## Do not read this when
- session 成果物を本流へ取り込む `cmoc session join` の仕様だけを確認するとき
- 未 join の編集 run を破棄する `cmoc run abandon` の仕様だけを確認するとき
- 既に join 済みの結果を取り消す rollback の仕様を確認するとき

## hash
- a676bb88b4bf61db7ec4360a1547bca344d7bd6e76c29d97ffb2e4495ee074f0

# `session_fork.md`

## Summary
- 対象は `cmoc session fork` の正本仕様で、現在のローカルブランチからセッション用ブランチを作成・checkoutし、セッション状態ファイルを初期化する処理の入口である。引数、実行前提、ブランチ命名、分岐元制約、状態保存、終了時の primary report 要件を確認したい場合に読む。
- セッション fork の正常終了・エラー終了を含む報告内容や、doctor preprocess、事前条件違反時の扱い、rollback・残存資源・診断ログの要約要件を確認する際の仕様上の入口でもある。

## Read this when
- `cmoc session fork` の引数、実行可能な checkout 状態、未コミット差分や既存 active session によるエラー条件を確認するとき
- セッションブランチの作成元、命名規則、session ID、状態ファイルの初期状態を確認するとき
- fork 実行時の primary report の保存先、Front Matter の必須情報、終了経路ごとの報告内容を確認するとき

## Do not read this when
- session fork 以外のサブコマンドの仕様や、一般的な Git ブランチ操作だけを確認したいとき
- 実装上の責務配置やテスト実行手順を確認したいときは、対応する設計・テストの正本資料を直接読む

## hash
- 5843e517d87391cc3b4e5540d04cf9353b22db917be9cd6816e71813e389c079

# `session_join.md`

## Summary
- `cmoc session join` のセッション完了処理を定義する仕様書。現在のセッションブランチを対応するホームブランチへマージし、事前検証、conflict 解消、session state 更新、条件付き cleanup、primary report 保存までの終了経路を扱う。セッション join の実装・挙動・エラー処理・conflict 解消・report 要件を確認する際の入口となる。

## Read this when
- `cmoc session join` の引数、事前条件、実行手順、merge 対象を確認するとき
- session branch と home branch の merge、home branch が進んでいる場合の扱い、または conflict 解消手順を実装・検証するとき
- session state の遷移、session branch cleanup、primary report の項目や保存条件を確認するとき
- repository-local feedback state を session join の merge 対象外として扱う必要があるとき

## Do not read this when
- 通常の git branch 間 merge wrapper の仕様を確認したいとき
- session 作成・実行・離脱など、session join 以外の subcommand の挙動を確認するとき
- repository-local feedback state 自体の管理仕様や Markdown report の一般仕様を確認するときは、それぞれの専用仕様書を直接読むとき

## hash
- b8ac3e16a06b2e3bbfb99b931d74916739ab12c21a7a4da353344a340d8d9800

# `tui.md`

## Summary
- `cmoc tui` サブコマンドの意味上の責務、実行手順、プロンプトエディタ入力、AI Agent CLI/TUI 起動時の共通契約と Codex CLI 固有条件を定義する。
- TUI の正確な prompt part、起動パラメータ、選択理由は oracle の `build_tui_launch_tui_parameter` に委譲され、関連する正本仕様への入口を提供する。

## Read this when
- `cmoc tui` の起動条件、引数、事前条件、実行フローを確認するとき
- プロンプトエディタ入力から AI Agent CLI/TUI 起動までの契約を確認するとき
- cmoc 基本規定、installed skill、indexing preflight、feedback observation、Windows toast 通知の TUI 適用条件を確認するとき
- Codex CLI バックエンドでの起動コマンド、環境変数、preflight validation、引数上書きの扱いを確認するとき

## Do not read this when
- プロンプトエディタ入力の正確な lifecycle や prompt skeleton の構築方法だけを確認したいときは、直接 `prompt_editor_input.md` と参照先の oracle src を読む
- 起動パラメータの具体的な内容や選択理由だけを確認したいときは、直接 `launch_tui.py` の `build_tui_launch_tui_parameter` を読む
- oracle file と realization file の責務・適合性、oracle review の所見成立条件だけを確認したいときは、直接 `oracle_and_realization.md` または `oracle_review.md` を読む
- indexing、feedback observation、Windows toast 通知の詳細仕様だけを確認したいときは、それぞれの正本仕様を直接読む

## hash
- 10c7afb3581d1a936342b6939c9301e54e5d0f997bfa25e0fc04b26205612d97
