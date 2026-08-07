# `doctor.md`

## Summary
- `cmoc doctor` の役割は、リポジトリが `cmoc` を正常実行できる状態かを検証し、必要なら修復を試みることにある。中身は doctor preprocess を明示的に呼ぶための入口なので、このコマンドの振る舞いを実装・変更するときに読む。

## Read this when
- `cmoc doctor` の実行開始条件や、doctor preprocess への委譲方法を確認したいとき。
- `cmoc` の環境診断と修復の入口として、このコマンドが何を保証すべきかを把握したいとき。

## Do not read this when
- doctor preprocess の内部処理だけを変えたいときは、まずその処理側の定義を読む。
- 引数設計や追加オプションの検討ではなく、単に `cmoc doctor` の入力なし実行を前提にしたいだけのとき。

## hash
- 8354ebcd7f732dcf70eb06ee6ed33abe6093b06e6effe5dcf1084dc3dce1f39c

# `editing_run.md`

## Summary
- 明示的な join を必要とする realization 編集 run の共通ライフサイクル仕様。workload 固有 fork の事前条件・開始処理、同時実行境界、編集責務、想定内差分、join/abandon の事前条件・差分検査・merge・cleanup、report 要件を定義する。realization apply/refactor の run lifecycle や、run join/abandon の実装・挙動を確認する際の入口となる。

## Read this when
- realization apply または realization refactor の fork、join、abandon のライフサイクルを実装・変更・検証するとき
- 編集 run の session state、branch/worktree、想定内差分、merge 後 hook、cleanup、report の契約を確認するとき
- 明示的な join を要求する編集 run と、session lifecycle・read-only investigation・oracle edit などの対象外範囲を区別するとき

## Do not read this when
- cmoc session join/abandon など外側の session lifecycle だけを扱うとき
- oracle edit、read-only investigation/review、cmoc 自身による機械的更新、session join の conflict 解消だけを扱うとき
- 編集 run の個別 workload 固有仕様や refactor state 同期の詳細だけを確認する場合は、それぞれの workload 仕様または refactor 仕様を直接読む

## hash
- d2497f520c68c3f20aac45a085fc969a946ce4fe2df94a56774c6a39fa773fb3

# `feedback_report.md`

## Summary
- `cmoc feedback report` の正本仕様。feedback state を検証し、raw observation の immutable snapshot を起点に増分 normalization・assessment・ingestion を処理し、Markdown report と state snapshot を durable に確定する。
- machine observation の統合、曖昧な agent observation の normalization、notification threshold、fingerprint に基づく鮮度評価、checkpoint による中断・再開、重複防止を定義する。
- report の保存形式、front matter、既定表示と `--all` 表示、差分基準、ユーザー中断時の扱い、および終了コードを定義する。feedback の詳細な observation schema と state record schema は参照先の正本仕様へ委譲する。

## Read this when
- `cmoc feedback report` の引数、事前条件、終了コード、保存先、出力形式を確認するとき。
- raw observation から normalized issue、assessment、ingestion receipt、report を生成する処理や、notification threshold・鮮度評価を実装または確認するとき。
- report snapshot、state snapshot、checkpoint、predecessor に基づく増分処理・再実行・中断復旧の挙動を確認するとき。
- 既定 report と `--all` の表示対象、差分の判定基準、issue の表示順を確認するとき。

## Do not read this when
- raw observation のフィールド定義や不正値の詳細を確認するだけの場合は、観測仕様を直接読む。
- repository-local feedback state の record schema、hash、参照整合性、retention の詳細を確認するだけの場合は、feedback state 仕様を直接読む。
- 共通のユーザー中断動作だけを確認する場合は、subcommand interruption 仕様を直接読む。
- feedback report 以外のサブコマンドの挙動や、一般的な report 生成手順を確認する場合。

## hash
- 430750e55d1e019d74d2f59af57b4e37a7d58b24ba76ba38005fb4a723881195

# `indexing.md`

