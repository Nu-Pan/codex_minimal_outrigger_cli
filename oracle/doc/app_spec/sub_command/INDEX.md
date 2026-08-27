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
- `cmoc feedback report` の実装仕様を定める正本文書。feedback observation と feedback state を前提に、CLI 契約、report cut の固定、validation・deduplication・集約、normalization/verification agent の境界、正常 publication、`incomplete` 診断、中断・エラー処理、cleanup、終了コードを規定する。
- feedback report 処理の全体フローと、正常時の active generation 更新および異常時の current state 維持を確認するための入口となる。

## Read this when
- `cmoc feedback report` の挙動、事前条件、処理順序、report cut、候補検証、publication、再開、中断、終了コードを実装・レビュー・変更するとき。
- feedback observation と feedback state の関係、および正常 report・`incomplete` 診断 report・invocation summary report の保存仕様を確認するとき。

## Do not read this when
- raw observation の schema や観測記録そのものだけを確認する場合は、`feedback_observation.md` を直接読む。
- state、checkpoint、publication、cleanup の永続化契約だけを確認する場合は、`feedback_state.md` を直接読む。
- normalization または verification agent の prompt、schema、起動条件だけを確認する場合は、本文中で指定された各正本ファイルを直接読む。

## hash
- 46550b2ba44151982f293cc18532e824a7f6bcf23e66c4ae5ba4f60797ac372d

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
- `cmoc oracle edit` の目的、引数なしの実行契約、ユーザー指示からの prompt 構築、本命・仕様削減 agent call の順序と失敗条件を定義する。
- doctor preprocess、indexing preflight、main worktree と session branch の起動前検査、oracle file の編集境界、差分保持、primary report・ログ・通知の終了処理を確認するための上位仕様入口である。
- oracle edit の実行フローや agent call の起動条件・完了状態・報告形式を変更または調査するときに読む。

## Read this when
- `cmoc oracle edit` のサブコマンド実装、実行順序、起動可否、agent call の成否処理を確認するとき。
- oracle file の編集権限、既存差分の扱い、終了後の成果物・report・ログ・通知の契約を確認するとき。
- 関連する prompt editor、codex exec、doctor preprocess、indexing、console/log、toast の正本仕様との接続点を特定するとき。

## Do not read this when
- prompt editor の入力形式だけを確認したい場合は `prompt_editor_input.md` を直接読む。
- agent call の共通 retry、prompt 受け渡し、ログ保存規則だけを確認したい場合は `codex_exec_rule.md` を直接読む。
- oracle file の判断基準だけを確認したい場合は `oracle_and_realization.md` の該当節を直接読む。
- doctor preprocess、indexing、feedback、Windows toast の個別契約だけを確認したい場合は、それぞれの正本仕様を直接読む。

## hash
- ffb30e5c39db3456be71a0b56dfe595bd43d001867de6b48cd93cbb979732572

# `oracle_investigation.md`

## Summary
- 対象は、oracle file に関するユーザーの調査指示を受け取り、doctor 前処理と prompt editor の lifecycle を経て、指定 builder が構築したパラメータで Codex CLI の TUI を起動するサブコマンド仕様である。oracle file を根拠に調査し、結果を TUI で日本語中心に回答する際の意味上の責務と調査境界を確認する入口となる。

## Read this when
- oracle file の内容や判断基準についてユーザーから調査指示を受け付ける TUI 起動フローを確認するとき
- oracle investigation の実行手順、prompt editor input、TUI 起動パラメータの責務境界を確認するとき
- 調査結果の言語方針や oracle file・realization file の変更禁止を確認するとき

## Do not read this when
- 正確な prompt 文面、prompt part の選択、AgentCallParameter、または選択理由だけを確認したいときは、指定された launch TUI parameter builder を直接読む
- prompt editor input の正本仕様だけを確認したいときは、指定された prompt_editor_input.md を直接読む
- oracle file の変更判断基準だけを確認したいときは、指定された oracle_and_realization.md の該当節を直接読む
- Codex CLI の環境変数、preflight validation、引数上書き、または Windows toast 通知の詳細だけを確認したいときは、指定された各 app_spec 文書を直接読む

