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
- `cmoc feedback report` の責務と処理全体を定義するサブコマンド仕様。pending observation と直前の active state を report cut に固定し、検証・重複排除・集約・候補化・normalization・verification を経て、正常な active generation と Markdown report、または `incomplete` 診断 report を publication する。
- CLI の引数、事前条件、state の整合性検証、排他、再開、cleanup、ユーザー中断、エラー時の扱いを確認する必要がある。
- feedback report の実装や挙動仕様を確認するときの入口であり、raw observation の正本、state/checkpoint/publication/cleanup の正本、normalization/verification agent の prompt・schema の正本へ分岐する。

## Read this when
- `cmoc feedback report` の実装、CLI 契約、事前条件、report cut、処理順序、候補の検証、publication、再開・中断、report 保存、終了コードを確認するとき。
- 正常な `ok`/`attention` result と `incomplete` result の違い、active generation や current pointer の更新条件を確認するとき。
- feedback report のテストで、validation、deduplication、threshold、verification、cleanup、終了コードの挙動を確認するとき。

## Do not read this when
- raw observation の schema、保存、受理規則を確認したいときは `oracle/doc/app_spec/feedback_observation.md` を直接読む。
- state root、checkpoint、publication、current pointer、cleanup の正本仕様を確認したいときは `oracle/doc/app_spec/feedback_state.md` を直接読む。
- 中断共通動作を確認したいときは `oracle/doc/app_spec/subcommand_interruption.md` を直接読む。
- normalization agent の正確な prompt、起動パラメータ、選択理由、Structured Output schema を確認したいときは `oracle/src/oracle/acp_builder/feedback/normalize_issue.py` と `normalize_issue.json` を直接読む。
- verification agent の正確な prompt、起動パラメータ、選択理由、Structured Output schema を確認したいときは `oracle/src/oracle/acp_builder/feedback/verify_issue.py` と `verify_issue.json` を直接読む。

## hash
- 6a098ea8551e07e9fd087a04d87f475b2498ce6107925be2c16d2b464029d259

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
- oracle file のユーザー指示を受け取り、本命 agent call と仕様削減 agent call を直列実行する `cmoc oracle edit` サブコマンドの仕様を定義する。
- prompt editor、doctor preprocess、indexing preflight、起動前条件、Codex exec の構成と実行順序を扱う。
- oracle file のみを編集対象とし、差分の扱い、終了状態、primary report、console・ログ・Windows toast、feedback の記録、および排他制御の境界を定める。
- oracle edit の実装・仕様変更時はこのファイルを入口とし、prompt 構築や editor input、Codex exec の受け渡し、doctor・indexing、miscellaneous な判断基準の詳細は本文が指定する対応する oracle 文書・実装へ進む。

## Read this when
- `cmoc oracle edit` の実行順序、agent call 前の検査、2 回の独立した Codex session、失敗時の扱いを確認したいとき。
- oracle file だけに限定された agent の編集境界、未コミット差分の扱い、終了後の状態保持を確認したいとき。
- primary report の保存要件、共通 terminal result、サブコマンドログ、Codex call log、Windows toast、feedback observation の扱いを確認したいとき。
- lock file、process 重複検出、run section、worktree lifecycle などの排他・中断制御を導入すべきか判断するとき。

## Do not read this when
- prompt editor input の初期表示や skeleton の正確な構築を確認したい場合は、指定された `prompt_editor_input.md` と参照先を直接読む。
- agent call の prompt part、起動パラメータ、retry・resume、stdin 渡し、完全 prompt 保存の規約を確認したい場合は、指定された `codex_exec_rule.md` と launch builder を直接読む。
- doctor preprocess や indexing の変更・commit 規約を確認したい場合は、それぞれの指定 oracle 文書を直接読む。
- oracle file を扱う一般的な判断基準や用語を確認したい場合は、指定された `misc_spec.md` を直接読む。
- このサブコマンドの realization 実装、通常の test、または INDEX.md 自体の編集方法を確認したい場合。

## hash
- 49b8972f9a521ff5d8868fe2db05478caef45f4cfa1d28a04ec6aa9277877c7e

# `oracle_investigation.md`

