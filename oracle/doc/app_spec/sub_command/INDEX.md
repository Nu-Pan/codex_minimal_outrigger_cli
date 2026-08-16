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
- oracle file の最終状態に関するユーザー指示を受け取り、本命の編集 agent call と仕様削減 agent call を直列実行する `cmoc oracle edit` の仕様を定義する。prompt 構築、doctor・indexing preflight、起動条件、agent の編集境界、失敗時の扱い、primary report、ログ通知、差分維持までを扱う。oracle edit サブコマンドの実装・仕様確認時の入口となる。

## Read this when
- `cmoc oracle edit` の実行順序、agent call の起動条件、または本命・仕様削減 call の責務を確認するとき
- oracle file 編集の権限境界、差分・commit・worktree の扱い、または失敗時の終了条件を確認するとき
- oracle edit の primary report、console/log、terminal result、Windows toast の出力要件を確認するとき

## Do not read this when
- oracle edit 以外のサブコマンドの仕様だけを確認するとき
- prompt editor input や prompt policy など、本文で正本として直接指定されている個別仕様を確認するときは、それぞれの正本仕様を直接読む
- oracle file の分類基準や doctor・indexing の詳細規約だけを確認するときは、本文が指定する対応する正本仕様を直接読む

## hash
- fe550b3d17b18e9aaae0507a7181a960c879deab55b5168ea38f0853bb531236

# `oracle_investigation.md`

## Summary
- oracle file に関する調査指示をエディタから受け取り、完全な調査プロンプトを構築して Codex CLI の TUI を起動するサブコマンドの仕様。doctor preprocess、プロンプト編集、TUI 起動、調査結果の扱いと編集 handoff の境界を定める。oracle investigation の起動手順や、oracle/realization file のアクセス制約、Codex CLI 起動規則を確認する際の入口となる。

## Read this when
- oracle file に関するユーザー調査を受け付けるサブコマンドの挙動を変更・検証するとき
- 調査プロンプトの構築、エディタ入力、TUI 起動パラメータ、調査から編集への handoff を確認するとき
- oracle file を読み取り専用、realization file を読み書き禁止とする調査境界や、Codex CLI の起動規則を確認するとき

## Do not read this when
- oracle file の一般的な調査指針や対象判定を確認するだけの場合は misc_spec.md を読む
- エディタ入力の正本仕様を確認する場合は prompt_editor_input.md を直接読む
- プロンプトの汎用規定と動的プロンプトの責務境界を確認する場合は prompt_policy.md を直接読む
- Codex CLI の共通起動規則や Windows toast 通知の詳細を確認する場合は、それぞれの正本仕様を直接読む

## hash
- 66818113dee555de0bef6269b7fce19c6340e04b45f25a5f1bd1f697e78d1160

# `oracle_review.md`

## Summary
- `cmoc oracle review` サブコマンドの正本仕様。oracle ファイルのレビュー範囲、所見の列挙・統合・検証・採否判定、隔離実行、レポート生成、責務境界を定義する。oracle review の挙動やレポート形式を変更・確認するときの入口となる。

## Read this when
- `cmoc oracle review` の引数、事前条件、実行手順、スコープ、割り込み処理を確認するとき
- oracle file に対する所見の成立条件、重大度、検証、採否判定の仕様を確認するとき
- oracle review レポートの保存先、frontmatter、本文構成、verdict を確認するとき
- oracle review の責務境界や、実装・自動生成ファイルをレビュー対象外とする制約を確認するとき

## Do not read this when
- oracle review 以外のサブコマンドの仕様や、共通の隔離実行・中断・feedback の詳細だけを確認したいときは、それぞれの正本仕様を直接読む
- Codex CLI の各 agent call の具体的な prompt 構築や policy 実装を確認したいときは、本文が参照する prompt builder または policy の仕様を直接読む
- oracle file 自体の個別内容や変更履歴を確認したいときは、このサブコマンド仕様ではなく対象 oracle file や git の情報を読む

## hash
- 744c96e7edc152ab522c09b2046f8873c34c284428cb53a76a8061d6e8886d04

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
- `cmoc session join` の完了処理、事前条件、ブランチ merge、conflict 解消、session state 更新、session branch cleanup、および primary report の挙動を確認・変更するときに読む仕様。通常の git merge wrapper や repository-local feedback state の merge 仕様を調べる入口ではない。

## Read this when
- `cmoc session join` の引数、実行前検証、merge 対象、home branch の進行時の扱いを確認するとき
- merge conflict 発生時の解消手順、oracle file の優先順位、agent call の制約を確認するとき
- session state の遷移、session branch 削除条件、終了時 report の必須内容を確認するとき

## Do not read this when
- 通常のブランチ merge の一般仕様や `repository-default-branch` の扱いを調べるとき
- pending observation や active issue など repository-local feedback state の取り込み・競合解消・report 管理を調べるとき
- `cmoc session join` 以外の session サブコマンドの仕様を直接確認するとき

## hash
- 68e41408eb82b8e087d49531e6d8dcef44a3bc63cc727942f922a85792be4e7f

# `tui.md`

## Summary
- `cmoc tui` サブコマンドの責務と実行手順を定義する正本仕様。ユーザープロンプトへの cmoc 固有契約の注入、エディタ入力、起動パラメータの構築、AI Agent CLI/TUI の起動条件を扱う。
- 全バックエンド共通の固定注入規定、モデル・推論・ファイルアクセス設定、indexing preflight、feedback、終了通知など、TUI 起動時に適用される共通契約の入口となる。
- Codex CLI をバックエンドとして扱う場合の起動コマンド、環境変数、preflight validation、CLI 引数による設定上書きの参照入口を示す。

## Read this when
- `cmoc tui` のサブコマンドの挙動、引数、事前条件、実行順序を確認・変更するとき。
- ユーザープロンプトへの固定規定の注入や、完全プロンプトおよび TUI 起動パラメータの構築責務を確認するとき。
- AI Agent CLI/TUI の共通起動条件、indexing preflight、feedback 観測、Windows toast 通知の適用範囲を確認するとき。
- Codex CLI バックエンドの起動方法や、Codex 固有の環境変数・preflight・引数設定を確認するとき。

## Do not read this when
- プロンプトエディタ入力の具体的な仕組みを確認する場合は、プロンプトエディタ入力の正本仕様を直接読む。
- oracle/realization の責務、oracle review の所見成立条件、indexing、feedback、Windows 通知の詳細を確認する場合は、それぞれの指定された正本仕様を直接読む。
- TUI サブコマンドの責務や起動契約ではなく、個別の builder 実装やエディタ初期値生成実装だけを確認する場合は、対応する実装対象を直接読む。

## hash
- 3c7cf802582647687f707f6b6f9fd52b5a20f95259a20fc9d775eb8b1e3765e5
