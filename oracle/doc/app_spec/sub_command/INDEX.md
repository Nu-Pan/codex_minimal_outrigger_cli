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
- 編集 run を開始する workload 固有 fork と、`cmoc run join` / `cmoc run abandon` による終了 lifecycle の共通仕様を定義する正本文書。
- session 単位の同時実行制約、fork・join・abandon の事前条件、state 管理、差分検査、merge、cleanup、report 要件を扱う。
- 編集 run lifecycle の実装・レビューでは本書を入口として参照し、workload 固有仕様や session lifecycle の確認はそれぞれの正本文書へ進む。

## Read this when
- realization apply/refactor の fork、run join、run abandon の挙動を実装・変更・レビューするとき
- 編集 run の state、branch/worktree、想定内差分、merge conflict、cleanup、report 形式を確認するとき
- 複数の編集 run の同時実行境界や fork 共通処理を確認するとき

## Do not read this when
- `cmoc session join` や `cmoc session abandon` など外側の session lifecycle だけを扱うとき
- `cmoc oracle edit`、read-only investigation/review、cmoc の機械的更新だけを扱うとき
- workload 固有の編集内容や join 後 hook の詳細だけを確認するときは、対応する workload 固有仕様を直接読む

## hash
- 76969e326f23fb26b657950058ecd8d28206799f0c14986258f9627523c9a85e

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
- `cmoc oracle edit` の目的、入力、TUI 起動前条件・パラメータ、実行順序、編集境界、終了時の差分維持、中断・ログ方針を定義するサブコマンド仕様。oracle file を直接編集するフローの入口。

## Read this when
- `cmoc oracle edit` の実装、起動条件、Codex CLI TUI へのパラメータ受け渡しを確認するとき
- oracle file 編集時の agent 権限、worktree・branch・未コミット差分の制約を確認するとき
- TUI 終了後の差分、indexing、commit・rollback 等の扱いを確認するとき

## Do not read this when
- realization file の編集や通常の編集 run の lifecycle を調べるとき
- oracle investigation の権限や挙動を調べるとき
- Codex CLI の一般的な起動規則だけを確認するときは、参照されている共通仕様を直接読む

## hash
- 1c8a30c9c5f0717b6e1d66c5617484e034b6850477d09395288aebc325465624

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
- `cmoc oracle review` の正本仕様。oracle ファイルを対象に、隔離実行・所見列挙/統合/検証/採否判定を経て Markdown レポートを生成する CLI サブコマンドの責務、前提条件、スコープ、割り込み、出力形式を定義する。

## Read this when
- oracle の致命的問題レビュー、`cmoc oracle review` の実行条件・処理ループ・agent call・所見判定を確認するとき
- oracle review レポートの frontmatter、本文構成、所見の分類・表示順、保存先を確認するとき
- レビュー対象範囲、隔離実行、ユーザー中断時の確定結果の扱いを確認するとき

## Do not read this when
- INDEX.md の更新方法や一般的なルーティング規則だけを確認したいとき
- oracle review 以外のサブコマンドの仕様を確認したいとき
- 実装詳細や個別 agent call builder の本文を直接確認する必要があるときは、対応する実装・正本 builder を読む

## hash
- 6e7224ec0ab34ebd47c51fd7a750826e289406794645750a37d84249d9d84561

# `realization_apply.md`

## Summary
- realization apply fork の目的・追従対象差分・agent call 実行・変更検査・run lifecycle・report・エラー処理・join 後 hook を定義する仕様書。realization apply fork の実装や運用フローを確認する入口。

## Read this when
- realization apply fork の開始条件、差分の始点・終点、oracle file の追従範囲を確認するとき
- agent call の実行条件、file access mode、変更後の検査・commit、run state を確認するとき
- fork report の形式・保存先・終了コード、join 後の session 更新を確認するとき

## Do not read this when
- fork・join・abandon に共通する lifecycle の詳細だけを確認したいときは、指定された editing_run.md を読む
- ファイル単位の網羅的な realization 追従や refactor の方針を確認したいとき
- INDEX.md の生成方法そのものを確認したいとき

## hash
- d85d5413e8a956a89e078695cd555fad907a5b5762693d007f0dc5dde28428f6

# `realization_refactor.md`

## Summary
- realization refactor fork の目的、状態管理、調査ループ、完了・中断・エラー処理、レポート生成を定義する正本仕様。oracle file と realization file の追従調査を current fork 単位で管理し、未解決 target を次回 fork へ引き継がない境界を示す。

## Read this when
- realization refactor fork のライフサイクル、state.json の同期、調査対象選択、agent call の処理単位、unresolved target、完了判定を実装・変更・レビューするとき。
- fork report、終了コード、ユーザー中断、その他のエラー、join 後の動作を確認するとき。

## Do not read this when
- 短い変更ループを担う realization apply の仕様だけを確認するとき。
- 共通の fork・join・abandon lifecycle の一般仕様だけを確認するときは、共通 lifecycle の正本仕様を直接読む。
- Codex agent call の一般的な事後条件や実行規則だけを確認するときは、Codex exec の正本仕様を直接読む。

## hash
- 9ac7f96eca7d16d0d4712976e95bb8e540cb6783af901a42589abbd2532db87f

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
- `cmoc session join` の仕様を定義する正本ドキュメント。session branch の状態・未コミット差分などの事前条件、home branch への merge、conflict 解消、session state 更新、branch 削除条件を扱う。session join の挙動や実装条件を確認する際の入口。

## Read this when
- `cmoc session join` の引数、事前検証、merge 手順、後始末を確認するとき
- home branch が session 作成後に進んだ場合の扱いや merge conflict の解消手順を確認するとき
- session branch の削除条件や想定外エラー時の扱いを確認するとき

## Do not read this when
- session join 以外の session サブコマンドの仕様を確認するとき
- 通常の git branch 間 merge や repository default branch の一般的な扱いを確認するとき
- conflict 解消用 agent call の詳細なパラメータ仕様を確認するときは、専用の正本仕様を直接読む

## hash
- 11aa2971553013657e02052b2a4184d319ac9a3358b96460cc3f142a13b4a74b

# `tui.md`

## Summary
- `cmoc tui` サブコマンドの責務・引数・実行手順・TUI 起動契約を定義する正本仕様。プロンプト編集、固定規範の注入、バックエンド共通設定、Codex CLI 固有設定の確認入口となる。

## Read this when
- `cmoc tui` の起動フローやプロンプト編集仕様を確認するとき
- TUI 起動パラメータ、注入する cmoc 規範、モデル・推論・権限設定を変更または確認するとき
- Codex CLI 起動時の環境変数、preflight、引数上書き仕様を確認するとき

## Do not read this when
- `cmoc tui` 以外のサブコマンドの仕様だけを確認するとき
- エディタ入力の詳細仕様そのものを確認するときは、指定された `prompt_editor_input.md` を直接読む
- Codex CLI の実行規則全体を確認するときは、指定された `codex_exec_rule.md` を直接読む

## hash
- 64d50ee80bdaea88d81b3a78d714a3d0174ce9787dda0cc8d089fd3752bd1b45