## Summary
- `cmoc oracle investigation` のサブコマンド仕様を定義する文書。oracle file を対象にした調査指示をエディタ入力で受け取り、doctor preprocess と専用 builder を経て Codex CLI の TUI を起動し、調査結果をユーザーへ返すまでの責務・境界・起動規則をまとめる。oracle file の調査フローや TUI 起動仕様を確認・変更するときの入口であり、入力 lifecycle や起動パラメータの正確な実装詳細は参照先の正本へ進む。

## Read this when
- oracle file に関する調査用サブコマンドの挙動、実行手順、入力方法、TUI 起動境界を確認するとき
- oracle investigation の起動パラメータ構築や Codex CLI 起動規則を確認・変更するとき
- 調査結果の言語、oracle file・realization file の変更禁止、indexing preflight の扱いを確認するとき

## Do not read this when
- prompt editor input の lifecycle や初期表示・prompt skeleton の正確な構築だけを確認したいときは、直接その正本と参照先の oracle src を読む
- `build_oracle_investigation_launch_tui_parameter` の具体的な prompt 文面、prompt part、`AgentCallParameter`、選択理由だけを確認したいときは、直接 builder 実装を読む
- oracle file の判断基準だけを確認したいときは misc_spec.md を、Codex CLI の環境変数・preflight・引数上書きだけを確認したいときは codex_exec_rule.md を直接読む
- Windows toast 通知の仕様だけを確認したいときは windows_toast_notification.md を直接読む

## hash
- cb23eb75c1b90ad7f963a5a7dae4a262ced07bf413b2499a3820c2623003e1ef

# `oracle_review.md`

## Summary
- この oracle file は、現在の oracle 全体またはセッション差分に対して、隔離実行内で Codex CLI による所見の列挙・統合・検証・採否判定を反復し、最終的なレビュー結果を Markdown レポートとして保存・提示する `cmoc oracle review` の仕様を定義する。レビュー対象の選定、前提条件、割り込み時の扱い、finding の成立条件と重大度、レポートの構造および責務境界を確認するための入口である。

## Read this when
- oracle file の致命的問題をレビューするサブコマンドの挙動、対象スコープ、反復する agent call、finding の採否基準を確認するとき
- oracle review レポートの保存先、frontmatter、本文セクション、verdict の意味を確認するとき
- レビューの事前条件、隔離実行、ユーザー中断、finding ID 管理、責務境界を調べるとき

## Do not read this when
- oracle review の agent call 用 prompt の正確な構築方法を確認したいときは、本文が案内する acp_builder の review 実装を直接読む
- 所見成立条件そのものの共通定義を確認したいときは、本文が案内する oracle_findings.py と misc_spec.md を直接読む
- run の隔離実行の共通仕様や中断の共通動作だけを確認したいときは、本文が案内する各 app_spec を直接読む

## hash
- b7cdbbd89bff8bf86541f1fbcf23c0cd48bc91a0e217f63fb015e878486c53c6

# `realization_apply.md`

## Summary
- `cmoc realization apply fork` の目的、追従対象となる oracle 差分、agent call の実行条件、エラー処理、report、join 後 hook を定める realization apply 仕様。realization apply の fork lifecycle と、oracle file の変更を realization file へ反映する判断・完了条件を確認する入口となる。

## Read this when
- realization apply の fork を開始、実行、完了判定、エラー処理する場合
- 追従対象の git diff の始点・終点、oracle file の rename、作業範囲を確認する場合
- fork report の保存内容、終了状態、終了コード、feedback 情報を確認する場合
- apply fork の join 後に session state を更新する処理を確認する場合

## Do not read this when
- fork・join・abandon に共通する lifecycle 自体を確認したい場合は、共通仕様である editing_run.md を直接読む
- oracle file と realization file の一般的な適合性判断を確認したい場合は、misc_spec.md を直接読む
- 正確な agent call の prompt、prompt part、起動パラメータ、選択理由を確認したい場合は、指定された launch_exec.py を直接読む
- feedback の共通収集・報告仕様を確認したい場合は、feedback.md を直接読む
- ファイル単位の網羅的な realization 追従や refactor の仕様を確認したい場合

## hash
- 18af449e0b9fc6ba0079ed4017f47163398b54076377c32feb701b87004328fe

# `realization_refactor.md`

