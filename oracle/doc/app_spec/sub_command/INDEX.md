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
- `cmoc feedback report` の仕様を定義する正本文書。pending observation と active state を report cut に固定し、候補の検証結果に応じて active generation と正常／incomplete／invocation summary report を publication する処理契約を扱う。
- CLI 引数、事前条件、cut 固定、validation・deduplication・machine／agent observation 処理、normalization／verification、publication、再開・中断、state cleanup、保存形式、終了コードを定める。feedback report 機能の実装、挙動仕様、状態遷移、エラー処理、レポート形式を確認する際の入口である。
- raw observation の正本、state・checkpoint・publication・cleanup の正本、normalization／verification agent の prompt と schema、共通の中断動作は本文中で指定された別の正本へ進む。

## Read this when
- `cmoc feedback report` のCLI契約や処理順序を実装・変更・検証するとき
- pending observation、active issue、report cut、verification checkpoint、current pointer の扱いを調査するとき
- 正常 report、incomplete 診断 report、invocation summary report の publication・cleanup・終了コードを確認するとき
- 中断後の再開、validation failure、AI call failure、state corruption、publication failure の挙動を確認するとき

## Do not read this when
- raw observation の schema や保存規則だけを確認する場合は、指定された feedback observation の正本を直接読むとき
- state、checkpoint、current pointer、publication、cleanup の詳細だけを確認する場合は、指定された feedback state の正本を直接読むとき
- normalization または verification agent の正確な prompt・起動パラメータ・Structured Output schema を確認する場合は、本文が指定する oracle source と schema を直接読むとき
- 共通のユーザー中断動作だけを確認する場合は、subcommand interruption の正本を直接読むとき
- feedback report 以外のサブコマンドや、一般的なテスト実行手順を確認する場合

## hash
- bbd128bf9348fe8bd9c6d6c87cf308c33273b28ac3111663c143e92a2eb50368

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
- oracle file の編集サブコマンド `cmoc oracle edit` の正本仕様。ユーザー指示の入力、doctor preprocess・indexing preflight、本命および仕様削減の agent call、実行順序、編集境界、終了状態、差分、primary report、ログ通知、並行実行時の扱いを定義する。oracle edit の挙動や実装責務を確認・変更するときの入口となる。

## Read this when
- `cmoc oracle edit` の実行フロー、agent call の起動条件・パラメータ・失敗処理を確認するとき。
- oracle file の編集権限、差分の扱い、report・ログ・terminal result・Windows toast の要件を確認するとき。
- 本命 agent call 後の仕様削減 agent call、または oracle edit 固有の終了・中断・排他制御を変更するとき。

## Do not read this when
- oracle file の一般的な編集基準や misc spec の判定基準だけを確認したいときは、対応する app_spec または dev_rule の正本を直接読む。
- editor 入力の形式、prompt 共通規則、doctor preprocess、indexing の詳細仕様だけを確認するときは、本文が指定する各正本ドキュメントを直接読む。
- realization 実装や realization test の配置・実行方法を確認するときは、この oracle edit 仕様ではなく対応する design_rule・test_rule・test_execution を読む。

## hash
- 74ff7dafef8c15a13f157e9970ce1f7e10c3bbfe42d13993fb85ac15b6e52b74

# `oracle_investigation.md`

## Summary
- oracle file に関する調査指示をエディタから受け取り、oracle file を根拠に調査する Codex CLI TUI サブコマンドの責務、入力、実行手順、プロンプト構築、起動条件、調査結果の扱いを定める。oracle investigation の TUI 起動仕様や、調査から editor handoff への境界を確認する入口である。

## Read this when
- oracle file の調査用 TUI サブコマンドの挙動、引数、実行手順を変更または確認するとき
- oracle investigation 用の完全プロンプト、エディタ入力、Codex CLI 起動パラメータの責務境界を確認するとき
- oracle investigation から edit への handoff、ファイルアクセス制約、調査結果や自動 commit の扱いを確認するとき

## Do not read this when
- realization 側の具体的な実装配置や CLI 内部処理を直接確認する必要があるとき
- エディタ入力形式だけを確認する場合は prompt_editor_input.md を読むとき
- プロンプト標準や Codex CLI 起動規則など、本文が正本として指定する個別仕様を直接確認するとき

## hash
- f01dffc2c9daa51ed0a841f00a8e78b0fbf6f2cb91b770bec083c6566f0a6c15

# `oracle_review.md`

## Summary
- `cmoc oracle review` の仕様本文です。oracle のレビュー範囲、所見の成立条件・重大度・検証と採否、隔離実行、割り込み、レポート保存と表示形式を定義します。該当サブコマンドの挙動やレビュー結果のレポート仕様を確認・変更するときの入口です。

## Read this when
- `cmoc oracle review` のサブコマンド仕様を確認・変更するとき
- 所見の列挙、統合、検証、採否判定のルールを確認するとき
- レビュー対象スコープ、隔離実行、ユーザー中断、レポート保存形式を確認するとき

