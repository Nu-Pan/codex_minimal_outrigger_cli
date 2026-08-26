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
- `cmoc feedback report` の CLI 契約、事前条件、report cut の固定、観測の検証・集約・候補化、normalization/verification、正常 publication と incomplete 診断、再開・中断・cleanup、report 保存形式、終了コードを定義する正本仕様。feedback report の実装方針や挙動条件を確認する入口であり、raw observation の形式や state の詳細は指定された別の正本仕様へ委譲する。

## Read this when
- `cmoc feedback report` の入力制約、前提状態、処理順序、候補判定、publication、再実行、中断、エラー処理を確認・変更するとき。
- 正常 report と `incomplete` 診断 report の内容、保存先、current pointer、終了コードの契約を確認するとき。

## Do not read this when
- raw observation の schema や記録規則だけを確認したい場合は `feedback_observation.md` を直接読む。
- state、checkpoint、publication、cleanup の永続化規則だけを確認したい場合は `feedback_state.md` を直接読む。
- normalization または verification agent の正確な prompt、起動条件、Structured Output schema を確認したい場合は、対応する oracle 実装・schema を直接読む。
- サブコマンド共通の中断動作だけを確認したい場合は `subcommand_interruption.md` を直接読む。

## hash
- cf3822c662469562b104660c8578545ef85cc3d11304800c19dc2f40bf81d5b8

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
- `cmoc oracle edit` サブコマンドの目的、引数、ユーザー指示からの prompt 構築、本命・仕様削減 agent call の実行順序と判断条件を定義する。doctor preprocess、indexing preflight、実行前検査、失敗時の終了、差分維持、primary report・ログ・通知の扱いまでを対象とする。
- oracle file の編集フローや agent の編集境界、Git 操作禁止、session/worktree lifecycle 非使用、既存差分との非分離など、`cmoc oracle edit` 固有の運用契約を確認するための仕様入口である。

## Read this when
- `cmoc oracle edit` の実装、実行順序、起動可否判定、agent call の retry・失敗処理を変更または検証するとき
- oracle edit における prompt editor、indexing、oracle file 編集権限、primary report、console・Codex call log・Windows toast の責務境界を確認するとき
- 本命 agent call と仕様削減 agent call の入力・独立性・成功条件を確認するとき

## Do not read this when
- oracle file の編集判断基準そのものを確認する場合は、本文が参照する `oracle_and_realization.md` を直接読むとよい
- prompt editor の入力 lifecycle や完全な prompt skeleton を確認する場合は、本文が正本として指定する `prompt_editor_input.md` と参照先を読むとよい
- codex exec の prompt 引き渡し、retry、ログ保存規約だけを確認する場合は、本文が参照する `codex_exec_rule.md` を直接読むとよい
- doctor preprocess、indexing、console・ファイルログ、Windows toast、feedback の詳細規約だけを確認する場合は、それぞれ本文が指定する正本文書を読むとよい

## hash
- 9e517e022921d9bcfa9a6679db4ff999f3245a1c8c2e990eae8706cd23e06ff6

# `oracle_investigation.md`

## Summary
- oracle file に関するユーザーの調査指示をエディタから受け取り、oracle file を根拠とする調査を行う Codex CLI の TUI を起動するサブコマンド仕様。入力 lifecycle、TUI 起動パラメータ構築、Codex CLI 起動時の設定、調査結果とファイル変更の扱いを定める。

## Read this when
- oracle file に関する調査指示を受け付ける TUI の起動フローや責務を確認するとき
- oracle investigation の prompt 入力、起動パラメータ、Codex CLI 起動方法、調査境界を変更または確認するとき
- 調査結果の回答方法や oracle file・realization file の変更禁止を確認するとき

## Do not read this when
- oracle file の調査対象そのものの内容や判断基準を確認したい場合は、記載された oracle の正本文書を直接読むとき
- エディタ入力 lifecycle の詳細や prompt skeleton の正確な構築を確認したい場合は、prompt_editor_input.md と参照先の oracle src を直接読むとき
- Codex CLI の共通起動規則や Windows toast 通知の詳細だけを確認したい場合は、各正本文書を直接読むとき

## hash
- f1a081d61ed149b79831e68377876a6a53252f341286485c547342d664db937d

# `oracle_review.md`

## Summary
- `cmoc oracle review` の責務、引数、事前条件、実行手順、agent call、隔離実行、所見の成立条件・重大度・検証・採否、レポート形式と保存方法を定義する正本仕様。
- oracle file のスナップショットを対象に、セッションまたは全体スコープで所見を列挙・統合・検証・判定し、Markdown レポートとして人間へ提示する処理の入口。