## Summary
- realization refactor fork の workload 仕様を定義する正本文書である。oracle file と realization file を起点に、current fork の unresolved target を管理しながら、調査・修正・検証・commit を繰り返す処理の入口となる。
- refactor state の schema、entry 同期、調査対象の選択順、1 処理単位の結果判定、完了理由、report、ユーザー中断・エラー処理を扱う。短い変更ループの realization apply や、共通の fork・join・abandon lifecycle の詳細そのものは扱わない。

## Read this when
- realization refactor fork の実装、状態管理、調査対象選択、処理ループ、完了条件を確認・変更するとき
- current fork の unresolved target と refactor state の関係、調査結果の正規化、変更 path の検証を確認するとき
- refactor fork の report、終了イベント、ユーザー中断、続行不能エラーの扱いを確認するとき

## Do not read this when
- 短い変更ループを担う realization apply の仕様だけを確認するとき
- 共通の fork・join・abandon lifecycle だけを確認するときは、共通 lifecycle の正本仕様を直接読む
- oracle file と realization file の適合性判定基準だけを確認するときは、本文が参照する適合性仕様を直接読む

## hash
- 8a7ca9d5e7a2c8256e4fd4666d24f1abc6d8820060fce9ab2a7c3bb725cb4e8f

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
- `cmoc session join` は、active/ready 状態の session 作業ブランチに未コミット差分がないことなどを検証したうえで、session 作成時の home branch へ session branch を `--no-ff` merge し、session state を joined に更新する完了処理の仕様を定める。
- home branch の進行、merge conflict、conflict 解消用 agent call、session branch の安全な cleanup、想定外エラー時の扱いを含む。repository-local feedback state は merge 対象外として明確に分離される。
- session join の実装、事前条件、merge/conflict 解消、session state 遷移、primary report、エラー時の次操作を確認する際の正本仕様であり、実装やテストの挙動確認の入口になる。

## Read this when
- `cmoc session join` の引数、事前条件、実行手順、対象 branch を確認するとき
- session branch を home branch へ merge する処理や、home branch が進んでいる場合の挙動を実装・検証するとき
- merge conflict の解消手順、oracle file の扱い、conflict 解消用 agent call の規則を確認するとき
- session state の joined 遷移、branch cleanup、安全性確認、primary report の保存内容を確認するとき
- session join と repository-local feedback state の責務境界を確認するとき

## Do not read this when
- 通常の git branch 間 merge wrapper の仕様を確認したいとき
- session join の内部実装で参照する conflict 解消 prompt の正確な生成規則を確認したいときは、直接 `oracle/src/oracle/acp_builder/session/join/conflict_resolution.py` を読む
- エラー分類やスタックトレースの詳細を確認したいときは、直接 `oracle/doc/app_spec/error_handling.md` を読む
- repository-local feedback state のデータ構造や report の個別仕様だけを確認したいときは、それぞれの専用仕様を直接読む

## hash
- 7ec6ed0257d53791135ba673285fdb808a6f179e47cf6d5c0a7b3f185a2d052e

# `tui.md`

## Summary
- `cmoc tui` サブコマンドの責務、実行手順、プロンプト入力、TUI 起動契約を定義する正本。doctor preprocess から起動パラメータ構築、AI Agent CLI/TUI 起動までの挙動を確認する入口。
- 全バックエンド共通の prompt 適用条件、indexing preflight、feedback observation、Windows toast 通知など、TUI 起動時の横断契約を確認するときに読む。
- Codex CLI バックエンドの起動コマンド、環境変数、preflight validation、引数による設定上書きの扱いを確認するときに読む。関連文書の詳細な入力形式・選択ロジック・通知仕様そのものを確認する場合は、本書から参照される各 oracle 文書へ進む。

## Read this when
- `cmoc tui` の実行フロー、引数、事前条件、未コミット差分を許容する挙動を調査・変更するとき。
- ユーザープロンプトのエディタ入力から TUI 起動までの契約を確認するとき。
- バックエンド共通の prompt 注入、indexing、feedback、通知、または Codex CLI 固有の起動条件を確認するとき。

## Do not read this when
- doctor preprocess、prompt editor input、起動パラメータ構築、indexing、feedback、通知の詳細実装や正確な文面だけを確認したい場合は、本文が指定する各 oracle 文書・oracle src を直接読む。
- `cmoc tui` 以外のサブコマンドの責務や実行契約を調査する場合。

## hash
- 3ea1490ea492fcf43de9e43db27f2e65a2f6df2cb7445a804326169a68de2de1
