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
- 人間対応が必要なフィードバックだけを検証し、正常な active state と Markdown report を publication する `cmoc feedback report` の正本仕様。pending observation の固定、重複排除・集約、normalization と verification、正常 publication、`incomplete` 診断、再開・中断、cleanup、終了コードまでを定義する。feedback report の処理順序、候補の判定、report 内容、state 遷移を確認する入口。

## Read this when
- `cmoc feedback report` の CLI 契約、事前条件、処理順序、state publication、終了コードを実装・レビューするとき
- feedback observation や feedback state と連携する処理の挙動、verification verdict、正常 report と `incomplete` report の違いを確認するとき
- 中断後の再開、`inconclusive` 後の再実行、cleanup recovery の仕様を確認するとき

## Do not read this when
- raw observation の schema や記録規則だけを確認する場合は feedback observation の正本を読む
- state、checkpoint、current pointer、publication、cleanup の永続化規則だけを確認する場合は feedback state の正本を直接読む
- normalization または verification agent の prompt・Structured Output schema を確認する場合は、それぞれの実装・schema 正本を直接読む
- `cmoc feedback report` 以外のサブコマンドの契約や一般的な割り込み規則だけを確認する場合

## hash
- 548db3cc149293086029cd4c400d06c0ca29a00fe95de6a3e4fa3c321c4147c4

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
- oracle file を編集する `cmoc oracle edit` サブコマンドの正本仕様。目的、ユーザー指示の入力経路、起動前条件、TUI 起動パラメータ、実行順序、編集境界、終了時の差分保持、中断・排他制御、ログ方針を定める。サブコマンドの実装や関連するプロンプト生成・doctor・indexing・Codex CLI 連携の入口となる。

## Read this when
- `cmoc oracle edit` の挙動、引数、実行順序、終了条件を確認するとき
- oracle file を編集する TUI の起動条件、起動パラメータ、編集権限を実装・変更するとき
- TUI 終了後の未コミット差分、indexing、branch・worktree・session state の扱いを確認するとき
- oracle edit 固有の中断、排他制御、ログ、feedback の責務を確認するとき

## Do not read this when
- realization file の通常編集や `cmoc oracle investigation` の権限を確認するとき
- プロンプト入力形式そのものの詳細を確認するときは、指定された prompt editor input の正本を直接読む
- doctor preprocess、indexing、Windows toast、Codex CLI 実行規則など個別機能の詳細仕様を確認するときは、各機能の正本を直接読む

## hash
- 64ed9944a0db51b73cf6716d01dd3e193b2c90164720a96215c4c019855e98e2

# `oracle_investigation.md`

## Summary
- エディタから受け取った oracle file 調査指示を完全プロンプトへ組み込み、Codex CLI の TUI を起動するサブコマンドの仕様を扱う。oracle file の調査フロー、入力編集、起動パラメータ、調査結果と変更の扱いを確認するための入口である。

## Read this when
- oracle file を根拠に調査するサブコマンドの挙動や実行手順を確認するとき
- エディタ入力から調査用 TUI 起動までのプロンプト構築契約を確認するとき
- oracle file と realization file の読み書き制約、調査結果の扱いを確認するとき

## Do not read this when
- oracle file の内容そのものを調査するとき
- プロンプト編集機構や起動パラメータの実装詳細を直接確認するとき
- oracle file の調査を伴わない別のサブコマンドの仕様を確認するとき

## hash
- f4c19cf7e8fd5019ff0f12a59f12ad199d8a530c21c62b66bc7b933c17c7b257

# `oracle_review.md`

## Summary
- `cmoc oracle review` サブコマンドの正本仕様。oracle のレビュー範囲、所見の列挙・統合・検証・採否判定、隔離実行、割り込み処理、および Markdown レポート生成の責務と手順を定義する。oracle の整合性や明白な誤りをレビューし、結果を人間へ報告する処理の入口となる。

## Read this when
- oracle file のレビュー処理、レビュー範囲（セッション／全体）、所見の重大度や採否基準を確認するとき
- 所見の列挙・マージ・検証・判定を行う agent call の責務や反復条件を確認するとき
- レビューの中断処理、隔離実行、またはレポートの体裁・保存方法を変更するとき

## Do not read this when
- oracle review の実装詳細だけを確認する場合
- レビュー結果をもとに oracle file 自体を修正する場合
- 自動生成される INDEX.md の内容や一般的なレビュー手法だけを確認する場合

## hash
- 3d3af739d12e1cce2c7ba68739dd4607588a081461f8a7db0052875c4b77951f

# `realization_apply.md`