## hash
- 764b8c984e61315e8e752895fa5b4584b1e2ebca7f85aab655101de5f07997c1

# `oracle_review.md`

## Summary
- `cmoc oracle review` サブコマンドの正本仕様。oracle file を session または full スコープでレビューし、所見の列挙・統合・検証・採否判定を経て、人間向け Markdown レポートを保存・提示する。
- レビュー対象の選定、隔離 run、agent call の責務委譲、所見の成立条件と重大度、ユーザー中断時の確定結果の扱い、レポートの frontmatter・本文構成・終了結果を定義する。oracle レビューの実行フローや所見判定、レポート形式を確認する入口となる。

## Read this when
- `cmoc oracle review` の引数、事前条件、実行手順、終了経路を確認・変更するとき
- oracle file のレビュー対象範囲、所見の成立条件・重大度・採否判定を確認するとき
- 所見列挙・マージ・検証の agent call やループ上限の責務境界を確認するとき
- レビュー結果の保存先、frontmatter、本文セクション、Verdict の意味を確認するとき
- ユーザー中断時の部分結果や隔離実行の扱いを確認するとき

## Do not read this when
- レビュー対象の個別 oracle file の内容や、oracle と realization の一般的な関係だけを確認したいときは、それぞれの対象文書を直接読む
- agent call の具体的な prompt、prompt part、起動パラメータを確認したいときは、本文で委譲先として示された各 builder を直接読む
- run 隔離の共通仕様やサブコマンド中断の共通仕様を確認したいときは、本文で参照される `run_isolation.md` または `subcommand_interruption.md` を直接読む
- レポートを feedback observation または active issue へ変換する規則を確認したいときは、`feedback.md` を直接読む

## hash
- f00bee82741a154aaf44f5cc3de75b74cd5d14a665c251e10cef08beb1956122

# `realization_apply.md`

## Summary
- `realization apply fork` の目的、追従対象となる oracle file 差分、agent call の実行条件、想定内差分、エラー処理、report、join 後 hook を定める仕様。realization apply の fork 実行や結果確認における入口となる。
- 直近の git commit 群から始点・終点を決めて raw diff を構築し、単一の Codex agent call で realization file へ反映する一連の lifecycle を扱う。fork, join, abandon の共通 lifecycle は別の編集 run 仕様を参照する。

## Read this when
- realization apply の fork を実行、実装、検証、またはエラー処理する場合
- oracle file の commit 差分を realization file に反映する範囲や、agent call の回数・cwd・変更許可範囲を確認する場合
- fork report、終了コード、run state、feedback 記録、join 後の commit 更新を確認する場合

## Do not read this when
- fork, join, abandon に共通する lifecycle のみを確認したい場合は、共通仕様である editing_run.md を直接読む
- realization apply のファイル単位の網羅的な追従や refactor の仕様を確認したい場合
- oracle file と realization file の一般的な適合性基準を確認したい場合は、oracle_and_realization.md を直接読む
- 実行パラメータの正確な prompt、prompt part、起動パラメータの構築方法を確認したい場合は、launch_exec.py を直接読む
- feedback 収集の共通仕様を確認したい場合は、feedback.md を直接読む

## hash
- 3e0a3986d3b77710a528643f410c60b31da45381acec94633efc6a13d520aed2

# `realization_refactor.md`

## Summary
- realization refactor サブコマンドの正本仕様。oracle file と realization file を対象に、state 同期、調査・修正ループ、所見処理、commit、完了判定、report、interruption、error を定義する。
- 短い変更ループを担う realization apply とは別の workload であり、fork・join・abandon の共通 lifecycle や中断規則は指定された共通正本仕様へ委譲する。
- 調査対象の選択、current fork の unresolved target、refactor state の保存・同期、natural_completion と completed_with_unresolved の判定を確認する必要がある場合の入口となる。