## Do not read this when
- oracle 全体の一般的な判断基準を確認する場合
- 隔離実行の共通仕様だけを確認する場合
- サブコマンド中断の共通動作だけを確認する場合
- 実装ファイルや自動生成される `INDEX.md` のレビューを行う場合

## hash
- 2b45350b72162025f63fa5d0e606b25ae54c95949ee996ebc0134f36ee010ff2

# `realization_apply.md`

## Summary
- 直近の git commit 群から読み取った oracle file の変更を realization file へ反映する、realization apply の fork workload を定義する。対象差分の構築、単一の Codex CLI agent call による追従、変更検査・commit、joinable または error への終了処理、fork report と join 後 hook までを扱う。

## Read this when
- realization apply fork の追従要否や oracle file と realization file の適合性を確認するとき
- 直近の適用済み commit から今回の fork までの oracle 差分を基に realization file を更新するとき
- apply fork の agent call、実行手順、エラー処理、report 保存、join 後の session 更新を実装・変更するとき

## Do not read this when
- 引数なしの realization apply コマンド自体の一般仕様だけを確認したいとき
- ファイル単位の網羅的な realization 追従や realization refactor の責務を確認したいとき
- fork・join・abandon に共通する lifecycle の正本を確認したいときは editing_run の仕様を直接読む
- oracle file に対する realization file の適合性の正本を確認したいときは misc_spec の該当仕様を直接読む
- feedback の収集・保存規則だけを確認したいときは feedback の仕様を直接読む

## hash
- 1b90edeb04c3eb2a65fd926935b712e3960b6318b7c2344fea6920886ea11bdb

# `realization_refactor.md`

## Summary
- realization refactor fork の目的、refactor state、調査ループ、完了条件、中断・エラー処理、fork report を定める正本仕様。oracle file と realization file の追従調査を実行する fork のライフサイクル全体を確認するための入口であり、短い変更ループの realization apply や適合性判定の正本仕様とは役割が異なる。

## Read this when
- realization refactor fork の開始、state 同期、調査対象の選択、agent call、差分検証、commit の処理を確認・変更するとき
- current fork の unresolved target、investigation_required、natural_completion、completed_with_unresolved の扱いを確認するとき
- ユーザー中断、その他のエラー、fork report、終了コード、join 後の動作を確認するとき

## Do not read this when
- 短い変更ループを担う realization apply の仕様だけを確認するとき
- oracle file と realization file の適合性判定基準を確認するときは、適合性の正本仕様を直接読む

## hash
- 043bb3cc902aba2e726bffc2d89400e9e5dd06ecfb4d8eb694e18bbf5a80056e

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
- `cmoc session join` の正本仕様。セッション作業ブランチをホームブランチへ安全に merge して完了状態へ遷移させるコマンドの責務、引数、事前条件、実行手順、競合解消、state 更新、cleanup、報告要件を定義する。
- session join の挙動、セッション状態検証、merge 先・merge 元の扱い、conflict 解消規則、repository-local feedback state との境界を確認・変更するときの入口。

## Read this when
- `cmoc session join` のコマンド仕様、事前条件、merge 手順、session state 遷移を実装またはレビューするとき
- session join における git conflict の解消方法、oracle file の扱い、cleanup 条件を確認するとき
- session join の primary report に必要な終了経路・記録項目を確認するとき

## Do not read this when
- 通常の git merge wrapper や、session join 以外の session サブコマンドの仕様を扱うとき
- repository-local feedback state の merge・競合解消・巻き戻し仕様を確認するときは、feedback state の専用仕様を直接読む

## hash
- bb9048af8efe3c83b5cb9b849f6b6c649309d584d30aadcbdb656abaa3d879f5

# `tui.md`

## Summary
- `cmoc tui` サブコマンドの責務、引数・事前条件、プロンプト編集から AI Agent CLI/TUI 起動までの実行手順、共通注入規範、バックエンド共通契約、および Codex CLI 固有の起動条件を定める正本仕様。`cmoc tui` の挙動や起動条件を確認・変更するときの入口となる。

## Read this when
- `cmoc tui` の実行フロー、プロンプト編集、完全プロンプト構築、TUI 起動パラメータを確認するとき
- cmoc 固有規範の固定注入、適用条件、builder の設定、indexing preflight、feedback、通知の扱いを確認するとき
- Codex CLI バックエンドの起動コマンド、環境変数、preflight validation、引数上書きを確認するとき

## Do not read this when
- プロンプトエディタ入力の詳細仕様だけを確認する場合は、正本である `prompt_editor_input.md` を直接読む
- oracle・realization の責務や適合性だけを確認する場合は、`misc_spec.md` を直接読む
- oracle review の所見成立条件だけを確認する場合は、`oracle_review.md` を直接読む
- indexing preflight、feedback observation、Windows toast 通知の詳細だけを確認する場合は、それぞれ指定された個別仕様を直接読む

## hash
- 826c62049396df095b9c687eef45f94385f0087a3fc25a0a4fc60eaf70d0c786