## Summary
- `cmoc indexing` のサブコマンド入口として、作業ツリー全体に対するインデクシングの実行条件と、その結果を自動コミットする責務を持つ。
- この文書は、引数なしで実行されること、実行前に未コミット差分がある場合は失敗すること、そして `doctor preprocess` の後にインデクシングと git commit を行う必要があることを確認したいときに読む。
- インデクシングの意味そのものは別の正本仕様に委ねられているため、この文書はサブコマンドの手順と事前条件の確認に絞る。

## Read this when
- `cmoc indexing` の実行可否や前提条件を確認したいとき。
- このサブコマンドが何を順に呼び出し、どこで差分が確定してコミットされるかを確認したいとき。
- インデクシングの定義そのものではなく、サブコマンドとしての入出力や実行フローだけを知りたいとき。

## Do not read this when
- インデクシング処理の詳細仕様そのものを知りたいときは、参照先の正本仕様を読む。
- 引数設計や他サブコマンドとの比較を知りたいだけなら、ここではなくより上位のルーティング文書を読む。
- git commit の一般的な運用や doctor preprocess の内部動作を知りたいときは、この文書ではなく各処理の本体を読む。

## hash
- 00122849aac5fb7274dffd1fdeadb48c89c3dc735f7dfc6668c3a2fa8fe02b15

# `oracle_edit.md`

## Summary
- `cmoc oracle edit` サブコマンドの正本仕様。oracle file を編集する Codex CLI TUI の目的、入力、起動前提、実行順序、編集境界、終了時の差分保持、中断制御、ログ方針を定義する。oracle edit の挙動や実装責務を確認する際の入口となる。

## Read this when
- `cmoc oracle edit` の実行順序、TUI 起動条件、起動パラメータ、編集可能範囲を実装・レビューするとき
- oracle file 編集時のユーザー指示入力、権限境界、終了後の差分やログの扱いを確認するとき
- oracle edit 固有の fork/join、session state、排他制御、中断処理の有無を判断するとき

## Do not read this when
- realization file の通常の編集やテスト実行の仕様だけを確認したいとき
- 他の cmoc サブコマンドのライフサイクルや TUI 起動仕様を調べるときは、それぞれのサブコマンド仕様を直接読む
- プロンプト入力形式、標準プロンプト規範、Windows toast、Codex CLI 実行規則の詳細だけを確認したいときは、本文中で指定された各正本仕様を直接読む

## hash
- adbf3c7de6fc441a05ba640594d7cd570ae6ef1e4a3311ce2ab0c6c2b9baa8bb

# `oracle_investigation.md`

## Summary
- oracle file を根拠にユーザーの調査指示を受け付け、Codex CLI の TUI で調査結果を回答するサブコマンドの仕様を定義する。入力エディタ、調査用 launch parameter の構築、Codex CLI 起動、読み取り専用・変更禁止の扱いを扱う。

## Read this when
- oracle file に関する調査サブコマンドの起動手順、ユーザー指示の入力方法、TUI 起動パラメータ、Codex CLI の実行条件を確認するとき。
- oracle investigation の実装や関連する正本仕様との責務境界を調べるとき。

## Do not read this when
- oracle file 自体の一般的な調査方法や編集規則を確認したいときは、共通の oracle 契約や調査対象の正本仕様を直接読む。
- プロンプトエディタ入力の詳細文面を確認したいときは、指定された prompt editor input の正本を直接読む。
- TUI 起動パラメータの具体的な構築内容を確認したいときは、対応する launch parameter builder の実装を直接読む。
- Codex CLI の起動規則や Windows toast 通知の仕様だけを確認したいときは、それぞれの専用仕様を直接読む。

## hash
- 8973fa7f0b0033d99ac7337531679dfe25b2c7524c6d656924c19df6026fba50

# `oracle_review.md`

