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
- 編集 run を開始・終了する workload 固有コマンドと、明示的な join／abandon を必要とする共通 lifecycle を定義する仕様。
- session ごとの未 join run 数、fork の事前条件・開始処理、編集責務、想定内差分、state 遷移を扱う。
- `cmoc run join` の対象解決、事前条件、差分検査、merge、post-join hook、state 同期、cleanup の契約を確認する入口である。
- `cmoc run abandon` の対象解決、破棄範囲、process 停止、worktree／branch cleanup、state 復旧の契約を確認する入口である。
- fork／join／abandon report に必要な追跡情報と、feedback data の扱いを定義する。

## Read this when
- realization apply または realization refactor の fork と、対応する run の join／abandon lifecycle を実装・レビューするとき。
- 編集 run の同時実行制約、session state の run section、fork／join／abandon の state 遷移を確認するとき。
- run branch と session branch の想定内差分、merge conflict、force-resolve、cleanup の挙動を確認するとき。
- fork／join／abandon report の出力要件や post-join 処理の責務を確認するとき。

## Do not read this when
- oracle edit、read-only investigation／review、cmoc 自身による機械的更新、session lifecycle、または session join の conflict 解消だけを扱うとき。
- 編集 run の workload 固有仕様や refactor state 同期の詳細だけを確認したいときは、それぞれの workload 固有仕様・正本仕様を直接読む。

## hash
- fa9c245afa67b89a8dc9b391ea4a1151595c9484bae24de9225e0cc94d9152a0

# `feedback_report.md`

## Summary
- `cmoc feedback report` の引数、開始前検証、report cut 固定、observation の検証・集約、normalization、verification、atomic publication、cleanup、中断再開、Markdown report 保存、終了コードを定義する。feedback の処理フローと人間向け issue report の仕様を確認するための正本である。

## Read this when
- `cmoc feedback report` の挙動、引数、前提条件、終了コードを実装または確認するとき
- feedback observation から issue candidate を作成・集約する処理を実装または確認するとき
- normalization agent、verification agent、Structured Output の受理条件を扱うとき
- report cut、active generation、current pointer、atomic publication、cleanup、再開処理を扱うとき
- 人間向け feedback report の形式や表示対象を確認するとき

## Do not read this when
- raw observation の schema や送信規則だけを確認するときは feedback observation の正本を読む
- repository-local feedback state の schema、durability、generation、pointer、cleanup retention だけを確認するときは feedback state の正本を読む
- サブコマンド共通の中断動作だけを確認するときは subcommand interruption の正本を読む
- normalization または verification の専用 builder・schema の詳細だけを確認するときは対応する oracle source と schema を直接読む

## hash
- c6d1fb25344d0f507b12cca38c7b6a5f487dde969ca7fe4400d6eb9c44850948

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
- oracle file を直接編集するサブコマンドの正本仕様。目的、入力プロンプト、起動前提、TUI 起動パラメータ、編集境界、実行順序、終了時の差分保持、中断制御、ログの扱いを定義する。oracle edit の実装や挙動を確認する際の入口。

## Read this when
- oracle file を編集するサブコマンドの仕様、起動条件、TUI 連携、編集権限、終了処理を変更・確認するとき。
- doctor preprocess、indexing preflight、Codex CLI TUI の起動順序やパラメータを調べるとき。
- TUI 終了後の差分、エラー終了、中断、ログ記録の扱いを確認するとき。

## Do not read this when
- oracle investigation など別サブコマンドの仕様だけを確認するとき。
- 一般的なプロンプト入力規則や共通標準の詳細を確認する場合は、参照先の正本仕様を直接読む。
- oracle file の内容編集そのものではなく、realization 実装の配置やテスト規約だけを確認するとき。

## hash
- a9670777613cbc02485cfe0be8a35658b12d7c48eb4b303b3755e5c4d35b1e4b

# `oracle_investigation.md`

## Summary
- oracle file の調査指示をエディタから受け取り、oracle を根拠に調査する Codex CLI TUI の起動フローと制約を定義する。調査サブコマンドの実装・プロンプト構築・TUI 起動条件を確認する際の入口。

## Read this when
- oracle file に関する調査サブコマンドの挙動、エディタ入力、完全プロンプトの構築、Codex CLI TUI の起動方法を確認するとき。
- 調査中の oracle file と realization file の読み書き制約、indexing preflight や自動 commit の扱いを確認するとき。

## Do not read this when
- oracle 調査以外のサブコマンドの仕様を確認するとき。
- プロンプト入力の一般規範だけを確認したいときは、エディタ入力やプロンプト標準の正本を直接読む。
- TUI 起動パラメータの詳細だけを確認したいときは、起動パラメータを構築する実装を直接読む。

