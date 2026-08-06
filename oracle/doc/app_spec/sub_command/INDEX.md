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
- 編集 run を開始・終了する共通ライフサイクル仕様を定める。対象は realization apply/refactor の fork と、run join/abandon である。
- session state による同時実行制約、fork の事前条件・開始処理、編集差分と state の管理、join の差分検査・merge・hook・cleanup、abandon の破棄・cleanup、および各操作の report 要件を扱う。
- workload 固有仕様が定める処理の共通基盤として、対象 workload の fork/join 後処理や session lifecycle との境界を確認する入口となる。

## Read this when
- realization apply または realization refactor の fork 実装・挙動・事前条件を確認するとき
- cmoc run join または cmoc run abandon の引数、state 遷移、差分検査、merge、cleanup を実装・レビューするとき
- 編集 run と session lifecycle の責務境界、同時実行制約、想定内差分、report 要件を確認するとき

## Do not read this when
- cmoc session join や cmoc session abandon など、外側の session lifecycle だけを扱うとき
- cmoc oracle edit、read-only の investigation/review、cmoc 自身による機械的更新、session join の conflict 解消だけを扱うとき
- workload 固有の編集内容、許可ファイル、fork report の保存先、join 後 hook の詳細だけを確認するときは、対応する workload 固有仕様を直接読む

## hash
- 6fee5370ce0cc454cfc8fab2f2ad99264d6c451a4b7ab31bd34afc4b93c967b9

# `feedback_report.md`

## Summary
- `cmoc feedback report` の仕様を定める文書。feedback の正本仕様を参照し、引数、実行前提、raw observation の snapshot・増分処理、normalization agent、assessment、threshold、checkpoint、commit・再開、中断、report 保存形式、既定表示、終了コードを定義する。feedback report の実装や挙動を確認・変更する際の入口となる。

## Read this when
- `cmoc feedback report` の引数、実行条件、状態更新、終了コードを確認するとき
- feedback observation や tracked feedback state を report に取り込む処理、deduplication、normalization、assessment、threshold を実装・検証するとき
- report の snapshot、checkpoint、unit commit、再開・中断、Markdown report の front matter や既定表示を扱うとき

## Do not read this when
- raw observation の schema や生成・保存規則だけを確認したいときは feedback observation の仕様を読む
- tracked feedback record の schema や revision・assessment・disposition のデータ構造だけを確認したいときは feedback state の仕様を読む
- normalization agent の builder 入力・出力 schema だけを確認したいときは専用 builder と schema を直接読む
- subcommand 共通のユーザー中断動作だけを確認したいときは subcommand interruption の仕様を読む

## hash
- 1c30e8012e627aa0736f011c8438b13dc81a3115c28403dfd31561d2a41b3539

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
- oracle file の最終状態を編集する `cmoc oracle edit` サブコマンドの正本仕様。引数、ユーザー指示の入力、doctor・indexing preflight、TUI 起動条件とパラメータ、編集境界、終了時の差分保持、中断・排他制御、ログ方針を定義する。oracle 編集サブコマンドの実装や関連する起動・事前条件・ログ仕様を確認する際の入口。

## Read this when
- `cmoc oracle edit` の挙動、実行順序、起動条件を変更または確認するとき
- oracle file を編集する TUI の入力内容、権限境界、起動パラメータを実装・検証するとき
- TUI 終了後の差分、終了コード、中断、排他制御、ログの扱いを確認するとき

## Do not read this when
- realization file の通常編集や `cmoc oracle investigation` の権限を確認したいとき
- prompt editor input、prompt standard、Codex CLI 起動規則など個別仕様の詳細だけを確認したいときは、本文が参照する各正本仕様を直接読む
- oracle edit の実装詳細や具体的な文面を確認したいときは、対応する realization file を直接読む

## hash
- 6a15e73c80aa7d14fcf22ac93888159272484729f6f39cc99231cda5f39cc141

# `oracle_investigation.md`

## Summary
- oracle file を根拠に調査を行う Codex CLI TUI サブコマンドの仕様を定義する文書。doctor preprocess、エディタ入力、起動パラメータ構築、Codex CLI 起動、読み取り専用の調査結果提示までの流れを扱う。

## Read this when
- oracle file に関する調査用サブコマンドの挙動や実行手順を確認するとき
- oracle investigation のエディタ入力、TUI 起動パラメータ、Codex CLI 起動規則を変更・調査するとき
- 調査中の oracle file および realization file のアクセス制約を確認するとき

## Do not read this when
- エディタ入力の共通仕様だけを確認したいときは prompt_editor_input.md を直接読む
- 汎用プロンプト規範だけを確認したいときは prompt_standard.md を直接読む
- TUI 起動パラメータの詳細だけを確認したいときは launch_tui.py を直接読む
- Codex CLI の起動環境や引数上書き規則だけを確認したいときは codex_exec_rule.md を直接読む

## hash
- 538e05a68e9be671d7490d0d75a0f095406cb3574dd1f820e6313502d7008215

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
- セッション作業ブランチをホームブランチへマージし、セッションを joined に遷移させる `cmoc session join` の正本仕様。引数、事前条件、doctor preprocess、マージ、コンフリクト解消、状態更新、ブランチ削除条件を扱う。

## Read this when
- `cmoc session join` の挙動、引数、実行前検証、マージ先・マージ元を確認するとき
- session join のコンフリクト処理や tracked feedback state の扱いを実装・検証するとき
- join 後のセッション状態更新やセッションブランチ削除条件を確認するとき

## Do not read this when
- 通常の git branch 間マージや `repository-default-branch` の扱いを確認したいとき
- session の作成・実行・離脱など、join 以外のライフサイクル動作を確認するとき
- conflict resolution agent call の詳細パラメータ自体を確認するときは、そのビルダー仕様を直接読む

## hash
- 041840c61fcea0cc518e31d84088a68ca7f78339577bafc4b4bcc86e080138c3

# `tui.md`

## Summary
- `cmoc tui` サブコマンドの責務と実行契約を定義する仕様。ユーザープロンプトへの cmoc 固有規範の注入、doctor preprocess、エディタ入力、AI Agent CLI/TUI の起動、共通バックエンド規則、Codex CLI 固有設定を扱う。`cmoc tui` の挙動や起動パラメータ、注入規範を確認する際の入口となる。

## Read this when
- `cmoc tui` の実行手順、引数、事前条件を確認するとき
- プロンプト編集入力や TUI 起動時の固定パラメータ・注入規範を確認するとき
- Codex CLI バックエンドの起動コマンド、環境変数、preflight、引数上書きを確認するとき

## Do not read this when
- プロンプトエディタ入力の詳細仕様だけを確認したいとき
- feedback observation の保持・collector context の詳細だけを確認したいとき
- TUI 起動パラメータの実装や初期入力文の生成箇所を直接調査するとき

## hash
- cbbe73191a257b9d686e1e49b0ec78367dcac15c35cc678dc9f1e1b3dd63e9f8