## Read this when
- `cmoc oracle review` の引数、事前条件、処理フロー、割り込み時の扱いを確認するとき
- oracle file のレビュー対象範囲、所見の成立条件・重大度・採否判定を確認するとき
- レビュー結果の frontmatter、本文構成、保存先、終了結果を実装・検証するとき
- 隔離実行やレビュー用 agent call の責務境界を確認するとき

## Do not read this when
- レビュー対象となる個別 oracle file の内容や仕様を確認したいとき
- run の隔離実行そのものの共通仕様を確認したいときは、`oracle/doc/app_spec/run_isolation.md` を直接読む
- 中断時の共通サブコマンド動作を確認したいときは、`oracle/doc/app_spec/subcommand_interruption.md` を直接読む
- agent call の具体的な prompt、prompt part、起動パラメータを確認したいときは、指定された review builder と findings policy を直接読む
- feedback observation や active issue の共通変換規則を確認したいときは、`oracle/doc/app_spec/feedback.md` を直接読む

## hash
- 3698d0993f3b086ef572ecd4a9d694a5cfe9b14d5f74c7f456778211f7a20b7e

# `realization_apply.md`

## Summary
- realization apply fork の目的、追従対象となる oracle file の git 差分、単一の Codex agent call による realization file 反映、後処理と run 状態遷移を定める仕様。fork の共通 lifecycle は editing run 仕様、agent 起動パラメータは realization apply fork の launch 実装、適合性判定は oracle と realization の仕様を入口とする。

## Read this when
- 直近の oracle file の commit 差分を realization file へ反映する fork の挙動を確認するとき
- fork の差分範囲、agent call の回数・実行条件、変更可能な対象を確認するとき
- fork report、終了コード、エラー状態、feedback 記録、join 後 hook の要件を確認するとき

## Do not read this when
- fork・join・abandon に共通する lifecycle 自体を確認する場合は editing run の正本を直接読むとき
- agent 起動時の正確な prompt、prompt part、起動パラメータを確認する場合は launch 実装を直接読むとき
- oracle file と realization file の一般的な適合性基準を確認する場合は oracle_and_realization の正本を直接読むとき
- realization refactor やファイル単位の全面的な追従を扱うとき

## hash
- 7f6beb2f86e4a8adea3dbd836e7c72e61c5a73ad8d2d713937bc363ddedb10b0

# `realization_refactor.md`

## Summary
- realization refactor fork の目的、refactor state の同期と調査ループ、current fork の unresolved target 管理、完了・中断・エラー時の扱い、および report 生成要件を定義する正本仕様。realization refactor の実行フローや状態遷移、終了理由、変更確定の整合性を確認・変更するときの入口となる。

## Read this when
- realization refactor fork の処理順序、調査対象の選択、state 更新、unresolved の扱い、完了条件を確認するとき。
- 中断・エラー時の rollback、run state、終了コード、report の要件を確認するとき。
- refactor fork の agent call、変更 path 検証、commit、join 後 hook の仕様を確認するとき。

## Do not read this when
- 短い変更ループを担う realization apply の仕様だけを確認するときは、realization apply の仕様へ直接進む。
- fork・join・abandon に共通する lifecycle の詳細だけを確認するときは、共通 lifecycle の正本仕様へ直接進む。
- oracle file と realization file の適合性基準そのものを確認するときは、oracle_and_realization.md へ直接進む。

## hash
- 1030a62973aa67107d168202db9be549955881d16e8fd3263c51b2b1725e64f4

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
- `cmoc tui` サブコマンドの責務・実行手順・前提条件・TUI 起動契約を定義する正本。プロンプト入力から起動パラメータ構築、AI Agent CLI/TUI 起動までの共通規則と Codex CLI 固有の起動条件を確認する入口。

## Read this when
- `cmoc tui` の挙動、引数、実行前提、プロンプトエディタ入力、TUI 起動手順を実装・変更・レビューするとき
- TUI に注入する cmoc 基本規定、indexing preflight、feedback、Windows toast 通知の適用範囲を確認するとき
- Codex CLI バックエンドの起動コマンド、環境変数、preflight validation、引数上書きを確認するとき

## Do not read this when
- プロンプトエディタ入力の正確な skeleton や表示文面だけを確認する場合は、参照先の prompt editor input oracle を直接読む
- 起動パラメータの正確な選択・文面・選択理由だけを確認する場合は、`build_tui_launch_tui_parameter` の oracle src を直接読む
- TUI サブコマンド以外のサブコマンドの仕様や、個別の oracle・realization ファイルの詳細実装だけを確認する場合

## hash
- df1aed6006a6996ab64fd53a623ebd006adc46eb145b9aeb42219b3b99ad4135