## hash
- 739df540e4968d8c651c866e90e76ff42db17c11de6b959c98bba946de815a09

# `oracle_review.md`

## Summary
- 対象は `cmoc oracle review` サブコマンドの正本仕様で、oracle の致命的問題をレビューし、隔離実行・反復的な所見列挙/統合/検証・採否判定を経て Markdown レポートを保存・提示する責務を定義する。レビューの引数、事前条件、スコープ、agent call 規則、所見管理、中断時の扱い、レポート形式までを扱う。

## Read this when
- `cmoc oracle review` の引数、実行条件、レビュー処理の段階や反復上限を確認するとき
- oracle review の agent call、finding の列挙・マージ・検証・採否判定の責務やデータフローを確認するとき
- レビューの中断処理、責務境界、レポートの保存先・frontmatter・本文構成を確認するとき

## Do not read this when
- oracle review の判定基準そのものを確認したいときは、指定された `build_oracle_review_standard` の正本を直接読む
- 隔離実行の共通仕様を確認したいときは、run isolation の仕様を直接読む
- 中断の共通動作を確認したいときは、subcommand interruption の仕様を直接読む
- 実装ファイルや自動生成 `INDEX.md` のレビューを行うとき

## hash
- 82712e15416ae7100a74de6fb79210b7e9fb4257b18e065ae5d1cf1dce9132cf

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
- 日本語の技術文書として、realization refactor fork の目的、refactor state の管理、current fork の unresolved target、処理ループ、完了・中断・エラー、report と join 後 hook の契約を定義する正本仕様。realization refactor fork の挙動や lifecycle、状態同期、所見処理、終了判定を確認する入口。

## Read this when
- realization refactor fork の実装、状態同期、調査対象選択、処理単位の commit、完了判定、ユーザー中断、エラー処理を確認・変更するとき。
- fork report、終了 log、completion_reason、unresolved target の扱い、または join 後の共通 lifecycle との関係を確認するとき。

## Do not read this when
- 短い変更ループを担う realization apply の仕様だけを確認するとき。
- 一般的な oracle／realization の定義や INDEX.md のルーティング規則だけを確認するときは、より上位の共通仕様を読む。
- 実装やテストの具体的な配置・責務だけを確認したいときは、対応する設計・テスト規則や realization ファイルを直接読む。

## hash
- 3ee8ab0708cd57acb13ec268588665960a60a36719b46dbd152111f63894b086

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
- session join コマンドの責務、引数なしの前提、セッション状態・ブランチ・未コミット差分の事前検証、home branch への no-ff merge、conflict 解消、状態更新と安全な後始末を定義する仕様書。session join の実装、挙動確認、conflict 対応、セッション完了処理を調べる際の入口。

## Read this when
- `cmoc session join` の実装や CLI 挙動を確認するとき
- session の完了、home branch への merge、merge conflict の処理を確認するとき
- session state の joined 遷移や session branch の安全な削除条件を確認するとき

## Do not read this when
- 汎用的な git merge wrapper の仕様や repository default branch の扱いだけを確認したいとき
- session join 以外の session サブコマンドの仕様を確認するとき
- repository-local feedback state の独立した管理・集計仕様を確認するとき

## hash
- 56f8d25fd0a1f2bc7d17700b7564a2c370d4c2726a46546cda8b7706ef5dc1c4

# `tui.md`

## Summary
- `cmoc tui` は、cmoc 固有の契約と適用条件付きの基本規範をユーザープロンプトへ注入し、固定起動パラメータで AI Agent CLI/TUI を直接起動するサブコマンド。プロンプト編集、起動前処理、共通規範、feedback・通知、Codex CLI 固有設定の入口を担う。

## Read this when
- `cmoc tui` の実行手順、プロンプト skeleton の構築・編集・確定、または AI Agent CLI/TUI の起動条件を確認するとき。
- cmoc 固有規範の固定注入、model class・reasoning effort・file access mode、Structured Output の扱いを確認するとき。
- Codex CLI バックエンドでの起動コマンド、`$CODEX_HOME`、preflight validation、CLI 引数による設定上書きを確認するとき。

## Do not read this when
- プロンプトエディタの入力仕様だけを確認するときは、本文が示す prompt editor input の正本を直接読む。
- indexing preflight、feedback observation、Windows toast 通知の詳細だけを確認するときは、本文が示す各専用の正本を直接読む。
- `cmoc tui` 以外のサブコマンドの実装や起動契約だけを確認するとき。

## hash
- cd20c3f389050775bff6007054a381fc5ff187d203f93ecc5d6d0dafb41b1c3c