## Summary
- 対象は `cmoc oracle review` のサブコマンド仕様で、oracle file のレビュー範囲、所見の列挙・統合・検証・採否判定、隔離実行、中断処理、レポート生成を定義する。oracle review の挙動や責務境界を確認する作業の入口となる。

## Read this when
- `cmoc oracle review` の引数、事前条件、実行手順、所見処理ループ、agent call 規則を実装・変更・検証するとき。
- レビューのスコープ、所見 ID、ユーザー中断時の確定結果、レポート体裁や判定結果を確認するとき。
- oracle review と feedback observation、実装レビュー、INDEX.md レビューの責務境界を確認するとき。

## Do not read this when
- oracle review 以外のサブコマンドの挙動だけを調べるとき。
- 所見判定基準そのものを確認する場合は、`build_oracle_review_standard` の正本を直接読む。
- 隔離実行や中断の共通仕様だけを確認する場合は、対応する共通仕様を直接読む。
- 個別 agent call の prompt 詳細だけを確認する場合は、対応する parameter builder の正本を直接読む。

## hash
- 71825339f2c00979831c84e4ecc381abf0ee103624b7d9df58f1da5d56fa53da

# `realization_apply.md`

## Summary
- 直近の git commit 群から読み取った oracle file の変更を realization file へ反映する、`cmoc realization apply fork` の仕様を定義する。引数、追従対象となる commit 範囲と oracle 差分、単一 agent call による実行、realization file の変更範囲、検査・commit、run state、report、エラー処理、join 後 hook を扱う。realization apply の fork 実行仕様へ進む入口であり、fork・join・abandon の共通 lifecycle は編集 run の仕様を確認する。

## Read this when
- realization apply fork の引数、oracle 差分の追従範囲、agent call の実行条件を確認するとき
- fork の実行手順、変更対象、検査、commit、run state、終了コードを確認するとき
- fork report の項目・保存先・feedback の扱い、または join 後の session 更新を確認するとき
- realization apply のエラー処理や joinable/error 終了条件を確認するとき

## Do not read this when
- fork・join・abandon に共通する lifecycle 自体を確認する場合は、共通編集 run の正本仕様を直接読む
- ファイル単位の網羅的な realization 追従や refactor の方針を確認する場合は、realization refactor の仕様を読む
- feedback の共通収集規則を確認する場合は、feedback の正本仕様を直接読む

## hash
- 43ca4121d35ab0964cbce0ead1f33ef282081473f8ecf840bbb859cbb5a701bf

# `realization_refactor.md`

## Summary
- realization file と oracle file のファイル単位調査を繰り返す、realization refactor fork サブコマンドの正本仕様。refactor state の同期、current fork 内の unresolved target 管理、調査・修正・検証・commit の処理単位、完了・中断・エラー時の状態、および report と終了コードを定義する。realization refactor fork の挙動、state schema、調査対象の選択、完了条件、run lifecycle を確認する入口となる。

## Read this when
- realization refactor fork の処理フロー、調査対象の選択、agent call、変更検証、state 更新、commit 単位を実装または確認するとき
- refactor state の保存形式、entry 同期、investigation_required、調査履歴、current fork の unresolved target を扱うとき
- natural_completion、completed_with_unresolved、user_interruption、error の判定や run state、report、終了コードを実装または確認するとき
- realization refactor fork と共通の fork、join、abandon、中断 lifecycle の境界を確認するとき

## Do not read this when
- 短い変更ループを担う realization apply の仕様だけを確認するときは、そちらの workload 固有仕様を直接読む
- fork、join、abandon の共通 lifecycle や中断の一般規則だけを確認するときは、指定された共通 lifecycle の正本を直接読む
- Codex call の一般的な事後条件だけを確認するときは、codex exec の正本仕様を直接読む
- feedback observation の保存規則だけを確認するときは、feedback の正本仕様を直接読む

## hash
- dcca7dede335566696024ee0367764870be53583356f739ec50388e957d9e707

# `session_abandon.md`