## Summary
- realization apply fork の目的、追従対象となる oracle file 差分、単一の Codex agent call による realization file 反映、後処理と fork report、join 後 hook を定めるサブコマンド仕様。realization apply の fork lifecycle や実行手順を確認する入口であり、共通 lifecycle の詳細は編集 run 仕様へ委譲する。

## Read this when
- realization apply fork の引数、追従対象差分、agent call の実行条件、file access mode、実行手順、エラー処理、report、join 後 hook を確認するとき
- realization apply fork の挙動変更や、関連する oracle file と realization file の適合性を調査するとき

## Do not read this when
- fork・join・abandon に共通する lifecycle の詳細だけを確認するときは、共通の編集 run 仕様を直接読む
- ファイル単位の網羅的な realization 追従や refactor の方針を確認するときは、realization refactor の仕様を直接読む
- feedback の共通収集・保存規則だけを確認するときは、feedback 仕様を直接読む

## hash
- e5a17052c2aa0756da0cf25cd1ff6899a42d012d9c1ee2b1283632364d896e25

# `realization_refactor.md`

## Summary
- realization refactor fork の目的、refactor state の保存・同期、current fork の unresolved target、調査ループ、完了条件、中断・エラー処理、report 生成を定義する正本仕様。realization file の追従調査を繰り返す workload の入口。

## Read this when
- realization refactor fork の挙動、引数、想定内差分、state schema、entry 同期を確認するとき
- 調査対象の選択、処理単位、変更検証、unresolved target の扱いを確認するとき
- natural_completion、completed_with_unresolved、user_interruption、error の完了・終了条件を確認するとき
- fork report、終了 log、終了コード、join 後 hook の仕様を確認するとき

## Do not read this when
- 短い変更ループを担う realization apply の仕様だけを確認するとき
- fork・join・abandon に共通する lifecycle の詳細だけを確認するときは、共通 lifecycle の正本を直接読むとき
- oracle file に対する realization file の適合性基準だけを確認するときは、適合性の正本を直接読むとき
- 割り込みの共通動作だけを確認するときは、subcommand interruption の正本を直接読むとき

## hash
- 7849e81efbc99e625fe43bbaaadc0816eb20bcd0e6ab9093405e74d437d6aee8

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
- `cmoc session join` のセッション完了処理を定義する仕様。現在のセッションブランチと状態を検証し、ホームブランチへマージし、必要に応じて競合解消・状態更新・ブランチ削除を行う一連の責務を扱う。セッション join の引数、事前条件、マージ手順、競合解消、feedback state の境界を確認する必要がある場合の入口となる。

## Read this when
- `cmoc session join` の動作、引数、事前条件、実行順序を実装または確認するとき
- セッションブランチをホームブランチへマージする処理を変更するとき
- merge conflict の解消手順や oracle file の扱いを確認するとき
- session state の更新やセッションブランチ削除条件を確認するとき
- repository-local feedback state を session join の対象外として扱う境界を確認するとき

## Do not read this when
- 通常の git branch 間 merge wrapper の仕様を確認したいとき
- session の作成、実行、状態管理のうち join 処理以外を確認したいとき
- feedback state 自体の生成・集約・報告仕様を確認したいとき
- 一般的な oracle file 編集や realization refactor の規則だけを確認したいとき

## hash
- 890046a7082a55da8b4afa5a7bd132a63ddcb2afc6021743bd9603f3c6206021

# `tui.md`

## Summary
- `cmoc tui` サブコマンドの正本仕様。ユーザープロンプトへの固定規範・契約の注入、エディタによる完全プロンプト確定、固定パラメータでの AI Agent CLI/TUI 起動手順を定義する。共通バックエンド規則と Codex CLI 固有の起動条件の入口となる。

## Read this when
- `cmoc tui` の引数、事前条件、実行手順、プロンプト編集フローを確認するとき
- AI Agent CLI/TUI に注入される cmoc 固有規範、モデル設定、ファイルアクセス、Structured Output、indexing・feedback・通知の起動条件を確認するとき
- Codex CLI バックエンドの起動コマンド、環境変数、preflight、引数による設定上書きを確認するとき

## Do not read this when
- プロンプト編集の詳細仕様だけを確認したい場合は、本文から参照される prompt editor input の正本を直接読むとき
- oracle file と realization file の一般的な責務や oracle review の成立条件だけを確認したい場合は、本文から参照される各正本仕様を直接読むとき
- `cmoc tui` 以外のサブコマンドや、builder 内部の実装詳細だけを調べるとき

## hash
- 7b3ddf391d97c35b5ed27eccedce59e66d13e19dc5255a905172ae2bb898c6b3