## Read this when
- realization refactor fork の実行フロー、調査対象選択、state 更新、所見の正規化、変更確定を確認するとき
- realization refactor の完了条件、unresolved target の扱い、report 内容、終了コードや終了イベントを確認するとき
- realization file の追従調査・修正と、oracle file に対する適合性判断の責務境界を確認するとき

## Do not read this when
- 短い変更ループとしての realization apply の仕様だけを確認するとき
- fork・join・abandon の一般 lifecycle を確認するときは editing_run の正本仕様を直接読むとき
- ユーザー中断の共通動作だけを確認するときは subcommand_interruption の正本仕様を直接読むとき
- oracle file と realization file の適合性基準だけを確認するときは oracle_and_realization の該当節を直接読むとき
- Codex CLI の事後条件や変更 path 検証だけを確認するときは codex_exec_rule の正本仕様を直接読むとき

## hash
- cf90aa4585a4404040ad20973dc4f798995a445dfda41ba34bc52f56bbe985cb

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
- `cmoc session join` の正本仕様。アクティブな session branch を対応する home branch へマージし、session state を joined に更新して安全な場合のみ session branch を削除する完了処理を定義する。通常の汎用 git merge wrapper ではない。
- 引数、事前条件、doctor preprocess、branch 切替、no-ff merge、conflict 解消用 agent call、state 遷移、cleanup、primary report、エラー時の扱いを扱う。
- session join の merge 対象は session branch の実装成果に限られ、repository-local feedback state は対象外である。

## Read this when
- `cmoc session join` の引数、実行条件、merge 先・merge 元、または session 完了処理を確認するとき。
- merge conflict 発生時の conflict marker 解消手順、oracle file の扱い、agent call の委譲先を確認するとき。
- session state の更新、session branch cleanup、primary report の生成内容、エラー終了時の扱いを実装またはレビューするとき。

## Do not read this when
- session の作成、実行、再開、状態確認など、join 以外の session サブコマンドの仕様だけを確認するとき。
- repository-local feedback state の保存・集約・report cut・checkpoint の仕様を確認するときは、feedback 関連の正本仕様を直接読む。
- 通常の git merge の一般仕様や、session join と無関係な branch 操作の仕様を確認するとき。

## hash
- 20a98ef4853f417d06037b7d54e583513ff8acfcdd696a8d1faa16644c3bfe27

# `tui.md`

## Summary
- `cmoc tui` サブコマンドの責務、実行手順、プロンプト入力、AI Agent CLI/TUI 起動契約を確認するための入口。
- cmoc 固有規定の注入条件、indexing preflight、feedback observation、Windows toast 通知など、TUI 起動時に共通して適用される契約を確認するための入口。
- Codex CLI をバックエンドとして起動する場合の `codex` コマンド、`$CODEX_HOME`、preflight validation、引数による設定上書きの適用範囲を確認するための入口。

## Read this when
- `cmoc tui` の実行責務や実行手順を確認・変更するとき。
- TUI に渡すオリジナルプロンプトの受け取り方や、起動パラメータ構築後の起動契約を確認するとき。
- cmoc 固有規定、indexing preflight、feedback observation、Windows toast 通知の TUI 適用条件を確認するとき。
- Codex CLI 用の起動条件を確認するとき。

## Do not read this when
- プロンプトエディタ入力の正確な lifecycle、初期表示文面、完全 prompt skeleton を確認したいときは、正本として指定された `prompt_editor_input.md` とその参照先を直接読む。
- 正確な prompt part の選択、文面、起動パラメータ、選択理由を確認したいときは、`build_tui_launch_tui_parameter` の oracle src を直接読む。
- Codex CLI の環境変数、preflight validation、引数による設定上書きの詳細を確認したいときは、`codex_exec_rule.md` を直接読む。
- oracle と realization の責務・適合性、oracle review の所見、indexing、feedback observation、Windows toast 通知の詳細を確認したいときは、本文が指定する各正本文書を直接読む。

## hash
- c278a255224158dd0ea242117a5f3e9fa67eb7494abbb3966c70d1fe87c0a2f0