## Summary
- `cmoc session abandon` の仕様を定義する文書。session branch を home branch に統合せず破棄する際の引数、事前条件、破棄対象、実行手順、状態遷移、失敗時の扱いを扱う。session abandon の実装・テストや、session の破棄条件と状態管理を確認する入口となる。

## Read this when
- `cmoc session abandon` の挙動を実装・修正・レビューするとき
- session branch、session state、run state の事前検証やクリーンアップ処理を確認するとき
- session の abandon 後の状態遷移や失敗時ロールバックを確認するとき

## Do not read this when
- session の成果物を home branch に取り込む `cmoc session join` の仕様だけを確認するとき
- 未 join の編集 run を破棄する `cmoc run abandon` の詳細だけを確認するとき
- join 済み session の rollback や、session fork の詳細だけを確認するとき

## hash
- 2a06a246197e7eae75c325ccf2b7c6c10a5641b249900af9c7b143c770ea9e0d

# `session_fork.md`

## Summary
- `cmoc session fork` の正本仕様。現在のローカルブランチを分岐元兼マージ先として、セッション用ブランチを作成・checkoutし、session情報を保存してブランチ名を表示する。引数、事前条件、実行手順、ブランチ命名規則、start point制約、sessionの原則を扱う。

## Read this when
- `cmoc session fork` の挙動、引数、実行前エラー条件を確認するとき
- session branch の作成・命名・初期状態保存の実装やテストを変更するとき
- ローカルブランチ、managed branch、active session の扱いを確認するとき

## Do not read this when
- session fork 以外のサブコマンドの仕様だけを確認するとき
- 共通の doctor preprocess や session 状態形式の詳細を確認したいときは、それぞれの共通仕様・実装を直接読むとき

## hash
- e914f7872441d53ee60a6b5dd13d02a515e9a1159130098b798a0160a2f46a69

# `session_join.md`

## Summary
- `cmoc session join` の正本仕様。セッションブランチをホームブランチへマージしてセッションを完了するコマンドの責務、引数、事前条件、実行手順、競合解消、状態更新、ブランチ削除条件を定める。session join の挙動や実装・テストの入口となる。

## Read this when
- `cmoc session join` の実装、テスト、CLI 挙動を確認または変更するとき
- セッション完了時のブランチマージ、状態遷移、競合解消、後始末の仕様を確認するとき
- ホームブランチの進行や repository-local feedback state のマージ境界を確認するとき

## Do not read this when
- 通常の git merge wrapper や、`cmoc session join` 以外の session サブコマンドを扱うとき
- doctor preprocess、競合解消用 agent call、または session state の詳細仕様だけを直接確認したいときは、それぞれの正本仕様を読むとき
- INDEX.md のルーティング情報だけを確認する必要があるとき

## hash
- bdd1ca02b01f8793c07fc24dbe5b9dd609d534d52f03a1f0f40280a8d070e320

# `tui.md`

## Summary
- `cmoc tui` サブコマンドの責務・引数・実行手順・プロンプト編集・AI Agent CLI/TUI 起動契約を定義する正本仕様。TUI 起動パラメータ、固定注入規範、Codex CLI 固有設定、feedback や通知の関連仕様を確認する入口。

## Read this when
- `cmoc tui` の挙動、実行順序、プロンプト入力、固定起動パラメータ、注入規範、バックエンド共通契約を実装・レビューするとき。
- TUI 起動前の indexing preflight、feedback observation、Windows toast 通知、Codex CLI 起動設定との連携を確認するとき。

## Do not read this when
- エディタ入力の詳細仕様だけを確認する場合は、指定された prompt editor input の正本を直接読む。
- feedback observation や Windows toast 通知の詳細だけを確認する場合は、それぞれの正本仕様を直接読む。
- Codex CLI の実行規則だけを確認する場合は、Codex exec rule の正本を直接読む。

## hash
- 56df86f658dc3c7df25308cdc0ded77d31381c3b437657232d769e94f5adc8d4
